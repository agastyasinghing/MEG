# PRD-0B-IMPL-07 Bronze/Silver Semantic Hardening

## Purpose and posture
This ticket hardens PRD-0B Bronze/Silver skeleton semantics for synthetic, in-memory validation only.

## Relationship to PRD-0B-IMPL-06
IMPL-06 introduced view skeleton topology. IMPL-07 keeps the same approved view set and strengthens semantic status columns, unresolved propagation, and dependency visibility.

## Bronze semantic contract
Each Bronze view exposes: source_dataset, source_platform, source_relative_path, bronze_view_version, raw_ingested_at, source_record_ref, bronze_unresolved_status, required_field_status.

## Silver semantic contract
Each Silver view exposes: silver_view_version, source_platform, normalized_entity_type, source_dataset, source_relative_path, source_record_ref, unresolved_status, dependency_status, and stable reference fields.

## Required unresolved/dependency cases
Synthetic rows include missing Kalshi market join, missing Polymarket CLOB market join, missing Polymarket block join, missing legacy collateral join, and missing required raw references.

## Synthetic-only test posture
Only in-memory DuckDB sources are used. No archive files, fixture ingestion, or external loaders are used.

## In-memory smoke summary
Summary includes ok, status, view counts, missing views, row_count_checks, unresolved_status_counts, dependency_status_counts, warnings, wrote_outputs false, created_duckdb_file false.

## Safety/no-output guarantees
No output artifacts are written.

## What counts as success
Expected views exist, unresolved and missing dependencies are preserved and observable, and CLI JSON smoke returns status ok.

## What remains out of scope
Archive-scale implementation, final normalization, and trading readiness.

## Relationship to PRD-0A
This work stays aligned with shared rails and does not add autonomous execution authority.

## Recommended next tickets
- PRD-0B-IMPL-08 query latency gate skeleton
- PRD-0B-IMPL-09 archive-backed bounded smoke approval gate
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved

## Explicit non-approvals
- no archive reads
- no parquet_scan
- no full data import
- no generated SQL outputs
- no generated reports
- no generated dictionary files
- no .duckdb files
- no fixture derivation
- no fixture commit
- no production loaders
- no query engine service
- no connectors/API calls
- no order placement
- no live trading
- no autonomous execution
- no weather implementation
- no cross-platform opportunity labels
- no cross-platform equivalence claims
- no final trading readiness claim
