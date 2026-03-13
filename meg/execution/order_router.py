"""
Order router.

The only module in MEG that submits orders to the Polymarket CLOB.
Handles the full lifecycle: entry_filter → slippage_guard → place order →
notify position_manager → handle fills and partial fills.

Paper trading mode: when config.risk.paper_trading is True, logs the intended
order with [PAPER] prefix and returns a synthetic result without submitting.

In v1, order_router.place() is only called after human approval via Telegram.
Never call this directly from signal_engine or agent_core.
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import TradeProposal


async def place(
    proposal: TradeProposal,
    redis: Redis,
    config: MegConfig,
) -> dict:
    """
    Execute the full order placement sequence:
      1. entry_filter.check() — abort if price has drifted
      2. slippage_guard.check() — abort if spread/slippage too high
      3. clob_client.place_order() — submit limit order (or log if paper mode)
      4. position_manager.open_position() — record the new position
      5. Return the order result dict

    Raises on unrecoverable execution error (not swallowed — let caller handle).
    """
    raise NotImplementedError("order_router.place")


async def cancel(order_id: str, redis: Redis, config: MegConfig) -> bool:
    """
    Cancel an open order. Returns True if successfully cancelled.
    Updates position_manager if position is fully cancelled.
    """
    raise NotImplementedError("order_router.cancel")


async def handle_fill(
    order_id: str,
    fill_size_usdc: float,
    fill_price: float,
    redis: Redis,
) -> None:
    """
    Process an order fill event from the CLOB websocket.
    Updates position_manager with the actual fill details.
    Handles partial fills by tracking remaining open quantity.
    """
    raise NotImplementedError("order_router.handle_fill")
