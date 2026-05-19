from __future__ import annotations

import json
from pathlib import Path

import pytest

from meg.research.duckdb_lake.loader import (
    connect_duckdb,
    create_normalized_fills_table,
    create_price_snapshots_table,
    load_normalized_fills_csv,
    load_price_snapshots_csv,
)
from meg.research.duckdb_lake.reports import build_fixture_lead_lag_report, write_report_json

FILLS_FIXTURE = Path("tests/fixtures/phase0b/normalized_fills_sample.csv")
SNAPSHOTS_FIXTURE = Path("tests/fixtures/phase0b/price_snapshots_sample.csv")


def _loaded_conn():
    conn = connect_duckdb()
    create_normalized_fills_table(conn)
    create_price_snapshots_table(conn)
    load_normalized_fills_csv(conn, FILLS_FIXTURE)
    load_price_snapshots_csv(conn, SNAPSHOTS_FIXTURE)
    return conn


def test_build_fixture_lead_lag_report_deterministic_summary_and_rows() -> None:
    conn = _loaded_conn()
    try:
        report = build_fixture_lead_lag_report(conn, horizon_ms=300000)
    finally:
        conn.close()

    assert set(report.keys()) == {
        "report_name",
        "horizon_ms",
        "fills_analyzed",
        "fills_with_future_price",
        "average_forward_return_bps",
        "rows",
        "generated_from",
    }
    assert report["report_name"] == "fixture_lead_lag_report"
    assert report["generated_from"] == "fixture"
    assert report["horizon_ms"] == 300000
    assert report["fills_analyzed"] == 3
    assert report["fills_with_future_price"] == 2
    assert report["average_forward_return_bps"] == pytest.approx(350.0)

    rows = report["rows"]
    assert isinstance(rows, list)
    assert len(rows) == 3
    values = [row["forward_return_bps"] for row in rows]
    assert values[0] == pytest.approx(300.0)
    assert values[1] == pytest.approx(400.0)
    assert values[2] is None


def test_write_report_json_writes_valid_json_to_tmp_path(tmp_path: Path) -> None:
    conn = _loaded_conn()
    try:
        report = build_fixture_lead_lag_report(conn, horizon_ms=300000)
    finally:
        conn.close()

    output_path = tmp_path / "fixture_report.json"
    write_report_json(report, output_path)

    assert output_path.exists()
    parsed = json.loads(output_path.read_text(encoding="utf-8"))
    assert parsed["generated_from"] == "fixture"
    assert parsed["rows"][0]["forward_return_bps"] == pytest.approx(300.0)


def test_report_module_does_not_pull_runtime_rails() -> None:
    source = Path("meg/research/duckdb_lake/reports.py").read_text(encoding="utf-8")
    forbidden_tokens = ("redis", "postgres", "meg.execution", "meg.telegram", "sqlalchemy")
    for token in forbidden_tokens:
        assert token not in source.lower()
