"""
Risk controller — 4-gate risk framework + position size clamp.

Gates 1–4 are hard blocks: any failure immediately rejects the signal.
Position size clamping (PRD §10 Gate 2) is a separate function that
reduces oversized trades to the maximum allowed — it never blocks.

Gate order (cheapest first):
  Gate 1: Paper trading mode     — config read only (cheapest)
  Gate 2: Daily loss limit       — 1 Redis GET
  Gate 3: Max open positions     — 1 Redis HLEN
  Gate 4: Market exposure limit  — 2 Redis GETs (exposure + portfolio)

Size clamp (called separately by decision_agent after check()):
  clamp_position_size()          — 1 Redis GET (portfolio)

Gate evaluation flow:
  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Gate 1   │─►│ Gate 2   │─►│ Gate 3   │─►│ Gate 4   │─► (True, "")
  │ Paper    │  │ Daily    │  │ Max      │  │ Market   │
  │ Trading  │  │ Loss     │  │ Positions│  │ Exposure │
  └──────────┘  └──────────┘  └──────────┘  └──────────┘
       │              │              │              │
    (False,        (False,        (False,        (False,
     reason)        reason)        reason)        reason)

Missing Redis key semantics:
  - daily_pnl_usdc missing   → default 0.0 (no loss recorded yet) → PASS
  - open_positions missing    → default 0 positions                → PASS
  - market_exposure missing   → default 0.0 (no exposure)          → PASS
  - portfolio_value missing   → FAIL (cannot compute ratios safely)

NOTE: Implement with Opus + ultrathink. Risk gate bugs = real financial loss.
"""
from __future__ import annotations

import structlog
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, SignalEvent

logger = structlog.get_logger(__name__)


async def check(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """
    Run all 4 risk gates in order. Return (True, "") if all pass.
    Return (False, reason) on first failure — short-circuit, no further gates.

    Position size clamping is NOT in this function — call
    clamp_position_size() separately after check() passes.
    """
    # Gate 1: Paper trading safety check
    passed, reason = _check_paper_trading(config)
    if not passed:
        return False, reason

    # Gate 2: Daily loss circuit breaker
    passed, reason = await _check_daily_loss(redis, config)
    if not passed:
        return False, reason

    # Gate 3: Max open positions
    passed, reason = await _check_max_positions(redis, config)
    if not passed:
        return False, reason

    # Gate 4: Market exposure limit
    passed, reason = await _check_market_exposure(signal.market_id, redis, config)
    if not passed:
        return False, reason

    return True, ""


def _check_paper_trading(config: MegConfig) -> tuple[bool, str]:
    """
    Gate 1: Paper trading mode check.

    In paper mode (paper_trading=True): always PASS.
    TradeProposals still flow through the full pipeline — Telegram approval
    still runs, CLOB mock handles the no-op execution. This gate exists as a
    safety backstop for misconfigured live mode, not to block paper trading.

    In live mode (paper_trading=False): also PASS.
    This gate doesn't add live-mode-only restrictions in v1. It exists to
    document the boundary and provide a hook for v2 live-mode safety checks
    (e.g. verify wallet balance, check CLOB connection, confirm credentials).
    """
    # v1: always pass. The gate is structural — wired for v2 live-mode checks.
    return True, ""


async def _check_daily_loss(redis: Redis, config: MegConfig) -> tuple[bool, str]:
    """
    Gate 2: Circuit breaker — reject if today's cumulative loss has hit the limit.

    Reads meg:daily_pnl_usdc from Redis (written by position_manager on close).
    Missing key → 0.0 (no trades closed today, no loss).

    Comparison: if daily loss (negative PnL) exceeds the threshold, halt.
    Uses abs() because daily_pnl_usdc can be negative (loss) or positive (gain).
    Only triggers on negative PnL — gains never trigger the circuit breaker.
    """
    daily_pnl = await _get_redis_float(redis, RedisKeys.daily_pnl_usdc(), 0.0)

    # Circuit breaker triggers on loss only (negative PnL)
    if daily_pnl < 0 and abs(daily_pnl) >= config.risk.max_daily_loss_usdc:
        return False, (
            f"circuit_breaker_triggered: daily loss ${abs(daily_pnl):.2f} "
            f">= limit ${config.risk.max_daily_loss_usdc:.2f}"
        )
    return True, ""


async def _check_max_positions(redis: Redis, config: MegConfig) -> tuple[bool, str]:
    """
    Gate 3: Reject if we're already at the max open position count.

    Reads the length of the meg:open_positions hash (HLEN).
    Missing/empty hash → 0 positions → PASS.
    """
    count = await redis.hlen(RedisKeys.open_positions())

    if count >= config.risk.max_open_positions:
        return False, (
            f"max_positions_reached: {count} open "
            f">= limit {config.risk.max_open_positions}"
        )
    return True, ""


async def _check_market_exposure(
    market_id: str,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """
    Gate 4: Reject if this market already has too much exposure.

    Compares market_exposure_usdc / portfolio_value_usdc against
    config.risk.max_market_exposure_pct.

    Missing portfolio_value → FAIL (cannot compute ratio safely).
    Missing market_exposure → 0.0 (no existing exposure) → PASS.
    """
    portfolio_val = await _get_redis_float(
        redis, RedisKeys.portfolio_value_usdc(), None
    )
    if portfolio_val is None or portfolio_val <= 0:
        # Fall back to config default
        portfolio_val = config.kelly.portfolio_value_usdc
        if portfolio_val <= 0:
            return False, "no_portfolio_value: cannot compute market exposure ratio"

    market_exposure = await _get_redis_float(
        redis, RedisKeys.market_exposure_usdc(market_id), 0.0
    )
    exposure_pct = market_exposure / portfolio_val

    if exposure_pct >= config.risk.max_market_exposure_pct:
        return False, (
            f"max_market_exposure_reached: {exposure_pct:.1%} "
            f">= limit {config.risk.max_market_exposure_pct:.1%} "
            f"(market={market_id})"
        )
    return True, ""


async def clamp_position_size(
    proposed_size_usdc: float,
    redis: Redis,
    config: MegConfig,
) -> float:
    """
    Clamp proposed position size to max_position_pct * portfolio_value.

    PRD §10 Gate 2: "Reduce position size to maximum allowed. Do not block
    the trade."  This is a size reducer, not a hard block — Kelly sizing
    should naturally stay within the limit; this is the backstop.

    Returns the original size if within limits, or the clamped maximum.
    If portfolio value is unavailable, returns the proposed size unchanged.
    """
    portfolio_val = await _get_redis_float(
        redis, RedisKeys.portfolio_value_usdc(), None
    )
    if portfolio_val is None or portfolio_val <= 0:
        portfolio_val = config.kelly.portfolio_value_usdc
        if portfolio_val <= 0:
            return proposed_size_usdc

    max_size = config.risk.max_position_pct * portfolio_val

    if proposed_size_usdc > max_size:
        logger.info(
            "risk_controller.position_size_clamped",
            proposed=round(proposed_size_usdc, 2),
            max_allowed=round(max_size, 2),
            portfolio_value=round(portfolio_val, 2),
        )
        return max_size

    return proposed_size_usdc


# ── Helper ────────────────────────────────────────────────────────────────────


async def _get_redis_float(
    redis: Redis, key: str, default: float | None
) -> float | None:
    """Read a Redis key as float. Returns default if key is missing or unparseable."""
    val = await redis.get(key)
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        logger.warning("risk_controller.invalid_redis_value", key=key, value=val)
        return default
