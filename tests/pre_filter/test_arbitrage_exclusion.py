"""
Tests for pre_filter/arbitrage_exclusion.py (Gate 2).

Coverage map:
  ARBITRAGE archetype → short-circuit (no DB query)
    → test_check_arb_archetype_short_circuits

  Absent archetype → proceed to behavioral check (no arb found)
    → test_check_absent_archetype_proceeds_to_behavioral

  Behavioral: YES + NO within window → False
    → test_check_simultaneous_both_sides_in_window

  Behavioral: only YES trades → True
    → test_check_only_yes_trades_passes

  Behavioral: only NO trades → True
    → test_check_only_no_trades_passes

  Behavioral: YES + NO outside window → True
    → test_check_both_sides_outside_window_passes

  INFORMATION archetype, no both-sides → True
    → test_check_information_archetype_passes

  MANIPULATOR archetype passes Gate 2 (excluded elsewhere)
    → test_check_manipulator_archetype_passes_gate2

  session=None → behavioral check skipped (returns True if clean archetype)
    → test_check_no_session_skips_behavioral

  Redis error on archetype lookup → treats as non-arb (proceeds to behavioral)
    → (covered implicitly by absent_archetype test; explicit error tested below)
    → test_check_archetype_redis_error_falls_through

  _is_arb_archetype: ARBITRAGE → True
    → test_is_arb_archetype_arbitrage

  _is_arb_archetype: MOMENTUM → False
    → test_is_arb_archetype_non_arb

  _is_arb_archetype: absent key → False
    → test_is_arb_archetype_absent_key
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys
from meg.pre_filter import arbitrage_exclusion
from tests.pre_filter.conftest import (
    insert_trade_record,
    make_raw_trade,
    set_wallet_redis_data,
)


# ── Archetype short-circuit ───────────────────────────────────────────────────


async def test_check_arb_archetype_short_circuits(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    ARBITRAGE archetype in Redis → check() returns False immediately.
    The behavioral DB query must NOT be called (no trades needed in DB).
    """
    trade = make_raw_trade(wallet_address="0xARB001", market_id="market_001")
    await set_wallet_redis_data(mock_redis, wallet_address="0xARB001", archetype="ARBITRAGE")
    # Intentionally no Trade records inserted — if DB were queried, it would
    # find no both-sides trades and return True. The archetype short-circuit
    # must prevent any DB access.

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, db_session)

    assert result is False


async def test_check_absent_archetype_proceeds_to_behavioral(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    When archetype key is absent, Gate 2 proceeds to the behavioral check.
    With no both-sides trades in the DB, the trade passes.
    """
    trade = make_raw_trade(wallet_address="0xUNKNOWN001", market_id="market_001")
    # No archetype key set — unknown wallet

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, db_session)

    assert result is True


# ── Behavioral detection ──────────────────────────────────────────────────────


async def test_check_simultaneous_both_sides_in_window(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    YES and NO trades for the same wallet+market within arb_detection_window_hours
    → check() returns False (behavioral arb detected).
    """
    trade = make_raw_trade(wallet_address="0xBOTH001", market_id="market_001")
    await set_wallet_redis_data(
        mock_redis, wallet_address="0xBOTH001", archetype="MOMENTUM"
    )
    now = datetime.now(tz=timezone.utc)
    await insert_trade_record(
        db_session,
        wallet_address="0xBOTH001",
        market_id="market_001",
        outcome="YES",
        tx_hash="0xtx_yes",
        traded_at=now - timedelta(hours=2),
    )
    await insert_trade_record(
        db_session,
        wallet_address="0xBOTH001",
        market_id="market_001",
        outcome="NO",
        tx_hash="0xtx_no",
        traded_at=now - timedelta(hours=1),
    )

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, db_session)

    assert result is False


async def test_check_only_yes_trades_passes(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """Only YES trades in the window → not an arb → check() returns True."""
    trade = make_raw_trade(wallet_address="0xYES001", market_id="market_001")
    await set_wallet_redis_data(
        mock_redis, wallet_address="0xYES001", archetype="INFORMATION"
    )
    now = datetime.now(tz=timezone.utc)
    for i in range(3):
        await insert_trade_record(
            db_session,
            wallet_address="0xYES001",
            market_id="market_001",
            outcome="YES",
            tx_hash=f"0xtx_yes_{i}",
            traded_at=now - timedelta(hours=i + 1),
        )

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, db_session)

    assert result is True


async def test_check_only_no_trades_passes(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """Only NO trades in the window → not an arb → check() returns True."""
    trade = make_raw_trade(
        wallet_address="0xNO001", market_id="market_001", outcome="NO"
    )
    await set_wallet_redis_data(
        mock_redis, wallet_address="0xNO001", archetype="INFORMATION"
    )
    now = datetime.now(tz=timezone.utc)
    await insert_trade_record(
        db_session,
        wallet_address="0xNO001",
        market_id="market_001",
        outcome="NO",
        tx_hash="0xtx_no_only",
        traded_at=now - timedelta(hours=1),
    )

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, db_session)

    assert result is True


async def test_check_both_sides_outside_window_passes(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    YES and NO trades exist, but both are older than arb_detection_window_hours
    → outside the window → not flagged as arb → returns True.
    """
    trade = make_raw_trade(wallet_address="0xOLD001", market_id="market_001")
    await set_wallet_redis_data(
        mock_redis, wallet_address="0xOLD001", archetype="MOMENTUM"
    )
    window_hours = test_config.pre_filter.arb_detection_window_hours
    now = datetime.now(tz=timezone.utc)
    outside_window = now - timedelta(hours=window_hours + 2)

    await insert_trade_record(
        db_session,
        wallet_address="0xOLD001",
        market_id="market_001",
        outcome="YES",
        tx_hash="0xtx_old_yes",
        traded_at=outside_window,
    )
    await insert_trade_record(
        db_session,
        wallet_address="0xOLD001",
        market_id="market_001",
        outcome="NO",
        tx_hash="0xtx_old_no",
        traded_at=outside_window,
    )

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, db_session)

    assert result is True


# ── Archetype variants ────────────────────────────────────────────────────────


async def test_check_information_archetype_passes(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """INFORMATION archetype + no both-sides behavioral pattern → passes Gate 2."""
    trade = make_raw_trade(wallet_address="0xINFO001", market_id="market_001")
    await set_wallet_redis_data(
        mock_redis, wallet_address="0xINFO001", archetype="INFORMATION"
    )

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, db_session)

    assert result is True


async def test_check_manipulator_archetype_passes_gate2(
    mock_redis: Redis, test_config: MegConfig, db_session: AsyncSession
) -> None:
    """
    MANIPULATOR archetype passes Gate 2. Manipulators are excluded via
    wallet_registry.is_qualified() / whale_qualification.exclude_archetypes,
    not by Gate 2 (which is specifically for arb exclusion).
    """
    trade = make_raw_trade(wallet_address="0xMANIP001", market_id="market_001")
    await set_wallet_redis_data(
        mock_redis, wallet_address="0xMANIP001", archetype="MANIPULATOR"
    )

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, db_session)

    assert result is True


# ── Session=None edge case ────────────────────────────────────────────────────


async def test_check_no_session_skips_behavioral(
    mock_redis: Redis, test_config: MegConfig
) -> None:
    """
    When session=None, the behavioral DB check is skipped entirely.
    A wallet with MOMENTUM archetype passes without any DB query.
    """
    trade = make_raw_trade(wallet_address="0xMOM001", market_id="market_001")
    await set_wallet_redis_data(
        mock_redis, wallet_address="0xMOM001", archetype="MOMENTUM"
    )

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, session=None)

    assert result is True


# ── _is_arb_archetype unit tests ──────────────────────────────────────────────


async def test_is_arb_archetype_arbitrage(mock_redis: Redis) -> None:
    """wallet with ARBITRAGE archetype → _is_arb_archetype returns True."""
    await mock_redis.set(RedisKeys.wallet_archetype("0xARB"), "ARBITRAGE")
    result = await arbitrage_exclusion._is_arb_archetype("0xARB", mock_redis)
    assert result is True


async def test_is_arb_archetype_non_arb(mock_redis: Redis) -> None:
    """wallet with MOMENTUM archetype → _is_arb_archetype returns False."""
    await mock_redis.set(RedisKeys.wallet_archetype("0xMOM"), "MOMENTUM")
    result = await arbitrage_exclusion._is_arb_archetype("0xMOM", mock_redis)
    assert result is False


async def test_is_arb_archetype_absent_key(mock_redis: Redis) -> None:
    """Absent archetype key → _is_arb_archetype returns False (unknown wallet is non-arb)."""
    result = await arbitrage_exclusion._is_arb_archetype("0xNOKEY", mock_redis)
    assert result is False


async def test_check_archetype_redis_error_falls_through(
    mock_redis: Redis, test_config: MegConfig, mocker
) -> None:
    """
    When redis.get raises ConnectionError during archetype lookup, _is_arb_archetype
    returns False (treats as non-arb) and the trade proceeds to the behavioral check.
    With session=None the behavioral check is skipped → check() returns True overall.
    """
    trade = make_raw_trade(wallet_address="0xREDIS_ERR", market_id="market_001")
    mocker.patch.object(mock_redis, "get", side_effect=ConnectionError("Redis timeout"))

    result = await arbitrage_exclusion.check(trade, mock_redis, test_config, session=None)

    assert result is True
