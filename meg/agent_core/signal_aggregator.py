"""
Signal aggregator — entry point for agent_core layer.

Subscribes to Redis CHANNEL_SIGNAL_EVENTS, validates each incoming SignalEvent,
checks TTL/expiry, and routes valid signals to the decision agent.

This is a pure router — no DB writes. Composite_scorer (signal_engine) owns
the INSERT into signal_outcomes. Decision_agent owns the status UPDATE.

Event flow:
  CHANNEL_SIGNAL_EVENTS (Redis pub/sub)
       │
       ▼
  Deserialize → SignalEvent
       │
       ├── malformed JSON        → log + skip
       ├── expired (TTL)         → log + skip
       ├── duplicate (seen set)  → log + skip
       └── valid                 → decision_agent.evaluate()
                                      └── exception → log + skip (never crash)

Dedup strategy: in-memory set of seen signal_ids. This is a best-effort
dedup for the current process lifetime — not a persistent guarantee. At v1
signal volume (~10/day), the set is tiny. For v2, consider a Redis set with
TTL matching signal TTL.
"""
from __future__ import annotations

import time

import structlog
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from meg.agent_core import decision_agent
from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, SignalEvent
from meg.core.redis_client import subscribe

logger = structlog.get_logger(__name__)

# In-memory dedup set. Bounded by signal TTL at ~10 signals/day = tiny.
_seen_signal_ids: set[str] = set()

# Cap dedup set to prevent unbounded growth on very long-running processes
_MAX_SEEN_SIGNALS = 10_000


async def run(
    redis: Redis,
    config: MegConfig,
    session: AsyncSession | None = None,
) -> None:
    """
    Subscribe to CHANNEL_SIGNAL_EVENTS and process incoming signals forever.
    Routes each valid signal to decision_agent.evaluate().
    Skips expired signals (logs and discards). Never raises on a single bad event.
    """
    logger.info("signal_aggregator.starting")

    async for message in subscribe(redis, RedisKeys.CHANNEL_SIGNAL_EVENTS):
        try:
            data = message.get("data")
            if data is None:
                continue

            # Handle bytes from Redis
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            if isinstance(data, int):
                continue  # subscription confirmation message

            await _validate_and_route(data, redis, config, session)

        except Exception:
            logger.error(
                "signal_aggregator.event_error",
                exc_info=True,
            )


async def _validate_and_route(
    raw_data: str,
    redis: Redis,
    config: MegConfig,
    session: AsyncSession | None = None,
) -> None:
    """
    Validate a signal (parse, check TTL, check dedup).
    Route to decision_agent.evaluate() if valid.
    Log and discard if expired or already processed.
    """
    # 1. Deserialize
    try:
        signal = SignalEvent.model_validate_json(raw_data)
    except Exception:
        logger.warning(
            "signal_aggregator.malformed_event",
            raw=raw_data[:500],
        )
        return

    signal_id = signal.signal_id

    # 2. Check dedup
    if signal_id in _seen_signal_ids:
        logger.debug(
            "signal_aggregator.duplicate_signal",
            signal_id=signal_id,
        )
        return

    # 3. Check TTL expiry
    now_ms = int(time.time() * 1000)
    if signal.ttl_expires_at_ms > 0 and now_ms > signal.ttl_expires_at_ms:
        logger.info(
            "signal_aggregator.expired_signal",
            signal_id=signal_id,
            expired_ms_ago=now_ms - signal.ttl_expires_at_ms,
        )
        return

    # 4. Mark as seen
    _seen_signal_ids.add(signal_id)
    # Prevent unbounded growth
    if len(_seen_signal_ids) > _MAX_SEEN_SIGNALS:
        # Remove oldest entries (set is unordered, but at v1 volume this is fine)
        excess = len(_seen_signal_ids) - _MAX_SEEN_SIGNALS
        for _ in range(excess):
            _seen_signal_ids.pop()

    # 5. Route to decision_agent
    logger.info(
        "signal_aggregator.routing",
        signal_id=signal_id,
        market_id=signal.market_id,
        composite_score=signal.composite_score,
    )

    if session is not None:
        try:
            await decision_agent.evaluate(signal, redis, config, session)
        except Exception:
            logger.error(
                "signal_aggregator.decision_agent_error",
                signal_id=signal_id,
                exc_info=True,
            )
    else:
        logger.warning(
            "signal_aggregator.no_session",
            signal_id=signal_id,
            note="signal received but no DB session available — cannot route to decision_agent",
        )
