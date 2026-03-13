"""
SQLAlchemy ORM models for MEG's PostgreSQL database.

Tables:
  wallets          — tracked whale wallets and their metadata
  wallet_scores    — time-series of wallet scores (for reputation decay)
  trades           — all whale trades observed (raw + qualified)
  signal_outcomes  — every signal event, FILTERED or EXECUTED (training data moat)
  whale_trap_events — detected pump-and-exit patterns for model training

Alembic manages schema migrations. Run `alembic upgrade head` to apply.
Do not alter table definitions here without creating a corresponding migration.
"""
from __future__ import annotations

raise NotImplementedError(
    "meg.db.models: implement at DB schema phase (phase 2). "
    "Run: alembic init meg/db/migrations"
)
