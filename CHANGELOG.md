# Changelog

All notable changes to MEG (Megalodon) are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.2.0] - 2026-03-13

### Added
- `meg/data_layer/capital_refresh.py` — `CapitalRefreshJob`: daily USDC balance sweep via
  Polygon RPC ERC-20 `balanceOf()` eth_call; single WebSocket connection reused across all
  wallets per sweep (not one per wallet); per-wallet errors logged and skipped; connection
  closed in `finally` block; `_get_usdc_balance()` raises `RuntimeError` if called outside sweep.
- `meg/core/redis_client.py` — Full implementation: `create_redis_client` (3-retry exponential
  backoff, immediate raise on `AuthenticationError`); `publish`; `subscribe` (async generator,
  re-raises `ConnectionError` on disconnect — never swallows it); `close`; `_redact_url` for
  safe logging.
- `meg/core/events.py` — `MarketState` Pydantic model; 10 new `RedisKeys` class methods
  (`market_bid`, `market_ask`, `market_volume_24h`, `market_participants`,
  `market_last_updated_ms`, `market_price_history`, `active_markets`,
  `last_processed_block`, `consensus_window`, `meg_config`).
- `meg/data_layer/polygon_feed.py` — Full implementation: `PolygonRPCConnection` ABC for
  testability; `Web3RPCConnection` (block polling, 1s interval); `PolygonFeed` (reconnect
  with exponential backoff 1s→60s, `_check_block_gap` logs WARNING on missed blocks,
  per-transaction try/except — feed never crashes on malformed txs); `_filter_whale_transaction`
  (CLOB contract filter, gas heuristic size proxy, `RawWhaleTrade` construction);
  `_emit_event` publishes to `CHANNEL_RAW_WHALE_TRADES`.
- `meg/data_layer/clob_client.py` — `CLOBMarketFeed`: polls Polymarket CLOB REST every 5s,
  writes all 8 market state scalar keys to Redis, maintains `price_history` sorted set with
  hourly ZREMRANGEBYSCORE trim; per-market error isolation; active market subscription via
  `active_markets` Redis set.
- `meg/data_layer/wallet_registry.py` — Full rewrite: dual-write (DB first, Redis cache second),
  Redis-first cache with 300s TTL, SQLAlchemy 2.0 async ORM, session injection for testability,
  12 public functions (`get_wallet`, `register_wallet`, `register_if_new`, `get_tracked_addresses`,
  `get_qualified_whale_wallets`, `is_qualified_whale`, `update_wallet_score`, `get_wallet_archetype`,
  `qualify`, `disqualify`, `flag_excluded`, `update_capital`).
- `meg/db/models.py` — 7 new `Wallet` columns (`total_volume_usdc`, `total_trades`,
  `total_capital_usdc`, `is_tracked`, `is_excluded`, `exclusion_reason`, `avg_hold_time_hours`)
  and 9 new `Trade` columns (`market_category`, `lead_time_hours`, `exit_price`, `exit_at`,
  `resolved_at`, `resolution`, `pnl_usdc`, `pnl_pct`, `tx_hash_exit`).
- `meg/db/migrations/versions/b4e2f9a1c3d7` — Alembic migration for all new wallet/trade columns.
- `TODOS.md` — P1: polygon_feed gap-fill replay; P2: wallet auto-discovery from on-chain data.
- `tests/data_layer/test_polygon_feed.py` — 18 tests (ABC contract, filter logic, per-tx error
  isolation, gap detection, `_emit_event` pubsub).
- `tests/data_layer/test_clob_client.py` — 11 tests (all 8 Redis scalar keys, price history
  sorted set, per-market error isolation).
- `tests/data_layer/test_capital_refresh.py` — 6 tests (per-wallet calls, error isolation,
  no-op on empty registry, connection cleanup in finally, `_get_usdc_balance` guard).
- `tests/core/test_redis_client.py` — 7 tests covering `create_redis_client` retry logic,
  `subscribe` ConnectionError re-raise guarantee, `publish` and `close` smoke tests.

### Changed
- `tests/conftest.py` — `mock_redis` fixture uses `decode_responses=True` to match production
  Redis client behavior (string responses instead of bytes); fixed `test_config` stub.
- `tests/data_layer/test_polygon_feed.py` — Fixed `test_emit_event_publishes_to_channel` to
  consume subscribe confirmation before asserting on published message (fakeredis pubsub behavior).

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
