"""
Consensus filter.

Detects when multiple independent qualified whales are trading in the same
direction on the same market within a time window. Multi-whale agreement
significantly boosts signal confidence — it reduces the probability that
any single whale is acting on noise or manipulating.

A signal with consensus gets a score boost. A signal from a single whale
with no consensus gets no boost (but is not penalised).
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade


async def score(
    trade: QualifiedWhaleTrade,
    redis: Redis,
    config: MegConfig,
) -> float:
    """
    Return a consensus score in [0.0, 1.0].
    0.0 = no other qualified whale in same direction within the time window.
    1.0 = config.signal.min_whales_for_consensus or more whales in agreement.
    """
    raise NotImplementedError("consensus_filter.score")


async def get_recent_whale_trades(
    market_id: str,
    outcome: str,
    window_seconds: int,
    redis: Redis,
) -> list[str]:
    """
    Return wallet addresses of qualified whales who traded the same outcome
    in this market within the last window_seconds. Fetched from Redis.
    """
    raise NotImplementedError("consensus_filter.get_recent_whale_trades")
