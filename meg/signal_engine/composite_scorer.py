"""
Composite scorer.

Combines all signal engine module scores into a single composite score in
[0.0, 1.0]. This is the final gate before a signal reaches agent_core.
Signals below config.signal.composite_score_threshold are marked FILTERED
and logged to signal_outcomes (the training data moat) but never executed.

Score composition:
  composite = (
      lead_lag       * w_lead_lag       +   # primary: is this whale actually early?
      conviction     * w_conviction     +   # how much of their stack is on this?
      consensus      * w_consensus      +   # are other quality whales agreeing?
      contrarian     * w_contrarian     +   # against order flow? (can be negative)
      ladder         * w_ladder             # building a ladder? (escalating conviction)
  ) * archetype_weight                      # multiplier by archetype

  Weights are hot-configurable. Default weights are defined in config.yaml.

NOTE: Implement with Opus + ultrathink. Weight calibration directly determines
which signals get executed. This is the most financially consequential module.
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade, SignalEvent


async def score(
    trade: QualifiedWhaleTrade,
    redis: Redis,
    config: MegConfig,
) -> SignalEvent:
    """
    Run all scoring modules and combine into a SignalEvent.
    Sets status=FILTERED if composite_score < threshold.
    Sets status=PENDING if composite_score >= threshold.
    Always logs the result to signal_outcomes regardless of status.
    """
    raise NotImplementedError("composite_scorer.score")


async def _gather_component_scores(
    trade: QualifiedWhaleTrade,
    redis: Redis,
    config: MegConfig,
) -> dict[str, float]:
    """
    Run all scoring modules concurrently and return a dict of component scores.
    Keys: lead_lag, conviction, consensus, contrarian, ladder, archetype_weight.
    """
    raise NotImplementedError("composite_scorer._gather_component_scores")


def _combine_scores(
    components: dict[str, float],
    config: MegConfig,
) -> float:
    """
    Apply weights to component scores and return the composite in [0.0, 1.0].
    Weights are read from config (hot-reloadable).
    """
    raise NotImplementedError("composite_scorer._combine_scores")
