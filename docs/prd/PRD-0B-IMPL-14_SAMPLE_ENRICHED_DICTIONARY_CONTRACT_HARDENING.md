# PRD-0B-IMPL-14 Sample-Enriched Dictionary Contract Hardening

## Purpose and posture
This ticket hardens the IMPL-13 sample-enriched dictionary contract with explicit field, summary, and no-output validations.

## Relationship to PRD-0B-IMPL-13
IMPL-14 is contract hardening on top of IMPL-13 bounded sample enrichment behavior; it does not expand archive-read scope.

## Frozen approved sample field set
Only the following keys are approved in each sample-enrichment result:
- family
- source_platform
- source_kind
- source_relative_path
- sample_enrichment_status
- sample_source_relative_path
- sample_file_kind
- sample_row_limit
- sample_row_count_observed
- sample_column_count_observed
- sample_columns_observed
- sample_elapsed_ms
- sample_warning
- sample_generated_from_archive_root
- sample_persistent_output_written

## Runtime-vs-committed flag semantics
- Runtime summaries produced from explicit archive-root enrichment may set `sample_generated_from_archive_root=true`.
- Persistent committed/generated outputs are not approved.
- `sample_persistent_output_written` must always be `false`.
- Summary `wrote_outputs` must remain `false`.
- Summary `generated_artifacts` must remain empty.
- Summary `committed_fixtures` must remain `false`.
- `production_readiness_claim` must remain `false`.
- `final_trading_readiness_claim` must remain `false`.

## Forbidden payload classes
The contract forbids raw or derived payload/label classes, including:
- raw row values
- full archive-derived payloads
- fixture payloads
- generated committed dictionaries
- production model features
- strategy labels
- trade/opportunity labels
- user/event/trader personal data dumps

## No-output/no-artifact contract
No generated dictionary files, SQL outputs, reports, committed fixtures, or persistent `.duckdb` files are approved.

## Validation helper contract
Validation helpers are pure checks over in-memory dictionaries. They do not read archives, import DuckDB, call network APIs, read/write files, or mutate input payloads.

## Test posture using synthetic mini-archives
Tests use synthetic mini-archives and local temporary paths to validate success and fail-closed semantics.

## Safety/no-output guarantees
The hardened contract enforces no-output defaults and reject-on-drift behavior for forbidden payload keys and output flags.

## What counts as success
- Approved sample keys are frozen and validated.
- Runtime summary flags remain no-output/no-artifact.
- Forbidden payload/label classes are rejected.
- IMPL-13 runtime behavior remains bounded and fail-closed.

## What remains out of scope
Production loaders, query-engine service, connectors/API calls, order placement, live trading, autonomous execution, weather implementation, production readiness claims, and production latency SLO claims.

## Relationship to PRD-0A
This hardening supports Phase 0A/0B shared-rail readiness by preserving operator-safe and no-autonomy posture.

## Recommended next tickets
- PRD-0B-IMPL-15 sample-enriched dictionary latency/readiness audit
- PRD-0B-IMPL-16 Phase 0B readiness rollup
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved

## Explicit non-approvals
- no new archive reads beyond IMPL-13
- no archive reads without explicit --archive-root
- no recursive full-archive scan
- no unbounded parquet glob
- no full data import
- no generated dictionary files
- no generated SQL outputs
- no generated reports
- no persistent `.duckdb` files
- no fixture derivation
- no committed fixtures
- no raw row payload capture
- no full archive-derived payload capture
- no user/event/trader personal data dumps
- no production model features
- no strategy labels
- no trade/opportunity labels
- no production loaders
- no query engine service
- no connectors/API calls
- no order placement
- no live trading
- no autonomous execution
- no weather implementation
- no production readiness claim
- no production latency SLO claim
- no final trading readiness claim
