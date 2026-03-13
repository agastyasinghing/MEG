"""
Position manager.

Tracks all open positions, their entry prices, current P&L, and exit targets.
Provides the risk_controller with current exposure data. Monitors positions
for stop-loss conditions and emits exit signals when triggered.
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig


async def get_open_positions(redis: Redis) -> list[dict]:
    """Return all currently open positions with their sizes and entry prices."""
    raise NotImplementedError("position_manager.get_open_positions")


async def get_total_exposure_usdc(redis: Redis) -> float:
    """Return total capital currently deployed across all open positions."""
    raise NotImplementedError("position_manager.get_total_exposure_usdc")


async def get_market_exposure_usdc(market_id: str, redis: Redis) -> float:
    """Return total capital deployed in a specific market."""
    raise NotImplementedError("position_manager.get_market_exposure_usdc")


async def open_position(
    market_id: str,
    outcome: str,
    size_usdc: float,
    entry_price: float,
    proposal_id: str,
    redis: Redis,
) -> None:
    """Record a new open position after trade execution."""
    raise NotImplementedError("position_manager.open_position")


async def close_position(
    market_id: str,
    outcome: str,
    exit_price: float,
    redis: Redis,
) -> dict:
    """
    Record the closure of a position and return the P&L summary.
    Triggers wallet registry score update based on outcome.
    """
    raise NotImplementedError("position_manager.close_position")


async def get_daily_pnl_usdc(redis: Redis) -> float:
    """Return net P&L for today. Used by risk_controller daily loss gate."""
    raise NotImplementedError("position_manager.get_daily_pnl_usdc")
