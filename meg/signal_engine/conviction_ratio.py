"""
Conviction ratio scorer.

Measures the trade size as a fraction of the whale's total wallet capital.
A whale betting 40% of their portfolio on an outcome is expressing far more
conviction than one betting 1%. High conviction ratio = stronger signal weight.

NOTE: Implement with Opus + ultrathink. Sizing errors = real money lost.
"""
from __future__ import annotations

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade


async def score(
    trade: QualifiedWhaleTrade,
    wallet_data: dict,
    config: MegConfig,
) -> float:
    """
    Return a conviction score in [0.0, 1.0].
    Computed as: min(trade.size_usdc / wallet_capital, 1.0).

    wallet_data: pre-fetched wallet dict from wallet_registry.
      Expected key: total_capital_usdc (float | None). Falls back to
      total_volume_usdc as a proxy when total_capital_usdc is None.
    """
    capital = get_wallet_capital(wallet_data)
    return min(trade.size_usdc / capital, 1.0)


def get_wallet_capital(wallet_data: dict) -> float:
    """
    Extract wallet capital in USDC from pre-fetched wallet_data dict.
    Prefers total_capital_usdc (refreshed from Polygon USDC balance).
    Falls back to total_volume_usdc as a proxy when capital is unknown.
    Returns 1.0 as a safe fallback to avoid division by zero.
    """
    capital = wallet_data.get("total_capital_usdc")
    if capital is not None and capital > 0:
        return float(capital)

    volume = wallet_data.get("total_volume_usdc", 0.0)
    if volume and float(volume) > 0:
        return float(volume)

    return 1.0
