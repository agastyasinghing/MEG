# PRD-0B-IMPL-06 Bronze/Silver DuckDB View Skeleton

## Purpose and posture
This ticket adds a skeleton-only Bronze/Silver DuckDB view layer and an in-memory smoke runner.

## PRD Phase 0B alignment
This aligns with Phase 0B research-lake contracts and does not introduce production execution readiness.

## Relationship to PRD-0B-DEP-02 and QA-01
DuckDB is consumed through the approved dev/research dependency posture and lockfile consolidation smoke baseline.

## Source relation assumptions
Views assume these source relations already exist in the connection:
`source_kalshi_markets`, `source_kalshi_trades`, `source_poly_markets`, `source_poly_clob_trades`, `source_poly_blocks`, `source_poly_legacy_fpmm_trades`, `source_poly_fpmm_collateral_lookup`.

## Bronze view skeletons
Seven Bronze views are committed in `sql/prd_0b/bronze_views.sql` with shared metadata columns:
`source_dataset`, `source_relative_path`, `bronze_view_version`, `raw_ingested_at`, `unresolved_status`, `source_record_ref`.

## Silver view skeletons
Planned Kalshi and Polymarket Silver views are committed in `sql/prd_0b/silver_views.sql` with:
`silver_view_version`, `source_platform`, `normalized_entity_type`, `unresolved_status`, `source_dataset`, `source_relative_path`, and stable references.

## Dependency map
- Bronze views depend only on `source_*` relations.
- Silver views depend only on Bronze views.
- Runner applies Bronze SQL before Silver SQL.

## Unresolved-state taxonomy
- none
- missing_source_record
- missing_required_raw_field
- malformed_raw_value
- unresolved_ticker_ref
- unresolved_event_ref
- unresolved_result
- unresolved_taker_side
- unresolved_condition_ref
- unresolved_token_ref
- unresolved_token_outcome_mapping
- unresolved_block_timestamp
- timestamp_mismatch
- unresolved_legacy_fpmm_ref
- unresolved_collateral_ref
- unsupported_source_shape

## In-memory smoke behavior
`scripts/prd_0b/run_view_smoke.py` creates synthetic source relations, applies SQL, verifies expected views, and emits an in-memory summary.

## Safety/no-output guarantees
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
- no final trading readiness claim

## What counts as success
- SQL skeleton files are committed.
- In-memory smoke passes and confirms expected Bronze/Silver view names.
- Summary reports no output writes and no DuckDB file creation.

## What remains out of scope
Semantic hardening, archive-scale inputs, cross-platform equivalence, and readiness claims remain out of scope.

## Relationship to PRD-0A
This work stays in Phase 0B research shape and does not alter Phase 0A shared rails.

## Recommended next tickets
- PRD-0B-IMPL-07 Bronze/Silver view semantic hardening
- PRD-0B-IMPL-08 query latency gate skeleton
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved
