# MEG — Session Status
> Update this file at the end of every Claude Code session. Read it at the start of every session.
> Last updated: 2026-03-13

---

## Current Phase
- [x] Repo scaffolding — **COMPLETE** (merged: feat/repo-scaffold, v0.1.0.0)
- [x] DB schema — **COMPLETE** (merged: v0.1.1.0)
- [~] Data Layer — **BUILT, needs /review + /ship**
- [ ] Pre-Filter Gates
- [ ] Signal Engine
- [ ] Agent Core
- [ ] Execution Layer
- [ ] Telegram Bot
- [ ] Dashboard
- [ ] Bootstrap script

**Active phase:** Data Layer

---

## What Was Just Completed

**Data Layer phase (2026-03-13):**
- `meg/db/models.py` — Added 7 Wallet columns (total_volume_usdc, total_trades,
  total_capital_usdc, is_tracked, is_excluded, exclusion_reason, avg_hold_time_hours)
  and 9 Trade columns (market_category, lead_time_hours, exit/resolution fields, pnl,
  tx_hash_exit) + ix_trades_market_category index
- `meg/core/events.py` — Added `MarketState` Pydantic model; 10 new `RedisKeys` methods
  (market_bid/ask/volume_24h/participants/last_updated_ms/price_history,
  active_markets, last_processed_block, consensus_window, meg_config)
- `meg/core/redis_client.py` — Full implementation: create_redis_client (3-retry backoff),
  publish, subscribe (async generator, re-raises ConnectionError), close
- `meg/data_layer/polygon_feed.py` — Full implementation: PolygonRPCConnection ABC,
  Web3RPCConnection (polling), PolygonFeed (reconnect backoff, gap tracking, per-tx try/except)
- `meg/data_layer/clob_client.py` — CLOBMarketFeed: polls CLOB REST every 5s, all 8 market
  state Redis keys, price_history sorted set with ZREMRANGEBYSCORE; stubs kept intact
- `meg/data_layer/wallet_registry.py` — Full rewrite: dual-write, Redis-first cache (300s TTL),
  session injection, full CRUD suite (12 functions)
- `meg/data_layer/capital_refresh.py` — New: CapitalRefreshJob (daily USDC balance via RPC)
- `meg/db/migrations/versions/b4e2f9a1c3d7_add_wallet_capital_and_trade_metadata.py`
  — Alembic migration (revises 42acac652ac5) for all new wallet + trade columns
- `tests/data_layer/test_polygon_feed.py` — 18 tests (ABC, filter, error handling, gap detection)
- `tests/data_layer/test_clob_client.py` — 11 tests (all Redis keys, price trim, error isolation)
- `tests/data_layer/test_wallet_registry.py` — 19 tests (CRUD, cache, dual-write, exclusion)
- `TODOS.md` — 2 new items: gap-fill replay (P1), wallet auto-discovery (P2)

**DB schema phase (completed prior session, v0.1.1.0):**
- `meg/db/models.py` — 6 tables with full index strategy, VARCHAR enums, JSONB sub-scores
- `meg/db/session.py` — init_db() + get_session() async context manager
- `meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py` — initial migration

---

## In Progress

- Data Layer built — ready for `/review` then `/ship`

---

## Known Broken / Blocked

- `polygon_feed._filter_whale_transaction()` uses gas heuristics as size proxy;
  full CLOB ABI decoding (exact USDC, market_id, outcome from OrderFilled event) is TODO.
  All structural/architectural pieces are correct; values are placeholders.
- `capital_refresh._get_usdc_balance()` requires Alchemy RPC connection (production only).

---

## Next 3 Tasks

1. **Run `/review` on Data Layer** — paranoid staff engineer review before shipping.
2. **Run `/ship`** — sync main, test, push, PR for data layer phase.
3. **Start Pre-Filter Gates** — `market_quality.py`, `arbitrage_exclusion.py`, `intent_classifier.py`.

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-13 | polygon_feed uses gas heuristics until ABI decode ready | CLOB ABI decoding requires receipt parsing; scaffold is correct, values are placeholders |
| 2026-03-13 | CLOBMarketFeed uses httpx for REST polling | py-clob-client is for order placement; httpx for read-only REST is lighter |
| 2026-03-13 | Web3RPCConnection uses block polling (not eth_subscribe) | More reliable across provider restarts; websocket subscription is a later upgrade |
| 2026-03-13 | wallet_registry dual-write: DB first, then Redis | DB is authoritative; Redis failure logs warning and continues (cache can be rebuilt) |
| 2026-03-13 | Cache TTL = 300s for wallet data | Matches signal decay TTL; fresh enough for scores, long enough for latency budget |
| 2026-03-13 | Session injection (session: AsyncSession | None) | Tests inject rollback fixture; production uses get_session() internally |
| 2026-03-13 | CapitalRefreshJob built now (not deferred) | conviction_ratio needs total_capital_usdc; without it sub-score defaults to 0 |
| 2026-03-13 | ZREMRANGEBYSCORE trim on every write | O(log N + M) cost; avoids periodic cleanup job; bounded memory per market |
| 2026-03-13 | Price history TTL = 1 hour | Matches signal_decay half_life_seconds; sufficient for contrarian/saturation detectors |
| 2026-03-13 | active_markets Redis set (SADD by polygon_feed) | Decoupled subscription: CLOBMarketFeed polls whatever polygon_feed has observed |
| 2026-03-13 | gap-fill replay deferred to TODO | Adds complexity; acceptable risk at v1 scale where outages are rare |
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
