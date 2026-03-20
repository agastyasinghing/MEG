"""
Decision agent — final gating before trade proposal (PRD §9.4.1).

Gates a signal through all agent_core risk checks before creating a
TradeProposal. In v1, all proposals require human approval via Telegram.

Decision flow:
  SignalEvent
    ↓
  Hard blocks (cheapest first, decision_agent owns these):
    • system_paused?           → Redis GET (instant emergency stop)
    • blacklisted_market?      → config list check
    • duplicate_position?      → Redis HEXISTS
    ↓
  risk_controller.check()      → 4-gate risk framework
    ↓
  trap_detector.check()        → warn-only (operator decides, PRD §9.4.2)
    ↓
  saturation_monitor.score()   → adjusts size (does NOT block)
    ↓
  clamp_position_size()        → reduce to max if oversized (PRD §10)
    ↓
  crowding_detector.check()    → blocks if entry window closed
    ↓
  TradeProposal (PENDING_APPROVAL) → published to CHANNEL_TRADE_PROPOSALS
    ↓
  UPDATE signal_outcomes status

Write responsibility:
  - decision_agent UPDATEs signal_outcomes.status (composite_scorer owns INSERT)
  - decision_agent PUBLISHes TradeProposal to CHANNEL_TRADE_PROPOSALS

NOTE: Implement with Opus + ultrathink. Decision bugs = real financial loss.
"""
from __future__ import annotations

import json
import time
import uuid

import structlog
from redis.asyncio import Redis
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from meg.agent_core import (
    crowding_detector,
    risk_controller,
    saturation_monitor,
    trap_detector,
)
from meg.core.config_loader import MegConfig
from meg.core.events import AlertMessage, RedisKeys, SignalEvent, TradeProposal
from meg.db.models import SignalOutcome

logger = structlog.get_logger(__name__)


async def evaluate(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
    session: AsyncSession,
) -> TradeProposal | None:
    """
    Run all risk gates against the signal. Return a TradeProposal if all
    gates pass, or None if any gate rejects.

    Every outcome (approve/reject/block) updates signal_outcomes.status in DB.
    """
    # ── Hard blocks (decision_agent owns these) ──────────────────────────

    # 1. Emergency pause — instant check, Redis GET
    paused = await redis.get(RedisKeys.system_paused())
    if paused is not None:
        await _update_signal_status(signal.signal_id, "BLOCKED", session)
        logger.info(
            "decision_agent.blocked",
            signal_id=signal.signal_id,
            reason="system_paused",
        )
        return None

    # 2. Blacklisted market — config list check
    if signal.market_id in config.risk.blacklisted_markets:
        await _update_signal_status(signal.signal_id, "BLOCKED", session)
        logger.info(
            "decision_agent.blocked",
            signal_id=signal.signal_id,
            reason="market_blacklisted",
            market_id=signal.market_id,
        )
        return None

    # 3. Duplicate position — same market + outcome already open
    has_dup = await _has_duplicate_position(
        signal.market_id, signal.outcome, redis
    )
    if has_dup:
        await _update_signal_status(signal.signal_id, "BLOCKED", session)
        logger.info(
            "decision_agent.blocked",
            signal_id=signal.signal_id,
            reason="duplicate_position",
            market_id=signal.market_id,
            outcome=signal.outcome,
        )
        return None

    # ── Risk controller — 5-gate framework ───────────────────────────────

    risk_passed, risk_reason = await risk_controller.check(signal, redis, config)
    if not risk_passed:
        await _update_signal_status(signal.signal_id, "REJECTED", session)
        logger.info(
            "decision_agent.rejected",
            signal_id=signal.signal_id,
            reason=risk_reason,
        )
        # Circuit breaker fires → alert operators immediately (PRD §10 URGENT)
        if risk_reason.startswith(risk_controller.CIRCUIT_BREAKER_REASON_PREFIX):
            await _publish_alert(
                redis,
                AlertMessage(
                    alert_type="circuit_breaker",
                    message=f"🛑 Circuit breaker triggered. {risk_reason}. All new signals halted. Use /resume to restart.",
                    urgent=True,
                ),
            )
        return None

    # ── Trap detector — warn-only (PRD §9.4.2: operator decides) ─────────

    trap_warning = False
    trap_detected, trap_reason = await trap_detector.check(
        signal, redis, config, session
    )
    if trap_detected:
        await _update_signal_status(signal.signal_id, "TRAP_DETECTED", session)
        trap_warning = True
        logger.warning(
            "decision_agent.trap_warning",
            signal_id=signal.signal_id,
            reason=trap_reason,
        )

    # ── Saturation monitor — size adjustment (never blocks) ──────────────

    sat_score, size_multiplier = await saturation_monitor.score(
        signal, redis, config
    )
    adjusted_size = signal.recommended_size_usdc * size_multiplier

    # ── Position size clamp (PRD §10: reduce, don't block) ───────────────

    adjusted_size = await risk_controller.clamp_position_size(
        adjusted_size, redis, config
    )

    # ── Crowding detector — entry distance gate ──────────────────────────

    crowded, crowd_reason = await crowding_detector.check(signal, redis, config)
    if crowded:
        await _update_signal_status(signal.signal_id, "BLOCKED", session)
        logger.info(
            "decision_agent.blocked",
            signal_id=signal.signal_id,
            reason=crowd_reason,
        )
        return None

    # ── All gates passed — build and publish proposal ────────────────────

    proposal = await _build_proposal(signal, adjusted_size, sat_score, trap_warning, config, redis)

    # Update signal_outcomes status — keep TRAP_DETECTED if trap was flagged
    if not trap_warning:
        await _update_signal_status(signal.signal_id, "APPROVED", session)

    # Publish proposal to Redis
    try:
        await redis.publish(
            RedisKeys.CHANNEL_TRADE_PROPOSALS,
            proposal.model_dump_json(),
        )
    except Exception:
        logger.error(
            "decision_agent.publish_failed",
            signal_id=signal.signal_id,
            proposal_id=proposal.proposal_id,
            exc_info=True,
        )

    logger.info(
        "decision_agent.proposal_created",
        signal_id=signal.signal_id,
        proposal_id=proposal.proposal_id,
        market_id=signal.market_id,
        outcome=signal.outcome,
        size_usdc=adjusted_size,
        saturation_score=sat_score,
        size_multiplier=size_multiplier,
    )

    return proposal


async def _build_proposal(
    signal: SignalEvent,
    adjusted_size_usdc: float,
    saturation_score: float,
    trap_warning: bool,
    config: MegConfig,
    redis: Redis,
) -> TradeProposal:
    """
    Construct a TradeProposal from an approved SignalEvent.

    Reads two additional Redis keys to populate operator-facing display fields:
      current_price      — live market mid-price (written by CLOBMarketFeed every 5s)
      estimated_slippage — proxy: size_usdc / liquidity_usdc, fail-closed at 1.0
                           (intentional duplication of slippage_guard.estimate_slippage()
                           formula; importing execution layer here would violate CLAUDE.md
                           no-layer-coupling rule)

    Both fields default to 0.0 / 1.0 on Redis miss (CLOBMarketFeed may not have
    polled a new market yet). A warning is logged on mid_price miss.
    """
    # Live mid-price for operator display (not used for execution — entry_filter re-checks)
    mid_raw = await redis.get(RedisKeys.market_mid_price(signal.market_id))
    if mid_raw is None:
        logger.warning(
            "decision_agent.no_mid_price_for_proposal",
            market_id=signal.market_id,
        )
    current_price = float(mid_raw) if mid_raw is not None else 0.0

    # Slippage proxy: size / liquidity (fail-closed at 1.0 when liquidity absent)
    liq_raw = await redis.get(RedisKeys.market_liquidity(signal.market_id))
    liquidity = float(liq_raw) if liq_raw else 0.0
    estimated_slippage = (
        min(adjusted_size_usdc / liquidity, 1.0) if liquidity > 0 else 1.0
    )

    return TradeProposal(
        proposal_id=f"meg_prop_{uuid.uuid4().hex[:12]}",
        signal_id=signal.signal_id,
        market_id=signal.market_id,
        outcome=signal.outcome,
        size_usdc=adjusted_size_usdc,
        limit_price=signal.market_price_at_signal,
        status="PENDING_APPROVAL",
        created_at_ms=int(time.time() * 1000),
        composite_score=signal.composite_score,
        scores=signal.scores,
        saturation_score=saturation_score,
        trap_warning=trap_warning,
        contributing_wallets=signal.contributing_wallets,
        market_price_at_signal=signal.market_price_at_signal,
        estimated_half_life_minutes=signal.estimated_half_life_minutes,
        current_price=current_price,
        estimated_slippage=estimated_slippage,
    )


async def _publish_alert(redis: Redis, alert: AlertMessage) -> None:
    """
    Publish an AlertMessage to CHANNEL_BOT_ALERTS.
    Wrapped in try/except — alert delivery failure must never crash the pipeline.
    """
    try:
        await redis.publish(RedisKeys.CHANNEL_BOT_ALERTS, alert.model_dump_json())
    except Exception:
        logger.error(
            "decision_agent.alert_publish_failed",
            alert_type=alert.alert_type,
            exc_info=True,
        )


async def _has_duplicate_position(
    market_id: str, outcome: str, redis: Redis
) -> bool:
    """Check if there's already an open position in this market + outcome."""
    raw_positions = await redis.hgetall(RedisKeys.open_positions())
    for pos_json in raw_positions.values():
        try:
            pos = json.loads(pos_json)
            if pos.get("market_id") == market_id and pos.get("outcome") == outcome:
                return True
        except (json.JSONDecodeError, TypeError):
            continue
    return False


async def _update_signal_status(
    signal_id: str,
    status: str,
    session: AsyncSession,
) -> None:
    """
    UPDATE signal_outcomes SET status = X WHERE signal_id = Y.

    Best-effort: if DB write fails, log error but don't crash the pipeline.
    The signal_outcomes row was INSERTed by composite_scorer — we only UPDATE status.
    """
    try:
        await session.execute(
            update(SignalOutcome)
            .where(SignalOutcome.signal_id == signal_id)
            .values(status=status)
        )
        await session.flush()
    except Exception:
        logger.error(
            "decision_agent.status_update_failed",
            signal_id=signal_id,
            status=status,
            exc_info=True,
        )
