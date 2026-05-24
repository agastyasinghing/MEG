# PRD-0B-IMPL-13 Data Dictionary Sample Enrichment

## Purpose and posture
Bounded, local-only, archive-backed sample metadata enrichment for in-memory dictionary structures.

## Relationship to PRD-0B-IMPL-12
Implements the exact IMPL-12 approval gate and fail-closed posture.

## Reused IMPL-10 archive selection posture
Reuses approved family specs and representative-file selection from IMPL-10.

## Sample enrichment mode
`bounded_sample_metadata_only`

## Approved sample metadata fields
family, source_platform, source_kind, source_relative_path, sample_enrichment_status, sample_source_relative_path, sample_file_kind, sample_row_limit, sample_row_count_observed, sample_column_count_observed, sample_columns_observed, sample_elapsed_ms, sample_warning, sample_generated_from_archive_root, sample_persistent_output_written.

Runtime summaries may set `sample_generated_from_archive_root=true` when bounded metadata is read from an explicit archive root. Committed/static/default repository artifacts must not claim archive-derived generation because no generated enrichment artifacts are committed.

## In-memory dictionary enrichment behavior
Only enriches in-memory dictionary-like object and returns JSON-friendly summary; no files are written.

## Archive root contract
Explicit `--archive-root` is required and must be valid/safe.

## Representative file selection
At most one representative file per approved family.

## Row limit policy
Row limit must be within 1..1000, fail closed otherwise.

## JSON summary shape
Includes: ok, status, archive_root_status, duckdb_status, enrichment_mode, family_count, enriched_families, skipped_families, missing_families, representative_files, row_limit, sample_enrichment_results, warnings, wrote_outputs, created_duckdb_file, generated_artifacts, committed_fixtures, production_readiness_claim, final_trading_readiness_claim.

## Failure/status semantics
Fail-closed for missing/invalid/unsafe archive root, unknown family, invalid row limit, missing family, missing DuckDB, and empty active family set.

## CLI behavior
`python -m scripts.prd_0b.data_dictionary_sample_enrichment run --archive-root <path> [--row-limit N] [--family NAME] [--json]`

## Test posture using synthetic mini-archives
Tests only use temporary synthetic mini-archives.

## Safety/no-output guarantees
No generated dictionary files, no generated SQL outputs, no generated reports, no persistent `.duckdb` files, no committed fixtures.

## What counts as success
All active families are enriched with bounded metadata and summary `ok=true`.

## What remains out of scope
Production loaders, query engine service, connectors/API calls, order placement, live trading, autonomous execution, weather implementation.

## Relationship to PRD-0A
Supports shared rail readiness while preserving operator-approved execution posture.

## Recommended next tickets
- PRD-0B-IMPL-14 sample-enriched dictionary contract hardening
- PRD-0B-IMPL-15 sample-enriched dictionary latency/readiness audit
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved

## Explicit non-approvals
- no real archive access in tests
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
