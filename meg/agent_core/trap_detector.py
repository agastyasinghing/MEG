"""
Whale trap detector.

Detects the pump-and-exit pattern: a whale enters a large position (triggering
copy traders to follow), then exits before the position resolves — leaving
copy followers holding a deteriorating position.

Indicators of a trap:
  - Whale has a history of short-duration large positions
  - Whale exits within hours of entry while price hasn't resolved
  - Multiple instances of same wallet executing this pattern

NOTE: Implement with Opus + ultrathink. False negatives = following manipulators.
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade


async def check(
    trade: QualifiedWhaleTrade,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """
    Return (False, "") if no trap detected (trade is safe to proceed).
    Return (True, reason) if a whale trap pattern is detected.
    """
    raise NotImplementedError("trap_detector.check")


async def get_wallet_exit_history(
    wallet_address: str,
    redis: Redis,
) -> list[dict]:
    """
    Return recent exit events for this wallet, used to detect short-hold patterns.
    """
    raise NotImplementedError("trap_detector.get_wallet_exit_history")


def _score_trap_probability(exit_history: list[dict]) -> float:
    """
    Return a trap probability score in [0.0, 1.0] based on exit history.
    High score = wallet has a strong history of pump-and-exit behaviour.
    """
    raise NotImplementedError("trap_detector._score_trap_probability")
