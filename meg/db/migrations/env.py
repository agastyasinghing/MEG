"""
Alembic migration environment for MEG.

Uses async SQLAlchemy (asyncpg driver) to match the application's runtime
engine. DATABASE_URL is read from the environment — never hardcoded here.

Running migrations:
    export DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/meg
    alembic upgrade head

Generating a new migration after editing models.py:
    alembic revision --autogenerate -m "your description"
    # Review the generated file in meg/db/migrations/versions/ before applying.

CI drift check (TODO: add to CI pipeline):
    alembic check   # exits non-zero if models.py has drifted from migrations
"""
from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Import Base so autogenerate can detect model changes.
# IMPORTANT: importing Base also imports all model classes via their module-level
# definitions — models.py must be importable at migration time.
from meg.db.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _get_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Set it before running alembic commands:\n"
            "  export DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/meg"
        )
    return url


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode (no live DB connection needed).
    Generates SQL script output instead of executing against the DB.
    Useful for reviewing what will run before applying.
    """
    context.configure(
        url=_get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode against a live database.
    Uses async engine to match the application runtime.
    """
    connectable = create_async_engine(_get_url(), poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
