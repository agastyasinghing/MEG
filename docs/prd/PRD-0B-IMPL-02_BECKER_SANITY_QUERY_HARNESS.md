# PRD-0B-IMPL-02 Becker Archive Sanity Query Harness

## Purpose and posture
This ticket adds a local-only, read-only sanity harness for bounded Becker archive checks. It does not import or transform archive datasets.

## PRD Phase 0B alignment
The harness validates source archive accessibility and minimal schema compatibility for Phase 0B preflight.

## Relationship to PRD-0B-IMPL-01
This extends the local research-lake smoke posture and reuses optional DuckDB import and archive root validation patterns.

## Seven sanity checks
1. `kalshi_markets_schema_count_sample`
2. `kalshi_trades_schema_count_sample`
3. `poly_markets_schema_count_sample`
4. `poly_clob_trades_schema_count_sample`
5. `poly_blocks_schema_count_sample`
6. `poly_legacy_fpmm_trades_schema_count_sample`
7. `poly_fpmm_collateral_lookup_presence`

## Local-only behavior
- Operator supplies `--archive-root`.
- Harness reads only small bounded metadata/query outputs.
- No network access and no secrets.

## DuckDB optional/no dependency added
DuckDB is optional at runtime via optional import logic; no dependency added to project manifests.

## Archive root requirements
Archive root must be an existing directory containing expected family folders.

## Harness CLI behavior
Command:
- `run --archive-root <path> [--row-limit 5] [--json] [--require-duckdb]`

Exit behavior:
- exit `0` only when summary `ok` is true
- exit non-zero otherwise

## Success/failure semantics
- `ok` is true only when checks satisfy required conditions.
- With `--require-duckdb`, DuckDB unavailability is a hard failure.
- Without `--require-duckdb`, DuckDB unavailability can still produce a non-fatal status for parquet checks, while sidecar checks continue.

## Safety/no-output guarantees
- no committed data
- no fixture commit
- no archive outputs
- no full import
- no Bronze/Silver view implementation
- no production loaders
- no query engine service
- no connectors/API calls
- no order routing
- no live trading
- no autonomous execution
- no `.duckdb` files
- no generated reports

## What remains out of scope
This ticket does not implement Bronze/Silver views, production loading, services, or any execution path.

## Recommended next tickets
- PRD-0B-IMPL-03 data dictionary generation plan/static contract
- PRD-0B-IMPL-04 Bronze/Silver view implementation plan
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
