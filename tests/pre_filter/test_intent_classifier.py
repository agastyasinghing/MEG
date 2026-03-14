"""
Test SPEC for pre_filter/intent_classifier.py (Gate 3).

⚠️  THIS IS A SPEC FILE — tests are fully written but will fail with
NotImplementedError until Opus implements classify() and build_qualified_trade().

OPUS SESSION INSTRUCTIONS:
  1. Read this file in full before writing any code.
  2. Implement intent_classifier.classify() and intent_classifier.build_qualified_trade()
     to make all tests pass.
  3. Use ultrathink. Do not cut corners on HEDGE/REBALANCE edge cases.
  4. Do not modify test assertions — the tests define the expected behaviour.

Coverage map:
  SIGNAL: new directional, size >= min_signal_size_pct * capital
    → test_classify_signal_new_position

  SIGNAL: size exactly at threshold (boundary)
    → test_classify_signal_at_size_threshold

  REBALANCE: size below min_signal_size_pct * capital
    → test_classify_too_small_is_rebalance

  SIGNAL_LADDER: same direction + >= ladder_min_trades prior trades in window
    → test_classify_signal_ladder_detected

  SIGNAL_LADDER: prior trades exist but outside ladder_window → plain SIGNAL
    → test_classify_ladder_trades_outside_window_is_signal

  SIGNAL_LADDER: prior trades exist but wrong direction → plain SIGNAL
    → test_classify_ladder_wrong_direction_is_signal

  HEDGE: opposing direction to existing same-market position
    → test_classify_hedge_opposing_direction

  REBALANCE: reducing existing same-direction position (partial exit)
    → test_classify_rebalance_partial_exit

  Wallet data unavailable → conservatively returns SIGNAL
    → test_classify_wallet_data_unavailable_returns_signal

  session=None → Trade queries skipped → returns SIGNAL (conservative default)
    → test_classify_no_session_returns_signal

  build_qualified_trade: enriches with whale_score + archetype from Redis
    → test_build_qualified_trade_enriches_correctly

  build_qualified_trade: wallet score absent → returns None
    → test_build_qualified_trade_wallet_score_missing_returns_none

  build_qualified_trade: wallet archetype absent → returns None
    → test_build_qualified_trade_wallet_archetype_missing_returns_none

  build_qualified_trade: intent is preserved in output
    → test_build_qualified_trade_preserves_intent
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade, RedisKeys
from meg.pre_filter import intent_classifier
from tests.pre_filter.conftest import (
    insert_trade_record,
    make_raw_trade,
    set_wallet_redis_data,
)


# ── SIGNAL ────────────────────────────────────────────────────────────────────


async def test_classify_signal_new_position(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    New directional trade, size >= min_signal_size_pct * wallet capital,
    no opposing position → classified as SIGNAL.

    Setup: wallet capital = 50_000 USDC, min_signal_size_pct = 0.02 (default)
    → threshold = 1_000 USDC. Trade size = 2_000 USDC → well above threshold.
    No prior trades in the DB for this wallet+market.
    """
    wallet = "0xSIG001"
    trade = make_raw_trade(wallet_address=wallet, market_id="market_001", outcome="YES", size_usdc=2_000.0)
    await set_wallet_redis_data(mock_redis, wallet_address=wallet, total_capital_usdc=50_000.0)

    result = await intent_classifier.classify(trade, mock_redis, test_config, db_session)

    assert result == "SIGNAL"


async def test_classify_signal_at_size_threshold(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    Trade size exactly at min_signal_size_pct * capital boundary → SIGNAL.
    (boundary: threshold = 0.02 * 50_000 = 1_000 USDC, trade size = 1_000)
    """
    wallet = "0xSIG002"
    threshold_usdc = test_config.pre_filter.min_signal_size_pct * 50_000.0
    trade = make_raw_trade(
        wallet_address=wallet,
        market_id="market_001",
        outcome="YES",
        size_usdc=threshold_usdc,
    )
    await set_wallet_redis_data(mock_redis, wallet_address=wallet, total_capital_usdc=50_000.0)

    result = await intent_classifier.classify(trade, mock_redis, test_config, db_session)

    assert result == "SIGNAL"


# ── REBALANCE ─────────────────────────────────────────────────────────────────


async def test_classify_too_small_is_rebalance(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    Trade size well below min_signal_size_pct * capital → REBALANCE.
    (e.g. 100 USDC vs threshold of 1_000 USDC on a 50k capital wallet)
    """
    wallet = "0xREBAL001"
    trade = make_raw_trade(
        wallet_address=wallet,
        market_id="market_001",
        outcome="YES",
        size_usdc=100.0,  # well below threshold
    )
    await set_wallet_redis_data(mock_redis, wallet_address=wallet, total_capital_usdc=50_000.0)

    result = await intent_classifier.classify(trade, mock_redis, test_config, db_session)

    assert result == "REBALANCE"


async def test_classify_rebalance_partial_exit(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    Whale has an existing YES position in the market and buys more YES but at
    a small size (reducing overall expected value, partial position management).
    Small size relative to capital → REBALANCE.
    """
    wallet = "0xREBAL002"
    now = datetime.now(tz=timezone.utc)
    # Prior large YES trade indicating an existing position
    await insert_trade_record(
        db_session,
        wallet_address=wallet,
        market_id="market_001",
        outcome="YES",
        size_usdc=5_000.0,
        tx_hash="0xtx_prior_yes",
        traded_at=now - timedelta(hours=3),
    )
    # Current small YES trade (below threshold) → REBALANCE
    trade = make_raw_trade(
        wallet_address=wallet,
        market_id="market_001",
        outcome="YES",
        size_usdc=50.0,
    )
    await set_wallet_redis_data(mock_redis, wallet_address=wallet, total_capital_usdc=50_000.0)

    result = await intent_classifier.classify(trade, mock_redis, test_config, db_session)

    assert result == "REBALANCE"


# ── SIGNAL_LADDER ─────────────────────────────────────────────────────────────


async def test_classify_signal_ladder_detected(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    Whale has >= ladder_min_trades prior same-direction trades in the market
    within ladder_window_hours → SIGNAL_LADDER (escalating conviction).
    Default: ladder_min_trades=2, ladder_window_hours=6.
    """
    wallet = "0xLADDER001"
    now = datetime.now(tz=timezone.utc)
    ladder_min = test_config.pre_filter.ladder_min_trades
    window_hours = test_config.pre_filter.ladder_window_hours

    # Insert enough prior same-direction trades within the window
    for i in range(ladder_min):
        await insert_trade_record(
            db_session,
            wallet_address=wallet,
            market_id="market_001",
            outcome="YES",
            size_usdc=1_500.0,
            tx_hash=f"0xtx_ladder_{i}",
            traded_at=now - timedelta(hours=window_hours - 1 - i * 0.5),
        )

    trade = make_raw_trade(
        wallet_address=wallet,
        market_id="market_001",
        outcome="YES",
        size_usdc=2_000.0,
    )
    await set_wallet_redis_data(mock_redis, wallet_address=wallet, total_capital_usdc=50_000.0)

    result = await intent_classifier.classify(trade, mock_redis, test_config, db_session)

    assert result == "SIGNAL_LADDER"


async def test_classify_ladder_trades_outside_window_is_signal(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    Same-direction trades exist but are older than ladder_window_hours → plain SIGNAL,
    not SIGNAL_LADDER. The window resets — escalation must be recent.
    """
    wallet = "0xLADDER002"
    now = datetime.now(tz=timezone.utc)
    window_hours = test_config.pre_filter.ladder_window_hours

    # Prior trades exist but are outside the ladder window
    for i in range(3):
        await insert_trade_record(
            db_session,
            wallet_address=wallet,
            market_id="market_001",
            outcome="YES",
            size_usdc=1_500.0,
            tx_hash=f"0xtx_old_ladder_{i}",
            traded_at=now - timedelta(hours=window_hours + 2 + i),
        )

    trade = make_raw_trade(
        wallet_address=wallet,
        market_id="market_001",
        outcome="YES",
        size_usdc=2_000.0,
    )
    await set_wallet_redis_data(mock_redis, wallet_address=wallet, total_capital_usdc=50_000.0)

    result = await intent_classifier.classify(trade, mock_redis, test_config, db_session)

    assert result == "SIGNAL"


async def test_classify_ladder_wrong_direction_is_signal(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    Prior trades exist but in the OPPOSITE direction → not a ladder.
    A YES after multiple NOs is a potential reversal (SIGNAL), not SIGNAL_LADDER.
    """
    wallet = "0xLADDER003"
    now = datetime.now(tz=timezone.utc)
    window_hours = test_config.pre_filter.ladder_window_hours

    # Prior NO trades within the window
    for i in range(3):
        await insert_trade_record(
            db_session,
            wallet_address=wallet,
            market_id="market_001",
            outcome="NO",
            size_usdc=1_500.0,
            tx_hash=f"0xtx_no_prior_{i}",
            traded_at=now - timedelta(hours=i + 1),
        )

    # Current trade is YES — opposite direction, not a ladder
    trade = make_raw_trade(
        wallet_address=wallet,
        market_id="market_001",
        outcome="YES",
        size_usdc=2_000.0,
    )
    await set_wallet_redis_data(mock_redis, wallet_address=wallet, total_capital_usdc=50_000.0)

    result = await intent_classifier.classify(trade, mock_redis, test_config, db_session)

    assert result == "SIGNAL"


# ── HEDGE ─────────────────────────────────────────────────────────────────────


async def test_classify_hedge_opposing_direction(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    Whale has a significant existing YES position in the market and now places
    a significant NO trade → HEDGE (offsetting prior exposure).
    Both YES prior and current NO must be above min_signal_size_pct threshold.
    """
    wallet = "0xHEDGE001"
    now = datetime.now(tz=timezone.utc)
    # Prior significant YES position
    await insert_trade_record(
        db_session,
        wallet_address=wallet,
        market_id="market_001",
        outcome="YES",
        size_usdc=3_000.0,
        tx_hash="0xtx_hedge_prior_yes",
        traded_at=now - timedelta(hours=4),
    )
    # Current significant NO trade (opposing direction)
    trade = make_raw_trade(
        wallet_address=wallet,
        market_id="market_001",
        outcome="NO",
        size_usdc=2_000.0,
    )
    await set_wallet_redis_data(mock_redis, wallet_address=wallet, total_capital_usdc=50_000.0)

    result = await intent_classifier.classify(trade, mock_redis, test_config, db_session)

    assert result == "HEDGE"


# ── Edge cases ────────────────────────────────────────────────────────────────


async def test_classify_wallet_data_unavailable_returns_signal(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    When wallet data is not in Redis (cache miss), classify() returns SIGNAL
    as the conservative default — never filter a potentially valid signal due
    to a cache miss.
    """
    trade = make_raw_trade(wallet_address="0xNODATA001", market_id="market_001")
    # No wallet data written to Redis

    result = await intent_classifier.classify(trade, mock_redis, test_config, db_session)

    assert result == "SIGNAL"


async def test_classify_no_session_returns_signal(
    mock_redis: Redis, test_config: MegConfig
) -> None:
    """
    session=None: Trade table queries are skipped. Without behavioral context
    (hedge/ladder detection), classify() returns SIGNAL conservatively.
    """
    wallet = "0xNOSESS001"
    trade = make_raw_trade(wallet_address=wallet, market_id="market_001", size_usdc=2_000.0)
    await set_wallet_redis_data(mock_redis, wallet_address=wallet, total_capital_usdc=50_000.0)

    result = await intent_classifier.classify(trade, mock_redis, test_config, session=None)

    assert result == "SIGNAL"


# ── build_qualified_trade ─────────────────────────────────────────────────────


async def test_build_qualified_trade_enriches_correctly(
    mock_redis: Redis,
) -> None:
    """
    build_qualified_trade() reads whale_score and archetype from Redis and
    populates all required QualifiedWhaleTrade fields correctly.
    """
    wallet = "0xBUILD001"
    trade = make_raw_trade(wallet_address=wallet, market_id="market_001", outcome="YES")
    await set_wallet_redis_data(
        mock_redis, wallet_address=wallet, score=0.82, archetype="INFORMATION"
    )

    result = await intent_classifier.build_qualified_trade(trade, "SIGNAL", mock_redis)

    assert result is not None
    assert isinstance(result, QualifiedWhaleTrade)
    assert result.wallet_address == wallet
    assert result.market_id == "market_001"
    assert result.outcome == "YES"
    assert result.whale_score == pytest.approx(0.82, abs=1e-6)
    assert result.archetype == "INFORMATION"
    assert result.intent == "SIGNAL"


async def test_build_qualified_trade_wallet_score_missing_returns_none(
    mock_redis: Redis,
) -> None:
    """
    When wallet:{addr}:score is absent (cache miss with no DB fallback),
    build_qualified_trade() returns None. Never emit with whale_score=0.0.
    """
    wallet = "0xNOSCORE001"
    trade = make_raw_trade(wallet_address=wallet, market_id="market_001")
    # Only set archetype, not score
    await mock_redis.set(RedisKeys.wallet_archetype(wallet), "MOMENTUM")

    result = await intent_classifier.build_qualified_trade(trade, "SIGNAL", mock_redis)

    assert result is None


async def test_build_qualified_trade_wallet_archetype_missing_returns_none(
    mock_redis: Redis,
) -> None:
    """
    When wallet:{addr}:archetype is absent, build_qualified_trade() returns None.
    archetype is required for the QualifiedWhaleTrade schema.
    """
    wallet = "0xNOARCH001"
    trade = make_raw_trade(wallet_address=wallet, market_id="market_001")
    # Only set score, not archetype
    await mock_redis.set(RedisKeys.wallet_score(wallet), "0.75")

    result = await intent_classifier.build_qualified_trade(trade, "SIGNAL", mock_redis)

    assert result is None


async def test_build_qualified_trade_preserves_intent(
    mock_redis: Redis,
) -> None:
    """
    The intent passed to build_qualified_trade() is preserved in the output
    QualifiedWhaleTrade. SIGNAL_LADDER must be distinguishable from SIGNAL.
    """
    wallet = "0xBUILD002"
    trade = make_raw_trade(wallet_address=wallet, market_id="market_001")
    await set_wallet_redis_data(mock_redis, wallet_address=wallet)

    result = await intent_classifier.build_qualified_trade(trade, "SIGNAL_LADDER", mock_redis)

    assert result is not None
    assert result.intent == "SIGNAL_LADDER"
