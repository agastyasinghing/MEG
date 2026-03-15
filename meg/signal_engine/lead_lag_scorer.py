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
    wallet_data: dict,
    config: MegConfig,
) -> float:
    """
    Return a lead-lag score in [0.0, 1.0] for this whale trade.
    1.0 = consistently leads price moves (strong information signal).
    0.0 = consistently lags (follows crowd, no edge).
    Applies reputation decay based on recency of the wallet's track record.

    wallet_data: pre-fetched wallet dict from wallet_registry (keyed by field name).
      Expected keys: avg_lead_time_hours, last_profitable_trade_at (ISO string | None),
      reputation_decay_factor, composite_whale_score.
    """
    raise NotImplementedError("lead_lag_scorer.score")


async def compute_reputation_decay(
    wallet_data: dict,
    config: MegConfig,
) -> float:
    """
    Compute reputation decay multiplier from pre-fetched wallet data.
    Returns a multiplier in (0.0, 1.0] that scales the raw lead-lag score.
    Decay increases with time since last profitable trade.

    Formula: decay_factor = exp(-days_since_last_good_trade / tau)
    tau = config.reputation.decay_tau_days (default 30)
    Returns 1.0 (no decay) when wallet_data["last_profitable_trade_at"] is None.
    """
    raise NotImplementedError("lead_lag_scorer.compute_reputation_decay")
