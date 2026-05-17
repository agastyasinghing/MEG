# Phase 0A Shared Rail

Derived from `MEG_MASTER_PRD_v4.1_patched.md` v4.1. This document turns Phase 0A into implementation-ready tickets. It intentionally stops at shared rail documentation and does not define weather strategy code, whale strategy code, or live autonomous execution.

## Phase objective

Build the shared Polymarket execution and research rail that any strategy can plug into:

- Canonical identifiers.
- Versioned event schemas and Redis contracts.
- CLOB market-state cache.
- Authenticated user-stream service.
- Telegram operator approval queue.
- Postgres operational journal.
- Paper execution simulator.
- Heartbeat and health alerts.
- Risk envelope skeleton.

Phase 0A is a prerequisite for Phase 1. It must allow an end-to-end paper flow without whale-specific runtime dependencies.

## Non-goals

- Do not implement weather strategy generation.
- Do not implement whale strategy generation.
- Do not create autonomous execution authority.
- Do not modify the frozen master PRD.
- Do not add Phase 0B lake ingestion beyond respecting the data contracts.
- Do not add Phase 0C Polygon decoder or whale runner implementation except where needed to define shared contracts.

## Phase exit gates

Phase 0A exits only when all of the following are true:

1. A strategy can run in paper mode through `signals -> proposals -> approvals -> simulated execution -> journal closure` without whale-specific code in the runtime path.
2. 25 paper trades exercise the full proposal-to-journal lifecycle with zero unreconciled state.
3. Telegram dispatches structured proposal messages and supports `/approve`, `/reject`, and `/defer` with approval latency journaled on every transition.
4. Heartbeat publishes every 60 seconds with all health indicators populated.
5. Risk envelope refuses an order that breaches the per-position cap in a synthetic test.
6. Phase 0A unit tests pass, with a target of 80%+ line coverage on rail-adjacent modules.

## Ticket 0A-01: Canonical identifier migration

**Priority:** P0
**Estimate:** 8h
**Dependencies:** None

### Goal

Make `condition_id`, `token_id`, and `outcome` the canonical routing identifiers across shared-rail schemas, Redis payloads, Postgres journals, and tests. Remove new internal dependence on legacy `market_id`.

### Implementation notes

- Inventory current event schemas, Redis publishers/subscribers, DB models, fixtures, and tests that use `market_id`.
- Replace shared-rail routing fields with `condition_id`, `token_id`, and `outcome`.
- Keep `market_slug` only as nullable display metadata.
- If a boundary still receives `market_id` from an external source, normalize at the boundary and do not persist `market_id` in Phase 0A tables.
- Update test fixtures so they fail when canonical identifiers are missing.

### Acceptance criteria

- All Phase 0A event schemas include required `condition_id`, `token_id`, and `outcome` fields.
- No new shared-rail Postgres table contains a `market_id` column.
- No Phase 0A Redis payload routes or matches on `market_id`.
- Boundary shims, if unavoidable, are explicitly named and covered by tests.
- Contract tests reject events missing `condition_id`, `token_id`, or `outcome`.

### Suggested tests

- Schema validation tests for missing canonical identifiers.
- Fixture migration tests proving old `market_id`-only payloads are rejected or normalized only at approved boundaries.
- Static check or targeted search for forbidden `market_id` usage in Phase 0A modules.

## Ticket 0A-02: Event schemas and Redis bus contracts

**Priority:** P0
**Estimate:** 5h
**Dependencies:** 0A-01

### Goal

Define versioned schemas for `RawWhaleFill`, `QualifiedWhaleFill`, `Signal`, `TradeProposal`, `ExecutionRequest`, `UserFill`, and `MarketState`, then enforce the Redis channel ownership matrix.

### Implementation notes

- Add schema versioning starting at `schema_version = 1`.
- Keep strategy-specific details inside `metadata` or `score_breakdown` rather than adding shared fields.
- Enforce channel ownership:
  - `signal_events` is written by strategy signal workers.
  - `trade_proposals` is written by the decision agent.
  - `execution_requests` is written by Telegram approval handling.
  - `fills.user` is written by the authenticated user-stream service.
  - `bot_alerts` can be written by any module.
  - `market:{token_id}:*` is written by the market-state feed only.
- Treat whale-specific channels as shared contracts only; Phase 0C owns their producers/consumers.

### Acceptance criteria

- Versioned schemas are documented and machine-validated for all Phase 0A payloads.
- Redis channel ownership matrix is represented in documentation and code review checklist or tests.
- Invalid payloads are rejected before publication.
- Consumers can dispatch based on `event_type` and `schema_version`.
- No module writes to a channel it does not own.

### Suggested tests

- Valid payload round-trip tests for every schema.
- Invalid payload tests for missing identifiers, invalid side/outcome, expired proposals, and non-finite probabilities.
- Publisher ownership tests using mocked Redis clients.

## Ticket 0A-03: CLOB market-state cache writer

**Priority:** P0
**Estimate:** 7h
**Dependencies:** 0A-01, 0A-02

### Goal

Publish fresh bid/ask/spread/liquidity/volume/category state for watched Polymarket outcome tokens to Redis, so pre-filter, paper execution, and monitoring do not call REST directly in hot paths.

### Implementation notes

- Read the active token watch list from `meg:active_markets`.
- Subscribe to Polymarket CLOB market data for watched `token_id` values.
- Publish latest state to `market:{token_id}:state`, a concrete member of the master PRD's `market:{token_id}:*` namespace.
- Publish book depth to `market:{token_id}:book` if the paper simulator requires it; this is also a concrete member of the `market:{token_id}:*` namespace, not a replacement contract.
- Include `ts_updated_ms`, `condition_id`, `token_id`, `outcome`, `best_bid`, `best_ask`, `mid`, `spread_bps`, `liquidity_pusd`, `volume_24h_pusd`, `category`, `neg_risk`, and `tick_size` where available.
- Emit `bot_alerts` when market cache age exceeds the configured staleness threshold.

### Acceptance criteria

- Cache writer publishes a valid `MarketState` payload for each watched token.
- Every payload contains canonical identifiers.
- Staleness alarms fire when a watched market has no fresh update within threshold.
- Paper execution can read market state without direct REST calls.
- Health status reports stale market count to heartbeat.

### Suggested tests

- Unit tests using mocked CLOB updates.
- Redis integration test with a temporary watched token set.
- Staleness timer test with frozen/deterministic time.

## Ticket 0A-04: CLOB user-stream service

**Priority:** P0
**Estimate:** 7h
**Dependencies:** 0A-01, 0A-02

### Goal

Subscribe to the authenticated Polymarket user WebSocket and publish authoritative user fills to `fills.user` for reconciliation and journal closure.

### Implementation notes

- Authenticate using the existing Polymarket credentials flow.
- Normalize user fill payloads to the `UserFill` schema.
- Correlate fills to `execution_id` and `proposal_id` when possible.
- Preserve raw fill payloads in `raw` for audit diagnostics.
- Reconnect with backoff, but surface prolonged disconnects to `bot_alerts`.

### Acceptance criteria

- User stream publishes valid `UserFill` events to `fills.user`.
- Fill events contain `condition_id`, `token_id`, `outcome`, price, size, fee, order ID, and trade ID where provided.
- Reconciler can consume fill events and update `trade_journal` lifecycle state.
- Heartbeat reports `poly user ws OK` only when the stream is connected and fresh.
- Disconnects and malformed payloads emit operator alerts.

### Suggested tests

- Mock WebSocket payload normalization tests.
- Reconnect/backoff tests.
- Fill-to-execution correlation tests.

## Ticket 0A-05: Telegram proposal queue infrastructure

**Priority:** P0
**Estimate:** 7h
**Dependencies:** 0A-02

### Goal

Harden the existing Telegram bot into the required operator approval plane for all execution. Every proposal must be approved, rejected, deferred, or expired; nothing auto-executes.

### Implementation notes

- Consume `TradeProposal` objects from `trade_proposals`.
- Render structured messages with signal ID, strategy, condition ID, slug, side, size, model probability, market probability, estimated edge, expiry, and risk envelope.
- Support `/approve`, `/reject`, and `/defer` commands.
- On approve, publish `ExecutionRequest` to `execution_requests`.
- On reject/defer/expire, append an immutable row to `proposal_state_transitions` and update `proposal_current_state`.
- Defer should requeue for strategy/decision-agent re-evaluation, not execute.
- Track `approval_latency_ms` for every terminal or deferred transition.
- Support `/halt <reason>` and `/resume`; resume requires typed confirmation.
- Multi-operator support is a design decision requiring explicit operator consensus before implementation.

### Acceptance criteria

- Structured proposal messages include all required decision fields.
- `/approve` publishes exactly one valid `ExecutionRequest` for a non-expired proposal.
- `/reject` records rejection and never publishes an execution request.
- `/defer` records defer state and requeues for re-evaluation.
- Expired proposals are dropped, not auto-approved.
- Approval latency is written for approve, reject, defer, and expire transitions.
- Every proposal transition persists timestamp, actor, previous state, next state, reason/notes, and latency where applicable.
- `/halt <reason>` journals a halt event, blocks new execution requests/submissions, and cancels open orders where applicable.
- `/resume` requires typed confirmation before new submissions are allowed.
- Heartbeat displays halted mode and reason.

### Suggested tests

- Command handler unit tests for approve/reject/defer/expired proposal paths.
- Idempotency tests ensuring duplicate approval commands do not duplicate execution requests.
- Journal assertions for transition timestamps and latency.

## Ticket 0A-06: Postgres journal schema and writers

**Priority:** P0
**Estimate:** 6h
**Dependencies:** 0A-01, 0A-02

### Goal

Create and exercise the operational journal tables: `signal_journal`, `proposal_current_state`, `proposal_state_transitions`, `trade_journal`, `position_lots`, and `daily_strategy_stats`.

### Implementation notes

- Use `docs/DATA_MODEL.md` as the DDL source.
- Store operational facts only: signals, proposals, approvals, execution attempts, fills, positions, audit transitions, and daily rollups.
- Do not store raw quote streams or historical market data in Postgres.
- Ensure writers are idempotent by natural IDs such as `signal_id`, `proposal_id`, and `execution_id`.
- Add indexes specified by the data model.

### Acceptance criteria

- All Phase 0A operational journal tables are created by migration.
- Writers can insert signal, proposal current-state, immutable proposal-transition, trade, position, and daily stats records in paper mode.
- Duplicate event handling is idempotent or safely rejected with clear errors.
- Indexes exist for required lookup paths.
- Journal records can reconstruct a full proposal-to-fill lifecycle.
- Proposal audit history is immutable and transition-safe across repeated defer/requeue cycles.
- Daily/end-of-session reconciliation compares journal open positions against user-channel balances.
- Reconciliation discrepancies emit high-priority alerts and block startup until operator acknowledgement.

### Suggested tests

- Migration upgrade/downgrade test if the migration framework supports it.
- Repository/writer unit tests with a temporary Postgres database.
- End-to-end paper lifecycle journal test.

## Ticket 0A-07: Paper execution simulator

**Priority:** P0
**Estimate:** 5h
**Dependencies:** 0A-03, 0A-06

### Goal

Implement `paper` mode for the execution rail using the same interface as future live mode. Paper fills simulate against market-state cache and close the journal lifecycle without venue submission.

### Implementation notes

- Consume approved `ExecutionRequest` payloads.
- Read latest `MarketState` and optional book depth from Redis.
- Enforce price constraints and risk envelope before simulated fill.
- Generate trade journal state transitions: requested, submitted, posted, filled, partially_filled, partially_filled_closed_out, cancelled/rejected, reconciled.
- Generate `position_lots` records for filled orders.
- Treat stale market cache as a hard rejection.

### Acceptance criteria

- Paper execution accepts valid approved requests and simulates fills against fresh market state.
- Paper execution refuses stale-cache orders.
- Paper execution refuses orders violating price constraints or risk gates.
- Shared market/execution gates reject orders with liquidity below floor, spread above ceiling, mid-price outside allowed bounds, stale market cache, near-resolution timing, or incomplete canonical identifiers.
- `trade_journal` distinguishes in-progress `partially_filled` from terminal `partially_filled_closed_out`.
- Any order stuck in `posted` for more than 60 seconds without venue acknowledgement emits a high-priority reconciliation alert visible in heartbeat/health output.
- Every paper order reaches a terminal journal state.
- A 25-trade paper run completes with zero unreconciled state.

### Suggested tests

- Simulated fill tests for bid/ask crossing behavior.
- Stale cache rejection test.
- Price constraint rejection test.
- 25-trade deterministic lifecycle test.

## Ticket 0A-08: Heartbeat emitter

**Priority:** P1
**Estimate:** 3h
**Dependencies:** 0A-03, 0A-04, 0A-05, 0A-06

### Goal

Emit a structured heartbeat to Telegram every 60 seconds during active sessions and on strategy state changes.

### Implementation notes

Heartbeat should include:

- Timestamp and mode: `paper`, `live`, `mixed`, or `halted`.
- Approval-first status.
- Pause/halt state and reason.
- Signal/proposal/approval/fill counts over the last 60 minutes.
- Top strategy, net PnL today, and open exposure versus cap.
- Detect, proposal-to-approval, and submit-to-ack p50/p95 latency.
- Health for market WebSocket, user WebSocket, Gamma, Redis, Postgres, and replay lag.
- Guardrails: drawdown, slippage p95, stale cache count, rejected orders.

### Acceptance criteria

- Heartbeat publishes every 60 seconds during active sessions and immediately on every strategy state change.
- Heartbeat includes every required health indicator.
- Any non-OK health indicator escalates to a priority alert.
- Heartbeat uses journal/cache data rather than strategy-specific internals.
- Halted mode is clearly displayed.

### Suggested tests

- Formatting snapshot test for heartbeat message.
- Health aggregation unit tests.
- Timer test with deterministic time.
- Alert escalation test for a non-OK dependency.

## Ticket 0A-09: Risk envelope skeleton

**Priority:** P1
**Estimate:** 2h
**Dependencies:** 0A-06, 0A-07

### Goal

Enforce the first shared risk gates at the rail level for paper trades. The same interface must be reusable for live mode in Phase 2.

### Implementation notes

- Configure per-position cap, daily exposure cap, and daily loss limit in config.
- Evaluate risk before order submission/simulation.
- Return structured reject reasons to `trade_journal`.
- Include open exposure and drawdown in heartbeat.
- Keep weather-specific anomaly veto out of Phase 0A implementation; this ticket only defines shared risk gates.

### Acceptance criteria

- Paper rail refuses an order breaching per-position cap in a synthetic test.
- Paper rail refuses an order breaching daily exposure cap.
- Paper rail refuses new orders after daily loss limit breach.
- Reject reasons are journaled and visible in alerts/heartbeat.
- Risk interface is mode-agnostic and can be called by both paper and live rail.

### Suggested tests

- Per-position cap rejection test.
- Daily exposure cap rejection test.
- Daily loss limit rejection test.
- Journaled reject reason assertion.

## Recommended implementation order

1. 0A-01 Canonical identifier migration.
2. 0A-02 Event schemas and Redis contracts.
3. 0A-06 Postgres journal schema and writers.
4. 0A-03 Market-state cache and 0A-04 user stream in parallel.
5. 0A-05 Telegram proposal queue.
6. 0A-07 Paper execution simulator.
7. 0A-09 Risk envelope skeleton.
8. 0A-08 Heartbeat emitter.
9. Full 25-trade paper lifecycle verification.

## Definition of done for Phase 0A documentation

- `AGENTS.md` gives practical repo-agent guardrails.
- `docs/DATA_MODEL.md` documents identifiers, event schemas, Redis contracts, Postgres tables, and DuckDB views derived from the master PRD.
- `docs/PHASE_0A_SHARED_RAIL.md` converts the master PRD Phase 0A scope into implementation-ready tickets with acceptance criteria.
