"""
Slippage guard.

Checks the current spread and expected slippage before order submission.
A wide spread means we lose edge on entry. Excessive slippage on a thin
book means our own order moves the market against us.

Evaluated immediately before order submission, after entry_filter passes.
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import TradeProposal


async def check(
    proposal: TradeProposal,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """
    Return (True, "") if spread and expected slippage are within acceptable limits:
      - Current spread <= config.entry.max_spread_pct
      - Expected slippage (based on order size vs book depth) is acceptable
    Return (False, reason) if either check fails.
    """
    raise NotImplementedError("slippage_guard.check")


async def estimate_slippage(
    market_id: str,
    outcome: str,
    size_usdc: float,
    redis: Redis,
) -> float:
    """
    Estimate slippage as a fraction of the order size given current book depth.
    Returns a value in [0.0, 1.0] — e.g., 0.02 = 2% slippage expected.
    """
    raise NotImplementedError("slippage_guard.estimate_slippage")
