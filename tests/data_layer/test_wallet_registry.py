"""
Tests for meg/data_layer/wallet_registry.py.

All DB tests use the db_session fixture (real PostgreSQL via pytest-postgresql).
Cache tests use the mock_redis fixture (fakeredis).

Test categories:
  1. upsert_wallet — DB write + cache invalidation
  2. get_wallet — Redis-first cache hit/miss
  3. is_qualified_whale — fast path cache + slow path DB
  4. update_wallet_score — score update + cache refresh
  5. get_wallet_archetype — cache-first
  6. qualify / disqualify / flag_excluded — state mutations
  7. update_capital — CapitalRefreshJob write path
  8. register_if_new — idempotent registration
  9. get_tracked_addresses — returns only is_tracked wallets
"""
from __future__ import annotations

import json

import pytest

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys
from meg.data_layer import wallet_registry
from meg.data_layer.wallet_registry import _wallet_data_key


# ── Fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture
def config() -> MegConfig:
    return MegConfig()


SAMPLE_ADDRESS = "0x1234567890123456789012345678901234567890"

SAMPLE_WALLET_DATA = {
    "archetype": "INFORMATION",
    "is_qualified": True,
    "composite_whale_score": 0.85,
    "win_rate": 0.72,
    "avg_lead_time_hours": 6.5,
    "roi_30d": 0.18,
    "roi_90d": 0.42,
    "roi_all_time": 0.61,
    "total_closed_positions": 87,
    "consistency_score": 0.80,
    "avg_conviction_ratio": 0.15,
    "reputation_decay_factor": 0.95,
    "category_scores": {"politics": 0.82, "crypto": 0.61},
    "total_volume_usdc": 250_000.0,
    "total_trades": 120,
    "total_capital_usdc": 50_000.0,
    "is_tracked": True,
    "is_excluded": False,
}


# ── 1. upsert_wallet — DB write ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_upsert_wallet_creates_new_row(db_session, mock_redis, config):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )

    result = await wallet_registry.get_wallet(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert result is not None
    assert result["address"] == SAMPLE_ADDRESS
    assert result["archetype"] == "INFORMATION"
    assert result["composite_whale_score"] == pytest.approx(0.85)


@pytest.mark.asyncio
async def test_upsert_wallet_updates_existing_row(db_session, mock_redis, config):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )

    updated = {**SAMPLE_WALLET_DATA, "composite_whale_score": 0.92, "win_rate": 0.78}
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, updated, mock_redis, session=db_session
    )

    result = await wallet_registry.get_wallet(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert result["composite_whale_score"] == pytest.approx(0.92)
    assert result["win_rate"] == pytest.approx(0.78)


@pytest.mark.asyncio
async def test_upsert_wallet_invalidates_cache(db_session, mock_redis, config):
    """Cache is cleared after upsert so next get_wallet fetches fresh data."""
    # Seed stale data in cache
    stale = {"address": SAMPLE_ADDRESS, "composite_whale_score": 0.10}
    await mock_redis.set(_wallet_data_key(SAMPLE_ADDRESS), json.dumps(stale))

    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )

    # Cache should be gone after upsert
    cached = await mock_redis.get(_wallet_data_key(SAMPLE_ADDRESS))
    assert cached is None


# ── 2. get_wallet — Redis-first ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_wallet_returns_none_for_unknown(db_session, mock_redis, config):
    result = await wallet_registry.get_wallet(
        "0x0000000000000000000000000000000000000000", mock_redis, session=db_session
    )
    assert result is None


@pytest.mark.asyncio
async def test_get_wallet_populates_cache_on_db_hit(db_session, mock_redis, config):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )

    # Ensure cache is empty (upsert invalidated it)
    assert await mock_redis.get(_wallet_data_key(SAMPLE_ADDRESS)) is None

    # get_wallet should hit DB and populate cache
    result = await wallet_registry.get_wallet(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert result is not None

    # Cache should now be populated
    cached_raw = await mock_redis.get(_wallet_data_key(SAMPLE_ADDRESS))
    assert cached_raw is not None
    cached = json.loads(cached_raw)
    assert cached["address"] == SAMPLE_ADDRESS


@pytest.mark.asyncio
async def test_get_wallet_cache_hit_skips_db(mock_redis, config):
    """Cache hit returns cached data without touching DB (no session injected)."""
    fake_data = {"address": SAMPLE_ADDRESS, "composite_whale_score": 0.99}
    await mock_redis.set(_wallet_data_key(SAMPLE_ADDRESS), json.dumps(fake_data))

    # No db_session injected — if it hits DB without init_db(), it would raise RuntimeError
    result = await wallet_registry.get_wallet(SAMPLE_ADDRESS, mock_redis)
    assert result is not None
    assert result["composite_whale_score"] == 0.99


# ── 3. is_qualified_whale ─────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_is_qualified_whale_true_for_qualified(db_session, mock_redis, config):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )
    result = await wallet_registry.is_qualified_whale(
        SAMPLE_ADDRESS, config, mock_redis, session=db_session
    )
    assert result is True


@pytest.mark.asyncio
async def test_is_qualified_whale_false_for_unknown(db_session, mock_redis, config):
    result = await wallet_registry.is_qualified_whale(
        "0x9999999999999999999999999999999999999999",
        config,
        mock_redis,
        session=db_session,
    )
    assert result is False


@pytest.mark.asyncio
async def test_is_qualified_whale_false_for_excluded(db_session, mock_redis, config):
    excluded_data = {
        **SAMPLE_WALLET_DATA,
        "is_excluded": True,
        "archetype": "ARBITRAGE",
    }
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, excluded_data, mock_redis, session=db_session
    )
    result = await wallet_registry.is_qualified_whale(
        SAMPLE_ADDRESS, config, mock_redis, session=db_session
    )
    assert result is False


@pytest.mark.asyncio
async def test_is_qualified_whale_false_for_excluded_archetype(
    db_session, mock_redis, config
):
    arb_data = {**SAMPLE_WALLET_DATA, "archetype": "MANIPULATOR"}
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, arb_data, mock_redis, session=db_session
    )
    result = await wallet_registry.is_qualified_whale(
        SAMPLE_ADDRESS, config, mock_redis, session=db_session
    )
    # MANIPULATOR is in exclude_archetypes by default
    assert result is False


# ── 4. update_wallet_score ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_update_wallet_score_persists_to_db(db_session, mock_redis, config):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )
    await wallet_registry.update_wallet_score(
        SAMPLE_ADDRESS, 0.91, mock_redis, session=db_session
    )

    result = await wallet_registry.get_wallet(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert result["composite_whale_score"] == pytest.approx(0.91)


@pytest.mark.asyncio
async def test_update_wallet_score_updates_redis_score_key(db_session, mock_redis, config):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )
    await wallet_registry.update_wallet_score(
        SAMPLE_ADDRESS, 0.77, mock_redis, session=db_session
    )

    score_str = await mock_redis.get(RedisKeys.wallet_score(SAMPLE_ADDRESS))
    assert score_str == "0.77"


# ── 5. get_wallet_archetype ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_wallet_archetype_returns_correct_value(db_session, mock_redis, config):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )
    archetype = await wallet_registry.get_wallet_archetype(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert archetype == "INFORMATION"


@pytest.mark.asyncio
async def test_get_wallet_archetype_returns_none_for_unknown(db_session, mock_redis):
    archetype = await wallet_registry.get_wallet_archetype(
        "0x0000000000000000000000000000000000000000",
        mock_redis,
        session=db_session,
    )
    assert archetype is None


@pytest.mark.asyncio
async def test_get_wallet_archetype_uses_cache(mock_redis):
    """Cache hit returns archetype without DB query."""
    await mock_redis.set(RedisKeys.wallet_archetype(SAMPLE_ADDRESS), "MOMENTUM")
    archetype = await wallet_registry.get_wallet_archetype(SAMPLE_ADDRESS, mock_redis)
    assert archetype == "MOMENTUM"


# ── 6. qualify / disqualify / flag_excluded ───────────────────────────────────


@pytest.mark.asyncio
async def test_qualify_sets_is_qualified_true(db_session, mock_redis, config):
    unqualified = {**SAMPLE_WALLET_DATA, "is_qualified": False}
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, unqualified, mock_redis, session=db_session
    )
    await wallet_registry.qualify(SAMPLE_ADDRESS, mock_redis, session=db_session)

    result = await wallet_registry.get_wallet(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert result["is_qualified"] is True


@pytest.mark.asyncio
async def test_disqualify_sets_is_qualified_false(db_session, mock_redis, config):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )
    await wallet_registry.disqualify(SAMPLE_ADDRESS, mock_redis, session=db_session)

    result = await wallet_registry.get_wallet(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert result["is_qualified"] is False


@pytest.mark.asyncio
async def test_flag_excluded_sets_excluded_and_unqualifies(db_session, mock_redis, config):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )
    await wallet_registry.flag_excluded(
        SAMPLE_ADDRESS, "ARBITRAGE pattern detected", mock_redis, session=db_session
    )

    result = await wallet_registry.get_wallet(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert result["is_excluded"] is True
    assert result["is_qualified"] is False
    assert result["exclusion_reason"] == "ARBITRAGE pattern detected"


# ── 7. update_capital ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_update_capital_persists_and_invalidates_cache(
    db_session, mock_redis, config
):
    await wallet_registry.upsert_wallet(
        SAMPLE_ADDRESS, SAMPLE_WALLET_DATA, mock_redis, session=db_session
    )
    await wallet_registry.update_capital(
        SAMPLE_ADDRESS, 75_000.0, mock_redis, session=db_session
    )

    # Cache should be invalidated
    assert await mock_redis.get(_wallet_data_key(SAMPLE_ADDRESS)) is None

    # DB should have updated value
    result = await wallet_registry.get_wallet(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert result["total_capital_usdc"] == pytest.approx(75_000.0)


# ── 8. register_if_new ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_register_if_new_creates_wallet(db_session, mock_redis):
    created = await wallet_registry.register_if_new(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert created is True

    result = await wallet_registry.get_wallet(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert result is not None
    assert result["is_tracked"] is True


@pytest.mark.asyncio
async def test_register_if_new_is_idempotent(db_session, mock_redis):
    await wallet_registry.register_if_new(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    created_again = await wallet_registry.register_if_new(
        SAMPLE_ADDRESS, mock_redis, session=db_session
    )
    assert created_again is False


# ── 9. get_tracked_addresses ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_tracked_addresses_returns_only_tracked(db_session, mock_redis):
    addr1 = "0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    addr2 = "0xBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"

    await wallet_registry.upsert_wallet(
        addr1, {**SAMPLE_WALLET_DATA, "is_tracked": True}, mock_redis, session=db_session
    )
    await wallet_registry.upsert_wallet(
        addr2, {**SAMPLE_WALLET_DATA, "is_tracked": False}, mock_redis, session=db_session
    )

    tracked = await wallet_registry.get_tracked_addresses(mock_redis, session=db_session)
    assert addr1 in tracked
    assert addr2 not in tracked
