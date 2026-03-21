"""
Tests for MEG Dashboard API — GET /api/v1/* and SSE feed.

All tests use the api_client fixture (httpx + FakeRedis + SQLite).
DB rows are seeded within each test using a separate session on the same
StaticPool engine — StaticPool shares one connection, so committed rows are
immediately visible to the endpoint's session.

Coverage:
  - GET /api/v1/positions   (2 tests)
  - GET /api/v1/signals     (2 tests)
  - GET /api/v1/whales      (2 tests)
  - GET /api/v1/markets     (3 tests)
  - GET /api/v1/status      (2 tests)
  - GET /api/v1/feed/signals (1 test — headers + connection comment)
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.events import PositionState, RedisKeys
from meg.dashboard.api.main import app, get_redis
from meg.db.models import SignalOutcome, Wallet


# ── helpers ───────────────────────────────────────────────────────────────────


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def make_position(market_id: str = "MKT-001", outcome: str = "YES") -> PositionState:
    now_ms = int(time.time() * 1000)
    return PositionState(
        position_id=f"pos-{market_id}",
        market_id=market_id,
        outcome=outcome,
        entry_price=0.55,
        current_price=0.62,
        size_usdc=100.0,
        shares=181.8,
        entry_signal_id="sig-001",
        opened_at_ms=now_ms,
        take_profit_price=0.75,
        stop_loss_price=0.40,
    )


def make_signal(signal_id: str = "sig-001", status: str = "EXECUTED") -> SignalOutcome:
    return SignalOutcome(
        signal_id=signal_id,
        market_id="MKT-001",
        outcome="YES",
        composite_score=0.72,
        recommended_size_usdc=120.0,
        kelly_fraction=0.08,
        scores_json={},
        status=status,
        triggering_wallet="0x" + "a" * 40,
        market_price_at_signal=0.54,
        fired_at=_utcnow(),
    )


def make_wallet(address: str = "0x" + "b" * 40, score: float = 0.85) -> Wallet:
    return Wallet(
        address=address,
        archetype="INFORMATION",
        is_qualified=True,
        composite_whale_score=score,
        win_rate=0.71,
        avg_lead_time_hours=6.2,
        roi_30d=0.14,
        roi_90d=0.31,
        roi_all_time=0.55,
        total_closed_positions=42,
        consistency_score=0.68,
        avg_conviction_ratio=0.24,
        reputation_decay_factor=0.95,
        category_scores={},
    )


async def _seed(db_engine, *objects) -> None:
    """Insert rows and commit so the endpoint's session can read them."""
    async with AsyncSession(db_engine, expire_on_commit=False) as session:
        async with session.begin():
            for obj in objects:
                session.add(obj)


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/positions
# ═══════════════════════════════════════════════════════════════════════


async def test_get_positions_empty(api_client):
    """Empty Redis hash → empty list."""
    response = await api_client.get("/api/v1/positions")
    assert response.status_code == 200
    assert response.json() == {"positions": []}


async def test_get_positions_returns_open_positions(api_client, fake_redis):
    """Position stored in Redis hash is returned with all state fields."""
    pos = make_position("MKT-777", "YES")
    await fake_redis.hset(RedisKeys.open_positions(), pos.position_id, pos.model_dump_json())

    response = await api_client.get("/api/v1/positions")
    assert response.status_code == 200
    positions = response.json()["positions"]
    assert len(positions) == 1
    assert positions[0]["market_id"] == "MKT-777"
    assert positions[0]["outcome"] == "YES"
    assert positions[0]["entry_price"] == pytest.approx(0.55)


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/signals
# ═══════════════════════════════════════════════════════════════════════


async def test_get_signals_empty(api_client):
    """Empty DB → empty list."""
    response = await api_client.get("/api/v1/signals")
    assert response.status_code == 200
    assert response.json() == {"signals": []}


async def test_get_signals_returns_recent(api_client, db_engine):
    """Signal row in DB is returned with correct fields serialised."""
    await _seed(db_engine, make_signal("sig-test", "EXECUTED"))

    response = await api_client.get("/api/v1/signals")
    assert response.status_code == 200
    signals = response.json()["signals"]
    assert len(signals) == 1
    s = signals[0]
    assert s["signal_id"] == "sig-test"
    assert s["status"] == "EXECUTED"
    assert s["market_id"] == "MKT-001"
    assert s["composite_score"] == pytest.approx(0.72)
    assert "fired_at" in s


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/whales
# ═══════════════════════════════════════════════════════════════════════


async def test_get_whales_empty(api_client):
    """No qualified wallets in DB → empty list."""
    response = await api_client.get("/api/v1/whales")
    assert response.status_code == 200
    assert response.json() == {"whales": []}


async def test_get_whales_returns_qualified(api_client, db_engine):
    """Qualified wallet is returned; unqualified wallet is excluded."""
    qualified = make_wallet("0x" + "c" * 40, score=0.88)
    unqualified = make_wallet("0x" + "d" * 40, score=0.91)
    unqualified.is_qualified = False

    await _seed(db_engine, qualified, unqualified)

    response = await api_client.get("/api/v1/whales")
    assert response.status_code == 200
    whales = response.json()["whales"]
    assert len(whales) == 1
    assert whales[0]["address"] == "0x" + "c" * 40
    assert whales[0]["archetype"] == "INFORMATION"
    assert whales[0]["composite_whale_score"] == pytest.approx(0.88)


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/markets
# ═══════════════════════════════════════════════════════════════════════


async def test_get_markets_empty(api_client):
    """No active markets in Redis → empty list."""
    response = await api_client.get("/api/v1/markets")
    assert response.status_code == 200
    assert response.json() == {"markets": []}


async def test_get_markets_returns_market_state(api_client, fake_redis):
    """Market registered in active set with state keys is returned fully."""
    mid = "MKT-ACTIVE"
    await fake_redis.sadd(RedisKeys.active_markets(), mid)
    await fake_redis.set(RedisKeys.market_mid_price(mid), "0.55")
    await fake_redis.set(RedisKeys.market_bid(mid), "0.54")
    await fake_redis.set(RedisKeys.market_ask(mid), "0.56")
    await fake_redis.set(RedisKeys.market_spread(mid), "0.02")
    await fake_redis.set(RedisKeys.market_volume_24h(mid), "12500.0")
    await fake_redis.set(RedisKeys.market_liquidity(mid), "8000.0")
    await fake_redis.set(RedisKeys.market_participants(mid), "134")
    await fake_redis.set(RedisKeys.market_last_updated_ms(mid), "1711000000000")

    response = await api_client.get("/api/v1/markets")
    assert response.status_code == 200
    markets = response.json()["markets"]
    assert len(markets) == 1
    m = markets[0]
    assert m["market_id"] == mid
    assert m["mid_price"] == pytest.approx(0.55)
    assert m["bid"] == pytest.approx(0.54)
    assert m["participants"] == 134
    assert m["last_updated_ms"] == 1711000000000


async def test_get_markets_partial_redis_keys(api_client, fake_redis):
    """Market with some keys missing returns None for those fields, not an error."""
    mid = "MKT-SPARSE"
    await fake_redis.sadd(RedisKeys.active_markets(), mid)
    await fake_redis.set(RedisKeys.market_mid_price(mid), "0.48")
    # bid, ask, spread, etc. are absent

    response = await api_client.get("/api/v1/markets")
    assert response.status_code == 200
    markets = response.json()["markets"]
    assert len(markets) == 1
    assert markets[0]["mid_price"] == pytest.approx(0.48)
    assert markets[0]["bid"] is None
    assert markets[0]["participants"] is None


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/status
# ═══════════════════════════════════════════════════════════════════════


async def test_get_status_defaults(api_client):
    """Empty Redis → not paused, zero P&L, null block, default paper mode."""
    response = await api_client.get("/api/v1/status")
    assert response.status_code == 200
    status = response.json()
    assert status["is_paused"] is False
    assert status["daily_pnl_usdc"] == pytest.approx(0.0)
    assert status["last_block_processed"] is None


async def test_get_status_paused_with_pnl(api_client, fake_redis):
    """is_paused true when key exists; daily_pnl and last_block populated."""
    await fake_redis.set(RedisKeys.system_paused(), "1")
    await fake_redis.set(RedisKeys.daily_pnl_usdc(), "47.32")
    await fake_redis.set(RedisKeys.last_processed_block(), "68234891")

    response = await api_client.get("/api/v1/status")
    assert response.status_code == 200
    status = response.json()
    assert status["is_paused"] is True
    assert status["daily_pnl_usdc"] == pytest.approx(47.32)
    assert status["last_block_processed"] == 68234891


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/feed/signals — SSE
# ═══════════════════════════════════════════════════════════════════════


async def test_feed_signals_sse_headers_and_connection(fake_redis, monkeypatch):
    """
    SSE endpoint returns text/event-stream, no-cache header, and sends the
    initial ': connected' comment.

    pubsub.get_message is mocked to raise immediately on first call so the
    generator exits after sending ': connected'. This lets us use client.get()
    (non-streaming) to assert the full response body without hanging.

    Root cause of the hang if using real FakeRedis: get_message() returns None
    instantly → tight infinite loop → GeneratorExit never delivered cleanly.
    """
    from unittest.mock import MagicMock

    mock_pubsub = MagicMock()
    mock_pubsub.subscribe = AsyncMock()
    mock_pubsub.get_message = AsyncMock(side_effect=ConnectionError("test_end"))
    mock_pubsub.unsubscribe = AsyncMock()
    mock_pubsub.aclose = AsyncMock()

    mock_sse_client = MagicMock()
    mock_sse_client.pubsub = MagicMock(return_value=mock_pubsub)
    mock_sse_client.aclose = AsyncMock()

    monkeypatch.setattr(
        "meg.dashboard.api.main.create_redis_client",
        AsyncMock(return_value=mock_sse_client),
    )
    app.dependency_overrides[get_redis] = lambda: fake_redis

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Non-streaming GET: the stream ends as soon as get_message raises,
            # so httpx collects the full (short) body and returns.
            response = await client.get("/api/v1/feed/signals")

        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        assert response.headers["cache-control"] == "no-cache"
        assert b": connected" in response.content
    finally:
        app.dependency_overrides.clear()
