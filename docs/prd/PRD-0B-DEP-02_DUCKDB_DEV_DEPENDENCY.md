# PRD-0B-DEP-02 DuckDB Dev Dependency

## 1) Purpose and posture
This ticket adds DuckDB as a dev/research dependency for PRD Phase 0B.

This ticket does not implement Bronze/Silver views. This ticket does not read archive data. This ticket does not create `.duckdb` files or generated outputs. This ticket does not implement loaders, connectors, API calls, trading, autonomy, or weather work.

## 2) PRD Phase 0B alignment
DuckDB support is required for reproducible research-lake execution, Becker sanity-query execution, future Bronze/Silver view skeleton work, and future query-latency gate coverage in CI.

This follows PRD-0B-DEP-01, which explicitly allowed a separate dependency PR for DuckDB. Existing optional DuckDB tooling already exists in PRD-0B-IMPL-01, PRD-0B-IMPL-02, and PRD-0B-IMPL-05.

## 3) Dependency placement
DuckDB was added in `pyproject.toml` under `[dependency-groups].dev`.

DuckDB is dev/research-only in this change and is not a production runtime dependency. This preserves the existing runtime dependency posture while enabling reproducible CI/lab execution for PRD-0B research utilities.

## 4) Backward compatibility
Existing optional import behavior remains valid.

Local tooling continues to fail closed when DuckDB import is unavailable in unusual environments.

Future tests can now add real DuckDB coverage where CI environment and lockfile policy permit.

## 5) Explicit non-approvals
- no archive reads
- no data import
- no generated outputs
- no `.duckdb` files
- no fixtures
- no Bronze/Silver view implementation
- no SQL files
- no production loaders
- no query engine service
- no connectors/API calls
- no order routing/live trading/autonomy
- no weather implementation
