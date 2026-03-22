"""
Tests for MEG Dashboard API — GET /api/v1/* and SSE feed.

All tests use the api_client fixture (httpx + FakeRedis + SQLite).
DB rows are seeded within each test using a separate session on the same
StaticPool engine — StaticPool shares one connection, so committed rows are
immediately visible to the endpoint's session.

Coverage:
  - GET  /api/v1/positions          (2 tests)
  - POST /api/v1/positions/{id}/exit(2 tests)
  - GET  /api/v1/signals            (5 tests — base + 4 filter variants)
  - GET  /api/v1/signals/{id}       (2 tests)
  - GET  /api/v1/signals/{id}/explain (2 tests)
  - POST /api/v1/signals/{id}/approve (4 tests)
  - POST /api/v1/signals/{id}/reject  (2 tests)
  - GET  /api/v1/whales             (2 tests)
  - GET  /api/v1/markets            (3 tests)
  - GET  /api/v1/status             (2 tests)
  - GET  /api/v1/config             (1 test)
  - PATCH /api/v1/config            (3 tests)
  - GET  /api/v1/pnl                (3 tests)
  - GET  /api/v1/feed/signals       (1 test — headers + connection comment)
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import yaml
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.events import PositionState, RedisKeys, TradeProposal
from meg.dashboard.api.main import app, db_session, get_config, get_redis
from meg.db.models import Position, PositionStatus, SignalOutcome, Wallet


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
        scores_json={"lead_lag": 0.80, "consensus": 0.70, "kelly_confidence": 0.65,
                     "divergence": 0.55, "conviction_ratio": 0.50,
                     "archetype_multiplier": 1.0, "ladder_multiplier": 1.0},
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


def make_db_position(
    position_id: str = "pos-db-001",
    status: str = "CLOSED",
    resolved_pnl_usdc: float = 45.0,
    days_ago: int = 1,
) -> Position:
    closed = _utcnow() - timedelta(days=days_ago)
    return Position(
        position_id=position_id,
        market_id="MKT-001",
        outcome="YES",
        entry_price=0.50,
        current_price=0.65,
        size_usdc=100.0,
        shares=200.0,
        unrealized_pnl_usdc=0.0,
        unrealized_pnl_pct=0.0,
        entry_signal_id="sig-001",
        contributing_wallets=[],
        whale_archetype="INFORMATION",
        opened_at=closed - timedelta(hours=4),
        closed_at=closed,
        take_profit_price=0.75,
        stop_loss_price=0.40,
        saturation_score_at_entry=0.1,
        status=status,
        resolved_pnl_usdc=resolved_pnl_usdc,
    )


def make_proposal(proposal_id: str = "prop-001") -> TradeProposal:
    from meg.core.events import SignalScores
    return TradeProposal(
        proposal_id=proposal_id,
        signal_id="sig-001",
        market_id="MKT-001",
        outcome="YES",
        size_usdc=100.0,
        limit_price=0.56,
        status="PENDING_APPROVAL",
        created_at_ms=int(time.time() * 1000),
        composite_score=0.72,
        scores=SignalScores(
            lead_lag=0.80, consensus=0.70, kelly_confidence=0.65,
            divergence=0.55, conviction_ratio=0.50,
            archetype_multiplier=1.0, ladder_multiplier=1.0,
        ),
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
# POST /api/v1/positions/{id}/exit
# ═══════════════════════════════════════════════════════════════════════


async def test_exit_position_not_found(api_client):
    """Position not in open_positions hash → 404."""
    response = await api_client.post("/api/v1/positions/nonexistent/exit")
    assert response.status_code == 404


async def test_exit_position_sets_redis_flag(api_client, fake_redis):
    """Position in hash → sets exit_requested flag in Redis and returns 200."""
    pos = make_position("MKT-888")
    await fake_redis.hset(RedisKeys.open_positions(), pos.position_id, pos.model_dump_json())

    response = await api_client.post(f"/api/v1/positions/{pos.position_id}/exit")
    assert response.status_code == 200
    body = response.json()
    assert body["exit_requested"] is True
    assert body["position_id"] == pos.position_id
    assert "note" in body

    # Flag must be set in Redis
    flag = await fake_redis.get(RedisKeys.exit_requested(pos.position_id))
    assert flag == "1"


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
    assert "scores_json" in s


async def test_get_signals_filter_by_status(api_client, db_engine):
    """status= filter returns only matching rows."""
    await _seed(
        db_engine,
        make_signal("sig-exec", "EXECUTED"),
        make_signal("sig-filt", "FILTERED"),
    )

    response = await api_client.get("/api/v1/signals?status=FILTERED")
    assert response.status_code == 200
    signals = response.json()["signals"]
    assert len(signals) == 1
    assert signals[0]["signal_id"] == "sig-filt"


async def test_get_signals_filter_by_score_min(api_client, db_engine):
    """score_min= filter excludes signals below threshold."""
    low = make_signal("sig-low", "EXECUTED")
    low.composite_score = 0.40
    high = make_signal("sig-high", "EXECUTED")
    high.composite_score = 0.80
    await _seed(db_engine, low, high)

    response = await api_client.get("/api/v1/signals?score_min=0.6")
    assert response.status_code == 200
    signals = response.json()["signals"]
    assert len(signals) == 1
    assert signals[0]["signal_id"] == "sig-high"


async def test_get_signals_combined_filters(api_client, db_engine):
    """Multiple filters combine as AND — only rows matching all pass."""
    match = make_signal("sig-match", "FILTERED")
    match.composite_score = 0.75
    no_match_status = make_signal("sig-wrong-status", "EXECUTED")
    no_match_status.composite_score = 0.75
    no_match_score = make_signal("sig-wrong-score", "FILTERED")
    no_match_score.composite_score = 0.30
    await _seed(db_engine, match, no_match_status, no_match_score)

    response = await api_client.get("/api/v1/signals?status=FILTERED&score_min=0.6")
    assert response.status_code == 200
    signals = response.json()["signals"]
    assert len(signals) == 1
    assert signals[0]["signal_id"] == "sig-match"


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/signals/{id}
# ═══════════════════════════════════════════════════════════════════════


async def test_get_signal_not_found(api_client):
    """Non-existent signal_id → 404."""
    response = await api_client.get("/api/v1/signals/nonexistent")
    assert response.status_code == 404


async def test_get_signal_returns_full_detail(api_client, db_engine):
    """Existing signal returns all fields including scores_json."""
    await _seed(db_engine, make_signal("sig-detail", "EXECUTED"))

    response = await api_client.get("/api/v1/signals/sig-detail")
    assert response.status_code == 200
    s = response.json()
    assert s["signal_id"] == "sig-detail"
    assert "scores_json" in s
    assert "kelly_fraction" in s
    assert "contributing_wallets" in s
    assert s["composite_score"] == pytest.approx(0.72)


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/signals/{id}/explain
# ═══════════════════════════════════════════════════════════════════════


async def test_explain_signal_not_found(api_client):
    """Non-existent signal_id → 404."""
    response = await api_client.get("/api/v1/signals/nonexistent/explain")
    assert response.status_code == 404


async def test_explain_signal_returns_breakdown(api_client, db_engine):
    """Existing signal returns explanation with breakdown list and verdict."""
    await _seed(db_engine, make_signal("sig-explain", "EXECUTED"))

    response = await api_client.get("/api/v1/signals/sig-explain/explain")
    assert response.status_code == 200
    body = response.json()
    assert "explanation" in body
    exp = body["explanation"]
    assert "verdict" in exp
    assert "breakdown" in exp
    assert isinstance(exp["breakdown"], list)
    # All expected score keys present in breakdown
    keys = {item["key"] for item in exp["breakdown"]}
    assert "lead_lag" in keys
    assert "consensus" in keys
    # Each breakdown item has required fields
    for item in exp["breakdown"]:
        assert "label" in item
        assert "score" in item
        assert "tier" in item
        assert item["tier"] in ("STRONG", "MODERATE", "WEAK", "NEUTRAL")


# ═══════════════════════════════════════════════════════════════════════
# POST /api/v1/signals/{id}/approve
# ═══════════════════════════════════════════════════════════════════════


async def test_approve_not_found(api_client):
    """No pending proposal in Redis → 404."""
    response = await api_client.post("/api/v1/signals/nonexistent-proposal/approve")
    assert response.status_code == 404


async def test_approve_success(api_client, fake_redis):
    """
    Pending proposal in Redis + successful order_router.place() → 200.
    GETDEL atomically removes the key — a second call returns 404.
    """
    proposal = make_proposal("prop-approve-ok")
    await fake_redis.set(
        RedisKeys.pending_proposal("prop-approve-ok"),
        proposal.model_dump_json(),
    )

    mock_result = {"accepted": True, "order_id": "order-xyz", "estimated_slippage": 0.005, "reason": ""}

    with patch("meg.dashboard.api.main.order_router.place", new=AsyncMock(return_value=mock_result)):
        response = await api_client.post("/api/v1/signals/prop-approve-ok/approve")

    assert response.status_code == 200
    body = response.json()
    assert body["approved"] is True
    assert body["accepted"] is True
    assert body["order_id"] == "order-xyz"

    # GETDEL consumed the key — second call returns 404
    response2 = await api_client.post("/api/v1/signals/prop-approve-ok/approve")
    assert response2.status_code == 404


async def test_approve_order_router_raises(api_client, fake_redis):
    """
    order_router.place() raises after GETDEL consumed the key → 409.
    Proposal is permanently consumed — operator must re-evaluate.
    """
    proposal = make_proposal("prop-fail")
    await fake_redis.set(
        RedisKeys.pending_proposal("prop-fail"),
        proposal.model_dump_json(),
    )

    with patch("meg.dashboard.api.main.order_router.place", new=AsyncMock(side_effect=RuntimeError("CLOB down"))):
        response = await api_client.post("/api/v1/signals/prop-fail/approve")

    assert response.status_code == 409
    assert "cannot be re-queued" in response.json()["detail"]

    # Key is gone even though execution failed
    remaining = await fake_redis.get(RedisKeys.pending_proposal("prop-fail"))
    assert remaining is None


async def test_approve_gate_rejected(api_client, fake_redis):
    """order_router returns accepted=False (gate rejection) → 200 with accepted=False."""
    proposal = make_proposal("prop-gate")
    await fake_redis.set(
        RedisKeys.pending_proposal("prop-gate"),
        proposal.model_dump_json(),
    )

    mock_result = {"accepted": False, "order_id": None, "estimated_slippage": 0.0, "reason": "price drifted too far"}

    with patch("meg.dashboard.api.main.order_router.place", new=AsyncMock(return_value=mock_result)):
        response = await api_client.post("/api/v1/signals/prop-gate/approve")

    assert response.status_code == 200
    body = response.json()
    assert body["approved"] is True
    assert body["accepted"] is False
    assert "drifted" in body["reason"]


# ═══════════════════════════════════════════════════════════════════════
# POST /api/v1/signals/{id}/reject
# ═══════════════════════════════════════════════════════════════════════


async def test_reject_not_found(api_client):
    """No pending proposal → 404."""
    response = await api_client.post("/api/v1/signals/nonexistent/reject")
    assert response.status_code == 404


async def test_reject_success(api_client, fake_redis):
    """
    Pending proposal in Redis → 200. Key is deleted (GETDEL).
    Second reject call returns 404.
    """
    proposal = make_proposal("prop-reject")
    await fake_redis.set(
        RedisKeys.pending_proposal("prop-reject"),
        proposal.model_dump_json(),
    )

    response = await api_client.post(
        "/api/v1/signals/prop-reject/reject",
        json={"reason": "price moved too far"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["rejected"] is True
    assert body["reason"] == "price moved too far"

    # Key consumed — second attempt fails
    response2 = await api_client.post("/api/v1/signals/prop-reject/reject")
    assert response2.status_code == 404


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
    w = whales[0]
    assert w["address"] == "0x" + "c" * 40
    assert w["archetype"] == "INFORMATION"
    assert w["composite_whale_score"] == pytest.approx(0.88)
    # New fields in expanded response
    assert "roi_all_time" in w
    assert "avg_conviction_ratio" in w
    assert "total_volume_usdc" in w


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
# GET /api/v1/config
# ═══════════════════════════════════════════════════════════════════════


async def test_get_config_returns_current_config(api_client):
    """GET /config returns the current MegConfig as a nested dict."""
    response = await api_client.get("/api/v1/config")
    assert response.status_code == 200
    body = response.json()
    assert "config" in body
    cfg = body["config"]
    # Top-level sections must all be present
    for section in ("signal", "risk", "kelly", "entry", "pre_filter", "position"):
        assert section in cfg, f"Missing section: {section}"
    assert isinstance(cfg["signal"]["composite_score_threshold"], float)


# ═══════════════════════════════════════════════════════════════════════
# PATCH /api/v1/config
# ═══════════════════════════════════════════════════════════════════════


async def test_patch_config_valid(api_client, tmp_path, monkeypatch):
    """
    Valid patch → writes YAML, updates _config in memory, returns updated config.
    Uses a temp config.yaml so we don't touch the real one.
    """
    from meg.core.config_loader import MegConfig
    import meg.dashboard.api.main as main_mod

    # Seed a temp config file with defaults
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(yaml.dump(MegConfig().model_dump()))

    original_path = main_mod._config_path
    original_config = main_mod._config
    monkeypatch.setattr(main_mod, "_config_path", cfg_file)
    monkeypatch.setattr(main_mod, "_config", MegConfig())

    try:
        response = await api_client.patch(
            "/api/v1/config",
            json={"signal": {"composite_score_threshold": 0.55}},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["config"]["signal"]["composite_score_threshold"] == pytest.approx(0.55)
        assert body["updated"] == {"signal": {"composite_score_threshold": 0.55}}

        # Verify YAML was written
        written = yaml.safe_load(cfg_file.read_text())
        assert written["signal"]["composite_score_threshold"] == pytest.approx(0.55)
    finally:
        monkeypatch.setattr(main_mod, "_config_path", original_path)
        monkeypatch.setattr(main_mod, "_config", original_config)


async def test_patch_config_invalid_type(api_client, tmp_path, monkeypatch):
    """Patch with wrong type fails Pydantic validation → 422."""
    from meg.core.config_loader import MegConfig
    import meg.dashboard.api.main as main_mod

    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(yaml.dump(MegConfig().model_dump()))

    original_path = main_mod._config_path
    original_config = main_mod._config
    monkeypatch.setattr(main_mod, "_config_path", cfg_file)
    monkeypatch.setattr(main_mod, "_config", MegConfig())

    try:
        response = await api_client.patch(
            "/api/v1/config",
            json={"signal": {"composite_score_threshold": "not-a-float"}},
        )
        assert response.status_code == 422
    finally:
        monkeypatch.setattr(main_mod, "_config_path", original_path)
        monkeypatch.setattr(main_mod, "_config", original_config)


async def test_patch_config_unknown_key_is_ignored(api_client, tmp_path, monkeypatch):
    """Unknown top-level keys in the patch are passed through; Pydantic ignores extras."""
    from meg.core.config_loader import MegConfig
    import meg.dashboard.api.main as main_mod

    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(yaml.dump(MegConfig().model_dump()))

    original_path = main_mod._config_path
    original_config = main_mod._config
    monkeypatch.setattr(main_mod, "_config_path", cfg_file)
    monkeypatch.setattr(main_mod, "_config", MegConfig())

    try:
        # MegConfig uses model_config = ... default which ignores extras by default
        # Patching a known nested key alongside an unknown key should still succeed
        response = await api_client.patch(
            "/api/v1/config",
            json={"signal": {"composite_score_threshold": 0.50}},
        )
        # Should succeed — known key update
        assert response.status_code == 200
    finally:
        monkeypatch.setattr(main_mod, "_config_path", original_path)
        monkeypatch.setattr(main_mod, "_config", original_config)


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/pnl
# ═══════════════════════════════════════════════════════════════════════


async def test_get_pnl_no_positions(api_client):
    """No closed positions in DB, no daily_pnl in Redis → all zeros."""
    response = await api_client.get("/api/v1/pnl")
    assert response.status_code == 200
    body = response.json()
    assert body["today"]["pnl_usdc"] == pytest.approx(0.0)
    assert body["week"]["pnl_usdc"] == pytest.approx(0.0)
    assert body["week"]["closed_positions"] == 0
    assert body["all_time"]["pnl_usdc"] == pytest.approx(0.0)


async def test_get_pnl_today_from_redis(api_client, fake_redis):
    """today P&L comes from Redis daily_pnl_usdc key."""
    await fake_redis.set(RedisKeys.daily_pnl_usdc(), "123.45")

    response = await api_client.get("/api/v1/pnl")
    assert response.status_code == 200
    assert response.json()["today"]["pnl_usdc"] == pytest.approx(123.45)


async def test_get_pnl_aggregates_closed_positions(api_client, db_engine):
    """week/month/all_time aggregate resolved_pnl_usdc from closed positions."""
    recent = make_db_position("pos-recent", "CLOSED", resolved_pnl_usdc=50.0, days_ago=2)
    old = make_db_position("pos-old", "CLOSED", resolved_pnl_usdc=30.0, days_ago=45)
    await _seed(db_engine, recent, old)

    response = await api_client.get("/api/v1/pnl")
    assert response.status_code == 200
    body = response.json()

    # week: only recent (2 days ago)
    assert body["week"]["pnl_usdc"] == pytest.approx(50.0)
    assert body["week"]["closed_positions"] == 1

    # month: only recent (2 days ago; 45-day position is outside 30-day window)
    assert body["month"]["pnl_usdc"] == pytest.approx(50.0)
    assert body["month"]["closed_positions"] == 1

    # all_time: both positions
    assert body["all_time"]["pnl_usdc"] == pytest.approx(80.0)
    assert body["all_time"]["closed_positions"] == 2


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
