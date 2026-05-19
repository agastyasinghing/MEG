from __future__ import annotations

from pathlib import Path
import duckdb

NORMALIZED_FILLS_COLUMNS: tuple[str, ...] = (
    "condition_id",
    "token_id",
    "outcome",
    "market_slug",
    "source_market_ref",
    "wallet_address",
    "timestamp_ms",
    "price",
    "size_usdc",
    "side",
    "source",
)


def connect_duckdb(path: str | Path = ":memory:") -> duckdb.DuckDBPyConnection:
    db_path = str(path) if isinstance(path, Path) else path
    return duckdb.connect(database=db_path)


def create_normalized_fills_table(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS normalized_fills (
            condition_id TEXT NOT NULL,
            token_id TEXT NOT NULL,
            outcome TEXT NOT NULL,
            market_slug TEXT,
            source_market_ref TEXT,
            wallet_address TEXT,
            timestamp_ms BIGINT NOT NULL,
            price DOUBLE NOT NULL,
            size_usdc DOUBLE,
            side TEXT NOT NULL,
            source TEXT NOT NULL
        )
        """
    )


def load_normalized_fills_csv(conn: duckdb.DuckDBPyConnection, csv_path: str | Path) -> int:
    csv_path = Path(csv_path)
    conn.execute(
        """
        INSERT INTO normalized_fills
        SELECT condition_id, token_id, outcome, market_slug, source_market_ref, wallet_address,
               timestamp_ms, price, size_usdc, side, source
        FROM read_csv_auto(?, header=true)
        """,
        [str(csv_path)],
    )
    return normalized_fills_row_count(conn)


def normalized_fills_row_count(conn: duckdb.DuckDBPyConnection) -> int:
    return conn.execute("SELECT COUNT(*) FROM normalized_fills").fetchone()[0]


def normalized_fills_schema_fingerprint(conn: duckdb.DuckDBPyConnection) -> tuple[tuple[str, str], ...]:
    rows = conn.execute("DESCRIBE normalized_fills").fetchall()
    return tuple((name, dtype) for name, dtype, *_ in rows)


def validate_normalized_fills_ingest(conn: duckdb.DuckDBPyConnection, expected_rows: int) -> dict[str, object]:
    actual_rows = normalized_fills_row_count(conn)
    ts_min, ts_max = conn.execute("SELECT MIN(timestamp_ms), MAX(timestamp_ms) FROM normalized_fills").fetchone()
    duplicate_rows = conn.execute(
        """
        SELECT COUNT(*) FROM (
            SELECT condition_id, token_id, outcome, wallet_address, timestamp_ms, side, source, COUNT(*) AS c
            FROM normalized_fills
            GROUP BY 1,2,3,4,5,6,7
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()[0]
    null_source_rows = conn.execute("SELECT COUNT(*) FROM normalized_fills WHERE source IS NULL OR source = ''").fetchone()[0]
    return {
        "row_count_matches": actual_rows == expected_rows,
        "actual_rows": actual_rows,
        "expected_rows": expected_rows,
        "timestamp_min_ms": ts_min,
        "timestamp_max_ms": ts_max,
        "duplicate_key_rows": duplicate_rows,
        "source_non_null": null_source_rows == 0,
    }
