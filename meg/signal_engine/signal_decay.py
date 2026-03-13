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
"""
from __future__ import annotations

import time

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import SignalEvent


def apply_decay(
    original_score: float,
    signal_age_seconds: float,
    config: MegConfig,
) -> float:
    """
    Return the decayed score for a signal of the given age.
    Uses exponential decay: score * 0.5 ^ (age / half_life).
    Returns 0.0 if decayed score is below min_score_after_decay.
    """
    raise NotImplementedError("signal_decay.apply_decay")


async def is_expired(signal: SignalEvent, config: MegConfig) -> bool:
    """
    Return True if the signal's TTL has elapsed or its decayed score
    has fallen below the minimum threshold.
    Expired signals must never be executed.
    """
    raise NotImplementedError("signal_decay.is_expired")


async def set_signal_ttl(signal: SignalEvent, redis: Redis, config: MegConfig) -> None:
    """
    Store the signal's expiry timestamp in Redis.
    Used by agent_core to quickly check signal validity before processing.
    """
    raise NotImplementedError("signal_decay.set_signal_ttl")
