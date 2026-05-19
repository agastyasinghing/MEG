from __future__ import annotations

from typing import Any

import duckdb


def market_price_after_trades(conn: duckdb.DuckDBPyConnection, horizon_ms: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        WITH fills AS (
            SELECT
                condition_id,
                token_id,
                outcome,
                wallet_address,
                timestamp_ms,
                price AS fill_price,
                side,
                source
            FROM normalized_fills
        )
        SELECT
            f.condition_id,
            f.token_id,
            f.outcome,
            f.wallet_address,
            f.timestamp_ms,
            f.fill_price,
            f.side,
            f.source,
            ps.timestamp_ms AS future_timestamp_ms,
            ps.price AS future_price,
            CASE
                WHEN ps.price IS NULL THEN NULL
                WHEN f.side = 'BUY' THEN (ps.price - f.fill_price) * 10000
                WHEN f.side = 'SELL' THEN (f.fill_price - ps.price) * 10000
                ELSE NULL
            END AS forward_return_bps
        FROM fills f
        LEFT JOIN LATERAL (
            SELECT p.timestamp_ms, p.price
            FROM price_snapshots p
            WHERE p.condition_id = f.condition_id
              AND p.token_id = f.token_id
              AND p.outcome = f.outcome
              AND p.timestamp_ms >= (f.timestamp_ms + ?)
            ORDER BY p.timestamp_ms ASC
            LIMIT 1
        ) ps ON TRUE
        ORDER BY f.timestamp_ms ASC, f.token_id ASC
        """,
        [horizon_ms],
    ).fetchall()

    out: list[dict[str, Any]] = []
    for row in rows:
        out.append(
            {
                "condition_id": row[0],
                "token_id": row[1],
                "outcome": row[2],
                "wallet_address": row[3],
                "timestamp_ms": row[4],
                "fill_price": row[5],
                "side": row[6],
                "source": row[7],
                "future_timestamp_ms": row[8],
                "future_price": row[9],
                "forward_return_bps": row[10],
            }
        )
    return out


def wallet_forward_returns(conn: duckdb.DuckDBPyConnection, horizon_ms: int) -> list[dict[str, Any]]:
    rows = market_price_after_trades(conn, horizon_ms)
    return [row for row in rows if row["future_price"] is not None]


def lead_lag_summary(conn: duckdb.DuckDBPyConnection, horizon_ms: int) -> dict[str, Any]:
    rows = market_price_after_trades(conn, horizon_ms)
    with_future = [row for row in rows if row["forward_return_bps"] is not None]
    avg_bps = sum(float(row["forward_return_bps"]) for row in with_future) / len(with_future) if with_future else None
    return {
        "fills_analyzed": len(rows),
        "fills_with_future_price": len(with_future),
        "average_forward_return_bps": avg_bps,
    }
