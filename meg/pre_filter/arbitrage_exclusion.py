"""
Pre-filter Gate 2: Arbitrage Whale Exclusion.

Detects wallets operating pure arbitrage strategies and excludes their trades.
Arb whales provide no directional signal — they're exploiting price discrepancies,
not expressing a view on outcome probability. Following them is noise.

Gate decision:
  RawWhaleTrade ──► check() ──► True  → pass to Gate 3 (intent classifier)
                            └──► False → log FILTERED via structlog, discard

Detection has two layers (short-circuited in order):

  1. ARCHETYPE CHECK (O(1) Redis read):
     If wallet:{addr}:archetype == "ARBITRAGE", reject immediately.
     Written by wallet_registry dual-write — always up to date within cache TTL.

  2. BEHAVIORAL CHECK (Trade table query):
     If the wallet has traded both YES and NO in the same market within
     config.pre_filter.arb_detection_window_hours, reject as behavioral arb.
     This catches wallets whose archetype hasn't been classified yet and wallets
     that recently shifted to arb behavior.

Architecture note: This module reads wallet data directly from Redis (no import
of meg.data_layer.wallet_registry — layer coupling violation). Trade table queries
use meg.db.models (shared infrastructure, not a layer). The compound index
ix_trades_wallet_market_time makes these queries efficient.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import structlog
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import RawWhaleTrade, RedisKeys
from meg.db.models import Trade

logger = structlog.get_logger(__name__)


async def check(
    trade: RawWhaleTrade,
    redis: Redis,
    config: MegConfig,
    session: AsyncSession | None = None,
) -> bool:
    """
    Return True if the wallet is NOT an arbitrage whale (i.e., passes this gate).

    Short-circuits on archetype check: if ARBITRAGE archetype is found in Redis,
    the behavioral DB query is skipped entirely. The behavioral check provides
    a secondary signal for wallets not yet classified or recently reclassified.

    session=None skips the behavioral check (returns True if archetype is clean).
    This is the default for tests that don't exercise the behavioral path.
    """
    wallet_address = trade.wallet_address
    market_id = trade.market_id

    # Check 1: archetype-based (fast path — O(1) Redis read)
    if await _is_arb_archetype(wallet_address, redis):
        logger.warning(
            "arbitrage_exclusion.rejected",
            wallet_address=wallet_address,
            market_id=market_id,
            tx_hash=trade.tx_hash,
            filter_reason="GATE_2_ARB_ARCHETYPE",
        )
        return False

    # Check 2: behavioral (Trade table — detects unclassified or reclassified arb wallets)
    if await _has_simultaneous_both_sides(wallet_address, market_id, config, session):
        logger.warning(
            "arbitrage_exclusion.rejected",
            wallet_address=wallet_address,
            market_id=market_id,
            tx_hash=trade.tx_hash,
            filter_reason="GATE_2_BOTH_SIDES_DETECTED",
        )
        return False

    return True


async def _is_arb_archetype(wallet_address: str, redis: Redis) -> bool:
    """
    Return True if the wallet's registered archetype is ARBITRAGE.

    Reads wallet:{addr}:archetype directly from Redis (written by wallet_registry
    dual-write). Returns False if the key is absent — unknown wallets are treated
    as non-arb and proceed to the behavioral check.

    On Redis error: logs WARNING and returns False (conservative — lets the trade
    proceed to the behavioral check rather than silently dropping it).
    """
    try:
        archetype = await redis.get(RedisKeys.wallet_archetype(wallet_address))
    except Exception as exc:
        logger.warning(
            "arbitrage_exclusion.archetype_lookup_error",
            wallet_address=wallet_address,
            error=str(exc),
        )
        return False  # on Redis error: treat as non-arb, proceed to behavioral check

    return archetype == "ARBITRAGE"


async def _has_simultaneous_both_sides(
    wallet_address: str,
    market_id: str,
    config: MegConfig,
    session: AsyncSession | None = None,
) -> bool:
    """
    Return True if the wallet has traded both YES and NO in the same market
    within config.pre_filter.arb_detection_window_hours.

    Queries the Trade table directly — authoritative over all observed trades,
    including those that were filtered at Gate 1. The compound index
    ix_trades_wallet_market_time (wallet_address, market_id, traded_at DESC)
    makes this query efficient even at high trade volume.

    Returns False when session is None — behavioral check is skipped. This is
    safe: the archetype check already ran. If a wallet has no archetype and we
    can't query the DB, we conservatively allow the trade through.

    On DB error: logs WARNING and returns False (non-arb) so the trade is not
    silently dropped due to a transient infrastructure failure.
    """
    if session is None:
        return False

    window_hours = config.pre_filter.arb_detection_window_hours
    cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=window_hours)

    try:
        stmt = (
            select(Trade.outcome)
            .where(
                Trade.wallet_address == wallet_address,
                Trade.market_id == market_id,
                Trade.traded_at >= cutoff,
            )
            .distinct()
        )
        result = await session.execute(stmt)
        outcomes = {row[0] for row in result.all()}
        return "YES" in outcomes and "NO" in outcomes

    except Exception as exc:
        logger.warning(
            "arbitrage_exclusion.behavioral_check_error",
            wallet_address=wallet_address,
            market_id=market_id,
            error=str(exc),
        )
        return False  # on DB error: treat as non-arb (conservative)
