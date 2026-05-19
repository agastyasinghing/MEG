"""DuckDB historical-lake helpers for Phase 0B research workflows."""

from .loader import (
    connect_duckdb,
    create_normalized_fills_table,
    load_normalized_fills_csv,
    normalized_fills_row_count,
    normalized_fills_schema_fingerprint,
    validate_normalized_fills_ingest,
)

__all__ = [
    "connect_duckdb",
    "create_normalized_fills_table",
    "load_normalized_fills_csv",
    "normalized_fills_row_count",
    "normalized_fills_schema_fingerprint",
    "validate_normalized_fills_ingest",
]
