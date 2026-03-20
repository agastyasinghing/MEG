"""
Whale trap detector — detects pump-and-exit pattern (PRD §9.4.2).

Detection flow:
  SignalEvent.triggering_wallet
       │
       ▼
  Query Trade table: most recent BUY by this wallet in this market
       │
       ▼
  Query Trade table: all SELLs by this wallet in same market within trap_window
       │
       ▼
  total_sold >= entry_size * trap_exit_threshold?
       │                    │
       NO → safe            YES → TRAP DETECTED
                              ├── INSERT whale_trap_events (DB)
                              ├── PUBLISH wallet_penalty (Redis)
                              └── trap_count >= manipulator_threshold?
                                    └── YES → PUBLISH manipulator flag

Write scope: trap_detector owns whale_trap_events table only.
Wallet score penalty is published to CHANNEL_WALLET_PENALTIES for
wallet_registry (data_layer) to apply — clean layer ownership.

NOTE: Implement with Opus + ultrathink. False negatives = following manipulators.
"""
from __future__ import annotations

import json
import time

import structlog
from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import AlertMessage, RedisKeys, SignalEvent
from meg.db.models import Trade, WhaleTrapEvent

logger = structlog.get_logger(__name__)


async def check(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
    session: AsyncSession,
) -> tuple[bool, str]:
    """
    Return (False, "") if no trap detected (trade is safe to proceed).
    Return (True, reason) if a whale trap pattern is detected.

    Fail-open on DB errors: log + return (False, "") — never block
    a legitimate signal because of a transient DB issue.
    """
    try:
        return await _detect_trap(signal, redis, config, session)
    except Exception:
        logger.error(
            "trap_detector.check_error",
            signal_id=signal.signal_id,
            wallet=signal.triggering_wallet,
            exc_info=True,
        )
        return False, ""


async def _detect_trap(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
    session: AsyncSession,
) -> tuple[bool, str]:
    """Core trap detection logic — separated for testability."""
    wallet = signal.triggering_wallet
    market_id = signal.market_id
    agent_cfg = config.agent

    # 1. Find the triggering wallet's most recent entry trade in this market
    #    Filter by signal's outcome (the entry side, not the exit side)
    entry_trade = await _get_entry_trade(wallet, market_id, signal.outcome, session)
    if entry_trade is None:
        # No trade found — can't detect trap without an entry reference
        return False, ""

    entry_size = float(entry_trade.size_usdc)
    entry_time = entry_trade.traded_at

    # 2. Find all exits (opposite-direction trades) within the trap window
    opposite_outcome = "NO" if entry_trade.outcome == "YES" else "YES"
    from datetime import timedelta

    window_start = entry_time
    window_end = entry_time + timedelta(minutes=agent_cfg.trap_window_minutes)

    recent_sells = await _get_sells_in_window(
        wallet, market_id, opposite_outcome, window_start, window_end, session
    )

    total_sold = sum(float(t.size_usdc) for t in recent_sells)

    # 3. Compare against threshold
    if total_sold < entry_size * agent_cfg.trap_exit_threshold:
        return False, ""

    # TRAP DETECTED
    confidence = min(total_sold / entry_size, 1.0) if entry_size > 0 else 0.0
    time_delta_ms = None
    if recent_sells:
        last_sell_time = max(t.traded_at for t in recent_sells)
        time_delta_ms = int((last_sell_time - entry_time).total_seconds() * 1000)

    # 4. Write whale_trap_events record
    trap_event = WhaleTrapEvent(
        wallet_address=wallet,
        market_id=market_id,
        pump_size_usdc=entry_size,
        exit_size_usdc=total_sold,
        time_between_ms=time_delta_ms,
        confidence_score=confidence,
        notes=f"Signal {signal.signal_id}: sold {total_sold:.2f} of {entry_size:.2f} within {agent_cfg.trap_window_minutes}min",
    )
    session.add(trap_event)
    await session.flush()

    # 5. Publish penalty event to Redis (wallet_registry applies it)
    penalty_event = {
        "wallet_address": wallet,
        "penalty": agent_cfg.trap_score_penalty,
        "reason": "whale_trap_detected",
        "signal_id": signal.signal_id,
        "market_id": market_id,
        "timestamp_ms": int(time.time() * 1000),
    }
    await redis.publish(
        RedisKeys.CHANNEL_WALLET_PENALTIES,
        json.dumps(penalty_event),
    )

    # 6. Check if wallet should be flagged as MANIPULATOR
    trap_count = await _get_trap_count(wallet, session)
    if trap_count >= agent_cfg.trap_manipulator_threshold:
        manipulator_event = {
            "wallet_address": wallet,
            "flag": "MANIPULATOR",
            "trap_count": trap_count,
            "reason": f"trap_count {trap_count} >= threshold {agent_cfg.trap_manipulator_threshold}",
            "timestamp_ms": int(time.time() * 1000),
        }
        await redis.publish(
            RedisKeys.CHANNEL_WALLET_PENALTIES,
            json.dumps(manipulator_event),
        )
        logger.warning(
            "trap_detector.manipulator_flagged",
            wallet=wallet,
            trap_count=trap_count,
        )

    reason = (
        f"whale_trap: {wallet[:10]}... sold {total_sold:.0f} USDC "
        f"({confidence:.0%} of entry) within {agent_cfg.trap_window_minutes}min"
    )
    logger.warning(
        "trap_detector.trap_detected",
        wallet=wallet,
        market_id=market_id,
        signal_id=signal.signal_id,
        entry_size=entry_size,
        total_sold=total_sold,
        confidence=confidence,
    )

    # Alert operators — trap warning is URGENT (PRD §9.6: alert #2)
    try:
        await redis.publish(
            RedisKeys.CHANNEL_BOT_ALERTS,
            AlertMessage(
                alert_type="trap",
                message=(
                    f"🪤 Whale trap detected on signal {signal.signal_id[:8]}…\n"
                    f"Market: {market_id}\n"
                    f"Wallet: {wallet[:10]}…\n"
                    f"Sold {total_sold:.0f} USDC ({confidence:.0%} of entry) "
                    f"within {agent_cfg.trap_window_minutes}min.\n"
                    f"Proposal still sent — operator decides (PRD §9.4.2)."
                ),
                urgent=True,
            ).model_dump_json(),
        )
    except Exception:
        logger.error("trap_detector.alert_publish_failed", exc_info=True)

    return True, reason


async def _get_entry_trade(
    wallet: str, market_id: str, outcome: str, session: AsyncSession
) -> Trade | None:
    """Get the most recent trade by this wallet matching the signal's outcome."""
    result = await session.execute(
        select(Trade)
        .where(
            Trade.wallet_address == wallet,
            Trade.market_id == market_id,
            Trade.outcome == outcome,
        )
        .order_by(Trade.traded_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def _get_sells_in_window(
    wallet: str,
    market_id: str,
    outcome: str,
    window_start,
    window_end,
    session: AsyncSession,
) -> list[Trade]:
    """Get all trades by wallet in the given outcome within the time window."""
    result = await session.execute(
        select(Trade).where(
            Trade.wallet_address == wallet,
            Trade.market_id == market_id,
            Trade.outcome == outcome,
            Trade.traded_at >= window_start,
            Trade.traded_at <= window_end,
        )
    )
    return list(result.scalars().all())


async def _get_trap_count(wallet: str, session: AsyncSession) -> int:
    """Count total whale trap events for this wallet."""
    result = await session.execute(
        select(func.count(WhaleTrapEvent.id)).where(
            WhaleTrapEvent.wallet_address == wallet
        )
    )
    return result.scalar_one()
