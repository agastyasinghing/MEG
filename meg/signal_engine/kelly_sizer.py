"""
Kelly criterion position sizer.

Computes the optimal fraction of portfolio to bet on a signal using the
Kelly criterion, scaled by config.kelly.fraction (default 0.25 = quarter Kelly)
for conservative sizing. Output is capped at config.kelly.max_bet_usdc.

Formula: f* = (p * b - q) / b
  p = estimated probability of winning (win_prob)
  q = 1 - p
  b = net odds = (1 - entry_price) / entry_price  (binary prediction market)

On a binary market priced at entry_price = 0.40:
  b = 0.60 / 0.40 = 1.5 (win $1.50 per $1 risked)

NOTE: Implement with Opus + ultrathink. This directly determines trade size.
"""
from __future__ import annotations

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade


def compute_size(
    trade: QualifiedWhaleTrade,
    win_prob: float,
    entry_price: float,
    portfolio_value_usdc: float,
    config: MegConfig,
) -> float:
    """
    Return the recommended position size in USDC for this signal.

    win_prob: model's estimated probability the outcome resolves correctly (0.0–1.0).
    entry_price: limit price to enter the position (0.0–1.0, binary market price).
    portfolio_value_usdc: current portfolio value (from config.kelly.portfolio_value_usdc
      or live balance when available).

    Applies Kelly fraction (config.kelly.fraction) and hard cap (config.kelly.max_bet_usdc).
    Returns 0.0 if Kelly formula yields a negative or zero bet (no positive edge).
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
