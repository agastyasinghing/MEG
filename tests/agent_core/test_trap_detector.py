"""
Tests for meg.agent_core.trap_detector — pump-and-exit detection (PRD §9.4.2).

Detection logic:
  1. Find triggering wallet's entry trade in this market
  2. Find all opposite-direction trades within trap_window_minutes
  3. If total_sold >= entry_size * trap_exit_threshold → TRAP
  4. Write WhaleTrapEvent, publish penalty, check MANIPULATOR threshold
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from meg.agent_core import trap_detector
from meg.core.events import RedisKeys
from meg.db.models import WhaleTrapEvent

import pytest_asyncio

from .conftest import insert_trade_record, insert_wallet, make_signal_event


@pytest_asyncio.fixture(autouse=True)
async def _create_test_wallet(db_session):
    """Auto-create the default test wallet for FK constraints on WhaleTrapEvent."""
    await insert_wallet(db_session, address="0xWHALE001")


# ── No trap scenarios ─────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_no_entry_trade_returns_safe(mock_redis, test_config, db_session):
    """No entry trade found → (False, '') — can't detect trap without reference."""
    signal = make_signal_event(triggering_wallet="0xUNKNOWN")
    is_trap, reason = await trap_detector.check(signal, mock_redis, test_config, db_session)
    assert is_trap is False
    assert reason == ""


@pytest.mark.asyncio
async def test_no_sells_returns_safe(mock_redis, test_config, db_session):
    """Entry trade found but no sells → (False, '')."""
    now = datetime.now(tz=timezone.utc)
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        size_usdc=10_000,
        traded_at=now,
    )
    signal = make_signal_event(triggering_wallet="0xWHALE001", market_id="market_001")
    is_trap, reason = await trap_detector.check(signal, mock_redis, test_config, db_session)
    assert is_trap is False


@pytest.mark.asyncio
async def test_sells_below_threshold_returns_safe(mock_redis, test_config, db_session):
    """Sells exist but below trap_exit_threshold → (False, '')."""
    now = datetime.now(tz=timezone.utc)
    # Entry: 10,000 USDC YES
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        size_usdc=10_000,
        traded_at=now,
    )
    # Sell: 3,000 USDC NO (30% of entry, threshold is 50%)
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="NO",
        size_usdc=3_000,
        traded_at=now + timedelta(minutes=10),
    )
    signal = make_signal_event(triggering_wallet="0xWHALE001", market_id="market_001")
    is_trap, reason = await trap_detector.check(signal, mock_redis, test_config, db_session)
    assert is_trap is False


# ── Trap detected ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_trap_detected_above_threshold(mock_redis, test_config, db_session):
    """Sells >= entry * exit_threshold → trap detected."""
    now = datetime.now(tz=timezone.utc)
    # Entry: 10,000 USDC YES
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        size_usdc=10_000,
        traded_at=now,
    )
    # Sell: 6,000 USDC NO (60% of entry, threshold is 50%)
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="NO",
        size_usdc=6_000,
        traded_at=now + timedelta(minutes=10),
    )
    signal = make_signal_event(triggering_wallet="0xWHALE001", market_id="market_001")
    is_trap, reason = await trap_detector.check(signal, mock_redis, test_config, db_session)
    assert is_trap is True
    assert "whale_trap" in reason


@pytest.mark.asyncio
async def test_trap_writes_event_to_db(mock_redis, test_config, db_session):
    """Trap detection writes a WhaleTrapEvent record."""
    now = datetime.now(tz=timezone.utc)
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        size_usdc=10_000,
        traded_at=now,
    )
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="NO",
        size_usdc=6_000,
        traded_at=now + timedelta(minutes=10),
    )
    signal = make_signal_event(triggering_wallet="0xWHALE001", market_id="market_001")
    await trap_detector.check(signal, mock_redis, test_config, db_session)

    from sqlalchemy import select
    result = await db_session.execute(
        select(WhaleTrapEvent).where(WhaleTrapEvent.wallet_address == "0xWHALE001")
    )
    events = result.scalars().all()
    assert len(events) == 1
    assert float(events[0].pump_size_usdc) == 10_000
    assert float(events[0].exit_size_usdc) == 6_000
    assert events[0].confidence_score == pytest.approx(0.6, abs=0.01)


@pytest.mark.asyncio
async def test_trap_publishes_penalty_event(mock_redis, test_config, db_session):
    """Trap detection publishes a wallet penalty event to Redis."""
    now = datetime.now(tz=timezone.utc)
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        size_usdc=10_000,
        traded_at=now,
    )
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="NO",
        size_usdc=6_000,
        traded_at=now + timedelta(minutes=10),
    )

    # Subscribe to penalty channel before publishing
    pubsub = mock_redis.pubsub()
    await pubsub.subscribe(RedisKeys.CHANNEL_WALLET_PENALTIES)
    # Consume the subscription confirmation message
    await pubsub.get_message(timeout=1)

    signal = make_signal_event(triggering_wallet="0xWHALE001", market_id="market_001")
    await trap_detector.check(signal, mock_redis, test_config, db_session)

    # Check for penalty message
    msg = await pubsub.get_message(timeout=1)
    assert msg is not None
    data = json.loads(msg["data"])
    assert data["wallet_address"] == "0xWHALE001"
    assert data["penalty"] == test_config.agent.trap_score_penalty
    await pubsub.unsubscribe()


@pytest.mark.asyncio
async def test_sells_outside_window_ignored(mock_redis, test_config, db_session):
    """Sells outside trap_window_minutes are not counted."""
    now = datetime.now(tz=timezone.utc)
    window = test_config.agent.trap_window_minutes  # 30 minutes
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        size_usdc=10_000,
        traded_at=now,
    )
    # Sell AFTER the window (31 minutes later)
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="NO",
        size_usdc=8_000,
        traded_at=now + timedelta(minutes=window + 1),
    )
    signal = make_signal_event(triggering_wallet="0xWHALE001", market_id="market_001")
    is_trap, reason = await trap_detector.check(signal, mock_redis, test_config, db_session)
    assert is_trap is False


@pytest.mark.asyncio
async def test_multiple_sells_sum_to_threshold(mock_redis, test_config, db_session):
    """Multiple small sells that sum above threshold → trap detected."""
    now = datetime.now(tz=timezone.utc)
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        size_usdc=10_000,
        traded_at=now,
    )
    # 3 sells: 2000 + 2000 + 2000 = 6000 (60% > 50% threshold)
    for i in range(3):
        await insert_trade_record(
            db_session,
            wallet_address="0xWHALE001",
            market_id="market_001",
            outcome="NO",
            size_usdc=2_000,
            traded_at=now + timedelta(minutes=5 + i),
        )
    signal = make_signal_event(triggering_wallet="0xWHALE001", market_id="market_001")
    is_trap, reason = await trap_detector.check(signal, mock_redis, test_config, db_session)
    assert is_trap is True


# ── MANIPULATOR flagging ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_manipulator_flag_on_threshold(mock_redis, test_config, db_session):
    """After trap_manipulator_threshold trap events → publishes MANIPULATOR flag."""
    now = datetime.now(tz=timezone.utc)
    threshold = test_config.agent.trap_manipulator_threshold  # 3

    # Pre-insert trap events to bring count to threshold - 1
    for i in range(threshold - 1):
        trap_event = WhaleTrapEvent(
            wallet_address="0xWHALE001",
            market_id=f"market_{i}",
            pump_size_usdc=10_000,
            exit_size_usdc=6_000,
            confidence_score=0.6,
        )
        db_session.add(trap_event)
    await db_session.flush()

    # Now trigger one more trap
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_final",
        outcome="YES",
        size_usdc=10_000,
        traded_at=now,
    )
    await insert_trade_record(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_final",
        outcome="NO",
        size_usdc=6_000,
        traded_at=now + timedelta(minutes=10),
    )

    pubsub = mock_redis.pubsub()
    await pubsub.subscribe(RedisKeys.CHANNEL_WALLET_PENALTIES)
    await pubsub.get_message(timeout=1)  # subscription confirm

    signal = make_signal_event(
        triggering_wallet="0xWHALE001",
        market_id="market_final",
    )
    await trap_detector.check(signal, mock_redis, test_config, db_session)

    # Should get 2 messages: penalty + manipulator flag
    messages = []
    for _ in range(5):
        msg = await pubsub.get_message(timeout=1)
        if msg and msg["type"] == "message":
            messages.append(json.loads(msg["data"]))
    await pubsub.unsubscribe()

    assert len(messages) == 2
    flags = [m.get("flag") for m in messages if "flag" in m]
    assert "MANIPULATOR" in flags


# ── Error handling ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_db_error_fails_open(mock_redis, test_config):
    """DB connection error → fail open (False, '')."""
    from unittest.mock import AsyncMock, MagicMock

    # Create a session that raises on execute
    broken_session = MagicMock(spec=["execute", "add", "flush"])
    broken_session.execute = AsyncMock(side_effect=Exception("DB down"))

    signal = make_signal_event()
    is_trap, reason = await trap_detector.check(
        signal, mock_redis, test_config, broken_session
    )
    assert is_trap is False
    assert reason == ""
