"""
Signal crowding detector.

Detects when too many copy-follower bots have already entered the same position,
eliminating the edge MEG exploits. Even if the whale signal is fresh, a crowded
entry means we're buying into already-inflated prices with reduced upside.

Distinct from saturation_monitor:
  - saturation_monitor: has the market price moved? (price-based)
  - crowding_detector: have copy bots already entered? (volume/wallet-count-based)
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import SignalEvent


async def check(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """
    Return (False, "") if entry is not yet crowded (edge still exists).
    Return (True, reason) if copy-follower entry has already occurred at scale.
    """
    raise NotImplementedError("crowding_detector.check")


async def get_copy_follower_volume(
    market_id: str,
    outcome: str,
    since_timestamp_ms: int,
    redis: Redis,
) -> float:
    """
    Return estimated USDC volume from known copy-follower wallets in this
    market/outcome since the given timestamp.
    """
    raise NotImplementedError("crowding_detector.get_copy_follower_volume")
