"""
Entry ladder detector.

Detects when a whale is building a position in escalating increments over
time (ladder buying). This pattern indicates growing conviction — the whale
is comfortable adding to their position as they gather more information.
Distinguishes from a single large trade by tracking the series pattern.
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
    Return a ladder score in [0.0, 1.0].
    0.0 = isolated trade, no ladder pattern detected.
    1.0 = clear escalating ladder — 3+ trades in same direction, each larger.
    """
    raise NotImplementedError("ladder_detector.score")


async def get_wallet_trade_history(
    wallet_address: str,
    market_id: str,
    outcome: str,
    window_seconds: int,
    redis: Redis,
) -> list[dict]:
    """
    Return recent trades by this wallet in this market and direction,
    ordered by timestamp ascending. Used to detect ladder patterns.
    """
    raise NotImplementedError("ladder_detector.get_wallet_trade_history")


def _is_escalating_ladder(trades: list[dict]) -> bool:
    """
    Return True if the trade series shows an escalating ladder pattern:
    each trade's size is >= the previous, with no reversals.
    """
    raise NotImplementedError("ladder_detector._is_escalating_ladder")
