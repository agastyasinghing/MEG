"""
Signal engine test fixtures and factory helpers.

DB fixtures (db_engine, db_session) use SQLite in-memory for fast local
tests. ladder_detector queries only the Trade table, which has no JSONB
columns — SQLite handles it correctly.

Redis: use the root-level mock_redis fixture (fakeredis, shared by all layers).

sample_wallet_data (make_wallet_data) is the canonical dict shape returned by
wallet_registry and consumed by lead_lag_scorer and conviction_ratio.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade
from meg.db.models import Trade


# ── DB fixtures ─────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def db_engine() -> AsyncEngine:
    """
    SQLite in-memory engine for ladder_detector DB tests.
    Creates only the Trade table (no JSONB columns — SQLite compatible).
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
    Yield a fresh session per test. Always rolls back — no data bleeds between tests.
    """
    async with AsyncSession(db_engine) as session:
        await session.begin()
        try:
            yield session
        finally:
            await session.rollback()


# ── Config fixture ────────────────────────────────────────────────────────────


import pytest


@pytest.fixture
def test_config() -> MegConfig:
    """
    MegConfig with Pydantic defaults. All signal engine tests use this.
    Override individual sub-fields in tests as needed:
        test_config.signal.lead_lag_min_gate = 0.50
    The root conftest also provides test_config — this local version shadows
    it for signal_engine tests so we can extend it if needed in future.
    """
    return MegConfig()


# ── Factory helpers ──────────────────────────────────────────────────────────


def make_qualified_trade(
    *,
    wallet_address: str = "0xWHALE001",
    market_id: str = "market_001",
    outcome: str = "YES",
    size_usdc: float = 2_000.0,
    timestamp_ms: int | None = None,
    tx_hash: str = "0xtx001",
    block_number: int = 12_345,
    market_price_at_trade: float = 0.60,
    whale_score: float = 0.75,
    archetype: str = "INFORMATION",
    intent: str = "SIGNAL",
    market_category: str = "politics",
) -> QualifiedWhaleTrade:
    """Return a QualifiedWhaleTrade with sensible defaults. Override as needed."""
    return QualifiedWhaleTrade(
        wallet_address=wallet_address,
        market_id=market_id,
        outcome=outcome,
        size_usdc=size_usdc,
        timestamp_ms=timestamp_ms or int(datetime.now(tz=timezone.utc).timestamp() * 1000),
        tx_hash=tx_hash,
        block_number=block_number,
        market_price_at_trade=market_price_at_trade,
        whale_score=whale_score,
        archetype=archetype,
        intent=intent,
        market_category=market_category,
    )


def make_wallet_data(
    *,
    address: str = "0xWHALE001",
    archetype: str = "INFORMATION",
    composite_whale_score: float = 0.75,
    win_rate: float = 0.62,
    avg_lead_time_hours: float = 6.0,
    total_capital_usdc: float | None = 50_000.0,
    total_volume_usdc: float = 200_000.0,
    avg_conviction_ratio: float = 0.05,
    last_profitable_trade_at: str | None = "2026-02-14T00:00:00+00:00",
    reputation_decay_factor: float = 0.95,
    is_qualified: bool = True,
) -> dict:
    """
    Return the wallet_data dict shape written by wallet_registry dual-write
    and consumed by lead_lag_scorer.score() and conviction_ratio.score().

    last_profitable_trade_at: ISO string or None. None triggers decay_factor=1.0
    (no decay) in lead_lag_scorer.compute_reputation_decay().
    """
    return {
        "address": address,
        "archetype": archetype,
        "composite_whale_score": composite_whale_score,
        "win_rate": win_rate,
        "avg_lead_time_hours": avg_lead_time_hours,
        "total_capital_usdc": total_capital_usdc,
        "total_volume_usdc": total_volume_usdc,
        "avg_conviction_ratio": avg_conviction_ratio,
        "last_profitable_trade_at": last_profitable_trade_at,
        "reputation_decay_factor": reputation_decay_factor,
        "is_qualified": is_qualified,
    }


async def insert_trade(
    session: AsyncSession,
    *,
    wallet_address: str = "0xWHALE001",
    market_id: str = "market_001",
    outcome: str = "YES",
    size_usdc: float = 2_000.0,
    tx_hash: str = "0xtx_db_001",
    traded_at: datetime | None = None,
    is_qualified: bool = True,
) -> Trade:
    """
    Insert a qualified Trade record. Used by ladder_detector DB tests.
    Flushes immediately so the record is visible in the same session.
    """
    trade = Trade(
        wallet_address=wallet_address,
        market_id=market_id,
        outcome=outcome,
        size_usdc=size_usdc,
        traded_at=traded_at or datetime.now(tz=timezone.utc),
        tx_hash=tx_hash,
        block_number=12_345,
        market_price_at_trade=0.60,
        is_qualified=is_qualified,
    )
    session.add(trade)
    await session.flush()
    return trade
