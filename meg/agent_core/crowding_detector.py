"""
Signal crowding detector — price-based entry distance gate (v1).

Detects when copy-follower bots have already entered the same position,
eliminating the edge MEG exploits. Even if the whale signal is fresh, a crowded
entry means we're buying into already-inflated prices with reduced upside.

v1 implementation: price-based heuristics (no copy-follower wallet registry):
  1. Entry distance: current_mid vs whale's fill price (market_price_at_signal)
  2. Direction check: only counts drift in the signal's direction

Distinct from saturation_monitor:
  - saturation_monitor: reduces position SIZE (does not block)
  - crowding_detector: BLOCKS the signal entirely (edge is gone)

Distinct from execution layer entry_filter:
  - crowding_detector (agent_core): coarser, pre-execution, saves operator attention
  - entry_filter (execution):       finer, at fill time, handles slippage

v1.5 upgrade (see TODOS.md): add copy-follower wallet registry for volume-based
crowding detection alongside price-based checks.
"""
from __future__ import annotations

import structlog
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, SignalEvent

logger = structlog.get_logger(__name__)


async def check(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """
    Return (False, "") if entry is not yet crowded (edge still exists).
    Return (True, reason) if copy-follower entry has already occurred at scale.

    Returns (False, "") when market data is unavailable — fail open.
    """
    # Read current market price
    mid_raw = await redis.get(RedisKeys.market_mid_price(signal.market_id))
    if mid_raw is None:
        # No price data — cannot assess crowding. Fail open.
        return False, ""

    current_mid = float(mid_raw)
    signal_price = signal.market_price_at_signal

    if signal_price <= 0:
        return False, ""

    # Calculate directional entry distance
    # For YES outcome: price moving UP from whale fill = copy traders entered
    # For NO outcome:  price moving DOWN from whale fill = copy traders entered
    if signal.outcome == "YES":
        entry_distance = (current_mid - signal_price) / signal_price
    else:
        entry_distance = (signal_price - current_mid) / signal_price

    # Only positive drift (in signal direction) counts as crowding
    # Negative drift (price moved against signal) = no crowding
    if entry_distance <= 0:
        return False, ""

    threshold = config.agent.crowding_max_entry_distance_pct

    if entry_distance > threshold:
        reason = (
            f"window_closed: price moved {entry_distance:.1%} "
            f"in signal direction (threshold: {threshold:.1%}). "
            f"whale_fill={signal_price:.4f}, current={current_mid:.4f}"
        )
        logger.info(
            "crowding_detector.blocked",
            market_id=signal.market_id,
            signal_id=signal.signal_id,
            entry_distance=round(entry_distance, 4),
            threshold=threshold,
        )
        return True, reason

    return False, ""
