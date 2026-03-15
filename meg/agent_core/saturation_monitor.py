"""
Market saturation monitor — simplified v1 formula (PRD §9.4.3 adapted).

v1 uses available data (no 30-day baselines — see TODOS.md):
  Signal 1: Directional price drift since whale entry (weight 0.60)
  Signal 2: Liquidity thinning vs quality floor       (weight 0.40)

Full PRD formula (v1.5 upgrade when baselines exist):
  Signal 1: Price velocity spike vs 30-day avg        (weight 0.40)
  Signal 2: Order book thinning vs baseline depth      (weight 0.35)
  Signal 3: Trade frequency spike vs 30-day avg        (weight 0.25)

Saturation does NOT block — it reduces position size:
  score <= threshold  →  size_multiplier = 1.0  (no reduction)
  score >  threshold  →  size_multiplier = clamp(1 - (s-t)*sens, 0.25, 1.0)

Size reduction curve (default threshold=0.60, sensitivity=2.0):
  score 0.60 → multiplier 1.00 (no reduction)
  score 0.70 → multiplier 0.80 (20% reduction)
  score 0.80 → multiplier 0.60 (40% reduction)
  score 0.90 → multiplier 0.40 (60% reduction)
  score 1.00 → multiplier 0.25 (75% reduction — floor)
"""
from __future__ import annotations

import structlog
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, SignalEvent

logger = structlog.get_logger(__name__)

# v1 constant: 10% price drift in signal direction = maximum saturation score.
# Not in config because it's an internal normalization constant, not an operator knob.
_DRIFT_MAX_PCT = 0.10


async def score(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
) -> tuple[float, float]:
    """
    Return (saturation_score, size_multiplier).

    saturation_score: [0.0, 1.0] — how saturated the market is.
    size_multiplier:  [0.25, 1.0] — factor to apply to position size.

    Returns (0.0, 1.0) when market data is unavailable — fail open.
    """
    # Read current market price
    mid_raw = await redis.get(RedisKeys.market_mid_price(signal.market_id))
    if mid_raw is None:
        # No price data — cannot assess saturation. Fail open.
        return 0.0, 1.0

    current_mid = float(mid_raw)
    signal_price = signal.market_price_at_signal

    if signal_price <= 0:
        return 0.0, 1.0

    # ── Signal 1: Directional price drift (weight 0.60) ──────────────────
    # Drift in the signal's direction = copy traders have already entered.
    # Drift against the signal = opportunity (no saturation).
    if signal.outcome == "YES":
        directional_drift = (current_mid - signal_price) / signal_price
    else:
        # For NO outcome, price moving DOWN from signal price = favorable
        directional_drift = (signal_price - current_mid) / signal_price

    # Only positive drift (in signal direction) counts as saturation
    directional_drift = max(directional_drift, 0.0)
    drift_score = _clamp(directional_drift / _DRIFT_MAX_PCT, 0.0, 1.0)

    # ── Signal 2: Liquidity thinning (weight 0.40) ───────────────────────
    # Compare current liquidity to twice the quality floor.
    # Below floor = severely thinned (score 1.0).
    # Above 2x floor = healthy (score 0.0).
    liquidity_raw = await redis.get(
        RedisKeys.market_liquidity(signal.market_id)
    )
    if liquidity_raw is not None:
        current_liquidity = float(liquidity_raw)
        baseline = config.pre_filter.min_market_liquidity_usdc * 2
        if baseline > 0:
            liquidity_ratio = current_liquidity / baseline
            thinning_score = _clamp(1.0 - liquidity_ratio, 0.0, 1.0)
        else:
            thinning_score = 0.0
    else:
        # No liquidity data — assume maximum thinning (conservative).
        thinning_score = 1.0

    # ── Composite score ──────────────────────────────────────────────────
    saturation_score = drift_score * 0.60 + thinning_score * 0.40

    # ── Size multiplier ──────────────────────────────────────────────────
    threshold = config.agent.saturation_threshold
    sensitivity = config.agent.saturation_size_reduction_sensitivity

    if saturation_score > threshold:
        size_multiplier = 1.0 - (saturation_score - threshold) * sensitivity
        size_multiplier = _clamp(size_multiplier, 0.25, 1.0)
    else:
        size_multiplier = 1.0

    logger.info(
        "saturation_monitor.scored",
        market_id=signal.market_id,
        signal_id=signal.signal_id,
        drift_score=round(drift_score, 3),
        thinning_score=round(thinning_score, 3),
        saturation_score=round(saturation_score, 3),
        size_multiplier=round(size_multiplier, 3),
    )

    return saturation_score, size_multiplier


def _clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value to [min_val, max_val]."""
    return max(min_val, min(value, max_val))
