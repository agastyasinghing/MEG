"""DuckDB historical-lake helpers for Phase 0B research workflows."""

from .loader import (
    PRICE_SNAPSHOTS_COLUMNS,
    NORMALIZED_FILLS_COLUMNS,
    connect_duckdb,
    create_normalized_fills_table,
    create_price_snapshots_table,
    load_normalized_fills_csv,
    load_price_snapshots_csv,
    normalized_fills_row_count,
    normalized_fills_schema_fingerprint,
    validate_normalized_fills_ingest,
)
from .queries import lead_lag_summary, market_price_after_trades, wallet_forward_returns

__all__ = [
    "connect_duckdb",
    "create_normalized_fills_table",
    "create_price_snapshots_table",
    "load_normalized_fills_csv",
    "load_price_snapshots_csv",
    "normalized_fills_row_count",
    "normalized_fills_schema_fingerprint",
    "validate_normalized_fills_ingest",
    "wallet_forward_returns",
    "market_price_after_trades",
    "lead_lag_summary",
    "NORMALIZED_FILLS_COLUMNS",
    "PRICE_SNAPSHOTS_COLUMNS",
]
