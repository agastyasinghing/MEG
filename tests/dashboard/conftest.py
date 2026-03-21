"""
Dashboard API test fixtures.

Uses:
  - fakeredis.aioredis.FakeRedis  — no real Redis required
  - SQLite in-memory via aiosqlite + StaticPool — no real PostgreSQL required
    StaticPool forces all sessions to share a single connection, so seeded
    data is immediately visible to subsequent sessions in the same test.

JSONB columns (SignalOutcome.scores_json, Wallet.category_scores, etc.) are
handled by the @compiles shim below. The ORM stores/reads them as SQLite JSON
text. Our API responses don't include those fields, so no deserialization issue.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

import fakeredis.aioredis
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.pool import StaticPool

from meg.dashboard.api.main import app, db_session, get_redis
from meg.db.models import Base


# ── SQLite JSONB shim — same pattern as tests/agent_core/conftest.py ─────────

@compiles(JSONB, "sqlite")
def _compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def fake_redis() -> AsyncGenerator[Redis, None]:
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    yield client
    await client.aclose()


@pytest_asyncio.fixture
async def db_engine():
    """SQLite in-memory engine shared across all sessions in a test via StaticPool."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def api_client(fake_redis, db_engine) -> AsyncGenerator[AsyncClient, None]:
    """
    httpx AsyncClient wired to the FastAPI app with dependencies overridden:
      - get_redis()  → FakeRedis
      - db_session() → AsyncSession on the test SQLite engine
    """
    app.dependency_overrides[get_redis] = lambda: fake_redis

    async def _db_override() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSession(db_engine, expire_on_commit=False) as session:
            async with session.begin():
                yield session

    app.dependency_overrides[db_session] = _db_override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
