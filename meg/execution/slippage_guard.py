"""
Slippage guard.

Checks spread and price drift before order submission. Two sequential gates;
the first failure returns immediately (fail-fast). Slippage estimate is always
computed and returned for logging/analytics regardless of gate outcome.

Gate 1 — Spread: (ask - bid) / mid <= config.entry.max_spread_pct
  Wide spread = we lose edge on both entry and (eventual) exit.
  If spread fails, the drift gate is NOT evaluated.

Gate 2 — Price drift: abs(mid - signal_price) / signal_price
                      <= config.entry.max_price_drift_since_signal
  Catches cases where entry_filter passes (price near whale entry in one
  direction) but the overall mid has drifted away from the signal price.
  Reference: proposal.market_price_at_signal (whale's fill price).
  Skipped when signal_price <= 0 (TradeProposal default = unset).

Slippage estimate: size_usdc / liquidity_usdc — proxy for book depth.
  Returns 1.0 (100%) when liquidity is unknown or zero (fail-closed).
  Capped at 1.0. Always computed for analytics; does not gate the trade.

  TODO: replace proxy with full bid-side depth walk once get_orderbook()
  live mode is implemented. See TODOS.md.

Decision tree:
  ┌───────────────────────────────────────────────────────────────┐
  │ estimate_slippage(market_id, size_usdc, redis)                 │
  │   liquidity key absent → 1.0  (fail closed)                   │
  │   liquidity = 0        → 1.0  (fail closed)                   │
  │   normal               → min(size / liquidity, 1.0)           │
  │                                                                │
  │ check(proposal, redis, config) → (bool, str, float)           │
  │   bid/ask absent   → (False, "no_market_data",      slippage) │
  │   spread too wide  → (False, "spread_too_wide:...", slippage) │
  │                        ↑ drift gate not evaluated             │
  │   drift exceeded   → (False, "price_drift_exceeded:...", slip)│
  │   both pass        → (True,  "",                   slippage)  │
  └───────────────────────────────────────────────────────────────┘
"""
from __future__ import annotations

import structlog
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, TradeProposal

logger = structlog.get_logger(__name__)


async def estimate_slippage(
    market_id: str,
    size_usdc: float,
    redis: Redis,
) -> float:
    """
    Estimate slippage as a fraction of the order size given current book depth.
    Returns a value in [0.0, 1.0] — e.g., 0.02 = 2% slippage expected.

    Uses market:{id}:liquidity (total USDC depth within 5 ticks) from Redis as
    a proxy for full orderbook depth. size_usdc / liquidity_usdc estimates the
    fraction of the book our order consumes, capped at 1.0.

    Fail-closed: returns 1.0 when liquidity data is absent or zero.
    This causes slippage_guard.check() to see worst-case slippage but does NOT
    directly gate the trade (only spread and drift are gates).

    TODO: replace proxy with full bid-side depth walk once get_orderbook() live
    mode is implemented. See TODOS.md: "Real orderbook depth slippage estimation".
    """
    raw = await redis.get(RedisKeys.market_liquidity(market_id))
    if raw is None:
        logger.debug(
            "slippage_guard.liquidity_absent",
            market_id=market_id,
            note="returning 1.0 (fail closed)",
        )
        return 1.0
    liquidity = float(raw)
    if liquidity <= 0.0:
        logger.debug(
            "slippage_guard.zero_liquidity",
            market_id=market_id,
            note="returning 1.0 (fail closed)",
        )
        return 1.0
    return min(size_usdc / liquidity, 1.0)


async def check(
    proposal: TradeProposal,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str, float]:
    """
    Return (True, "", estimated_slippage) if both gates pass.
    Return (False, reason, estimated_slippage) if either gate fails.

    Gates are evaluated in order; spread failure returns before drift is checked.
    estimated_slippage is always computed and returned for logging/analytics
    regardless of gate outcome.

    Fail-closed: absent bid/ask Redis keys → (False, "no_market_data", slippage).
    """
    bid_raw = await redis.get(RedisKeys.market_bid(proposal.market_id))
    ask_raw = await redis.get(RedisKeys.market_ask(proposal.market_id))

    # Slippage computed before gate checks — always returned for analytics.
    slippage = await estimate_slippage(
        proposal.market_id, proposal.size_usdc, redis
    )

    if bid_raw is None or ask_raw is None:
        logger.warning(
            "slippage_guard.no_market_data",
            market_id=proposal.market_id,
            proposal_id=proposal.proposal_id,
        )
        return False, "no_market_data", slippage

    bid = float(bid_raw)
    ask = float(ask_raw)
    mid = (bid + ask) / 2.0

    if mid <= 0.0:
        return False, "invalid_mid_price", slippage

    spread_pct = (ask - bid) / mid

    # Gate 1: spread check — fail fast; drift not evaluated on spread failure
    if spread_pct > config.entry.max_spread_pct:
        logger.warning(
            "slippage_guard.spread_too_wide",
            market_id=proposal.market_id,
            proposal_id=proposal.proposal_id,
            spread_pct=round(spread_pct, 4),
            max_spread_pct=config.entry.max_spread_pct,
        )
        return (
            False,
            f"spread_too_wide: {spread_pct:.4f} > {config.entry.max_spread_pct:.4f}",
            slippage,
        )

    # Gate 2: price drift check (skipped when signal_price is unset / zero)
    signal_price = proposal.market_price_at_signal
    if signal_price > 0.0:
        drift = abs(mid - signal_price) / signal_price
        if drift > config.entry.max_price_drift_since_signal:
            logger.warning(
                "slippage_guard.price_drift_exceeded",
                market_id=proposal.market_id,
                proposal_id=proposal.proposal_id,
                drift=round(drift, 4),
                max_drift=config.entry.max_price_drift_since_signal,
                mid=mid,
                signal_price=signal_price,
            )
            return (
                False,
                f"price_drift_exceeded: {drift:.4f} > {config.entry.max_price_drift_since_signal:.4f}",
                slippage,
            )

    return True, "", slippage
