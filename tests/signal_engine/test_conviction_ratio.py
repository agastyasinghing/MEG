"""
Tests for meg/signal_engine/conviction_ratio.py

⚠️  OPUS SPEC — module stubs raise NotImplementedError.
Implement conviction_ratio.score() and get_wallet_capital() with Sonnet.
(This module is Sonnet-eligible — logic is straightforward division + normalisation.)

Key implementation constraints:
  - score() returns a float in [0.0, 1.0]
  - Core formula: min(trade.size_usdc / wallet_capital, 1.0)
  - wallet_capital = get_wallet_capital(wallet_data) (sync helper)
  - get_wallet_capital() prefers total_capital_usdc (from Polygon USDC balance refresh)
  - Falls back to total_volume_usdc as proxy when total_capital_usdc is None
  - Falls back to 1.0 (safe fallback) to avoid division by zero
  - score() normalises the raw fraction: a 5% bet is moderate, 40% is high conviction

wallet_data keys: total_capital_usdc (float | None), total_volume_usdc (float)

PRD reference: §9.3.3 Conviction Ratio
"""
from __future__ import annotations

import pytest

from meg.core.config_loader import MegConfig
from meg.signal_engine.conviction_ratio import get_wallet_capital, score
from tests.signal_engine.conftest import make_qualified_trade, make_wallet_data


# ── get_wallet_capital() ──────────────────────────────────────────────────────


def test_prefers_total_capital_usdc_over_volume() -> None:
    """
    total_capital_usdc is the accurate Polygon USDC balance — prefer it.
    total_volume_usdc is a rough proxy and should only be used as fallback.
    """
    wallet_data = make_wallet_data(total_capital_usdc=80_000.0, total_volume_usdc=200_000.0)
    capital = get_wallet_capital(wallet_data)
    assert capital == pytest.approx(80_000.0)


def test_falls_back_to_volume_when_capital_is_none() -> None:
    """When total_capital_usdc is None, use total_volume_usdc as proxy."""
    wallet_data = make_wallet_data(total_capital_usdc=None, total_volume_usdc=150_000.0)
    capital = get_wallet_capital(wallet_data)
    assert capital == pytest.approx(150_000.0)


def test_fallback_to_1_0_when_both_missing() -> None:
    """
    When both capital fields are missing/zero, return 1.0 to avoid division by zero.
    A conviction score of size_usdc / 1.0 is effectively size_usdc — but capped at 1.0
    by the score() formula. This is the safe conservative fallback.
    """
    wallet_data = make_wallet_data(total_capital_usdc=None, total_volume_usdc=0.0)
    capital = get_wallet_capital(wallet_data)
    assert capital >= 1.0  # must never be 0 or negative


# ── score() return range ──────────────────────────────────────────────────────


async def test_score_returns_float_in_unit_interval(test_config: MegConfig) -> None:
    """score() must always return a value in [0.0, 1.0]."""
    trade = make_qualified_trade(size_usdc=2_000.0)
    wallet_data = make_wallet_data(total_capital_usdc=50_000.0)
    result = await score(trade, wallet_data, test_config)
    assert 0.0 <= result <= 1.0


# ── Conviction logic ──────────────────────────────────────────────────────────


async def test_large_bet_relative_to_capital_high_conviction(test_config: MegConfig) -> None:
    """
    Betting 40% of capital (20k of 50k) is high conviction.
    Score should be materially higher than a 1% bet.
    """
    trade_large = make_qualified_trade(size_usdc=20_000.0)
    trade_small = make_qualified_trade(size_usdc=500.0)
    wallet_data = make_wallet_data(total_capital_usdc=50_000.0)

    large_score = await score(trade_large, wallet_data, test_config)
    small_score = await score(trade_small, wallet_data, test_config)

    assert large_score > small_score


async def test_bet_exceeding_capital_capped_at_1_0(test_config: MegConfig) -> None:
    """
    A trade larger than total capital (e.g. leverage or capital estimate error)
    must be capped at 1.0 — never return > 1.0.
    """
    trade = make_qualified_trade(size_usdc=100_000.0)
    wallet_data = make_wallet_data(total_capital_usdc=10_000.0)  # trade > capital

    result = await score(trade, wallet_data, test_config)
    assert result <= 1.0


async def test_very_small_bet_produces_low_conviction(test_config: MegConfig) -> None:
    """
    A 0.1% bet (100 USDC on 100k capital) should produce a low conviction score.
    """
    trade = make_qualified_trade(size_usdc=100.0)
    wallet_data = make_wallet_data(total_capital_usdc=100_000.0)

    result = await score(trade, wallet_data, test_config)
    assert result < 0.05  # 0.1% bet = very low conviction


async def test_uses_capital_not_volume_when_available(test_config: MegConfig) -> None:
    """
    score() uses total_capital_usdc (not total_volume_usdc) when both are present.
    Same trade, same volume proxy, but different capital → different score.
    """
    trade = make_qualified_trade(size_usdc=5_000.0)

    # Both have the same volume proxy but different capital
    wallet_small_capital = make_wallet_data(total_capital_usdc=10_000.0, total_volume_usdc=500_000.0)
    wallet_large_capital = make_wallet_data(total_capital_usdc=100_000.0, total_volume_usdc=500_000.0)

    score_small = await score(trade, wallet_small_capital, test_config)
    score_large = await score(trade, wallet_large_capital, test_config)

    # Smaller capital → larger fraction bet → higher conviction
    assert score_small > score_large
