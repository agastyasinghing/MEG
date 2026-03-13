"""
Async Redis client factory and pub/sub helpers for MEG.

All layers receive a Redis client via dependency injection — no module-level
singletons, no hidden global state. The client is created once at startup
and passed as an argument to every function that needs it.

Usage:
    from meg.core.redis_client import create_redis_client, publish, subscribe
    from meg.core.events import RedisKeys, RawWhaleTrade

    redis = await create_redis_client(url="redis://localhost:6379/0")

    # Publisher (data_layer):
    await publish(redis, RedisKeys.CHANNEL_RAW_WHALE_TRADES, event.model_dump_json())

    # Subscriber (pre_filter):
    async for message in subscribe(redis, RedisKeys.CHANNEL_RAW_WHALE_TRADES):
        trade = RawWhaleTrade.model_validate_json(message)

Design constraints:
  - subscribe() MUST NOT swallow ConnectionError silently. On disconnect,
    re-raise so the caller's reconnect loop can handle it. Silent event loss
    in the pub/sub pipeline is a critical failure mode.
  - create_redis_client() retries 3x with exponential backoff before raising.
  - All functions use redis.asyncio (never the sync redis client).
"""
from __future__ import annotations

from collections.abc import AsyncIterator

from redis.asyncio import Redis


async def create_redis_client(url: str) -> Redis:
    """
    Create and return a connected async Redis client.
    Retries up to 3 times with exponential backoff on ConnectionError.
    Raises redis.ConnectionError if all retries are exhausted.
    Raises redis.AuthenticationError immediately on auth failure (no retry).
    """
    raise NotImplementedError("redis_client.create_redis_client")


async def publish(client: Redis, channel: str, message: str) -> None:
    """
    Publish a JSON-serialized message string to a Redis pub/sub channel.
    message should be produced via Pydantic's model.model_dump_json().
    """
    raise NotImplementedError("redis_client.publish")


async def subscribe(client: Redis, channel: str) -> AsyncIterator[str]:
    """
    Subscribe to a Redis pub/sub channel and yield decoded message strings.

    DESIGN CONSTRAINT: Must re-raise redis.ConnectionError on disconnect.
    Never return silently if the channel goes quiet — block until a message
    arrives. Callers are expected to wrap this in a reconnect loop.

    Usage:
        async for message in subscribe(redis, channel):
            process(message)
    """
    raise NotImplementedError("redis_client.subscribe")
    yield  # marks this as an async generator; remove when implementing


async def close(client: Redis) -> None:
    """Close the Redis connection pool cleanly. Call at process shutdown."""
    raise NotImplementedError("redis_client.close")
