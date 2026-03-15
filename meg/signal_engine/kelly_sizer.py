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

PRD reference: §9.3.5 Kelly Position Sizer
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
    portfolio_value_usdc: current portfolio value.

    Applies Kelly fraction (config.kelly.fraction) and hard cap (config.kelly.max_bet_usdc).
    Returns 0.0 if Kelly formula yields a negative or zero bet (no positive edge).
    """
    if entry_price <= 0.0 or entry_price >= 1.0:
        return 0.0

    payout_odds = (1.0 - entry_price) / entry_price
    f_star = _kelly_fraction(win_prob, payout_odds)

    if f_star <= 0.0:
        return 0.0

    scaled_fraction = f_star * config.kelly.fraction
    size = scaled_fraction * portfolio_value_usdc

    return min(size, config.kelly.max_bet_usdc)


def _kelly_fraction(
    win_probability: float,
    payout_odds: float,
) -> float:
    """
    Compute raw Kelly fraction f* = (p*b - q) / b.
    Returns 0.0 if result is negative (no edge — do not bet).
    """
    p = win_probability
    q = 1.0 - p
    b = payout_odds

    if b <= 0.0:
        return 0.0

    f_star = (p * b - q) / b

    return max(0.0, f_star)
