# PRD-0B-IMPL-15 Sample-Enriched Dictionary Latency/Readiness Audit

## Purpose and posture
This ticket adds a local bounded audit harness that evaluates sample-enriched dictionary behavior from IMPL-13 and contract hardening from IMPL-14 without expanding scope.

## Relationship to PRD-0B-IMPL-13
The audit reuses IMPL-13 enrichment behavior exactly and only runs when an explicit archive root is provided.

## Relationship to PRD-0B-IMPL-14
The audit runs IMPL-14 validation against IMPL-13 runtime summaries and reports contract validation status and errors.

## Audit mode
- `sample_enriched_dictionary_local_audit_only`

## Input contract
- `archive_root` is required and explicit.
- `row_limit` defaults to 1000.
- `family_allowlist` is optional and follows IMPL-13 semantics.

## Timing audit fields
- `sample_result_count`
- `sample_total_elapsed_ms`
- `sample_max_elapsed_ms`
- `sample_avg_elapsed_ms`
- `slowest_sample_family`

Timing uses only `sample_elapsed_ms` values from IMPL-13 sample rows and does not introduce production thresholds or SLO claims.

## Contract validation audit
The audit invokes IMPL-14 validation helpers and returns:
- `contract_validation_status`
- `contract_errors`

## Readiness flag semantics
- Local flags may become true when audit passes:
  - `local_sample_enrichment_contract_ready`
  - `local_sample_enrichment_latency_observed`
- Production/trading approvals are always false:
  - `production_readiness_approved`
  - `production_latency_slo_approved`
  - `final_trading_readiness_approved`

## JSON summary shape
The audit returns a JSON-friendly dictionary with status, timing, contract, readiness, warnings, and no-output guard fields.

## CLI behavior
- `python -m scripts.prd_0b.sample_enriched_dictionary_audit run --archive-root <path> --json`
- `--archive-root` is required.
- `--row-limit` defaults to 1000.
- `--family` is repeatable.
- `--json` prints JSON; non-JSON prints human-readable summary.
- Exit code 0 when `ok=true`; otherwise exit code 1.

## Test posture using synthetic mini-archives
Tests use only synthetic mini-archives and temporary paths. No production archive roots or external sources are used.

## Safety/no-output guarantees
The audit does not write outputs, does not create persistent `.duckdb` files, and does not commit fixtures or generated artifacts.

## What counts as success
- IMPL-13 enrichment summary is ok.
- IMPL-14 contract validation passes.
- Timing fields are computed from sample metadata.
- No output/artifact flags are set.
- No production readiness, latency SLO, or final trading readiness claims are made.

## What remains out of scope
Production loaders, query engine service, connectors/API calls, order placement, autonomous execution, weather implementation, and live trading remain out of scope.

## Relationship to PRD-0A
This audit supports Phase 0A/0B safety posture and shared-rail readiness by preserving local-only, no-output behavior.

## Recommended next tickets
- PRD-0B-IMPL-16 Phase 0B readiness rollup
- PRD-0B-IMPL-17 Phase 0B merge/readiness decision gate
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
