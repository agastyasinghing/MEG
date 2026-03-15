"""
Signal decay timer.

Manages TTL for active signals. Signals degrade in strength over time using
an information half-life model: a signal's effective score is multiplied by
a decay factor that halves every config.signal_decay.half_life_seconds.

Signals with decayed score below config.signal_decay.min_score_after_decay
are marked EXPIRED and are never executed, regardless of their original score.

  t=0      score = 0.80  (strong signal)
  t=30min  score = 0.57  (half-life = 1hr, so ~71% after 30min)
  t=1hr    score = 0.40  (half of original)
  t=2hr    score = 0.20  (min threshold — signal expires)

v1 uses a single uniform half_life for all signal types.
TODO(v1.5): calibrate per-signal-type half-life baselines from signal_outcomes data.
  RESOLUTION_ASYMMETRY signals decay faster (resolution is imminent — 15–30min half-life).
  EVENT_CASCADE signals decay faster than WHALE_REACTION (crowd catches up quickly).
  BEHAVIORAL_DRIFT signals decay slower (structural edge, not time-sensitive).
  See TODOS.md: "per-signal-type half-life baselines".

PRD reference: §9.3.10 Signal Decay Timer
"""
from __future__ import annotations

import time

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, SignalEvent


def apply_decay(
    original_score: float,
    signal_age_seconds: float,
    config: MegConfig,
) -> float:
    """
    Return the decayed score for a signal of the given age.
    Uses exponential decay: score * 0.5 ^ (age / half_life).
    Returns 0.0 if decayed score is below min_score_after_decay.
    Returns 0.0 if signal_age_seconds < 0 (clock skew guard).
    """
    if signal_age_seconds < 0:
        return 0.0

    half_life = float(config.signal_decay.half_life_seconds)
    min_threshold = config.signal_decay.min_score_after_decay

    if half_life <= 0:
        return 0.0

    decayed = original_score * (0.5 ** (signal_age_seconds / half_life))

    if decayed < min_threshold:
        return 0.0

    return decayed


async def is_expired(signal: SignalEvent, config: MegConfig) -> bool:
    """
    Return True if the signal's TTL has elapsed or its decayed score
    has fallen below the minimum threshold.
    Expired signals must never be executed.
    """
    now_ms = int(time.time() * 1000)
    return now_ms >= signal.ttl_expires_at_ms


async def set_signal_ttl(signal: SignalEvent, redis: Redis, config: MegConfig) -> None:
    """
    Store the signal's expiry timestamp in Redis.
    Used by agent_core to quickly check signal validity before processing.

    TTL = max(half_life, min_half_life_minutes * 60) * ttl_half_life_multiplier
    """
    half_life_s = float(config.signal_decay.half_life_seconds)
    min_half_life_s = config.signal.min_half_life_minutes * 60.0
    multiplier = config.signal.ttl_half_life_multiplier

    effective_half_life = max(half_life_s, min_half_life_s)
    ttl_seconds = effective_half_life * multiplier

    now_ms = int(time.time() * 1000)
    expires_at_ms = now_ms + int(ttl_seconds * 1000)

    ttl_key = RedisKeys.signal_ttl(signal.signal_id)
    await redis.set(ttl_key, str(expires_at_ms))
