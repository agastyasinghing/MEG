from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import duckdb
from scripts.prd_0b import run_view_smoke

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/prd/PRD-0B-IMPL-07_BRONZE_SILVER_SEMANTIC_HARDENING.md'
BRONZE = ROOT / 'sql/prd_0b/bronze_views.sql'
SILVER = ROOT / 'sql/prd_0b/silver_views.sql'

def _conn():
    con = duckdb.connect(':memory:')
    run_view_smoke.create_synthetic_source_relations(con, include_unresolved_cases=True)
    run_view_smoke.apply_view_sql(con, BRONZE.read_text(), SILVER.read_text())
    return con

def test_doc_exists_non_approvals():
    t = DOC.read_text().lower()
    assert 'synthetic-only' in t and 'no archive reads' in t and 'no parquet_scan' in t and 'no live trading' in t

def test_bronze_and_silver_semantic_columns():
    con = _conn()
    bcols = [r[1] for r in con.execute("PRAGMA table_info('bronze_kalshi_trades')").fetchall()]
    for c in ['source_dataset','source_platform','source_relative_path','bronze_view_version','raw_ingested_at','source_record_ref','bronze_unresolved_status','required_field_status']:
        assert c in bcols
    scols = [r[1] for r in con.execute("PRAGMA table_info('silver_kalshi_fills')").fetchall()]
    for c in ['silver_view_version','source_platform','normalized_entity_type','source_dataset','source_relative_path','source_record_ref','unresolved_status','dependency_status']:
        assert c in scols

def test_dependency_unresolved_cases_and_guards():
    con = _conn()
    assert con.execute("select count(*) from bronze_kalshi_trades where source_record_ref is null").fetchone()[0] == 0
    assert con.execute("select count(*) from bronze_kalshi_trades where bronze_unresolved_status <> 'none'").fetchone()[0] >= 1
    assert con.execute("select count(*) from silver_kalshi_fills where dependency_status='missing_dependency'").fetchone()[0] >= 1
    assert con.execute("select count(*) from silver_poly_clob_fills where market_dependency_status='missing_dependency'").fetchone()[0] >= 1
    assert con.execute("select count(*) from silver_poly_clob_fills where block_dependency_status='missing_dependency'").fetchone()[0] >= 1
    assert con.execute("select count(*) from silver_poly_legacy_fpmm_fills where dependency_status='missing_dependency'").fetchone()[0] >= 1

def test_smoke_summary_and_cli_json():
    summary = run_view_smoke.run_in_memory_view_smoke()
    assert 'unresolved_status_counts' in summary and 'dependency_status_counts' in summary and summary['ok'] is True
    out = subprocess.run([sys.executable, '-m', 'scripts.prd_0b.run_view_smoke', 'run', '--json'], cwd=ROOT, check=True, capture_output=True, text=True)
    p = json.loads(out.stdout)
    assert 'unresolved_status_counts' in p and 'dependency_status_counts' in p and p['ok'] is True

def test_forbidden_patterns_and_labels():
    all_sql = (BRONZE.read_text() + SILVER.read_text()).lower()
    assert 'parquet_scan' not in all_sql
    for bad in ['http://','https://','api.','requests.','urllib','websocket','opportunity','equivalence']:
        assert bad not in all_sql
