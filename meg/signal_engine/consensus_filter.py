"""
Consensus filter.

Detects when multiple independent qualified whales are trading in the same
direction on the same market within a time window. Multi-whale agreement
significantly boosts signal confidence — it reduces the probability that
any single whale is acting on noise or manipulating.

A signal with consensus gets a score boost. A signal from a single whale
with no consensus gets no boost (but is not penalised).

Score formula: tanh(n_agreeing_whales * consensus_sensitivity / 2)
  n_agreeing_whales = count of OTHER whales in same direction within window
  consensus_sensitivity = config.signal.consensus_sensitivity (default 1.5)

  0 others → tanh(0) = 0.0
  1 other  → tanh(0.75) ≈ 0.64
  2 others → tanh(1.50) ≈ 0.91

PRD reference: §9.3.4 Consensus Filter
"""
from __future__ import annotations

import math
import time

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade, RedisKeys


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
    consensus_key = RedisKeys.consensus_window(trade.market_id, trade.outcome)
    now_ms = int(time.time() * 1000)
    window_ms = int(config.signal.consensus_window_hours * 3600 * 1000)
    cutoff_ms = now_ms - window_ms

    # Add current whale to the consensus window
    await redis.zadd(consensus_key, {trade.wallet_address: now_ms})

    # Trim stale entries outside the window
    await redis.zremrangebyscore(consensus_key, "-inf", cutoff_ms)

    # Count distinct wallets in window (excluding current wallet)
    members = await redis.zrange(consensus_key, 0, -1)
    n_agreeing = sum(1 for m in members if m != trade.wallet_address)

    sensitivity = config.signal.consensus_sensitivity
    return math.tanh(n_agreeing * sensitivity / 2.0)


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
    consensus_key = RedisKeys.consensus_window(market_id, outcome)
    now_ms = int(time.time() * 1000)
    cutoff_ms = now_ms - (window_seconds * 1000)

    members = await redis.zrangebyscore(consensus_key, cutoff_ms, "+inf")
    return list(members)
