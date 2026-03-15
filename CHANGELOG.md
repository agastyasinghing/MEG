# Changelog

All notable changes to MEG (Megalodon) are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.6.0] - 2026-03-14

### Added
- `meg/pre_filter/intent_classifier.py` — Gate 3 `classify()` and `build_qualified_trade()`
  fully implemented. 6-step decision tree: wallet data check → size threshold (REBALANCE) →
  session check → HEDGE (opposing trade with size >= current) → SIGNAL_LADDER (same-direction
  trades within ladder window) → default SIGNAL. All behavioral detection pushed to SQL queries.
- `build_qualified_trade()` enriches RawWhaleTrade with whale_score and archetype from Redis;
  returns None on cache miss (never emits whale_score=0.0).

### Changed
- `tests/pre_filter/conftest.py` — DB fixtures switched from pytest-postgresql to SQLite
  in-memory (aiosqlite) for local testing. Only creates Trade table (other models use JSONB
  which SQLite doesn't support). TODO added to restore pytest-postgresql for CI.
- `meg/pre_filter/intent_classifier.py` — HEDGE docstring corrected: "current trade opposing
  a prior position of equal or greater size" (was incorrectly symmetric "or vice versa").
- `tests/pre_filter/conftest.py` — Removed dead `Base` import; removed unused
  `meg.db.session` imports (`init_db`, `close_db`, `get_engine`).

## [0.1.5.0] - 2026-03-14

### Added
- `meg/pre_filter/market_quality.py` — Gate 1 now checks `volume_24h_usdc >= min_volume_24h_usdc`
  (PRD §9.1 first threshold, previously missing). Adds `_get_volume_24h()` helper. Docstring
  updated to list all five checks including the new volume check.
- `meg/db/models.py` — `Trade.price_at_market_end` column (`Numeric(6,4)`, nullable). Required
  by PRD §12 for lead-lag calibration and PnL attribution at market resolution.
- `meg/db/migrations/versions/d1e3f5a2b8c4_add_trade_price_at_market_end.py` — Alembic migration
  adding `price_at_market_end` to the `trades` table. Revises `c8f2e4b1a9d3`.
- `TODOS.md` — Gate 2 heuristic #2 (hold-time arb, P2) and #3 (tight-spread volume
  concentration, P2) added as deferred v1.5 items with full implementation context.
- `TODOS.md` — HEDGE detection note added to Opus session TODO: implement against test spec
  (same-market opposing position), not PRD §9.1 pseudocode (cross-market correlated exposure).

### Changed
- `meg/core/config_loader.py` — `PreFilterConfig`: split `min_market_liquidity_usdc` (now
  `10_000` per PRD §9.1 `mq_min_liquidity`) from new `min_volume_24h_usdc` (`50_000` per PRD
  `mq_min_volume_24h`). `max_spread_pct` corrected to `0.06` per PRD default.
- `config/config.yaml` — pre_filter section updated: `min_volume_24h_usdc: 50000` added,
  `min_market_liquidity_usdc: 10000` (was 50000), `max_spread_pct: 0.06` (was 0.05).
- `meg/pre_filter/arbitrage_exclusion.py` — Docstring updated with explicit v1 simplification
  rationale: covers PRD heuristic #1 only; heuristics #2 and #3 deferred to v1.5 with
  rationale and TODOS.md references.
- `tests/pre_filter/conftest.py` — `set_market_redis_data()` adds `volume_24h` param
  (default `500_000.0`) and writes `market:{id}:volume_24h` to fakeredis.
- `tests/pre_filter/test_market_quality.py` — New test `test_check_low_volume_24h` covers
  the volume_24h threshold path. Comment corrections for updated defaults (10k, 0.06).

## [0.1.4.0] - 2026-03-14

### Added
- `meg/pre_filter/market_quality.py` — Gate 1 full implementation: UNCHARACTERIZED vs
  BELOW_THRESHOLD state machine, negative cache (`quality_failed` EX 3600s), 5 threshold
  checks (liquidity, spread, participants, days_to_resolution, stale-data guard). Helper
  functions `_get_last_updated_ms`, `_get_market_liquidity`, `_get_market_spread`,
  `_get_participants`, `_get_days_to_resolution`.
- `meg/pre_filter/arbitrage_exclusion.py` — Gate 2 full implementation: ARBITRAGE archetype
  short-circuit (O(1) Redis read) + Trade table behavioral detection (YES+NO same-market
  within `arb_detection_window_hours`). Session injection for testability; Redis/DB errors
  fail open (conservative). Adds `session: AsyncSession | None` parameter.
- `meg/pre_filter/pipeline.py` — New: full pipeline orchestration. Subscribes to
  `raw_whale_trades`, runs Gate 1→2→3 in order, per-gate try/except (fail closed on error),
  re-raises `NotImplementedError` (unimplemented gate must be fixed), publishes
  `QualifiedWhaleTrade` to `qualified_whale_trades`. Structlog-only rejection logging.
- `meg/core/events.py` — `RedisKeys.market_days_to_resolution(market_id)` and
  `RedisKeys.wallet_data(address)` static key methods.
- `meg/db/session.py` — `get_engine()` public accessor; eliminates need to import private
  `_engine` from outside the module.
- `config/config.yaml` — 5 new `pre_filter` params: `min_days_to_resolution: 3`,
  `arb_detection_window_hours: 24`, `ladder_window_hours: 6`, `ladder_min_trades: 2`,
  `min_signal_size_pct: 0.02`.
- `meg/core/config_loader.py` — 4 new `PreFilterConfig` fields matching config.yaml additions;
  `min_days_to_resolution` default updated 1→3.
- `meg/data_layer/clob_client.py` — `_write_state()` now writes `market:{id}:days_to_resolution`
  (int string or `""` for None) on every poll cycle.
- `meg/pre_filter/intent_classifier.py` — Updated signatures (`session: AsyncSession | None`
  on `classify()`; `QualifiedWhaleTrade | None` return on `build_qualified_trade()`); full
  docstrings with intent definitions; OPUS marker. Stubs remain `NotImplementedError`.
- `tests/pre_filter/conftest.py` — DB fixtures (`db_engine`, `db_session` via pytest-postgresql)
  + factory helpers (`make_raw_trade`, `set_wallet_redis_data`, `set_market_redis_data`,
  `insert_trade_record`) shared across all pre-filter test modules.
- `tests/pre_filter/test_market_quality.py` — 15 tests covering all Gate 1 branches (cache
  hit, UNCHARACTERIZED no-cache, liquidity/spread/participants/days_to_resolution thresholds,
  negative days, None skip, all-pass, multi-failure single write, helper unit tests).
- `tests/pre_filter/test_arbitrage_exclusion.py` — 12 tests covering all Gate 2 branches
  (archetype short-circuit, absent archetype, YES+NO behavioral, single-side, outside-window,
  INFORMATION/MANIPULATOR pass, session=None, Redis error fallthrough).
- `tests/pre_filter/test_intent_classifier.py` — 14 test SPECS (full arrange/act/assert,
  stubs raise `NotImplementedError`). Opus implements against these in a future session.
- `tests/pre_filter/test_pipeline.py` — 10 orchestration tests (mocked gates): Gate 1/2/3
  short-circuit, HEDGE/REBALANCE filter, SIGNAL/SIGNAL_LADDER full pass, schema validation,
  wallet-data-unavailable discard, gate exception fails closed.
- `requirements-dev.txt` — `pytest-mock==3.14.0` (required by pipeline mock tests).
- `TODOS.md` — 4 new deferred items: Opus intent_classifier session (P1), Gate 1 Redis
  pipeline optimization (P3), behavioral state Redis cache for Gates 2/3 (P2), pre-filter
  rejection analytics (P2).

## [0.1.3.0] - 2026-03-14

### Added
- `meg/core/config_loader.py` — Full `ConfigLoader` implementation: `_ConfigFileHandler`
  watchdog handler (directory-watch, resolved-path filter); `ConfigLoader.start()` initial
  load + observer startup (raises fatal on bad YAML/schema); `get()` thread-safe read under
  `threading.Lock`; `stop()` idempotent observer teardown; `_load_and_validate()` with
  empty-file→defaults handling; `_on_config_changed()` hot-reload with keep-last-good on
  any error. Thread-safety diagram in module docstring.
- `meg/core/config_loader.py` — `PreFilterConfig.min_days_to_resolution: int = 1` — Gate 1
  minimum calendar days until market resolution.
- `meg/core/events.py` — `MarketState.days_to_resolution: int | None` — calendar days until
  market end date; `None` for indefinite markets or parse failures (Gate 1 skips check
  conservatively). `RedisKeys.market_quality_failed(market_id)` — Gate 1 rejection cache key.
- `meg/data_layer/clob_client.py` — `_parse_days_to_resolution(market_id, raw_date)` helper:
  parses ISO-8601 end dates with `Z` suffix, naive datetime, and three Polymarket field name
  variants (`end_date_iso`, `end_date`, `endDate`); returns `None` on any parse failure.
  `_fetch_market_state` now extracts and passes `days_to_resolution` to `MarketState`.
- `meg/data_layer/wallet_registry.py` — `get_recent_trades`, `get_recent_same_direction`,
  `get_correlated_exposure` trade history queries for pre-filter Gates 2/3. All use the new
  `ix_trades_wallet_market_time` compound index. `_CORRELATED_EXPOSURE_WINDOW_DAYS = 30`
  named constant for the 30-day HEDGE exposure window.
- `meg/db/models.py` — `ix_trades_wallet_market_time` compound index on
  `(wallet_address, market_id, traded_at DESC)` for Gate 3 hot-path queries.
- `meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py` — Alembic
  migration creating the compound trade index.
- `tests/core/test_config_loader.py` — 17 tests covering `_load_and_validate`, `start`,
  `get`, `_on_config_changed` (hot-reload, keep-last-good), `stop` (idempotent), and a
  concurrency test (500 `get()` calls racing against background reload thread).
- `tests/data_layer/test_clob_client.py` — 4 new tests: `_parse_days_to_resolution` valid
  date, `None` input, invalid format, expired market; 1 test for `_fetch_market_state`
  happy-path `days_to_resolution` extraction via mocked httpx.
- `tests/data_layer/test_wallet_registry.py` — 10 new tests for `get_recent_trades`,
  `get_recent_same_direction`, and `get_correlated_exposure`.
- `TODOS.md` — `[P1] Gate 1: resolution_source field and flagged_sources config` entry with
  full resume context; blocked on confirming Polymarket CLOB API field name.

### Fixed
- `meg/pre_filter/intent_classifier.py` — `Intent` type alias was missing `SIGNAL_LADDER`;
  the literal union now correctly includes all four intent values.

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
