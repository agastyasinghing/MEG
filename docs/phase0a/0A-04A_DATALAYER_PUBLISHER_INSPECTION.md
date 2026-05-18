# Phase 0A-04A Data-layer Publisher Inspection

Status: documentation-only inspection for the next Phase 0A boundary candidate. This note does not change production code, tests, workflows, dependency files, parser behavior, or the frozen master PRD.

## Purpose

Phase 0A-03B migrated exactly one production consumer boundary: `meg/pre_filter/pipeline.py::run()` consuming `RawWhaleTrade` JSON from `RedisKeys.CHANNEL_RAW_WHALE_TRADES`. Phase 0A-03C recommended inspecting the upstream data-layer raw-whale publisher before selecting the next migration ticket.

This inspection determines whether the data-layer raw-whale publisher can be migrated next by adding outbound shared-event validation/wrapping only, without rewriting Polygon receipt decoding, CLOB parsing, canonical identifier extraction, or the already-migrated pre-filter consumer.

## Boundary inspected

| Item | Finding |
| --- | --- |
| Producer module | `meg/data_layer/polygon_feed.py` |
| Model creation function | `_filter_whale_transaction(tx, config) -> RawWhaleTrade | None` |
| Publish function | `_emit_event(redis, event)` |
| Redis channel | `RedisKeys.CHANNEL_RAW_WHALE_TRADES` |
| Downstream consumer | `meg/pre_filter/pipeline.py::run()`; already migrated in Phase 0A-03B and out of scope for the next ticket |

## Code-path observations

1. `PolygonFeed._process_block(...)` fetches block transactions and calls `_filter_whale_transaction(...)` for each transaction. If the return value is not `None`, the code optionally enriches `market_category` from Redis, calls `_emit_event(...)`, and then registers the active market using the existing legacy market identifier.
2. `_filter_whale_transaction(...)` is the exact function that creates `RawWhaleTrade`. It currently uses heuristic transaction parsing and explicitly documents that full CLOB `OrderFilled` receipt decoding remains a TODO.
3. `_emit_event(...)` is the exact function that serializes and publishes the event. It receives a `RawWhaleTrade` model instance and publishes `event.model_dump_json()` to `RedisKeys.CHANNEL_RAW_WHALE_TRADES`.
4. Because the publisher boundary already accepts a constructed `RawWhaleTrade`, a future migration can validate the model or its dumped payload immediately before `publish(...)` without changing Polygon transaction filtering or CLOB receipt semantics.

## Required inspection answers

| Question | Answer |
| --- | --- |
| 1. Where is `RawWhaleTrade` created? | In `meg/data_layer/polygon_feed.py::_filter_whale_transaction(...)`, at the return that constructs `RawWhaleTrade(...)`. |
| 2. Where is it serialized/published? | In `meg/data_layer/polygon_feed.py::_emit_event(...)`, which calls `publish(redis, RedisKeys.CHANNEL_RAW_WHALE_TRADES, event.model_dump_json())`. |
| 3. Does the publisher already construct a `RawWhaleTrade` model before publish? | Yes. `_filter_whale_transaction(...)` returns a `RawWhaleTrade`; `_process_block(...)` may copy it to add `market_category`; `_emit_event(...)` receives the model instance. |
| 4. Does it currently publish `model_dump_json()` or raw dict/json? | It publishes `event.model_dump_json()`, not an unvalidated raw dict or hand-built JSON string. |
| 5. Are `event_type` and `schema_version` present/defaulted before publish? | Yes. `RawWhaleTrade` inherits `schema_version: int = 1` and defines `event_type: Literal["raw_whale_trade"] = "raw_whale_trade"`, so model construction/default dumping includes both unless a future code path deliberately suppresses defaults. |
| 6. Are `condition_id`/`token_id` available at this boundary or still unavailable? | They are still generally unavailable. The current parser derives a legacy market identifier from the transaction hash prefix and has TODOs for receipt-log extraction of the true market/outcome/price. No canonical identifier extraction exists in this boundary today. |
| 7. Can canonical IDs remain optional? | Yes. `CanonicalIdentifiers` keeps `condition_id`, `token_id`, and `market_slug` optional during the compatibility window, and the 0A-03B consumer migration already depends on legacy raw-whale payload compatibility. |
| 8. Can legacy market identity remain preserved? | Yes. A publisher-boundary validation ticket should preserve the existing legacy field and values exactly, including active-market registration and category lookup behavior, while only validating/wrapping the outbound shared event. |
| 9. Can outbound validation be added without changing parser semantics? | Yes. The seam is `_emit_event(...)`: validate the already-built model or its dumped payload immediately before `publish(...)`. That does not require changing `_filter_whale_transaction(...)`, receipt decoding, CLOB parsing, or category enrichment. |
| 10. Can malformed/out-of-contract publisher payloads fail closed before publish? | Yes. A future ticket can make `_emit_event(...)` validate through the shared-event dispatch/channel helper before calling `publish(...)`, and skip/raise before Redis publication if validation fails. The exact fail-closed behavior should be tested and documented in that ticket. |
| 11. What tests would be needed for a future migration? | Add focused data-layer publisher tests proving valid `RawWhaleTrade` publishes unchanged, canonical identifier fields remain optional, optional canonical fields are preserved when present, wrong event type/schema version/malformed model or payload is rejected before `publish(...)`, Redis channel remains `CHANNEL_RAW_WHALE_TRADES`, and parser tests remain unchanged. Core shared-event tests may be extended only if a reusable outbound helper is added. |
| 12. What files should be allowed in that future migration? | Keep the future migration tiny: `meg/data_layer/polygon_feed.py` for `_emit_event(...)` only; `tests/data_layer/test_polygon_feed.py` for publisher-boundary tests; and, only if required for a reusable outbound helper, `meg/core/events.py` plus focused `tests/core/...` boundary tests. Do not touch `meg/pre_filter/pipeline.py`, Polygon/CLOB parser logic, workflows, dependencies, strategy code, execution code, or the frozen PRD. |

## Safety assessment

Recommendation: proceed with a tiny publisher-boundary migration in the next ticket.

Rationale:

- The data-layer publisher already constructs a `RawWhaleTrade` Pydantic model before publish.
- Serialization is already centralized in `_emit_event(...)` and uses `model_dump_json()`.
- The shared event defaults for `event_type` and `schema_version` exist at model level before publish.
- Canonical IDs can remain optional; the next ticket does not need to extract `condition_id` or `token_id`.
- Legacy market identity can remain preserved for current downstream compatibility.
- The outbound validation seam is narrow and does not require touching the pre-filter consumer again.

## Risks and constraints for the next ticket

- Do not rewrite `_filter_whale_transaction(...)`; its Polygon/CLOB parsing TODOs are intentionally out of scope.
- Do not add receipt-log decoding, canonical ID extraction, or order-book metadata lookup in the publisher-boundary migration.
- Do not change active-market registration or market-category enrichment semantics.
- Decide explicitly whether outbound validation failure should raise to `_process_block(...)`'s per-transaction error handler or be caught/logged inside `_emit_event(...)`; either way, no invalid payload should reach Redis.
- Avoid combining the producer migration with any downstream pre-filter, signal, decision, execution, or Telegram approval behavior.

## Future boundary candidate

Exact next boundary candidate: `meg/data_layer/polygon_feed.py::_emit_event(redis, event)` publishing `RawWhaleTrade` to `RedisKeys.CHANNEL_RAW_WHALE_TRADES`.

Suggested next-ticket title: `Phase 0A-04B: Validate data-layer RawWhaleTrade outbound publisher boundary`.

## Required future tests

A future migration should add or update tests that prove:

1. `_emit_event(...)` publishes a valid `RawWhaleTrade` to `RedisKeys.CHANNEL_RAW_WHALE_TRADES` with the same payload fields currently expected.
2. The published JSON includes/defaults `event_type="raw_whale_trade"` and `schema_version=1`.
3. Payloads without canonical IDs still publish successfully during the compatibility window.
4. Payloads with `condition_id`, `token_id`, and `market_slug` preserve those fields.
5. Wrong event type or unsupported schema version is rejected before `publish(...)` is called.
6. A malformed/out-of-contract event cannot be published to Redis.
7. Existing `_filter_whale_transaction(...)` tests continue to cover parser behavior without semantic changes.

## Repository inspection commands

Commands used for this inspection:

```bash
rg -n "RawWhaleTrade" meg/data_layer tests
rg -n "_emit_event|publish\(" meg/data_layer tests
rg -n "CHANNEL_RAW_WHALE_TRADES" meg/data_layer tests
rg -n "condition_id|token_id|market""_id|outcome" meg/data_layer tests
rg -n "model_dump_json|model_validate|RawWhaleTrade\(" meg/data_layer tests
```

Additional spot checks used while drafting this note:

```bash
sed -n '1,220p' docs/DATA_MODEL.md
sed -n '1,240p' docs/PHASE_0A_SHARED_RAIL.md
sed -n '1,240p' docs/phase0a/0A-03A_PRODUCTION_BOUNDARY_MIGRATION_PLAN.md
sed -n '1,260p' docs/phase0a/0A-03C_PREFILTER_BOUNDARY_POSTMIGRATION_AUDIT.md
nl -ba meg/data_layer/polygon_feed.py | sed -n '286,455p'
nl -ba meg/core/events.py | sed -n '83,125p;353,419p;425,445p'
nl -ba tests/data_layer/test_polygon_feed.py | sed -n '140,153p;330,388p;555,586p'
```

## Documentation-only confirmation

This ticket intentionally changes only `docs/phase0a/0A-04A_DATALAYER_PUBLISHER_INSPECTION.md`. It does not modify production source, tests, workflows, dependencies, parser behavior, strategy code, execution authority, or the frozen PRD.
