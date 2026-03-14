# Changelog

All notable changes to MEG (Megalodon) are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.1.0] - 2026-03-13

### Added
- `meg/db/models.py` — 6 SQLAlchemy 2.0 ORM tables: `wallets`, `trades`, `wallet_scores`,
  `signal_outcomes`, `whale_trap_events`, `positions`. Full index strategy locked at schema
  time (leaderboard, score history, signal log, market activity, tx dedup). VARCHAR enums
  via `SAEnum(native_enum=False)` for zero-migration status additions. JSONB for signal
  sub-scores and JSONB for list fields (contributing wallets, category scores).
- `meg/db/session.py` — `init_db(url)` async engine factory + `get_session()` async context
  manager. Explicit `RuntimeError` guard if called before `init_db()`. Auto-commit on clean
  exit, auto-rollback on exception. One pattern works for both asyncio background tasks and
  FastAPI route handlers.
- `meg/db/migrations/` — Alembic initialized with async `env.py` (asyncpg driver, `DATABASE_URL`
  from environment). Initial migration `42acac652ac5` creates all 6 tables with full indexes.
  `alembic.ini` configured with ruff post-write hooks.
- `tests/db/` — 18 tests: 6 pure-Python (Pydantic validation, session guard) pass now;
  12 DB-level tests (table constraints, FK enforcement, JSONB round-trips) run with
  `pytest-postgresql` + live PostgreSQL. `pytest-postgresql==5.0.0` added to `requirements-dev.txt`.
- `TODOS.md` — 3 new deferred items: wallet_scores retention policy (P2), Alembic drift
  check in CI (P1), resolved_pnl_usdc backfill job (P1).

### Changed
- `meg/core/events.py` — aligned with PRD §12 as authoritative source of truth. `SignalScores`
  model added (7 sub-scores with `ge`/`le` Pydantic constraints). `SignalEvent` updated with
  12 new fields (`scores`, `triggering_wallet`, `is_contrarian`, `is_ladder`, `trap_warning`,
  etc.). `source_wallet_addresses` renamed to `contributing_wallets`. `SIGNAL_LADDER` added
  to `Intent` literal. Shared type aliases extracted (`Outcome`, `Archetype`, `Intent`,
  `SignalStatus`).

### Fixed
- `meg/db/models.py` — `_utcnow()` now returns timezone-aware datetime
  (`datetime.now(tz=timezone.utc)`) instead of naive `datetime.utcnow()`, which asyncpg
  rejects for TIMESTAMPTZ columns at runtime.

## [0.1.0.0] - 2026-03-13

### Added
- Full repo scaffold: `meg/` Python package at root with `pip install -e .` via `pyproject.toml`
- `meg/core/` shared kernel: `events.py` (full Pydantic schemas for `RawWhaleTrade`,
  `QualifiedWhaleTrade`, `SignalEvent`, `TradeProposal`, and `RedisKeys` constants),
  `config_loader.py` (hot-reloadable YAML config via watchdog + `MegConfig` Pydantic model),
  `redis_client.py` (injected async factory, no global state), `logger.py` (structlog JSON)
- Complete stub tree for all 5 layers: `meg/data_layer/`, `meg/pre_filter/`,
  `meg/signal_engine/`, `meg/agent_core/`, `meg/execution/` — typed signatures +
  `raise NotImplementedError` throughout; no bare `pass`
- `meg/db/` inside the package for consistent import paths (`from meg.db.models import ...`)
- `meg/telegram/bot.py` and `meg/dashboard/` stubs
- `docker-compose.yml` with profiles: `infra` (Postgres + Redis), `bot`, `dashboard`, `all`
- `config/config.yaml`: full schema with all known parameters (whale qualification, signal,
  risk, Kelly, entry, pre-filter, signal decay, reputation, logging)
- `.env.example`: all required environment variables documented
- `requirements.txt` (exact pins) and `requirements-dev.txt` (dev/test deps, split)
- `.python-version` pinning Python 3.11 for pyenv/mise
- `tests/conftest.py` with `asyncio_mode=auto`, `mock_redis` (fakeredis), `test_config` stub
- `tests/` mirror structure with `__init__.py` markers in every layer directory
- `TODOS.md` seeded with deferred items (pip-audit in CI, P2)
- `.gitignore` expanded to cover `.env`, `__pycache__`, venvs, pytest cache, mypy, ruff
