"""
Entry distance filter.

Final re-check immediately before order submission. Between human approval
and order placement, the market may have moved. If the current price has
drifted too far from the whale's entry price, abort the trade.

This is the last line of defence before money leaves the account.
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
    Return (True, "") if current price is within config.entry.max_entry_distance_pct
    of the proposal's limit_price.
    Return (False, reason) if the market has drifted beyond the threshold.
    Called immediately before order_router.place(), not before Telegram approval.
    """
    raise NotImplementedError("entry_filter.check")


async def get_current_price(market_id: str, redis: Redis) -> float:
    """Return the current mid price for a market from the Redis cache."""
    raise NotImplementedError("entry_filter.get_current_price")
