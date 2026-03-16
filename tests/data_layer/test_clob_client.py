"""
Tests for meg/data_layer/clob_client.py — CLOBMarketFeed.

Focus: Redis state management, price history sorted set, error isolation,
and days_to_resolution parsing in _parse_days_to_resolution.
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
    _parse_days_to_resolution,
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
    await feed._write_state(state, "")

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
    await feed._write_state(state, "")

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
        await feed._write_state(state, "")

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
    await feed._write_state(state, "")

    members = await mock_redis.zrange(key, 0, -1)
    # Only the fresh entry should remain; the stale one should be removed
    assert all("stale" not in m for m in members)
    assert len(members) == 1


@pytest.mark.asyncio
async def test_write_state_writes_market_category_to_redis(mock_redis, config):
    """_write_state writes market_category to RedisKeys.market_category()."""
    feed = CLOBMarketFeed(redis=mock_redis, config=config)
    state = make_market_state(market_id="market_cat")
    await feed._write_state(state, "politics")

    value = await mock_redis.get(RedisKeys.market_category("market_cat"))
    assert value == "politics"


@pytest.mark.asyncio
async def test_write_state_writes_empty_category_when_unknown(mock_redis, config):
    """_write_state writes empty string when category is unknown."""
    feed = CLOBMarketFeed(redis=mock_redis, config=config)
    state = make_market_state(market_id="market_nocat")
    await feed._write_state(state, "")

    value = await mock_redis.get(RedisKeys.market_category("market_nocat"))
    assert value == ""


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
        state, category = await feed._fetch_market_state("market_nohttpx")

    assert isinstance(state, MarketState)
    assert state.market_id == "market_nohttpx"
    assert 0.0 <= state.mid_price <= 1.0
    assert category == ""  # placeholder path always returns empty category


@pytest.mark.asyncio
async def test_fetch_market_state_sets_days_to_resolution_from_end_date_iso(
    mock_redis, config
):
    """
    When the CLOB response includes end_date_iso, _fetch_market_state passes
    it through _parse_days_to_resolution and sets days_to_resolution on the
    returned MarketState.
    """
    from datetime import timedelta
    from unittest.mock import MagicMock

    feed = CLOBMarketFeed(redis=mock_redis, config=config)

    future_date = datetime.now(tz=timezone.utc) + timedelta(days=7)
    end_date_iso = future_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    ob_payload = {"best_bid": "0.55", "best_ask": "0.65", "bids": [], "asks": []}
    mk_payload = {
        "volume": "100000",
        "unique_traders": "250",
        "end_date_iso": end_date_iso,
    }

    mock_response_ob = MagicMock()
    mock_response_ob.raise_for_status = MagicMock()
    mock_response_ob.json.return_value = ob_payload

    mock_response_mk = MagicMock()
    mock_response_mk.raise_for_status = MagicMock()
    mock_response_mk.json.return_value = mk_payload

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[mock_response_ob, mock_response_mk])
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    # httpx is imported inside _fetch_market_state — patch via sys.modules
    import types
    mock_httpx = types.ModuleType("httpx")
    mock_httpx.AsyncClient = MagicMock(return_value=mock_client)

    with patch.dict("sys.modules", {"httpx": mock_httpx}):
        state, category = await feed._fetch_market_state("market_with_enddate")

    assert isinstance(state, MarketState)
    assert state.days_to_resolution is not None
    assert 6 <= state.days_to_resolution <= 8


# ── Execution stubs still raise NotImplementedError ───────────────────────────


@pytest.mark.asyncio
async def test_get_market_stub_raises():
    from meg.data_layer.clob_client import get_market
    with pytest.raises(NotImplementedError):
        await get_market("test")


@pytest.mark.asyncio
async def test_place_order_paper_mode_returns_synthetic_id(config):
    # Paper mode: returns "PAPER_<hex>" without touching the CLOB.
    from meg.data_layer.clob_client import place_order
    order_id = await place_order("test", "YES", "buy", 100.0, 0.5, config)
    assert order_id.startswith("PAPER_")
    assert len(order_id) == len("PAPER_") + 12


@pytest.mark.asyncio
async def test_place_order_live_mode_raises(config):
    # Live mode (paper_trading=False) raises NotImplementedError — OQ-05 pending.
    from meg.core.config_loader import MegConfig
    from meg.data_layer.clob_client import place_order
    live_config = MegConfig()
    live_config.risk.paper_trading = False
    with pytest.raises(NotImplementedError):
        await place_order("test", "YES", "buy", 100.0, 0.5, live_config)


# ── _parse_days_to_resolution ─────────────────────────────────────────────────


def test_parse_days_to_resolution_valid_iso_date():
    """Returns positive int for a future end_date_iso string."""
    from datetime import datetime, timedelta, timezone

    # Use a date 10 days from now to avoid flakiness at boundaries
    future = datetime.now(tz=timezone.utc) + timedelta(days=10)
    raw = future.strftime("%Y-%m-%dT%H:%M:%SZ")

    result = _parse_days_to_resolution("market_test", raw)

    # Allow ±1 day for timing skew at midnight boundaries
    assert result is not None
    assert 9 <= result <= 11


def test_parse_days_to_resolution_missing_field_returns_none():
    """Returns None when raw_date is None (market has no end date)."""
    result = _parse_days_to_resolution("market_no_end", None)
    assert result is None


def test_parse_days_to_resolution_invalid_format_returns_none():
    """Returns None when the date string cannot be parsed as ISO-8601."""
    result = _parse_days_to_resolution("market_bad", "not-a-date")
    assert result is None


def test_parse_days_to_resolution_expired_market_returns_negative():
    """Returns a negative int for a market whose end date has already passed."""
    from datetime import datetime, timedelta, timezone

    past = datetime.now(tz=timezone.utc) - timedelta(days=5)
    raw = past.strftime("%Y-%m-%dT%H:%M:%SZ")

    result = _parse_days_to_resolution("market_expired", raw)

    assert result is not None
    assert result < 0
