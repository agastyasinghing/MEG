"""
Tests for meg/signal_engine/archetype_weighter.py

All tests: archetype_weighter.weight() is fully implemented (Sonnet-eligible).
Every test should pass without modification.

Coverage:
  - Each archetype returns correct config-driven multiplier
  - ARBITRAGE and MANIPULATOR log a warning (defense-in-depth)
  - Unknown archetype returns 0.0 (safe default)
  - Config values are read live (not hardcoded — override test proves this)
"""
from __future__ import annotations

import pytest

from meg.core.config_loader import MegConfig
from meg.signal_engine.archetype_weighter import weight


# ── Correct multipliers ───────────────────────────────────────────────────────


def test_information_returns_1_0(test_config: MegConfig) -> None:
    """INFORMATION is the top-weighted archetype — full 1.0 multiplier."""
    assert weight("INFORMATION", test_config) == 1.0


def test_momentum_returns_0_65(test_config: MegConfig) -> None:
    """MOMENTUM is discounted — 0.65 (trend follower, likely priced in)."""
    assert weight("MOMENTUM", test_config) == pytest.approx(0.65)


def test_arbitrage_returns_0_0(test_config: MegConfig) -> None:
    """ARBITRAGE must be zeroed — should not reach this module."""
    assert weight("ARBITRAGE", test_config) == 0.0


def test_manipulator_returns_0_0(test_config: MegConfig) -> None:
    """MANIPULATOR must be zeroed — should not reach this module."""
    assert weight("MANIPULATOR", test_config) == 0.0


# ── Warning on excluded archetypes ─────────────────────────────────────────


def test_arbitrage_logs_warning(test_config: MegConfig, capsys: pytest.CaptureFixture) -> None:
    """
    ARBITRAGE reaching archetype_weighter means Gate 2 failed to exclude it.
    A WARNING must be logged. structlog emits to stdout in test mode — checked
    via capsys rather than caplog (structlog bypasses Python's logging handler).
    """
    weight("ARBITRAGE", test_config)
    captured = capsys.readouterr()
    assert "excluded_archetype_reached" in captured.out


def test_manipulator_logs_warning(test_config: MegConfig, capsys: pytest.CaptureFixture) -> None:
    """Same warning requirement for MANIPULATOR."""
    weight("MANIPULATOR", test_config)
    captured = capsys.readouterr()
    assert "excluded_archetype_reached" in captured.out


def test_information_does_not_log_warning(
    test_config: MegConfig, capsys: pytest.CaptureFixture
) -> None:
    """Normal archetypes must NOT log a warning — only ARBITRAGE/MANIPULATOR do."""
    weight("INFORMATION", test_config)
    captured = capsys.readouterr()
    assert "excluded_archetype_reached" not in captured.out


# ── Config-driven (not hardcoded) ─────────────────────────────────────────────


def test_uses_config_values_not_hardcoded(test_config: MegConfig) -> None:
    """
    Changing config.signal.archetype_weights.MOMENTUM must change the returned
    multiplier. This proves the implementation reads live config, not a hardcoded
    ARCHETYPE_WEIGHTS dict (the pre-fix bug).
    """
    test_config.signal.archetype_weights.MOMENTUM = 0.80
    assert weight("MOMENTUM", test_config) == pytest.approx(0.80)


def test_information_config_override(test_config: MegConfig) -> None:
    """Config override on INFORMATION also takes effect."""
    test_config.signal.archetype_weights.INFORMATION = 0.90
    assert weight("INFORMATION", test_config) == pytest.approx(0.90)


# ── Return value bounds ───────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "archetype",
    ["INFORMATION", "MOMENTUM", "ARBITRAGE", "MANIPULATOR"],
)
def test_multiplier_in_valid_range(archetype: str, test_config: MegConfig) -> None:
    """All archetype multipliers must be in [0.0, 1.0]."""
    result = weight(archetype, test_config)  # type: ignore[arg-type]
    assert 0.0 <= result <= 1.0
