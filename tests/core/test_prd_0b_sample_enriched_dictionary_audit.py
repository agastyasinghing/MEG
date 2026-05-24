from __future__ import annotations

import ast
import importlib
import json
import subprocess
import sys
from pathlib import Path

from scripts.prd_0b.sample_enriched_dictionary_audit import (
    AUDIT_MODE,
    run_sample_enriched_dictionary_audit,
)
from tests.core.test_prd_0b_data_dictionary_sample_enrichment import _build_archive


REQUIRED_FIELDS = {
    "ok",
    "status",
    "audit_mode",
    "archive_root_status",
    "enrichment_status",
    "contract_validation_status",
    "enrichment_mode",
    "family_count",
    "enriched_family_count",
    "missing_family_count",
    "skipped_family_count",
    "row_limit",
    "sample_result_count",
    "sample_total_elapsed_ms",
    "sample_max_elapsed_ms",
    "sample_avg_elapsed_ms",
    "slowest_sample_family",
    "contract_errors",
    "readiness_flags",
    "warnings",
    "wrote_outputs",
    "created_duckdb_file",
    "generated_artifacts",
    "committed_fixtures",
    "production_readiness_claim",
    "production_latency_slo_claim",
    "final_trading_readiness_claim",
}


def test_doc_exists_and_has_required_sections_non_approvals() -> None:
    text = Path("docs/prd/PRD-0B-IMPL-15_SAMPLE_ENRICHED_DICTIONARY_LATENCY_READINESS_AUDIT.md").read_text(encoding="utf-8")
    required = [
        "Purpose and posture",
        "Relationship to PRD-0B-IMPL-13",
        "Relationship to PRD-0B-IMPL-14",
        "Audit mode",
        "Input contract",
        "Timing audit fields",
        "Contract validation audit",
        "Readiness flag semantics",
        "JSON summary shape",
        "CLI behavior",
        "Test posture using synthetic mini-archives",
        "Safety/no-output guarantees",
        "What counts as success",
        "What remains out of scope",
        "Relationship to PRD-0A",
        "no generated dictionary files",
        "no production readiness claim",
        "no final trading readiness claim",
    ]
    for value in required:
        assert value in text


def test_import_side_effect_safe() -> None:
    module = importlib.import_module("scripts.prd_0b.sample_enriched_dictionary_audit")
    assert hasattr(module, "run_sample_enriched_dictionary_audit")


def test_no_top_level_runtime_imports() -> None:
    tree = ast.parse(Path("scripts/prd_0b/sample_enriched_dictionary_audit.py").read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
    assert "duckdb" not in imports
    assert "scripts.prd_0b.data_dictionary_sample_enrichment" not in imports


def test_requires_explicit_archive_root() -> None:
    try:
        run_sample_enriched_dictionary_audit(None)  # type: ignore[arg-type]
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_success_audit_shape_and_flags(tmp_path: Path) -> None:
    _build_archive(tmp_path)
    summary = run_sample_enriched_dictionary_audit(tmp_path)
    assert summary["ok"] is True
    assert REQUIRED_FIELDS.issubset(summary.keys())
    assert summary["audit_mode"] == AUDIT_MODE
    assert summary["contract_validation_status"] == "pass"
    assert summary["sample_total_elapsed_ms"] is not None
    assert summary["sample_max_elapsed_ms"] is not None
    assert summary["sample_avg_elapsed_ms"] is not None
    assert summary["slowest_sample_family"]
    readiness = summary["readiness_flags"]
    assert isinstance(readiness, dict)
    assert readiness["local_sample_enrichment_contract_ready"] is True
    assert readiness["local_sample_enrichment_latency_observed"] is True
    assert readiness["production_readiness_approved"] is False
    assert readiness["production_latency_slo_approved"] is False
    assert readiness["final_trading_readiness_approved"] is False
    assert summary["production_readiness_claim"] is False
    assert summary["production_latency_slo_claim"] is False
    assert summary["final_trading_readiness_claim"] is False
    assert not list(tmp_path.rglob("*.duckdb"))
    assert not list(tmp_path.rglob("*dictionary*.json"))


def test_contract_validation_error_status(tmp_path: Path, monkeypatch) -> None:
    _build_archive(tmp_path)

    def _bad_validate(_: dict[str, object]) -> list[str]:
        return ["bad_contract"]

    monkeypatch.setattr(
        "scripts.prd_0b.data_dictionary_sample_enrichment.validate_sample_enrichment_summary",
        _bad_validate,
    )
    summary = run_sample_enriched_dictionary_audit(tmp_path)
    assert summary["status"] == "contract_validation_failed"
    assert summary["ok"] is False


def test_enrichment_not_ok_status(tmp_path: Path, monkeypatch) -> None:
    _build_archive(tmp_path)

    def _bad_enrich(*args, **kwargs):
        return {
            "ok": False,
            "status": "missing_required_families",
            "archive_root_status": "ok",
            "enrichment_mode": "bounded_sample_metadata_only",
            "family_count": 0,
            "enriched_families": [],
            "missing_families": [],
            "skipped_families": [],
            "warnings": [],
            "wrote_outputs": False,
            "created_duckdb_file": False,
            "generated_artifacts": [],
            "committed_fixtures": False,
            "sample_enrichment_results": [],
        }

    monkeypatch.setattr("scripts.prd_0b.data_dictionary_sample_enrichment.enrich_data_dictionary_with_samples", _bad_enrich)
    monkeypatch.setattr("scripts.prd_0b.data_dictionary_sample_enrichment.validate_sample_enrichment_summary", lambda _summary: [])
    summary = run_sample_enriched_dictionary_audit(tmp_path)
    assert summary["status"] == "enrichment_not_ok"
    assert summary["ok"] is False


def test_sample_timing_missing_status(tmp_path: Path, monkeypatch) -> None:
    _build_archive(tmp_path)

    def _bad_enrich(*args, **kwargs):
        return {
            "ok": True,
            "status": "ok",
            "archive_root_status": "ok",
            "enrichment_mode": "bounded_sample_metadata_only",
            "family_count": 1,
            "enriched_families": ["x"],
            "missing_families": [],
            "skipped_families": [],
            "warnings": [],
            "wrote_outputs": False,
            "created_duckdb_file": False,
            "generated_artifacts": [],
            "committed_fixtures": False,
            "sample_enrichment_results": [{"family": "x"}],
        }

    monkeypatch.setattr("scripts.prd_0b.data_dictionary_sample_enrichment.enrich_data_dictionary_with_samples", _bad_enrich)
    monkeypatch.setattr("scripts.prd_0b.data_dictionary_sample_enrichment.validate_sample_enrichment_summary", lambda _summary: [])
    summary = run_sample_enriched_dictionary_audit(tmp_path)
    assert summary["status"] == "sample_timing_missing"
    assert summary["ok"] is False


def test_cli_json_success(tmp_path: Path) -> None:
    _build_archive(tmp_path)
    proc = subprocess.run(
        [sys.executable, "-m", "scripts.prd_0b.sample_enriched_dictionary_audit", "run", "--archive-root", str(tmp_path), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True


def test_cli_human_readable(tmp_path: Path) -> None:
    _build_archive(tmp_path)
    proc = subprocess.run(
        [sys.executable, "-m", "scripts.prd_0b.sample_enriched_dictionary_audit", "run", "--archive-root", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "audit_mode:" in proc.stdout
    assert "status:" in proc.stdout


def test_cli_bad_root_json_nonzero() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "scripts.prd_0b.sample_enriched_dictionary_audit", "run", "--archive-root", "/nope", "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0
    payload = json.loads(proc.stdout)
    assert payload["ok"] is False


def test_test_module_has_no_production_runtime_imports() -> None:
    tree = ast.parse(Path("tests/core/test_prd_0b_sample_enriched_dictionary_audit.py").read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    assert "meg" not in imported
