"""
Polygon RPC websocket feed.

Connects to the Polygon network via Alchemy websocket RPC, listens for
on-chain Polymarket transactions, filters for qualifying whale trades,
and emits RawWhaleTrade events to Redis pub/sub.

  Polygon RPC ──(websocket)──► _filter_whale_transaction()
                                        │
                               qualifies? (size >= threshold, wallet in registry)
                                        │
                               RawWhaleTrade ──► Redis CHANNEL_RAW_WHALE_TRADES

Critical constraint: this function must NEVER raise an unhandled exception.
Malformed transactions → log with full context, skip, continue the feed.
A crashed feed = blind system. Handle every exception explicitly.
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RawWhaleTrade, RedisKeys


async def run(rpc_url: str, redis: Redis, config: MegConfig) -> None:
    """
    Main entry point. Opens a websocket to the Polygon RPC and runs forever.
    Reconnects automatically on disconnect. Never returns under normal operation.
    Call this as a long-running asyncio task.
    """
    raise NotImplementedError("polygon_feed.run")


async def _filter_whale_transaction(
    tx: dict,
    config: MegConfig,
) -> RawWhaleTrade | None:
    """
    Inspect a raw Polygon transaction dict. Return a RawWhaleTrade if the
    transaction meets whale thresholds, or None if it should be skipped.
    Must not raise — return None on any parse/decode error and log the raw tx.
    """
    raise NotImplementedError("polygon_feed._filter_whale_transaction")


async def _emit_event(redis: Redis, event: RawWhaleTrade) -> None:
    """Publish a RawWhaleTrade to the Redis CHANNEL_RAW_WHALE_TRADES channel."""
    raise NotImplementedError("polygon_feed._emit_event")
