"""Signal-engine runner skeleton for Phase 0A-05D.

Consumes QualifiedWhaleTrade events, scores them, and publishes SignalEvent
payloads to the shared Redis rail.
"""
from __future__ import annotations

import structlog
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import (
    QualifiedWhaleTrade,
    RedisKeys,
    SignalDroppedError,
    SignalEvent,
    validate_qualified_whale_trade_for_publish,
)
from meg.core.redis_client import publish, subscribe
from meg.db.session import get_session
from meg.signal_engine import composite_scorer

logger = structlog.get_logger(__name__)

CONSUME_CHANNEL = RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES
PUBLISH_CHANNEL = RedisKeys.CHANNEL_SIGNAL_EVENTS


async def process_qualified_trade_payload(
    redis: Redis,
    raw_data: str,
    config: MegConfig,
    session: AsyncSession,
) -> bool:
    """Process one QualifiedWhaleTrade payload.

    Returns True only when a validated SignalEvent was published.
    """
    try:
        trade = QualifiedWhaleTrade.model_validate_json(raw_data)
        trade = validate_qualified_whale_trade_for_publish(trade)
    except ValueError as exc:
        logger.warning("signal_engine.runner.invalid_payload", error=str(exc))
        return False

    try:
        signal = await composite_scorer.score(trade, redis, session, config)
    except SignalDroppedError as exc:
        logger.info(
            "signal_engine.runner.signal_dropped",
            reason=exc.reason,
            score=exc.score,
            wallet=trade.wallet_address,
        )
        return False

    if signal is None:
        logger.debug("signal_engine.runner.no_signal")
        return False

    validated_signal = SignalEvent.model_validate(signal)
    await publish(redis, PUBLISH_CHANNEL, validated_signal.model_dump_json())
    return True


async def run(redis: Redis, config: MegConfig, session_factory=None) -> None:
    """Run the signal-engine channel bridge.

    Redis subscription failures propagate to caller.
    """
    session_factory = session_factory or get_session

    async with session_factory() as session:
        async for raw_data in subscribe(redis, CONSUME_CHANNEL):
            await process_qualified_trade_payload(redis, raw_data, config, session)
