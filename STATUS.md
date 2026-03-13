# MEG — Session Status
> Update this file at the end of every Claude Code session. Read it at the start of every session.
> Last updated: 2026-03-12

---

## Current Phase
- [~] Repo scaffolding — **PLANNED, READY TO BUILD**
- [ ] DB schema
- [ ] Data Layer
- [ ] Pre-Filter Gates
- [ ] Signal Engine
- [ ] Agent Core
- [ ] Execution Layer
- [ ] Telegram Bot
- [ ] Dashboard
- [ ] Bootstrap script

**Active phase:** Repo scaffolding

---

## What Was Just Completed

- `/plan-ceo-review` — full CEO-mode review of scaffold plan; 3 foundational decisions made
- `/plan-eng-review` — full eng review; 10 issues resolved, plan locked, 0 critical gaps

---

## In Progress

- Nothing yet — plan complete, implementation not started

---

## Known Broken / Blocked

- None

---

## Next 3 Tasks

1. **Build the full scaffold** — create all folders, REAL files, STUB files, and MARKER `__init__.py` files exactly per the locked plan (see Decisions Log below)
2. **Run `/review`** on the scaffold — staff-engineer-level review before committing
3. **Run `/ship`** — commit and push the scaffold as the first real code commit

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
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

- Planning is complete — go straight to building the scaffold (Task 1 above)
- All decisions are locked in the Decisions Log — do not re-litigate
- REAL files to write: `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`, `docker-compose.yml`, `.env.example`, `config/config.yaml`, `tests/conftest.py`, `.gitignore`, `.python-version`, `meg/core/events.py` (full schemas), `meg/core/redis_client.py` (stubs), `meg/core/logger.py` (stub), `meg/core/config_loader.py` (stub)
- STUB files: all layer modules (`polygon_feed.py`, etc.) — docstring + typed sigs + `raise NotImplementedError`
- MARKER files: `__init__.py` in every package directory
- After scaffold is built: run `/review` before `/ship`
