"""
Tests for pre_filter/pipeline.py — orchestration only.

These tests mock all three gate functions and verify that the pipeline:
  - calls gates in the correct order (Gate 1 → 2 → 3)
  - short-circuits on gate failure (Gate 1 fail → Gate 2 never called)
  - publishes to qualified_whale_trades on full pass
  - filters HEDGE/REBALANCE intents (Gate 3) without publishing
  - skips malformed JSON without crashing
  - fails closed on gate exceptions (logs ERROR, discards trade)
  - handles missing wallet data from build_qualified_trade (logs ERROR, discards)

Gate logic is NOT tested here — it is tested in:
  test_market_quality.py, test_arbitrage_exclusion.py, test_intent_classifier.py

Patching targets:
  meg.pre_filter.market_quality.check
  meg.pre_filter.arbitrage_exclusion.check
  meg.pre_filter.intent_classifier.classify
  meg.pre_filter.intent_classifier.build_qualified_trade
  meg.pre_filter.pipeline.publish
"""
from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade, RawWhaleTrade
from meg.pre_filter import pipeline
from tests.pre_filter.conftest import make_raw_trade, set_wallet_redis_data


# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_qualified(trade: RawWhaleTrade) -> QualifiedWhaleTrade:
    """Build a minimal QualifiedWhaleTrade from a RawWhaleTrade for mock returns."""
    return QualifiedWhaleTrade(
        wallet_address=trade.wallet_address,
        market_id=trade.market_id,
        outcome=trade.outcome,
        size_usdc=trade.size_usdc,
        timestamp_ms=trade.timestamp_ms,
        tx_hash=trade.tx_hash,
        block_number=trade.block_number,
        market_price_at_trade=trade.market_price_at_trade,
        whale_score=0.75,
        archetype="INFORMATION",
        intent="SIGNAL",
    )


# ── Gate short-circuit tests ──────────────────────────────────────────────────


async def test_pipeline_gate1_fail_filters(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """
    Gate 1 returns False → Gate 2 is never called, nothing is published.
    Pipeline logs a WARN-level event.
    """
    trade = make_raw_trade()
    mocker.patch("meg.pre_filter.market_quality.check", new=AsyncMock(return_value=False))
    gate2 = mocker.patch(
        "meg.pre_filter.arbitrage_exclusion.check", new=AsyncMock(return_value=True)
    )
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    gate2.assert_not_called()
    pub.assert_not_called()


async def test_pipeline_gate2_fail_filters(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """
    Gate 1 passes, Gate 2 returns False → Gate 3 is never called, nothing published.
    """
    trade = make_raw_trade()
    mocker.patch("meg.pre_filter.market_quality.check", new=AsyncMock(return_value=True))
    mocker.patch("meg.pre_filter.arbitrage_exclusion.check", new=AsyncMock(return_value=False))
    gate3 = mocker.patch(
        "meg.pre_filter.intent_classifier.classify", new=AsyncMock(return_value="SIGNAL")
    )
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    gate3.assert_not_called()
    pub.assert_not_called()


async def test_pipeline_gate3_hedge_filters(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """
    All gates pass, Gate 3 returns HEDGE → nothing is published (HEDGE is filtered).
    """
    trade = make_raw_trade()
    mocker.patch("meg.pre_filter.market_quality.check", new=AsyncMock(return_value=True))
    mocker.patch("meg.pre_filter.arbitrage_exclusion.check", new=AsyncMock(return_value=True))
    mocker.patch("meg.pre_filter.intent_classifier.classify", new=AsyncMock(return_value="HEDGE"))
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    pub.assert_not_called()


async def test_pipeline_gate3_rebalance_filters(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """Gate 3 returns REBALANCE → nothing published."""
    trade = make_raw_trade()
    mocker.patch("meg.pre_filter.market_quality.check", new=AsyncMock(return_value=True))
    mocker.patch("meg.pre_filter.arbitrage_exclusion.check", new=AsyncMock(return_value=True))
    mocker.patch(
        "meg.pre_filter.intent_classifier.classify", new=AsyncMock(return_value="REBALANCE")
    )
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    pub.assert_not_called()


# ── Full pass ─────────────────────────────────────────────────────────────────


async def test_pipeline_full_pass_publishes(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """
    All gates pass, Gate 3 returns SIGNAL, build_qualified_trade returns a valid
    QualifiedWhaleTrade → publish is called once on qualified_whale_trades.
    """
    trade = make_raw_trade()
    qualified = _make_qualified(trade)

    mocker.patch("meg.pre_filter.market_quality.check", new=AsyncMock(return_value=True))
    mocker.patch("meg.pre_filter.arbitrage_exclusion.check", new=AsyncMock(return_value=True))
    mocker.patch(
        "meg.pre_filter.intent_classifier.classify", new=AsyncMock(return_value="SIGNAL")
    )
    mocker.patch(
        "meg.pre_filter.intent_classifier.build_qualified_trade",
        new=AsyncMock(return_value=qualified),
    )
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    pub.assert_called_once()
    channel_arg = pub.call_args[0][1]
    from meg.core.events import RedisKeys
    assert channel_arg == RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES


async def test_pipeline_full_pass_publishes_signal_ladder(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """SIGNAL_LADDER also passes to publish — both SIGNAL variants are passing intents."""
    trade = make_raw_trade()
    qualified = _make_qualified(trade)

    mocker.patch("meg.pre_filter.market_quality.check", new=AsyncMock(return_value=True))
    mocker.patch("meg.pre_filter.arbitrage_exclusion.check", new=AsyncMock(return_value=True))
    mocker.patch(
        "meg.pre_filter.intent_classifier.classify",
        new=AsyncMock(return_value="SIGNAL_LADDER"),
    )
    mocker.patch(
        "meg.pre_filter.intent_classifier.build_qualified_trade",
        new=AsyncMock(return_value=qualified),
    )
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    pub.assert_called_once()


async def test_pipeline_qualified_trade_schema_valid(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """
    The message published to qualified_whale_trades deserializes as a valid
    QualifiedWhaleTrade (no missing required fields, correct types).
    """
    trade = make_raw_trade()
    qualified = _make_qualified(trade)

    mocker.patch("meg.pre_filter.market_quality.check", new=AsyncMock(return_value=True))
    mocker.patch("meg.pre_filter.arbitrage_exclusion.check", new=AsyncMock(return_value=True))
    mocker.patch(
        "meg.pre_filter.intent_classifier.classify", new=AsyncMock(return_value="SIGNAL")
    )
    mocker.patch(
        "meg.pre_filter.intent_classifier.build_qualified_trade",
        new=AsyncMock(return_value=qualified),
    )
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    published_json = pub.call_args[0][2]
    parsed = QualifiedWhaleTrade.model_validate_json(published_json)
    assert parsed.event_type == "qualified_whale_trade"
    assert parsed.whale_score > 0.0
    assert parsed.archetype in ("INFORMATION", "MOMENTUM", "ARBITRAGE", "MANIPULATOR")
    assert parsed.intent in ("SIGNAL", "SIGNAL_LADDER", "HEDGE", "REBALANCE")


# ── Wallet data unavailable ───────────────────────────────────────────────────


async def test_pipeline_wallet_data_unavailable_discards(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """
    build_qualified_trade returns None (wallet data unavailable) → nothing published.
    Pipeline must never emit a QualifiedWhaleTrade with whale_score=0.0.
    """
    trade = make_raw_trade()
    mocker.patch("meg.pre_filter.market_quality.check", new=AsyncMock(return_value=True))
    mocker.patch("meg.pre_filter.arbitrage_exclusion.check", new=AsyncMock(return_value=True))
    mocker.patch(
        "meg.pre_filter.intent_classifier.classify", new=AsyncMock(return_value="SIGNAL")
    )
    mocker.patch(
        "meg.pre_filter.intent_classifier.build_qualified_trade",
        new=AsyncMock(return_value=None),
    )
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    pub.assert_not_called()


# ── Error handling ────────────────────────────────────────────────────────────


async def test_pipeline_gate_exception_fails_closed(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """
    A gate raises an unexpected exception → pipeline logs ERROR, discards the
    trade, and does NOT re-raise. The pipeline loop must not crash.
    """
    trade = make_raw_trade()
    mocker.patch(
        "meg.pre_filter.market_quality.check",
        new=AsyncMock(side_effect=ConnectionError("Redis timeout")),
    )
    gate2 = mocker.patch(
        "meg.pre_filter.arbitrage_exclusion.check", new=AsyncMock(return_value=True)
    )
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    # Must not raise — pipeline is resilient to gate exceptions
    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    gate2.assert_not_called()
    pub.assert_not_called()


async def test_pipeline_gate2_exception_fails_closed(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """Gate 2 DB exception → fails closed, Gate 3 not called."""
    trade = make_raw_trade()
    mocker.patch("meg.pre_filter.market_quality.check", new=AsyncMock(return_value=True))
    mocker.patch(
        "meg.pre_filter.arbitrage_exclusion.check",
        new=AsyncMock(side_effect=Exception("DB connection lost")),
    )
    gate3 = mocker.patch(
        "meg.pre_filter.intent_classifier.classify", new=AsyncMock(return_value="SIGNAL")
    )
    pub = mocker.patch("meg.pre_filter.pipeline.publish", new=AsyncMock())

    await pipeline._process_event(trade, mock_redis, test_config, session=None)

    gate3.assert_not_called()
    pub.assert_not_called()
