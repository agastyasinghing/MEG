"""
Async Redis client factory and pub/sub helpers for MEG.

All layers receive a Redis client via dependency injection — no module-level
singletons, no hidden global state. The client is created once at startup
and passed as an argument to every function that needs it.

Usage:
    from meg.core.redis_client import create_redis_client, publish, subscribe
    from meg.core.events import RedisKeys, RawWhaleTrade

    redis = await create_redis_client(url=os.environ.get("REDIS_URL", "redis://redis:6379/0"))

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

import asyncio
from collections.abc import AsyncIterator

import structlog
from redis.asyncio import Redis
from redis.exceptions import AuthenticationError
from redis.exceptions import ConnectionError as RedisConnectionError

logger = structlog.get_logger(__name__)

# Backoff delays between connect attempts (seconds). First attempt is immediate.
_CONNECT_BACKOFFS = [1.0, 2.0, 4.0]


async def create_redis_client(url: str) -> Redis:
    """
    Create and return a connected async Redis client.
    Retries up to 3 times with exponential backoff on ConnectionError.
    Raises redis.exceptions.ConnectionError if all retries are exhausted.
    Raises redis.exceptions.AuthenticationError immediately on auth failure (no retry).
    """
    last_exc: Exception | None = None
    attempts = [0.0] + _CONNECT_BACKOFFS  # first attempt: no wait

    for attempt, backoff in enumerate(attempts):
        if backoff:
            await asyncio.sleep(backoff)
        try:
            client: Redis = Redis.from_url(url, decode_responses=True)
            await client.ping()
            logger.info("redis.connected", url=_redact_url(url), attempt=attempt)
            return client
        except AuthenticationError:
            # Never retry auth failures — misconfiguration, not a transient error.
            raise
        except Exception as exc:
            last_exc = exc
            logger.warning(
                "redis.connect_failed",
                attempt=attempt,
                max_attempts=len(attempts),
                error=str(exc),
            )

    raise RedisConnectionError(
        f"Redis connection to {_redact_url(url)} failed after {len(attempts)} attempts"
    ) from last_exc


async def publish(client: Redis, channel: str, message: str) -> None:
    """
    Publish a JSON-serialized message string to a Redis pub/sub channel.
    message should be produced via Pydantic's model.model_dump_json().
    """
    await client.publish(channel, message)


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
    pubsub = client.pubsub()
    await pubsub.subscribe(channel)
    try:
        async for raw in pubsub.listen():
            if raw["type"] == "message":
                yield raw["data"]
    except Exception as exc:
        # Wrap and re-raise — callers must see a ConnectionError, not a generic one.
        raise RedisConnectionError(
            f"Redis pubsub disconnected on channel '{channel}': {exc}"
        ) from exc
    finally:
        try:
            await pubsub.unsubscribe(channel)
            await pubsub.aclose()
        except Exception:
            pass  # best-effort cleanup


async def close(client: Redis) -> None:
    """Close the Redis connection pool cleanly. Call at process shutdown."""
    await client.aclose()


def _redact_url(url: str) -> str:
    """Replace password in Redis URL with *** for safe logging."""
    try:
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(url)
        if parsed.password:
            redacted = parsed._replace(
                netloc=parsed.netloc.replace(parsed.password, "***")
            )
            return urlunparse(redacted)
    except Exception:
        pass
    return url
