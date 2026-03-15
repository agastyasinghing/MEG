"""
Tests for meg/signal_engine/kelly_sizer.py

⚠️  OPUS SPEC — module stubs raise NotImplementedError.
Implement kelly_sizer.compute_size() and _kelly_fraction() with Opus + ultrathink.
Sizing errors directly determine real money at risk.

Key implementation constraints:
  - compute_size() returns USDC float ≥ 0.0
  - Core formula: f* = (p * b - q) / b where b = (1-entry_price) / entry_price
  - Quarter-Kelly: final_fraction = f* * config.kelly.fraction (default 0.25)
  - Position size: min(final_fraction * portfolio_value_usdc, config.kelly.max_bet_usdc)
  - Returns 0.0 when Kelly fraction ≤ 0 (no positive edge — never bet)
  - Returns 0.0 when win_prob ≤ entry_price (no positive expected value)
  - Hard cap: never exceeds config.kelly.max_bet_usdc regardless of Kelly output

Binary market formula derivation:
  On a market priced at 0.40 (YES costs $0.40, pays $1.00):
    net odds b = (1.0 - 0.40) / 0.40 = 1.5  (win $1.50 per $1 risked)
    if win_prob = 0.60: f* = (0.60 * 1.5 - 0.40) / 1.5 = (0.90 - 0.40) / 1.5 = 0.333
    quarter Kelly: 0.333 * 0.25 = 0.083 = 8.3% of portfolio

PRD reference: §9.3.5 Kelly Position Sizer
"""
from __future__ import annotations

import pytest

from meg.core.config_loader import MegConfig
from meg.signal_engine.kelly_sizer import _kelly_fraction, compute_size
from tests.signal_engine.conftest import make_qualified_trade

pytestmark = pytest.mark.xfail(
    reason="OPUS SPEC: kelly_sizer stubs raise NotImplementedError",
    strict=False,
)


# ── _kelly_fraction() ─────────────────────────────────────────────────────────


def test_kelly_fraction_positive_edge() -> None:
    """
    win_prob=0.60, payout_odds=1.5 (market priced at 0.40):
    f* = (0.60 * 1.5 - 0.40) / 1.5 = 0.50/1.5 ≈ 0.333
    """
    result = _kelly_fraction(win_probability=0.60, payout_odds=1.5)
    assert result == pytest.approx(0.333, abs=0.01)


def test_kelly_fraction_no_edge_returns_0() -> None:
    """
    When win_prob * odds == loss_prob, Kelly fraction = 0 (breakeven — don't bet).
    win_prob=0.40, payout_odds=1.5: f* = (0.40*1.5 - 0.60)/1.5 = (0.60-0.60)/1.5 = 0
    """
    result = _kelly_fraction(win_probability=0.40, payout_odds=1.5)
    assert result == pytest.approx(0.0, abs=0.001)


def test_kelly_fraction_negative_edge_returns_0() -> None:
    """
    Negative Kelly (unfavorable bet) must return 0.0, never a negative fraction.
    win_prob=0.30, payout_odds=1.0: f* = (0.30*1.0 - 0.70)/1.0 = -0.40 → clamp to 0
    """
    result = _kelly_fraction(win_probability=0.30, payout_odds=1.0)
    assert result == pytest.approx(0.0)


def test_kelly_fraction_certainty_returns_1() -> None:
    """
    100% win probability with any positive odds → f* = 1.0 (all in).
    Theoretical max: win_prob=1.0, payout_odds=b: f* = (1.0*b - 0) / b = 1.0
    """
    result = _kelly_fraction(win_probability=1.0, payout_odds=2.0)
    assert result == pytest.approx(1.0)


# ── compute_size() ────────────────────────────────────────────────────────────


def test_positive_edge_returns_positive_size(test_config: MegConfig) -> None:
    """
    win_prob=0.65 on a 0.40-priced market = clear positive edge → positive size.
    b = 0.60/0.40 = 1.5
    """
    trade = make_qualified_trade(market_price_at_trade=0.40)
    result = compute_size(
        trade=trade,
        win_prob=0.65,
        entry_price=0.40,
        portfolio_value_usdc=10_000.0,
        config=test_config,
    )
    assert result > 0.0


def test_no_edge_returns_zero(test_config: MegConfig) -> None:
    """
    win_prob equal to entry_price = no positive expected value → size = 0.0.
    Market is fairly priced for this win_prob estimate.
    """
    trade = make_qualified_trade(market_price_at_trade=0.50)
    result = compute_size(
        trade=trade,
        win_prob=0.50,  # same as market price — no edge
        entry_price=0.50,
        portfolio_value_usdc=10_000.0,
        config=test_config,
    )
    assert result == pytest.approx(0.0)


def test_negative_edge_returns_zero(test_config: MegConfig) -> None:
    """
    win_prob below market implied probability = negative edge → must return 0.0.
    Never bet when Kelly is negative.
    """
    trade = make_qualified_trade(market_price_at_trade=0.70)
    result = compute_size(
        trade=trade,
        win_prob=0.50,  # market says 70% chance, we only think 50%
        entry_price=0.70,
        portfolio_value_usdc=10_000.0,
        config=test_config,
    )
    assert result == pytest.approx(0.0)


def test_hard_cap_applied(test_config: MegConfig) -> None:
    """
    Even with massive portfolio and great edge, size is capped at config.kelly.max_bet_usdc.
    With max_bet_usdc=1000 and portfolio_value_usdc=1_000_000, Kelly would suggest huge bet.
    """
    test_config.kelly.max_bet_usdc = 1_000.0
    trade = make_qualified_trade(market_price_at_trade=0.10)  # extreme edge: buy at 0.10

    result = compute_size(
        trade=trade,
        win_prob=0.90,
        entry_price=0.10,
        portfolio_value_usdc=1_000_000.0,
        config=test_config,
    )
    assert result <= 1_000.0


def test_quarter_kelly_scaling(test_config: MegConfig) -> None:
    """
    Full Kelly fraction is scaled by config.kelly.fraction (default 0.25).
    Result should be ≤ 25% of what full Kelly would recommend.
    """
    test_config.kelly.fraction = 0.25
    test_config.kelly.max_bet_usdc = 100_000.0  # disable cap for this test

    trade = make_qualified_trade(market_price_at_trade=0.40)
    full_kelly_size = compute_size(
        trade=trade,
        win_prob=0.65,
        entry_price=0.40,
        portfolio_value_usdc=10_000.0,
        config=test_config,
    )

    test_config.kelly.fraction = 1.0  # full Kelly
    full_kelly_size_unbounded = compute_size(
        trade=trade,
        win_prob=0.65,
        entry_price=0.40,
        portfolio_value_usdc=10_000.0,
        config=test_config,
    )

    assert full_kelly_size <= full_kelly_size_unbounded * 0.26  # ≤ 25% + tiny float tolerance


def test_higher_portfolio_produces_larger_size(test_config: MegConfig) -> None:
    """Kelly size scales with portfolio value (same fraction, bigger pool = bigger bet)."""
    test_config.kelly.max_bet_usdc = 100_000.0  # disable cap

    trade = make_qualified_trade(market_price_at_trade=0.40)

    small_portfolio = compute_size(
        trade=trade, win_prob=0.65, entry_price=0.40,
        portfolio_value_usdc=1_000.0, config=test_config,
    )
    large_portfolio = compute_size(
        trade=trade, win_prob=0.65, entry_price=0.40,
        portfolio_value_usdc=100_000.0, config=test_config,
    )

    assert large_portfolio > small_portfolio
