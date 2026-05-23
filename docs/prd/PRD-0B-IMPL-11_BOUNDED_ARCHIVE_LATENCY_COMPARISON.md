# PRD-0B-IMPL-11 — Bounded Archive Latency Comparison

## Purpose and posture
Local-only bounded smoke comparison harness between synthetic latency gate and bounded archive smoke summary. No production latency SLO claim and no final trading readiness claim.

## Relationship to PRD-0B-IMPL-08
Reuses synthetic gate contract and timing fields from IMPL-08 through `run_latency_gate()`.

## Relationship to PRD-0B-IMPL-10
Reuses bounded archive family selection/query smoke behavior from IMPL-10 through `run_bounded_archive_query_smoke()`.

## Comparison input contract
- Explicit `archive_root` is required.
- Optional `row_limit` (default 1000).
- Optional repeatable family allowlist.
- Optional unresolved-case toggle.

## Timing normalization
The harness normalizes total elapsed ms, max elapsed ms, and query counts for both synthetic and archive summaries into one JSON-safe structure.

## Ratio and interpretation semantics
- Synthetic missing/zero timing: `insufficient_synthetic_timing`.
- Archive not ok: `archive_smoke_not_ok`.
- Synthetic not ok: `synthetic_gate_not_ok`.
- Ratio <= 10: `archive_within_synthetic_smoke_band`.
- Ratio > 10: `archive_slower_than_synthetic_smoke_band`.

## JSON summary shape
Includes: `ok`, `status`, `source_posture`, `archive_root_status`, `synthetic_status`, `archive_status`, `synthetic_query_count`, `archive_query_count`, `synthetic_total_elapsed_ms`, `archive_total_elapsed_ms`, `synthetic_max_elapsed_ms`, `archive_max_elapsed_ms`, `comparison_ratio_archive_to_synthetic`, `comparison_interpretation`, `row_limit`, `checked_families`, `missing_families`, `warnings`, `wrote_outputs`, `created_duckdb_file`, `generated_artifacts`, `production_slo_claim`, `final_trading_readiness_claim`.

## CLI behavior
`python -m scripts.prd_0b.bounded_archive_latency_comparison run --archive-root <path> [--row-limit N] [--family X ...] [--without-unresolved-cases] [--json]`
- `--json` prints JSON.
- default prints human-readable summary.
- exit 0 when `ok=true`; otherwise exit 1.

## Test posture using synthetic mini-archives
Tests create temporary mini archives only (tiny parquet + JSON sidecar), with no real archive use.

## Safety/no-output guarantees
- no archive reads without explicit --archive-root
- no real archive access in tests
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

## What counts as success
Harness returns a complete local comparison summary and safe status interpretation without writing artifacts.

## What remains out of scope
Production SLO validation, readiness sign-off, remote APIs/connectors, order routing, and strategy implementation.

## Relationship to PRD-0A
Supports Phase 0A/0B shared rail validation posture only; does not change execution authority.

## Recommended next tickets
- PRD-0B-IMPL-12 archive-backed data dictionary sample enrichment approval gate
- PRD-0B-IMPL-13 archive-backed data dictionary sample enrichment
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved
