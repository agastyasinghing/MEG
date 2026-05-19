from __future__ import annotations

import json
from pathlib import Path

from meg.research.duckdb_lake.cli import (
    DEFAULT_FILLS_CSV,
    DEFAULT_SNAPSHOTS_CSV,
    build_fixture_report_cli,
)


def test_fixture_report_cli_writes_valid_json_and_returns_zero(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "fixture_report.json"

    code = build_fixture_report_cli(["--output", str(output_path)])

    assert code == 0
    assert output_path.exists()
    parsed = json.loads(output_path.read_text(encoding="utf-8"))
    assert parsed["generated_from"] == "fixture"
    assert parsed["report_name"] == "fixture_lead_lag_report"
    assert parsed["horizon_ms"] == 300000
    assert set(parsed.keys()) == {
        "report_name",
        "generated_from",
        "horizon_ms",
        "fills_analyzed",
        "fills_with_future_price",
        "average_forward_return_bps",
        "rows",
    }

    captured = capsys.readouterr()
    assert "written to" in captured.out


def test_fixture_report_cli_accepts_explicit_fixture_paths_and_horizon(tmp_path: Path) -> None:
    output_path = tmp_path / "fixture_report_explicit.json"

    code = build_fixture_report_cli(
        [
            "--fills-csv",
            str(DEFAULT_FILLS_CSV),
            "--snapshots-csv",
            str(DEFAULT_SNAPSHOTS_CSV),
            "--horizon-ms",
            "600000",
            "--output",
            str(output_path),
        ]
    )

    assert code == 0
    parsed = json.loads(output_path.read_text(encoding="utf-8"))
    assert parsed["horizon_ms"] == 600000


def test_cli_module_does_not_pull_runtime_rails() -> None:
    source = Path("meg/research/duckdb_lake/cli.py").read_text(encoding="utf-8")
    forbidden_tokens = ("redis", "postgres", "meg.execution", "meg.telegram", "sqlalchemy")
    for token in forbidden_tokens:
        assert token not in source.lower()
