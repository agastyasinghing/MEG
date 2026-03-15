"""
Tests for meg/signal_engine/ladder_detector.py

ladder_detector.multiplier() is fully implemented (Sonnet-eligible).
All tests should pass without modification.

Decision log:
  - multiplier() uses the Trade table (authoritative) not Redis
  - Returns [1.0, 2.0] — 1.0 = isolated trade, 2.0 = max ladder boost
  - Each qualifying prior trade = one rung; rung adds ladder_conviction_per_rung (0.15)
  - "Prior" = traded_at < current trade's timestamp (strictly before)
  - "Within window" = traded_at >= cutoff (now - ladder_window_hours)
  - Only is_qualified=True trades count as rungs

Coverage:
  - No prior trades → 1.0
  - 1 prior trade → 1 rung → 1.15
  - 2 prior trades → 2 rungs → 1.30
  - Enough trades to exceed cap → hard-capped at 2.0
  - Different outcome direction not counted
  - Different market not counted
  - Different wallet not counted
  - Trade after current timestamp not counted (only prior trades are rungs)
  - Trade outside window not counted
  - Unqualified trade (is_qualified=False) not counted
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from meg.core.config_loader import MegConfig
from meg.signal_engine.ladder_detector import multiplier
from tests.signal_engine.conftest import insert_trade, make_qualified_trade


# ── No prior trades ───────────────────────────────────────────────────────────


async def test_no_prior_trades_returns_1_0(
    db_session, test_config: MegConfig
) -> None:
    """Isolated trade with no ladder history → multiplier = 1.0 (no boost)."""
    trade = make_qualified_trade()
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.0)


# ── Rung counting ─────────────────────────────────────────────────────────────


async def test_one_prior_trade_adds_one_rung(
    db_session, test_config: MegConfig
) -> None:
    """
    One qualified prior same-direction trade = one rung.
    Expected: 1.0 + 1 * 0.15 = 1.15
    """
    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    earlier = datetime.now(tz=timezone.utc) - timedelta(hours=2)

    await insert_trade(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        tx_hash="0xprev_001",
        traded_at=earlier,
        is_qualified=True,
    )

    trade = make_qualified_trade(timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.15)


async def test_two_prior_trades_adds_two_rungs(
    db_session, test_config: MegConfig
) -> None:
    """Two prior qualified trades = 2 rungs → 1.0 + 2 * 0.15 = 1.30."""
    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)

    for i, hours_ago in enumerate([3, 1], start=1):
        await insert_trade(
            db_session,
            wallet_address="0xWHALE001",
            market_id="market_001",
            outcome="YES",
            tx_hash=f"0xprev_{i:03d}",
            traded_at=datetime.now(tz=timezone.utc) - timedelta(hours=hours_ago),
            is_qualified=True,
        )

    trade = make_qualified_trade(timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.30)


async def test_multiplier_capped_at_2_0(
    db_session, test_config: MegConfig
) -> None:
    """
    8 prior trades × 0.15/rung = 2.20 raw → hard-capped at 2.0.
    Default ladder_window_hours=6, so all prior trades are within window.
    """
    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)

    for i in range(8):
        await insert_trade(
            db_session,
            wallet_address="0xWHALE001",
            market_id="market_001",
            outcome="YES",
            tx_hash=f"0xprev_cap_{i:03d}",
            traded_at=datetime.now(tz=timezone.utc) - timedelta(minutes=30 * (i + 1)),
            is_qualified=True,
        )

    trade = make_qualified_trade(timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(2.0)


# ── Filtering: only matching trades count ─────────────────────────────────────


async def test_different_outcome_not_counted(
    db_session, test_config: MegConfig
) -> None:
    """
    A prior NO trade when the current trade is YES does not count as a rung.
    Ladder is direction-specific: YES-side and NO-side are independent.
    """
    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    await insert_trade(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="NO",  # opposite direction
        tx_hash="0xno_trade",
        traded_at=datetime.now(tz=timezone.utc) - timedelta(hours=2),
        is_qualified=True,
    )

    trade = make_qualified_trade(outcome="YES", timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.0)


async def test_different_market_not_counted(
    db_session, test_config: MegConfig
) -> None:
    """Prior trades in a different market do not contribute rungs."""
    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    await insert_trade(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_DIFFERENT",  # different market
        outcome="YES",
        tx_hash="0xother_mkt",
        traded_at=datetime.now(tz=timezone.utc) - timedelta(hours=2),
        is_qualified=True,
    )

    trade = make_qualified_trade(market_id="market_001", timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.0)


async def test_different_wallet_not_counted(
    db_session, test_config: MegConfig
) -> None:
    """Prior trades from a different wallet do not count — ladder is per-wallet."""
    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    await insert_trade(
        db_session,
        wallet_address="0xOTHER_WHALE",  # different wallet
        market_id="market_001",
        outcome="YES",
        tx_hash="0xother_wallet",
        traded_at=datetime.now(tz=timezone.utc) - timedelta(hours=2),
        is_qualified=True,
    )

    trade = make_qualified_trade(wallet_address="0xWHALE001", timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.0)


async def test_trade_after_current_timestamp_not_counted(
    db_session, test_config: MegConfig
) -> None:
    """
    A trade with traded_at AFTER the current trade's timestamp must not count.
    Only strictly prior trades are rungs (future state is not available yet).
    """
    now = datetime.now(tz=timezone.utc)
    now_ms = int(now.timestamp() * 1000)
    future = now + timedelta(hours=1)

    await insert_trade(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        tx_hash="0xfuture_trade",
        traded_at=future,
        is_qualified=True,
    )

    trade = make_qualified_trade(timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.0)


async def test_trade_outside_window_not_counted(
    db_session, test_config: MegConfig
) -> None:
    """
    A qualified trade older than ladder_window_hours (default 6h) is excluded.
    The window is a sliding lookback — stale trades don't inflate the multiplier.
    """
    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    too_old = datetime.now(tz=timezone.utc) - timedelta(hours=8)  # outside 6h window

    await insert_trade(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        tx_hash="0xold_trade",
        traded_at=too_old,
        is_qualified=True,
    )

    trade = make_qualified_trade(timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.0)


async def test_unqualified_trade_not_counted(
    db_session, test_config: MegConfig
) -> None:
    """
    Trades with is_qualified=False (e.g. failed Gate 1) must not count as rungs.
    Only trades that passed all pre-filter gates are meaningful rung evidence.
    """
    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    await insert_trade(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        tx_hash="0xunqualified",
        traded_at=datetime.now(tz=timezone.utc) - timedelta(hours=2),
        is_qualified=False,  # not qualified — should not count
    )

    trade = make_qualified_trade(timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.0)


# ── Config-driven window ──────────────────────────────────────────────────────


async def test_respects_custom_ladder_window(
    db_session, test_config: MegConfig
) -> None:
    """
    When ladder_window_hours is shortened to 1h, a trade 2h ago is excluded.
    Confirms the window is read from config, not hardcoded.
    """
    test_config.pre_filter.ladder_window_hours = 1.0  # override: 1-hour window

    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    await insert_trade(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        tx_hash="0xoutside_narrow_window",
        traded_at=datetime.now(tz=timezone.utc) - timedelta(hours=2),  # outside 1h window
        is_qualified=True,
    )

    trade = make_qualified_trade(timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.0)


async def test_respects_custom_conviction_per_rung(
    db_session, test_config: MegConfig
) -> None:
    """
    When ladder_conviction_per_rung is overridden, the formula uses the new value.
    1 rung × 0.25 = 1.25 (not the default 0.15).
    """
    test_config.signal.ladder_conviction_per_rung = 0.25

    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    await insert_trade(
        db_session,
        wallet_address="0xWHALE001",
        market_id="market_001",
        outcome="YES",
        tx_hash="0xcustom_rung",
        traded_at=datetime.now(tz=timezone.utc) - timedelta(hours=2),
        is_qualified=True,
    )

    trade = make_qualified_trade(timestamp_ms=now_ms)
    result = await multiplier(trade, db_session, test_config)
    assert result == pytest.approx(1.25)
