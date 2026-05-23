from __future__ import annotations

import ast
from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-09_ARCHIVE_BACKED_BOUNDED_SMOKE_APPROVAL_GATE.md")


def _doc_text() -> str:
    assert DOC_PATH.exists()
    return DOC_PATH.read_text(encoding="utf-8")


def test_doc_exists_and_posture_lines_present() -> None:
    text = _doc_text()
    required = [
        "approval gate only",
        "does not read archives",
        "does not execute parquet_scan",
        "does not import data",
        "does not create fixtures",
        "does not create generated outputs",
        "does not create `.duckdb` files",
        "does not claim production latency or trading readiness",
    ]
    for phrase in required:
        assert phrase in text


def test_doc_references_impl_02_through_impl_08() -> None:
    text = _doc_text()
    for phrase in [
        "IMPL-02 Becker sanity harness",
        "IMPL-03 data dictionary contract",
        "IMPL-04 Bronze/Silver plan",
        "IMPL-05 data dictionary generator",
        "IMPL-06 view skeleton",
        "IMPL-07 semantic hardening",
        "IMPL-08 synthetic latency gate",
    ]:
        assert phrase in text


def test_doc_contains_gate_rationale_and_impl_10_scope_sections() -> None:
    text = _doc_text()
    for phrase in [
        "Why an approval gate is needed",
        "touches local archive paths and bounded parquet/json reads",
        "prevents accidental full-archive scans or generated artifact commits",
        "Approved future IMPL-10 scope",
        "--archive-root",
        "fail closed on missing DuckDB",
    ]:
        assert phrase in text


def test_doc_contains_mandatory_limits_input_output_safety_and_matrix() -> None:
    text = _doc_text()
    for phrase in [
        "Mandatory IMPL-10 limits",
        "no recursive full-archive scan",
        "no unbounded parquet glob",
        "no more than one representative file per dataset family by default",
        "no more than seven dataset families",
        "no more than 1000 rows per query by default",
        "Required IMPL-10 input contract",
        "explicit family allowlist",
        "explicit row limit",
        "explicit representative-file selection strategy",
        "explicit JSON summary mode",
        "explicit no-output default",
        "explicit fail-closed status fields",
        "Required IMPL-10 output summary shape",
        "archive_root_status",
        "duckdb_status",
        "family_count",
        "checked_families",
        "skipped_families",
        "missing_families",
        "representative_files",
        "row_limit",
        "query_results",
        "elapsed_ms_by_query",
        "warnings",
        "wrote_outputs",
        "created_duckdb_file",
        "generated_artifacts",
        "Required IMPL-10 safety tests",
        "missing archive root fails closed",
        "unsafe archive root rejected",
        "Approval decision matrix",
        "| Decision item | Approved for IMPL-10? | Required constraint | Failure mode if violated |",
    ]:
        assert phrase in text


def test_doc_contains_explicit_non_approvals_and_next_ticket() -> None:
    text = _doc_text()
    for phrase in [
        "Explicit non-approvals",
        "no archive reads in this ticket",
        "no parquet_scan in this ticket",
        "no full data import",
        "no generated SQL outputs",
        "no generated reports",
        "no generated dictionary files",
        "no `.duckdb` files",
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
        "PRD-0B-IMPL-10 bounded archive query smoke",
    ]:
        assert phrase in text


def test_repository_hygiene_constraints_hold() -> None:
    assert Path("pyproject.toml").exists()
    assert Path("uv.lock").exists()
    assert not any(Path(".").glob("*.duckdb"))
    assert not any(Path(".").glob("**/*.duckdb"))

    for disallowed in [
        Path("reports"),
        Path("generated"),
        Path("artifacts"),
        Path("fixtures/output"),
    ]:
        assert not disallowed.exists()


def test_test_module_has_no_production_runtime_imports() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(not name.name.startswith("meg") for name in node.names)
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert not node.module.startswith("meg")
