# Phase 0A-04E Next Boundary Inspection After Qualified Publisher

Status: documentation-only planning inspection for the next Phase 0A shared-event migration after the completed `QualifiedWhaleTrade` publisher boundary work. This document does not modify production code, tests, workflows, dependencies, DB models, or the frozen PRD.

## 1) Status and purpose

Phase 0A has now completed the three boundary migrations listed below. The goal of this note is to inspect remaining shared-event seams and select **exactly one** safest next boundary for Phase 0A-04F, with preference for non-execution/read-only risk profile and a single-function implementation seam.

## 2) Recently completed migrations

1. RawWhaleTrade consumer boundary
   - `meg/pre_filter/pipeline.py::run()`
   - `RedisKeys.CHANNEL_RAW_WHALE_TRADES`
2. RawWhaleTrade publisher boundary
   - `meg/data_layer/polygon_feed.py::_emit_event()`
   - `RedisKeys.CHANNEL_RAW_WHALE_TRADES`
3. QualifiedWhaleTrade publisher boundary
   - `meg/pre_filter/pipeline.py::_process_event()`
   - `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES`

## 3) Repository inspection commands used

```bash
rg -n "CHANNEL_QUALIFIED_WHALE_TRADES|CHANNEL_SIGNAL_EVENTS|CHANNEL_TRADE_PROPOSALS" meg tests docs
rg -n "QualifiedWhaleTrade|SignalEvent|TradeProposal" meg tests
rg -n "publish\(|\.publish\(" meg tests
rg -n "subscribe\(|listen\(|get_message\(" meg tests
rg -n "model_validate_json|model_validate\(" meg tests
rg -n "approve_signal|feed_signals|decision_agent|signal_aggregator|composite_scorer|runner" meg tests
```

Additional direct reads were performed for the files requested in this ticket, including `meg/core/events.py`, `meg/signal_engine/composite_scorer.py`, `meg/agent_core/signal_aggregator.py`, `meg/agent_core/decision_agent.py`, and `meg/dashboard/api/main.py`.

## 4) Candidate boundary table

| Boundary name | File/function | Event model/channel | Producer or consumer | Risk level | Recommendation / defer reason |
| --- | --- | --- | --- | --- | --- |
| Signal-engine qualified-trade runtime consumer | No clear runtime subscribe runner found in `meg/signal_engine` for qualified-trade channel | Expected `QualifiedWhaleTrade` / `CHANNEL_QUALIFIED_WHALE_TRADES` | Consumer candidate, but seam not concretely wired in inspected runtime path | High | **Defer**. Not a single explicit runtime seam yet; selecting this now likely forces wiring/runner work, which violates this ticket's documentation-first and non-wiring constraints. |
| SignalEvent publisher candidate | `meg/signal_engine/composite_scorer.py::score()` | Builds `SignalEvent`; no direct `CHANNEL_SIGNAL_EVENTS` publish in this function | Model constructor, not confirmed publish seam | High | **Defer**. This function appears scoring/model-construction adjacent; migrating here risks strategy/scoring adjacency and ambiguous producer boundary ownership. |
| Agent-core SignalEvent consumer | `meg/agent_core/signal_aggregator.py::run()` + `_validate_and_route()` | `SignalEvent` / `CHANNEL_SIGNAL_EVENTS` | Consumer | Medium-high | **Defer for now**. Single seam exists, but valid signals route immediately into `decision_agent.evaluate()` (proposal path), so changes here are proposal/execution-adjacent. |
| Agent-core TradeProposal publisher | `meg/agent_core/decision_agent.py::evaluate()` | `TradeProposal` / `CHANNEL_TRADE_PROPOSALS` | Producer | High | **Defer**. Directly tied to risk gates, proposal publication, and operator-approval rail; too close to execution plane for the next safest boundary. |
| Dashboard read-only signal feed | `meg/dashboard/api/main.py::feed_signals()` (with `_normalize_signal_feed_data`) | Reads `CHANNEL_SIGNAL_EVENTS`; forwards SSE payload | Read-only consumer/forwarder | **Low** | **Recommend for Phase 0A-04F.** Single-function seam, read-only, non-execution, not Telegram/order-router/risk-sizing adjacent, no DB migration needed, and compatible with optional canonical IDs. |
| Dashboard approval parser | `meg/dashboard/api/main.py::approve_signal()` | Parses pending `TradeProposal` for approval flow | Consumer/parser | Very High | **Defer**. Explicitly order-router/approval adjacent and disallowed by this phase's safety constraints. |

## 5) Recommended next boundary for Phase 0A-04F

**Selected boundary:** `meg/dashboard/api/main.py::feed_signals()` (including its local data-forwarding path via `_normalize_signal_feed_data`).

- Event model/channel: `SignalEvent` from `RedisKeys.CHANNEL_SIGNAL_EVENTS`.
- Boundary type: non-execution read-only consumer/forwarder.

Why this is the safest next step:

1. Exactly one practical seam in one file/function path.
2. Read-only path that forwards signal stream to dashboard clients; no proposal creation, no approval mutation, no order placement.
3. No Telegram, order-router, or risk-sizing adjacency.
4. No DB/model migration required.
5. No strategy scoring changes required.
6. Works with current compatibility model where canonical IDs remain optional; forwarding can preserve legacy payload behavior.
7. Easy to validate with focused API/feed tests and existing shared-event models.

## 6) If no production-safe boundary is ready

A production-safe boundary **is** ready (dashboard signal feed read-only seam). Therefore no docs/test-only placeholder is required as the primary recommendation.

## 7) Future implementation ticket outline (Phase 0A-04F)

### Allowed files

- `meg/dashboard/api/main.py`
- `tests/dashboard/test_api.py`
- Optional shared-event helper touch-ups only if strictly necessary and still non-execution:
  - `meg/core/events.py`
  - corresponding focused tests in `tests/core/`

### Tests required

1. Feed continues to stream valid `SignalEvent` payloads over SSE from `CHANNEL_SIGNAL_EVENTS`.
2. Invalid JSON payloads in feed path are forwarded safely as raw (or handled per explicit contract) without crashing stream.
3. Canonical IDs remain optional: payloads missing `condition_id`/`token_id` still stream.
4. Canonical IDs, when present, remain preserved in streamed payload.
5. No behavior change in `approve_signal()` or order placement path.
6. No behavior change in decision-agent proposal publishing path.

### Acceptance criteria

- Only the selected read-only feed boundary is changed.
- Feed behavior remains backward-compatible for legacy signal payloads.
- Shared-event validation/normalization (if added) is fail-safe and does not crash the SSE loop.
- No execution-adjacent behavior changes.
- No workflow/dependency/DB model changes.

### Non-goals

- No migration of signal-engine consumer wiring.
- No strategy scoring or threshold changes.
- No decision-agent proposal behavior changes.
- No Telegram approval changes.
- No dashboard approval (`approve_signal`) changes.
- No order-router/execution changes.
- No parser/CLOB/Polygon changes.

### Rollback / kill criteria

Rollback or halt Phase 0A-04F if any of the following occurs:

1. Feed migration requires touching `approve_signal()` or order-router logic.
2. Feed migration requires strategy/decision-agent changes.
3. SSE feed loses backward compatibility for current valid legacy signal payloads.
4. Canonical IDs become mandatory at this boundary.
5. Any DB migration, workflow change, or dependency change is needed.

## 8) Documentation-only confirmation

This 0A-04E ticket is documentation-only and intentionally makes no runtime, test, workflow, or dependency changes.

## Recommended next ticket

**Phase 0A-04F: Dashboard SignalEvent Read-Only Feed Boundary Migration** — migrate only `meg/dashboard/api/main.py::feed_signals()` boundary behavior with focused dashboard feed tests, keeping execution and approval paths untouched.
