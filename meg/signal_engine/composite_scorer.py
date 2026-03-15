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
    raise SignalDroppedError. A whale with weak predictive history produces
    no signal regardless of consensus or size.

Scoring is concurrent: all modules called with asyncio.gather(). The
lead-lag gate is checked AFTER gather returns — all components are computed
concurrently first, then the gate aborts if the lead-lag score is too low.

Wallet data is fetched ONCE in score() and passed to all sub-scorers that
need it (lead_lag_scorer, conviction_ratio) — avoids N DB lookups per signal.
"""
from __future__ import annotations

import asyncio
import inspect
import time
import uuid

import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import (
    QualifiedWhaleTrade,
    RedisKeys,
    SignalDroppedError,
    SignalEvent,
    SignalScores,
)
from meg.signal_engine import (  # noqa: F401  # imported for patch() in tests
    archetype_weighter,
    consensus_filter,
    contrarian_detector,
    conviction_ratio,
    kelly_sizer,
    ladder_detector,
    lead_lag_scorer,
)

logger = structlog.get_logger(__name__)


async def _maybe_await(value):
    """Await a value if it's a coroutine/awaitable, otherwise return directly."""
    if inspect.isawaitable(value):
        return await value
    return value


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
    import json

    # Pre-fetch wallet data ONCE from Redis
    raw_wallet = await redis.get(RedisKeys.wallet_data(trade.wallet_address))
    if raw_wallet is None:
        raise SignalDroppedError(reason="wallet_data_miss", score=0.0)

    wallet_data = json.loads(raw_wallet)

    # Gather all component scores (may raise SignalDroppedError for lead_lag gate)
    components = await _gather_component_scores(
        trade, wallet_data, redis, session, config
    )

    composite = _combine_scores(components, config)

    status = (
        "PENDING"
        if composite >= config.signal.composite_score_threshold
        else "FILTERED"
    )

    is_contrarian = components["contrarian"] > config.signal.contrarian_threshold

    # Compute TTL
    half_life_s = float(config.signal_decay.half_life_seconds)
    min_half_life_s = config.signal.min_half_life_minutes * 60.0
    effective_half_life = max(half_life_s, min_half_life_s)
    ttl_seconds = effective_half_life * config.signal.ttl_half_life_multiplier
    now_ms = int(time.time() * 1000)
    ttl_expires_at_ms = now_ms + int(ttl_seconds * 1000)

    kelly_raw = components.get("_kelly_raw_usdc", 0.0)
    portfolio_value = config.kelly.portfolio_value_usdc
    kelly_frac = kelly_raw / portfolio_value if portfolio_value > 0 else 0.0

    signal = SignalEvent(
        signal_id=str(uuid.uuid4()),
        market_id=trade.market_id,
        outcome=trade.outcome,
        composite_score=composite,
        scores=SignalScores(
            lead_lag=components["lead_lag"],
            consensus=components["consensus"],
            kelly_confidence=components["kelly"],
            divergence=components["contrarian"],
            conviction_ratio=components["conviction"],
            archetype_multiplier=components["archetype_mult"],
            ladder_multiplier=components["ladder_mult"],
        ),
        recommended_size_usdc=kelly_raw,
        kelly_fraction=kelly_frac,
        ttl_expires_at_ms=ttl_expires_at_ms,
        status=status,
        triggering_wallet=trade.wallet_address,
        market_price_at_signal=trade.market_price_at_trade,
        is_contrarian=is_contrarian,
        is_ladder=trade.intent == "SIGNAL_LADDER",
        whale_archetype=trade.archetype,
        market_category=trade.market_category,
        intent=trade.intent,
    )

    logger.info(
        "composite_scorer.scored",
        signal_id=signal.signal_id,
        composite_score=composite,
        status=status,
        wallet=trade.wallet_address,
        market_id=trade.market_id,
    )

    return signal


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
    win_prob = float(wallet_data.get("win_rate", 0.5))
    entry_price = trade.market_price_at_trade
    portfolio_value = config.kelly.portfolio_value_usdc

    # Run all scorers concurrently. Sync calls are wrapped for mock compatibility.
    ll, cr, ks_raw, cf, cd, ld, aw = await asyncio.gather(
        lead_lag_scorer.score(trade, wallet_data, config),
        conviction_ratio.score(trade, wallet_data, config),
        _maybe_await(
            kelly_sizer.compute_size(
                trade, win_prob, entry_price, portfolio_value, config
            )
        ),
        consensus_filter.score(trade, redis, config),
        contrarian_detector.score(trade, redis, config),
        ladder_detector.multiplier(trade, session, config),
        _maybe_await(archetype_weighter.weight(trade.archetype, config)),
    )

    # Lead-lag gate: checked AFTER gather (all components computed concurrently)
    if ll < config.signal.lead_lag_min_gate:
        raise SignalDroppedError(reason="lead_lag_below_gate", score=ll)

    # Normalise kelly to [0, 1] confidence score
    kelly_confidence = (
        min(ks_raw / config.kelly.max_bet_usdc, 1.0) if ks_raw > 0 else 0.0
    )

    return {
        "lead_lag": ll,
        "conviction": cr,
        "kelly": kelly_confidence,
        "consensus": cf,
        "contrarian": cd,
        "archetype_mult": aw,
        "ladder_mult": ld,
        "_kelly_raw_usdc": ks_raw,
    }


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
