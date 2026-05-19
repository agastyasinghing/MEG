from __future__ import annotations

from pathlib import Path

from meg.research.duckdb_lake.loader import (
    connect_duckdb,
    create_normalized_fills_table,
    create_price_snapshots_table,
    load_normalized_fills_csv,
    load_price_snapshots_csv,
)
from meg.research.duckdb_lake.queries import lead_lag_summary, market_price_after_trades, wallet_forward_returns

FILLS_FIXTURE = Path("tests/fixtures/phase0b/normalized_fills_sample.csv")
SNAPSHOTS_FIXTURE = Path("tests/fixtures/phase0b/price_snapshots_sample.csv")


def _loaded_conn():
    conn = connect_duckdb()
    create_normalized_fills_table(conn)
    create_price_snapshots_table(conn)
    load_normalized_fills_csv(conn, FILLS_FIXTURE)
    load_price_snapshots_csv(conn, SNAPSHOTS_FIXTURE)
    return conn


def test_wallet_forward_returns_deterministic_rows_and_signs() -> None:
    conn = _loaded_conn()
    try:
        rows = wallet_forward_returns(conn, horizon_ms=300000)
        assert len(rows) == 2

        buy_row = next(row for row in rows if row["side"] == "BUY")
        sell_row = next(row for row in rows if row["side"] == "SELL")

        assert buy_row["token_id"] == "10001"
        assert buy_row["forward_return_bps"] > 0
        assert buy_row["forward_return_bps"] == 300.0000000000003

        assert sell_row["token_id"] == "10002"
        assert sell_row["forward_return_bps"] > 0
        assert sell_row["forward_return_bps"] == 499.9999999999999
    finally:
        conn.close()


def test_missing_future_price_is_retained_in_market_price_after_trades() -> None:
    conn = _loaded_conn()
    try:
        rows = market_price_after_trades(conn, horizon_ms=300000)
        assert len(rows) == 3
        missing = [row for row in rows if row["future_price"] is None]
        assert len(missing) == 1
        assert missing[0]["token_id"] == "20001"
    finally:
        conn.close()


def test_lead_lag_summary_counts_and_average() -> None:
    conn = _loaded_conn()
    try:
        summary = lead_lag_summary(conn, horizon_ms=300000)
        assert summary["fills_analyzed"] == 3
        assert summary["fills_with_future_price"] == 2
        assert summary["average_forward_return_bps"] == 400.0000000000001
    finally:
        conn.close()


def test_query_module_does_not_pull_runtime_rails() -> None:
    source = Path("meg/research/duckdb_lake/queries.py").read_text(encoding="utf-8")
    forbidden_tokens = ("redis", "postgres", "meg.execution", "meg.telegram", "sqlalchemy")
    for token in forbidden_tokens:
        assert token not in source.lower()
