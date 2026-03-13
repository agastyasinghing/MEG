"""
Contrarian detector.

Detects when a high-quality whale is trading AGAINST the prevailing order
flow. This is a high-conviction signal: an informed whale fading the crowd
often precedes a market correction. Penalises signals that merely follow
momentum (lower score) and boosts signals that go against it.

NOTE: Implement with Opus + ultrathink. Contrarian logic is nuanced and
incorrect implementation produces the opposite of intended signal direction.
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
    Return a contrarian score modifier in [-0.2, +0.3].
    Positive: whale is against order flow (contrarian boost).
    Negative: whale is following order flow (momentum penalty).
    Zero: insufficient data to determine order flow direction.
    """
    raise NotImplementedError("contrarian_detector.score")


async def get_order_flow_direction(
    market_id: str,
    redis: Redis,
) -> float:
    """
    Return the net order flow direction for the market as a float in [-1.0, 1.0].
    +1.0 = strong YES buying pressure, -1.0 = strong NO buying pressure, 0.0 = neutral.
    """
    raise NotImplementedError("contrarian_detector.get_order_flow_direction")
