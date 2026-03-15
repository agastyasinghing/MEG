"""
Tests for meg/signal_engine/signal_decay.py

⚠️  OPUS SPEC — module stubs raise NotImplementedError.
Implement signal_decay.apply_decay(), is_expired(), set_signal_ttl() with Opus.

Key implementation constraints:
  - apply_decay() uses exponential decay: score * (0.5 ** (age_s / half_life_s))
    Equivalently: score * exp(-age_s * ln(2) / half_life_s)
  - Returns 0.0 when decayed score < config.signal_decay.min_score_after_decay
  - Returns 0.0 when signal_age_seconds < 0 (guard: clock skew)
  - is_expired() checks both: (1) TTL elapsed and (2) decayed score < threshold
  - set_signal_ttl() writes expiry to Redis at RedisKeys.signal_ttl(signal_id)
  - TTL formula: half_life * config.signal.ttl_half_life_multiplier (default 3.0)
    → 3 half-lives = signal retains 12.5% of original score at expiry
  - TTL is never shorter than config.signal.min_half_life_minutes * 60 * multiplier

v1: all signals use uniform half_life_seconds (config.signal_decay.half_life_seconds).
v1.5: per-signal-type baselines (see TODOS.md and signal_decay.py docstring).

Default config values (from config.yaml):
  signal_decay.half_life_seconds: 3600  (1 hour)
  signal_decay.min_score_after_decay: 0.20
  signal.ttl_half_life_multiplier: 3.0  (TTL = 3 * half_life = 3 hours)
  signal.min_half_life_minutes: 5.0

PRD reference: §9.3.10 Signal Decay Timer
"""
from __future__ import annotations

import time

import pytest

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, SignalEvent, SignalScores
from meg.signal_engine.signal_decay import apply_decay, is_expired, set_signal_ttl

pytestmark = pytest.mark.xfail(
    reason="OPUS SPEC: signal_decay stubs raise NotImplementedError",
    strict=False,
)


# ── Helpers ───────────────────────────────────────────────────────────────────


def make_signal_event(
    *,
    signal_id: str = "sig_001",
    composite_score: float = 0.80,
    status: str = "PENDING",
) -> SignalEvent:
    return SignalEvent(
        signal_id=signal_id,
        market_id="market_001",
        outcome="YES",
        composite_score=composite_score,
        scores=SignalScores(
            lead_lag=0.75,
            consensus=0.60,
            kelly_confidence=0.55,
            divergence=0.70,
            conviction_ratio=0.40,
            archetype_multiplier=1.0,
            ladder_multiplier=1.0,
        ),
        recommended_size_usdc=200.0,
        kelly_fraction=0.083,
        ttl_expires_at_ms=int(time.time() * 1000) + 10_800_000,  # 3h from now
        status=status,
        triggering_wallet="0xWHALE001",
        market_price_at_signal=0.60,
    )


# ── apply_decay() ─────────────────────────────────────────────────────────────


def test_zero_age_no_decay(test_config: MegConfig) -> None:
    """A brand-new signal (age=0) should retain its full score."""
    result = apply_decay(0.80, signal_age_seconds=0.0, config=test_config)
    assert result == pytest.approx(0.80)


def test_half_life_halves_score(test_config: MegConfig) -> None:
    """After exactly half_life_seconds, score should be halved."""
    half_life = test_config.signal_decay.half_life_seconds  # default 3600
    result = apply_decay(0.80, signal_age_seconds=float(half_life), config=test_config)
    assert result == pytest.approx(0.40, rel=0.01)


def test_two_half_lives_quarters_score(test_config: MegConfig) -> None:
    """After 2 half-lives, score is reduced to 1/4 of original."""
    half_life = test_config.signal_decay.half_life_seconds
    result = apply_decay(0.80, signal_age_seconds=float(half_life * 2), config=test_config)
    assert result == pytest.approx(0.20, rel=0.01)


def test_below_min_threshold_returns_zero(test_config: MegConfig) -> None:
    """
    When decayed score falls below min_score_after_decay (default 0.20),
    apply_decay must return 0.0 — signal is expired.
    After 2 half-lives: 0.80 → 0.20 = exactly at threshold (boundary).
    After 3 half-lives: 0.80 → 0.10 < 0.20 → 0.0.
    """
    half_life = test_config.signal_decay.half_life_seconds
    result = apply_decay(0.80, signal_age_seconds=float(half_life * 3), config=test_config)
    assert result == pytest.approx(0.0)


def test_monotonically_decreasing(test_config: MegConfig) -> None:
    """Decayed score must always decrease (or stay equal) as age increases."""
    ages = [0, 900, 1800, 3600, 7200, 10800]
    scores = [apply_decay(0.80, float(age), test_config) for age in ages]
    for i in range(len(scores) - 1):
        assert scores[i] >= scores[i + 1]


def test_already_low_score_expires_faster(test_config: MegConfig) -> None:
    """
    A signal at 0.25 hits the 0.20 min threshold before a signal at 0.80.
    Lower starting scores expire (return 0.0) after fewer half-lives.
    """
    half_life = test_config.signal_decay.half_life_seconds
    high_score_result = apply_decay(0.80, float(half_life), test_config)
    low_score_result = apply_decay(0.25, float(half_life), test_config)

    # Low score after 1 half-life: 0.25 * 0.5 = 0.125 < 0.20 → returns 0.0
    assert high_score_result > 0.0
    assert low_score_result == pytest.approx(0.0)


# ── is_expired() ─────────────────────────────────────────────────────────────


async def test_fresh_signal_not_expired(test_config: MegConfig) -> None:
    """A signal with TTL 3 hours in the future and high score is not expired."""
    signal = make_signal_event()  # ttl_expires_at_ms = now + 3h
    result = await is_expired(signal, test_config)
    assert result is False


async def test_signal_past_ttl_is_expired(test_config: MegConfig) -> None:
    """A signal whose TTL has elapsed must be marked expired regardless of score."""
    signal = make_signal_event()
    # Override TTL to be in the past
    signal = signal.model_copy(update={"ttl_expires_at_ms": int(time.time() * 1000) - 1})
    result = await is_expired(signal, test_config)
    assert result is True


# ── set_signal_ttl() ──────────────────────────────────────────────────────────


async def test_set_signal_ttl_writes_to_redis(mock_redis, test_config: MegConfig) -> None:
    """
    After set_signal_ttl(), the signal's expiry should be readable from Redis
    at RedisKeys.signal_ttl(signal_id).
    """
    signal = make_signal_event(signal_id="sig_ttl_test")
    await set_signal_ttl(signal, mock_redis, test_config)

    ttl_key = RedisKeys.signal_ttl("sig_ttl_test")
    value = await mock_redis.get(ttl_key)
    assert value is not None
    assert int(value) > int(time.time() * 1000)  # TTL is in the future


async def test_set_signal_ttl_is_at_least_min_half_life(
    mock_redis, test_config: MegConfig
) -> None:
    """
    TTL must never be shorter than min_half_life_minutes * ttl_half_life_multiplier.
    Default: 5 min * 3.0 = 15 minutes minimum TTL from now.
    """
    signal = make_signal_event(signal_id="sig_min_ttl")
    await set_signal_ttl(signal, mock_redis, test_config)

    ttl_key = RedisKeys.signal_ttl("sig_min_ttl")
    value = await mock_redis.get(ttl_key)
    ttl_ms = int(value)
    now_ms = int(time.time() * 1000)
    min_ttl_ms = int(
        test_config.signal.min_half_life_minutes
        * 60
        * 1000
        * test_config.signal.ttl_half_life_multiplier
    )
    assert ttl_ms - now_ms >= min_ttl_ms - 1000  # allow 1s clock tolerance
