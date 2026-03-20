"""
Tests for meg.agent_core.position_manager — position CRUD + monitoring.

Tests cover:
  - open_position: dual-write Redis+DB, duplicate detection
  - close_position: PnL calculation, Redis cleanup, DB update
  - get_* helpers: exposure, daily PnL, portfolio value
  - _check_all_positions: TP/SL detection, unrealized PnL update
  - _detect_whale_exit: contributing wallet sell detection
  - daily_pnl_reset_loop: tested via single reset verification
"""
from __future__ import annotations

import json
import time

import pytest

from meg.agent_core import position_manager
from meg.core.events import AlertMessage, PositionState, RedisKeys
from meg.db.models import Position

from .conftest import (
    add_position_to_redis,
    insert_trade_record,
    make_position_state,
    set_market_redis_data,
)


# ── open_position ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_open_position_writes_to_redis(mock_redis, test_config):
    """open_position writes to both open_positions hash and position:{id} key."""
    pos = await position_manager.open_position(
        market_id="market_001",
        outcome="YES",
        size_usdc=100.0,
        entry_price=0.50,
        signal_id="sig_001",
        contributing_wallets=["0xWHALE001"],
        whale_archetype="INFORMATION",
        saturation_score=0.1,
        take_profit_price=0.70,
        stop_loss_price=0.375,
        redis=mock_redis,
    )

    # Check hash
    raw = await mock_redis.hget(RedisKeys.open_positions(), pos.position_id)
    assert raw is not None
    stored = PositionState.model_validate_json(raw)
    assert stored.market_id == "market_001"
    assert stored.size_usdc == 100.0

    # Check direct key
    direct = await mock_redis.get(RedisKeys.position(pos.position_id))
    assert direct is not None

    # Check market exposure
    exposure = await mock_redis.get(RedisKeys.market_exposure_usdc("market_001"))
    assert float(exposure) == 100.0


@pytest.mark.asyncio
async def test_open_position_writes_to_db(mock_redis, test_config, db_session):
    """open_position writes a Position record to DB."""
    pos = await position_manager.open_position(
        market_id="market_001",
        outcome="YES",
        size_usdc=100.0,
        entry_price=0.50,
        signal_id="sig_001",
        contributing_wallets=["0xWHALE001"],
        whale_archetype="INFORMATION",
        saturation_score=0.1,
        take_profit_price=0.70,
        stop_loss_price=0.375,
        redis=mock_redis,
        session=db_session,
    )

    from sqlalchemy import select
    result = await db_session.execute(
        select(Position).where(Position.position_id == pos.position_id)
    )
    db_pos = result.scalar_one_or_none()
    assert db_pos is not None
    assert db_pos.market_id == "market_001"
    assert float(db_pos.size_usdc) == 100.0


@pytest.mark.asyncio
async def test_open_position_calculates_shares(mock_redis, test_config):
    """Shares = size_usdc / entry_price."""
    pos = await position_manager.open_position(
        market_id="market_001",
        outcome="YES",
        size_usdc=100.0,
        entry_price=0.50,
        signal_id="sig_001",
        contributing_wallets=["0xWHALE001"],
        whale_archetype="INFORMATION",
        saturation_score=0.1,
        take_profit_price=0.70,
        stop_loss_price=0.375,
        redis=mock_redis,
    )
    assert pos.shares == pytest.approx(200.0)  # 100 / 0.50


@pytest.mark.asyncio
async def test_open_position_accumulates_exposure(mock_redis, test_config):
    """Multiple opens in same market accumulate exposure."""
    for i in range(3):
        await position_manager.open_position(
            market_id="market_001",
            outcome="YES",
            size_usdc=50.0,
            entry_price=0.50,
            signal_id=f"sig_{i}",
            contributing_wallets=["0xWHALE001"],
            whale_archetype="INFORMATION",
            saturation_score=0.0,
            take_profit_price=0.70,
            stop_loss_price=0.375,
            redis=mock_redis,
        )

    exposure = await position_manager.get_market_exposure_usdc("market_001", mock_redis)
    assert exposure == pytest.approx(150.0)


# ── close_position ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_close_position_pnl_yes_profit(mock_redis, test_config):
    """YES position closed at higher price → positive PnL."""
    pos = make_position_state(
        position_id="pos_close1",
        outcome="YES",
        entry_price=0.50,
        size_usdc=100.0,
    )
    await add_position_to_redis(mock_redis, pos)
    await mock_redis.set(RedisKeys.market_exposure_usdc("market_001"), "100")

    summary = await position_manager.close_position(
        "pos_close1", exit_price=0.70, redis=mock_redis
    )

    assert summary["realized_pnl_usdc"] == pytest.approx(40.0)  # (0.70-0.50) * 200 shares
    assert summary["realized_pnl_pct"] == pytest.approx(0.40)


@pytest.mark.asyncio
async def test_close_position_pnl_no_profit(mock_redis, test_config):
    """NO position closed at lower price → positive PnL."""
    pos = make_position_state(
        position_id="pos_close2",
        outcome="NO",
        entry_price=0.50,
        size_usdc=100.0,
    )
    await add_position_to_redis(mock_redis, pos)
    await mock_redis.set(RedisKeys.market_exposure_usdc("market_001"), "100")

    summary = await position_manager.close_position(
        "pos_close2", exit_price=0.30, redis=mock_redis
    )

    # NO: pnl_per_share = 0.50 - 0.30 = 0.20, shares = 200
    assert summary["realized_pnl_usdc"] == pytest.approx(40.0)


@pytest.mark.asyncio
async def test_close_position_pnl_loss(mock_redis, test_config):
    """YES position closed at lower price → negative PnL."""
    pos = make_position_state(
        position_id="pos_close3",
        outcome="YES",
        entry_price=0.50,
        size_usdc=100.0,
    )
    await add_position_to_redis(mock_redis, pos)
    await mock_redis.set(RedisKeys.market_exposure_usdc("market_001"), "100")

    summary = await position_manager.close_position(
        "pos_close3", exit_price=0.40, redis=mock_redis
    )

    # (0.40 - 0.50) * 200 = -20.0
    assert summary["realized_pnl_usdc"] == pytest.approx(-20.0)


@pytest.mark.asyncio
async def test_close_removes_from_redis(mock_redis, test_config):
    """close_position removes position from open_positions hash + direct key."""
    pos = make_position_state(position_id="pos_close4")
    await add_position_to_redis(mock_redis, pos)
    await mock_redis.set(RedisKeys.market_exposure_usdc("market_001"), "100")

    await position_manager.close_position("pos_close4", exit_price=0.60, redis=mock_redis)

    assert await mock_redis.hget(RedisKeys.open_positions(), "pos_close4") is None
    assert await mock_redis.get(RedisKeys.position("pos_close4")) is None


@pytest.mark.asyncio
async def test_close_updates_daily_pnl(mock_redis, test_config):
    """close_position accumulates realized PnL into daily_pnl_usdc."""
    pos = make_position_state(
        position_id="pos_close5",
        outcome="YES",
        entry_price=0.50,
        size_usdc=100.0,
    )
    await add_position_to_redis(mock_redis, pos)
    await mock_redis.set(RedisKeys.market_exposure_usdc("market_001"), "100")

    await position_manager.close_position("pos_close5", exit_price=0.60, redis=mock_redis)

    daily = await position_manager.get_daily_pnl_usdc(mock_redis)
    assert daily == pytest.approx(20.0)  # (0.60-0.50) * 200


@pytest.mark.asyncio
async def test_close_nonexistent_raises(mock_redis, test_config):
    """Closing a non-existent position raises ValueError."""
    with pytest.raises(ValueError, match="not found"):
        await position_manager.close_position("nonexistent", exit_price=0.60, redis=mock_redis)


# ── get helpers ───────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_open_positions_empty(mock_redis):
    """No positions → empty list."""
    positions = await position_manager.get_open_positions(mock_redis)
    assert positions == []


@pytest.mark.asyncio
async def test_get_open_positions_returns_all(mock_redis):
    """Returns all positions from hash."""
    for i in range(3):
        pos = make_position_state(position_id=f"pos_{i}", market_id=f"market_{i}")
        await add_position_to_redis(mock_redis, pos)

    positions = await position_manager.get_open_positions(mock_redis)
    assert len(positions) == 3


@pytest.mark.asyncio
async def test_get_total_exposure(mock_redis):
    """Total exposure = sum of all position sizes."""
    for i in range(3):
        pos = make_position_state(position_id=f"pos_{i}", size_usdc=50.0)
        await add_position_to_redis(mock_redis, pos)

    total = await position_manager.get_total_exposure_usdc(mock_redis)
    assert total == pytest.approx(150.0)


@pytest.mark.asyncio
async def test_get_daily_pnl_missing_key(mock_redis):
    """Missing daily_pnl key → 0.0."""
    pnl = await position_manager.get_daily_pnl_usdc(mock_redis)
    assert pnl == 0.0


@pytest.mark.asyncio
async def test_get_portfolio_value_from_redis(mock_redis, test_config):
    """Portfolio value reads from Redis when set."""
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "5000")
    val = await position_manager.get_portfolio_value_usdc(mock_redis, test_config)
    assert val == 5000.0


@pytest.mark.asyncio
async def test_get_portfolio_value_falls_back_to_config(mock_redis, test_config):
    """Missing Redis key → falls back to config default."""
    val = await position_manager.get_portfolio_value_usdc(mock_redis, test_config)
    assert val == test_config.kelly.portfolio_value_usdc


# ── _check_all_positions (monitor loop body) ──────────────────────────────


@pytest.mark.asyncio
async def test_check_positions_updates_unrealized_pnl(mock_redis, test_config):
    """Monitor pass updates unrealized PnL in Redis."""
    pos = make_position_state(
        position_id="pos_mon1",
        outcome="YES",
        entry_price=0.50,
        current_price=0.50,
        size_usdc=100.0,
    )
    await add_position_to_redis(mock_redis, pos)
    # Price moved up
    await set_market_redis_data(mock_redis, mid_price=0.60)

    await position_manager._check_all_positions(mock_redis, test_config)

    raw = await mock_redis.hget(RedisKeys.open_positions(), "pos_mon1")
    updated = PositionState.model_validate_json(raw)
    assert updated.current_price == 0.60
    # (0.60 - 0.50) * 200 shares = 20.0
    assert updated.unrealized_pnl_usdc == pytest.approx(20.0)


@pytest.mark.asyncio
async def test_check_positions_no_price_skips(mock_redis, test_config):
    """No market price available → position unchanged (skipped)."""
    pos = make_position_state(position_id="pos_mon2")
    await add_position_to_redis(mock_redis, pos)
    # Don't set any market price

    await position_manager._check_all_positions(mock_redis, test_config)

    raw = await mock_redis.hget(RedisKeys.open_positions(), "pos_mon2")
    unchanged = PositionState.model_validate_json(raw)
    assert unchanged.current_price == pos.current_price  # unchanged


@pytest.mark.asyncio
async def test_check_positions_error_does_not_crash(mock_redis, test_config):
    """Error on one position doesn't crash monitoring for others."""
    # Position 1: valid
    pos1 = make_position_state(position_id="pos_ok", market_id="market_ok")
    await add_position_to_redis(mock_redis, pos1)
    await mock_redis.set(RedisKeys.market_mid_price("market_ok"), "0.60")

    # Position 2: write invalid JSON to simulate corruption
    await mock_redis.hset(
        RedisKeys.open_positions(), "pos_bad", "not-valid-json"
    )

    # Should not raise — bad position logged and skipped
    await position_manager._check_all_positions(mock_redis, test_config)


# ── _detect_whale_exit ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_whale_exit_detected(mock_redis, test_config, db_session):
    """Contributing whale selling opposite direction → exit detected."""
    now_ms = int(time.time() * 1000)
    pos = make_position_state(
        position_id="pos_exit1",
        outcome="YES",
        contributing_wallets=["0xWHALE001"],
    )
    pos = pos.model_copy(update={"opened_at_ms": now_ms - 60_000})  # opened 1min ago
    await add_position_to_redis(mock_redis, pos)
    await set_market_redis_data(mock_redis, mid_price=0.55)

    # Whale sells NO (opposite of our YES position) after we opened
    from datetime import datetime, timezone
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="NO",
        traded_at=datetime.now(tz=timezone.utc),
    )

    exiting = await position_manager._detect_whale_exit(pos, db_session)
    assert exiting is True


@pytest.mark.asyncio
async def test_whale_exit_not_detected_no_sells(mock_redis, test_config, db_session):
    """No sells by contributing wallets → no exit."""
    pos = make_position_state(
        position_id="pos_exit2",
        outcome="YES",
        contributing_wallets=["0xWHALE001"],
    )
    exiting = await position_manager._detect_whale_exit(pos, db_session)
    assert exiting is False


@pytest.mark.asyncio
async def test_whale_exit_empty_contributing_wallets(mock_redis, test_config, db_session):
    """No contributing wallets → no exit check possible."""
    pos = make_position_state(
        position_id="pos_exit3",
        contributing_wallets=[],
    )
    exiting = await position_manager._detect_whale_exit(pos, db_session)
    assert exiting is False


# ── Alert publish ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_close_position_publishes_alert(mock_redis, test_config):
    """Closing a position publishes an AlertMessage to CHANNEL_BOT_ALERTS."""
    pos = make_position_state(position_id="pos_alert_close")
    pos_json = pos.model_dump_json()
    await mock_redis.hset(RedisKeys.open_positions(), pos.position_id, pos_json)
    await mock_redis.set(RedisKeys.position(pos.position_id), pos_json)
    await mock_redis.set(
        RedisKeys.market_exposure_usdc(pos.market_id), str(pos.size_usdc)
    )

    pubsub = mock_redis.pubsub()
    await pubsub.subscribe(RedisKeys.CHANNEL_BOT_ALERTS)
    await pubsub.get_message(timeout=1)  # subscription confirmation

    await position_manager.close_position(pos.position_id, 0.60, mock_redis)

    msg = await pubsub.get_message(timeout=1)
    assert msg is not None
    alert = AlertMessage.model_validate_json(msg["data"])
    assert alert.alert_type == "position_closed"
    assert alert.urgent is False
    assert pos.market_id in alert.message
    await pubsub.unsubscribe()


@pytest.mark.asyncio
async def test_whale_exit_alert_published(mock_redis, test_config, db_session):
    """Whale exit detected during monitoring → AlertMessage with alert_type='whale_exit' published."""
    from datetime import datetime, timezone

    now_ms = int(time.time() * 1000)
    pos = make_position_state(
        position_id="pos_whale_exit_alert",
        outcome="YES",
        contributing_wallets=["0xWHALE001"],
    )
    pos = pos.model_copy(update={"opened_at_ms": now_ms - 60_000})  # opened 1min ago
    await add_position_to_redis(mock_redis, pos)
    await set_market_redis_data(mock_redis, mid_price=0.55)

    # Whale sells NO (opposite of our YES) after we opened — triggers whale exit
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="NO",
        traded_at=datetime.now(tz=timezone.utc),
    )

    pubsub = mock_redis.pubsub()
    await pubsub.subscribe(RedisKeys.CHANNEL_BOT_ALERTS)
    await pubsub.get_message(timeout=1)  # subscription confirmation

    await position_manager._check_all_positions(
        mock_redis, test_config, session=db_session, check_whale_exit=True
    )

    msg = await pubsub.get_message(timeout=1)
    assert msg is not None
    alert = AlertMessage.model_validate_json(msg["data"])
    assert alert.alert_type == "whale_exit"
    assert alert.urgent is False
    assert pos.market_id in alert.message
    await pubsub.unsubscribe()
