from __future__ import annotations

import ast
import importlib
import json
import subprocess
import sys
from pathlib import Path

from scripts.prd_0b import bounded_archive_latency_comparison as impl

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-11_BOUNDED_ARCHIVE_LATENCY_COMPARISON.md")


def _make_mini_archive(root: Path) -> None:
    import duckdb

    for rel in ["kalshi/markets", "kalshi/trades", "polymarket/markets", "polymarket/trades", "polymarket/blocks", "polymarket/legacy_trades"]:
        d = root / rel
        d.mkdir(parents=True, exist_ok=True)
        con = duckdb.connect(":memory:")
        con.execute(f"COPY (SELECT 1 AS id, 'x' AS label) TO '{(d / 'a.parquet').as_posix()}' (FORMAT parquet)")
        con.close()
    (root / "polymarket").mkdir(parents=True, exist_ok=True)
    (root / "polymarket/fpmm_collateral_lookup.json").write_text('{"assets":[]}', encoding="utf-8")


def test_doc_exists_and_contains_required_sections() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Purpose and posture" in text
    assert "Relationship to PRD-0B-IMPL-08" in text
    assert "Relationship to PRD-0B-IMPL-10" in text
    assert "no production latency SLO claim" in text


def test_module_import_side_effect_safe() -> None:
    module = importlib.import_module("scripts.prd_0b.bounded_archive_latency_comparison")
    assert hasattr(module, "run_bounded_archive_latency_comparison")


def test_comparison_requires_explicit_archive_root() -> None:
    s = impl.run_bounded_archive_latency_comparison(archive_root=None)  # type: ignore[arg-type]
    assert s["ok"] is False
    assert s["status"] == "missing_archive_root"


def test_success_shape_and_flags(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    s = impl.run_bounded_archive_latency_comparison(tmp_path)
    assert s["ok"] is True
    required = {"ok", "status", "source_posture", "archive_root_status", "synthetic_status", "archive_status", "synthetic_query_count", "archive_query_count", "synthetic_total_elapsed_ms", "archive_total_elapsed_ms", "synthetic_max_elapsed_ms", "archive_max_elapsed_ms", "comparison_ratio_archive_to_synthetic", "comparison_interpretation", "row_limit", "checked_families", "missing_families", "warnings", "wrote_outputs", "created_duckdb_file", "generated_artifacts", "production_slo_claim", "final_trading_readiness_claim"}
    assert required.issubset(s)
    assert s["production_slo_claim"] is False
    assert s["final_trading_readiness_claim"] is False


def test_archive_missing_root_and_cli_json_nonzero(tmp_path: Path) -> None:
    s = impl.run_bounded_archive_latency_comparison(tmp_path / "missing")
    assert s["ok"] is False

    p = subprocess.run([sys.executable, "-m", "scripts.prd_0b.bounded_archive_latency_comparison", "run", "--archive-root", str(tmp_path / "missing"), "--json"], capture_output=True, text=True)
    assert p.returncode != 0
    payload = json.loads(p.stdout)
    assert payload["ok"] is False


def test_missing_family_propagates_archive_not_ok(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    (tmp_path / "kalshi/trades").rename(tmp_path / "kalshi/trades_missing")
    s = impl.run_bounded_archive_latency_comparison(tmp_path)
    assert s["status"] == "archive_smoke_not_ok"


def test_synthetic_failure_and_zero_timing(monkeypatch, tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)

    def bad_gate(*args, **kwargs):
        return {"status": "query_failures", "ok": False, "warnings": [], "query_results": []}

    monkeypatch.setattr("scripts.prd_0b.query_latency_gate.run_latency_gate", bad_gate)
    s1 = impl.run_bounded_archive_latency_comparison(tmp_path)
    assert s1["status"] == "synthetic_gate_not_ok"

    def zero_gate(*args, **kwargs):
        return {"status": "ok", "ok": True, "warnings": [], "query_results": [{"elapsed_ms": 0.0}]}

    monkeypatch.setattr("scripts.prd_0b.query_latency_gate.run_latency_gate", zero_gate)
    s2 = impl.run_bounded_archive_latency_comparison(tmp_path)
    assert s2["status"] == "insufficient_synthetic_timing"


def test_cli_json_and_human_readable(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    ok_json = subprocess.run([sys.executable, "-m", "scripts.prd_0b.bounded_archive_latency_comparison", "run", "--archive-root", str(tmp_path), "--json"], capture_output=True, text=True)
    assert ok_json.returncode == 0
    payload = json.loads(ok_json.stdout)
    assert payload["ok"] is True

    ok_text = subprocess.run([sys.executable, "-m", "scripts.prd_0b.bounded_archive_latency_comparison", "run", "--archive-root", str(tmp_path)], capture_output=True, text=True)
    assert ok_text.returncode == 0
    assert "status:" in ok_text.stdout


def test_no_duckdb_or_generated_outputs_created() -> None:
    assert not any(Path(".").glob("*.duckdb"))


def test_no_production_runtime_imports_and_no_legacy_identifier_literal() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert not node.module.startswith("meg")
    assert "market" + "_id" not in Path("scripts/prd_0b/bounded_archive_latency_comparison.py").read_text(encoding="utf-8")
