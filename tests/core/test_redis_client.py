"""
Tests for meg/core/redis_client.py.

Covers the three critical behaviors:
  1. create_redis_client: retries on ConnectionError, raises immediately on
     AuthenticationError, succeeds on ping.
  2. subscribe: re-raises ConnectionError on disconnect — never swallows it.
  3. publish / close: smoke tests for the thin wrappers.

All tests use fakeredis (via conftest mock_redis fixture) or direct mocking.
No real Redis process required.
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from redis.exceptions import AuthenticationError
from redis.exceptions import ConnectionError as RedisConnectionError

from meg.core.redis_client import close, create_redis_client, publish, subscribe


# ── create_redis_client ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_redis_client_succeeds_on_first_ping():
    """Returns client immediately when ping succeeds on first attempt."""
    mock_client = AsyncMock()
    mock_client.ping = AsyncMock(return_value=True)

    with patch("meg.core.redis_client.Redis") as MockRedis:
        MockRedis.from_url.return_value = mock_client
        client = await create_redis_client("redis://localhost:6379/0")

    assert client is mock_client
    mock_client.ping.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_redis_client_retries_on_connection_error():
    """Retries up to 4 times on ConnectionError before raising."""
    mock_client = AsyncMock()
    mock_client.ping = AsyncMock(side_effect=RedisConnectionError("refused"))

    with patch("meg.core.redis_client.Redis") as MockRedis:
        MockRedis.from_url.return_value = mock_client
        with patch("asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(RedisConnectionError):
                await create_redis_client("redis://localhost:6379/0")

    # 4 attempts: initial + 3 backoff retries
    assert mock_client.ping.await_count == 4


@pytest.mark.asyncio
async def test_create_redis_client_raises_immediately_on_auth_error():
    """AuthenticationError is not retried — raises on first attempt."""
    mock_client = AsyncMock()
    mock_client.ping = AsyncMock(side_effect=AuthenticationError("bad password"))

    with patch("meg.core.redis_client.Redis") as MockRedis:
        MockRedis.from_url.return_value = mock_client
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            with pytest.raises(AuthenticationError):
                await create_redis_client("redis://localhost:6379/0")

    # No sleep between attempts — raised immediately
    mock_sleep.assert_not_awaited()
    assert mock_client.ping.await_count == 1


@pytest.mark.asyncio
async def test_create_redis_client_succeeds_after_one_retry():
    """Succeeds on second attempt after first ping fails."""
    mock_client = AsyncMock()
    mock_client.ping = AsyncMock(
        side_effect=[RedisConnectionError("transient"), True]
    )

    with patch("meg.core.redis_client.Redis") as MockRedis:
        MockRedis.from_url.return_value = mock_client
        with patch("asyncio.sleep", new_callable=AsyncMock):
            client = await create_redis_client("redis://localhost:6379/0")

    assert client is mock_client
    assert mock_client.ping.await_count == 2


# ── subscribe: ConnectionError re-raise ───────────────────────────────────────


@pytest.mark.asyncio
async def test_subscribe_reraises_connection_error_on_disconnect(mock_redis):
    """
    CORE DESIGN CONSTRAINT: subscribe() must not swallow ConnectionError.
    When pubsub.listen() raises, subscribe must re-raise as RedisConnectionError.
    Silent disconnects = undetectable event loss.
    """
    async def mock_listen():
        yield {"type": "subscribe", "data": 1}
        raise RedisConnectionError("connection lost")

    mock_pubsub = MagicMock()
    mock_pubsub.subscribe = AsyncMock()
    mock_pubsub.listen = mock_listen
    mock_pubsub.unsubscribe = AsyncMock()
    mock_pubsub.aclose = AsyncMock()
    mock_redis.pubsub = MagicMock(return_value=mock_pubsub)

    with pytest.raises(RedisConnectionError):
        async for _ in subscribe(mock_redis, "test_channel"):
            pass  # should raise before yielding any message


@pytest.mark.asyncio
async def test_subscribe_yields_message_data(mock_redis):
    """subscribe() yields the data field from message-type events."""
    async def mock_listen():
        yield {"type": "subscribe", "data": 1}   # subscribe confirmation — skip
        yield {"type": "message", "data": '{"key": "value"}'}

    mock_pubsub = MagicMock()
    mock_pubsub.subscribe = AsyncMock()
    mock_pubsub.listen = mock_listen
    mock_pubsub.unsubscribe = AsyncMock()
    mock_pubsub.aclose = AsyncMock()
    mock_redis.pubsub = MagicMock(return_value=mock_pubsub)

    messages = []
    async for msg in subscribe(mock_redis, "test_channel"):
        messages.append(msg)

    assert messages == ['{"key": "value"}']


# ── publish / close: smoke tests ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_publish_calls_redis_publish(mock_redis):
    """publish() calls redis.publish with the correct channel and message."""
    mock_redis.publish = AsyncMock(return_value=1)
    await publish(mock_redis, "my_channel", '{"event": "test"}')
    mock_redis.publish.assert_awaited_once_with("my_channel", '{"event": "test"}')


@pytest.mark.asyncio
async def test_close_calls_aclose(mock_redis):
    """close() calls redis.aclose() to release the connection pool."""
    mock_redis.aclose = AsyncMock()
    await close(mock_redis)
    mock_redis.aclose.assert_awaited_once()
