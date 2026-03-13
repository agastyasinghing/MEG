"""
Polymarket CLOB API wrapper.

Thin async wrapper around py-clob-client. Handles authentication, rate limiting,
and retry logic. All other layers interact with Polymarket exclusively through
this module — never import py-clob-client directly outside this file.

Paper trading mode: when config.risk.paper_trading is True, place_order() logs
the intended order but does not submit it to the CLOB.
"""
from __future__ import annotations

from meg.core.config_loader import MegConfig


async def get_market(market_id: str) -> dict:
    """
    Fetch market metadata: question, end date, status, category.
    Raises on network error after retries.
    """
    raise NotImplementedError("clob_client.get_market")


async def get_orderbook(market_id: str) -> dict:
    """
    Fetch the current orderbook for a market.
    Returns bids, asks, mid price, and spread.
    """
    raise NotImplementedError("clob_client.get_orderbook")


async def get_mid_price(market_id: str) -> float:
    """Return the current mid price (0.0–1.0) for a market."""
    raise NotImplementedError("clob_client.get_mid_price")


async def place_order(
    market_id: str,
    outcome: str,
    side: str,
    size_usdc: float,
    limit_price: float,
    config: MegConfig,
) -> str:
    """
    Place a limit order on the CLOB. Returns the order ID.
    In paper trading mode (config.risk.paper_trading=True): logs the order
    and returns a synthetic order ID without submitting to the exchange.
    """
    raise NotImplementedError("clob_client.place_order")


async def cancel_order(order_id: str) -> bool:
    """Cancel an open order. Returns True if successfully cancelled."""
    raise NotImplementedError("clob_client.cancel_order")


async def get_open_orders(market_id: str | None = None) -> list[dict]:
    """Return all open orders, optionally filtered by market."""
    raise NotImplementedError("clob_client.get_open_orders")


async def get_position(market_id: str) -> dict | None:
    """Return current position for a market, or None if no position held."""
    raise NotImplementedError("clob_client.get_position")
