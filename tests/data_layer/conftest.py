"""
DB fixtures for data_layer tests.

Mirrors tests/db/conftest.py — wallet_registry tests need a real PostgreSQL
instance (not mocked) because they test FK constraints, UPSERT behavior,
and ORM-to-DB round-trips.

Uses pytest-postgresql to spin up a real temporary PostgreSQL instance.
Session scope: one engine per test session, one fresh schema per test function.
"""
from __future__ import annotations

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from meg.db.models import Base
from meg.db.session import init_db, close_db


@pytest_asyncio.fixture(scope="session")
async def db_engine(postgresql) -> AsyncEngine:
    """
    Spin up a real PostgreSQL instance via pytest-postgresql.
    Creates all tables from Base.metadata. Tears down after test session.
    """
    info = postgresql.info
    url = (
        f"postgresql+asyncpg://{info.user}:@{info.host}:{info.port}/{info.dbname}"
    )
    await init_db(url)

    from meg.db.session import _engine
    engine = _engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await close_db()


@pytest_asyncio.fixture
async def db_session(db_engine: AsyncEngine) -> AsyncSession:
    """
    Yield a fresh session for each test. Rolls back after the test so
    each test starts with a clean slate — no data bleeds between tests.
    """
    async with AsyncSession(db_engine) as session:
        await session.begin()
        try:
            yield session
        finally:
            await session.rollback()
