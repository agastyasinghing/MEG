"""
Lead-lag scorer with reputation decay.

Measures how consistently a whale enters positions BEFORE price moves in the
predicted direction (lead) vs. after the crowd has already moved (lag).
High lead-lag score = whale has genuine information edge. Decays over time
as the whale's recent trades lose predictive power.

Formula:
  raw_score = lead_factor * win_rate
  lead_factor = 1 - exp(-avg_lead_time_hours / REFERENCE_HOURS)
  final_score = clamp(raw_score * decay_factor, 0.0, 1.0)

Decay formula (PRD §9.3.2):
  decay_factor = exp(-days_since_last_good_trade / tau)
  tau = config.reputation.decay_tau_days (default 30)
  None last_profitable_trade_at → 1.0 (no penalty)
"""
from __future__ import annotations

import math
from datetime import datetime, timezone

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade

# Reference time constant for lead-time saturation curve.
# At 6 hours, lead_factor ≈ 0.63 (1 - 1/e). Whales consistently
# entering 12+ hours early saturate near 0.86.
_REFERENCE_HOURS: float = 6.0


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
      Expected keys: avg_lead_time_hours, win_rate, last_profitable_trade_at
      (ISO string | None).
    """
    avg_lead_time = float(wallet_data.get("avg_lead_time_hours", 0.0))
    win_rate = float(wallet_data.get("win_rate", 0.0))

    # Saturating lead-time factor: higher avg_lead_time → closer to 1.0
    lead_factor = 1.0 - math.exp(-avg_lead_time / _REFERENCE_HOURS)

    raw_score = lead_factor * win_rate

    decay_factor = await compute_reputation_decay(wallet_data, config)

    return max(0.0, min(1.0, raw_score * decay_factor))


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
    last_profitable = wallet_data.get("last_profitable_trade_at")
    if last_profitable is None:
        return 1.0

    last_dt = datetime.fromisoformat(last_profitable)
    now = datetime.now(tz=timezone.utc)
    days_since = (now - last_dt).total_seconds() / 86400.0

    if days_since <= 0:
        return 1.0

    tau = config.reputation.decay_tau_days
    return math.exp(-days_since / tau)
