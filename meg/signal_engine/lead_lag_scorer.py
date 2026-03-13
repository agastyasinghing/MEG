"""
Lead-lag scorer with reputation decay.

Measures how consistently a whale enters positions BEFORE price moves in the
predicted direction (lead) vs. after the crowd has already moved (lag).
High lead-lag score = whale has genuine information edge. Decays over time
as the whale's recent trades lose predictive power.

NOTE: Implement with Opus + ultrathink. Scoring errors = real money lost.
"""
from __future__ import annotations

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade


async def score(
    trade: QualifiedWhaleTrade,
    config: MegConfig,
) -> float:
    """
    Return a lead-lag score in [0.0, 1.0] for this whale trade.
    1.0 = consistently leads price moves (strong information signal).
    0.0 = consistently lags (follows crowd, no edge).
    Applies reputation decay based on recency of the wallet's track record.
    """
    raise NotImplementedError("lead_lag_scorer.score")


async def compute_reputation_decay(
    wallet_address: str,
    config: MegConfig,
) -> float:
    """
    Compute and apply reputation decay multiplier for the wallet.
    Returns a multiplier in (0.0, 1.0] that scales the raw lead-lag score.
    Decay increases with time since last profitable trade.
    """
    raise NotImplementedError("lead_lag_scorer.compute_reputation_decay")
