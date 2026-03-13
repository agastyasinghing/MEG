"""
Market saturation monitor.

Detects when a market has become too crowded with copy traders, narrowing or
eliminating the entry window that MEG exploits. If the market is already
saturated, entering now means paying a premium with no edge remaining.

Saturation signals:
  - Mid price has moved significantly since whale's entry (window closed)
  - Order book depth on the whale's side has thinned (others already entered)
  - Copy-follower volume spike detected in the market

NOTE: Implement with Opus + ultrathink. Market saturation detection directly
affects whether we enter at a price with genuine edge or not.
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
    Return (False, "") if market is not saturated (safe to enter).
    Return (True, reason) if market entry window has closed.
    """
    raise NotImplementedError("saturation_monitor.check")


async def get_price_drift_since_signal(
    signal: SignalEvent,
    redis: Redis,
) -> float:
    """
    Return the price movement (absolute) since the signal was first generated.
    Large drift = market has already reacted; entry window likely closed.
    """
    raise NotImplementedError("saturation_monitor.get_price_drift_since_signal")
