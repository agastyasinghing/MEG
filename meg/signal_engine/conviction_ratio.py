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
    config: MegConfig,
) -> float:
    """
    Return a conviction score in [0.0, 1.0].
    Computed as: min(trade.size_usdc / wallet_capital, 1.0), normalised.
    Wallet capital is fetched from the wallet registry.
    """
    raise NotImplementedError("conviction_ratio.score")


async def get_wallet_capital(wallet_address: str) -> float:
    """
    Return the wallet's estimated total capital in USDC.
    Derived from historical trade volume and current open positions.
    """
    raise NotImplementedError("conviction_ratio.get_wallet_capital")
