# Phase 0A-05G — Signal-engine runner post-wiring audit

## Scope and intent

This ticket is a **documentation-only** post-wiring audit for Phase 0A shared rail work.

It verifies the current runtime event rail after the signal-engine runner startup wiring, confirms boundary migrations completed so far, lists safeguards that remain unchanged, and records deferred items that remain intentionally out of scope.

## Current runtime rail map (as wired now)

End-to-end shared-event rail sequence:

1. `polygon_feed` publishes `raw_whale_trades`.
2. `pre_filter` consumes `raw_whale_trades`.
3. `pre_filter` publishes `qualified_whale_trades`.
4. `signal_engine_runner` consumes `qualified_whale_trades`.
5. `signal_engine_runner` publishes `signal_events`.
6. `signal_aggregator` consumes `signal_events`.
7. `signal_aggregator` validates/deduplicates/TTL-checks and routes valid signals toward `decision_agent`.

Runtime ownership boundaries remain aligned to shared rail design:

- `signal_engine.runner` owns qualified-trade consumption and signal-event publishing.
- `agent_core.signal_aggregator` owns signal-event intake hygiene and routing toward `decision_agent`.
- `agent_core.decision_agent` remains the final gate to `trade_proposals` and operator approval flow.

## Completed Phase 0A boundary migrations (to date)

The following boundary migrations or shared-rail wiring deliverables are now complete for Phase 0A:

1. **RawWhaleTrade consumer boundary validation** completed.
2. **RawWhaleTrade publisher boundary validation** completed.
3. **QualifiedWhaleTrade publisher boundary validation** completed.
4. **Dashboard SignalEvent read-only feed boundary** documented/retained.
5. **Signal-engine runner skeleton** implemented with explicit consume/publish contracts.
6. **Main startup wiring** includes exactly one `signal_engine_runner` task registration alongside existing core tasks.

## Safety confirmations (no behavior drift)

This wiring audit confirms no intentional behavior change in the following protected areas:

1. `decision_agent` behavior remains unchanged as Phase 0A risk/approval gate.
2. Execution/order placement path remains unchanged.
3. Telegram approval authority remains unchanged (operator-in-the-loop required).
4. DB models and migrations remain unchanged in this ticket.
5. Workflows and dependencies remain unchanged in this ticket.
6. Strategy/scoring formulas remain unchanged in this ticket.

## Tests protecting this wiring and contract continuity

The wiring is protected by existing contract-focused tests:

1. **Startup wiring contract** (`tests/core/test_signal_engine_startup_wiring_contract.py`)
   - verifies `main.py` imports `signal_engine_runner`
   - verifies runner task is wired once
   - verifies existing core task names remain present
2. **Runner contract checks** (`tests/core/test_signal_engine_runner_contract.py`)
   - verifies module run callable contract
   - verifies consume/publish Redis channel ownership constants
   - verifies qualified trade and signal event payload boundary behaviors
3. **Signal-engine runner tests** (`tests/signal_engine/test_runner.py`)
   - verifies valid qualified payload invokes scoring
   - verifies scored signal publishes to `signal_events`
   - verifies malformed/wrong-type/bad-schema inputs fail closed
   - verifies Redis disconnect propagation behavior
4. **Core event JSON/envelope contract coverage**
   - retained via event model validation and boundary fixture round-trip checks used by contract tests above.

## Remaining deferred items (explicitly not done yet)

The following remain deferred by design and are **not** introduced in this ticket:

1. No live autonomous execution changes.
2. No `TradeProposal` boundary migration yet.
3. No approval/order-router migration yet.
4. No DuckDB historical lake implementation yet.
5. No weather engine implementation yet.
6. No swing bot / sidecar strategy implementation yet.
7. No Polymarket repo feature-mining backlog implementation yet.

## Phase decision

Recommendation: **one more tiny Phase 0A preflight/audit ticket, then pause runtime rail changes and begin Phase 0B DuckDB planning.**

Rationale:

- The raw → qualified → signal rail is now wired and contract-tested.
- The highest-value immediate risk reducer is a narrow interface/ownership preflight on the **downstream proposal boundary** (signal -> proposal handoff assertions and observability checklist) without changing runtime behavior.
- After that, further runtime touching in 0A should pause in favor of 0B data-plane planning to avoid scope creep and preserve rail stability.

## Recommended next ticket

**0A-05H — TradeProposal boundary + approval handoff preflight (documentation-only).**

Suggested acceptance criteria:

1. Document current `signal_aggregator` -> `decision_agent` -> `trade_proposals` boundary contract and ownership.
2. Enumerate invariant checks for proposal TTL/approval latency/operator-action journaling fields.
3. Confirm no execution autonomy introduced.
4. Confirm no code/test/workflow/dependency changes.
5. Reference existing tests and identify any missing contract tests to be added in a later code ticket (not in the doc ticket).
