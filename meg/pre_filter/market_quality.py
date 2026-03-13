"""
Pre-filter Gate 1: Market Quality Filter.

Rejects trades on markets that don't meet minimum liquidity, spread, and
participant thresholds. A signal on a thin or manipulable market is worthless
regardless of the whale's quality.

Gate decision:
  RawWhaleTrade ──► check() ──► True  → pass to Gate 2 (arb exclusion)
                            └──► False → log as FILTERED, discard
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RawWhaleTrade


async def check(trade: RawWhaleTrade, redis: Redis, config: MegConfig) -> bool:
    """
    Return True if the trade's market meets all quality thresholds:
      - Market liquidity >= config.pre_filter.min_market_liquidity_usdc
      - Bid-ask spread <= config.pre_filter.max_spread_pct
      - Unique participant count >= config.pre_filter.min_unique_participants
    Market data is fetched from Redis cache (set by data_layer) or CLOB API.
    """
    raise NotImplementedError("market_quality.check")


async def _get_market_liquidity(market_id: str, redis: Redis) -> float:
    """Return the current liquidity (USDC) for a market from Redis cache."""
    raise NotImplementedError("market_quality._get_market_liquidity")


async def _get_market_spread(market_id: str, redis: Redis) -> float:
    """Return the current bid-ask spread (0.0–1.0) from Redis cache."""
    raise NotImplementedError("market_quality._get_market_spread")
