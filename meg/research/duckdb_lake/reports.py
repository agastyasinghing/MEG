from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import duckdb

from .queries import lead_lag_summary, market_price_after_trades


def build_fixture_lead_lag_report(conn: duckdb.DuckDBPyConnection, horizon_ms: int) -> dict[str, object]:
    summary = lead_lag_summary(conn, horizon_ms=horizon_ms)
    rows = market_price_after_trades(conn, horizon_ms=horizon_ms)

    report_rows: list[dict[str, Any]] = []
    for row in rows:
        report_rows.append(
            {
                "condition_id": row["condition_id"],
                "token_id": row["token_id"],
                "outcome": row["outcome"],
                "wallet_address": row["wallet_address"],
                "timestamp_ms": row["timestamp_ms"],
                "side": row["side"],
                "fill_price": row["fill_price"],
                "future_timestamp_ms": row["future_timestamp_ms"],
                "future_price": row["future_price"],
                "forward_return_bps": row["forward_return_bps"],
            }
        )

    return {
        "report_name": "fixture_lead_lag_report",
        "generated_from": "fixture",
        "horizon_ms": horizon_ms,
        "fills_analyzed": summary["fills_analyzed"],
        "fills_with_future_price": summary["fills_with_future_price"],
        "average_forward_return_bps": summary["average_forward_return_bps"],
        "rows": report_rows,
    }


def write_report_json(report: dict[str, object], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, sort_keys=True, indent=2), encoding="utf-8")
