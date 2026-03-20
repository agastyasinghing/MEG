"""
Position manager — tracks open positions, monitors TP/SL/whale exit, daily PnL.

Dual-write pattern (Redis-first, DB second — matches wallet_registry):
  1. Write to Redis (real-time state for risk_controller)
  2. Write to DB (persistence for dashboard, restart recovery)
  3. If DB write fails: log warning, continue (Redis is authoritative for runtime)

Redis state:
  meg:open_positions          — HASH: field=position_id, value=PositionState JSON
  position:{id}               — STRING: PositionState JSON (direct lookup)
  market:{id}:exposure_usdc   — STRING: total USDC deployed in this market
  meg:daily_pnl_usdc          — STRING: running P&L for current UTC day
  meg:portfolio_value_usdc    — STRING: current portfolio value

Monitor loop (asyncio.Task):
  TP/SL check:    every 30 seconds  (Redis reads only — cheap)
  Whale exit check: every 5 minutes  (DB queries — heavier)
  Daily PnL reset:  midnight UTC     (Redis SET to "0")

Position lifecycle (v1):
  ┌───────────┐   operator    ┌──────┐   TP/SL/whale   ┌───────────────┐
  │ PENDING_  │──approves──►│ OPEN │──exit flagged──►│ alert logged  │
  │ APPROVAL  │              └──────┘   (structlog)    │ (human exits) │
  └───────────┘                                        └───────────────┘
"""
from __future__ import annotations

import asyncio
import json
import time
import uuid
from datetime import datetime, timedelta, timezone

import structlog
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import AlertMessage, PositionState, RedisKeys
from meg.db.models import Position, PositionStatus, Trade

logger = structlog.get_logger(__name__)

# ── Module-level constants ────────────────────────────────────────────────────

_MONITOR_INTERVAL_SECONDS = 30
_WHALE_EXIT_CHECK_INTERVAL_SECONDS = 300  # 5 minutes


# ── CRUD operations ──────────────────────────────────────────────────────────


async def open_position(
    *,
    market_id: str,
    outcome: str,
    size_usdc: float,
    entry_price: float,
    signal_id: str,
    contributing_wallets: list[str],
    whale_archetype: str,
    saturation_score: float,
    take_profit_price: float,
    stop_loss_price: float,
    redis: Redis,
    session: AsyncSession | None = None,
) -> PositionState:
    """
    Record a new open position. Redis-first, then DB.

    Returns the created PositionState. Logs warning if position_id already
    exists in Redis (duplicate open — skips write).
    """
    position_id = f"meg_pos_{uuid.uuid4().hex[:12]}"
    now_ms = int(time.time() * 1000)
    shares = size_usdc / entry_price if entry_price > 0 else 0.0

    pos = PositionState(
        position_id=position_id,
        market_id=market_id,
        outcome=outcome,
        entry_price=entry_price,
        current_price=entry_price,
        size_usdc=size_usdc,
        shares=shares,
        entry_signal_id=signal_id,
        contributing_wallets=contributing_wallets,
        whale_archetype=whale_archetype,
        opened_at_ms=now_ms,
        take_profit_price=take_profit_price,
        stop_loss_price=stop_loss_price,
        saturation_score_at_entry=saturation_score,
        status="OPEN",
    )

    # Check duplicate
    exists = await redis.hexists(RedisKeys.open_positions(), position_id)
    if exists:
        logger.warning("position_manager.duplicate_open", position_id=position_id)
        return pos

    # Redis-first write
    pos_json = pos.model_dump_json()
    pipe = redis.pipeline()
    pipe.hset(RedisKeys.open_positions(), position_id, pos_json)
    pipe.set(RedisKeys.position(position_id), pos_json)
    pipe.incrbyfloat(RedisKeys.market_exposure_usdc(market_id), size_usdc)
    await pipe.execute()

    # DB write (best-effort)
    if session is not None:
        try:
            db_pos = Position(
                position_id=position_id,
                market_id=market_id,
                outcome=outcome,
                entry_price=entry_price,
                current_price=entry_price,
                size_usdc=size_usdc,
                shares=shares,
                unrealized_pnl_usdc=0.0,
                unrealized_pnl_pct=0.0,
                entry_signal_id=signal_id,
                contributing_wallets=contributing_wallets,
                whale_archetype=whale_archetype,
                take_profit_price=take_profit_price,
                stop_loss_price=stop_loss_price,
                saturation_score_at_entry=saturation_score,
                status=PositionStatus.OPEN,
            )
            session.add(db_pos)
            await session.flush()
        except Exception:
            logger.warning(
                "position_manager.db_write_failed",
                position_id=position_id,
                exc_info=True,
            )

    logger.info(
        "position_manager.opened",
        position_id=position_id,
        market_id=market_id,
        outcome=outcome,
        size_usdc=size_usdc,
        entry_price=entry_price,
    )
    return pos


async def close_position(
    position_id: str,
    exit_price: float,
    redis: Redis,
    session: AsyncSession | None = None,
) -> dict:
    """
    Close a position. Calculates realized PnL, updates Redis + DB.

    Returns a PnL summary dict:
      {"position_id", "market_id", "realized_pnl_usdc", "realized_pnl_pct"}

    Raises ValueError if position not found in Redis.
    """
    raw = await redis.hget(RedisKeys.open_positions(), position_id)
    if raw is None:
        raise ValueError(f"Position {position_id} not found in open_positions")

    pos = PositionState.model_validate_json(raw)

    # Calculate P&L
    if pos.outcome == "YES":
        pnl_per_share = exit_price - pos.entry_price
    else:
        pnl_per_share = pos.entry_price - exit_price

    realized_pnl_usdc = pnl_per_share * pos.shares
    realized_pnl_pct = (
        pnl_per_share / pos.entry_price if pos.entry_price > 0 else 0.0
    )

    # Redis cleanup
    pipe = redis.pipeline()
    pipe.hdel(RedisKeys.open_positions(), position_id)
    pipe.delete(RedisKeys.position(position_id))
    pipe.incrbyfloat(RedisKeys.daily_pnl_usdc(), realized_pnl_usdc)
    pipe.incrbyfloat(RedisKeys.market_exposure_usdc(pos.market_id), -pos.size_usdc)
    await pipe.execute()

    # DB update (best-effort)
    if session is not None:
        try:
            from sqlalchemy import update

            await session.execute(
                update(Position)
                .where(Position.position_id == position_id)
                .values(
                    status=PositionStatus.CLOSED,
                    current_price=exit_price,
                    unrealized_pnl_usdc=realized_pnl_usdc,
                    unrealized_pnl_pct=realized_pnl_pct,
                    resolved_pnl_usdc=realized_pnl_usdc,
                    closed_at=datetime.now(tz=timezone.utc),
                )
            )
            await session.flush()
        except Exception:
            logger.warning(
                "position_manager.db_close_failed",
                position_id=position_id,
                exc_info=True,
            )

    summary = {
        "position_id": position_id,
        "market_id": pos.market_id,
        "realized_pnl_usdc": realized_pnl_usdc,
        "realized_pnl_pct": realized_pnl_pct,
    }
    logger.info("position_manager.closed", **summary)

    # Alert operators with P&L result (PRD §9.6: alert #6)
    pnl_sign = "+" if realized_pnl_usdc >= 0 else ""
    try:
        await redis.publish(
            RedisKeys.CHANNEL_BOT_ALERTS,
            AlertMessage(
                alert_type="position_closed",
                message=(
                    f"📊 Position closed: {pos.market_id}\n"
                    f"Outcome: {pos.outcome} | Size: {pos.size_usdc:.0f} USDC\n"
                    f"P&L: {pnl_sign}{realized_pnl_usdc:.2f} USDC "
                    f"({pnl_sign}{realized_pnl_pct:.1%})"
                ),
                urgent=False,
            ).model_dump_json(),
        )
    except Exception:
        logger.error(
            "position_manager.close_alert_failed",
            position_id=position_id,
            exc_info=True,
        )

    return summary


async def get_open_positions(redis: Redis) -> list[PositionState]:
    """Return all currently open positions from Redis hash."""
    raw_positions = await redis.hgetall(RedisKeys.open_positions())
    positions = []
    for pos_json in raw_positions.values():
        try:
            positions.append(PositionState.model_validate_json(pos_json))
        except Exception:
            logger.warning(
                "position_manager.invalid_position_json",
                raw=pos_json[:200] if isinstance(pos_json, (str, bytes)) else str(pos_json)[:200],
            )
    return positions


async def get_total_exposure_usdc(redis: Redis) -> float:
    """Return total capital currently deployed across all open positions."""
    positions = await get_open_positions(redis)
    return sum(p.size_usdc for p in positions)


async def get_market_exposure_usdc(market_id: str, redis: Redis) -> float:
    """Return total capital deployed in a specific market."""
    val = await redis.get(RedisKeys.market_exposure_usdc(market_id))
    if val is None:
        return 0.0
    return float(val)


async def get_daily_pnl_usdc(redis: Redis) -> float:
    """Return net P&L for today. Used by risk_controller daily loss gate."""
    val = await redis.get(RedisKeys.daily_pnl_usdc())
    if val is None:
        return 0.0
    return float(val)


async def get_portfolio_value_usdc(redis: Redis, config: MegConfig) -> float:
    """
    Return current portfolio value. Falls back to config default if not
    yet initialized in Redis.
    """
    val = await redis.get(RedisKeys.portfolio_value_usdc())
    if val is None:
        return config.kelly.portfolio_value_usdc
    return float(val)


# ── Monitor loop ──────────────────────────────────────────────────────────────


async def monitor_positions(
    redis: Redis,
    config: MegConfig,
    session: AsyncSession | None = None,
) -> None:
    """
    Long-running monitor loop. Checks TP/SL every 30s, whale exits every 5min.

    In v1, all flags are logged via structlog (Telegram integration in Phase 8).
    No auto-exit — operator decides via Telegram approval flow.
    """
    iteration = 0
    while True:
        try:
            check_whale_exit = (
                iteration % (_WHALE_EXIT_CHECK_INTERVAL_SECONDS // _MONITOR_INTERVAL_SECONDS) == 0
            )
            await _check_all_positions(redis, config, session, check_whale_exit)
        except Exception:
            logger.error("position_manager.monitor_error", exc_info=True)

        iteration += 1
        await asyncio.sleep(_MONITOR_INTERVAL_SECONDS)


async def _check_all_positions(
    redis: Redis,
    config: MegConfig,
    session: AsyncSession | None = None,
    check_whale_exit: bool = False,
) -> None:
    """
    Single pass over all open positions. Updates unrealized PnL,
    checks TP/SL thresholds, optionally checks whale exits.

    Per-position errors are caught and logged — one bad position
    never crashes monitoring for all others.
    """
    positions = await get_open_positions(redis)
    if not positions:
        return

    for pos in positions:
        try:
            await _check_single_position(redis, config, pos, session, check_whale_exit)
        except Exception:
            logger.error(
                "position_manager.position_check_error",
                position_id=pos.position_id,
                exc_info=True,
            )


async def _check_single_position(
    redis: Redis,
    config: MegConfig,
    pos: PositionState,
    session: AsyncSession | None = None,
    check_whale_exit: bool = False,
) -> None:
    """Check a single position for TP/SL/whale exit and update unrealized PnL."""
    # Read current price
    mid_raw = await redis.get(RedisKeys.market_mid_price(pos.market_id))
    if mid_raw is None:
        return  # No price data — skip this iteration

    current_price = float(mid_raw)

    # Update unrealized PnL
    if pos.outcome == "YES":
        pnl_per_share = current_price - pos.entry_price
    else:
        pnl_per_share = pos.entry_price - current_price

    unrealized_pnl_usdc = pnl_per_share * pos.shares
    unrealized_pnl_pct = (
        pnl_per_share / pos.entry_price if pos.entry_price > 0 else 0.0
    )

    # Update position state in Redis
    pos_updated = pos.model_copy(
        update={
            "current_price": current_price,
            "unrealized_pnl_usdc": unrealized_pnl_usdc,
            "unrealized_pnl_pct": unrealized_pnl_pct,
        }
    )

    # Check take-profit
    tp_config = config.position
    if pos.outcome == "YES":
        tp_hit = current_price >= pos.take_profit_price
        sl_hit = current_price <= pos.stop_loss_price
    else:
        tp_hit = current_price <= pos.take_profit_price
        sl_hit = current_price >= pos.stop_loss_price

    if tp_hit:
        logger.warning(
            "position_manager.take_profit_reached",
            position_id=pos.position_id,
            market_id=pos.market_id,
            entry_price=pos.entry_price,
            current_price=current_price,
            take_profit_price=pos.take_profit_price,
            unrealized_pnl_usdc=unrealized_pnl_usdc,
            unrealized_pnl_pct=unrealized_pnl_pct,
        )

    if sl_hit:
        logger.warning(
            "position_manager.stop_loss_reached",
            position_id=pos.position_id,
            market_id=pos.market_id,
            entry_price=pos.entry_price,
            current_price=current_price,
            stop_loss_price=pos.stop_loss_price,
            unrealized_pnl_usdc=unrealized_pnl_usdc,
            unrealized_pnl_pct=unrealized_pnl_pct,
        )

    # Trailing take-profit (wired but dormant in v1: trailing_tp_enabled=False)
    if tp_config.trailing_tp_enabled and not pos.whale_exit_detected:
        if pos.outcome == "YES":
            price_drifting = current_price > pos.entry_price * 1.005
        else:
            price_drifting = current_price < pos.entry_price * 0.995

        no_saturation = pos.saturation_score_at_entry < config.agent.saturation_threshold
        if price_drifting and no_saturation:
            new_tp = current_price * (1 - tp_config.trailing_tp_floor_pct)
            if pos.outcome == "YES" and new_tp > pos.take_profit_price:
                pos_updated = pos_updated.model_copy(
                    update={"take_profit_price": new_tp}
                )
            elif pos.outcome == "NO" and new_tp < pos.take_profit_price:
                pos_updated = pos_updated.model_copy(
                    update={"take_profit_price": new_tp}
                )

    # Check whale exit (heavier — DB queries, runs every 5 min)
    if check_whale_exit and session is not None and not pos.whale_exit_detected:
        whale_exiting = await _detect_whale_exit(pos, session)
        if whale_exiting:
            now_ms = int(time.time() * 1000)
            pos_updated = pos_updated.model_copy(
                update={
                    "whale_exit_detected": True,
                    "whale_exit_detected_at_ms": now_ms,
                }
            )
            logger.warning(
                "position_manager.whale_exit_detected",
                position_id=pos.position_id,
                market_id=pos.market_id,
                contributing_wallets=pos.contributing_wallets,
                unrealized_pnl_usdc=unrealized_pnl_usdc,
            )
            # Alert operators — whale exit is ACTION REQUIRED (PRD §9.6: alert #7)
            pnl_sign = "+" if unrealized_pnl_usdc >= 0 else ""
            try:
                await redis.publish(
                    RedisKeys.CHANNEL_BOT_ALERTS,
                    AlertMessage(
                        alert_type="whale_exit",
                        message=(
                            f"🐋 Whale exit detected: {pos.market_id}\n"
                            f"Position: {pos.outcome} {pos.size_usdc:.0f} USDC\n"
                            f"Unrealized P&L: {pnl_sign}{unrealized_pnl_usdc:.2f} USDC\n"
                            f"Whales: {', '.join(w[:10] + '…' for w in pos.contributing_wallets[:3])}\n"
                            f"Consider exiting — information edge may be dissipating."
                        ),
                        urgent=False,
                    ).model_dump_json(),
                )
            except Exception:
                logger.error(
                    "position_manager.whale_exit_alert_failed",
                    position_id=pos.position_id,
                    exc_info=True,
                )

    # Write updated state back to Redis
    updated_json = pos_updated.model_dump_json()
    await redis.hset(RedisKeys.open_positions(), pos.position_id, updated_json)
    await redis.set(RedisKeys.position(pos.position_id), updated_json)


async def _detect_whale_exit(
    pos: PositionState,
    session: AsyncSession,
) -> bool:
    """
    Check if any contributing whale has begun selling their position
    in this market since we opened ours.

    Returns True if any contributing wallet has sold in the same market
    with the opposite outcome since our entry.
    """
    if not pos.contributing_wallets:
        return False

    opened_at = datetime.fromtimestamp(pos.opened_at_ms / 1000, tz=timezone.utc)
    opposite = "NO" if pos.outcome == "YES" else "YES"

    try:
        result = await session.execute(
            select(Trade.id)
            .where(
                Trade.wallet_address.in_(pos.contributing_wallets),
                Trade.market_id == pos.market_id,
                Trade.outcome == opposite,
                Trade.traded_at >= opened_at,
            )
            .limit(1)
        )
        return result.scalar_one_or_none() is not None
    except Exception:
        logger.warning(
            "position_manager.whale_exit_query_failed",
            position_id=pos.position_id,
            exc_info=True,
        )
        return False


# ── Daily PnL reset ──────────────────────────────────────────────────────────


async def daily_pnl_reset_loop(redis: Redis) -> None:
    """
    Reset daily PnL to 0.0 at midnight UTC. Runs as a separate asyncio.Task.

    Without this reset, the circuit breaker (risk_controller Gate 2) would
    accumulate losses across days and eventually trigger permanently.
    """
    while True:
        try:
            now = datetime.now(tz=timezone.utc)
            # Seconds until next midnight UTC
            tomorrow = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            if tomorrow <= now:
                tomorrow += timedelta(days=1)
            seconds_until_midnight = (tomorrow - now).total_seconds()
            await asyncio.sleep(seconds_until_midnight)

            await redis.set(RedisKeys.daily_pnl_usdc(), "0")
            logger.info("position_manager.daily_pnl_reset")
        except Exception:
            logger.error("position_manager.daily_pnl_reset_error", exc_info=True)
            await asyncio.sleep(60)  # Retry in a minute on error
