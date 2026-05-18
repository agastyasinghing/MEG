# Phase 0A-04C Next Boundary Inspection

Status: documentation-only planning inspection for Phase 0A-04D. This note selects exactly one safe future shared-event boundary to migrate after the completed raw-whale producer/consumer rail work. It does not change production code, tests, workflows, dependency files, runtime parsing, strategy behavior, approval flow, execution behavior, database models, CI, or the frozen master PRD.

## Purpose

Phase 0A has now validated both sides of the raw-whale shared-event rail:

1. **Phase 0A-03B pre-filter raw consumer** migrated `meg/pre_filter/pipeline.py::run()` so inbound `RawWhaleTrade` JSON on `RedisKeys.CHANNEL_RAW_WHALE_TRADES` is validated at the consumer boundary before gate processing.
2. **Phase 0A-04B data-layer raw publisher** migrated `meg/data_layer/polygon_feed.py::_emit_event()` so outbound `RawWhaleTrade` JSON on `RedisKeys.CHANNEL_RAW_WHALE_TRADES` is validated before publication.

The next step remains documentation-first. This inspection compares the remaining shared-event publisher/consumer seams and recommends exactly one future Phase 0A-04D migration boundary that is narrow, non-execution, compatible with legacy payloads, and testable with the existing shared event models.

## Repository inspection commands used

The following repository inspection commands were run from the repository root:

```bash
rg -n "CHANNEL_QUALIFIED_WHALE_TRADES|CHANNEL_SIGNAL_EVENTS|CHANNEL_TRADE_PROPOSALS" meg tests docs
rg -n "QualifiedWhaleTrade|SignalEvent|TradeProposal" meg tests
rg -n "publish\(|\.publish\(" meg tests
rg -n "subscribe\(|listen\(|get_message\(" meg tests
rg -n "model_validate_json|model_validate\(" meg tests
rg -n "approve_signal|feed_signals|decision_agent|signal_aggregator|composite_scorer" meg tests
```

Additional focused reads were performed on the requested files to confirm the exact functions and call paths for each candidate seam.

## Candidate boundary table

| Boundary name | File/function | Event model/channel | Producer or consumer | Risk level | Recommendation/defer reason |
| --- | --- | --- | --- | --- | --- |
| Pre-filter qualified-whale publisher | `meg/pre_filter/pipeline.py::_process_event()` | `QualifiedWhaleTrade` / `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES` | Producer | Low-medium | **Recommended for Phase 0A-04D.** It is one publish seam after the raw consumer has already validated input. The function already receives/builds a shared event model and publishes its JSON. A future ticket can add outbound boundary validation immediately before publish while preserving legacy compatibility and optional canonical identifiers. |
| Signal-engine qualified-whale consumer | No production Redis subscribe/listen loop found in `meg/signal_engine`; scoring entry point is `meg/signal_engine/composite_scorer.py::score()` | `QualifiedWhaleTrade` / expected `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES` | Consumer candidate, but clear runtime adapter not found | High | Defer. The inspection did not find a single production consumer adapter to migrate. Migrating this would first require rail wiring or worker-entry clarification, which is outside a small validation-only boundary ticket. |
| SignalEvent publisher | `meg/signal_engine/composite_scorer.py::score()` constructs and returns `SignalEvent`; no Redis publish call found in `meg/signal_engine` | `SignalEvent` / expected `RedisKeys.CHANNEL_SIGNAL_EVENTS` | Producer candidate, but publish seam not found | High | Defer. The scoring function constructs a shared event model but is strategy/scoring adjacent and does not expose a production Redis publish boundary in the inspected code. A migration here could blur validation with scoring or worker-wiring changes. |
| Agent-core signal consumer | `meg/agent_core/signal_aggregator.py::run()` and `_validate_and_route()` | `SignalEvent` / `RedisKeys.CHANNEL_SIGNAL_EVENTS` | Consumer | Medium-high | Defer. It is a real consumer boundary and already parses `SignalEvent`, but valid events route into `decision_agent.evaluate()`, which can create proposals. That is too close to proposal/risk/approval flow for the next safe post-raw migration. |
| Agent-core proposal publisher | `meg/agent_core/decision_agent.py::evaluate()` | `TradeProposal` / `RedisKeys.CHANNEL_TRADE_PROPOSALS` | Producer | High | Defer. This seam is downstream of signal gating, risk/crowding checks, proposal construction, status updates, and operator approval queue publication. It should not be the next validation-only migration because any behavior change could affect proposal availability. |
| Dashboard read-only signal feed | `meg/dashboard/api/main.py::feed_signals()` | `SignalEvent` / `RedisKeys.CHANNEL_SIGNAL_EVENTS` | Read-only consumer/forwarder | Low-medium | Defer despite being read-only. The feed forwards Redis messages to SSE clients and has client compatibility concerns; adding stricter validation could hide dashboard data without a dedicated UI/feed compatibility test plan. It is safer after upstream signal-event boundaries are clearer. |
| Dashboard approval parser | `meg/dashboard/api/main.py::approve_signal()` | `TradeProposal` pending proposal payload, not a pub/sub channel consumer | Consumer/parser | Very high | Defer. This is approval and order-router adjacent. It consumes pending proposal state and then calls order placement logic. It is explicitly outside the next safe shared-event boundary migration. |

## Recommended next boundary for Phase 0A-04D

**Recommended boundary:** `meg/pre_filter/pipeline.py::_process_event()` at the outbound publish call to `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES`.

**Event model/channel:** `QualifiedWhaleTrade` on `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES`.

**Why this is the safest next step:**

- It is exactly one function/seam: the existing publish point at the end of `_process_event()`.
- It is non-execution and not Telegram, order-router, risk-sizing, or dashboard approval adjacent.
- It is upstream of signal scoring and proposal creation, so a validation-only migration can stay limited to shared-event rail infrastructure.
- The seam already publishes a Pydantic shared event object as JSON, which makes outbound validation straightforward and testable.
- It can preserve legacy compatibility because canonical identifiers can remain optional and no parser, database, strategy, execution, or CI change is required.
- It complements the completed raw-whale rail work without migrating both a new producer and its consumer in the same ticket.

## Future implementation ticket outline: Phase 0A-04D

### Allowed files

Keep the future implementation small. Suggested allowed files are:

- `meg/pre_filter/pipeline.py` for the single outbound publish seam only.
- `tests/pre_filter/test_pipeline.py` for focused boundary coverage.
- `meg/core/events.py` and `tests/core/test_event_json_boundary_validation.py` or `tests/core/test_event_redis_envelope_boundary.py` only if a reusable channel-specific helper is needed rather than local validation.

No other production source, dashboard code, signal-engine code, agent-core code, execution code, database migrations, dependency files, workflow files, or frozen PRD/docs should be modified.

### Tests required

A future migration should add or extend focused tests proving:

1. A valid `QualifiedWhaleTrade` generated by `_process_event()` is published unchanged to `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES`.
2. Legacy-compatible qualified-whale payloads without canonical identifiers still publish.
3. Optional `condition_id`, `token_id`, `outcome`, and display metadata are preserved when present on the input/shared event path.
4. A wrong event type, unsupported schema version, malformed payload, or channel/event mismatch is rejected before Redis publish.
5. Existing gate behavior remains unchanged: market-quality rejection, arbitrage rejection, non-signal intent filtering, wallet-data miss handling, and gate exception fail-closed behavior continue to avoid publishing.
6. The migration does not call signal scoring, decision-agent proposal creation, Telegram approval, dashboard approval, order routing, database migrations, or parser changes.
7. Existing raw-whale consumer and data-layer raw publisher tests remain green.

### Acceptance criteria

- Exactly one runtime boundary is migrated: outbound `QualifiedWhaleTrade` publication from `_process_event()`.
- The Redis channel remains `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES`.
- Valid legacy payload behavior is preserved.
- Canonical identifiers remain optional during the compatibility window.
- Invalid shared-event/channel envelopes fail closed before publication.
- No signal scoring, proposal behavior, approval flow, execution behavior, parser behavior, database schema, workflow, dependency, or strategy code changes are included.
- The final diff is limited to the explicitly allowed implementation and test files for that future ticket.

### Non-goals

- Do not migrate the signal-engine qualified-whale consumer in the same ticket.
- Do not add or wire a missing signal-engine worker.
- Do not change composite scoring, signal thresholding, decay, Kelly sizing, or strategy logic.
- Do not change `decision_agent.evaluate()` behavior or proposal publication.
- Do not change Telegram approval, dashboard approval, or order-router behavior.
- Do not change DB models or migrations.
- Do not change Polygon/CLOB parsing.
- Do not add weather strategy, whale strategy, or live-trading strategy implementation.

### Rollback/kill criteria

Stop or roll back the future migration if:

- The change requires modifying strategy scoring, decision-agent proposal behavior, dashboard approval, Telegram approval, order routing, parser behavior, DB schema, dependencies, workflows, or CI.
- The change cannot preserve legacy-compatible qualified-whale publication.
- The change requires canonical identifiers to be mandatory before upstream extraction is complete.
- The test plan cannot prove invalid envelopes are rejected before Redis publish.
- The diff expands beyond the single intended outbound publish seam plus focused tests.

## Documentation-only confirmation

This Phase 0A-04C ticket is documentation-only. It adds only this inspection document and intentionally leaves production code, tests, workflows, dependency files, frozen PRD/docs, parser behavior, strategy behavior, database models, dashboard approval, Telegram approval, and execution/order placement unchanged.

## Recommended next ticket

Open **Phase 0A-04D: Pre-filter QualifiedWhaleTrade Publisher Boundary Migration**. The ticket should migrate only `meg/pre_filter/pipeline.py::_process_event()` at the `RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES` outbound publish seam, with focused tests in `tests/pre_filter/test_pipeline.py` and optional shared-event helper tests only if a reusable helper is introduced.
