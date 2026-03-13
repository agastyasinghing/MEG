"""
Signal aggregator.

Subscribes to Redis CHANNEL_SIGNAL_EVENTS, validates each incoming SignalEvent,
checks TTL/expiry, and routes valid signals to the decision agent.
Acts as the entry point for agent_core — nothing in this layer is triggered
except through events arriving on this channel.
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import SignalEvent


async def run(redis: Redis, config: MegConfig) -> None:
    """
    Subscribe to CHANNEL_SIGNAL_EVENTS and process incoming signals forever.
    Routes each valid signal to decision_agent.evaluate().
    Skips expired signals (logs and discards). Never raises on a single bad event.
    """
    raise NotImplementedError("signal_aggregator.run")


async def _validate_and_route(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
) -> None:
    """
    Validate a signal (check TTL, score threshold, status).
    Route to decision_agent.evaluate() if valid.
    Log and discard if expired or already processed.
    """
    raise NotImplementedError("signal_aggregator._validate_and_route")
