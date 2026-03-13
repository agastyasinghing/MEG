"""
Pre-filter Gate 2: Arbitrage Whale Exclusion.

Detects wallets operating pure arbitrage strategies and excludes their trades.
Arb whales provide no directional signal — they're exploiting price discrepancies,
not expressing a view on outcome probability. Following them is noise.

Gate decision:
  RawWhaleTrade ──► check() ──► True  → pass to Gate 3 (intent classifier)
                            └──► False → log as FILTERED (arb excluded), discard
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RawWhaleTrade


async def check(trade: RawWhaleTrade, redis: Redis, config: MegConfig) -> bool:
    """
    Return True if the wallet is NOT an arbitrage whale (i.e., passes this gate).
    An arbitrage whale is identified by:
      - Archetype == ARBITRAGE in wallet registry
      - OR behavioral pattern: simultaneous YES+NO positions in same market
    """
    raise NotImplementedError("arbitrage_exclusion.check")


async def _is_arb_archetype(wallet_address: str, redis: Redis) -> bool:
    """Return True if the wallet's registered archetype is ARBITRAGE."""
    raise NotImplementedError("arbitrage_exclusion._is_arb_archetype")


async def _has_simultaneous_both_sides(
    wallet_address: str,
    market_id: str,
    redis: Redis,
) -> bool:
    """
    Return True if the wallet holds or recently placed both YES and NO positions
    in the same market — a strong behavioural indicator of arbitrage intent.
    """
    raise NotImplementedError("arbitrage_exclusion._has_simultaneous_both_sides")
