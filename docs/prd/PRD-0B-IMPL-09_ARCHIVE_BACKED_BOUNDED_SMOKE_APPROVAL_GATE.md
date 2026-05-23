# PRD-0B-IMPL-09 Archive-Backed Bounded Smoke Approval Gate

## 1. Purpose and posture
This ticket is an approval gate only.

This ticket does not read archives.

This ticket does not execute parquet_scan.

This ticket does not import data.

This ticket does not create fixtures.

This ticket does not create generated outputs.

This ticket does not create `.duckdb` files.

This ticket does not claim production latency or trading readiness.

## 2. Relationship to previous PRD-0B tickets
This approval gate depends on and follows the accepted posture from:
- IMPL-02 Becker sanity harness
- IMPL-03 data dictionary contract
- IMPL-04 Bronze/Silver plan
- IMPL-05 data dictionary generator
- IMPL-06 view skeleton
- IMPL-07 semantic hardening
- IMPL-08 synthetic latency gate

## 3. Why an approval gate is needed
The next implementation step touches local archive paths and bounded parquet/json reads.

That step requires explicit limits before implementation starts.

This gate prevents accidental full-archive scans or generated artifact commits.

This gate separates approval from execution so policy is explicit before bounded smoke logic is added.

## 4. Approved future IMPL-10 scope
Future IMPL-10 may:
- require an explicit `--archive-root` argument
- reject missing or unsafe archive roots
- run bounded schema/row-count queries against a tiny subset only
- use strict row limits
- use source-relative family names
- produce stdout JSON summaries
- use tempdir-only outputs only if tests need it
- default to no persistent outputs
- fail closed on missing DuckDB
- fail closed when archive family paths are missing
- record elapsed query timings as local smoke only

## 5. Mandatory IMPL-10 limits
IMPL-10 must enforce all limits below:
- no recursive full-archive scan
- no unbounded parquet glob
- no more than one representative file per dataset family by default
- no more than seven dataset families
- no more than 1000 rows per query by default
- no persistent `.duckdb` database file
- no generated SQL files
- no generated reports
- no generated data dictionary files
- no committed fixtures
- no network/API calls
- no connectors
- no order placement
- no live trading
- no autonomous execution
- no weather implementation
- no production latency SLO claim
- no final trading readiness claim

## 6. Required IMPL-10 input contract
Future IMPL-10 must require:
- `--archive-root`
- explicit family allowlist
- explicit row limit
- explicit representative-file selection strategy
- explicit JSON summary mode
- explicit no-output default
- explicit fail-closed status fields

## 7. Required IMPL-10 output summary shape
Future summary must include:
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

## 8. Required IMPL-10 safety tests
Future tests must validate:
- missing archive root fails closed
- unsafe archive root rejected
- missing family paths reported
- no recursive full scan
- representative file selection bounded
- row limit enforced
- no `.duckdb` files created
- no generated outputs created
- no fixture commit
- no network/API calls
- no trading/autonomy/weather implementation
- JSON summary shape

## 9. Approval decision matrix
| Decision item | Approved for IMPL-10? | Required constraint | Failure mode if violated |
|---|---|---|---|
| Local archive root argument | Yes | `--archive-root` required and validated | Fail closed with non-ok status |
| Bounded representative file selection | Yes | At most one representative file per family by default | Fail closed and mark bounded-selection violation |
| Seven family coverage | Yes | No more than seven dataset families | Fail closed and report over-scope family count |
| Row-count/schema-only queries | Yes | Bounded schema/row-count query posture only | Fail closed and report unapproved query posture |
| JSON stdout summary | Yes | Explicit JSON summary mode required | Fail closed and report summary-mode contract breach |
| Tempdir-only test outputs | Yes | Allowed only for tests; default no persistent outputs | Fail closed and report output policy violation |
| Persistent database files | No | No persistent `.duckdb` file creation | Fail closed and report persistent DB artifact violation |
| Generated SQL/report/dictionary files | No | No generated SQL/report/dictionary artifacts | Fail closed and report generated artifact violation |
| Fixture derivation | No | No fixture derivation or fixture commit | Fail closed and report fixture policy violation |
| Network/API/connector calls | No | No connectors and no network/API calls | Fail closed and report external I/O policy violation |
| Trading/autonomy/weather implementation | No | No order placement, no live trading, no autonomous execution, no weather implementation | Fail closed and report forbidden execution-domain behavior |
| Production latency/readiness claims | No | Local smoke timing only; no production SLO/readiness claim | Fail closed and report readiness-claim policy violation |

## 10. Explicit non-approvals
This ticket explicitly does not approve:
- no archive reads in this ticket
- no parquet_scan in this ticket
- no full data import
- no generated SQL outputs
- no generated reports
- no generated dictionary files
- no `.duckdb` files
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

## 11. Recommended next tickets
- PRD-0B-IMPL-10 bounded archive query smoke
- PRD-0B-IMPL-11 bounded archive latency comparison
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved
