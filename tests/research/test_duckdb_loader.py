from __future__ import annotations

from pathlib import Path

import duckdb

from meg.research.duckdb_lake.loader import (
    NORMALIZED_FILLS_COLUMNS,
    connect_duckdb,
    create_normalized_fills_table,
    load_normalized_fills_csv,
    normalized_fills_row_count,
    normalized_fills_schema_fingerprint,
    validate_normalized_fills_ingest,
)

FIXTURE_PATH = Path("tests/fixtures/phase0b/normalized_fills_sample.csv")


def test_duckdb_in_memory_connection() -> None:
    conn = connect_duckdb()
    try:
        assert conn.execute("SELECT 1").fetchone()[0] == 1
    finally:
        conn.close()


def test_loader_create_load_and_validate() -> None:
    conn = connect_duckdb()
    try:
        create_normalized_fills_table(conn)
        loaded_rows = load_normalized_fills_csv(conn, FIXTURE_PATH)
        assert loaded_rows == 3
        assert normalized_fills_row_count(conn) == 3

        schema = normalized_fills_schema_fingerprint(conn)
        assert [name for name, _ in schema] == list(NORMALIZED_FILLS_COLUMNS)

        checks = validate_normalized_fills_ingest(conn, expected_rows=3)
        assert checks["row_count_matches"] is True
        assert checks["timestamp_min_ms"] == 1714500000000
        assert checks["timestamp_max_ms"] == 1714501200000
        assert checks["duplicate_key_rows"] == 0
        assert checks["source_non_null"] is True
    finally:
        conn.close()


def test_persistent_duckdb_only_in_temp_dir(tmp_path: Path) -> None:
    db_path = tmp_path / "phase0b_test.duckdb"
    conn = connect_duckdb(db_path)
    try:
        create_normalized_fills_table(conn)
        load_normalized_fills_csv(conn, FIXTURE_PATH)
    finally:
        conn.close()
    assert db_path.exists()


def test_loader_module_does_not_pull_runtime_rails() -> None:
    source = Path("meg/research/duckdb_lake/loader.py").read_text(encoding="utf-8")
    forbidden_tokens = ("redis", "postgres", "meg.execution", "meg.telegram", "sqlalchemy")
    for token in forbidden_tokens:
        assert token not in source.lower()
