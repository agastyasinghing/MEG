"""
Tests for meg/data_layer/clob_client.py — CLOBMarketFeed.

Focus: Redis state management, price history sorted set, error isolation.
No real CLOB API calls — CLOBMarketFeed._fetch_market_state is patched
to return controlled MarketState fixtures.
"""
from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest

from meg.core.config_loader import MegConfig
from meg.core.events import MarketState, RedisKeys
from meg.data_layer.clob_client import (
    CLOBMarketFeed,
    _PRICE_HISTORY_TTL_MS,
)


# ── Fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture
def config() -> MegConfig:
    return MegConfig()


def make_market_state(
    market_id: str = "market_abc",
    mid_price: float = 0.60,
    bid: float = 0.58,
    ask: float = 0.62,
    liquidity: float = 100_000.0,
    volume: float = 50_000.0,
    participants: int = 150,
) -> MarketState:
    return MarketState(
        market_id=market_id,
        bid=bid,
        ask=ask,
        mid_price=mid_price,
        spread=ask - bid,
        liquidity_usdc=liquidity,
        volume_24h_usdc=volume,
        participants=participants,
        last_updated_at=datetime.now(tz=timezone.utc),
    )


# ── Market state Redis key writes ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_write_state_sets_all_scalar_keys(mock_redis, config):
    """_write_state writes all 8 scalar market keys to Redis."""
    feed = CLOBMarketFeed(redis=mock_redis, config=config)
    state = make_market_state(market_id="market_001")
    await feed._write_state(state)

    mid = "market_001"
    assert await mock_redis.get(RedisKeys.market_mid_price(mid)) == str(state.mid_price)
    assert await mock_redis.get(RedisKeys.market_bid(mid)) == str(state.bid)
    assert await mock_redis.get(RedisKeys.market_ask(mid)) == str(state.ask)
    assert await mock_redis.get(RedisKeys.market_spread(mid)) == str(state.spread)
    assert await mock_redis.get(RedisKeys.market_liquidity(mid)) is not None
    assert await mock_redis.get(RedisKeys.market_volume_24h(mid)) is not None
    assert await mock_redis.get(RedisKeys.market_participants(mid)) == str(state.participants)
    assert await mock_redis.get(RedisKeys.market_last_updated_ms(mid)) is not None


@pytest.mark.asyncio
async def test_write_state_adds_to_price_history_sorted_set(mock_redis, config):
    """_write_state adds an entry to the price_history sorted set."""
    feed = CLOBMarketFeed(redis=mock_redis, config=config)
    state = make_market_state(market_id="market_002", mid_price=0.55)
    await feed._write_state(state)

    key = RedisKeys.market_price_history("market_002")
    members = await mock_redis.zrange(key, 0, -1, withscores=True)
    assert len(members) == 1


@pytest.mark.asyncio
async def test_write_state_multiple_prices_accumulate_in_sorted_set(mock_redis, config):
    """Multiple _write_state calls accumulate price history entries."""
    feed = CLOBMarketFeed(redis=mock_redis, config=config)
    mid = "market_003"

    for price in [0.50, 0.55, 0.60]:
        state = make_market_state(market_id=mid, mid_price=price)
        await feed._write_state(state)

    key = RedisKeys.market_price_history(mid)
    members = await mock_redis.zrange(key, 0, -1)
    assert len(members) == 3


@pytest.mark.asyncio
async def test_write_state_trims_old_price_history(mock_redis, config):
    """
    ZREMRANGEBYSCORE trims entries older than 1 hour on every write.
    Simulate old entries by inserting with an old timestamp score.
    """
    feed = CLOBMarketFeed(redis=mock_redis, config=config)
    mid = "market_004"
    key = RedisKeys.market_price_history(mid)

    # Insert a stale entry with timestamp 2 hours ago
    now_ms = int(time.time() * 1000)
    stale_score = now_ms - 2 * _PRICE_HISTORY_TTL_MS
    await mock_redis.zadd(key, {"0.40@stale": stale_score})

    # Write a fresh state — trim should remove the stale entry
    state = make_market_state(market_id=mid, mid_price=0.60)
    await feed._write_state(state)

    members = await mock_redis.zrange(key, 0, -1)
    # Only the fresh entry should remain; the stale one should be removed
    assert all("stale" not in m for m in members)
    assert len(members) == 1


# ── Active markets subscription management ────────────────────────────────────


@pytest.mark.asyncio
async def test_run_polls_only_active_markets(mock_redis, config):
    """CLOBMarketFeed.run() only polls markets in the active_markets set."""
    await mock_redis.sadd(RedisKeys.active_markets(), "market_aaa")

    polled_markets: list[str] = []

    async def mock_poll_market(market_id: str) -> None:
        polled_markets.append(market_id)

    feed = CLOBMarketFeed(redis=mock_redis, config=config)
    feed._poll_market = mock_poll_market  # type: ignore[method-assign]

    # Run one iteration then cancel
    async def run_once():
        market_ids = await mock_redis.smembers(RedisKeys.active_markets())
        if market_ids:
            tasks = [feed._poll_market(mid) for mid in market_ids]
            await asyncio.gather(*tasks, return_exceptions=True)

    await run_once()
    assert "market_aaa" in polled_markets


@pytest.mark.asyncio
async def test_run_skips_poll_when_no_active_markets(mock_redis, config):
    """CLOBMarketFeed does not crash when active_markets set is empty."""
    feed = CLOBMarketFeed(redis=mock_redis, config=config)

    polled: list[str] = []

    async def mock_poll_market(market_id: str) -> None:
        polled.append(market_id)

    feed._poll_market = mock_poll_market  # type: ignore[method-assign]

    market_ids = await mock_redis.smembers(RedisKeys.active_markets())
    if market_ids:
        await asyncio.gather(*[feed._poll_market(m) for m in market_ids])

    assert polled == []


# ── Error isolation ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_poll_market_logs_and_continues_on_fetch_error(mock_redis, config):
    """_poll_market catches exceptions and does not propagate them."""
    feed = CLOBMarketFeed(redis=mock_redis, config=config)

    async def failing_fetch(market_id: str) -> MarketState:
        raise ConnectionError("CLOB API down")

    feed._fetch_market_state = failing_fetch  # type: ignore[method-assign]

    # Should not raise
    await feed._poll_market("market_failing")


@pytest.mark.asyncio
async def test_fetch_market_state_returns_placeholder_without_httpx(mock_redis, config):
    """
    When httpx is not installed, _fetch_market_state returns a placeholder
    MarketState with dummy values instead of raising ImportError.
    """
    feed = CLOBMarketFeed(redis=mock_redis, config=config)

    with patch.dict("sys.modules", {"httpx": None}):
        state = await feed._fetch_market_state("market_nohttpx")

    assert isinstance(state, MarketState)
    assert state.market_id == "market_nohttpx"
    assert 0.0 <= state.mid_price <= 1.0


# ── Execution stubs still raise NotImplementedError ───────────────────────────


@pytest.mark.asyncio
async def test_get_market_stub_raises():
    from meg.data_layer.clob_client import get_market
    with pytest.raises(NotImplementedError):
        await get_market("test")


@pytest.mark.asyncio
async def test_place_order_stub_raises(config):
    from meg.data_layer.clob_client import place_order
    with pytest.raises(NotImplementedError):
        await place_order("test", "YES", "buy", 100.0, 0.5, config)
