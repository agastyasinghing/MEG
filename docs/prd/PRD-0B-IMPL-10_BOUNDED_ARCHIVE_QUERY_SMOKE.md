# PRD-0B-IMPL-10 Bounded Archive Query Smoke

## Purpose and posture
PRD-0B-IMPL-10 is the first bounded archive-backed smoke implementation after the IMPL-09 approval gate.

Its purpose is local-only, tiny-footprint validation of approved archive family slices using an explicit archive root and bounded row/sample checks.

This ticket is fail-closed by design and does not claim production readiness.

## Relationship to PRD-0B-IMPL-09
This implementation inherits and enforces the IMPL-09 approval posture:
- explicit archive-root requirement
- bounded representative file selection
- bounded per-file query posture
- no persistent artifacts
- no connectors or execution-domain behavior

## Approved dataset families
Exactly seven approved families are in scope:
- kalshi_markets -> `kalshi/markets`
- kalshi_trades -> `kalshi/trades`
- poly_markets -> `polymarket/markets`
- poly_clob_trades -> `polymarket/trades`
- poly_blocks -> `polymarket/blocks`
- poly_legacy_fpmm_trades -> `polymarket/legacy_trades`
- poly_fpmm_collateral_lookup -> `polymarket/fpmm_collateral_lookup.json`

## Archive root contract
- `--archive-root` is required at CLI.
- no archive reads without explicit --archive-root.
- Archive root must exist and be a directory.
- Archive root may be absolute or relative.
- Selected paths must resolve within archive root.
- Unsafe/out-of-root candidates fail closed.

## Representative file selection
- At most one representative file per family.
- No recursive full-archive scan.
- No unbounded parquet glob.
- Directory-backed parquet families inspect only their own family directory.
- First sorted `.parquet` is selected when present.
- AppleDouble/resource fork artifacts (`._*.parquet`) are ignored.
- JSON sidecar family uses exact JSON path.
- Missing family path is reported in `missing_families` and does not crash.

## Bounded DuckDB query posture
- DuckDB usage occurs only inside invoked run logic.
- In-memory connection only (`:memory:`).
- No persistent `.duckdb` files.
- Parquet checks are bounded with `LIMIT row_limit`.
- JSON sidecar receives presence/shape style summary only.
- No joins.
- No writes.
- No `CREATE TABLE`/`CREATE VIEW`.
- No `COPY`/`INSERT`/`UPDATE`/`DELETE`.
- No `ATTACH`/`EXPORT`/`INSTALL`/`LOAD`.

## Row limit policy
- Default row_limit is 1000.
- `row_limit <= 0` fails closed.
- `row_limit > 1000` fails closed.

## JSON summary shape
The summary includes:
- ok
- status
- archive_root_status
- duckdb_status
- family_count
- checked_families
- skipped_families
- missing_families
- representative_files
- row_limit
- query_results
- elapsed_ms_by_query
- warnings
- wrote_outputs
- created_duckdb_file
- generated_artifacts

## Failure/status semantics
Fail-closed outcomes include:
- missing/invalid archive root
- unsafe archive path detection
- unknown family allowlist names
- missing required family paths
- invalid row-limit values
- missing DuckDB
- policy violation indicators

## CLI behavior
Command:
`python -m scripts.prd_0b.bounded_archive_query_smoke run --archive-root <path> [--row-limit N] [--family NAME ...] [--json]`

Behavior:
- `--json` prints JSON summary.
- Without `--json`, prints human-readable non-JSON summary.
- Exit code `0` only when `ok` is true.
- Exit code `1` when `ok` is false.
- Bad archive root exits non-zero.
- Bad archive root with `--json` emits JSON summary when possible.

## Test posture using synthetic mini-archives
- Tests use temporary synthetic mini-archives only.
- Tests generate tiny parquet files in temp directories only.
- Tests create exact JSON sidecar in temp directories only.
- No repository data directory is used.
- No real Becker or external archive path is used.

## Safety/no-output guarantees
- no generated SQL outputs
- no generated reports
- no generated dictionary files
- no persistent `.duckdb` files
- no fixture derivation
- no committed fixtures
- wrote_outputs remains false
- generated_artifacts remains empty

## What counts as success
Success requires all of the following:
- valid archive root
- DuckDB available
- bounded representative selection succeeds safely
- at least one family checked
- no required family missing in active scope
- all checked family query results pass
- no artifact/persistence policy violations

## What remains out of scope
- no real archive access in tests
- no full data import
- no production loaders
- no query engine service
- no connectors/API calls
- no order placement
- no live trading
- no autonomous execution
- no weather implementation
- no production latency SLO claim
- no final trading readiness claim

## Relationship to PRD-0A
This is Phase 0B local research smoke infrastructure only.

It does not change PRD-0A shared rail scope or execution authority posture.

## Recommended next tickets
- PRD-0B-IMPL-11 bounded archive latency comparison
- PRD-0B-IMPL-12 archive-backed data dictionary sample enrichment approval gate
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved

## Explicit non-approvals
- no real archive access in tests
- no archive reads without explicit --archive-root
- no recursive full-archive scan
- no unbounded parquet glob
- no full data import
- no generated SQL outputs
- no generated reports
- no generated dictionary files
- no persistent `.duckdb` files
- no fixture derivation
- no committed fixtures
- no production loaders
- no query engine service
- no connectors/API calls
- no order placement
- no live trading
- no autonomous execution
- no weather implementation
- no production latency SLO claim
- no final trading readiness claim
