# PRD-0B-QA-01 DuckDB Dependency and Lockfile Consolidation Smoke

## 1) Purpose and posture

This ticket is **PRD-0B-QA-01 DuckDB dependency and lockfile consolidation smoke**.

This work is **QA/static-preflight only**.

This ticket **does not add dependencies**.

This ticket **does not modify `pyproject.toml` or `uv.lock`**.

This ticket does **not** implement Bronze/Silver views, DuckDB queries, archive reads, generated outputs, loaders, connectors, trading, autonomy, or weather work.

## 2) Why this ticket exists

PRD-0B-DEP-02 required a DuckDB **dev/research dependency** posture and a committed `uv.lock`.

The dependency PR required local lockfile generation because Codex/package-index access was unreliable in that workflow.

This ticket consolidates the final desired state so future PRD-0B work does not inherit dependency-posture ambiguity.

Duplicate/superseded dependency branches or PRs are non-canonical after merged `main` contains the final lockfile posture.

## 3) Required final repo state

- `pyproject.toml` contains DuckDB only under dev/research dependency posture.
- `uv.lock` exists.
- `uv.lock` includes DuckDB.
- `tests/core/test_prd_0b_duckdb_dependency_posture.py` requires `uv.lock` and does not return early when absent.
- Existing PRD-0B local tools still use optional/fail-closed DuckDB imports.
- No `.duckdb` database files are committed.
- No generated SQL/report/dictionary/fixture outputs are committed.
- No archive data is committed.

## 4) PRD Phase 0B alignment

This ticket aligns with:

- PRD-0B-DEP-01 (`docs/prd/PRD-0B-DEP-01_DUCKDB_GENERATOR_APPROVAL_GATE.md`)
- PRD-0B-DEP-02 (`docs/prd/PRD-0B-DEP-02_DUCKDB_DEV_DEPENDENCY.md`)
- PRD-0B-IMPL-01 through PRD-0B-IMPL-05

This ticket prepares for **PRD-0B-IMPL-06 Bronze/Silver DuckDB view skeleton**.

## 5) Verification matrix

| Check | Evidence | Expected result | Failure meaning | Follow-up action |
|---|---|---|---|---|
| DuckDB in `pyproject.toml` dev/research group | `[dependency-groups].dev` contains `duckdb` | DuckDB appears only in dev/research posture | Dependency posture drift | Restore dev-only declaration and re-run static tests |
| DuckDB in `uv.lock` | `uv.lock` package entries include `duckdb` | Lockfile captures DuckDB | Reproducibility regression | Regenerate lockfile in approved dependency workflow |
| Mandatory lockfile test | `tests/core/test_prd_0b_duckdb_dependency_posture.py` has direct lockfile assertion | Missing lockfile is a hard failure | Lockfile accidentally became optional | Reinstate mandatory assertion and remove any early return |
| Optional DuckDB helper remains in local smoke | `scripts/prd_0b/local_research_lake_smoke.py` retains optional import helper | Unavailable DuckDB remains fail-closed | Script runtime posture drift | Restore helper and unavailable branch signaling |
| Optional DuckDB/fail-closed path remains in sanity harness | `scripts/prd_0b/becker_sanity_query_harness.py` routes unavailable DuckDB to fail-closed summary path | Optional posture preserved | Harness may hard-crash or silently bypass required checks | Restore unavailable handling and summary semantics |
| Optional DuckDB/fail-closed path remains in data dictionary generator | `scripts/prd_0b/data_dictionary_generator.py` preserves unavailable DuckDB branch when optional mode is used | Optional posture preserved | Dictionary generation posture drift | Restore unavailable warnings path and guarded behavior |
| No `.duckdb` files | Repository tree scan | Zero `.duckdb` files committed | Artifact hygiene violation | Remove committed database artifacts |
| No generated SQL files | No committed generated SQL output paths | Zero generated SQL artifacts from this ticket | Generated output leakage | Remove generated SQL artifacts and keep generation out of ticket |
| No generated reports | No committed generated report paths | Zero generated report artifacts from this ticket | Generated output leakage | Remove generated reports |
| No generated dictionary files | No committed generated dictionary outputs | Zero generated dictionary artifacts from this ticket | Generated output leakage | Remove generated dictionary artifacts |
| No fixture outputs from this ticket | No committed fixture-output directories from ticket scope | Zero fixture-output artifacts | Fixture hygiene violation | Remove fixture outputs and keep ticket static-only |
| No archive reads in this ticket | New QA checks are static file-content checks only | No archive data reads performed by QA consolidation tests | Scope overreach into data execution | Rework tests to static checks only |
| No runtime production module changes | Diff limited to docs + pytest QA test file | Production runtime remains unchanged | Scope violation | Revert production runtime edits |

## 6) Explicit non-approvals

- no dependency changes
- no lockfile changes
- no archive reads
- no DuckDB query execution
- no `.duckdb` files
- no generated SQL files
- no generated reports
- no generated dictionary files
- no fixture derivation
- no fixture commit
- no data import
- no Bronze/Silver view implementation
- no loader implementation
- no query engine service
- no connector implementation
- no API calls
- no order placement
- no live trading
- no autonomous execution
- no weather implementation

## 7) Recommended next ticket

Recommended next ticket: **PRD-0B-IMPL-06 Bronze/Silver DuckDB view skeleton**.

PRD-0B-IMPL-06 may rely on DuckDB availability through the dev/research dependency posture validated here.

PRD-0A-AUDIT-01 should continue in parallel because dependency posture does not satisfy shared rail readiness.

PRD-P1-WX remains blocked until 0A/0B readiness is resolved.
