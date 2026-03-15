"""
Tests for meg/signal_engine/composite_scorer.py

⚠️  OPUS SPEC — module stubs raise NotImplementedError.
Implement composite_scorer.score(), _gather_component_scores(), and _combine_scores()
with Opus + ultrathink. This is the most financially consequential module.

PRD §9.3.9 composite score formula (see composite_scorer.py docstring for full spec):
  Step 1: base = lead_lag*0.35 + consensus*0.30 + kelly*0.20 + divergence*0.15
  Step 2: adjusted = base * archetype_mult * ladder_mult
  Step 3: final = adjusted * 0.85 + conviction_ratio * 0.15

Key implementation constraints for score():
  - Takes (trade, redis, session, config) → SignalEvent
  - Pre-fetches wallet_data ONCE from Redis, passes to sub-scorers (no N lookups)
  - If wallet_data unavailable → raise SignalDroppedError(reason="wallet_data_miss")
  - If lead_lag_score < config.signal.lead_lag_min_gate → raise SignalDroppedError
  - All sub-scorers called with asyncio.gather() (concurrent, not sequential)
  - Sets signal.status = PENDING if composite_score >= threshold; FILTERED otherwise
  - Always writes signal_outcomes record (training data moat)
  - SignalDroppedError must be caught by caller and logged to signal_outcomes with
    status=FILTERED and score=0.0

Key constraints for _combine_scores():
  - Uses config.signal.composite_weights (hot-reloadable, not hardcoded)
  - Result clamped to [0.0, 1.0]

Tests use AsyncMock to stub sub-scorer modules, letting composite_scorer logic
be tested without requiring Opus implementations of each sub-module.
"""
from __future__ import annotations

import time
from unittest.mock import AsyncMock, patch

import pytest

from meg.core.config_loader import MegConfig
from meg.core.events import SignalDroppedError
from meg.signal_engine.composite_scorer import _combine_scores
from tests.signal_engine.conftest import make_qualified_trade, make_wallet_data


# ── _combine_scores() — pure function, no mocks needed ───────────────────────


def test_combine_scores_with_full_weights(test_config: MegConfig) -> None:
    """
    PRD §9.3.9 formula verification with known inputs:
      lead_lag=0.80, consensus=0.60, kelly=0.50, divergence=0.70, conviction=0.40
      archetype_mult=1.0, ladder_mult=1.0

    Step 1: base = 0.80*0.35 + 0.60*0.30 + 0.50*0.20 + 0.70*0.15
                 = 0.280 + 0.180 + 0.100 + 0.105 = 0.665
    Step 2: adjusted = 0.665 * 1.0 * 1.0 = 0.665
    Step 3: final = 0.665 * 0.85 + 0.40 * 0.15 = 0.565 + 0.060 = 0.625
    """
    components = {
        "lead_lag": 0.80,
        "consensus": 0.60,
        "kelly": 0.50,
        "contrarian": 0.70,
        "conviction": 0.40,
        "archetype_mult": 1.0,
        "ladder_mult": 1.0,
    }
    result = _combine_scores(components, test_config)
    assert result == pytest.approx(0.625, abs=0.01)


def test_combine_scores_zero_archetype_mult_produces_zero(test_config: MegConfig) -> None:
    """
    ARBITRAGE archetype_mult=0.0 → adjusted=0 → final = 0 * 0.85 + conviction * 0.15.
    If conviction=0.40: final = 0.060 (only conviction survives the zero mult).
    """
    components = {
        "lead_lag": 0.90,
        "consensus": 0.80,
        "kelly": 0.70,
        "contrarian": 0.60,
        "conviction": 0.40,
        "archetype_mult": 0.0,  # ARBITRAGE
        "ladder_mult": 1.0,
    }
    result = _combine_scores(components, test_config)
    # Only conviction_ratio survives: 0.0 * 0.85 + 0.40 * 0.15 = 0.06
    assert result == pytest.approx(0.06, abs=0.01)


def test_combine_scores_ladder_mult_amplifies(test_config: MegConfig) -> None:
    """
    ladder_mult=1.30 should produce a higher score than ladder_mult=1.0,
    all else equal.
    """
    base_components = {
        "lead_lag": 0.70,
        "consensus": 0.60,
        "kelly": 0.50,
        "contrarian": 0.55,
        "conviction": 0.40,
        "archetype_mult": 1.0,
        "ladder_mult": 1.0,
    }
    ladder_components = {**base_components, "ladder_mult": 1.30}

    base_result = _combine_scores(base_components, test_config)
    ladder_result = _combine_scores(ladder_components, test_config)
    assert ladder_result > base_result


def test_combine_scores_result_clamped_to_unit_interval(test_config: MegConfig) -> None:
    """
    Even with all scores at 1.0 and maximum multipliers, result must not exceed 1.0.
    """
    components = {
        "lead_lag": 1.0,
        "consensus": 1.0,
        "kelly": 1.0,
        "contrarian": 1.0,
        "conviction": 1.0,
        "archetype_mult": 1.0,
        "ladder_mult": 2.0,  # maximum ladder multiplier
    }
    result = _combine_scores(components, test_config)
    assert result <= 1.0


def test_combine_scores_uses_config_weights(test_config: MegConfig) -> None:
    """
    Overriding composite_weights changes the result.
    Set lead_lag weight to 0.0 — lead_lag contribution should vanish.
    """
    test_config.signal.composite_weights.lead_lag = 0.0
    test_config.signal.composite_weights.consensus = 0.50
    test_config.signal.composite_weights.kelly = 0.30
    test_config.signal.composite_weights.divergence = 0.20

    components = {
        "lead_lag": 1.0,    # zero weight — should not contribute
        "consensus": 0.60,
        "kelly": 0.50,
        "contrarian": 0.70,
        "conviction": 0.40,
        "archetype_mult": 1.0,
        "ladder_mult": 1.0,
    }
    result = _combine_scores(components, test_config)
    # lead_lag has zero weight: base = 0*0 + 0.60*0.50 + 0.50*0.30 + 0.70*0.20
    #                                = 0 + 0.30 + 0.15 + 0.14 = 0.59
    # final = 0.59 * 0.85 + 0.40 * 0.15 = 0.5015 + 0.06 = 0.5615
    assert result == pytest.approx(0.5615, abs=0.01)


# ── score() — integration tests with mocked sub-scorers ──────────────────────

_OPUS_XFAIL = pytest.mark.xfail(
    reason="OPUS SPEC: composite_scorer.score() stub raises NotImplementedError",
    strict=False,
)


@_OPUS_XFAIL
async def test_score_below_threshold_sets_filtered_status(
    mock_redis, db_session, test_config: MegConfig
) -> None:
    """
    When composite_score < config.signal.composite_score_threshold (0.45),
    the returned SignalEvent must have status=FILTERED.
    """
    import json

    trade = make_qualified_trade()
    wallet_data = make_wallet_data()

    # Write wallet data to Redis so pre-fetch succeeds
    from meg.core.events import RedisKeys
    await mock_redis.set(
        RedisKeys.wallet_data(trade.wallet_address), json.dumps(wallet_data)
    )

    # Patch all sub-scorers to return values that produce a low composite
    with (
        patch("meg.signal_engine.composite_scorer.lead_lag_scorer") as mock_ll,
        patch("meg.signal_engine.composite_scorer.conviction_ratio") as mock_cr,
        patch("meg.signal_engine.composite_scorer.kelly_sizer") as mock_ks,
        patch("meg.signal_engine.composite_scorer.consensus_filter") as mock_cf,
        patch("meg.signal_engine.composite_scorer.contrarian_detector") as mock_cd,
        patch("meg.signal_engine.composite_scorer.ladder_detector") as mock_ld,
        patch("meg.signal_engine.composite_scorer.archetype_weighter") as mock_aw,
    ):
        mock_ll.score = AsyncMock(return_value=0.20)
        mock_cr.score = AsyncMock(return_value=0.15)
        mock_ks.compute_size = AsyncMock(return_value=0.0)
        mock_cf.score = AsyncMock(return_value=0.10)
        mock_cd.score = AsyncMock(return_value=0.20)
        mock_ld.multiplier = AsyncMock(return_value=1.0)
        mock_aw.weight = lambda archetype, config: 1.0

        from meg.signal_engine.composite_scorer import score
        signal = await score(trade, mock_redis, db_session, test_config)

    assert signal.status == "FILTERED"
    assert signal.composite_score < test_config.signal.composite_score_threshold


@_OPUS_XFAIL
async def test_score_above_threshold_sets_pending_status(
    mock_redis, db_session, test_config: MegConfig
) -> None:
    """
    When composite_score >= composite_score_threshold (0.45), status must be PENDING.
    """
    import json

    trade = make_qualified_trade()
    wallet_data = make_wallet_data()

    from meg.core.events import RedisKeys
    await mock_redis.set(
        RedisKeys.wallet_data(trade.wallet_address), json.dumps(wallet_data)
    )

    with (
        patch("meg.signal_engine.composite_scorer.lead_lag_scorer") as mock_ll,
        patch("meg.signal_engine.composite_scorer.conviction_ratio") as mock_cr,
        patch("meg.signal_engine.composite_scorer.kelly_sizer") as mock_ks,
        patch("meg.signal_engine.composite_scorer.consensus_filter") as mock_cf,
        patch("meg.signal_engine.composite_scorer.contrarian_detector") as mock_cd,
        patch("meg.signal_engine.composite_scorer.ladder_detector") as mock_ld,
        patch("meg.signal_engine.composite_scorer.archetype_weighter") as mock_aw,
    ):
        mock_ll.score = AsyncMock(return_value=0.80)
        mock_cr.score = AsyncMock(return_value=0.70)
        mock_ks.compute_size = AsyncMock(return_value=200.0)
        mock_cf.score = AsyncMock(return_value=0.75)
        mock_cd.score = AsyncMock(return_value=0.65)
        mock_ld.multiplier = AsyncMock(return_value=1.15)
        mock_aw.weight = lambda archetype, config: 1.0

        from meg.signal_engine.composite_scorer import score
        signal = await score(trade, mock_redis, db_session, test_config)

    assert signal.status == "PENDING"
    assert signal.composite_score >= test_config.signal.composite_score_threshold


@_OPUS_XFAIL
async def test_lead_lag_below_gate_raises_signal_dropped_error(
    mock_redis, db_session, test_config: MegConfig
) -> None:
    """
    When lead_lag_score < config.signal.lead_lag_min_gate (0.40), score() must
    raise SignalDroppedError. Caller is responsible for logging to signal_outcomes.
    """
    import json

    trade = make_qualified_trade()
    wallet_data = make_wallet_data()

    from meg.core.events import RedisKeys
    await mock_redis.set(
        RedisKeys.wallet_data(trade.wallet_address), json.dumps(wallet_data)
    )

    with (
        patch("meg.signal_engine.composite_scorer.lead_lag_scorer") as mock_ll,
        patch("meg.signal_engine.composite_scorer.conviction_ratio") as mock_cr,
        patch("meg.signal_engine.composite_scorer.kelly_sizer") as mock_ks,
        patch("meg.signal_engine.composite_scorer.consensus_filter") as mock_cf,
        patch("meg.signal_engine.composite_scorer.contrarian_detector") as mock_cd,
        patch("meg.signal_engine.composite_scorer.ladder_detector") as mock_ld,
        patch("meg.signal_engine.composite_scorer.archetype_weighter") as mock_aw,
    ):
        mock_ll.score = AsyncMock(return_value=0.25)  # below lead_lag_min_gate=0.40
        mock_cr.score = AsyncMock(return_value=0.60)
        mock_ks.compute_size = AsyncMock(return_value=150.0)
        mock_cf.score = AsyncMock(return_value=0.70)
        mock_cd.score = AsyncMock(return_value=0.60)
        mock_ld.multiplier = AsyncMock(return_value=1.0)
        mock_aw.weight = lambda archetype, config: 1.0

        from meg.signal_engine.composite_scorer import score
        with pytest.raises(SignalDroppedError) as exc_info:
            await score(trade, mock_redis, db_session, test_config)

    assert exc_info.value.score < test_config.signal.lead_lag_min_gate


@_OPUS_XFAIL
async def test_missing_wallet_data_raises_signal_dropped_error(
    mock_redis, db_session, test_config: MegConfig
) -> None:
    """
    When wallet_data is not in Redis (cache miss), score() must raise
    SignalDroppedError with reason="wallet_data_miss" rather than crashing.
    """
    trade = make_qualified_trade()
    # Do NOT write wallet data to Redis — simulating a cache miss

    from meg.signal_engine.composite_scorer import score
    with pytest.raises(SignalDroppedError) as exc_info:
        await score(trade, mock_redis, db_session, test_config)

    assert "wallet_data" in exc_info.value.reason.lower()
