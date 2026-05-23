from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-08_QUERY_LATENCY_GATE_SKELETON.md")
APPROVED_QUERY_NAMES = {
    "silver_view_inventory",
    "unresolved_status_counts",
    "dependency_status_counts",
    "kalshi_fill_dependency_scan",
    "poly_clob_dependency_scan",
    "legacy_fpmm_dependency_scan",
    "bronze_row_count_scan",
}
REQUIRED_FIELDS = {
    "name",
    "description",
    "sql",
    "expected_min_rows",
    "budget_ms",
    "source_posture",
}


def test_doc_exists_and_includes_purpose_and_non_approvals() -> None:
    assert DOC_PATH.exists()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Purpose and posture" in text
    assert "Safety/no-output guarantees" in text

    required_non_approvals = [
        "no archive reads",
        "no parquet_scan",
        "no full data import",
        "no generated SQL outputs",
        "no generated reports",
        "no generated dictionary files",
        "no .duckdb files",
        "no fixture derivation",
        "no fixture commit",
        "no production loaders",
        "no query engine service",
        "no connectors/API calls",
        "no order placement",
        "no live trading",
        "no autonomous execution",
        "no weather implementation",
        "no production latency SLO claim",
        "no final trading readiness claim",
    ]
    for line in required_non_approvals:
        assert line in text


def test_module_import_is_side_effect_safe() -> None:
    module = importlib.import_module("scripts.prd_0b.query_latency_gate")
    assert module.SOURCE_POSTURE == "synthetic_in_memory_only"


def test_get_latency_query_specs_returns_exact_approved_names() -> None:
    from scripts.prd_0b.query_latency_gate import get_latency_query_specs

    specs = get_latency_query_specs()
    assert {spec["name"] for spec in specs} == APPROVED_QUERY_NAMES


def test_query_specs_have_required_fields() -> None:
    from scripts.prd_0b.query_latency_gate import get_latency_query_specs

    specs = get_latency_query_specs()
    for spec in specs:
        assert REQUIRED_FIELDS.issubset(set(spec))


@pytest.mark.parametrize(
    ("patch", "error_substr"),
    [
        ({"name": "unresolved_status_counts"}, "Duplicate query name"),
        ({"sql": 123}, "SQL must be a string"),
        ({"sql": "SELECT * FROM parquet_scan('x')"}, "Forbidden SQL pattern"),
        ({"sql": "SELECT * FROM q WHERE endpoint='https://example.invalid'"}, "Forbidden SQL pattern"),
        ({"sql": "SELECT * FROM q WHERE source='archive/data'"}, "Forbidden SQL pattern"),
        ({"sql": "CREATE TABLE x AS SELECT 1"}, "Forbidden SQL pattern"),
        ({"budget_ms": 0}, "budget_ms must be positive"),
        ({"expected_min_rows": -1}, "expected_min_rows must be a non-negative integer"),
        ({"source_posture": "archive_backed"}, "source_posture must be synthetic_in_memory_only"),
    ],
)
def test_validate_latency_query_specs_rejects_invalid_specs(
    patch: dict[str, object],
    error_substr: str,
) -> None:
    from scripts.prd_0b.query_latency_gate import (
        get_latency_query_specs,
        validate_latency_query_specs,
    )

    specs = get_latency_query_specs()
    modified = dict(specs[0])
    modified.update(patch)
    specs[0] = modified
    with pytest.raises(ValueError, match=error_substr):
        validate_latency_query_specs(specs)


def test_validate_latency_query_specs_rejects_missing_required_fields() -> None:
    from scripts.prd_0b.query_latency_gate import validate_latency_query_specs

    with pytest.raises(ValueError, match="Missing required fields"):
        validate_latency_query_specs([
            {
                "name": "x",
                "description": "x",
                "sql": "SELECT 1",
                "expected_min_rows": 0,
                "budget_ms": 1,
            }
        ])


def test_run_latency_gate_summary_shape_and_defaults() -> None:
    from scripts.prd_0b.query_latency_gate import run_latency_gate

    summary = run_latency_gate()
    assert summary["source_posture"] == "synthetic_in_memory_only"
    assert summary["budgets_are_synthetic_only"] is True
    assert summary["wrote_outputs"] is False
    assert summary["created_duckdb_file"] is False
    assert summary["query_count"] == len(APPROVED_QUERY_NAMES)
    assert summary["passed_query_count"] == len(APPROVED_QUERY_NAMES)
    assert summary["failed_query_count"] == 0
    assert summary["ok"] is True
    assert summary["status"] == "ok"
    assert len(summary["query_results"]) == len(APPROVED_QUERY_NAMES)


def test_cli_run_json_and_without_unresolved_cases() -> None:
    cmd_base = [sys.executable, "-m", "scripts.prd_0b.query_latency_gate", "run", "--json"]
    result_default = subprocess.run(cmd_base, check=False, capture_output=True, text=True)
    assert result_default.returncode == 0
    payload = json.loads(result_default.stdout)
    assert payload["ok"] is True

    result_no_unresolved = subprocess.run(
        [*cmd_base, "--without-unresolved-cases"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result_no_unresolved.returncode == 0
    payload_no_unresolved = json.loads(result_no_unresolved.stdout)
    assert payload_no_unresolved["ok"] is True


def test_no_duckdb_or_generated_output_files_created() -> None:
    assert not any(Path(".").glob("*.duckdb"))
    assert not any(Path(".").glob("**/*dictionary*.json"))


def test_test_module_has_no_production_runtime_imports() -> None:
    import ast

    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(not name.name.startswith("meg") for name in node.names)
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert not node.module.startswith("meg")


def test_implementation_file_forbidden_runtime_patterns_are_absent() -> None:
    from scripts.prd_0b.query_latency_gate import get_latency_query_specs

    impl_text = Path("scripts/prd_0b/query_latency_gate.py").read_text(encoding="utf-8")
    forbidden_runtime_terms = ["http://", "https://", "requests.", "urllib", "websocket"]
    for term in forbidden_runtime_terms:
        assert term not in "\n".join(spec["sql"] for spec in get_latency_query_specs())

    assert "duckdb.connect(\":memory:\")" in impl_text
    assert "parquet_scan(" not in "\n".join(spec["sql"] for spec in get_latency_query_specs())
