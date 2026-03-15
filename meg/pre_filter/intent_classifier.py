"""
Pre-filter Gate 3: Intent Classifier.

Classifies a whale trade as one of: SIGNAL, SIGNAL_LADDER, HEDGE, or REBALANCE.
Only SIGNAL and SIGNAL_LADDER trades pass to the signal engine. HEDGE and
REBALANCE represent portfolio mechanics, not directional conviction — they are
logged via structlog but not acted upon.

Gate decision:
  RawWhaleTrade ──► classify() ──► SIGNAL        → build_qualified_trade() → emit
                               ├──► SIGNAL_LADDER → build_qualified_trade() → emit
                               ├──► HEDGE         → log FILTERED, discard
                               └──► REBALANCE     → log FILTERED, discard

⚠️  OPUS + ULTRATHINK REQUIRED
This module's classify() and build_qualified_trade() implementations must be
written in an Opus session. The classification logic directly determines what
reaches the signal engine — getting SIGNAL vs HEDGE/REBALANCE wrong means
either signal starvation (false HEDGEs) or noise injection (REBALANCEs reaching
the signal engine). The test spec is in tests/pre_filter/test_intent_classifier.py
— read that file first, then implement against the tests.

Architecture note: This module reads wallet data directly from Redis (no import
of meg.data_layer.wallet_registry — layer coupling violation). Trade table queries
use meg.db.models (shared infrastructure, not a layer).

Intent definitions:
  SIGNAL:        New directional position. Whale is expressing a view on outcome
                 probability. Characterised by: first or fresh position in this
                 market, size >= config.pre_filter.min_signal_size_pct * capital,
                 no opposing position in the same market.

  SIGNAL_LADDER: Whale is building conviction — multiple same-direction trades in
                 the same market within config.pre_filter.ladder_window_hours.
                 Requires >= config.pre_filter.ladder_min_trades prior same-direction
                 trades within the window. Higher conviction than a single SIGNAL.

  HEDGE:         Risk management. Whale is offsetting exposure elsewhere.
                 Characterised by: current trade opposing a prior position of
                 equal or greater size in the same market.

  REBALANCE:     Portfolio mechanics. Size adjustment, profit-taking, or
                 liquidity management. Characterised by: trade size below
                 min_signal_size_pct threshold, or trade reducing/closing
                 an existing same-direction position.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Literal

import structlog
from redis.asyncio import Redis
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade, RawWhaleTrade, RedisKeys
from meg.db.models import Trade

logger = structlog.get_logger(__name__)

Intent = Literal["SIGNAL", "SIGNAL_LADDER", "HEDGE", "REBALANCE"]


async def classify(
    trade: RawWhaleTrade,
    redis: Redis,
    config: MegConfig,
    session: AsyncSession | None = None,
) -> Intent:
    """
    Classify a whale trade's intent. Returns one of: SIGNAL, SIGNAL_LADDER,
    HEDGE, REBALANCE.

    Decision order:
      1. Read wallet data from Redis → wallet:{addr}:data JSON blob.
         If unavailable (cache miss), return SIGNAL conservatively.
      2. Compute size threshold = min_signal_size_pct * total_capital_usdc.
         If trade.size_usdc < threshold → REBALANCE (portfolio mechanics).
      3. If session is None → skip DB queries → return SIGNAL (conservative).
      4. Check HEDGE: prior opposing-direction trade with size >= current trade
         size → HEDGE (current trade fits within existing opposing exposure).
      5. Check SIGNAL_LADDER: >= ladder_min_trades same-direction trades within
         ladder_window_hours → SIGNAL_LADDER (escalating conviction).
      6. Default → SIGNAL.
    """
    # 1. Read wallet data from Redis
    wallet_data_raw = await redis.get(RedisKeys.wallet_data(trade.wallet_address))
    if wallet_data_raw is None:
        logger.info(
            "intent_classifier.wallet_data_missing",
            wallet=trade.wallet_address,
            fallback="SIGNAL",
        )
        return "SIGNAL"

    wallet_data = json.loads(wallet_data_raw)
    total_capital_usdc: float = wallet_data.get("total_capital_usdc", 0.0)

    # 2. Size threshold check — below threshold is portfolio noise
    threshold = config.pre_filter.min_signal_size_pct * total_capital_usdc
    if trade.size_usdc < threshold:
        logger.info(
            "intent_classifier.rebalance_below_threshold",
            wallet=trade.wallet_address,
            market=trade.market_id,
            size_usdc=trade.size_usdc,
            threshold_usdc=threshold,
        )
        return "REBALANCE"

    # 3. No session → can't query Trade table for behavioral patterns
    if session is None:
        logger.info(
            "intent_classifier.no_session_fallback",
            wallet=trade.wallet_address,
            market=trade.market_id,
            fallback="SIGNAL",
        )
        return "SIGNAL"

    # 4. HEDGE: the current trade fits within an existing opposing position.
    #    Requires at least one prior opposing-direction trade whose size >= the
    #    current trade's size — meaning the whale is offsetting part of their
    #    existing exposure, not making a new net directional bet.
    opposing_outcome = "NO" if trade.outcome == "YES" else "YES"
    hedge_stmt = (
        select(func.count())
        .select_from(Trade)
        .where(
            and_(
                Trade.wallet_address == trade.wallet_address,
                Trade.market_id == trade.market_id,
                Trade.outcome == opposing_outcome,
                Trade.size_usdc >= trade.size_usdc,
            )
        )
    )
    hedge_result = await session.execute(hedge_stmt)
    if hedge_result.scalar() > 0:
        logger.info(
            "intent_classifier.hedge_detected",
            wallet=trade.wallet_address,
            market=trade.market_id,
            outcome=trade.outcome,
            opposing=opposing_outcome,
        )
        return "HEDGE"

    # 5. SIGNAL_LADDER: same-direction trades within ladder window.
    #    Pushed to SQL to avoid timezone-naive vs timezone-aware comparison
    #    issues across database backends (PostgreSQL vs SQLite in tests).
    window_cutoff = datetime.now(tz=timezone.utc) - timedelta(
        hours=config.pre_filter.ladder_window_hours
    )
    ladder_stmt = (
        select(func.count())
        .select_from(Trade)
        .where(
            and_(
                Trade.wallet_address == trade.wallet_address,
                Trade.market_id == trade.market_id,
                Trade.outcome == trade.outcome,
                Trade.traded_at >= window_cutoff,
            )
        )
    )
    ladder_result = await session.execute(ladder_stmt)
    if ladder_result.scalar() >= config.pre_filter.ladder_min_trades:
        logger.info(
            "intent_classifier.signal_ladder_detected",
            wallet=trade.wallet_address,
            market=trade.market_id,
            outcome=trade.outcome,
            window_hours=config.pre_filter.ladder_window_hours,
        )
        return "SIGNAL_LADDER"

    # 6. Default — new directional position
    return "SIGNAL"


async def build_qualified_trade(
    trade: RawWhaleTrade,
    intent: Intent,
    redis: Redis,
) -> QualifiedWhaleTrade | None:
    """
    Construct a QualifiedWhaleTrade from a RawWhaleTrade after classification.

    Enriches with whale_score and archetype read directly from Redis keys:
      wallet:{addr}:score     → float string (composite_whale_score)
      wallet:{addr}:archetype → archetype string

    Returns None if either key is absent — never emit a QualifiedWhaleTrade
    with whale_score=0.0 or a missing archetype.
    """
    score_raw = await redis.get(RedisKeys.wallet_score(trade.wallet_address))
    if score_raw is None:
        logger.error(
            "intent_classifier.wallet_score_missing",
            wallet=trade.wallet_address,
        )
        return None

    archetype_raw = await redis.get(RedisKeys.wallet_archetype(trade.wallet_address))
    if archetype_raw is None:
        logger.error(
            "intent_classifier.wallet_archetype_missing",
            wallet=trade.wallet_address,
        )
        return None

    return QualifiedWhaleTrade(
        wallet_address=trade.wallet_address,
        market_id=trade.market_id,
        outcome=trade.outcome,
        size_usdc=trade.size_usdc,
        timestamp_ms=trade.timestamp_ms,
        tx_hash=trade.tx_hash,
        block_number=trade.block_number,
        market_price_at_trade=trade.market_price_at_trade,
        whale_score=float(score_raw),
        archetype=archetype_raw,
        intent=intent,
    )
