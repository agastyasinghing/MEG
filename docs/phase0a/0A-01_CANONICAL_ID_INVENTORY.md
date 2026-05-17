# Phase 0A Ticket 0A-01A — Canonical Identifier Inventory and Contract-Test Plan

## Scope and source of truth

Ticket 0A-01A inventories the existing `market_id` footprint before any migration work. The Phase 0A contract is: route, match, persist, and publish shared-rail events with `condition_id`, `token_id`, and `outcome`; keep `market_slug` only as nullable display metadata; never route on `market_id`.

This document is an inventory and test plan only. It intentionally does **not** change runtime source code, schemas, migrations, fixtures, or tests.

Inventory granularity is file/symbol/function-level, not literal line-by-line occurrence-level. The `rg` commands below found 62 unique pre-existing files and 557 individual `market_id` occurrence lines, excluding this inventory document. All 62 files are represented in the detailed inventory; Appendix A records per-file occurrence counts without listing all 557 lines.

## Search commands used

- `rg -n "market_id" . --glob '!*.git/*'`
- `rg -n "condition_id" . --glob '!*.git/*'`
- `rg -n "token_id" . --glob '!*.git/*'`
- `rg -n "\boutcome\b" . --glob '!*.git/*'`
- `rg -n "market_slug" . --glob '!*.git/*'`
- `rg -l "market_id" . --glob '!*.git/*' | sort`
- `for f in $(rg -l "market_id" meg tests --glob '!*.git/*' | sort); do rg -c "market_id" "$f"; done`

## Classification legend

- **Shared-rail routing field:** Internal payload, Redis key, DB column, execution/risk/journal path, or matching key that must migrate to `condition_id` + `token_id` + `outcome`.
- **External/API boundary:** Ingestion, API, CLOB, dashboard, or historical external-doc boundary where legacy `market_id` may be accepted temporarily, but only behind an explicit normalization shim that emits/persists canonical identifiers.
- **Harmless docs/comments/test reference:** Documentation, changelog, legacy PRD, comments, or test fixture assertions that are not runtime routing paths; update opportunistically after the code migration to avoid stale guidance.

Risk levels:

- **blocker:** Blocks Phase 0A canonical contract, paper execution correctness, or journal correctness.
- **high:** Internal routing/cache/risk behavior will be wrong until migrated.
- **medium:** Boundary or UI surface can be shimmed, or a test fixture will fail after migration until updated.
- **low:** Historical docs/comments only.

## Inventory summary by risk level

Counts in this section are grouped inventory rows/categories, not raw `rg` occurrence counts. Raw per-file occurrence counts are listed in Appendix A.

| Risk | Count | Main categories |
| --- | ---: | --- |
| blocker | 12 | Core event schemas, Redis key namespace, ORM/migrations, CLOB market-state feed, Polygon fabricated market IDs, proposal/execution/position models. |
| high | 15 | Agent-core risk/decision/position paths, pre-filter market-quality/intent/arbitrage paths, signal-engine Redis windows, execution guards, wallet trade repository. |
| medium | 25 | Dashboard/API surfaces and test/fixture files that encode the legacy contract. |
| low | 8 | Frozen/current docs, changelog/status/TODO notes, comments that mention legacy `market_id`. |

## Detailed inventory

| File path | Symbol/function/class/test name | Current `market_id` usage | Required migration action | Risk | Recommended next ticket |
| --- | --- | --- | --- | --- | --- |
| `meg/core/events.py` | `RawWhaleTrade` | Required event field on raw Redis event. | Replace with required `condition_id`, `token_id`, `outcome`; reject `market_id`-only payloads except approved boundary shims. | blocker | 0A-01B event schema migration |
| `meg/core/events.py` | `QualifiedWhaleTrade` | Carries `market_id` from pre-filter into signal engine. | Same canonical fields; preserve `outcome`; add validation that `condition_id` and `token_id` are non-empty. | blocker | 0A-01B event schema migration |
| `meg/core/events.py` | `SignalEvent` | Signal identity and routing use `market_id` + `outcome`. | Route by `condition_id` + `token_id` + `outcome`; keep `market_slug` display-only if added. | blocker | 0A-01B event schema migration |
| `meg/core/events.py` | `TradeProposal` | Operator approval and execution request precursor uses `market_id`. | Proposal contract must include canonical identifiers and never derive execution from slug or market id. | blocker | 0A-02 TradeProposal / ExecutionRequest contract |
| `meg/core/events.py` | `PositionState` | Open position de-duplication/exposure uses `market_id` + `outcome`. | Position identity/exposure keys must use canonical identifiers; likely `token_id` for outcome-specific holdings plus `condition_id` grouping. | blocker | 0A-06 journal schema + position lots |
| `meg/core/events.py` | `RedisKeys.market_*`, `active_markets`, `consensus_window`, `market_exposure_usdc` | Redis namespace routes/cache by `market:{market_id}:...`; active set stores market IDs. | Rename key constructors/active set around canonical identifiers; token-scoped quote keys should use `token_id`; condition-level metadata may use `condition_id`; include outcome where needed. | blocker | 0A-01C Redis key contract migration |
| `meg/db/models.py` | `Trade.market_id`, indexes | Historical/operational trade rows and indexes use `market_id`. | For Phase 0A operational journal tables, use `condition_id`, `token_id`, `outcome`; do not add `market_id` to new tables. Legacy whale tables can be migrated or isolated from shared rail. | blocker | 0A-06 Postgres journal schema |
| `meg/db/models.py` | `SignalOutcome.market_id`, indexes | Signal journal identity uses `market_id`. | Replace with canonical columns and indexes by `condition_id`, `token_id`, `outcome`, status/time. | blocker | 0A-06 Postgres journal schema |
| `meg/db/models.py` | `WhaleTrap.market_id` | Trap evidence keyed by market. | Replace with canonical fields if trap detection remains connected to shared rail; otherwise isolate as Phase 0C whale-specific legacy. | high | 0C whale repair / 0A boundary isolation |
| `meg/db/models.py` | `TradeProposalModel.market_id` | Approval queue persistence uses `market_id`. | New proposal journal/current-state tables must use canonical identifiers and optional `market_slug`. | blocker | 0A-05 Telegram proposal queue + 0A-06 journal |
| `meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py` | Initial Alembic schema | Creates legacy `market_id` columns and indexes. | Add new Phase 0A migration for canonical journal tables; avoid mutating this inventory ticket. | blocker | 0A-06 migration |
| `meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py` | Wallet/market index | Adds `(wallet_address, market_id, traded_at)` index. | Replace hot-path lookup index with canonical condition/token/outcome equivalent when wallet repositories migrate. | high | 0C-01 wallet trade repository canonicalization |
| `meg/data_layer/clob_client.py` | `CLOBMarketFeed.run`, `_poll_market`, `_fetch_market_state`, `_write_state_to_redis` | Reads `RedisKeys.active_markets()` as market IDs, calls CLOB by `token_id=market_id`, writes market keys. | Treat watched set as token IDs; normalize CLOB responses into `MarketState(condition_id, token_id, outcome, market_slug)`; publish/cache by canonical key. | blocker | 0A-03 CLOB market-state cache |
| `meg/data_layer/clob_client.py` | Compatibility helpers `get_market`, `get_orderbook`, `get_mid_price`, `place_order`, `get_open_orders`, `get_position` | Public helper signatures use `market_id`; `place_order` forwards market id to live client order args. | Boundary shim may accept legacy arg name temporarily but must normalize to `token_id` before order-book/order-placement calls and never persist `market_id`. | blocker | 0A-07 paper execution / future live boundary shim |
| `meg/data_layer/clob_client.py` | `_parse_days_to_resolution` | Helper name says market id but only logs/labels parse failures. | Rename parameter to canonical display context (`condition_id` or `token_id`) during CLOB migration. | medium | 0A-03 cleanup |
| `meg/data_layer/polygon_feed.py` | `PolygonFeed._process_block` | Reads category by `event.market_id`, adds event market to active set, logs market. | After ABI decoding/normalization, publish canonical raw trade and active token. No fabricated IDs. | blocker | 0C Polygon receipt decoder + 0A boundary shim |
| `meg/data_layer/polygon_feed.py` | `_filter_whale_transaction` | Fabricates `market_id = f"market_{tx_hash[:16]}"`; outcome is hard-coded. | Hard blocker: reject or quarantine unnormalized whale fills until receipt decoder can emit real `condition_id`, `token_id`, and `outcome`. | blocker | 0C Polygon receipt decoder |
| `meg/data_layer/wallet_registry.py` | `serialize_trade`, `get_recent_same_direction`, wallet trade insert/query helpers | Persists/queries wallet trades by `market_id`. | Update serialization plus same-direction/recent-trade filters to accept `condition_id`, `token_id`, and `outcome`; if imported history exposes only legacy IDs, normalize once at ingestion before repository writes. | high | 0C-01 wallet trade repository canonicalization |
| `meg/agent_core/decision_agent.py` | `handle_signal`, risk checks, proposal build | Checks blacklist, open position, risk, and proposal by `signal.market_id`. | Switch all decision/risk calls to canonical IDs; blacklist semantics should define condition/token granularity explicitly. | high | 0A-05 proposal queue / 0A-08 risk gates |
| `meg/agent_core/risk_controller.py` | `check_risk_gates` | Market exposure and duplicate-position checks use market id. | Use condition-level and token/outcome-level exposure gates; no `market_id` routing. | high | 0A-08 risk gates |
| `meg/agent_core/position_manager.py` | `open_position`, `close_position`, `monitor_open_positions`, Redis exposure keys | Position lifecycle and exposure accounting use market id. | Position lots must persist `condition_id`, `token_id`, `outcome`; exposure keys should be condition/token scoped. | high | 0A-06 journal + 0A-07 paper execution |
| `meg/agent_core/crowding_detector.py` | `check_crowding` | Looks up mid price and logs by signal market id. | Use token-scoped market-state cache and canonical log fields. | high | 0A-03 market-state cache / 0A-08 risk gates |
| `meg/agent_core/saturation_monitor.py` | `get_market_saturation` | Counts recent signals by market id. | Count by condition/token/outcome depending crowding semantics. | high | 0A-08 risk gates |
| `meg/agent_core/signal_aggregator.py` | Signal aggregation insert/update | References signal market id for DB writes. | Persist canonical signal journal fields. | high | 0A-06 journal writer |
| `meg/agent_core/trap_detector.py` | Trap detection queries and alerts | Looks up wallet exits and trap history by market id. | Phase 0C whale module should normalize to canonical IDs before interacting with shared rail. | high | 0C trap/wallet migration |
| `meg/execution/entry_filter.py` | `check_entry_price`, Redis reads | Uses proposal market id for price/entry guard. | Read `MarketState` by `token_id`; include condition/outcome in diagnostics. | high | 0A-07 paper execution |
| `meg/execution/slippage_guard.py` | `estimate_slippage`, `check_slippage` | Uses market id to fetch liquidity/bid/ask. | Token-scoped quote/liquidity lookup using `token_id`. | high | 0A-07 paper execution |
| `meg/execution/order_router.py` | `route_approved_proposal` | Forwards `proposal.market_id` into `open_position`. | Forward canonical execution request identifiers; no direct legacy field. | high | 0A-07 paper execution |
| `meg/pre_filter/market_quality.py` | `check_market_quality`, `_get_*` helpers | Reads market freshness/quality Redis keys by market id and caches rejects by market. | Gate 1 should consume canonical market state; token quote keys + condition-level metadata as appropriate. | high | 0A-03 market-state cache |
| `meg/pre_filter/arbitrage_exclusion.py` | `check_arbitrage_exclusion` | Queries recent opposing wallet trades by `trade.market_id`. | Use `condition_id` + `outcome` for cross-outcome/opposing-side logic. | high | 0C whale pre-filter migration |
| `meg/pre_filter/intent_classifier.py` | `classify_intent` | Wallet history calls and result payload use market id. | Migrate intent classifier to canonical fields before publishing qualified trades. | high | 0C whale pre-filter migration |
| `meg/pre_filter/pipeline.py` | `process_raw_trade` | Logs/publishes raw/qualified trades carrying market id. | Enforce canonical schema validation at pipeline input/output. | high | 0A-01B event schema migration |
| `meg/signal_engine/composite_scorer.py` | `score` | Signal ID/logs derive from qualified trade market id. | Signal identity should derive from `condition_id`, `token_id`, `outcome`, wallet/time; no market id. | high | 0A-01B event schema migration |
| `meg/signal_engine/consensus_filter.py` | `check_consensus` | Redis consensus window keyed by market id + outcome. | Key by condition/token/outcome as defined by consensus semantics. | high | 0A-01C Redis key contract |
| `meg/signal_engine/contrarian_detector.py` | `check_contrarian` | Reads bid/ask/history by market id. | Read token-scoped quote/history keys. | high | 0A-03 market-state cache |
| `meg/signal_engine/ladder_detector.py` | `check_ladder_pattern` | Detects repeated wallet activity by market id. | Use condition/token/outcome consistently; condition-level aggregation only if explicitly intended. | high | 0C whale signal migration |
| `meg/core/logger.py` | Structured event logging helper | Includes `market_id` in logging context. | Rename structured field(s) to canonical IDs; preserve backward-compatible log ingestion only behind an explicit boundary allowlist if needed. | medium | 0A-09 canonical observability cleanup |
| `meg/dashboard/api/main.py` | Signal/proposal/position/market endpoints | Query params, response DTOs, Redis reads, and mock data expose `market_id`. | API may accept legacy `market_id` only in a named boundary shim; translate before DB/Redis access, return canonical IDs plus display-only `market_slug`, and never persist or publish `market_id`. | medium | 0A-DASH-01 API canonical boundary/display contract |
| `meg/dashboard/ui/src/App.jsx` | Dashboard mock/API mapping/components | Displays and keys rows by market id; uses market id as market name fallback. | Display `market_slug` when present; key UI actions by proposal/position IDs plus canonical identifiers; never use slug or legacy market ID for action routing. | medium | 0A-DASH-02 UI canonical display/action contract |
| `meg/telegram/bot.py` | Approval rendering and pending proposal handling | Operator message includes market id; proposal payload carries market id. | Render condition/token/outcome and optional slug; approve by proposal ID only, execution request carries canonical IDs. | high | 0A-05 Telegram proposal queue |
| `tests/agent_core/conftest.py` | Fixtures `make_signal_event`, `make_trade_proposal`, `make_position_state` | Legacy fixtures build market-id-only payloads. | Update fixtures to canonical identifiers after event contracts land; add negative tests for missing canonical fields. | medium | 0A-01B canonical event contract tests |
| `tests/agent_core/test_decision_agent.py` | Decision tests | Assert duplicate/blacklist/proposal behavior by market id. | Convert expected behavior to canonical duplicate/exposure semantics once risk gate granularity is defined. | medium | 0A-08 canonical risk gate tests |
| `tests/agent_core/test_position_manager.py` | Position lifecycle tests | Position open/close/exposure assertions use market id. | Rewrite around canonical `position_lots` and paper execution lifecycle. | medium | 0A-06/0A-07 journal and paper execution tests |
| `tests/agent_core/test_risk_controller.py` | Risk gate tests | Market exposure fixture uses market id. | Test condition/token exposure gates. | medium | 0A-08 tests |
| `tests/agent_core/test_trap_detector.py` | Trap tests | Trap detection fixtures and DB rows use market id. | Move to canonical whale-specific tests after Phase 0C receipt and wallet normalization. | medium | 0C-02 whale trap detector canonical tests |
| `tests/dashboard/test_api.py` | API contract tests | Query/response assertions include market id. | Add boundary-shim tests, canonical response assertions, and `market_slug` display-only assertions. | medium | 0A-DASH-01 API canonical boundary/display contract |
| `tests/data_layer/test_clob_client.py` | CLOB feed tests | Active markets, fetched state, Redis writes, helper functions use market id. | Replace with watched token IDs and canonical MarketState assertions. | medium | 0A-03 tests |
| `tests/data_layer/test_polygon_feed.py` | Polygon feed tests | Expects fabricated market id behavior and active market SADD. | Mark old behavior invalid; add quarantine/rejection tests until ABI decoder emits canonical IDs. | medium | 0C-00 Polygon receipt decoder contract tests |
| `tests/data_layer/test_wallet_registry.py` | Wallet registry tests | Trade serialization/query tests use market id. | Update serialization and recent-trade query tests to canonical repository fields once migration lands. | medium | 0C-01 wallet trade repository canonicalization |
| `tests/db/test_models.py` | ORM model tests | Assert legacy columns and indexes. | Add Phase 0A table tests proving no `market_id` column; update legacy expectations only when schema migration occurs. | medium | 0A-06 tests |
| `tests/execution/conftest.py` | Proposal fixtures | Builds execution proposals with market id. | Update fixtures to `condition_id`, `token_id`, `outcome`. | medium | 0A-07 tests |
| `tests/execution/test_order_router.py` | Router tests | Expects `open_position` receives market id. | Expect canonical execution/position args. | medium | 0A-07 tests |
| `tests/pre_filter/conftest.py` | Raw/qualified trade fixtures and Redis setup | Uses market id in fixtures and market quality Redis keys. | Canonicalize fixtures and helper Redis keys after event and market-state contracts land. | medium | 0A-01B + 0A-03 canonical fixture tests |
| `tests/pre_filter/test_arbitrage_exclusion.py` | Arbitrage gate tests | Same/opposite market logic uses market id. | Convert to condition/outcome semantics after whale pre-filter normalization. | medium | 0C-03 whale pre-filter canonical tests |
| `tests/pre_filter/test_intent_classifier.py` | Intent classifier tests | Fixtures, assertions, and results use market id. | Convert fixtures, classifier inputs, and result assertions to canonical fields. | medium | 0C-03 whale pre-filter canonical tests |
| `tests/pre_filter/test_market_quality.py` | Market quality tests | Redis setup and reject-cache assertions use market id. | Use token-scoped market-state and no `market_id` reject cache. | medium | 0A-03 tests |
| `tests/pre_filter/test_pipeline.py` | Pipeline test | Raw trade construction carries market id. | Add canonical input/output contract tests once event schema tests define expected failures. | medium | 0A-01B canonical event contract tests |
| `tests/signal_engine/conftest.py` | Qualified trade/signal fixtures | Uses market id. | Canonicalize fixtures after shared event contracts land. | medium | 0A-01B canonical event contract tests |
| `tests/signal_engine/test_consensus_filter.py` | Consensus tests/docstring | Redis key documented as `consensus_window(market_id, outcome)`. | Update to canonical consensus key semantics. | medium | 0A-01C static/Redis key contract tests |
| `tests/signal_engine/test_contrarian_detector.py` | Contrarian tests | Quote/history Redis keys use market id. | Use token-scoped quote/history keys. | medium | 0A-03 tests |
| `tests/signal_engine/test_ladder_detector.py` | Ladder tests | Repeated-trade grouping uses market id. | Convert grouping to canonical IDs after whale signal normalization. | medium | 0C-04 whale signal canonical tests |
| `tests/signal_engine/test_signal_decay.py` | Signal decay fixture | Signal fixture includes market id. | Canonicalize fixture after shared event contracts land. | medium | 0A-01B canonical event contract tests |
| `tests/telegram/conftest.py` | Proposal fixture | Builds market-id-only proposal. | Canonicalize approval fixtures after proposal contract lands. | medium | 0A-05 Telegram proposal queue tests |
| `tests/telegram/test_bot.py` | Telegram approval tests | Message body assertion requires market id. | Assert condition/token/outcome and optional slug display; approve by proposal ID. | medium | 0A-05 Telegram proposal queue tests |
| `docs/DATA_MODEL.md` | Canonical identifier/data-model guidance | Declares `market_id` deprecated; external IDs appear as `external_market_id` for research venue metadata. | No action in this ticket; use as schema source for 0A-06. | low | none |
| `docs/PHASE_0A_SHARED_RAIL.md` | Ticket 0A-01 source | Defines this inventory and contract-test plan. | No action; this doc implements the inventory. | low | none |
| `AGENTS.md` | Agent rules | Explicitly forbids routing on market id. | No action. | low | none |
| `MEG_MASTER_PRD_v4.1_patched.md` | Frozen master PRD | Frozen source of truth says legacy `market_id` is removed in Phase 0A. | Do not edit. | low | none |
| `MEG_MASTER_PRD.md` | Older master PRD | Similar canonical ID guidance for Phase 0. | Historical doc; do not prioritize. | low | none |
| `MEG_PRD_v3_final.md` | Legacy PRD examples | Many v3 examples use market id. | Historical doc; avoid using for Phase 0A contract decisions. | low | none |
| `CHANGELOG.md` | Historical release notes | Mentions legacy API/Redis/index changes. | No runtime impact; update only if changelog policy requires. | low | none |
| `STATUS.md` | Status note | Notes ABI decoding TODO for exact market id/outcome. | Update after Phase 0C decoder, not now. | low | 0C-00 Polygon receipt decoder contract tests |
| `TODOS.md` | Legacy TODOs | Several TODOs propose market-id keyed Redis/proposal metadata. | Supersede with Phase 0A tickets; avoid implementing legacy TODOs as written. | low | 0A-BACKLOG legacy TODO canonicalization cleanup |

## Contract-test plan

No tests are added in this ticket because the task is inventory-only and the allowed diff is intentionally small. The following tests should be added as failing/xfail skeletons or active tests in the next contract-test ticket before production migration.

### 1. Reject payloads missing canonical identifiers

Recommended file: `tests/core/test_canonical_id_contract.py`

- `test_raw_whale_trade_rejects_missing_condition_id`
- `test_raw_whale_trade_rejects_missing_token_id`
- `test_raw_whale_trade_rejects_missing_outcome`
- `test_qualified_whale_trade_rejects_missing_condition_id_token_id_or_outcome`
- `test_signal_event_rejects_missing_condition_id_token_id_or_outcome`
- `test_trade_proposal_rejects_missing_condition_id_token_id_or_outcome`
- `test_execution_request_rejects_missing_condition_id_token_id_or_outcome` once `ExecutionRequest` exists.

Acceptance expectation: Pydantic/model construction fails for missing or empty `condition_id`, `token_id`, or `outcome` on all shared-rail payloads. A payload containing only `market_id` must fail except in an explicitly approved boundary-shim test.

### 2. Verify `market_slug` is display-only

Recommended files: `tests/core/test_canonical_id_contract.py`, `tests/telegram/test_bot.py`, `tests/dashboard/test_api.py`

- `test_market_slug_optional_and_nullable_on_shared_events`
- `test_market_slug_not_required_for_routing_or_execution_request`
- `test_telegram_displays_market_slug_but_approves_by_proposal_id`
- `test_dashboard_displays_market_slug_but_action_payload_uses_canonical_ids`

Acceptance expectation: changing `market_slug` must not change Redis keys, DB natural IDs, execution request routing, duplicate-position detection, or approval callback identity.

### 3. Verify new shared-rail tables do not include `market_id`

Recommended file: `tests/db/test_phase0a_schema_contract.py`

- `test_signal_journal_has_condition_id_token_id_outcome_and_no_market_id`
- `test_proposal_current_state_has_condition_id_token_id_outcome_and_no_market_id`
- `test_proposal_state_transitions_has_no_market_id`
- `test_trade_journal_has_condition_id_token_id_outcome_and_no_market_id`
- `test_position_lots_has_condition_id_token_id_outcome_and_no_market_id`
- `test_daily_strategy_stats_has_no_market_id`

Acceptance expectation: SQLAlchemy/Alembic inspection of Phase 0A operational journal tables finds `condition_id`, `token_id`, and `outcome` where relevant and never finds a `market_id` column.

### 4. Verify boundary shims normalize before persistence/publication

Recommended files: `tests/data_layer/test_clob_client.py`, `tests/data_layer/test_polygon_feed.py`, `tests/dashboard/test_api.py`

- `test_clob_boundary_normalizes_legacy_market_id_to_token_id_before_redis_write`
- `test_clob_boundary_rejects_market_id_without_token_mapping`
- `test_polygon_boundary_does_not_publish_fabricated_market_id`
- `test_polygon_boundary_publishes_only_after_condition_token_outcome_decoded`
- `test_api_boundary_accepts_legacy_market_id_filter_only_if_translated_before_db_query`
- `test_boundary_shim_never_persists_market_id_to_phase0a_tables`

Acceptance expectation: a boundary may receive legacy `market_id` from an external API/client only if a deterministic mapping exists and the object published to Redis or written to Postgres contains canonical IDs and no internal `market_id` field.

### 5. Static/search contract checks

Recommended file: `tests/test_static_canonical_ids.py`

- `test_no_market_id_in_phase0a_shared_rail_modules_after_migration`
- `test_market_slug_only_in_display_allowlist`
- `test_redis_keys_do_not_define_market_id_routing_parameters`

Suggested allowlist after migration: frozen/historical docs, explicit external-boundary shim modules, and legacy Phase 0C whale-only code until that phase is migrated. The allowlist should be narrow and reviewed every ticket.

## Recommended next Codex tickets

Immediate next task:

**Ticket 0A-01B: Add canonical event contract xfail/failing tests only.**

Scope:

1. Add xfail or failing contract tests for `RawWhaleTrade`, `QualifiedWhaleTrade`, `SignalEvent`, `TradeProposal`, and the upcoming `ExecutionRequest` requiring `condition_id`, `token_id`, and `outcome`.
2. Add tests proving `market_id`-only payloads are rejected unless passed through a named boundary shim.
3. Do not add static search enforcement, Redis key migration, runtime producers/consumers, or schema migrations in this ticket.

Follow-up task:

**Ticket 0A-01C: Add static allowlist/search enforcement and Redis-key contract tests.**

Scope:

1. Add a narrow static allowlist for remaining `market_id` references so future tickets can reduce it deliberately.
2. Add Redis key contract tests proving Phase 0A routing keys use canonical `token_id`, `condition_id`, and `outcome` semantics instead of `market_id`.
3. Keep this separate from 0A-01B so the immediate next Codex task remains small and event-contract focused.

## Appendix A — `market_id` occurrence count by file

Counts were generated with `rg -n "market_id" . --glob '!*.git/*' --glob '!docs/phase0a/0A-01_CANONICAL_ID_INVENTORY.md'`. The appendix lists per-file occurrence-line counts only; it intentionally does not duplicate all 557 matching lines.

| File path | `market_id` occurrence lines |
| --- | ---: |
| `AGENTS.md` | 1 |
| `CHANGELOG.md` | 7 |
| `MEG_MASTER_PRD.md` | 4 |
| `MEG_MASTER_PRD_v4.1_patched.md` | 4 |
| `MEG_PRD_v3_final.md` | 21 |
| `STATUS.md` | 1 |
| `TODOS.md` | 5 |
| `docs/DATA_MODEL.md` | 6 |
| `docs/PHASE_0A_SHARED_RAIL.md` | 7 |
| `meg/agent_core/crowding_detector.py` | 2 |
| `meg/agent_core/decision_agent.py` | 11 |
| `meg/agent_core/position_manager.py` | 17 |
| `meg/agent_core/risk_controller.py` | 4 |
| `meg/agent_core/saturation_monitor.py` | 3 |
| `meg/agent_core/signal_aggregator.py` | 1 |
| `meg/agent_core/trap_detector.py` | 11 |
| `meg/core/events.py` | 36 |
| `meg/core/logger.py` | 2 |
| `meg/dashboard/api/main.py` | 19 |
| `meg/dashboard/ui/src/App.jsx` | 25 |
| `meg/data_layer/clob_client.py` | 23 |
| `meg/data_layer/polygon_feed.py` | 11 |
| `meg/data_layer/wallet_registry.py` | 7 |
| `meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py` | 7 |
| `meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py` | 3 |
| `meg/db/models.py` | 10 |
| `meg/execution/entry_filter.py` | 7 |
| `meg/execution/order_router.py` | 3 |
| `meg/execution/slippage_guard.py` | 11 |
| `meg/pre_filter/arbitrage_exclusion.py` | 8 |
| `meg/pre_filter/intent_classifier.py` | 7 |
| `meg/pre_filter/market_quality.py` | 24 |
| `meg/pre_filter/pipeline.py` | 10 |
| `meg/signal_engine/composite_scorer.py` | 2 |
| `meg/signal_engine/consensus_filter.py` | 3 |
| `meg/signal_engine/contrarian_detector.py` | 3 |
| `meg/signal_engine/ladder_detector.py` | 2 |
| `meg/telegram/bot.py` | 5 |
| `tests/agent_core/conftest.py` | 12 |
| `tests/agent_core/test_decision_agent.py` | 8 |
| `tests/agent_core/test_position_manager.py` | 13 |
| `tests/agent_core/test_risk_controller.py` | 1 |
| `tests/agent_core/test_trap_detector.py` | 27 |
| `tests/dashboard/test_api.py` | 9 |
| `tests/data_layer/test_clob_client.py` | 20 |
| `tests/data_layer/test_polygon_feed.py` | 6 |
| `tests/data_layer/test_wallet_registry.py` | 4 |
| `tests/db/test_models.py` | 7 |
| `tests/execution/conftest.py` | 8 |
| `tests/execution/test_order_router.py` | 3 |
| `tests/pre_filter/conftest.py` | 12 |
| `tests/pre_filter/test_arbitrage_exclusion.py` | 16 |
| `tests/pre_filter/test_intent_classifier.py` | 20 |
| `tests/pre_filter/test_market_quality.py` | 20 |
| `tests/pre_filter/test_pipeline.py` | 1 |
| `tests/signal_engine/conftest.py` | 4 |
| `tests/signal_engine/test_consensus_filter.py` | 2 |
| `tests/signal_engine/test_contrarian_detector.py` | 14 |
| `tests/signal_engine/test_ladder_detector.py` | 12 |
| `tests/signal_engine/test_signal_decay.py` | 1 |
| `tests/telegram/conftest.py` | 2 |
| `tests/telegram/test_bot.py` | 2 |
