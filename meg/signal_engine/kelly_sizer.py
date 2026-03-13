"""
Kelly criterion position sizer.

Computes the optimal fraction of portfolio to bet on a signal using the
Kelly criterion, scaled by config.kelly.fraction (default 0.25 = quarter Kelly)
for conservative sizing. Output is capped at config.kelly.max_bet_usdc.

Formula: f* = (p * b - q) / b
  p = estimated probability of winning
  q = 1 - p
  b = net odds (payout per unit risked)

NOTE: Implement with Opus + ultrathink. This directly determines trade size.
"""
from __future__ import annotations

from meg.core.config_loader import MegConfig
from meg.core.events import SignalEvent


def compute_size(
    signal: SignalEvent,
    portfolio_value_usdc: float,
    config: MegConfig,
) -> float:
    """
    Return the recommended position size in USDC for this signal.
    Applies Kelly fraction (config.kelly.fraction) and hard cap (config.kelly.max_bet_usdc).
    Returns 0.0 if Kelly formula yields a negative or zero bet (no edge).
    """
    raise NotImplementedError("kelly_sizer.compute_size")


def _kelly_fraction(
    win_probability: float,
    payout_odds: float,
) -> float:
    """
    Compute raw Kelly fraction f* = (p*b - q) / b.
    Returns 0.0 if result is negative (no edge — do not bet).
    """
    raise NotImplementedError("kelly_sizer._kelly_fraction")
