# Phase 0A-05B — Signal-Engine Runner Ownership & Wiring Plan

## 1) Status and objective

**Status:** Documentation-only plan. No production runtime wiring, strategy logic, decision-agent behavior, execution behavior, Telegram flow, DB models, workflows, or dependency files are changed in this ticket.

**Objective:** Define ownership, runtime contract, startup registration plan, and pre-implementation tests for the missing signal-engine runner seam between:

- `qualified_whale_trades` producer (`pre_filter`), and
- `signal_events` consumer (`agent_core.signal_aggregator`).

This plan is scoped to Phase 0A shared-rail wiring and preserves operator-approved execution authority requirements.

---

## 2) Repository inspection commands used

The following commands were used to verify current wiring/state:

- `rg -n "CHANNEL_QUALIFIED_WHALE_TRADES|CHANNEL_SIGNAL_EVENTS" meg tests docs`
- `rg -n "QualifiedWhaleTrade|SignalEvent" meg tests`
- `rg -n "composite_scorer|score\(" meg tests`
- `rg -n "publish\(|subscribe\(|listen\(|get_message\(" meg tests`
- `rg -n "runner|worker|main|start|asyncio" meg tests`
- `rg -n "decision_agent|evaluate\(" meg tests`

Focused reads were also performed in ticket-specified files, including `meg/main.py`, `meg/pre_filter/pipeline.py`, `meg/signal_engine/composite_scorer.py`, `meg/agent_core/signal_aggregator.py`, and related docs/tests.

---

## 3) Current rail state (confirmed)

### 3.1 QualifiedWhaleTrade publisher exists

- `meg/pre_filter/pipeline.py::_process_event()` builds/validates a `QualifiedWhaleTrade` and publishes to `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES`.

### 3.2 SignalEvent model construction exists

- `meg/signal_engine/composite_scorer.py::score(...)` accepts a `QualifiedWhaleTrade` object and constructs/returns a `SignalEvent`.

### 3.3 SignalEvent consumer exists

- `meg/agent_core/signal_aggregator.py::run()` subscribes to `RedisKeys.CHANNEL_SIGNAL_EVENTS`.
- Valid `SignalEvent` payloads route to `decision_agent.evaluate(...)` when session is present.

### 3.4 Missing runner/publisher seam

- No clear production signal-engine worker/runner was found that:
  1. subscribes to `CHANNEL_QUALIFIED_WHALE_TRADES`,
  2. calls `composite_scorer.score(...)`, and
  3. publishes `SignalEvent` to `CHANNEL_SIGNAL_EVENTS`.
- `meg/main.py` currently starts `polygon_feed`, `pre_filter_pipeline`, `signal_aggregator`, `position_manager`, and `telegram_bot`; it does not start a dedicated signal-engine runner task.

---

## 4) Proposed ownership (future ticket)

### 4.1 Proposed module/function owner

**Proposed owner:** `meg/signal_engine/runner.py::run(redis, config)`

This future runner should be the sole production owner for qualified-trade consumption and signal-event publication in the signal-engine layer.

### 4.2 Ownership contract

- **Input ownership:** subscribe/consume `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES`.
- **Transformation ownership:** parse + validate `QualifiedWhaleTrade`, then call `composite_scorer.score(...)`.
- **Output ownership:** validate `SignalEvent` payload for publish and publish to `RedisKeys.CHANNEL_SIGNAL_EVENTS`.
- **Non-ownership:** no decision-agent evaluation, no proposal publishing, no execution/approval actions.

---

## 5) Proposed future runtime flow (implementation target, not implemented here)

1. Subscribe: `subscribe(redis, RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES)`.
2. Parse/validate inbound JSON as `QualifiedWhaleTrade` (event type + schema version checks through shared validator helpers).
3. Open/get DB session as required by `composite_scorer.score(...)` dependencies.
4. Call `composite_scorer.score(trade, redis, session, config)`.
5. Handle scorer outcomes:
   - If `SignalDroppedError` or no-signal semantics apply, fail closed and do not publish.
   - If `SignalEvent` is returned, validate publish payload.
6. Publish validated `SignalEvent` to `RedisKeys.CHANNEL_SIGNAL_EVENTS`.
7. Preserve Redis disconnect error propagation (do not silently swallow connection loss).

---

## 6) Startup wiring plan (future)

### 6.1 Planned main registration

Future ticket should register a dedicated task in `meg/main.py::_main()` TaskGroup, for example:

- `tg.create_task(signal_engine_runner.run(redis, config), name="signal_engine_runner")`

### 6.2 Non-goals for this ticket (explicit)

- No edits to `meg/main.py` now.
- No production runner implementation now.
- No score formula, thresholds, or strategy changes.
- No `decision_agent` behavior changes.
- No Telegram/risk/execution/order placement changes.
- No DB model/migration changes.

---

## 7) Required tests before implementation (acceptance checklist)

The future runner implementation ticket must include test coverage for:

1. **Valid qualified payload path**
   - Runner consumes valid `QualifiedWhaleTrade` payload from qualified channel.

2. **Invalid qualified payload path (fail closed)**
   - Malformed JSON, wrong `event_type`, unsupported `schema_version`, or invalid model payload is rejected/skipped without publish.

3. **Signal publish success path**
   - `score()` returning `SignalEvent` results in one publish to `RedisKeys.CHANNEL_SIGNAL_EVENTS`.

4. **No-signal path**
   - `score()` returning `None`/drop semantics (if applicable by implementation) produces no publish.

5. **Redis disconnect semantics**
   - Runner preserves disconnect propagation behavior from subscribe loop (no silent event loss).

6. **Isolation from decision/execution paths**
   - Runner does not call `decision_agent.evaluate()`.
   - Runner does not touch execution/order/approval channels or behavior.

---

## 8) Candidate next ticket

Recommended next ticket:

- **Phase 0A-05C Signal-Engine Runner Test-Only Contract**

If the test contract clarifies the seam sufficiently, follow with:

- **Phase 0A-05C Signal-Engine Runner Skeleton**

Rationale: preserving Phase 0A small-ticket discipline and contract-first validation before any production runtime wiring.

---

## 9) Kill criteria / stop-and-defer conditions

Stop implementation and defer if runner work requires any of:

- strategy/scoring behavior changes,
- `decision_agent` behavior changes,
- DB schema/model changes,
- execution- or order-router-adjacent behavior changes,
- Telegram approval flow changes.

If any of the above becomes necessary, pause and open a separate scoped design ticket before continuing.

---

## 10) Documentation-only confirmation

This Phase 0A-05B ticket is documentation-only and intentionally does **not** implement production worker wiring.
