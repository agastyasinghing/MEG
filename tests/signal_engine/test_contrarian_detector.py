"""
Tests for meg/signal_engine/contrarian_detector.py

⚠️  OPUS SPEC — module stubs raise NotImplementedError.
Implement contrarian_detector.score() and get_order_flow_direction() with Opus + ultrathink.
Contrarian logic is non-trivial: incorrect direction inversion = opposite signal effect.

Key implementation constraints:
  - score() returns a float in [0.0, 1.0] (divergence score)
  - 1.0 = whale strongly against order flow (contrarian — high conviction signal)
  - 0.5 = neutral (no prevailing order flow, or insufficient data)
  - 0.0 = whale following the crowd (momentum — lower information content)
  - get_order_flow_direction() returns float in [-1.0, 1.0]
    +1.0 = strong YES buying pressure, -1.0 = strong NO buying pressure, 0.0 = neutral
  - Order flow direction is inferred from Redis price history (sorted set ZRANGE)
    or bid/ask imbalance (market bid/ask keys written by CLOBMarketFeed)
  - A YES trade against negative order flow (NO pressure) = contrarian (score > 0.5)
  - A YES trade with positive order flow (YES pressure) = following crowd (score < 0.5)
  - Insufficient data (no price history, no bid/ask) → neutral 0.5

Redis keys consumed:
  RedisKeys.market_bid(market_id)           → best bid
  RedisKeys.market_ask(market_id)           → best ask
  RedisKeys.market_price_history(market_id) → sorted set of recent prices

PRD reference: §9.3.8 Contrarian Detector
"""
from __future__ import annotations

import pytest

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys
from meg.signal_engine.contrarian_detector import get_order_flow_direction, score
from tests.signal_engine.conftest import make_qualified_trade

# Most tests call stubs — mark per-test below to preserve the config check test
_OPUS_XFAIL = pytest.mark.xfail(
    reason="OPUS SPEC: contrarian_detector stubs raise NotImplementedError",
    strict=False,
)


# ── Return bounds ─────────────────────────────────────────────────────────────


@_OPUS_XFAIL
async def test_score_in_unit_interval(mock_redis, test_config: MegConfig) -> None:
    """score() must always be in [0.0, 1.0]."""
    trade = make_qualified_trade()
    result = await score(trade, mock_redis, test_config)
    assert 0.0 <= result <= 1.0


@_OPUS_XFAIL
async def test_no_market_data_returns_neutral(mock_redis, test_config: MegConfig) -> None:
    """
    When Redis has no bid/ask/price_history for this market, return 0.5 (neutral).
    Cannot determine order flow direction without market data.
    """
    trade = make_qualified_trade(market_id="market_no_data")
    result = await score(trade, mock_redis, test_config)
    assert result == pytest.approx(0.5, abs=0.1)


# ── Contrarian detection ──────────────────────────────────────────────────────


@_OPUS_XFAIL
async def test_yes_trade_against_no_pressure_is_contrarian(
    mock_redis, test_config: MegConfig
) -> None:
    """
    When the market has downward price pressure (NO buying) and the whale buys YES,
    that's a contrarian signal → divergence score should be > 0.5.
    """
    # Simulate NO pressure: ask > mid, bid falling (price history trending down)
    market_id = "market_001"
    await mock_redis.set(RedisKeys.market_bid(market_id), "0.35")
    await mock_redis.set(RedisKeys.market_ask(market_id), "0.40")

    # Price history: trending down (0.55 → 0.50 → 0.42 → 0.37)
    price_key = RedisKeys.market_price_history(market_id)
    import time
    now = int(time.time() * 1000)
    await mock_redis.zadd(price_key, {
        f"0.55@{now - 3600000}": now - 3600000,
        f"0.50@{now - 2400000}": now - 2400000,
        f"0.42@{now - 1200000}": now - 1200000,
        f"0.37@{now}": now,
    })

    trade = make_qualified_trade(market_id=market_id, outcome="YES")
    result = await score(trade, mock_redis, test_config)
    assert result > 0.5  # contrarian — whale going YES against NO pressure


@_OPUS_XFAIL
async def test_yes_trade_with_yes_pressure_is_momentum(
    mock_redis, test_config: MegConfig
) -> None:
    """
    When market has YES buying pressure and whale also buys YES,
    that's following momentum → divergence score should be < 0.5.
    """
    market_id = "market_001"
    await mock_redis.set(RedisKeys.market_bid(market_id), "0.70")
    await mock_redis.set(RedisKeys.market_ask(market_id), "0.75")

    # Price history: trending up (0.50 → 0.58 → 0.65 → 0.72)
    price_key = RedisKeys.market_price_history(market_id)
    import time
    now = int(time.time() * 1000)
    await mock_redis.zadd(price_key, {
        f"0.50@{now - 3600000}": now - 3600000,
        f"0.58@{now - 2400000}": now - 2400000,
        f"0.65@{now - 1200000}": now - 1200000,
        f"0.72@{now}": now,
    })

    trade = make_qualified_trade(market_id=market_id, outcome="YES")
    result = await score(trade, mock_redis, test_config)
    assert result < 0.5  # momentum — following the crowd


# ── get_order_flow_direction() ────────────────────────────────────────────────


@_OPUS_XFAIL
async def test_order_flow_direction_in_valid_range(mock_redis) -> None:
    """get_order_flow_direction() must always return a value in [-1.0, 1.0]."""
    result = await get_order_flow_direction("market_001", mock_redis)
    assert -1.0 <= result <= 1.0


@_OPUS_XFAIL
async def test_order_flow_direction_neutral_on_no_data(mock_redis) -> None:
    """No market data → order flow direction = 0.0 (neutral)."""
    result = await get_order_flow_direction("market_no_data", mock_redis)
    assert result == pytest.approx(0.0, abs=0.1)


# ── Contrarian threshold for is_contrarian flag ───────────────────────────────


@_OPUS_XFAIL
async def test_score_above_contrarian_threshold_means_is_contrarian(
    mock_redis, test_config: MegConfig
) -> None:
    """
    When score > config.signal.contrarian_threshold (default 0.55),
    composite_scorer will mark is_contrarian=True on the SignalEvent.
    This test verifies the threshold value is accessible from config.
    """
    # This test does not directly test composite_scorer — it verifies the config
    # value is correct so composite_scorer can use it
    assert test_config.signal.contrarian_threshold == pytest.approx(0.55)
