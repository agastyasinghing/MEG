"""
Async SQLAlchemy engine and session factory for MEG.

Usage pattern (everywhere in the codebase):

    from meg.db.session import get_session

    async with get_session() as session:
        session.add(some_orm_object)
    # Commits on clean exit. Rolls back automatically on exception.

Startup (called once in main entrypoint):

    from meg.db.session import init_db
    await init_db(os.environ["DATABASE_URL"])

Design decisions:
  - Single module-level engine (_engine), created once at startup.
  - get_session() is an async context manager — explicit, no hidden DI.
  - Works identically in asyncio background tasks AND FastAPI route handlers.
    FastAPI handlers can wrap get_session() in a Depends() adapter if preferred;
    background tasks call it directly. One pattern for both.
  - session.begin() auto-commits on __aexit__ and auto-rollbacks on exception.
    Callers never need to call session.commit() or session.rollback() manually.

Session lifecycle:
    ┌──────────────────────────────────────────────┐
    │ async with get_session() as session:         │
    │   session.add(obj)           ← writes staged │
    │   result = await session.   ← reads OK       │
    │       execute(stmt)                          │
    │   # ... no explicit commit needed            │
    └──────────┬───────────────────────────────────┘
               │ exit without exception → COMMIT
               │ exit with exception    → ROLLBACK
               ▼
         Connection returned to pool
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

import structlog

# Use structlog directly — meg.core.logger is implemented at data_layer phase.
# structlog.get_logger() works without explicit configuration (uses default processors).
logger = structlog.get_logger(__name__)

# Module-level engine — None until init_db() is called.
# Never access directly outside this module.
_engine: AsyncEngine | None = None


async def init_db(database_url: str) -> None:
    """
    Create the async engine. Call once at application startup before any
    get_session() calls. Idempotent — safe to call again with the same URL
    (reinitializes engine; existing sessions using the old engine continue
    until they naturally close).

    Args:
        database_url: asyncpg connection URL, e.g.:
            "postgresql+asyncpg://user:pass@host:5432/dbname"
    """
    global _engine
    _engine = create_async_engine(
        database_url,
        echo=False,          # Set True temporarily for SQL query debugging
        pool_pre_ping=True,  # Detect stale connections before use
        pool_size=10,
        max_overflow=20,
    )
    logger.info("db_engine_initialized", url=_redact_url(database_url))


async def close_db() -> None:
    """
    Dispose the engine and close all pooled connections.
    Call at application shutdown to allow clean process exit.
    """
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        logger.info("db_engine_closed")


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an AsyncSession with an open transaction.

    Commits on clean exit. Rolls back on any exception — the exception
    is re-raised after rollback, never swallowed.

    Raises:
        RuntimeError: if called before init_db().
    """
    if _engine is None:
        raise RuntimeError(
            "Database engine not initialized. "
            "Call await init_db(database_url) before using get_session()."
        )
    async with AsyncSession(_engine) as session:
        async with session.begin():
            yield session


def _redact_url(url: str) -> str:
    """Replace password in DB URL with *** for safe logging."""
    try:
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(url)
        if parsed.password:
            redacted = parsed._replace(
                netloc=parsed.netloc.replace(parsed.password, "***")
            )
            return urlunparse(redacted)
    except Exception:
        pass
    return url
