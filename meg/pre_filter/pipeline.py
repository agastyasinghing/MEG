"""
Pre-filter gate pipeline.

Subscribes to raw_whale_trades, runs each trade through the three gates in
order, and publishes qualified trades to qualified_whale_trades.

Gate pipeline:
  RawWhaleTrade (Redis: raw_whale_trades channel)
        │
        ├─ Gate 1: market_quality.check()
        │    fail → structlog WARN, discard
        │
        ├─ Gate 2: arbitrage_exclusion.check()
        │    fail → structlog WARN, discard
        │
        └─ Gate 3: intent_classifier.classify()
             HEDGE | REBALANCE → structlog INFO, discard
             SIGNAL | SIGNAL_LADDER
                  │
                  └─ build_qualified_trade()
                       wallet data unavailable → structlog ERROR, discard
                       QualifiedWhaleTrade → publish qualified_whale_trades

Logging: all gate rejections are logged via structlog only. Pre-filter events
are raw trades — they haven't become signals yet. signal_outcomes is written
by signal_engine, not pre_filter.

Error handling:
  - Each gate call is individually wrapped in try/except inside _process_event().
  - On any gate exception: log ERROR with gate_id + tx_hash, fail closed (discard).
  - Malformed JSON on Redis channel: log WARNING, skip, continue. Never crash.
  - NotImplementedError is re-raised — signals unimplemented code that must be
    fixed before the pipeline can run (e.g., intent_classifier.classify).

Session lifecycle:
  - run() creates one AsyncSession per trade event via get_session().
  - The session is passed through _process_event() to Gate 2 and Gate 3.
  - Tests call _process_event() directly with session=None (gates are mocked).
"""
from __future__ import annotations

import json

import structlog
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import RawWhaleTrade, RedisKeys
from meg.core.redis_client import publish, subscribe
from meg.pre_filter import arbitrage_exclusion, intent_classifier, market_quality

logger = structlog.get_logger(__name__)

# Intents that pass Gate 3 and proceed to signal_engine.
_PASSING_INTENTS = frozenset({"SIGNAL", "SIGNAL_LADDER"})


async def run(redis: Redis, config: MegConfig) -> None:
    """
    Main pipeline loop. Subscribes to raw_whale_trades and processes each
    event through all 3 gates.

    Runs forever — call as a long-running asyncio task:
        asyncio.create_task(pipeline.run(redis, config))

    Disconnects re-raise redis.exceptions.ConnectionError — the caller's
    reconnect loop is responsible for restarting this task on disconnect.
    """
    from meg.db.session import get_session

    logger.info("pre_filter.pipeline.started")

    async for raw in subscribe(redis, RedisKeys.CHANNEL_RAW_WHALE_TRADES):
        try:
            data = json.loads(raw)
            trade = RawWhaleTrade.model_validate(data)
        except Exception as exc:
            logger.warning(
                "pipeline.malformed_event",
                error=str(exc),
                raw_preview=raw[:200] if isinstance(raw, str) else repr(raw)[:200],
            )
            continue

        try:
            async with get_session() as session:
                await _process_event(trade, redis, config, session)
        except NotImplementedError:
            raise  # unimplemented gate — must be fixed, not swallowed
        except Exception as exc:
            logger.error(
                "pipeline.session_error",
                tx_hash=trade.tx_hash,
                market_id=trade.market_id,
                error=str(exc),
            )


async def _process_event(
    trade: RawWhaleTrade,
    redis: Redis,
    config: MegConfig,
    session: AsyncSession | None = None,
) -> None:
    """
    Run one trade through all 3 gates. Publish to qualified_whale_trades if
    it passes all gates with a SIGNAL or SIGNAL_LADDER intent.

    Each gate is individually wrapped in try/except — a single gate failure
    (Redis timeout, DB error) discards only the current trade and does not
    crash the pipeline loop.

    Exposed as a module-level function to allow direct testing of orchestration
    logic without exercising the subscribe() loop or session factory.
    """
    # ── Gate 1: Market Quality ────────────────────────────────────────────────
    try:
        g1_pass = await market_quality.check(trade, redis, config)
    except Exception as exc:
        logger.error(
            "pipeline.gate1_error",
            tx_hash=trade.tx_hash,
            market_id=trade.market_id,
            wallet_address=trade.wallet_address,
            error=str(exc),
        )
        return  # fail closed

    if not g1_pass:
        # Gate 1 already logs its own rejection reason — pipeline adds context.
        logger.warning(
            "pipeline.gate1_rejected",
            tx_hash=trade.tx_hash,
            market_id=trade.market_id,
            wallet_address=trade.wallet_address,
        )
        return

    # ── Gate 2: Arbitrage Exclusion ───────────────────────────────────────────
    try:
        g2_pass = await arbitrage_exclusion.check(trade, redis, config, session)
    except Exception as exc:
        logger.error(
            "pipeline.gate2_error",
            tx_hash=trade.tx_hash,
            market_id=trade.market_id,
            wallet_address=trade.wallet_address,
            error=str(exc),
        )
        return

    if not g2_pass:
        logger.warning(
            "pipeline.gate2_rejected",
            tx_hash=trade.tx_hash,
            market_id=trade.market_id,
            wallet_address=trade.wallet_address,
        )
        return

    # ── Gate 3: Intent Classification (OPUS) ─────────────────────────────────
    try:
        intent = await intent_classifier.classify(trade, redis, config, session)
    except NotImplementedError:
        raise  # unimplemented code must propagate — never swallow
    except Exception as exc:
        logger.error(
            "pipeline.gate3_error",
            tx_hash=trade.tx_hash,
            market_id=trade.market_id,
            wallet_address=trade.wallet_address,
            error=str(exc),
        )
        return

    if intent not in _PASSING_INTENTS:
        logger.info(
            "pipeline.gate3_filtered",
            tx_hash=trade.tx_hash,
            market_id=trade.market_id,
            wallet_address=trade.wallet_address,
            intent=intent,
            filter_reason="GATE_3",
        )
        return

    # ── Build and publish QualifiedWhaleTrade ─────────────────────────────────
    try:
        qualified = await intent_classifier.build_qualified_trade(trade, intent, redis)
    except NotImplementedError:
        raise
    except Exception as exc:
        logger.error(
            "pipeline.build_qualified_trade_error",
            tx_hash=trade.tx_hash,
            market_id=trade.market_id,
            wallet_address=trade.wallet_address,
            error=str(exc),
        )
        return

    if qualified is None:
        # Wallet data was unavailable in Redis — never emit with whale_score=0.0.
        logger.error(
            "pipeline.wallet_data_unavailable",
            tx_hash=trade.tx_hash,
            market_id=trade.market_id,
            wallet_address=trade.wallet_address,
        )
        return

    await publish(redis, RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES, qualified.model_dump_json())

    logger.info(
        "pipeline.qualified_trade_emitted",
        tx_hash=trade.tx_hash,
        market_id=trade.market_id,
        wallet_address=trade.wallet_address,
        intent=intent,
    )
