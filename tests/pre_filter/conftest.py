"""
Pre-filter test fixtures and factory helpers.

DB fixtures (db_engine, db_session) use SQLite in-memory via aiosqlite for
fast local testing. Production uses PostgreSQL — the ORM layer abstracts
differences (SAEnum(native_enum=False), no JSONB in these tables).

TODO: Restore pytest-postgresql as the CI fixture when PostgreSQL is available
in the CI environment. SQLite is acceptable for Gate 2/3 (Trade table only,
no JSONB) but real PG catches type/constraint edge cases SQLite masks.
See original conftest at commit 600bd9b for the pytest-postgresql pattern.

Factory helpers (make_raw_trade, set_wallet_redis_data, set_market_redis_data,
insert_trade_record) are shared across all four pre_filter test modules.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone

import pytest_asyncio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from meg.core.events import RawWhaleTrade, RedisKeys
from meg.db.models import Trade


# ── DB fixtures ───────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def db_engine() -> AsyncEngine:
    """
    SQLite in-memory engine for behavioral detection tests (Gate 2/3).
    Creates only the Trade table (other models use JSONB which SQLite
    doesn't support). Gate 2/3 tests only query the Trade table.
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Trade.__table__.create)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Trade.__table__.drop)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine: AsyncEngine) -> AsyncSession:
    """
    Yield a fresh session per test. Rolls back after the test — no data
    bleeds between tests.
    """
    async with AsyncSession(db_engine) as session:
        await session.begin()
        try:
            yield session
        finally:
            await session.rollback()


# ── Factory helpers ───────────────────────────────────────────────────────


def make_raw_trade(
    *,
    wallet_address: str = "0xWHALE001",
    market_id: str = "market_001",
    outcome: str = "YES",
    size_usdc: float = 1_000.0,
    tx_hash: str = "0xtx001",
    block_number: int = 12_345,
    market_price_at_trade: float = 0.65,
    timestamp_ms: int | None = None,
) -> RawWhaleTrade:
    """Return a RawWhaleTrade with sensible defaults. Override as needed."""
    return RawWhaleTrade(
        wallet_address=wallet_address,
        market_id=market_id,
        outcome=outcome,
        size_usdc=size_usdc,
        timestamp_ms=timestamp_ms or int(datetime.now(tz=timezone.utc).timestamp() * 1000),
        tx_hash=tx_hash,
        block_number=block_number,
        market_price_at_trade=market_price_at_trade,
    )


async def set_wallet_redis_data(
    redis: Redis,
    *,
    wallet_address: str = "0xWHALE001",
    archetype: str = "INFORMATION",
    score: float = 0.75,
    total_capital_usdc: float = 50_000.0,
    avg_conviction_ratio: float = 0.05,
) -> None:
    """
    Write wallet data to fakeredis as wallet_registry would.

    Writes three keys:
      wallet:{addr}:archetype  — used by Gate 2 archetype check
      wallet:{addr}:score      — used by build_qualified_trade
      wallet:{addr}:data       — JSON blob used by Gate 3 classify()
    """
    await redis.set(RedisKeys.wallet_archetype(wallet_address), archetype)
    await redis.set(RedisKeys.wallet_score(wallet_address), str(score))
    data = {
        "address": wallet_address,
        "archetype": archetype,
        "composite_whale_score": score,
        "is_qualified": True,
        "total_capital_usdc": total_capital_usdc,
        "avg_conviction_ratio": avg_conviction_ratio,
    }
    await redis.set(RedisKeys.wallet_data(wallet_address), json.dumps(data))


async def set_market_redis_data(
    redis: Redis,
    *,
    market_id: str = "market_001",
    volume_24h: float = 500_000.0,
    liquidity: float = 100_000.0,
    spread: float = 0.02,
    participants: int = 50,
    days_to_resolution: int | None = 30,
    last_updated_ms: int | None = None,
) -> None:
    """
    Write market state to fakeredis as CLOBMarketFeed would.

    All Gate 1 thresholds default to well-above-minimum values so individual
    tests only need to override the field under test.
    """
    ts = last_updated_ms or int(time.time() * 1000)
    await redis.set(RedisKeys.market_last_updated_ms(market_id), str(ts))
    await redis.set(RedisKeys.market_volume_24h(market_id), str(volume_24h))
    await redis.set(RedisKeys.market_liquidity(market_id), str(liquidity))
    await redis.set(RedisKeys.market_spread(market_id), str(spread))
    await redis.set(RedisKeys.market_participants(market_id), str(participants))
    if days_to_resolution is not None:
        await redis.set(RedisKeys.market_days_to_resolution(market_id), str(days_to_resolution))
    else:
        # Mirrors CLOBMarketFeed writing "" when days_to_resolution is None
        await redis.set(RedisKeys.market_days_to_resolution(market_id), "")


async def insert_trade_record(
    session: AsyncSession,
    *,
    wallet_address: str = "0xWHALE001",
    market_id: str = "market_001",
    outcome: str = "YES",
    size_usdc: float = 1_000.0,
    tx_hash: str = "0xtx_db_001",
    traded_at: datetime | None = None,
) -> Trade:
    """
    Insert a Trade record into the test DB. Used by Gate 2/3 behavioral tests.
    Flushes immediately so the record is visible within the same session.
    """
    trade = Trade(
        wallet_address=wallet_address,
        market_id=market_id,
        outcome=outcome,
        size_usdc=size_usdc,
        traded_at=traded_at or datetime.now(tz=timezone.utc),
        tx_hash=tx_hash,
        block_number=12_345,
        market_price_at_trade=0.65,
    )
    session.add(trade)
    await session.flush()
    return trade
