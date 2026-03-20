# Changelog

All notable changes to MEG (Megalodon) are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.15.0] - 2026-03-20

### Added
- `meg/dashboard/ui/` — Phase 9 dashboard scaffold: Vite + React 18 + React Three Fiber + Drei + GSAP.
  Full-screen R3F canvas with `ScrollControls` (5 pages). Camera lerps through megalodon body parts
  (Mouth → Eye → Head → Dorsal Fin → Tail) via `useFrame` + `THREE.Vector3.lerp`.
- `meg/dashboard/ui/src/Scene.jsx` — Megalodon GLB loaded via `useGLTF`/`useAnimations`. Plays "bite"
  once on mount then crossfades to "swim"; crossfades to "circle" when scroll enters eye section (18–42%).
  200-particle bioluminescent `Points` system drifting upward. `FogExp2` ocean atmosphere.
  `PanelController` drives panel opacity via direct DOM manipulation inside `useFrame` (zero re-renders).
- `meg/dashboard/ui/src/App.jsx` — 5 HUD panels (absolute-positioned, `pointer-events: none`) with mock
  data matching PRD §13 shapes: Approval Queue, Signal Feed, System Status, Open Positions, P&L History.
  Raw SVG line chart with area fill gradient for P&L panel. Seeded deterministic mock data (LCG, seed=42).
- Custom cyan crosshair cursor via CSS `url()` data-URI. No Tailwind, no component libraries.

### Changed
- `README.md` — replaced stub with concise architecture summary, stack table, and current status.

## [0.1.14.0] - 2026-03-20

### Added
- `meg/telegram/bot.py` — `_alert_loop()` subscribes to `CHANNEL_BOT_ALERTS` and forwards
  `AlertMessage` JSON to `send_alert()`. `urgent=True` alerts are prefixed with "🚨 URGENT:".
  Reconnect pattern mirrors `_subscriber_loop` (exponential backoff, cap 60s). Both loops
  run concurrently via `asyncio.TaskGroup` in `start()`.
- `meg/telegram/bot.py` — `handle_reject_command()` for `/reject {proposal_id} {reason}` operator
  command. Auth-gated (same check as `/pause`/`/resume`). Uses `redis.getdel()` atomic get+delete.
  Logs rejection reason via structlog (durable storage deferred to TODOS.md).
- `meg/telegram/bot.py` — `_is_authorized(uid)` module-level helper centralises the
  `_authorized_ids` check used by `_cb` closure and `handle_reject_command()`.
- `meg/core/events.py` — `AlertMessage` Pydantic model with `alert_type` Literal and `urgent` flag.
  `CHANNEL_BOT_ALERTS` Redis channel constant. Two new `TradeProposal` display fields:
  `current_price` and `estimated_slippage`.
- `meg/agent_core/decision_agent.py` — `_build_proposal()` made async; reads live
  `market_mid_price` and `market_liquidity` from Redis to populate `current_price` and
  `estimated_slippage` on every proposal. Circuit breaker rejection now publishes an urgent
  `AlertMessage` to `CHANNEL_BOT_ALERTS`.
- `meg/agent_core/trap_detector.py` — publishes urgent `AlertMessage(alert_type="trap")` to
  `CHANNEL_BOT_ALERTS` on every detected whale trap.
- `meg/agent_core/position_manager.py` — publishes `AlertMessage(alert_type="position_closed")`
  on close with P&L result; publishes `AlertMessage(alert_type="whale_exit")` when contributing
  whale selling is detected in `_check_single_position`.
- `meg/agent_core/risk_controller.py` — `CIRCUIT_BREAKER_REASON_PREFIX` constant exported for
  use by `decision_agent` to detect circuit breaker rejections without string guessing.
- `_format_proposal()` — shows `current_price`, `estimated_slippage`, and `entry_distance_pct`
  (distance from whale fill price) in the Telegram approval message.
- Inline button `_cb` closure in `start()` extended with auth check before dispatching to
  `handle_approval_callback()`.

### Changed
- `start()` now runs `_subscriber_loop` and `_alert_loop` concurrently via `asyncio.TaskGroup`
  instead of running only `_subscriber_loop` directly.

### Added (tests)
- `tests/telegram/test_bot.py` — 13 new tests: `_alert_loop` (valid dispatch, urgent prefix,
  invalid JSON skip, ConnectionError reconnect), `_cb` auth (unauthorized blocked, empty
  `_authorized_ids` allows all), `handle_reject_command` (valid, unknown proposal, missing args,
  unauthorized), `_format_proposal` (current_price, slippage, entry_distance_pct shown).
- `tests/agent_core/test_decision_agent.py` — circuit breaker alert publish + Redis miss fallback.
- `tests/agent_core/test_position_manager.py` — `position_closed` alert publish + `whale_exit`
  alert publish via `_check_all_positions`.
- `tests/agent_core/test_trap_detector.py` — trap alert publish to `CHANNEL_BOT_ALERTS`.

## [0.1.13.0] - 2026-03-20

### Added
- `meg/telegram/bot.py` — Phase 8 Telegram bot fully implemented. Functions: `start()`,
  `send_approval_request()`, `handle_approval_callback()`, `handle_pause_command()`,
  `handle_resume_command()`, `send_alert()`. Internal helpers: `_format_proposal()`,
  `_execute_approved_proposal()`, `_subscriber_loop()`.
  - `start()` uses lower-level PTB API (`initialize/start/updater.start_polling`) for
    non-blocking asyncio coexistence with the Redis subscriber loop.
  - `send_approval_request()` stores the full `TradeProposal` in Redis with TTL =
    `config.signal.ttl_seconds` and sends an HTML-formatted message with inline
    APPROVE / REJECT keyboard buttons.
  - `handle_approval_callback()` uses `redis.getdel()` for atomic get+delete —
    eliminates TOCTOU race between concurrent PTB update tasks (duplicate order prevention).
    Routes APPROVE → `order_router.place(session=None)`; REJECT → edits message only.
  - `handle_pause_command()` / `handle_resume_command()` write to `RedisKeys.system_paused()`.
    Optional `TELEGRAM_AUTHORIZED_USER_IDS` env var restricts commands to a whitelist.
  - `_subscriber_loop()` reconnects on `ConnectionError` with exponential backoff (cap 60s).
    Invalid JSON / `ValidationError` messages are logged and skipped — loop never crashes.
  - `send_alert()` safe to call before `start()` — logs warning, returns, never raises.
- `meg/core/events.py` — `RedisKeys.pending_proposal(proposal_id)` key builder added.
  Stores pending `TradeProposal` JSON between send and callback; deleted atomically by
  `handle_approval_callback()` as the double-click guard.
- `tests/telegram/` — 20 tests, all passing. Covers: approval request formatting, Redis
  TTL storage, inline keyboard, APPROVE/REJECT/expired/double-click callback paths,
  pause/resume auth, `send_alert` pre-start safety, subscriber loop error recovery.

### Fixed
- `handle_approval_callback`: replaced `redis.get()` + `redis.delete()` (two round trips,
  TOCTOU window) with `redis.getdel()` (atomic). Prevents duplicate `order_router.place()`
  calls if two Telegram callbacks arrive concurrently for the same proposal.

## [0.1.12.0] - 2026-03-16

### Added
- `meg/execution/entry_filter.py` — `check()` + `get_current_price()` implemented.
  Direction-aware entry distance gate against `market_price_at_signal` (whale fill price).
  Fail-closed: Redis miss → reject. Added explicit guard for `signal_price=0` (unset) → reject.
- `meg/execution/slippage_guard.py` — `check()` (spread gate + price-drift gate, 3-tuple return)
  + `estimate_slippage()` (size/liquidity proxy, fail-closed). Spread gate fails fast — drift gate
  not evaluated on spread failure. Slippage always computed and returned for analytics.
- `meg/execution/order_router.py` — `place()` full execution chain implemented:
  entry_filter → slippage_guard → `_place_with_retry()` (transport-only retry, exponential backoff)
  → `position_manager.open_position()`. Added `session: AsyncSession | None = None` param.
  Direction-aware TP/SL price computation (YES: price rises to TP, NO: price falls to TP).
- `meg/core/logger.py` — `setup_logging()` + `get_logger()` implemented with structlog JSON
  processor chain (stdlib backend, ISO timestamps, contextvars merge, exc_info rendering).
- `meg/data_layer/clob_client.py` — `place_order()` paper mode implemented: logs `[PAPER]`
  prefix, returns `PAPER_{12 hex chars}` synthetic ID without touching the exchange.
  Live mode raises `NotImplementedError` (blocked by OQ-05).
- `meg/core/config_loader.py` — `EntryConfig` extended with 3 new fields:
  `taker_spread`, `limit_timeout_seconds`, `max_price_drift_since_signal`; defaults fixed
  (`max_entry_distance_pct: 0.06`, `max_spread_pct: 0.04`).
- `config/config.yaml` — `entry` block updated to match new `EntryConfig`.
- `tests/execution/` — 29 tests: `conftest.py` (mock_redis, test_config, make_proposal,
  set_market_redis_data) + `test_entry_filter.py` (8) + `test_slippage_guard.py` (11)
  + `test_order_router.py` (10). All pass.
- `TODOS.md` — 3 new P1/P2 entries: live order placement auth, limit→market timeout
  conversion, real orderbook depth slippage estimation.

### Fixed
- `order_router._place_with_retry`: `asyncio.TimeoutError` removed from retryable set.
  In Python 3.11+ `asyncio.TimeoutError` is a subclass of `OSError` — it was being retried,
  which risks placing duplicate CLOB orders when a response timeout fires after the CLOB
  accepted the order. Added explicit `isinstance` guard to re-raise immediately.
- `tests/data_layer/test_clob_client.py` — `test_place_order_stub_raises` updated to
  `test_place_order_paper_mode_returns_synthetic_id` (paper mode now implemented) +
  new `test_place_order_live_mode_raises` (asserts live mode still raises `NotImplementedError`).

## [0.1.11.0] - 2026-03-15

### Changed
- `meg/agent_core/decision_agent.py` — Trap detection is now warn-only per PRD §9.4.2:
  trap-detected signals produce a TradeProposal with `trap_warning=True` instead of
  cancelling. Operator decides via Telegram approval. Status stays TRAP_DETECTED in
  signal_outcomes (not overwritten to APPROVED).
- `meg/agent_core/risk_controller.py` — Converted from 5-gate to 4-gate framework.
  Position size check removed from `check()` and replaced with public
  `clamp_position_size()` per PRD §10 Gate 2: "Reduce position size to maximum
  allowed. Do not block the trade." Called by decision_agent after saturation adjustment.
- `TODOS.md` — Removed completed intent_classifier TODO (P1). Added 5 deferred TODOs
  for PRD compliance gaps (P2–P3): saturation sensitivity default, trailing TP
  half-life condition, trailing TP 1-hour price change, position state machine
  states, decision agent gate ordering.

## [0.1.10.0] - 2026-03-15

### Added
- `meg/agent_core/signal_aggregator.py` — Redis pub/sub subscriber, TTL/dedup validation,
  routes valid signals to decision_agent. In-memory dedup set capped at 10k entries.
- `meg/agent_core/decision_agent.py` — Gate orchestration: system_paused → blacklist →
  duplicate → risk_controller → trap_detector → saturation_monitor → crowding_detector.
  Builds TradeProposal (PENDING_APPROVAL), publishes to CHANNEL_TRADE_PROPOSALS,
  updates signal_outcomes status in DB.
- `meg/agent_core/position_manager.py` — Redis-first CRUD for open positions, TP/SL
  monitor loop (30s interval), whale exit detection (5min interval via Trade table queries),
  daily PnL reset at midnight UTC. Dual-write pattern (Redis authoritative, DB best-effort).
- `meg/agent_core/risk_controller.py` — 5-gate risk framework (cheapest first):
  paper_trading → daily_loss circuit breaker → max_positions → market_exposure → position_size.
  All reads from Redis keys. Short-circuits on first failure.
- `meg/agent_core/trap_detector.py` — Pump-and-exit detection per PRD §9.4.2. Queries Trade
  table for entry + sells within trap_window. Writes WhaleTrapEvent to DB, publishes penalty
  to CHANNEL_WALLET_PENALTIES, flags MANIPULATOR after threshold.
- `meg/agent_core/saturation_monitor.py` — v1 formula: drift_score * 0.60 + thinning_score * 0.40.
  Returns size_multiplier [0.25, 1.0] — reduces position size, never blocks.
- `meg/agent_core/crowding_detector.py` — Price-based entry distance gate. Blocks if
  directional drift from whale fill exceeds crowding_max_entry_distance_pct (8%).
- `meg/core/events.py` — `PositionState` Pydantic model for Redis position serialization.
  `CHANNEL_WALLET_PENALTIES` Redis pub/sub channel.
- `meg/core/config_loader.py` — `crowding_max_entry_distance_pct` on AgentConfig.
- `config/config.yaml` — `crowding_max_entry_distance_pct: 0.08` under agent section.
- `tests/agent_core/conftest.py` — JSONB→JSON SQLite compiler, db_engine/db_session/mock_redis
  fixtures, 8 factory helpers (make_signal_event, make_position_state, set_market_redis_data,
  add_position_to_redis, insert_trade_record, insert_wallet, insert_signal_outcome).
- 92 agent_core tests across 7 test files covering all modules and edge cases.

### Fixed
- `meg/agent_core/position_manager.py` — `daily_pnl_reset_loop` used `.replace(day=day+1)`
  which crashes on month-end (day 31 → 32). Fixed to use `timedelta(days=1)`.
- `meg/agent_core/saturation_monitor.py` — removed dead code block (`if signal.scores ... pass`).

## [0.1.9.0] - 2026-03-15

### Added
- `meg/core/config_loader.py` — `AgentConfig` sub-model with saturation and trap
  detection parameters: `saturation_threshold` (0.60), `saturation_size_reduction_sensitivity`
  (2.0), `trap_window_minutes` (30), `trap_exit_threshold` (0.50), `trap_score_penalty` (0.20),
  `trap_manipulator_threshold` (3). Registered as `config.agent` on `MegConfig`.
- `meg/core/config_loader.py` — `PositionConfig` sub-model with position lifecycle risk
  parameters: `take_profit_pct` (0.40), `stop_loss_pct` (0.25), `trailing_tp_enabled` (false),
  `trailing_tp_floor_pct` (0.10), `auto_exit_stop_loss` (false), `auto_exit_take_profit`
  (false). Registered as `config.position` on `MegConfig`.
- `meg/core/config_loader.py` — `RiskConfig` extended with `max_portfolio_exposure_pct`
  (0.60, PRD §10 Gate 3), `blacklisted_markets: list[str]` (hot-reloadable market block list).
- `meg/core/events.py` — `RedisKeys` position tracking key builders: `open_positions()`,
  `position(id)`, `daily_pnl_usdc()`, `portfolio_value_usdc()`, `market_exposure_usdc(market_id)`.
  Used by `position_manager` and `risk_controller` in Phase 6.
- `meg/core/events.py` — `RedisKeys.system_paused()` → `"meg:system_paused"`. Emergency
  pause flag written atomically by Telegram `/pause`; read by `decision_agent`. Intentionally
  NOT in config.yaml — hot-reload latency (~1s) is unacceptable for an emergency stop.
- `meg/core/events.py` — `TradeProposal` enriched with dashboard approval queue fields:
  `composite_score`, `scores` (full `SignalScores` breakdown), `saturation_score`,
  `trap_warning`, `contributing_wallets`, `market_price_at_signal`,
  `estimated_half_life_minutes`. All optional with safe defaults for backward compat.
- `config/config.yaml` — `agent:` and `position:` sections matching new config models.
  `risk:` section extended with `max_portfolio_exposure_pct: 0.60` and `blacklisted_markets: []`.

## [0.1.8.0] - 2026-03-15

### Added
- `meg/signal_engine/lead_lag_scorer.py` — fully implemented. `score()` returns [0.0, 1.0]
  using saturating lead-time factor `1-exp(-hours/6)` × win_rate × reputation decay multiplier.
  `compute_reputation_decay()` uses exponential decay `exp(-days/τ)` with configurable τ
  (default 30 days). None last_profitable_trade_at → no penalty (1.0).
- `meg/signal_engine/kelly_sizer.py` — fully implemented. `_kelly_fraction()` computes
  `f* = (p·b - q) / b` for binary markets. `compute_size()` applies quarter-Kelly scaling
  (`config.kelly.fraction`), hard cap (`config.kelly.max_bet_usdc`), returns 0.0 on
  negative/zero edge.
- `meg/signal_engine/consensus_filter.py` — fully implemented. `score()` adds current wallet
  to Redis consensus sorted set, trims stale entries outside `consensus_window_hours`,
  counts agreeing whales (excluding self), returns `tanh(n × sensitivity / 2)`. YES/NO
  tracked independently via `RedisKeys.consensus_window(market_id, outcome)`.
- `meg/signal_engine/contrarian_detector.py` — fully implemented. `get_order_flow_direction()`
  reads price history from Redis sorted set, computes trend via `tanh(Δprice × 5.0)`.
  `score()` returns divergence `0.5 × (1 - trade_dir × flow_dir)`: 1.0 = contrarian,
  0.5 = neutral, 0.0 = momentum.
- `meg/signal_engine/signal_decay.py` — fully implemented. `apply_decay()` uses half-life
  formula `score × 0.5^(age/half_life)`, returns 0.0 below min threshold or negative age.
  `is_expired()` checks TTL. `set_signal_ttl()` writes expiry to Redis with configurable
  multiplier and minimum floor.
- `meg/signal_engine/composite_scorer.py` — `score()` and `_gather_component_scores()` fully
  implemented. Pre-fetches wallet_data once from Redis (SignalDroppedError on miss). Runs all
  7 sub-scorers concurrently via `asyncio.gather()`. Lead-lag gate checked after gather
  (raises SignalDroppedError if below threshold). Builds SignalEvent with all sub-scores,
  Kelly sizing, TTL, contrarian flag, and PENDING/FILTERED status.

### Changed
- `meg/signal_engine/composite_scorer.py` — fixed module docstring: lead-lag gate is checked
  AFTER asyncio.gather() returns (all components computed concurrently), not before.

## [0.1.7.0] - 2026-03-15

### Added
- `meg/signal_engine/archetype_weighter.py` — fully implemented. Config-driven multipliers
  (hot-reloadable via `config.signal.archetype_weights`). ARBITRAGE/MANIPULATOR log a structlog
  WARNING as defense-in-depth and return 0.0; INFORMATION returns 1.0; MOMENTUM returns 0.65.
- `meg/signal_engine/ladder_detector.py` — fully implemented. Returns a conviction multiplier
  in [1.0, 2.0]. Counts qualifying prior same-wallet/market/outcome DB trades within
  `config.pre_filter.ladder_window_hours` as rungs. Formula: `min(1.0 + rungs * per_rung, 2.0)`.
- `meg/signal_engine/composite_scorer._combine_scores()` — fully implemented. PRD §9.3.9 formula:
  Step 1 weighted base (lead_lag·0.35 + consensus·0.30 + kelly·0.20 + divergence·0.15),
  Step 2 archetype+ladder multipliers, Step 3 conviction blend (adjusted·0.85 + conviction·0.15),
  result clamped to [0.0, 1.0], all weights config-driven and hot-reloadable.
- `meg/signal_engine/conviction_ratio.py` — fully implemented. `get_wallet_capital()` prefers
  `total_capital_usdc`, falls back to `total_volume_usdc`, then 1.0 to avoid division by zero.
  `score()` returns `min(trade.size_usdc / capital, 1.0)`.
- `meg/core/events.py` — Added `SignalType` Literal, `SignalDroppedError` exception, `market_category`
  field on RawWhaleTrade/QualifiedWhaleTrade, 4 new SignalEvent fields (signal_type,
  estimated_half_life_minutes, whale_archetype, market_category). Fixed `RedisKeys.consensus_window()`
  to include outcome dimension; added `RedisKeys.market_category()`.
- `meg/core/config_loader.py` — New `CompositeWeightsConfig` and `ArchetypeWeightsConfig`
  sub-models. `SignalConfig` extended with 8 new fields (composite_weights, archetype_weights,
  consensus params, ladder params, TTL params, lead_lag gate, contrarian threshold).
  `ReputationConfig.decay_tau_days` and `KellyConfig.portfolio_value_usdc` added.
- `config/config.yaml` — All new config fields: composite_weights block, archetype_weights block,
  consensus_window_hours, consensus_sensitivity, min_whales_for_consensus, ladder_conviction_per_rung,
  ttl_half_life_multiplier, min_half_life_minutes, lead_lag_min_gate, contrarian_threshold,
  kelly.portfolio_value_usdc, reputation.decay_tau_days.
- `meg/db/models.py` — Added `last_profitable_trade_at` column to Wallet model (nullable DateTime).
- `meg/data_layer/clob_client.py` — `_fetch_market_state()` now returns `tuple[MarketState, str]`
  carrying market_category alongside state. `_write_state()` writes category to Redis at
  `market:{id}:category`.
- `meg/data_layer/polygon_feed.py` — `_process_block()` enriches emitted RawWhaleTrade with
  market_category from Redis (populated by CLOBMarketFeed).
- `meg/data_layer/wallet_registry.py` — Serialization includes `last_profitable_trade_at` field.
- `tests/signal_engine/` — Full test suite for signal engine: conftest with fixtures
  (`db_session`, `test_config`, `make_qualified_trade`, `make_wallet_data`, `insert_trade`).
  2 modules fully tested (archetype_weighter: 13 tests, ladder_detector: 12 tests).
  7 modules marked `xfail` as Opus specs (lead_lag_scorer, conviction_ratio, kelly_sizer,
  consensus_filter, contrarian_detector, signal_decay, composite_scorer integration tests).
- `tests/data_layer/test_clob_client.py` — 2 new tests for market_category Redis write.
- `tests/data_layer/test_polygon_feed.py` — 2 new tests for market_category enrichment branch.

### Fixed
- `meg/data_layer/clob_client.py:122` — `_fetch_market_state()` return type annotation corrected
  from `-> MarketState` to `-> tuple[MarketState, str]`; docstring updated to match.
- `meg/signal_engine/archetype_weighter.py:51` — Warning log `note` field reworded to not claim
  a hardcoded "0.0" return when the actual value comes from config.
- `tests/signal_engine/test_composite_scorer.py` — Corrected arithmetic error in
  `test_combine_scores_uses_config_weights` expected value (0.434 → 0.5615).
- Existing `test_clob_client.py` `_write_state()` calls updated to pass `market_category` arg.
- Existing `test_clob_client.py` `_fetch_market_state()` calls updated to unpack `(state, category)` tuple.

### Changed
- `meg/signal_engine/composite_scorer.py` — Imports all sub-scorer modules at module level
  (required for `unittest.mock.patch()` in integration tests).
- `TODOS.md` — Added TODO-1 (per-signal-type half-life v1.5) and TODO-2 (composite weight
  calibration from signal_outcomes data after 200+ resolved signals).

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
