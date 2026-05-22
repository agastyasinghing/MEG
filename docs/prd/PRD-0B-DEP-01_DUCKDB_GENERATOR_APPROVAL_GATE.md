# PRD-0B-DEP-01 DuckDB Dependency Posture and Data Dictionary Generator Approval Gate

## 1) Purpose and posture
- This document defines **PRD-0B-DEP-01 DuckDB dependency posture and generator approval gate**.
- This ticket is **docs/static-preflight only**.
- This ticket does **not add DuckDB** or any other dependency.
- This ticket does **not implement the data dictionary generator**.
- This ticket does **not read archive payloads**.
- This ticket does **not run DuckDB**.
- This ticket does **not create generated outputs, .duckdb files, fixtures, SQL files, reports, loaders, query engines, connectors, API calls, order routing, live trading, autonomous execution, or weather implementation**.

## 2) PRD Phase 0B alignment
The master PRD Phase 0B requires DuckDB + Parquet + Becker setup, Bronze/Silver normalization views, a data dictionary, seven sanity queries, and a query latency gate. PRD-0B-IMPL-01 covered local research-lake smoke. PRD-0B-IMPL-02 covered the seven sanity-query harness. PRD-0B-IMPL-03 covered the data dictionary static contract. PRD-0B-IMPL-04 covered the Bronze/Silver view implementation plan. This ticket gates the next implementation step, PRD-0B-IMPL-05.

## 3) Current dependency posture
- DuckDB is **not approved as a committed project dependency** in this ticket.
- PRD-0B-IMPL-01 and PRD-0B-IMPL-02 treat DuckDB as an optional runtime/local dependency.
- `pyproject.toml` and lockfiles must remain unchanged in this ticket.
- Future dependency changes require an explicit dependency PR.

## 4) Dependency decision options

### Option A: Keep DuckDB optional local-only
- No `pyproject.toml` change.
- Generator can only run when an operator has DuckDB installed locally.
- CI tests must monkeypatch/fake DuckDB behavior or skip runtime DuckDB execution.
- Lower dependency risk.
- Weaker CI coverage for real DuckDB behavior.

### Option B: Add DuckDB as dev dependency
- Requires explicit dependency PR.
- `pyproject.toml` and lockfile changes allowed only in that PR.
- CI can test real DuckDB execution paths.
- Better reproducibility.
- Requires dependency review.

### Option C: Add DuckDB as runtime dependency
- Highest commitment.
- Only allowed if production/runtime code needs DuckDB.
- Not approved by this gate.
- Requires stronger justification.

## 5) Decision recommendation
- For PRD-0B-IMPL-05, keep DuckDB optional local-only unless a separate dependency PR is explicitly approved first.
- Implement the future generator to fail closed with `duckdb_unavailable` when DuckDB is missing.
- Keep tests standard-library/pytest with fake DuckDB unless dependency posture changes.
- Do not add DuckDB directly inside IMPL-05.

## 6) Generator approval gates
Before PRD-0B-IMPL-05 can implement a local generator, require all of the following:
- PRD-0B-IMPL-03 merged and green.
- PRD-0B-IMPL-04 merged and green.
- Explicit approval for archive metadata reads.
- Explicit approval for local-only DuckDB execution when available.
- Explicit approval for generated dictionary output path.
- Explicit decision whether generated dictionary is stdout-only, tempdir-only, or committed artifact.
- Explicit no absolute local archive paths in generated dictionary.
- Explicit no secrets/API keys/private PII.
- Explicit no full archive data in dictionary output.
- Explicit no `.duckdb` files.
- Explicit no generated reports unless separately approved.
- Explicit no Bronze/Silver views.
- Explicit no runtime loaders/connectors/trading/autonomy.

## 7) Approved IMPL-05 scope if this gate passes
PRD-0B-IMPL-05 may implement:
- local-only generator module/script
- optional DuckDB import
- in-memory DuckDB only
- schema metadata extraction from one sample per approved family
- column metadata dictionary assembly
- stdout JSON output or explicitly approved output path
- dry-run/no-write mode
- fail-closed missing family/column behavior
- tests using fake DuckDB and `tmp_path`

PRD-0B-IMPL-05 must not implement:
- full archive import
- row-level data export
- Bronze/Silver views
- SQL view files
- `.duckdb` files
- generated reports
- production loaders
- query engine service
- connectors/API calls
- order routing/live trading/autonomy
- weather implementation

## 8) Generated dictionary output policy
Defined output modes:
- `stdout_only`
- `tempdir_only_for_tests`
- `explicit_path_requires_approval`
- `committed_dictionary_requires_separate_approval`

Immediate IMPL-05 recommendation:
- `stdout_only` + `tempdir_only_for_tests` only.
- No committed generated dictionary file yet.

## 9) CI/testing policy
Future IMPL-05 tests should:
- not require real DuckDB unless a dependency PR has landed
- use fake DuckDB to validate query behavior
- use `tmp_path` for any tempdir-only output
- prove no `.duckdb` files
- prove no generated reports
- prove no fixture outputs
- prove no production runtime imports
- prove no `pyproject.toml`/lockfile changes

## 10) Relationship to PRD-0A
- This gate does not satisfy PRD-0A shared rail.
- The data dictionary generator remains local research-lake tooling.
- Runtime proposal, paper execution, Telegram, Postgres, Redis, heartbeat, and risk envelope work still require PRD-0A-AUDIT-01 and follow-up repairs.
- Weather paper engine remains blocked until 0A/0B readiness is resolved.

## 11) Recommended next tickets
- PRD-0B-IMPL-05 data dictionary local generator, optional-DuckDB/stdout-only/tempdir-test-only.
- PRD-0B-DEP-02 optional DuckDB dependency PR, only if we choose dev dependency path.
- PRD-0B-IMPL-06 Bronze/Silver DuckDB view skeleton, only after generator and dependency/source gates.
- PRD-0A-AUDIT-01 shared rail implementation gap audit in parallel.
- PRD-P1-WX remains blocked until 0A/0B readiness is resolved.

## 12) Explicit non-approvals
- No DuckDB dependency addition.
- No `pyproject.toml`/lockfile changes.
- No data dictionary generator.
- No archive reads.
- No DuckDB execution.
- No generated dictionary files.
- No SQL files.
- No generated reports.
- No `.duckdb` files.
- No fixture derivation.
- No fixture commit.
- No data import.
- No Bronze/Silver view implementation.
- No loader implementation.
- No query engine service.
- No connector implementation.
- No API calls.
- No order placement.
- No live trading.
- No autonomous execution.
- No weather implementation.
