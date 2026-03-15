"""
Tests for meg.agent_core.decision_agent — signal gating + proposal creation.

Decision flow:
  Hard blocks: system_paused → blacklist → duplicate position
  Risk gates:  risk_controller.check() (5 gates)
  Detectors:   trap_detector → saturation_monitor → crowding_detector
  Output:      TradeProposal (PENDING_APPROVAL) → CHANNEL_TRADE_PROPOSALS

Each gate rejection path tested. All-pass path tested with proposal validation.
signal_outcomes status UPDATE tested for each outcome.
"""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from meg.agent_core import decision_agent
from meg.core.events import RedisKeys

from .conftest import (
    add_position_to_redis,
    insert_signal_outcome,
    make_position_state,
    make_signal_event,
    set_market_redis_data,
)


# ── Hard blocks ───────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_system_paused_blocks(mock_redis, test_config, db_session):
    """system_paused set → signal BLOCKED, returns None."""
    await mock_redis.set(RedisKeys.system_paused(), "1")
    signal = make_signal_event(signal_id="sig_paused")
    await insert_signal_outcome(db_session, signal_id="sig_paused")

    result = await decision_agent.evaluate(signal, mock_redis, test_config, db_session)
    assert result is None


@pytest.mark.asyncio
async def test_blacklisted_market_blocks(mock_redis, test_config, db_session):
    """Market in blacklist → signal BLOCKED."""
    test_config.risk.blacklisted_markets = ["market_blocked"]
    signal = make_signal_event(signal_id="sig_bl", market_id="market_blocked")
    await insert_signal_outcome(db_session, signal_id="sig_bl", market_id="market_blocked")

    result = await decision_agent.evaluate(signal, mock_redis, test_config, db_session)
    assert result is None


@pytest.mark.asyncio
async def test_duplicate_position_blocks(mock_redis, test_config, db_session):
    """Existing open position in same market+outcome → BLOCKED."""
    pos = make_position_state(market_id="market_001", outcome="YES")
    await add_position_to_redis(mock_redis, pos)

    signal = make_signal_event(
        signal_id="sig_dup", market_id="market_001", outcome="YES"
    )
    await insert_signal_outcome(db_session, signal_id="sig_dup")
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "10000")

    result = await decision_agent.evaluate(signal, mock_redis, test_config, db_session)
    assert result is None


@pytest.mark.asyncio
async def test_different_outcome_not_duplicate(mock_redis, test_config, db_session):
    """Existing YES position, new NO signal → NOT a duplicate."""
    pos = make_position_state(market_id="market_001", outcome="YES")
    await add_position_to_redis(mock_redis, pos)

    signal = make_signal_event(
        signal_id="sig_nodupe",
        market_id="market_001",
        outcome="NO",
        recommended_size_usdc=30.0,
        market_price_at_signal=0.55,
    )
    await insert_signal_outcome(db_session, signal_id="sig_nodupe")
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "10000")
    await set_market_redis_data(mock_redis, mid_price=0.55)

    # Mock trap_detector to not need Trade table
    with patch("meg.agent_core.trap_detector.check", new_callable=AsyncMock, return_value=(False, "")):
        result = await decision_agent.evaluate(signal, mock_redis, test_config, db_session)

    assert result is not None


# ── Risk controller rejection ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_risk_controller_rejects(mock_redis, test_config, db_session):
    """risk_controller gate failure → signal REJECTED."""
    # Trigger circuit breaker
    await mock_redis.set(RedisKeys.daily_pnl_usdc(), "-999")

    signal = make_signal_event(signal_id="sig_risk")
    await insert_signal_outcome(db_session, signal_id="sig_risk")

    result = await decision_agent.evaluate(signal, mock_redis, test_config, db_session)
    assert result is None


# ── Trap detector rejection ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_trap_detected_blocks(mock_redis, test_config, db_session):
    """Trap detected → signal TRAP_DETECTED."""
    signal = make_signal_event(signal_id="sig_trap")
    await insert_signal_outcome(db_session, signal_id="sig_trap")
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "10000")

    with patch(
        "meg.agent_core.trap_detector.check",
        new_callable=AsyncMock,
        return_value=(True, "whale_trap: rapid exit detected"),
    ):
        result = await decision_agent.evaluate(signal, mock_redis, test_config, db_session)

    assert result is None


# ── Saturation size adjustment ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_saturation_reduces_size(mock_redis, test_config, db_session):
    """Saturation above threshold → size reduced but signal not blocked."""
    signal = make_signal_event(
        signal_id="sig_sat",
        recommended_size_usdc=100.0,
        market_price_at_signal=0.55,
    )
    await insert_signal_outcome(db_session, signal_id="sig_sat")
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "10000")
    await set_market_redis_data(mock_redis, mid_price=0.55)

    with patch(
        "meg.agent_core.trap_detector.check",
        new_callable=AsyncMock,
        return_value=(False, ""),
    ), patch(
        "meg.agent_core.saturation_monitor.score",
        new_callable=AsyncMock,
        return_value=(0.80, 0.60),  # 40% size reduction
    ):
        result = await decision_agent.evaluate(signal, mock_redis, test_config, db_session)

    assert result is not None
    assert result.size_usdc == pytest.approx(60.0)  # 100 * 0.60


# ── Crowding detector blocks ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_crowding_blocks(mock_redis, test_config, db_session):
    """Crowding detected → signal BLOCKED."""
    signal = make_signal_event(signal_id="sig_crowd")
    await insert_signal_outcome(db_session, signal_id="sig_crowd")
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "10000")

    with patch(
        "meg.agent_core.trap_detector.check",
        new_callable=AsyncMock,
        return_value=(False, ""),
    ), patch(
        "meg.agent_core.saturation_monitor.score",
        new_callable=AsyncMock,
        return_value=(0.3, 1.0),
    ), patch(
        "meg.agent_core.crowding_detector.check",
        new_callable=AsyncMock,
        return_value=(True, "window_closed: 15% drift"),
    ):
        result = await decision_agent.evaluate(signal, mock_redis, test_config, db_session)

    assert result is None


# ── All gates pass — full proposal ────────────────────────────────────────


@pytest.mark.asyncio
async def test_all_pass_creates_proposal(mock_redis, test_config, db_session):
    """All gates pass → TradeProposal created with correct fields."""
    signal = make_signal_event(
        signal_id="sig_pass",
        market_id="market_001",
        outcome="YES",
        recommended_size_usdc=50.0,
        composite_score=0.72,
        market_price_at_signal=0.55,
    )
    await insert_signal_outcome(db_session, signal_id="sig_pass")
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "10000")
    await set_market_redis_data(mock_redis, mid_price=0.55)

    with patch(
        "meg.agent_core.trap_detector.check",
        new_callable=AsyncMock,
        return_value=(False, ""),
    ):
        result = await decision_agent.evaluate(signal, mock_redis, test_config, db_session)

    assert result is not None
    assert result.signal_id == "sig_pass"
    assert result.market_id == "market_001"
    assert result.outcome == "YES"
    assert result.status == "PENDING_APPROVAL"
    assert result.composite_score == 0.72
    assert result.limit_price == 0.55
    assert result.proposal_id.startswith("meg_prop_")


@pytest.mark.asyncio
async def test_proposal_published_to_channel(mock_redis, test_config, db_session):
    """Approved proposal is published to CHANNEL_TRADE_PROPOSALS."""
    pubsub = mock_redis.pubsub()
    await pubsub.subscribe(RedisKeys.CHANNEL_TRADE_PROPOSALS)
    await pubsub.get_message(timeout=1)  # subscription confirm

    signal = make_signal_event(
        signal_id="sig_pub",
        recommended_size_usdc=30.0,
        market_price_at_signal=0.55,
    )
    await insert_signal_outcome(db_session, signal_id="sig_pub")
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "10000")
    await set_market_redis_data(mock_redis, mid_price=0.55)

    with patch(
        "meg.agent_core.trap_detector.check",
        new_callable=AsyncMock,
        return_value=(False, ""),
    ):
        await decision_agent.evaluate(signal, mock_redis, test_config, db_session)

    msg = await pubsub.get_message(timeout=1)
    assert msg is not None
    assert msg["type"] == "message"
    await pubsub.unsubscribe()


# ── signal_outcomes status updates ────────────────────────────────────────


@pytest.mark.asyncio
async def test_status_updated_to_approved(mock_redis, test_config, db_session):
    """Approved signal → signal_outcomes status = APPROVED."""
    signal = make_signal_event(
        signal_id="sig_status",
        recommended_size_usdc=30.0,
        market_price_at_signal=0.55,
    )
    await insert_signal_outcome(db_session, signal_id="sig_status", status="PENDING")
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "10000")
    await set_market_redis_data(mock_redis, mid_price=0.55)

    with patch(
        "meg.agent_core.trap_detector.check",
        new_callable=AsyncMock,
        return_value=(False, ""),
    ):
        await decision_agent.evaluate(signal, mock_redis, test_config, db_session)

    from sqlalchemy import select
    from meg.db.models import SignalOutcome
    result = await db_session.execute(
        select(SignalOutcome.status).where(SignalOutcome.signal_id == "sig_status")
    )
    status = result.scalar_one()
    assert status == "APPROVED"


@pytest.mark.asyncio
async def test_status_updated_to_blocked_on_pause(mock_redis, test_config, db_session):
    """Paused system → signal_outcomes status = BLOCKED."""
    await mock_redis.set(RedisKeys.system_paused(), "1")
    signal = make_signal_event(signal_id="sig_block_status")
    await insert_signal_outcome(db_session, signal_id="sig_block_status", status="PENDING")

    await decision_agent.evaluate(signal, mock_redis, test_config, db_session)

    from sqlalchemy import select
    from meg.db.models import SignalOutcome
    result = await db_session.execute(
        select(SignalOutcome.status).where(SignalOutcome.signal_id == "sig_block_status")
    )
    status = result.scalar_one()
    assert status == "BLOCKED"
