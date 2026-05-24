from __future__ import annotations

import ast
import importlib
import json
import subprocess
import sys
from pathlib import Path

from scripts.prd_0b.data_dictionary_sample_enrichment import (
    APPROVED_SAMPLE_KEYS,
    enrich_data_dictionary_with_samples,
    get_sample_enrichment_mode,
)


REQUIRED_SUMMARY_KEYS = {
    "ok",
    "status",
    "archive_root_status",
    "duckdb_status",
    "enrichment_mode",
    "family_count",
    "enriched_families",
    "skipped_families",
    "missing_families",
    "representative_files",
    "row_limit",
    "sample_enrichment_results",
    "warnings",
    "wrote_outputs",
    "created_duckdb_file",
    "generated_artifacts",
    "committed_fixtures",
    "production_readiness_claim",
    "final_trading_readiness_claim",
}


def _build_archive(root: Path) -> None:
    import duckdb
    from scripts.prd_0b.bounded_archive_query_smoke import get_approved_archive_family_specs

    for spec in get_approved_archive_family_specs():
        rel = Path(str(spec["relative_path"]))
        full = root / rel
        if str(spec["file_kind"]) == "json":
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text('{"shape":"sidecar"}', encoding="utf-8")
        else:
            full.mkdir(parents=True, exist_ok=True)
            target = full / "part-000.parquet"
            con = duckdb.connect(":memory:")
            escaped_target = str(target).replace("'", "''")
            con.execute(f"COPY (SELECT 1 AS condition_ref, 'yes' AS outcome) TO '{escaped_target}' (FORMAT PARQUET)")
            con.close()


def test_doc_exists() -> None:
    doc = Path("docs/prd/PRD-0B-IMPL-13_DATA_DICTIONARY_SAMPLE_ENRICHMENT.md")
    text = doc.read_text(encoding="utf-8")
    assert "Purpose and posture" in text
    assert "Explicit non-approvals" in text


def test_import_safe() -> None:
    module = importlib.import_module("scripts.prd_0b.data_dictionary_sample_enrichment")
    assert hasattr(module, "enrich_data_dictionary_with_samples")


def test_no_top_level_duckdb_or_impl10_helper_imports() -> None:
    script_path = Path("scripts/prd_0b/data_dictionary_sample_enrichment.py")
    tree = ast.parse(script_path.read_text(encoding="utf-8"))
    top_level_import_targets: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                top_level_import_targets.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            imported_names = [alias.name for alias in node.names]
            top_level_import_targets.add(module_name)
            for imported_name in imported_names:
                top_level_import_targets.add(f"{module_name}.{imported_name}")
    assert "duckdb" not in top_level_import_targets
    assert "scripts.prd_0b.bounded_archive_query_smoke" not in top_level_import_targets
    assert "scripts.prd_0b.bounded_archive_query_smoke.get_approved_archive_family_specs" not in top_level_import_targets
    assert "scripts.prd_0b.bounded_archive_query_smoke.select_representative_files" not in top_level_import_targets


def test_mode() -> None:
    assert get_sample_enrichment_mode() == "bounded_sample_metadata_only"


def test_missing_archive_root_fails_closed() -> None:
    summary = enrich_data_dictionary_with_samples(None)  # type: ignore[arg-type]
    assert summary["ok"] is False


def test_invalid_row_limits_fail(tmp_path: Path) -> None:
    _build_archive(tmp_path)
    assert enrich_data_dictionary_with_samples(tmp_path, row_limit=0)["status"] == "invalid_row_limit"
    assert enrich_data_dictionary_with_samples(tmp_path, row_limit=1001)["status"] == "invalid_row_limit"


def test_unknown_family_fails(tmp_path: Path) -> None:
    _build_archive(tmp_path)
    out = enrich_data_dictionary_with_samples(tmp_path, family_allowlist=["unknown"])
    assert out["status"] == "unknown_family_allowlist"


def test_success_summary(tmp_path: Path) -> None:
    _build_archive(tmp_path)
    summary = enrich_data_dictionary_with_samples(tmp_path)
    assert summary["ok"] is True
    assert REQUIRED_SUMMARY_KEYS.issubset(summary.keys())
    for row in summary["sample_enrichment_results"]:
        assert set(row.keys()) == APPROVED_SAMPLE_KEYS
        assert not Path(row["source_relative_path"]).is_absolute()
        assert row["sample_generated_from_archive_root"] is True
        assert row["sample_persistent_output_written"] is False
    assert summary["wrote_outputs"] is False
    assert summary["created_duckdb_file"] is False
    assert summary["generated_artifacts"] == []
    assert summary["committed_fixtures"] is False
    assert "condition_ref" in json.dumps(summary)
    assert "yes" not in json.dumps(summary)


def test_missing_family_fails(tmp_path: Path) -> None:
    _build_archive(tmp_path)
    (tmp_path / "kalshi" / "markets").rename(tmp_path / "kalshi" / "markets_missing")
    summary = enrich_data_dictionary_with_samples(tmp_path)
    assert summary["ok"] is False
    assert summary["status"] == "missing_required_families"


def test_cli_json(tmp_path: Path) -> None:
    _build_archive(tmp_path)
    proc = subprocess.run(
        [sys.executable, "-m", "scripts.prd_0b.data_dictionary_sample_enrichment", "run", "--archive-root", str(tmp_path), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True


def test_cli_bad_root_json() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "scripts.prd_0b.data_dictionary_sample_enrichment", "run", "--archive-root", "/nope", "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
    assert json.loads(proc.stdout)["ok"] is False
