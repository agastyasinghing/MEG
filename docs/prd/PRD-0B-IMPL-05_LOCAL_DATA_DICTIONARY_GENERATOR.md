# PRD-0B-IMPL-05 Local Data Dictionary Generator

## Purpose and posture
Local-only generator for PRD-0B data dictionary JSON from static dataset specs and optional/local-only DuckDB schema metadata.

## PRD Phase 0B alignment
Implements dictionary generation gate after IMPL-01/02/03/04 and DEP-01; remains research-only and operator-safe.

## Relationship to PRD-0B-DEP-01
Dependency posture remains optional/local-only. No dependency addition is approved in this ticket.

## DuckDB optional/local-only behavior
DuckDB is optional/local-only runtime path through `try_import_duckdb`; unavailable DuckDB returns static fallback unless `--require-duckdb` is set.

## Dataset coverage
Exactly seven datasets:
- kalshi_markets
- kalshi_trades
- poly_markets
- poly_clob_trades
- poly_blocks
- poly_legacy_fpmm_trades
- poly_fpmm_collateral_lookup

## Generator modes
- `static_specs_only`
- `duckdb_schema_metadata_if_available`

## Output modes
- `stdout_only`
- `tempdir_only_for_tests`

Blocked:
- `explicit_path_requires_approval`
- `committed_dictionary_requires_separate_approval`

## Dictionary shape
Top-level fields: dictionary_ref, schema_version, phase, dictionary_status, created_by, created_at, source_manifest_ref, source_repo_ref, source_repo_commit, source_archive_ref, generation_mode, dataset_entries, global_posture, artifact_hygiene, reviewer_envelope.

## Column metadata behavior
Includes required per-column metadata fields with static defaults and optional observed type fill when DuckDB metadata is available.

## Safety/no-output guarantees
- No DuckDB dependency addition
- no pyproject/lockfile changes
- no committed generated dictionary file
- no row-level archive export
- no full archive import
- no .duckdb files
- no generated reports
- no fixtures
- no Bronze/Silver views
- no SQL files
- no production loaders
- no query engine service
- no connectors/API calls
- no order routing/live trading/autonomy
- no weather implementation

## CLI behavior
`python -m scripts.prd_0b.data_dictionary_generator generate ...`

Requires source refs and created-by; supports mode, output-mode, optional archive-root and optional require-duckdb.

## What counts as success
- Generates dictionary JSON to stdout or tempdir-only test output.
- No committed artifacts or runtime side effects.

## What remains out of scope
Any production loader/service, Bronze/Silver view implementation, SQL/view generation, dependency changes, or live execution integrations.

## Recommended next tickets
- PRD-0B-DEP-02 optional DuckDB dev dependency PR if choosing dependency path
- PRD-0B-IMPL-06 Bronze/Silver DuckDB view skeleton after dependency/source gates
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved
