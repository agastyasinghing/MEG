"""
DB-layer test fixtures.

Uses pytest-postgresql to spin up a real temporary PostgreSQL instance.
All tests in tests/db/ run against a real DB — no mocking. This ensures:
  - JSONB columns serialize/deserialize correctly
  - FK constraints (wallet_scores → wallets) are actually enforced
  - UniqueConstraint (trades.tx_hash) is enforced at DB level
  - Enum values are validated and stored correctly

Session scope: one engine per test session, one fresh schema per test function.
"""
from __future__ import annotations

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from meg.db.models import Base
from meg.db.session import init_db, close_db, get_session


@pytest_asyncio.fixture(scope="session")
async def db_engine(postgresql) -> AsyncEngine:
    """
    Spin up a real PostgreSQL instance via pytest-postgresql.
    Create all tables from Base.metadata. Tear down after test session.

    'postgresql' fixture is provided by pytest-postgresql and gives us
    a real PG process with a temporary database — no Docker needed locally
    if pytest-postgresql is configured with an existing PG installation,
    or it can manage its own PG process.
    """
    info = postgresql.info
    url = (
        f"postgresql+asyncpg://{info.user}:@{info.host}:{info.port}/{info.dbname}"
    )
    await init_db(url)

    # Import engine from session module after init_db sets it
    from meg.db.session import _engine
    engine = _engine

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Teardown
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await close_db()


@pytest_asyncio.fixture
async def db_session(db_engine: AsyncEngine) -> AsyncSession:
    """
    Yield a fresh session for each test. Rolls back after the test so
    each test starts with a clean slate — no data bleeds between tests.

    Uses begin()/rollback() directly (not the context manager form of begin())
    so the explicit rollback in finally doesn't collide with an implicit commit
    on context manager exit.
    """
    async with AsyncSession(db_engine) as session:
        await session.begin()
        try:
            yield session
        finally:
            await session.rollback()
