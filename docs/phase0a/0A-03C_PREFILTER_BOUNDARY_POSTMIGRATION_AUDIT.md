# Phase 0A-03C Pre-filter Boundary Post-Migration Audit

Status: documentation-only post-migration audit for Phase 0A-03B. This note does not change runtime code, tests, workflows, dependency files, or the frozen master PRD.

## Purpose

Phase 0A-03B migrated the first real production boundary onto the shared-event validation contract. This audit records the selected boundary, the helper now used at that boundary, the preserved behavior, the test coverage that protects the migration, and the constraints to apply before selecting the next production-boundary migration.

## Migration summary

| Item | Phase 0A-03B result |
| --- | --- |
| Selected boundary | `meg/pre_filter/pipeline.py::run()` consuming `RawWhaleTrade` JSON from `RedisKeys.CHANNEL_RAW_WHALE_TRADES`. |
| Helper used | `validate_raw_whale_trade_channel_payload(...)`, which delegates to the shared JSON/event dispatch validation path before returning a `RawWhaleTrade`. |
| Behavior before | The pre-filter consumer parsed raw channel JSON directly as a `RawWhaleTrade`, so basic model validation happened but channel-specific event dispatch, supported-version checks, and wrong-event rejection were not centralized at the consumer boundary. |
| Behavior after | The pre-filter consumer validates the incoming JSON through the shared boundary helper before calling business logic. Valid legacy raw-whale payloads still reach `_process_event(...)`; malformed JSON, non-object JSON, unsupported schema versions, missing event types, and supported but wrong event types are rejected before gate processing. |

## Safety confirmations

- `_process_event(...)` was intentionally left unchanged. The gate sequence, gate fail-closed handling, session usage, and qualified-trade publication behavior remain outside the Phase 0A-03B boundary migration.
- Publishers were intentionally left unchanged. The data-layer raw-whale publisher and the pre-filter qualified-whale publisher were not migrated or rewritten in the same ticket.
- Canonical identifiers remain optional during the compatibility window. Payloads may carry `condition_id`, `token_id`, and `market_slug`, but legacy raw-whale payloads without those fields still validate and continue into `_process_event(...)`.
- The legacy market identifier is preserved for existing raw-whale compatibility. The migration did not remove, rename, or reroute existing legacy identifier fields.
- Malformed payloads, non-object JSON payloads, unsupported schema versions, missing event types, and supported but wrong event types are rejected before business logic runs.
- Redis disconnect propagation is unchanged. Subscription-level disconnects still bubble to the caller's reconnect supervision rather than being converted into malformed-event skips.

## Test coverage protecting the boundary

- `tests/pre_filter/test_pipeline.py`
  - Confirms the `run(...)` loop consumes `RedisKeys.CHANNEL_RAW_WHALE_TRADES`, validates valid raw-whale JSON, preserves legacy payload compatibility, defaults a missing schema version to the supported version, carries optional canonical identifiers through to `_process_event(...)`, rejects malformed or wrong-boundary payloads before processing, and preserves Redis disconnect propagation.
- `tests/core/test_event_json_boundary_validation.py`
  - Confirms shared JSON validation dispatches by `event_type` and supported schema version, rejects missing/unknown event types, rejects unsupported versions and malformed JSON, keeps canonical identifiers optional, and validates the production raw-whale channel helper.
- `tests/core/test_event_redis_envelope_boundary.py`
  - Confirms Redis channel-envelope expectations route shared-event payloads through the correct channel/event pairing and reject mismatches before a consumer treats a payload as its expected event type.
- `tests/core/test_static_canonical_ids.py`
  - Confirms new or increased legacy identifier usage cannot appear silently and documents the target Phase 0A end state where shared-rail modules route by canonical identifiers.

## Known non-goals still deferred

- No Polygon/CLOB parser rewrite was included.
- No `signal_engine` or `agent_core` migration was included.
- No dashboard approval migration was included.
- No live execution, order placement, sizing, or approval-authority behavior was changed.
- No weather strategy or whale strategy implementation was added.

## Next-boundary selection guidance

Before opening the next production-boundary migration ticket:

1. Choose exactly one boundary.
2. Avoid execution-adjacent flows, including proposal approval, execution requests, order routing, live placement, and risk-controller paths that could affect operator authority.
3. Prefer a read-only consumer boundary or an upstream parse/validation boundary where the acceptance tests can prove malformed data is stopped before business logic.
4. Do not migrate a producer and its consumer in the same ticket; preserve rollback clarity and isolate compatibility risk.
5. Preserve existing payload compatibility unless the ticket explicitly declares and tests a breaking migration.
6. Keep the change limited to Phase 0A shared-rail infrastructure and continue to defer strategy implementation.

## Recommended next ticket

A good next ticket would migrate one non-execution, upstream validation boundary only. The preferred candidate is the data-layer raw-whale publisher boundary after a focused inspection confirms that the ticket can wrap or validate the outbound `RawWhaleTrade` payload without rewriting Polygon/CLOB parsing and without changing the pre-filter consumer again.

If that inspection shows the parser and publisher are too coupled, choose a read-only consumer or envelope-validation boundary instead, but still keep the ticket to exactly one production boundary and do not combine producer and consumer migration.
