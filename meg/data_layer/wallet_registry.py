"""
Whale wallet registry — PostgreSQL reads/writes and Redis score cache.

Maintains the database of tracked whale wallets, their scores, archetypes,
and historical performance. The registry is the source of truth for wallet
qualification. Redis caches hot-path score lookups (TTL: 5 minutes).

Cache-through read pattern:
  get_wallet(address, redis) → Redis HIT → return cached dict
                             → Redis MISS → query PG → populate Redis → return

Dual-write on mutation:
  upsert_wallet / update_wallet_score → write PG first → then update Redis
  Order: PG first (durable) → Redis second (cache). On Redis failure: log
  WARNING and continue — the DB is authoritative; cache can be rebuilt.

Session injection for tests:
  All DB-touching functions accept `session: AsyncSession | None = None`.
  Production calls use get_session() internally.
  Tests inject the rollback-protected db_session fixture directly.

Redis key layout:
  wallet:{address}:score       → composite_whale_score (string float)
  wallet:{address}:archetype   → archetype string
  wallet:{address}:data        → full wallet dict as JSON (TTL 300s)

TTL: 300 seconds (5 minutes) for all wallet cache keys.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import structlog
from redis.asyncio import Redis
from sqlalchemy import select, update as sa_update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys
from meg.db.models import Wallet
from meg.db.session import get_session

logger = structlog.get_logger(__name__)

# Redis cache TTL for wallet data (seconds)
_CACHE_TTL = 300

# Redis key for full wallet data cache
def _wallet_data_key(address: str) -> str:
    return f"wallet:{address}:data"


# ── Internal DB helpers ────────────────────────────────────────────────────────


async def _db_get_wallet(address: str, session: AsyncSession) -> Wallet | None:
    result = await session.execute(
        select(Wallet).where(Wallet.address == address)
    )
    return result.scalar_one_or_none()


def _wallet_to_dict(w: Wallet) -> dict[str, Any]:
    """Serialize a Wallet ORM row to a plain dict for caching and return."""
    return {
        "address": w.address,
        "archetype": w.archetype,
        "is_qualified": w.is_qualified,
        "composite_whale_score": float(w.composite_whale_score),
        "win_rate": float(w.win_rate),
        "avg_lead_time_hours": float(w.avg_lead_time_hours),
        "roi_30d": float(w.roi_30d),
        "roi_90d": float(w.roi_90d),
        "roi_all_time": float(w.roi_all_time),
        "total_closed_positions": w.total_closed_positions,
        "consistency_score": float(w.consistency_score),
        "avg_conviction_ratio": float(w.avg_conviction_ratio),
        "reputation_decay_factor": float(w.reputation_decay_factor),
        "category_scores": w.category_scores or {},
        "first_seen_at": w.first_seen_at.isoformat() if w.first_seen_at else None,
        "last_seen_at": w.last_seen_at.isoformat() if w.last_seen_at else None,
        "notes": w.notes,
        "total_volume_usdc": float(w.total_volume_usdc),
        "total_trades": w.total_trades,
        "total_capital_usdc": float(w.total_capital_usdc) if w.total_capital_usdc is not None else None,
        "is_tracked": w.is_tracked,
        "is_excluded": w.is_excluded,
        "exclusion_reason": w.exclusion_reason,
        "avg_hold_time_hours": float(w.avg_hold_time_hours) if w.avg_hold_time_hours is not None else None,
    }


async def _cache_wallet(address: str, data: dict[str, Any], redis: Redis) -> None:
    """Write all three Redis cache keys for a wallet. Logs on failure, never raises."""
    try:
        pipe = redis.pipeline(transaction=False)
        # Full data blob (used by get_wallet cache hit)
        pipe.set(_wallet_data_key(address), json.dumps(data), ex=_CACHE_TTL)
        # Scalar score key (hot path for pre_filter and signal_engine)
        pipe.set(
            RedisKeys.wallet_score(address),
            str(data["composite_whale_score"]),
            ex=_CACHE_TTL,
        )
        # Archetype key (hot path for archetype_weighter)
        pipe.set(
            RedisKeys.wallet_archetype(address),
            str(data["archetype"]),
            ex=_CACHE_TTL,
        )
        await pipe.execute()
    except Exception as exc:
        logger.warning(
            "wallet_registry.cache_write_failed",
            address=address,
            error=str(exc),
        )


async def _invalidate_cache(address: str, redis: Redis) -> None:
    """Delete all Redis cache keys for a wallet. Logs on failure, never raises."""
    try:
        await redis.delete(
            _wallet_data_key(address),
            RedisKeys.wallet_score(address),
            RedisKeys.wallet_archetype(address),
        )
    except Exception as exc:
        logger.warning(
            "wallet_registry.cache_invalidate_failed",
            address=address,
            error=str(exc),
        )


# ── Public API ─────────────────────────────────────────────────────────────────


async def get_wallet(
    address: str,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> dict[str, Any] | None:
    """
    Return wallet data for the given address, or None if not in registry.
    Redis-first: checks wallet:{address}:data cache before hitting PostgreSQL.
    Populates cache on DB hit (TTL 300s).
    """
    # Fast path: Redis cache hit
    try:
        cached = await redis.get(_wallet_data_key(address))
        if cached is not None:
            return json.loads(cached)
    except Exception as exc:
        logger.warning("wallet_registry.cache_read_failed", address=address, error=str(exc))

    # Slow path: query PostgreSQL
    if session is not None:
        wallet = await _db_get_wallet(address, session)
        if wallet is None:
            return None
        data = _wallet_to_dict(wallet)
        await _cache_wallet(address, data, redis)
        return data

    async with get_session() as s:
        wallet = await _db_get_wallet(address, s)
        if wallet is None:
            return None
        data = _wallet_to_dict(wallet)

    await _cache_wallet(address, data, redis)
    return data


async def upsert_wallet(
    address: str,
    data: dict[str, Any],
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> None:
    """
    Insert or update a wallet record in PostgreSQL, then refresh Redis cache.
    Write order: DB first (durable), then Redis (cache). On Redis failure: log + continue.

    data dict fields map directly to Wallet ORM columns. Unknown keys are ignored.
    """
    now = datetime.now(tz=timezone.utc)

    # Build insert statement with ON CONFLICT DO UPDATE (true upsert)
    stmt = pg_insert(Wallet).values(
        address=address,
        archetype=data.get("archetype", "MOMENTUM"),
        is_qualified=data.get("is_qualified", False),
        composite_whale_score=data.get("composite_whale_score", 0.0),
        win_rate=data.get("win_rate", 0.0),
        avg_lead_time_hours=data.get("avg_lead_time_hours", 0.0),
        roi_30d=data.get("roi_30d", 0.0),
        roi_90d=data.get("roi_90d", 0.0),
        roi_all_time=data.get("roi_all_time", 0.0),
        total_closed_positions=data.get("total_closed_positions", 0),
        consistency_score=data.get("consistency_score", 0.0),
        avg_conviction_ratio=data.get("avg_conviction_ratio", 0.0),
        reputation_decay_factor=data.get("reputation_decay_factor", 1.0),
        category_scores=data.get("category_scores", {}),
        first_seen_at=data.get("first_seen_at", now),
        last_seen_at=now,
        notes=data.get("notes"),
        total_volume_usdc=data.get("total_volume_usdc", 0.0),
        total_trades=data.get("total_trades", 0),
        total_capital_usdc=data.get("total_capital_usdc"),
        is_tracked=data.get("is_tracked", False),
        is_excluded=data.get("is_excluded", False),
        exclusion_reason=data.get("exclusion_reason"),
        avg_hold_time_hours=data.get("avg_hold_time_hours"),
    ).on_conflict_do_update(
        index_elements=["address"],
        set_={
            "archetype": data.get("archetype", "MOMENTUM"),
            "is_qualified": data.get("is_qualified", False),
            "composite_whale_score": data.get("composite_whale_score", 0.0),
            "win_rate": data.get("win_rate", 0.0),
            "avg_lead_time_hours": data.get("avg_lead_time_hours", 0.0),
            "roi_30d": data.get("roi_30d", 0.0),
            "roi_90d": data.get("roi_90d", 0.0),
            "roi_all_time": data.get("roi_all_time", 0.0),
            "total_closed_positions": data.get("total_closed_positions", 0),
            "consistency_score": data.get("consistency_score", 0.0),
            "avg_conviction_ratio": data.get("avg_conviction_ratio", 0.0),
            "reputation_decay_factor": data.get("reputation_decay_factor", 1.0),
            "category_scores": data.get("category_scores", {}),
            "last_seen_at": now,
            "notes": data.get("notes"),
            "total_volume_usdc": data.get("total_volume_usdc", 0.0),
            "total_trades": data.get("total_trades", 0),
            "total_capital_usdc": data.get("total_capital_usdc"),
            "is_tracked": data.get("is_tracked", False),
            "is_excluded": data.get("is_excluded", False),
            "exclusion_reason": data.get("exclusion_reason"),
            "avg_hold_time_hours": data.get("avg_hold_time_hours"),
        },
    )

    if session is not None:
        await session.execute(stmt)
    else:
        async with get_session() as s:
            await s.execute(stmt)

    # Invalidate cache so next read pulls fresh data from DB
    await _invalidate_cache(address, redis)
    logger.debug("wallet_registry.upserted", address=address)


async def register_if_new(
    address: str,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> bool:
    """
    Register a wallet as is_tracked=True if it does not already exist.
    Returns True if a new row was created, False if wallet already existed.

    Called by polygon_feed when an unknown wallet address appears in a CLOB tx.
    Minimal initial data — scores default to 0; reputation system fills them in.
    """
    existing = await get_wallet(address, redis, session=session)
    if existing is not None:
        return False

    await upsert_wallet(
        address,
        {
            "archetype": "MOMENTUM",  # default until classifier runs
            "is_tracked": True,
            "is_qualified": False,
        },
        redis,
        session=session,
    )
    logger.info("wallet_registry.registered_new_wallet", address=address)
    return True


async def get_qualified_whale_wallets(
    config: MegConfig,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> list[dict[str, Any]]:
    """
    Return all wallets meeting current whale qualification thresholds.
    Thresholds are read from config — hot-reloadable.

    Qualification criteria (from config.whale_qualification):
      - win_rate >= min_win_rate
      - total_closed_positions >= min_closed_positions
      - total_volume_usdc >= min_total_volume_usdc
      - archetype NOT IN exclude_archetypes
      - is_excluded = False
    """
    qc = config.whale_qualification

    stmt = select(Wallet).where(
        Wallet.win_rate >= qc.min_win_rate,
        Wallet.total_closed_positions >= qc.min_closed_positions,
        Wallet.total_volume_usdc >= qc.min_total_volume_usdc,
        Wallet.is_excluded.is_(False),
        Wallet.archetype.notin_(qc.exclude_archetypes),
    )

    if session is not None:
        result = await session.execute(stmt)
        return [_wallet_to_dict(w) for w in result.scalars().all()]

    async with get_session() as s:
        result = await s.execute(stmt)
        return [_wallet_to_dict(w) for w in result.scalars().all()]


async def is_qualified_whale(
    address: str,
    config: MegConfig,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> bool:
    """
    Return True if the wallet meets all whale qualification thresholds.
    Fast path: checks cached score first; then DB if cache miss.
    """
    # Fast path: if score key exists in Redis, check the qualification flag from full data
    try:
        score_str = await redis.get(RedisKeys.wallet_score(address))
        if score_str is not None:
            # Score cache hit — fetch full data to check qualification flags
            cached = await redis.get(_wallet_data_key(address))
            if cached is not None:
                data = json.loads(cached)
                if data.get("is_excluded"):
                    return False
                archetype = data.get("archetype", "")
                if archetype in config.whale_qualification.exclude_archetypes:
                    return False
                return bool(data.get("is_qualified", False))
    except Exception as exc:
        logger.warning(
            "wallet_registry.is_qualified_cache_error",
            address=address,
            error=str(exc),
        )

    # Slow path: DB query
    data = await get_wallet(address, redis, session=session)
    if data is None:
        return False
    if data.get("is_excluded"):
        return False
    if data.get("archetype") in config.whale_qualification.exclude_archetypes:
        return False
    return bool(data.get("is_qualified", False))


async def update_wallet_score(
    address: str,
    score: float,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> None:
    """
    Persist an updated composite_whale_score to PostgreSQL and refresh Redis.
    Called by reputation_decay after each trade outcome.
    Write order: DB first (durable), then Redis (cache).
    """
    stmt = (
        sa_update(Wallet)
        .where(Wallet.address == address)
        .values(composite_whale_score=score, last_seen_at=datetime.now(tz=timezone.utc))
    )

    if session is not None:
        await session.execute(stmt)
    else:
        async with get_session() as s:
            await s.execute(stmt)

    # Update Redis score key directly (fast) then invalidate full data blob
    try:
        pipe = redis.pipeline(transaction=False)
        pipe.set(RedisKeys.wallet_score(address), str(score), ex=_CACHE_TTL)
        pipe.delete(_wallet_data_key(address))  # force full re-fetch on next get_wallet
        await pipe.execute()
    except Exception as exc:
        logger.warning(
            "wallet_registry.score_cache_update_failed",
            address=address,
            error=str(exc),
        )

    logger.debug("wallet_registry.score_updated", address=address, score=score)


async def get_wallet_archetype(
    address: str,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> str | None:
    """
    Return the archetype string for a wallet, or None if not in registry.
    Redis-first: checks wallet:{address}:archetype before hitting PostgreSQL.
    """
    try:
        cached = await redis.get(RedisKeys.wallet_archetype(address))
        if cached is not None:
            return cached
    except Exception as exc:
        logger.warning(
            "wallet_registry.archetype_cache_error",
            address=address,
            error=str(exc),
        )

    data = await get_wallet(address, redis, session=session)
    return data.get("archetype") if data else None


async def qualify(
    address: str,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> None:
    """
    Mark a wallet as is_qualified=True after it meets all qualification thresholds.
    Called by the bootstrap script and by reputation_decay after re-evaluation.
    """
    stmt = (
        sa_update(Wallet)
        .where(Wallet.address == address)
        .values(is_qualified=True, last_seen_at=datetime.now(tz=timezone.utc))
    )
    if session is not None:
        await session.execute(stmt)
    else:
        async with get_session() as s:
            await s.execute(stmt)

    await _invalidate_cache(address, redis)
    logger.info("wallet_registry.qualified", address=address)


async def disqualify(
    address: str,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> None:
    """
    Mark a wallet as is_qualified=False.
    Called by reputation_decay when a wallet falls below thresholds.
    """
    stmt = (
        sa_update(Wallet)
        .where(Wallet.address == address)
        .values(is_qualified=False, last_seen_at=datetime.now(tz=timezone.utc))
    )
    if session is not None:
        await session.execute(stmt)
    else:
        async with get_session() as s:
            await s.execute(stmt)

    await _invalidate_cache(address, redis)
    logger.info("wallet_registry.disqualified", address=address)


async def flag_excluded(
    address: str,
    reason: str,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> None:
    """
    Mark a wallet as is_excluded=True (ARBITRAGE or MANIPULATOR detection).
    Excluded wallets are never used for signals, regardless of score.
    """
    stmt = (
        sa_update(Wallet)
        .where(Wallet.address == address)
        .values(
            is_excluded=True,
            exclusion_reason=reason,
            is_qualified=False,
            last_seen_at=datetime.now(tz=timezone.utc),
        )
    )
    if session is not None:
        await session.execute(stmt)
    else:
        async with get_session() as s:
            await s.execute(stmt)

    await _invalidate_cache(address, redis)
    logger.info("wallet_registry.excluded", address=address, reason=reason)


async def update_capital(
    address: str,
    capital_usdc: float,
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> None:
    """
    Update total_capital_usdc for a wallet.
    Called daily by CapitalRefreshJob from Polygon RPC USDC balance query.
    Required for conviction ratio calculation.
    """
    stmt = (
        sa_update(Wallet)
        .where(Wallet.address == address)
        .values(
            total_capital_usdc=capital_usdc,
            last_seen_at=datetime.now(tz=timezone.utc),
        )
    )
    if session is not None:
        await session.execute(stmt)
    else:
        async with get_session() as s:
            await s.execute(stmt)

    # Invalidate full data blob so next get_wallet returns fresh capital value
    await _invalidate_cache(address, redis)
    logger.debug(
        "wallet_registry.capital_updated",
        address=address,
        capital_usdc=capital_usdc,
    )


async def get_tracked_addresses(
    redis: Redis,
    *,
    session: AsyncSession | None = None,
) -> list[str]:
    """
    Return all wallet addresses with is_tracked=True.
    Used by CapitalRefreshJob to iterate tracked wallets for USDC balance refresh.
    """
    stmt = select(Wallet.address).where(Wallet.is_tracked.is_(True))

    if session is not None:
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async with get_session() as s:
        result = await s.execute(stmt)
        return list(result.scalars().all())
