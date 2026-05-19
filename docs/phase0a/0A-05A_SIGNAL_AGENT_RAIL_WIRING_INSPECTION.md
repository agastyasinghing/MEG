# Phase 0A-05A — Signal/Agent Rail Wiring Inspection

## 1) Status and purpose

**Status:** Documentation-only inspection (no runtime, test, workflow, or dependency changes).

**Purpose:** Map the QualifiedWhaleTrade → SignalEvent → agent-core path end-to-end, verify actual Redis publish/subscribe ownership, and choose the safest next Phase 0A step without entering proposal/execution behavior changes.

## 2) Completed Phase 0A boundary migrations (context)

Per prior Phase 0A documentation trail, the following boundary migrations/audits have already been completed:

1. RawWhaleTrade consumer boundary.
2. RawWhaleTrade publisher boundary.
3. QualifiedWhaleTrade publisher boundary.
4. Dashboard SignalEvent read-only feed boundary.

This ticket inspects the remaining unclear signal-engine ↔ agent-core runtime wiring.

## 3) Repository inspection commands used

The following commands were run for this inspection:

- `rg -n "CHANNEL_QUALIFIED_WHALE_TRADES|CHANNEL_SIGNAL_EVENTS|CHANNEL_TRADE_PROPOSALS" meg tests docs`
- `rg -n "QualifiedWhaleTrade|SignalEvent|TradeProposal" meg tests`
- `rg -n "composite_scorer|score\(" meg tests`
- `rg -n "signal_aggregator|decision_agent|evaluate\(" meg tests`
- `rg -n "publish\(|subscribe\(|listen\(|get_message\(" meg tests`
- `rg -n "model_validate_json|model_validate\(" meg tests`
- `rg -n "runner|worker|main|start|asyncio" meg tests`

Plus focused file reads of:
- `meg/main.py`
- `meg/pre_filter/pipeline.py`
- `meg/signal_engine/composite_scorer.py`
- `meg/agent_core/signal_aggregator.py`
- `meg/agent_core/decision_agent.py`
- `meg/dashboard/api/main.py`
- `meg/core/events.py`
- listed docs/tests in ticket scope.

## 4) Signal rail map (current production wiring)

### A. QualifiedWhaleTrade source

- `meg/pre_filter/pipeline.py::_process_event()` builds `QualifiedWhaleTrade` via `intent_classifier.build_qualified_trade(...)`, validates it via `validate_qualified_whale_trade_for_publish(...)`, then publishes JSON to `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES`.
- This is a confirmed production publisher seam.

### B. QualifiedWhaleTrade consumption after publish

- `meg/signal_engine/composite_scorer.py::score(trade, redis, session, config)` **consumes a `QualifiedWhaleTrade` object as a function argument** and returns a `SignalEvent` object.
- However, inspection found **no production Redis subscribe/listen loop in `meg/signal_engine`** that subscribes to `CHANNEL_QUALIFIED_WHALE_TRADES` and calls `composite_scorer.score(...)`.
- `meg/main.py` also does not start any signal-engine worker task.

**Conclusion:** after pre-filter publication, a production runtime subscriber/worker seam for `CHANNEL_QUALIFIED_WHALE_TRADES` is not evident in current wiring.

### C. SignalEvent creation

- `SignalEvent` is created inside `meg/signal_engine/composite_scorer.py::score()` (explicit `signal = SignalEvent(...)` construction).
- This is a model-construction seam, not by itself a Redis publisher seam.

### D. SignalEvent publication (if any)

- Inspection did **not** find a production `redis.publish(..., RedisKeys.CHANNEL_SIGNAL_EVENTS, ...)` in `meg/signal_engine`.
- `meg/core/events.py` and docstrings describe expected ownership (`signal_engine -> SignalEvent -> CHANNEL_SIGNAL_EVENTS`), but concrete signal-engine publish wiring is not found in inspected runtime code.

**Conclusion:** production publisher ownership exists conceptually, but concrete runtime publisher seam is currently unclear/missing in inspected code.

### E. SignalEvent consumption

- `meg/agent_core/signal_aggregator.py::run()` explicitly iterates `subscribe(redis, RedisKeys.CHANNEL_SIGNAL_EVENTS)`.
- `_validate_and_route()` parses inbound payload via `SignalEvent.model_validate_json(raw_data)`, applies de-dup + TTL checks, and routes valid signals to `decision_agent.evaluate(...)` when a DB session is available.

### F. Proposal-adjacent transition point

- In `signal_aggregator`, valid SignalEvent routing leads directly to `decision_agent.evaluate(...)`.
- In `decision_agent.evaluate(...)`, passing signals can produce and publish `TradeProposal` to `RedisKeys.CHANNEL_TRADE_PROPOSALS`.
- Therefore, the SignalEvent consumer boundary is proposal/execution-adjacent even though it is not direct order placement.

## 5) Direct answers to required questions

1. **Where is QualifiedWhaleTrade consumed after pre-filter publishes it?**  
   No production subscriber loop was found in `meg/signal_engine`; only function-level consumption by `composite_scorer.score(trade, ...)` is visible.

2. **Is there a production subscriber for `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES`?**  
   Not found in inspected production runtime wiring.

3. **Where is SignalEvent created?**  
   `meg/signal_engine/composite_scorer.py::score()`.

4. **Is there a production publisher for `RedisKeys.CHANNEL_SIGNAL_EVENTS`?**  
   Not found in inspected signal-engine runtime code.

5. **Where is SignalEvent consumed?**  
   `meg/agent_core/signal_aggregator.py::run()` / `_validate_and_route()`.

6. **Does `signal_aggregator.run()` subscribe directly to `CHANNEL_SIGNAL_EVENTS`?**  
   Yes.

7. **Does valid SignalEvent consumption immediately call `decision_agent.evaluate()`?**  
   Yes (when session is present); otherwise it logs `signal_aggregator.no_session` and does not route.

8. **Is the next migration safe, or too proposal/execution-adjacent?**  
   Direct agent-core SignalEvent consumer migration is proposal-adjacent and higher risk; safest next step is documentation/test preflight around missing signal-engine wiring first.

9. **Is there missing runtime wiring between signal_engine and agent_core?**  
   Yes, or at minimum unresolved ownership: no explicit production signal-engine subscriber (`qualified_whale_trades`) and no explicit production signal-engine publisher (`signal_events`) were found.

10. **What exact file/function should be inspected or planned next?**  
    `meg/main.py::_main()` task wiring plus a new/identified signal-engine runner entrypoint (expected seam: subscribe `CHANNEL_QUALIFIED_WHALE_TRADES` → call `composite_scorer.score()` → publish `CHANNEL_SIGNAL_EVENTS`).

## 6) Gap analysis

### Confirmed gaps

- **Missing/unclear qualified-trade subscriber seam:** no production runtime consumer of `CHANNEL_QUALIFIED_WHALE_TRADES` found in `meg/signal_engine`.
- **Missing/unclear signal-event publisher seam:** no production runtime publisher to `CHANNEL_SIGNAL_EVENTS` found in `meg/signal_engine`.
- **Main task wiring mismatch:** `meg/main.py` comments indicate `signal_aggregator` processes qualified trades, but implementation subscribes to signal events; no signal-engine worker is started.

### Ownership ambiguity

- Contract docs and model docstrings assign channel ownership, but concrete worker ownership for converting qualified trades into published signal events is not presently explicit in runtime startup wiring.

## 7) Candidate next steps

| Option | Files/functions | Risk level | Recommendation |
|---|---|---|---|
| Signal-engine worker/publisher wiring inspection | `meg/main.py::_main()`, potential signal-engine runner module (to be identified), `meg/signal_engine/composite_scorer.py::score()` | Medium | **Recommended now (docs/test-only planning first).** Clarifies ownership before any boundary migration touching proposal-adjacent paths. |
| SignalEvent publisher boundary plan | Expected publisher seam in signal-engine runner once identified | Medium-high | Defer until concrete publisher function exists/is identified. |
| Agent-core SignalEvent consumer preflight plan | `meg/agent_core/signal_aggregator.py::run()/_validate_and_route()` | Medium-high | Defer as runtime migration; keep only preflight/docs until upstream wiring is explicit. |
| Test-only integration seam (`QualifiedWhaleTrade -> SignalEvent -> SignalAggregator`) | New test harness only (no prod changes) | Medium | Good companion after runner ownership is documented; enables safety checks without altering runtime. |
| Pause Phase 0A runtime migrations, shift to 0B planning | docs planning only | Low | Contingency if runtime ownership remains unresolved after one focused wiring-inspection ticket. |

## 8) Recommended next ticket

**Exact title:** `Phase 0A-05B Signal-Engine Runner Ownership & Wiring Plan (Docs/Test-Only)`

**Why this is safest:**
- Resolves missing ownership/wiring ahead of any proposal-adjacent boundary migration.
- Avoids touching scoring logic, decision logic, approval, or execution behavior.
- Produces a concrete seam for subsequent boundary migration with lower blast radius.

**Allowed files:**
- `docs/phase0a/*` planning document(s)
- optionally `tests/` for non-runtime, seam-detection/integration-contract tests only

**Tests required (docs/test-only):**
- Add/extend tests proving expected channel contract sequence at seam level (qualified input accepted, signal output expected) via mocks/fakes.
- Add a startup-wiring assertion test (or equivalent static contract check) that fails when no signal-engine worker is registered.

**Non-goals:**
- No production worker implementation.
- No strategy/scoring behavior changes.
- No decision-agent/proposal/execution logic changes.
- No Telegram/dashboard approval-path changes.
- No dependency/workflow changes.

**Rollback / kill criteria:**
- If inspection cannot identify a single owner module/function for signal-engine runtime wiring without production edits, stop runtime Phase 0A migrations and move to Phase 0B/DuckDB planning until ownership is explicitly defined.

## 9) Documentation-only confirmation

This ticket performed inspection and documentation only. No production source, tests, workflows, dependencies, or frozen PRD documents were modified.
