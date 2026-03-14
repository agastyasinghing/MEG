"""
Tests for pre_filter/market_quality.py (Gate 1).

Coverage map:
  check() fast-exit path        → test_check_quality_failed_cache_hit
  UNCHARACTERIZED (no cache)    → test_check_uncharacterized_market
  liquidity threshold           → test_check_low_liquidity
  spread threshold              → test_check_spread_too_wide
  participants threshold        → test_check_too_few_participants
  days_to_resolution threshold  → test_check_days_to_resolution_too_low
  days_to_resolution None skip  → test_check_days_to_resolution_none_skips
  all thresholds pass           → test_check_all_pass
  multiple failures / one write → test_check_multi_failure_writes_one_cache_entry
  helper: _get_participants     → test_get_participants_returns_int
  helper: _get_days_to_resolution (empty string) → test_get_days_to_resolution_empty_string
  helper: _get_days_to_resolution (absent key)   → test_get_days_to_resolution_absent
"""
from __future__ import annotations

import pytest
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys
from meg.pre_filter import market_quality
from tests.pre_filter.conftest import make_raw_trade, set_market_redis_data


# ── Fast-exit / negative cache ────────────────────────────────────────────────


async def test_check_quality_failed_cache_hit(mock_redis: Redis, test_config: MegConfig) -> None:
    """
    When market:{id}:quality_failed exists, check() returns False immediately
    without reading any other Redis keys.
    """
    trade = make_raw_trade(market_id="market_001")
    await mock_redis.set(RedisKeys.market_quality_failed("market_001"), "1")

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is False


async def test_check_quality_failed_cache_not_written_on_uncharacterized(
    mock_redis: Redis, test_config: MegConfig
) -> None:
    """
    When last_updated_ms is absent (UNCHARACTERIZED), check() returns False
    but does NOT write quality_failed — the next event gets a fresh check.
    """
    trade = make_raw_trade(market_id="market_fresh")
    # No keys set at all — market is completely uncharacterized

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is False
    # Critical: quality_failed must NOT be cached for uncharacterized markets
    cached = await mock_redis.exists(RedisKeys.market_quality_failed("market_fresh"))
    assert cached == 0


# ── Individual threshold failures ─────────────────────────────────────────────


async def test_check_low_liquidity(mock_redis: Redis, test_config: MegConfig) -> None:
    """Liquidity below min_market_liquidity_usdc → rejected, quality_failed written."""
    trade = make_raw_trade(market_id="market_001")
    await set_market_redis_data(
        mock_redis,
        market_id="market_001",
        liquidity=1_000.0,  # well below default 50_000
    )

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is False
    cached = await mock_redis.exists(RedisKeys.market_quality_failed("market_001"))
    assert cached == 1


async def test_check_spread_too_wide(mock_redis: Redis, test_config: MegConfig) -> None:
    """Spread above max_spread_pct → rejected, quality_failed written."""
    trade = make_raw_trade(market_id="market_001")
    await set_market_redis_data(
        mock_redis,
        market_id="market_001",
        spread=0.20,  # well above default max 0.05
    )

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is False
    cached = await mock_redis.exists(RedisKeys.market_quality_failed("market_001"))
    assert cached == 1


async def test_check_too_few_participants(mock_redis: Redis, test_config: MegConfig) -> None:
    """Participants below min_unique_participants → rejected, quality_failed written."""
    trade = make_raw_trade(market_id="market_001")
    await set_market_redis_data(
        mock_redis,
        market_id="market_001",
        participants=5,  # below default min 20
    )

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is False
    cached = await mock_redis.exists(RedisKeys.market_quality_failed("market_001"))
    assert cached == 1


async def test_check_days_to_resolution_too_low(
    mock_redis: Redis, test_config: MegConfig
) -> None:
    """days_to_resolution < min_days_to_resolution → rejected."""
    trade = make_raw_trade(market_id="market_001")
    await set_market_redis_data(
        mock_redis,
        market_id="market_001",
        days_to_resolution=1,  # below default min 3
    )

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is False


async def test_check_days_to_resolution_none_skips(
    mock_redis: Redis, test_config: MegConfig
) -> None:
    """
    When days_to_resolution is None (empty string in Redis), the check is
    skipped and the trade can still pass if all other thresholds are met.
    """
    trade = make_raw_trade(market_id="market_001")
    await set_market_redis_data(
        mock_redis,
        market_id="market_001",
        days_to_resolution=None,  # written as "" by CLOBMarketFeed
    )

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is True


async def test_check_days_to_resolution_negative_fails(
    mock_redis: Redis, test_config: MegConfig
) -> None:
    """
    Negative days_to_resolution (market past end date) fails the check.
    The market is technically expired and should not be traded.
    """
    trade = make_raw_trade(market_id="market_001")
    await set_market_redis_data(
        mock_redis,
        market_id="market_001",
        days_to_resolution=-2,
    )

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is False


# ── Pass case ─────────────────────────────────────────────────────────────────


async def test_check_all_pass(mock_redis: Redis, test_config: MegConfig) -> None:
    """
    When all thresholds are met, check() returns True and does NOT write
    quality_failed.
    """
    trade = make_raw_trade(market_id="market_001")
    await set_market_redis_data(mock_redis, market_id="market_001")  # all above minimums

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is True
    cached = await mock_redis.exists(RedisKeys.market_quality_failed("market_001"))
    assert cached == 0


# ── Multiple failures → single cache write ────────────────────────────────────


async def test_check_multi_failure_writes_one_cache_entry(
    mock_redis: Redis, test_config: MegConfig
) -> None:
    """
    When multiple thresholds fail, quality_failed is written exactly once
    (the key has a TTL and a value of '1').
    """
    trade = make_raw_trade(market_id="market_bad")
    await set_market_redis_data(
        mock_redis,
        market_id="market_bad",
        liquidity=0.0,
        spread=0.99,
        participants=0,
        days_to_resolution=0,
    )

    result = await market_quality.check(trade, mock_redis, test_config)

    assert result is False
    value = await mock_redis.get(RedisKeys.market_quality_failed("market_bad"))
    assert value == "1"
    ttl = await mock_redis.ttl(RedisKeys.market_quality_failed("market_bad"))
    assert ttl > 0  # has a TTL (not persistent)


# ── Helper function tests ─────────────────────────────────────────────────────


async def test_get_participants_returns_int(mock_redis: Redis) -> None:
    """_get_participants returns an int when the key is populated."""
    await mock_redis.set(RedisKeys.market_participants("m1"), "42")
    result = await market_quality._get_participants("m1", mock_redis)
    assert result == 42


async def test_get_participants_returns_none_on_missing(mock_redis: Redis) -> None:
    """_get_participants returns None when the key is absent."""
    result = await market_quality._get_participants("nonexistent_market", mock_redis)
    assert result is None


async def test_get_days_to_resolution_empty_string(mock_redis: Redis) -> None:
    """
    _get_days_to_resolution returns None when the Redis value is "" (empty string).
    CLOBMarketFeed writes "" when the market has no end_date or parse failed.
    """
    await mock_redis.set(RedisKeys.market_days_to_resolution("m1"), "")
    result = await market_quality._get_days_to_resolution("m1", mock_redis)
    assert result is None


async def test_get_days_to_resolution_absent(mock_redis: Redis) -> None:
    """_get_days_to_resolution returns None when the key does not exist."""
    result = await market_quality._get_days_to_resolution("no_such_market", mock_redis)
    assert result is None


async def test_get_days_to_resolution_valid_int(mock_redis: Redis) -> None:
    """_get_days_to_resolution parses a valid integer string correctly."""
    await mock_redis.set(RedisKeys.market_days_to_resolution("m1"), "14")
    result = await market_quality._get_days_to_resolution("m1", mock_redis)
    assert result == 14
