# PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-01 — Offline Real Ingestion Implementation Skeleton

## Status and scope

Canonical ID: PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-01

This PRD records a narrow Weather Bot Stage 2 offline implementation skeleton only. It permits deterministic validation of caller-supplied, already-reviewed real-ingestion source descriptor mappings. It does not create production ingestion behavior.

## Approval and predecessor context

This implementation skeleton follows the approved Weather Bot Stage 2 real-ingestion planning and closeout sequence:

- PRD-P1-WX-STAGE2-REAL-INGESTION-PLANNING-APPROVAL-01
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-01
- PRD-P1-WX-STAGE2-REAL-INGESTION-PLAN-CLOSEOUT-01
- MEG-OPS-WX-ACTIVE-STATE-07
- PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-APPROVAL-01
- PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01

The human decision after PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-APPROVAL-01 allowed a later narrow offline real-ingestion implementation skeleton. This PRD stays inside that skeleton boundary.

## Offline implementation skeleton boundary

The implementation is limited to standard-library dataclasses, closed-set constants, mapping conversion, and deterministic validation results. Callers must supply every source descriptor value. The skeleton may reject unsupported or unsafe values; it must not acquire source data.

The implementation-only boundary is:

- offline implementation skeleton only;
- caller-supplied source descriptor validation only;
- already-reviewed source descriptor values only;
- no provider/API connectors are implemented;
- no source fetching is implemented;
- no external API calls are implemented;
- no secrets/config loading is implemented;
- no forecast pulls are implemented;
- no scraping/polling/streaming/scheduling/jobs are implemented;
- no scoring/back-testing/runtime/trading/order-placement/autonomy is implemented;
- no production service behavior is implemented.

## Source module contract

The source module is `meg/weather/stage2/real_ingestion.py`. It defines closed sets for source categories, source-intake modes, prohibited modes, blocker codes, evidence statuses, validation severities, and validation states. It also defines:

- `RealIngestionSourceDescriptor`
- `RealIngestionValidationResult`
- `real_ingestion_source_descriptor_from_mapping`
- `validate_real_ingestion_source_descriptor`
- `validate_real_ingestion_source_mapping`

The validator requires source identity, source name, source category, source-intake mode, provenance URL or provenance note, access date, retrieval context, no-lookahead statement, human-reviewed flag, and static caller-supplied flag. It fails closed on prohibited modes, unsupported categories, unsupported modes, missing metadata, and wording that implies connector, source-retrieval, probability, runtime, or execution drift.

## Non-approval boundaries

This PRD and implementation do not approve provider/API connectors, source fetching, external API calls, secrets/config loading, forecast pulls, scraping, polling, streaming, scheduling, jobs, scoring, back-testing, runtime behavior, trading, order-placement, autonomy, production behavior, generated data, fixture changes, or historical-label data creation.

Future provider connector implementation requires later approval. Future source fetching requires later approval. Future scoring/back-testing/runtime/trading requires later approval. Future production use also requires later approval.

## Fixture, loader, and data separation

This implementation does not read fixture README files, fixture JSON files, generated data, or historical-label data. It does not modify fixture README files, fixture JSON files, generated data, or historical-label data. It does not expand the static historical-label loader and does not replace the existing static ingestion boundary skeleton.

## Machine-checkable implementation posture

- implementation stage: offline_real_ingestion_implementation_skeleton
- implementation status: implemented_as_static_skeleton
- data acquisition posture: no_source_fetching
- data acquisition posture: caller_supplied_values_only
- connector posture: no_provider_api_connectors
- connector posture: later_approval_required
- external call posture: no_external_api_calls
- credential posture: no_secrets_config_loading
- forecast posture: no_forecast_pulls
- job posture: no_scraping_polling_streaming_scheduling_jobs
- analytics posture: no_scoring_back_testing_runtime_trading_order_placement_autonomy
- source posture: no_fixture_readme_or_json_modification
- source posture: no_historical_label_or_generated_data_creation

## Acceptance criteria

- The PRD exists with canonical ID PRD-P1-WX-STAGE2-REAL-INGESTION-IMPLEMENTATION-01.
- The source module remains standard-library only.
- Unit tests cover valid descriptors, missing metadata, unsupported values, prohibited modes, drift wording, mapping conversion, and absence of runtime/data-acquisition behavior.
- Static tests cover this PRD boundary, predecessor references, non-approval statements, and forbidden positive approval drift.

## Later-ticket handoff

If clean, the recommended next ticket is an offline real ingestion implementation closeout/checkpoint. Do not recommend provider connectors, source fetching, scoring, back-testing, runtime, trading, order-placement, autonomy, or production behavior from this skeleton ticket.
