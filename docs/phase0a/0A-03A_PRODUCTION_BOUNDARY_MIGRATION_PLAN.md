# Phase 0A-03A Production Boundary Migration Plan

Status: planning only. This ticket does not change runtime code, tests, CI workflows, dependency files, or the frozen master PRD.

## Purpose

Phase 0A has test-only shared-event boundaries for dict payloads, JSON payloads, Redis channel envelopes, schema-version defaults, event-type dispatch validation, and canonical identifier compatibility. The next ticket should migrate one real production boundary to the same validation contract while preserving current legacy payload compatibility.

This document inventories the current shared-event producers and consumers, recommends exactly one low-risk first boundary for a later implementation ticket, and defines acceptance, rollback, and test requirements for that later work.

## Inspection summary

The production event rail currently contains these shared-event paths:

- `meg.data_layer.polygon_feed._emit_event()` publishes `RawWhaleTrade` JSON to `RedisKeys.CHANNEL_RAW_WHALE_TRADES`.
- `meg.pre_filter.pipeline.run()` consumes `RedisKeys.CHANNEL_RAW_WHALE_TRADES` and validates incoming JSON as `RawWhaleTrade`.
- `meg.pre_filter.pipeline._process_event()` publishes `QualifiedWhaleTrade` JSON to `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES` after the pre-filter gates pass.
- `meg.signal_engine.composite_scorer.score()` constructs `SignalEvent`, but this inspection did not find a production Redis publish call to `RedisKeys.CHANNEL_SIGNAL_EVENTS` in `meg/signal_engine`.
- `meg.agent_core.signal_aggregator.run()` subscribes to `RedisKeys.CHANNEL_SIGNAL_EVENTS` and routes parsed `SignalEvent` objects to `decision_agent.evaluate()`.
- `meg.agent_core.decision_agent.evaluate()` publishes `TradeProposal` JSON to `RedisKeys.CHANNEL_TRADE_PROPOSALS` after sizing and status updates.
- `meg.dashboard.api.main.approve_signal()` reads pending proposal JSON from Redis and validates it as a `TradeProposal` before order-router placement.
- `meg.dashboard.api.main.feed_signals()` is a read-only SSE forwarder for `RedisKeys.CHANNEL_SIGNAL_EVENTS`.


## Repository inspection commands

These read-only searches were used to inventory candidate shared-event production boundaries and confirm the current producer/consumer footprint:

```bash
rg -n "\.publish\(|publish\(" meg tests --glob '!**/__pycache__/**'
rg -n "subscribe\(|psubscribe\(|listen\(|get_message\(" meg tests --glob '!**/__pycache__/**'
rg -n "CHANNEL_RAW_WHALE_TRADES|CHANNEL_QUALIFIED_WHALE_TRADES|CHANNEL_SIGNAL_EVENTS|CHANNEL_TRADE_PROPOSALS" meg tests docs --glob '!**/__pycache__/**'
rg -n "RawWhaleTrade|QualifiedWhaleTrade|SignalEvent|TradeProposal" meg tests --glob '!**/__pycache__/**'
rg -n "model_validate_json|model_validate\(" meg tests --glob '!**/__pycache__/**'
rg -n "RedisKeys\.CHANNEL_" meg tests --glob '!**/__pycache__/**'
```

## Candidate production boundaries

| Boundary name | Files/functions | Event model/channel | Producer or consumer | Risk level | Why not first / why candidate |
| --- | --- | --- | --- | --- | --- |
| Data-layer raw whale trade publisher | `meg/data_layer/polygon_feed.py::_emit_event()` | `RawWhaleTrade` / `RedisKeys.CHANNEL_RAW_WHALE_TRADES` | Producer | Medium | Candidate because it is a single named publisher. Not first because the upstream parser still contains low-level Polygon/CLOB TODOs, including provisional legacy identifiers and outcome extraction, so changing this first could blur boundary validation with parser remediation. |
| Pre-filter raw whale trade consumer | `meg/pre_filter/pipeline.py::run()` | `RawWhaleTrade` / `RedisKeys.CHANNEL_RAW_WHALE_TRADES` | Consumer | Low | Recommended first. It is one named production consumer, already JSON-based, non-execution, easy to test with fixture payloads, and can preserve legacy payload compatibility while adding dispatch/channel-envelope validation. |
| Pre-filter qualified whale trade publisher | `meg/pre_filter/pipeline.py::_process_event()` | `QualifiedWhaleTrade` / `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES` | Producer | Medium | Candidate because it is a direct shared-event publisher. Not first because it sits after market-quality, arbitrage, intent, and wallet-data gates; test setup must mock more moving parts before isolating boundary behavior. |
| Signal-engine qualified trade consumer | No production subscribe/listen loop found in `meg/signal_engine`; scoring entry point is `meg/signal_engine/composite_scorer.py::score()` | `QualifiedWhaleTrade` / expected `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES` | Consumer, but missing or not wired in inspected runtime code | High | Not first because there is no clear single Redis consumer boundary to migrate. A later Phase 0C or rail-wiring ticket should first define the worker entry point. |
| Signal publisher | `meg/signal_engine/composite_scorer.py::score()` constructs `SignalEvent`; no Redis publish call found in `meg/signal_engine` | `SignalEvent` / expected `RedisKeys.CHANNEL_SIGNAL_EVENTS` | Producer, but publish boundary not found | High | Not first because the inspected code builds the event object but does not expose a clear production publish adapter. A future ticket should identify or add that adapter before migration. |
| Agent-core signal consumer | `meg/agent_core/signal_aggregator.py::run()` and `_validate_and_route()` | `SignalEvent` / `RedisKeys.CHANNEL_SIGNAL_EVENTS` | Consumer | Medium-high | Candidate because `_validate_and_route()` already parses JSON. Not first because valid events call `decision_agent.evaluate()`, which can create trade proposals and enter approval/execution-adjacent flows. Boundary validation here must be extra conservative. |
| Agent-core proposal publisher | `meg/agent_core/decision_agent.py::evaluate()` | `TradeProposal` / `RedisKeys.CHANNEL_TRADE_PROPOSALS` | Producer | High | Not first because this is downstream of sizing, status updates, proposal creation, and operator approval flow. It is not order placement, but it is too close to execution for the first production-boundary migration. |
| Dashboard pending proposal parser | `meg/dashboard/api/main.py::approve_signal()` | `TradeProposal` / Redis pending proposal key | Consumer | High | Not first because it immediately calls `order_router.place()` after parsing. Even though approval remains operator initiated, this path is execution-adjacent and should not be the first migration. |
| Dashboard signal SSE feed | `meg/dashboard/api/main.py::feed_signals()` | `SignalEvent` / `RedisKeys.CHANNEL_SIGNAL_EVENTS` | Read-only consumer/forwarder | Low-medium | Candidate because it is read-only and non-execution. Not first because it currently forwards raw Redis messages to clients; adding strict validation could unexpectedly hide data from the UI unless client compatibility tests are in place. |
| Replay/test harness boundaries | `tests/core/event_fixture_boundary.py` and Redis/JSON boundary tests | Shared event fixture, JSON, and channel-envelope helpers | Test-only | Low | Not first because Phase 0A has already covered test-only boundaries. The next step should be production runtime code, not another test harness migration. |

## Recommended first production boundary

### Selected boundary

- File/function: `meg/pre_filter/pipeline.py::run()`.
- Event model: `RawWhaleTrade`.
- Channel: `RedisKeys.CHANNEL_RAW_WHALE_TRADES`.
- Direction: production consumer.

### Why this is the safest first migration

This boundary is the safest first production migration because it is:

1. One named function with one Redis input channel.
2. Non-execution and not part of Telegram approval, order placement, risk sizing, or autonomous routing.
3. Already dedicated to JSON decoding and event model validation before business logic runs.
4. Upstream of the pre-filter gates, so invalid payloads can be rejected before market-quality, arbitrage, and intent-classifier logic sees them.
5. Compatible with existing fixture-driven tests because the input can be represented as JSON strings and validated with the shared `RawWhaleTrade` model.
6. Able to preserve the current legacy identifier payload shape while allowing optional canonical `condition_id`, `token_id`, and `outcome` compatibility.
7. Independent of low-level CLOB/Polygon parsing fixes because the migration can focus only on the Redis/JSON boundary.

### Expected behavior before migration

`pipeline.run()` currently receives decoded Redis messages from `subscribe()`, calls `json.loads(raw)`, validates the resulting dict with `RawWhaleTrade.model_validate(data)`, logs and skips malformed events, and passes valid events to `_process_event()`.

### Expected behavior after migration

The future migration should replace ad hoc parse-and-validate logic in `pipeline.run()` with the shared production-boundary validator chosen by that ticket. The behavior should remain equivalent for valid legacy payloads, with these additional guarantees:

- Missing `schema_version` defaults to `1`.
- Unsupported `schema_version` is rejected and skipped without crashing the loop.
- Wrong `event_type` is rejected and skipped without invoking `_process_event()`.
- If the future validator uses a Redis channel envelope, channel/event-type mismatches are rejected before business logic.
- Optional canonical identifiers remain optional during the compatibility window.
- Existing valid legacy payloads continue to flow through the pre-filter gates unchanged.
- No execution, proposal, approval, or order-placement behavior changes.

## Required tests before implementation

The future implementation ticket must add focused tests before or alongside the migration. Required coverage:

1. Valid current `RawWhaleTrade` JSON still calls `_process_event()` exactly once.
2. Legacy payloads without canonical identifiers still validate and continue through the boundary.
3. Payloads missing `schema_version` default to `1` and continue through the boundary.
4. Payloads with unsupported `schema_version` are rejected, logged, and do not call `_process_event()`.
5. Payloads with the wrong `event_type` are rejected, logged, and do not call `_process_event()`.
6. If channel envelopes are introduced at this production boundary, a channel/event-type mismatch is rejected before `_process_event()`.
7. Canonical `condition_id` and `token_id` remain optional, while `outcome` remains governed by the existing shared event model.
8. Valid payloads carrying canonical identifiers preserve those values when `_process_event()` receives the event.
9. Redis disconnect behavior remains unchanged: connection errors from `subscribe()` still propagate to the caller/reconnect supervisor.
10. Malformed JSON still logs and skips without crashing the run loop.
11. No tests assert, require, or introduce live routing, Telegram approval, risk sizing, order placement, or autonomous execution behavior.

## Acceptance criteria for the future migration ticket

The future implementation ticket is acceptable only when all of the following are true:

- Only the selected pre-filter consumer boundary is migrated.
- `pipeline.run()` uses the shared event-boundary validation path for `RawWhaleTrade` messages from `RedisKeys.CHANNEL_RAW_WHALE_TRADES`.
- Valid current payloads and legacy-compatible payloads still reach `_process_event()` unchanged except for documented schema defaulting.
- Invalid schema versions, wrong event types, malformed JSON, and channel/event mismatches are rejected before business logic.
- The compatibility window remains intact: canonical identifiers are accepted when present but not globally required.
- The legacy market identifier field is not removed.
- No production source outside the selected boundary and any shared validation helper is changed.
- No Telegram approval, order-router, risk-controller, dashboard approve, CLOB parser, Polygon parser, or strategy code is changed.
- Tests prove both acceptance and rejection paths.
- Existing Phase 0A core tests still pass in the full-dev dependency boundary.

## Rollback criteria / kill criteria

Stop or roll back the future migration if any of these occur:

- Any valid legacy raw whale trade payload is rejected unexpectedly.
- `_process_event()` receives mutated business fields other than documented schema-version defaulting.
- Redis disconnect propagation changes or the run loop silently swallows connection failures.
- Pre-filter gates are invoked for payloads with unsupported schema versions, wrong event types, malformed JSON, or channel/event mismatches.
- Canonical identifiers become mandatory before the compatibility window is explicitly closed.
- Any execution-adjacent path changes, including Telegram approval, proposal publishing, risk sizing, order routing, or dashboard approval.
- The migration requires CLOB/Polygon parser rewrites, weather strategy code, whale strategy changes, live execution, or CI broadening.

## Non-goals

- No live execution.
- No strategy changes.
- No autonomous order placement.
- No Telegram approval changes.
- No risk sizing changes.
- No CLOB or Polygon parser rewrite in this migration.
- No removal of the legacy market identifier field.
- No global requirement for `condition_id` or `token_id`.
- No weather strategy implementation.
- No whale strategy implementation.
- No CI broadening, workflow changes, dependency changes, or test harness rewrites in this planning ticket.

## Future implementation ticket outline

Suggested ticket name: Phase 0A-03B migrate pre-filter raw whale trade consumer boundary.

Suggested branch name: `phase0a-03b-prefilter-raw-boundary-validation`.

Allowed files for that future ticket:

- `meg/pre_filter/pipeline.py`.
- A shared validation helper in `meg/core/events.py` or a narrowly scoped new helper under `meg/core/`, if the implementation needs one.
- Focused tests under `tests/pre_filter/` and/or `tests/core/` for this boundary only.
- Documentation updates only if behavior differs from this plan.

Future implementation acceptance criteria:

- `pipeline.run()` validates raw whale trade Redis input through the shared event-boundary contract.
- Valid legacy JSON, valid canonical JSON, and missing-`schema_version` JSON continue to route to `_process_event()`.
- Unsupported schema versions, wrong event types, malformed JSON, and channel/event mismatches are rejected and skipped.
- Redis disconnect propagation remains unchanged.
- No production behavior changes beyond input-boundary validation.
- No order placement, Telegram approval, risk sizing, dashboard approval, CLOB parser, Polygon parser, or strategy code changes.

Suggested future test commands:

```bash
python -m pytest -q tests/core/test_event_json_boundary_validation.py
python -m pytest -q tests/core/test_event_redis_envelope_boundary.py
python -m pytest -q tests/pre_filter/test_pipeline.py
python -m pytest -q tests/core
```

## Recommended next ticket

Implement Phase 0A-03B: migrate `meg/pre_filter/pipeline.py::run()` to the shared production-boundary validation path for `RawWhaleTrade` messages on `RedisKeys.CHANNEL_RAW_WHALE_TRADES`, with the tests and acceptance criteria listed above.
