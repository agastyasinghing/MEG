from __future__ import annotations

import ast
from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-12_DATA_DICTIONARY_SAMPLE_ENRICHMENT_APPROVAL_GATE.md")
TEST_PATH = Path(__file__)


def _doc() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_contains_required_approval_gate_statements() -> None:
    text = _doc()
    required = [
        "approval gate only",
        "does **not** read archives",
        "does **not** execute `parquet_scan`",
        "does **not** parse archive JSON",
        "does **not** import data",
        "does **not** enrich the data dictionary",
        "does **not** create generated dictionary files",
        "does **not** create reports",
        "does **not** create fixtures",
        "does **not** create `.duckdb` files",
    ]
    for phrase in required:
        assert phrase in text


def test_doc_references_required_prior_prd_tickets() -> None:
    text = _doc()
    for ticket in [
        "PRD-0B-IMPL-03",
        "PRD-0B-IMPL-05",
        "PRD-0B-IMPL-09",
        "PRD-0B-IMPL-10",
        "PRD-0B-IMPL-11",
    ]:
        assert ticket in text


def test_doc_contains_required_sections_and_constraints() -> None:
    text = _doc()
    required_phrases = [
        "Why an approval gate is needed",
        "Approved future IMPL-13 scope",
        "Mandatory IMPL-13 limits",
        "Required IMPL-13 input contract",
        "Approved sample enrichment fields",
        "Required IMPL-13 output summary shape",
        "Required IMPL-13 safety tests",
        "Approval decision matrix",
        "Explicit non-approvals",
        "PRD-0B-IMPL-13 archive-backed data dictionary sample enrichment",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_doc_contains_required_safety_disclaimer_phrases() -> None:
    text = _doc()
    for phrase in ["no order placement", "no live trading", "no connectors/API calls"]:
        assert phrase in text


def test_repo_posture_static_guardrails() -> None:
    assert not any(Path(".").glob("*.duckdb"))
    assert Path("pyproject.toml").exists()
    assert Path("uv.lock").exists()


def test_test_file_has_no_production_runtime_imports() -> None:
    tree = ast.parse(TEST_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert not node.module.startswith("scripts")
            assert not node.module.startswith("meg")


def test_no_deprecated_literal_identifier_introduced() -> None:
    assert "market" + "_id" not in DOC_PATH.read_text(encoding="utf-8")
    assert "market" + "_id" not in TEST_PATH.read_text(encoding="utf-8")
