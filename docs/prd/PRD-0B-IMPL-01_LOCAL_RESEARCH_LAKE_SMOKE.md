# PRD-0B-IMPL-01 Local Research Lake Smoke

## Purpose and posture
This ticket adds a local-only preflight smoke command for Phase 0B research-lake readiness.

## PRD Phase 0B alignment
The command validates archive layout and optionally runs tiny read-only DuckDB checks over approved parquet families.

## Local-only behavior
Execution is operator-invoked against a local archive root and does not alter repository state.

## Dependency posture
DuckDB is optional in this ticket and imported only at runtime in an optional path. No dependency added. (no dependency added)

## Archive root requirements
The archive root must exist, be a directory, avoid parent traversal path segments, and contain expected family paths.

## Expected family directories
- data/kalshi/markets
- data/kalshi/trades
- data/polymarket/blocks
- data/polymarket/markets
- data/polymarket/trades
- data/polymarket/legacy_trades

Expected JSON sidecar:
- data/polymarket/fpmm_collateral_lookup.json

## Smoke command behavior
`python scripts/prd_0b/local_research_lake_smoke.py check --archive-root <path> --json`

Behavior:
- validates archive root safety constraints
- discovers expected families and one sample parquet per family
- ignores AppleDouble prefixed entries
- if DuckDB is available locally, uses in-memory connection only and runs tiny DESCRIBE/COUNT smoke checks
- returns structured JSON with reasons and warnings

## Safety/non-output guarantees
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
- no .duckdb file creation
- no report generation

## What counts as success
Success means archive root validation passes, family discovery runs, and either:
- DuckDB is available and tiny read-only smoke queries complete, or
- DuckDB is unavailable and explicit status is returned for follow-up local install.

## What remains out of scope
This ticket does not implement Bronze/Silver views, fixture derivation, full archive import, or production runtime pipelines.

## Recommended next tickets
- PRD-0B-IMPL-02 Becker archive sanity-query harness
- PRD-0B-IMPL-03 data dictionary generation plan/static contract
- PRD-0B-IMPL-04 Bronze/Silver view implementation plan
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
