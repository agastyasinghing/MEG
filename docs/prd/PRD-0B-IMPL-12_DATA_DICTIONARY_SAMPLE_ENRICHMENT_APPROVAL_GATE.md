# PRD-0B-IMPL-12 — Data Dictionary Sample Enrichment Approval Gate

## 1) Purpose and posture

This ticket is an **approval gate only** for a future bounded implementation ticket.

This ticket:
- does **not** read archives,
- does **not** execute `parquet_scan`,
- does **not** parse archive JSON,
- does **not** import data,
- does **not** enrich the data dictionary,
- does **not** create generated dictionary files,
- does **not** create reports,
- does **not** create fixtures,
- does **not** create `.duckdb` files,
- does **not** claim production readiness,
- does **not** claim final trading readiness.

## 2) Relationship to previous PRD-0B tickets

This approval gate is constrained by and extends prior PRD-0B work:
- PRD-0B-IMPL-03 data dictionary contract,
- PRD-0B-IMPL-05 local data dictionary generator,
- PRD-0B-IMPL-09 archive-backed bounded smoke approval gate,
- PRD-0B-IMPL-10 bounded archive query smoke,
- PRD-0B-IMPL-11 bounded archive latency comparison.

## 3) Why an approval gate is needed

Future sample enrichment will touch local archive paths and bounded representative files. Without explicit constraints, enrichment can drift into fixture derivation or generated dictionary outputs. This gate separates **approval** from **execution** and preserves data-contract safety before any sample-derived metadata is added.

## 4) Approved future IMPL-13 scope

Future IMPL-13 may:
- require an explicit `--archive-root` argument,
- reuse approved archive family specs from IMPL-10,
- use at most one representative file per approved family by default,
- use `row_limit` default 1000 or lower,
- inspect bounded schema/sample metadata only,
- enrich an in-memory data dictionary object only,
- print stdout JSON summary only,
- use tempdir-only outputs only for tests,
- default to no persistent outputs,
- fail closed on missing DuckDB,
- fail closed on missing archive family paths,
- fail closed on unsafe archive paths,
- fail closed on unknown family allowlist names,
- report sample enrichment status per family,
- preserve source-relative paths only.

## 5) Mandatory IMPL-13 limits

IMPL-13 must enforce all of the following:
- no recursive full-archive scan,
- no unbounded parquet glob,
- no more than one representative file per dataset family by default,
- no more than seven dataset families,
- no more than 1000 rows per query by default,
- no persistent `.duckdb` database file,
- no committed generated dictionary files,
- no generated SQL files,
- no generated reports,
- no committed fixtures,
- no fixture derivation,
- no network/API calls,
- no connectors,
- no order placement,
- no live trading,
- no autonomous execution,
- no weather implementation,
- no production readiness claim,
- no final trading readiness claim.

## 6) Required IMPL-13 input contract

Future IMPL-13 must require:
- `--archive-root`,
- explicit family allowlist support,
- explicit row limit,
- explicit representative-file selection strategy,
- explicit JSON summary mode,
- explicit no-output default,
- explicit fail-closed status fields,
- explicit sample enrichment mode name (for example `bounded_sample_metadata_only`).

## 7) Approved sample enrichment fields

Future IMPL-13 may add only bounded metadata fields such as:
- `sample_enrichment_status`,
- `sample_source_relative_path`,
- `sample_file_kind`,
- `sample_row_limit`,
- `sample_row_count_observed`,
- `sample_column_count_observed`,
- `sample_columns_observed`,
- `sample_elapsed_ms`,
- `sample_warning`,
- `sample_generated_from_archive_root: false` in committed outputs,
- `sample_persistent_output_written: false`.

Future IMPL-13 does **not** approve:
- raw row values,
- full archive-derived payloads,
- user/event/trader personal data dumps,
- fixture payloads,
- generated committed dictionaries,
- production model features,
- strategy labels,
- trade/opportunity labels.

## 8) Required IMPL-13 output summary shape

Future summary output must include:
- `ok`,
- `status`,
- `archive_root_status`,
- `duckdb_status`,
- `enrichment_mode`,
- `family_count`,
- `enriched_families`,
- `skipped_families`,
- `missing_families`,
- `representative_files`,
- `row_limit`,
- `sample_enrichment_results`,
- `warnings`,
- `wrote_outputs`,
- `created_duckdb_file`,
- `generated_artifacts`,
- `committed_fixtures`,
- `production_readiness_claim`,
- `final_trading_readiness_claim`.

## 9) Required IMPL-13 safety tests

Future IMPL-13 tests must validate:
- missing archive root fails closed,
- unsafe archive root rejected,
- missing family paths reported,
- unknown family allowlist fails closed,
- row limit enforced,
- representative file selection bounded,
- no recursive full scan,
- no unbounded parquet glob,
- no `.duckdb` files created,
- no generated dictionary files created by default,
- no generated reports created,
- no fixture commit,
- stdout JSON summary shape,
- tempdir-only output mode if any output mode is added,
- no network/API calls,
- no trading/autonomy/weather implementation,
- no production readiness claim,
- no final trading readiness claim.

## 10) Approval decision matrix

| Decision item | Approved for IMPL-13? | Required constraint | Failure mode if violated |
|---|---|---|---|
| Explicit archive root | Yes | Must require `--archive-root` | Fail closed with missing archive root status |
| Bounded representative files | Yes | Max one representative file per family by default | Fail closed with bounded-selection violation |
| Seven family coverage | Yes | Maximum seven approved families | Fail closed with family-count violation |
| Bounded schema/sample metadata | Yes | Metadata only; no raw payload extraction | Fail closed with data-scope violation |
| In-memory dictionary enrichment | Yes | Enrich runtime object only | Fail closed with persistence violation |
| Stdout JSON summary | Yes | JSON summary mode required | Fail closed with summary-mode violation |
| Tempdir-only test outputs | Yes | Tempdir-only and test-only | Fail closed with unsafe-output-path violation |
| Persistent dictionary output | No | Default no-output posture | Fail closed with persistent-output violation |
| Committed generated dictionary files | No | No committed generated artifacts | Fail closed with committed-artifact violation |
| Fixture derivation | No | No fixture derivation/commit | Fail closed with fixture-policy violation |
| Raw row payload capture | No | No raw row values or personal dumps | Fail closed with payload-scope violation |
| Network/API/connector calls | No | No network, API, or connector calls | Fail closed with external-call violation |
| Trading/autonomy/weather implementation | No | No order placement, live trading, autonomy, weather | Fail closed with execution-scope violation |
| Production readiness claims | No | No production or final trading readiness claims | Fail closed with readiness-claim violation |

## 11) Explicit non-approvals

For this ticket, explicit non-approvals are repeated and mandatory:
- no archive reads in this ticket,
- no `parquet_scan` in this ticket,
- no archive JSON parsing in this ticket,
- no full data import,
- no data dictionary enrichment in this ticket,
- no generated dictionary files,
- no generated SQL outputs,
- no generated reports,
- no `.duckdb` files,
- no fixture derivation,
- no fixture commit,
- no production loaders,
- no query engine service,
- no connectors/API calls,
- no order placement,
- no live trading,
- no autonomous execution,
- no weather implementation,
- no production readiness claim,
- no production latency SLO claim,
- no final trading readiness claim.

## 12) Recommended next tickets

- PRD-0B-IMPL-13 archive-backed data dictionary sample enrichment,
- PRD-0B-IMPL-14 sample-enriched dictionary contract hardening,
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel,
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved.
