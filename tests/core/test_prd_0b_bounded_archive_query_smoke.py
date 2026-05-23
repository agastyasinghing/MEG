from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

from scripts.prd_0b import bounded_archive_query_smoke as smoke

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-10_BOUNDED_ARCHIVE_QUERY_SMOKE.md")


def _make_mini_archive(root: Path) -> None:
    import duckdb

    for rel in [
        "kalshi/markets",
        "kalshi/trades",
        "polymarket/markets",
        "polymarket/trades",
        "polymarket/blocks",
        "polymarket/legacy_trades",
    ]:
        d = root / rel
        d.mkdir(parents=True, exist_ok=True)
        con = duckdb.connect(":memory:")
        con.execute(f"COPY (SELECT 1 AS id, 'x' AS label) TO '{(d / 'a.parquet').as_posix()}' (FORMAT parquet)")
        con.close()
    (root / "polymarket").mkdir(parents=True, exist_ok=True)
    (root / "polymarket/fpmm_collateral_lookup.json").write_text('{"assets":[]}', encoding="utf-8")


def test_doc_exists_and_contains_non_approvals() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Purpose and posture" in text
    assert "no archive reads without explicit --archive-root" in text


def test_import_safety_no_runtime_actions() -> None:
    tree = ast.parse(Path("scripts/prd_0b/bounded_archive_query_smoke.py").read_text(encoding="utf-8"))
    for node in tree.body:
        assert not isinstance(node, ast.With)


def test_specs_exactly_seven() -> None:
    specs = smoke.get_approved_archive_family_specs()
    assert len(specs) == 7


def test_select_rep_ignores_appledouble(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    p = tmp_path / "kalshi/markets"
    (p / "._bad.parquet").write_bytes(b"x")
    sel = smoke.select_representative_files(tmp_path, smoke.get_approved_archive_family_specs())
    assert sel["representative_files"]["kalshi_markets"].endswith("a.parquet")


def test_path_traversal_symlink_candidate_is_rejected(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    outside = tmp_path.parent / "outside.parquet"
    outside.write_bytes(b"not parquet content")
    markets = tmp_path / "kalshi/markets"
    symlink_path = markets / "0_evil.parquet"
    symlink_path.symlink_to(outside)
    selection = smoke.select_representative_files(tmp_path, smoke.get_approved_archive_family_specs())
    assert "kalshi_markets" in selection["unsafe_families"]


def test_missing_archive_root_fails_closed() -> None:
    s = smoke.run_bounded_archive_query_smoke(Path("/definitely/not/here"))
    assert s["ok"] is False


def test_unknown_allowlist_fails_closed(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    s = smoke.run_bounded_archive_query_smoke(tmp_path, family_allowlist=["bad"])
    assert s["status"] == "unknown_family_allowlist"


def test_missing_family_paths_are_reported(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    (tmp_path / "kalshi/trades").rename(tmp_path / "kalshi/trades_missing")
    s = smoke.run_bounded_archive_query_smoke(tmp_path)
    assert s["ok"] is False
    assert s["status"] == "missing_required_families"
    assert "kalshi_trades" in s["missing_families"]
    assert set(["ok", "status", "missing_families", "query_results", "warnings"]).issubset(s)


def test_row_limit_policy_fails_closed(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    assert smoke.run_bounded_archive_query_smoke(tmp_path, row_limit=0)["status"] == "invalid_row_limit"
    assert smoke.run_bounded_archive_query_smoke(tmp_path, row_limit=1001)["status"] == "invalid_row_limit"


def test_success_summary_shape(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    s = smoke.run_bounded_archive_query_smoke(tmp_path)
    assert s["ok"] is True
    for k in ["ok", "status", "archive_root_status", "duckdb_status", "family_count", "checked_families", "skipped_families", "missing_families", "representative_files", "row_limit", "query_results", "elapsed_ms_by_query", "warnings", "wrote_outputs", "created_duckdb_file", "generated_artifacts"]:
        assert k in s
    for q in s["query_results"]:
        assert set(["family", "source_platform", "source_kind", "source_relative_path", "file_kind", "status", "row_count_observed", "column_count_observed", "elapsed_ms", "warning"]).issubset(q)
        assert not Path(q["source_relative_path"]).is_absolute()


def test_cli_json_and_non_json_modes(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    ok_json = subprocess.run(
        [sys.executable, "-m", "scripts.prd_0b.bounded_archive_query_smoke", "run", "--archive-root", str(tmp_path), "--json"],
        capture_output=True,
        text=True,
    )
    assert ok_json.returncode == 0
    assert ok_json.stdout.lstrip().startswith("{")
    data = json.loads(ok_json.stdout)
    assert data["ok"] is True

    ok_text = subprocess.run(
        [sys.executable, "-m", "scripts.prd_0b.bounded_archive_query_smoke", "run", "--archive-root", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert ok_text.returncode == 0
    assert not ok_text.stdout.lstrip().startswith("{")
    assert "status:" in ok_text.stdout


def test_cli_bad_root_exits_non_zero_and_json_when_requested(tmp_path: Path) -> None:
    _make_mini_archive(tmp_path)
    bad = subprocess.run(
        [sys.executable, "-m", "scripts.prd_0b.bounded_archive_query_smoke", "run", "--archive-root", str(tmp_path / "missing"), "--json"],
        capture_output=True,
        text=True,
    )
    assert bad.returncode != 0
    payload = json.loads(bad.stdout)
    assert payload["ok"] is False
    assert payload["status"] == "invalid_archive_root"


def test_no_production_runtime_imports() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert not node.module.startswith("meg")
