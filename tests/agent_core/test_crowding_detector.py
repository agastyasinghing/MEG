"""
Tests for meg.agent_core.crowding_detector — price-based entry distance gate.

v1: blocks signal if price has moved > crowding_max_entry_distance_pct
in the signal's direction from the whale's fill price.
"""
from __future__ import annotations

import pytest

from meg.agent_core import crowding_detector
from meg.core.events import RedisKeys

from .conftest import make_signal_event, set_market_redis_data


# ── No data — fail open ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_no_price_data_passes(mock_redis, test_config):
    """Missing mid_price → (False, '') — fail open."""
    signal = make_signal_event()
    blocked, reason = await crowding_detector.check(signal, mock_redis, test_config)
    assert blocked is False
    assert reason == ""


@pytest.mark.asyncio
async def test_zero_signal_price_passes(mock_redis, test_config):
    """Signal with market_price_at_signal=0 → (False, '')."""
    await set_market_redis_data(mock_redis, mid_price=0.55)
    signal = make_signal_event(market_price_at_signal=0.0)
    blocked, reason = await crowding_detector.check(signal, mock_redis, test_config)
    assert blocked is False


# ── Within threshold — edge exists ────────────────────────────────────────


@pytest.mark.asyncio
async def test_no_drift_passes(mock_redis, test_config):
    """Price unchanged → no crowding."""
    signal = make_signal_event(market_price_at_signal=0.55)
    await set_market_redis_data(mock_redis, mid_price=0.55)
    blocked, reason = await crowding_detector.check(signal, mock_redis, test_config)
    assert blocked is False


@pytest.mark.asyncio
async def test_small_drift_yes_passes(mock_redis, test_config):
    """YES signal, small upward drift within threshold → PASS."""
    # 0.55 → 0.57 = 3.6% drift, threshold = 8%
    signal = make_signal_event(outcome="YES", market_price_at_signal=0.55)
    await set_market_redis_data(mock_redis, mid_price=0.57)
    blocked, reason = await crowding_detector.check(signal, mock_redis, test_config)
    assert blocked is False


@pytest.mark.asyncio
async def test_drift_against_direction_passes(mock_redis, test_config):
    """YES signal, price moved DOWN → no crowding (negative drift)."""
    signal = make_signal_event(outcome="YES", market_price_at_signal=0.55)
    await set_market_redis_data(mock_redis, mid_price=0.45)
    blocked, reason = await crowding_detector.check(signal, mock_redis, test_config)
    assert blocked is False


# ── Beyond threshold — window closed ──────────────────────────────────────


@pytest.mark.asyncio
async def test_large_drift_yes_blocks(mock_redis, test_config):
    """YES signal, large upward drift > threshold → BLOCKED."""
    # 0.50 → 0.60 = 20% drift, threshold = 8%
    signal = make_signal_event(outcome="YES", market_price_at_signal=0.50)
    await set_market_redis_data(mock_redis, mid_price=0.60)
    blocked, reason = await crowding_detector.check(signal, mock_redis, test_config)
    assert blocked is True
    assert "window_closed" in reason


@pytest.mark.asyncio
async def test_large_drift_no_blocks(mock_redis, test_config):
    """NO signal, large downward drift > threshold → BLOCKED."""
    # NO at 0.55, price dropped to 0.45 → 18% drift in signal direction
    signal = make_signal_event(outcome="NO", market_price_at_signal=0.55)
    await set_market_redis_data(mock_redis, mid_price=0.45)
    blocked, reason = await crowding_detector.check(signal, mock_redis, test_config)
    assert blocked is True
    assert "window_closed" in reason


@pytest.mark.asyncio
async def test_just_under_threshold_passes(mock_redis, test_config):
    """Drift just under threshold → PASS."""
    # threshold = 0.08, use 7% drift to stay clearly under
    signal = make_signal_event(outcome="YES", market_price_at_signal=0.50)
    # 0.50 → 0.535 = 7% drift < 8% threshold
    await set_market_redis_data(mock_redis, mid_price=0.535)
    blocked, reason = await crowding_detector.check(signal, mock_redis, test_config)
    assert blocked is False
