# PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01 — Static Ingestion Boundary Skeleton

Canonical ID: PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01

## 1. Status and scope

Status: implemented as a narrow static boundary skeleton.

This PRD records a static ingestion boundary skeleton implementation only. It validates already-human-reviewed source descriptor mappings against the Stage 2 ingestion boundary vocabulary. It does not create real ingestion, data acquisition, provider integration, scoring, runtime behavior, production behavior, or trading behavior.

## 2. Strategic framing

Weather Bot Stage 2 needs a fail-closed vocabulary checkpoint between approved static label artifacts and any later ingestion work. This ticket adds that checkpoint without widening the system into operational data access or decisioning.

## 3. Stage ladder position

This implementation follows the Stage 2 ingestion boundary planning closeout and the static historical-label loader closeout. It remains before any later operational ingestion gate.

## 4. Human approval basis

The preceding approval request asked for a later narrow static skeleton. The user separately approved proceeding with this static skeleton only. That approval is limited to static validation code and static tests.

## 5. Static ingestion skeleton implementation boundary

The implementation boundary is limited to caller-supplied descriptor validation. The module accepts mappings supplied by tests or later human-reviewed code and returns pass, caution, or blocked validation results.

## 6. Implemented source module

Implemented module: `meg/weather/stage2/ingestion_boundary.py`.

The module uses Python standard library features only and does not read files, write files, call services, open network connections, load credentials, load config, create schemas, or start jobs.

## 7. Implemented public API

The public API consists of:

- `StaticIngestionSourceDescriptor`
- `StaticIngestionValidationResult`
- `static_ingestion_source_descriptor_from_mapping(mapping)`
- `validate_static_ingestion_source_descriptor(descriptor)`
- `validate_static_ingestion_source_mapping(mapping)`

## 8. Closed source category vocabulary

Allowed future source categories are:

- `human_reviewed_fixture_source`
- `official_resolution_source`
- `venue_rule_source`
- `weather_station_source`
- `market_metadata_source`
- `manual_research_note`

Prohibited source categories are:

- `unattributed_social_post`
- `unverified_ai_summary`
- `live_market_feed`
- `broker_execution_feed`
- `private_credentials_source`
- `runtime_scrape`
- `unreviewed_bulk_dataset`
- `unknown_source`

## 9. Evidence and confidence vocabulary

Evidence statuses are:

- `source_backed`
- `reviewer_inferred`
- `missing`
- `conflicting`
- `not_applicable`

Label confidence values are:

- `confirmed`
- `unclear`
- `unknown`

Validation severities are:

- `pass`
- `caution`
- `blocked`

## 10. Fail-closed blocker taxonomy

The blocker taxonomy includes:

- `missing_source_identity`
- `missing_access_date`
- `missing_source_category`
- `missing_source_provenance`
- `missing_no_lookahead_note`
- `unsupported_source_category`
- `prohibited_source_category`
- `unknown_source_category`
- `missing_evidence_status`
- `unsupported_evidence_status`
- `missing_label_confidence`
- `unsupported_label_confidence`
- `fixture_ingestion_confusion`
- `loader_ingestion_confusion`
- `runtime_drift`
- `connector_drift`
- `scoring_drift`
- `trading_drift`
- `other_unclear`

## 11. Validation severity behavior

Validation blocks when required identity, provenance, access-date, no-lookahead, fixture-boundary, loader-boundary, evidence, confidence, or category fields are missing or unsupported. Invalid supplied ISO dates block. Prohibited categories block. Evidence status `missing` blocks. Evidence status `conflicting` cautions unless blockers exist. Label confidence `unclear` or `unknown` cautions unless blockers exist.

## 12. Fixture-to-ingestion separation

The descriptor requires a fixture boundary note. Missing fixture separation blocks with `fixture_ingestion_confusion`. This protects existing fixture artifacts from being treated as operational ingestion.

## 13. Static-loader-to-ingestion separation

The descriptor requires a loader boundary note. Missing loader separation blocks with `loader_ingestion_confusion`. The historical-label loader remains unchanged and is not expanded by this ticket.

## 14. No-lookahead safeguard behavior

The descriptor requires a no-lookahead note. Missing no-lookahead context blocks with `missing_no_lookahead_note`. Supplied access dates must parse as ISO dates so human review can anchor evidence timing.

## 15. Static validation tests

Static tests were added under `tests/core/test_prd_p1_wx_stage2_ingestion_implementation_01.py`. They compile the module, inspect exposed API, exercise pass/caution/blocked outcomes, confirm no fixture or generated artifacts were modified or created, and verify the explicit non-approval language in this PRD.

## 16. Explicit non-approval boundaries

This implementation is static ingestion boundary skeleton implementation only.

- No real ingestion was created.
- No provider/API connectors were created.
- No source fetching was created.
- No external API calls were created.
- No credentials/secrets/config loading was created.
- No forecast pulls were created.
- No scraping/polling/streaming/scheduling/queues/jobs were created.
- No scoring/probability scoring was created.
- No backtesting/paper simulation was created.
- No runtime observation was created.
- No trading/order placement/position sizing/autonomy was created.
- No production behavior was created.
- No C++/Rust runtime components were created.
- No loader expansion was created.
- No fixture JSON/README files were created or modified.
- No historical-label data/generated data was created.

## 17. What remains unbuilt

All operational capabilities remain unbuilt, including real ingestion, provider/API connectors, source fetching, external API calls, credential or config loading, forecast pulls, scraping, polling, streaming, scheduling, queues, jobs, scoring, backtesting, paper simulation, runtime observation, trading, order placement, position sizing, autonomy, production behavior, and C++/Rust runtime components.

## 18. Future gates

Future real ingestion requires separate explicit approval. Future provider/API connector implementation requires separate explicit approval. Future source fetching requires separate explicit approval. Future scoring/backtesting requires separate explicit approval. Future runtime/trading requires separate explicit approval.

## 19. Acceptance criteria

Acceptance requires the static module to compile, use standard library features only, expose the required dataclasses and functions, preserve closed vocabularies, fail closed on missing or unsupported required descriptor fields, caution on conflicting evidence and unclear or unknown confidence, block drift language that suggests operational work, and pass the static tests.

This implementation does not imply readiness for ingestion, providers, sources, scoring, runtime, production, or trading.

## 20. Later-ticket handoff

If this implementation remains clean, the recommended next ticket is a static ingestion skeleton implementation closeout/checkpoint. Do not use this ticket as approval for provider connectors, source fetching, scoring, backtesting, runtime behavior, production behavior, or trading.
