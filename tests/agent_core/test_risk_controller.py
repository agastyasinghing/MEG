"""
Tests for meg.agent_core.risk_controller — 5-gate risk framework.

Gate order (cheapest first):
  Gate 1: Paper trading mode   — config read only
  Gate 2: Daily loss limit     — 1 Redis GET
  Gate 3: Max open positions   — 1 Redis HLEN
  Gate 4: Market exposure      — 2 Redis GETs
  Gate 5: Position size        — 1 Redis GET

Each gate tested independently: pass, fail, and missing-data defaults.
"""
from __future__ import annotations

import pytest

from meg.agent_core import risk_controller
from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys

from .conftest import make_position_state, make_signal_event, add_position_to_redis


# ── Gate 1: Paper trading ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_gate1_paper_trading_passes(test_config):
    """Paper trading mode always passes Gate 1."""
    assert test_config.risk.paper_trading is True
    passed, reason = risk_controller._check_paper_trading(test_config)
    assert passed is True
    assert reason == ""


@pytest.mark.asyncio
async def test_gate1_live_mode_passes(test_config):
    """Live mode also passes in v1 — gate is structural, wired for v2."""
    test_config.risk.paper_trading = False
    passed, reason = risk_controller._check_paper_trading(test_config)
    assert passed is True


# ── Gate 2: Daily loss circuit breaker ────────────────────────────────────


@pytest.mark.asyncio
async def test_gate2_no_pnl_key_passes(mock_redis, test_config):
    """Missing daily_pnl_usdc key → default 0.0 → PASS."""
    passed, reason = await risk_controller._check_daily_loss(mock_redis, test_config)
    assert passed is True


@pytest.mark.asyncio
async def test_gate2_within_limit_passes(mock_redis, test_config):
    """Daily loss within limit → PASS."""
    await mock_redis.set(RedisKeys.daily_pnl_usdc(), "-200")
    passed, reason = await risk_controller._check_daily_loss(mock_redis, test_config)
    assert passed is True


@pytest.mark.asyncio
async def test_gate2_at_limit_fails(mock_redis, test_config):
    """Daily loss exactly at limit → FAIL."""
    limit = test_config.risk.max_daily_loss_usdc
    await mock_redis.set(RedisKeys.daily_pnl_usdc(), str(-limit))
    passed, reason = await risk_controller._check_daily_loss(mock_redis, test_config)
    assert passed is False
    assert "circuit_breaker" in reason


@pytest.mark.asyncio
async def test_gate2_over_limit_fails(mock_redis, test_config):
    """Daily loss exceeding limit → FAIL."""
    await mock_redis.set(RedisKeys.daily_pnl_usdc(), "-999")
    passed, reason = await risk_controller._check_daily_loss(mock_redis, test_config)
    assert passed is False
    assert "circuit_breaker" in reason


@pytest.mark.asyncio
async def test_gate2_positive_pnl_passes(mock_redis, test_config):
    """Positive daily PnL (gains) never triggers circuit breaker."""
    await mock_redis.set(RedisKeys.daily_pnl_usdc(), "9999")
    passed, reason = await risk_controller._check_daily_loss(mock_redis, test_config)
    assert passed is True


# ── Gate 3: Max open positions ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_gate3_no_positions_passes(mock_redis, test_config):
    """No open positions → PASS."""
    passed, reason = await risk_controller._check_max_positions(mock_redis, test_config)
    assert passed is True


@pytest.mark.asyncio
async def test_gate3_under_limit_passes(mock_redis, test_config):
    """Fewer than max positions → PASS."""
    pos = make_position_state(position_id="pos_1")
    await add_position_to_redis(mock_redis, pos)
    passed, reason = await risk_controller._check_max_positions(mock_redis, test_config)
    assert passed is True


@pytest.mark.asyncio
async def test_gate3_at_limit_fails(mock_redis, test_config):
    """Exactly at max positions → FAIL."""
    for i in range(test_config.risk.max_open_positions):
        pos = make_position_state(position_id=f"pos_{i}", market_id=f"market_{i}")
        await add_position_to_redis(mock_redis, pos)
    passed, reason = await risk_controller._check_max_positions(mock_redis, test_config)
    assert passed is False
    assert "max_positions" in reason


# ── Gate 4: Market exposure limit ─────────────────────────────────────────


@pytest.mark.asyncio
async def test_gate4_no_exposure_passes(mock_redis, test_config):
    """No existing market exposure → PASS."""
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "1000")
    passed, reason = await risk_controller._check_market_exposure(
        "market_001", mock_redis, test_config
    )
    assert passed is True


@pytest.mark.asyncio
async def test_gate4_under_limit_passes(mock_redis, test_config):
    """Market exposure under limit → PASS."""
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "1000")
    await mock_redis.set(RedisKeys.market_exposure_usdc("market_001"), "100")
    passed, reason = await risk_controller._check_market_exposure(
        "market_001", mock_redis, test_config
    )
    assert passed is True  # 100/1000 = 10% < 20% limit


@pytest.mark.asyncio
async def test_gate4_at_limit_fails(mock_redis, test_config):
    """Market exposure at limit → FAIL."""
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "1000")
    await mock_redis.set(RedisKeys.market_exposure_usdc("market_001"), "200")
    passed, reason = await risk_controller._check_market_exposure(
        "market_001", mock_redis, test_config
    )
    assert passed is False  # 200/1000 = 20% >= 20% limit
    assert "max_market_exposure" in reason


@pytest.mark.asyncio
async def test_gate4_no_portfolio_falls_back_to_config(mock_redis, test_config):
    """Missing portfolio_value → falls back to config kelly.portfolio_value_usdc."""
    # config default is 1000.0
    await mock_redis.set(RedisKeys.market_exposure_usdc("market_001"), "50")
    passed, reason = await risk_controller._check_market_exposure(
        "market_001", mock_redis, test_config
    )
    assert passed is True  # 50/1000 = 5% < 20% limit


# ── Gate 5: Position size limit ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_gate5_under_limit_passes(mock_redis, test_config):
    """Proposed size under limit → PASS."""
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "1000")
    # max_position_pct = 0.05 → max_size = 50
    passed, reason = await risk_controller._check_position_size(
        40.0, mock_redis, test_config
    )
    assert passed is True


@pytest.mark.asyncio
async def test_gate5_over_limit_fails(mock_redis, test_config):
    """Proposed size over limit → FAIL."""
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "1000")
    # max_position_pct = 0.05 → max_size = 50
    passed, reason = await risk_controller._check_position_size(
        60.0, mock_redis, test_config
    )
    assert passed is False
    assert "position_too_large" in reason


@pytest.mark.asyncio
async def test_gate5_no_portfolio_falls_back_to_config(mock_redis, test_config):
    """Missing portfolio_value → falls back to config default."""
    # config default kelly.portfolio_value_usdc = 1000.0, max_position_pct = 0.05 → 50
    passed, reason = await risk_controller._check_position_size(
        40.0, mock_redis, test_config
    )
    assert passed is True


# ── Full check() integration ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_check_all_pass(mock_redis, test_config):
    """All gates pass → (True, "")."""
    await mock_redis.set(RedisKeys.portfolio_value_usdc(), "1000")
    signal = make_signal_event(recommended_size_usdc=40.0)
    passed, reason = await risk_controller.check(signal, mock_redis, test_config)
    assert passed is True
    assert reason == ""


@pytest.mark.asyncio
async def test_check_short_circuits_on_first_failure(mock_redis, test_config):
    """First failing gate short-circuits — no further gates run."""
    await mock_redis.set(RedisKeys.daily_pnl_usdc(), "-999")
    signal = make_signal_event()
    passed, reason = await risk_controller.check(signal, mock_redis, test_config)
    assert passed is False
    assert "circuit_breaker" in reason
