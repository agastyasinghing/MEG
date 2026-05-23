# PRD-0B-IMPL-08 Query Latency Gate Skeleton

## Purpose and posture
This ticket adds a synthetic-only, in-memory query latency gate skeleton for PRD Phase 0B. It is a performance-contract harness for internal development posture only and is not a production readiness claim.

## Relationship to PRD-0B-IMPL-06 and IMPL-07
The gate consumes the existing Bronze/Silver view skeleton from IMPL-06 and semantic hardening posture from IMPL-07, and measures approved read-only queries against those in-memory synthetic views.

## Query spec contract
Each query spec contains:
- `name`
- `description`
- `sql`
- `expected_min_rows`
- `budget_ms`
- `source_posture`

All specs must declare `source_posture=synthetic_in_memory_only`.

## Approved query names
- `silver_view_inventory`
- `unresolved_status_counts`
- `dependency_status_counts`
- `kalshi_fill_dependency_scan`
- `poly_clob_dependency_scan`
- `legacy_fpmm_dependency_scan`
- `bronze_row_count_scan`

## Synthetic-only latency budgets
Budgets are intentionally soft and conservative to reduce CI timing flake. They are only meaningful for synthetic in-memory contract smoke and are not service-level objectives.

## In-memory gate behavior
- Build DuckDB with `:memory:` only.
- Create synthetic source relations.
- Load Bronze/Silver SQL definitions and apply views in memory.
- Validate query specs for read-only and synthetic-only posture.
- Execute approved queries, capture elapsed milliseconds, and collect row counts.

## JSON summary shape
The gate returns:
- `ok`
- `status`
- `query_count`
- `passed_query_count`
- `failed_query_count`
- `max_elapsed_ms`
- `total_elapsed_ms`
- `budgets_are_synthetic_only`
- `source_posture`
- `wrote_outputs`
- `created_duckdb_file`
- `query_results[]` containing:
  - `name`
  - `status`
  - `elapsed_ms`
  - `budget_ms`
  - `row_count`
  - `expected_min_rows`
  - `warning`

## Safety/no-output guarantees
- no archive reads
- no parquet_scan
- no full data import
- no generated SQL outputs
- no generated reports
- no generated dictionary files
- no fixture derivation
- no fixture commit
- no production loaders
- no query engine service
- no connectors/API calls
- no order placement
- no live trading
- no autonomous execution
- no weather implementation
- no production latency SLO claim
- no final trading readiness claim
- no .duckdb files

## What counts as success
Success means the harness validates the query contract, runs approved read-only queries against synthetic in-memory Bronze/Silver views, and emits consistent JSON summary output with pass/fail flags.

## What remains out of scope
This ticket intentionally excludes archive-backed bounded smoke checks, any runtime service integration, connector integration, and real data pipeline validation.

## Relationship to PRD-0A
This gate supports Phase 0B research scaffolding and does not change Phase 0A shared-rail execution authority posture.

## Recommended next tickets
- PRD-0B-IMPL-09 archive-backed bounded smoke approval gate
- PRD-0B-IMPL-10 bounded archive query smoke
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved
