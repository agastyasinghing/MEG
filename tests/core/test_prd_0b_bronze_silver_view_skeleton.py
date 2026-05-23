from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import duckdb

from scripts.prd_0b import run_view_smoke

ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs/prd/PRD-0B-IMPL-06_BRONZE_SILVER_DUCKDB_VIEW_SKELETON.md"
BRONZE_SQL_PATH = ROOT / "sql/prd_0b/bronze_views.sql"
SILVER_SQL_PATH = ROOT / "sql/prd_0b/silver_views.sql"


def test_doc_exists_and_posture_markers() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "skeleton" in text.lower()
    assert "no archive reads" in text.lower()
    assert "no parquet_scan" in text.lower()


def test_sql_files_exist() -> None:
    assert BRONZE_SQL_PATH.exists()
    assert SILVER_SQL_PATH.exists()


def test_import_has_no_side_effects() -> None:
    assert "duckdb.connect(" not in run_view_smoke.__dict__


def test_expected_view_lists() -> None:
    bronze = run_view_smoke.get_expected_bronze_views()
    silver = run_view_smoke.get_expected_silver_views()
    assert len(bronze) == 7
    assert bronze == [
        "bronze_kalshi_markets",
        "bronze_kalshi_trades",
        "bronze_poly_markets",
        "bronze_poly_clob_trades",
        "bronze_poly_blocks",
        "bronze_poly_legacy_fpmm_trades",
        "bronze_poly_fpmm_collateral_lookup",
    ]
    assert {
        "silver_kalshi_events",
        "silver_kalshi_markets",
        "silver_kalshi_outcomes",
        "silver_kalshi_market_snapshots",
        "silver_kalshi_fills",
        "silver_kalshi_results",
        "silver_poly_markets",
        "silver_poly_outcomes",
        "silver_poly_clob_tokens",
        "silver_poly_clob_fills",
        "silver_poly_blocks",
        "silver_poly_legacy_fpmm_fills",
        "silver_poly_collateral_assets",
    }.issubset(set(silver))


def test_sql_content_guards() -> None:
    bronze_sql = BRONZE_SQL_PATH.read_text(encoding="utf-8").lower()
    silver_sql = SILVER_SQL_PATH.read_text(encoding="utf-8").lower()
    for name in run_view_smoke.get_expected_bronze_views():
        assert name in bronze_sql
    for name in run_view_smoke.get_expected_silver_views():
        assert name in silver_sql
    assert "parquet_scan" not in bronze_sql + silver_sql
    for forbidden in ["http://", "https://", "requests.", "urllib", "websocket", "api."]:
        assert forbidden not in bronze_sql + silver_sql


def test_dependency_order_requires_bronze_before_silver() -> None:
    con = duckdb.connect(database=":memory:")
    silver_sql = run_view_smoke.load_sql_file(SILVER_SQL_PATH)
    try:
        con.execute(silver_sql)
    except duckdb.Error:
        pass
    else:
        raise AssertionError("Silver SQL unexpectedly succeeded without Bronze views")


def test_in_memory_smoke_and_view_queries(tmp_path: Path) -> None:
    before = {p for p in ROOT.rglob("*.duckdb")}
    summary = run_view_smoke.run_in_memory_view_smoke()
    assert summary["ok"] is True
    assert summary["wrote_outputs"] is False
    assert summary["created_duckdb_file"] is False

    con = duckdb.connect(database=":memory:")
    run_view_smoke.create_synthetic_source_relations(con)
    run_view_smoke.apply_view_sql(
        con,
        run_view_smoke.load_sql_file(BRONZE_SQL_PATH),
        run_view_smoke.load_sql_file(SILVER_SQL_PATH),
    )
    view_names = set(run_view_smoke.list_duckdb_views(con))
    assert set(run_view_smoke.get_expected_bronze_views()).issubset(view_names)
    assert set(run_view_smoke.get_expected_silver_views()).issubset(view_names)

    for name in run_view_smoke.get_expected_bronze_views():
        assert con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0] >= 1
    for name in run_view_smoke.get_expected_silver_views():
        con.execute(f"SELECT * FROM {name} LIMIT 1").fetchall()

    after = {p for p in ROOT.rglob("*.duckdb")}
    assert after == before


def test_cli_json_run() -> None:
    cmd = [sys.executable, "-m", "scripts.prd_0b.run_view_smoke", "run", "--json"]
    out = subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
    payload = json.loads(out.stdout.strip())
    assert payload["ok"] is True

