"""
Agent core test fixtures and factory helpers.

DB fixtures (db_engine, db_session) use SQLite in-memory via aiosqlite for
fast local testing. Agent core tests need Trade, WhaleTrapEvent, Position,
and SignalOutcome tables.

Note: SQLite doesn't support JSONB — tests that need JSONB columns
(SignalOutcome.scores_json, Position.contributing_wallets) use dict defaults
that SQLite stores as TEXT. This is acceptable for logic testing.
Real PG catches type edge cases — see TODOS.md: shared test fixture dedup.

Factory helpers create test objects with sensible defaults. Override fields
as needed per test case.
"""
from __future__ import annotations

import json
import time
import uuid

import fakeredis.aioredis
import pytest
import pytest_asyncio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import JSONB

from meg.core.config_loader import MegConfig


# ── SQLite JSONB compatibility ────────────────────────────────────────────
# SQLite has no JSONB type. Register a compiler that emits JSON instead.
# This lets us create SignalOutcome, Position tables in SQLite for testing.

@compiles(JSONB, "sqlite")
def _compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"
from meg.core.events import (
    PositionState,
    RedisKeys,
    SignalEvent,
    SignalScores,
)
from meg.db.models import (
    Base,
    Position,
    PositionStatus,
    SignalOutcome,
    Trade,
    Wallet,
    WhaleTrapEvent,
)


# ── DB fixtures ───────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def db_engine() -> AsyncEngine:
    """
    SQLite in-memory engine for agent_core tests.
    Creates Trade, WhaleTrapEvent, Position, and SignalOutcome tables.
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        # Wallet table must be created first — WhaleTrapEvent has FK to wallets.address
        await conn.run_sync(Wallet.__table__.create)
        await conn.run_sync(Trade.__table__.create)
        await conn.run_sync(WhaleTrapEvent.__table__.create)
        await conn.run_sync(Position.__table__.create)
        await conn.run_sync(SignalOutcome.__table__.create)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SignalOutcome.__table__.drop)
        await conn.run_sync(Position.__table__.drop)
        await conn.run_sync(WhaleTrapEvent.__table__.drop)
        await conn.run_sync(Trade.__table__.drop)
        await conn.run_sync(Wallet.__table__.drop)
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


# ── Redis fixture ─────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def mock_redis() -> Redis:
    """Fakeredis instance — in-memory, no real Redis needed."""
    return fakeredis.aioredis.FakeRedis()


# ── Config fixture ────────────────────────────────────────────────────────


@pytest.fixture
def test_config() -> MegConfig:
    """Default MegConfig with sensible test values."""
    return MegConfig()


# ── Factory helpers ───────────────────────────────────────────────────────


def make_signal_event(
    *,
    signal_id: str | None = None,
    market_id: str = "market_001",
    outcome: str = "YES",
    composite_score: float = 0.65,
    recommended_size_usdc: float = 50.0,
    kelly_fraction: float = 0.25,
    ttl_expires_at_ms: int | None = None,
    status: str = "PENDING",
    triggering_wallet: str = "0xWHALE001",
    contributing_wallets: list[str] | None = None,
    market_price_at_signal: float = 0.55,
    whale_archetype: str = "INFORMATION",
    is_contrarian: bool = False,
    trap_warning: bool = False,
    saturation_score: float = 0.0,
) -> SignalEvent:
    """Return a SignalEvent with sensible defaults. Override as needed."""
    return SignalEvent(
        signal_id=signal_id or f"sig_{uuid.uuid4().hex[:8]}",
        market_id=market_id,
        outcome=outcome,
        composite_score=composite_score,
        scores=SignalScores(
            lead_lag=0.6,
            consensus=0.5,
            kelly_confidence=0.7,
            divergence=0.4,
            conviction_ratio=0.5,
            archetype_multiplier=1.0,
            ladder_multiplier=1.0,
        ),
        recommended_size_usdc=recommended_size_usdc,
        kelly_fraction=kelly_fraction,
        ttl_expires_at_ms=ttl_expires_at_ms or int(time.time() * 1000) + 7_200_000,
        status=status,
        triggering_wallet=triggering_wallet,
        contributing_wallets=contributing_wallets or [triggering_wallet],
        market_price_at_signal=market_price_at_signal,
        whale_archetype=whale_archetype,
        is_contrarian=is_contrarian,
        trap_warning=trap_warning,
        saturation_score=saturation_score,
    )


def make_position_state(
    *,
    position_id: str | None = None,
    market_id: str = "market_001",
    outcome: str = "YES",
    entry_price: float = 0.50,
    current_price: float = 0.55,
    size_usdc: float = 100.0,
    entry_signal_id: str = "sig_test001",
    take_profit_price: float = 0.70,
    stop_loss_price: float = 0.375,
    contributing_wallets: list[str] | None = None,
) -> PositionState:
    """Return a PositionState with sensible defaults."""
    return PositionState(
        position_id=position_id or f"pos_{uuid.uuid4().hex[:8]}",
        market_id=market_id,
        outcome=outcome,
        entry_price=entry_price,
        current_price=current_price,
        size_usdc=size_usdc,
        shares=size_usdc / entry_price if entry_price > 0 else 0.0,
        entry_signal_id=entry_signal_id,
        contributing_wallets=contributing_wallets or ["0xWHALE001"],
        whale_archetype="INFORMATION",
        opened_at_ms=int(time.time() * 1000),
        take_profit_price=take_profit_price,
        stop_loss_price=stop_loss_price,
        status="OPEN",
    )


async def set_market_redis_data(
    redis: Redis,
    *,
    market_id: str = "market_001",
    mid_price: float = 0.55,
    liquidity: float = 100_000.0,
    volume_24h: float = 500_000.0,
) -> None:
    """Write market state to fakeredis as CLOBMarketFeed would."""
    await redis.set(RedisKeys.market_mid_price(market_id), str(mid_price))
    await redis.set(RedisKeys.market_liquidity(market_id), str(liquidity))
    await redis.set(RedisKeys.market_volume_24h(market_id), str(volume_24h))


async def add_position_to_redis(
    redis: Redis,
    pos: PositionState,
) -> None:
    """Add a PositionState to the open_positions Redis hash."""
    pos_json = pos.model_dump_json()
    await redis.hset(RedisKeys.open_positions(), pos.position_id, pos_json)
    await redis.set(RedisKeys.position(pos.position_id), pos_json)


async def insert_trade_record(
    session: AsyncSession,
    *,
    wallet_address: str = "0xWHALE001",
    market_id: str = "market_001",
    outcome: str = "YES",
    size_usdc: float = 1_000.0,
    tx_hash: str | None = None,
    traded_at=None,
) -> Trade:
    """Insert a Trade record into the test DB."""
    from datetime import datetime, timezone

    trade = Trade(
        wallet_address=wallet_address,
        market_id=market_id,
        outcome=outcome,
        size_usdc=size_usdc,
        traded_at=traded_at or datetime.now(tz=timezone.utc),
        tx_hash=tx_hash or f"0xtx_{uuid.uuid4().hex[:8]}",
        block_number=12_345,
        market_price_at_trade=0.65,
    )
    session.add(trade)
    await session.flush()
    return trade


async def insert_wallet(
    session: AsyncSession,
    *,
    address: str = "0xWHALE001",
    archetype: str = "INFORMATION",
) -> Wallet:
    """Insert a Wallet record — needed for WhaleTrapEvent FK."""
    from meg.db.models import WhaleArchetype
    wallet = Wallet(
        address=address,
        archetype=archetype,
        is_qualified=True,
        composite_whale_score=0.75,
        win_rate=0.65,
        avg_lead_time_hours=4.0,
        roi_30d=0.10,
        roi_90d=0.15,
        roi_all_time=0.20,
        total_closed_positions=100,
        consistency_score=0.70,
        avg_conviction_ratio=0.05,
        reputation_decay_factor=1.0,
        category_scores={},
    )
    session.add(wallet)
    await session.flush()
    return wallet


async def insert_signal_outcome(
    session: AsyncSession,
    *,
    signal_id: str = "sig_test001",
    market_id: str = "market_001",
    outcome: str = "YES",
    composite_score: float = 0.65,
    status: str = "PENDING",
) -> SignalOutcome:
    """Insert a SignalOutcome record for testing status updates."""
    so = SignalOutcome(
        signal_id=signal_id,
        market_id=market_id,
        outcome=outcome,
        composite_score=composite_score,
        recommended_size_usdc=50.0,
        kelly_fraction=0.25,
        scores_json={
            "lead_lag": 0.6,
            "consensus": 0.5,
            "kelly_confidence": 0.7,
            "divergence": 0.4,
            "conviction_ratio": 0.5,
            "archetype_multiplier": 1.0,
            "ladder_multiplier": 1.0,
        },
        status=status,
        triggering_wallet="0xWHALE001",
        contributing_wallets=["0xWHALE001"],
        market_price_at_signal=0.55,
    )
    session.add(so)
    await session.flush()
    return so
