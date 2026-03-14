# MEG — Session Status
> Update this file at the end of every Claude Code session. Read it at the start of every session.
> Last updated: 2026-03-13

---

## Current Phase
- [x] Repo scaffolding — **COMPLETE** (merged: feat/repo-scaffold, v0.1.0.0)
- [~] DB schema — **BUILT, needs /review + /ship**
- [ ] Data Layer
- [ ] Pre-Filter Gates
- [ ] Signal Engine
- [ ] Agent Core
- [ ] Execution Layer
- [ ] Telegram Bot
- [ ] Dashboard
- [ ] Bootstrap script

**Active phase:** DB schema

---

## What Was Just Completed

- Full repo scaffold built, reviewed, and merged (v0.1.0.0)
  - `meg/` package + `pyproject.toml`, all 5 layer stub trees, `meg/core/` kernel
  - `meg/core/events.py`: full Pydantic schemas + `RedisKeys`
  - `meg/core/config_loader.py`: `MegConfig` model + `ConfigLoader` stub (watchdog hot-reload)
  - `docker-compose.yml` with profiles, `config/config.yaml` full schema, `requirements.txt`
  - `tests/conftest.py`, `.gitignore`, `.env.example`, `TODOS.md`, `VERSION`, `CHANGELOG.md`
- `/plan-ceo-review`, `/plan-eng-review` (14 decisions locked)
- `/review` (3 informational issues found and fixed)
- `/ship` (PR created, merged)

**DB schema phase (2026-03-13):**
- `meg/core/events.py` — aligned with PRD §12: `SignalScores` model added, `SignalEvent`
  updated (+12 fields), `source_wallet_addresses` → `contributing_wallets`, `SIGNAL_LADDER` added
- `meg/db/models.py` — 6 tables: `wallets`, `trades`, `wallet_scores`, `signal_outcomes`,
  `whale_trap_events`, `positions`. Full index strategy, VARCHAR enums, JSONB sub-scores.
- `meg/db/session.py` — `init_db()` + `get_session()` async context manager
- `meg/db/migrations/env.py` — async Alembic env, DATABASE_URL from env
- `alembic.ini` — ruff post-write hooks, URL via env var
- `meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py` — initial migration
- `tests/db/conftest.py` — pytest-postgresql fixtures
- `tests/db/test_models.py` — 15 tests covering all tables + session + events.py alignment
- `requirements-dev.txt` — added pytest-postgresql==5.0.0
- `TODOS.md` — 3 new items (score retention, alembic CI check, PnL backfill job)

---

## In Progress

- DB schema built — ready for `/review` then `/ship`

---

## Known Broken / Blocked

- None

---

## Next 3 Tasks

1. **Run `/review` on DB schema** — paranoid staff engineer review before shipping.
2. **Run `/ship`** — sync main, test, push, PR for DB schema phase.
3. **Start Data Layer** — `meg/data_layer/polygon_feed.py`, CLOB client, wallet registry CRUD.

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-13 | 6 tables (added `positions`) | PRD §12 defines it; deferring would require mid-build migration |
| 2026-03-13 | Soft FK on `trades.wallet_address` | Feed must never crash on unregistered wallets |
| 2026-03-13 | JSONB `scores_json` for signal sub-scores | New signal modules add keys, not columns — zero migration cost |
| 2026-03-13 | `get_session()` async context manager in `session.py` | One pattern works in both asyncio tasks and FastAPI handlers |
| 2026-03-13 | PRD §12 as schema authority; `events.py` updated to match | One source of truth; ORM and Redis events agree on all field names |
| 2026-03-13 | VARCHAR enums via `SAEnum(native_enum=False)` | Adding new status values requires no `ALTER TYPE` migration |
| 2026-03-13 | wallet_scores retention deferred to v1.5 | 730k rows/year is acceptable for v1; see TODOS.md |
| 2026-03-13 | pytest-postgresql for DB tests (real PG, no mocking) | JSONB, FK constraints, UniqueConstraint all need a real DB to test |
| 2026-03-12 | Package: `meg/` at root + `pyproject.toml` + `pip install -e .` | Clean import paths, no PYTHONPATH hacks, modern Python standard |
| 2026-03-12 | Python 3.11 locked via `.python-version` + `pyproject.toml` + Dockerfile | Three sources agree, no accidental version drift |
| 2026-03-12 | Shared kernel at `meg/core/`: redis_client, logger, events, config_loader | Single import boundary, no circular deps, fully testable |
| 2026-03-12 | `meg/db/` inside meg/ package (not at repo root) | Consistent import paths: `from meg.db.models import Wallet` |
| 2026-03-12 | `config/config.yaml`: full schema at scaffold time (all known params) | Every module can read config from day 1 without editing the schema |
| 2026-03-12 | `meg/core/events.py`: full Pydantic schemas (RawWhaleTrade, QualifiedWhaleTrade, SignalEvent) + RedisKeys class | Defines inter-layer contract upfront; key strings never duplicated |
| 2026-03-12 | Config hot-reload: `watchdog` file watcher + Pydantic validation + last-good-config fallback | Reactive, sub-second, safe on partial writes |
| 2026-03-12 | Redis: injected async factory (`create_redis_client(url)`), no global state | Fully testable, explicit, no hidden imports |
| 2026-03-12 | Logger: `structlog`, `get_logger(__name__)` per module, JSON output | Async-safe, structured, trivially parseable by any log aggregator |
| 2026-03-12 | Stubs: `raise NotImplementedError('module.function')` — no bare `pass` or `...` | Explicit failures in tracebacks; impossible to accidentally call silently |
| 2026-03-12 | Docker: single `docker-compose.yml` with profiles (infra / bot / dashboard / all) | One file, full flexibility — devs can run only Redis+Postgres locally |
| 2026-03-12 | `requirements.txt`: exact pins (`==`); `requirements-dev.txt` for dev/test deps | Reproducible builds, no silent dep upgrades in a trading bot |
| 2026-03-12 | `tests/conftest.py`: `asyncio_mode=auto`, `mock_redis` (fakeredis), `test_config` stub | First test written can run immediately without hitting real Redis |
| 2026-03-12 | Design constraint: `subscribe()` disconnect must not be silent — re-raise or sentinel | Prevents silent event loss in the pub/sub pipeline |

---

## Open Questions Resolved

| OQ ID | Resolution | Date |
|-------|-----------|------|
| — | — | — |

---

## Test Coverage

| Module | Tests Written | Passing |
|--------|--------------|---------|
| — | No | — |

---

## TODOS.md Items

| Item | Priority | Blocked by |
|------|----------|-----------|
| pip-audit in CI (dep vuln scanning) | P2 | CI pipeline (post-dashboard) |

---

## Notes for Next Session

- Scaffold is merged and on main — pull main before starting DB schema work
- DB schema phase: run `/plan-ceo-review` first, then `/plan-eng-review`, then build
- `meg/db/models.py` is currently a stub with `raise NotImplementedError` — replace it entirely
- Alembic has NOT been initialized yet — run `alembic init meg/db/migrations` as first step
- 5 tables to design: `wallets`, `trades`, `wallet_scores`, `whale_trap_events`, `signal_outcomes`
- Use async SQLAlchemy (`asyncpg` driver) — `asyncpg` is already pinned in `requirements.txt`
- Check `MEG_PRD_v3_final.md` for any column-level detail on these tables before designing schema
