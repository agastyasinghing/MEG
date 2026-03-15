"""
Composite scorer.

Combines all signal engine module scores into a single composite score in
[0.0, 1.0]. This is the final gate before a signal reaches agent_core.
Signals below config.signal.composite_score_threshold are marked FILTERED
and logged to signal_outcomes (the training data moat) but never executed.

PRD §9.3.9 composite score formula:

  Step 1 — weighted base (4 components, weights from config.signal.composite_weights):
    base = lead_lag * w_lead_lag          # 0.35 — is this whale actually early?
         + consensus * w_consensus        # 0.30 — do other quality whales agree?
         + kelly_score * w_kelly          # 0.20 — positive expected value?
         + divergence * w_divergence      # 0.15 — against order flow?

  Step 2 — archetype + ladder multipliers:
    adjusted = base * archetype_mult * ladder_mult
      archetype_mult: 1.0 (INFORMATION), 0.65 (MOMENTUM), 0.0 (ARBITRAGE/MANIPULATOR)
      ladder_mult:    [1.0, 2.0] — each rung adds config.signal.ladder_conviction_per_rung

  Step 3 — conviction ratio blend:
    final = adjusted * 0.85 + conviction_ratio * 0.15

  Step 4 — lead-lag gate (SignalDroppedError):
    If lead_lag_score < config.signal.lead_lag_min_gate (default 0.40),
    raise SignalDroppedError BEFORE computing other components. A whale with
    weak predictive history produces no signal regardless of consensus or size.

Scoring is concurrent: all modules called with asyncio.gather() in step 1.
Lead-lag gate is checked first (sequential) to abort early if the wallet
has no demonstrated predictive edge.

Wallet data is fetched ONCE in score() and passed to all sub-scorers that
need it (lead_lag_scorer, conviction_ratio) — avoids N DB lookups per signal.

NOTE: Implement with Opus + ultrathink. Weight calibration directly determines
which signals get executed. This is the most financially consequential module.
"""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade, SignalDroppedError, SignalEvent
from meg.signal_engine import (  # noqa: F401  # imported for patch() in tests
    archetype_weighter,
    consensus_filter,
    contrarian_detector,
    conviction_ratio,
    kelly_sizer,
    ladder_detector,
    lead_lag_scorer,
)


async def score(
    trade: QualifiedWhaleTrade,
    redis: Redis,
    session: AsyncSession,
    config: MegConfig,
) -> SignalEvent:
    """
    Run all scoring modules and combine into a SignalEvent.

    Raises SignalDroppedError if lead_lag_score < config.signal.lead_lag_min_gate —
    caller must catch this and log the dropped signal to signal_outcomes with
    status=FILTERED and score=0.0.

    Sets status=FILTERED if composite_score < config.signal.composite_score_threshold.
    Sets status=PENDING if composite_score >= threshold.
    Always logs the result to signal_outcomes regardless of status.
    """
    raise NotImplementedError("composite_scorer.score")


async def _gather_component_scores(
    trade: QualifiedWhaleTrade,
    wallet_data: dict,
    redis: Redis,
    session: AsyncSession,
    config: MegConfig,
) -> dict[str, float]:
    """
    Run all scoring modules concurrently and return a dict of component scores.
    Keys: lead_lag, conviction, consensus, contrarian, kelly, archetype_mult, ladder_mult.

    wallet_data: pre-fetched wallet dict from wallet_registry — passed to lead_lag_scorer
    and conviction_ratio to avoid redundant DB lookups per scoring cycle.

    Lead-lag gate: if lead_lag_score < config.signal.lead_lag_min_gate, raises
    SignalDroppedError immediately. All other components are still computed concurrently
    first; the gate check happens after asyncio.gather() returns.
    """
    raise NotImplementedError("composite_scorer._gather_component_scores")


def _combine_scores(
    components: dict[str, float],
    config: MegConfig,
) -> float:
    """
    Apply PRD §9.3.9 formula to component scores and return the composite in [0.0, 1.0].

    components dict keys: lead_lag, consensus, kelly, contrarian (divergence),
      conviction, archetype_mult, ladder_mult.
    Weights are read from config.signal.composite_weights (hot-reloadable).
    """
    w = config.signal.composite_weights

    # Step 1: weighted base across 4 informational components
    base = (
        components["lead_lag"] * w.lead_lag
        + components["consensus"] * w.consensus
        + components["kelly"] * w.kelly
        + components["contrarian"] * w.divergence  # contrarian = divergence signal
    )

    # Step 2: apply archetype and ladder conviction multipliers
    adjusted = base * components["archetype_mult"] * components["ladder_mult"]

    # Step 3: blend with conviction ratio (conviction survives even at zero adjusted)
    final = adjusted * 0.85 + components["conviction"] * 0.15

    return max(0.0, min(1.0, final))
