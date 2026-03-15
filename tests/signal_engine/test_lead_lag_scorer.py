"""
Tests for meg/signal_engine/lead_lag_scorer.py

⚠️  OPUS SPEC — module stubs raise NotImplementedError.
Implement lead_lag_scorer.score() and compute_reputation_decay() with
Opus + ultrathink. Read these tests first and implement against them.

Key implementation constraints:
  - score() returns a float in [0.0, 1.0]
  - score() internally calls compute_reputation_decay() to apply decay
  - compute_reputation_decay() reads last_profitable_trade_at from wallet_data dict
  - decay formula: exp(-days_since_last_good_trade / tau); tau = config.reputation.decay_tau_days
  - When last_profitable_trade_at is None → decay_factor = 1.0 (no penalty; conservative)
  - lead_lag score is primarily driven by avg_lead_time_hours and win_rate
  - Higher avg_lead_time_hours = more consistently early = higher raw score
  - Decay is a MULTIPLIER applied to raw score (not a subtraction)
  - score() must NEVER return > 1.0 or < 0.0

wallet_data dict keys (from make_wallet_data in conftest):
  avg_lead_time_hours, win_rate, total_capital_usdc, total_volume_usdc,
  last_profitable_trade_at (ISO str | None), reputation_decay_factor

PRD reference: §9.3.1 Lead-Lag Scorer, §9.3.2 Reputation Decay
"""
from __future__ import annotations

import pytest

from meg.core.config_loader import MegConfig
from meg.signal_engine.lead_lag_scorer import compute_reputation_decay, score
from tests.signal_engine.conftest import make_qualified_trade, make_wallet_data

pytestmark = pytest.mark.xfail(
    reason="OPUS SPEC: lead_lag_scorer stubs raise NotImplementedError",
    strict=False,
)


# ── score() return range ──────────────────────────────────────────────────────


async def test_score_returns_float_in_unit_interval(test_config: MegConfig) -> None:
    """score() must return a value in [0.0, 1.0] — never outside bounds."""
    trade = make_qualified_trade()
    wallet_data = make_wallet_data()
    result = await score(trade, wallet_data, test_config)
    assert 0.0 <= result <= 1.0


async def test_high_lead_time_produces_higher_score(test_config: MegConfig) -> None:
    """
    A whale with avg_lead_time_hours=12 (enters 12h before price moves) must
    score higher than avg_lead_time_hours=1 (barely ahead of the crowd).
    """
    trade = make_qualified_trade()
    early_whale = make_wallet_data(avg_lead_time_hours=12.0, win_rate=0.65)
    late_whale = make_wallet_data(avg_lead_time_hours=1.0, win_rate=0.65)

    early_score = await score(trade, early_whale, test_config)
    late_score = await score(trade, late_whale, test_config)

    assert early_score > late_score


async def test_high_win_rate_produces_higher_score(test_config: MegConfig) -> None:
    """
    Holding lead time constant, a 75% win rate whale should outscore a 55% win rate whale.
    """
    trade = make_qualified_trade()
    strong = make_wallet_data(avg_lead_time_hours=6.0, win_rate=0.75)
    weak = make_wallet_data(avg_lead_time_hours=6.0, win_rate=0.55)

    strong_score = await score(trade, strong, test_config)
    weak_score = await score(trade, weak, test_config)

    assert strong_score > weak_score


# ── compute_reputation_decay() ────────────────────────────────────────────────


async def test_no_profitable_trade_returns_no_decay(test_config: MegConfig) -> None:
    """
    last_profitable_trade_at=None → decay_factor = 1.0 (no penalty).
    Conservative: new wallets or those with no profitable history are not penalised.
    """
    wallet_data = make_wallet_data(last_profitable_trade_at=None)
    factor = await compute_reputation_decay(wallet_data, test_config)
    assert factor == pytest.approx(1.0)


async def test_recent_profitable_trade_minimal_decay(test_config: MegConfig) -> None:
    """
    A profitable trade 1 day ago should have near-full factor (close to 1.0).
    With tau=30 days: exp(-1/30) ≈ 0.967
    """
    from datetime import datetime, timedelta, timezone

    yesterday = (datetime.now(tz=timezone.utc) - timedelta(days=1)).isoformat()
    wallet_data = make_wallet_data(last_profitable_trade_at=yesterday)
    factor = await compute_reputation_decay(wallet_data, test_config)
    # exp(-1/30) ≈ 0.967 — allow ±0.05 tolerance
    assert factor == pytest.approx(0.967, abs=0.05)


async def test_old_profitable_trade_significant_decay(test_config: MegConfig) -> None:
    """
    A profitable trade 90 days ago with tau=30: exp(-90/30) = exp(-3) ≈ 0.05.
    Score should be heavily reduced — wallet hasn't had a good trade in 3 months.
    """
    from datetime import datetime, timedelta, timezone

    ninety_days_ago = (datetime.now(tz=timezone.utc) - timedelta(days=90)).isoformat()
    wallet_data = make_wallet_data(last_profitable_trade_at=ninety_days_ago)
    factor = await compute_reputation_decay(wallet_data, test_config)
    # exp(-3) ≈ 0.05 — significant decay
    assert factor < 0.15


async def test_decay_factor_in_unit_interval(test_config: MegConfig) -> None:
    """decay_factor must always be in (0.0, 1.0]. Never negative, never > 1."""
    from datetime import datetime, timedelta, timezone

    for days_ago in [0, 7, 30, 90, 365]:
        dt = (datetime.now(tz=timezone.utc) - timedelta(days=days_ago)).isoformat()
        wallet_data = make_wallet_data(last_profitable_trade_at=dt)
        factor = await compute_reputation_decay(wallet_data, test_config)
        assert 0.0 < factor <= 1.0, f"factor={factor} out of range for days_ago={days_ago}"


async def test_longer_tau_means_slower_decay(test_config: MegConfig) -> None:
    """
    Increasing tau (decay_tau_days) reduces the decay for the same elapsed time.
    tau=60 should produce a higher factor than tau=15 for the same 30-day gap.
    """
    from datetime import datetime, timedelta, timezone

    thirty_days_ago = (datetime.now(tz=timezone.utc) - timedelta(days=30)).isoformat()
    wallet_data = make_wallet_data(last_profitable_trade_at=thirty_days_ago)

    test_config.reputation.decay_tau_days = 60.0
    factor_slow = await compute_reputation_decay(wallet_data, test_config)

    test_config.reputation.decay_tau_days = 15.0
    factor_fast = await compute_reputation_decay(wallet_data, test_config)

    assert factor_slow > factor_fast


# ── Integration: decay applied to score ──────────────────────────────────────


async def test_decayed_wallet_scores_lower_than_fresh(test_config: MegConfig) -> None:
    """
    Same whale archetype and lead time, but one has a 90-day-old last profitable
    trade vs. a 1-day-old one. The stale wallet should score materially lower.
    """
    from datetime import datetime, timedelta, timezone

    trade = make_qualified_trade()
    fresh = make_wallet_data(
        avg_lead_time_hours=8.0,
        last_profitable_trade_at=(
            datetime.now(tz=timezone.utc) - timedelta(days=1)
        ).isoformat(),
    )
    stale = make_wallet_data(
        avg_lead_time_hours=8.0,
        last_profitable_trade_at=(
            datetime.now(tz=timezone.utc) - timedelta(days=90)
        ).isoformat(),
    )

    fresh_score = await score(trade, fresh, test_config)
    stale_score = await score(trade, stale, test_config)

    assert fresh_score > stale_score
