from __future__ import annotations

from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-16_PHASE_0B_READINESS_ROLLUP.md")
TEST_PATH = Path("tests/core/test_prd_0b_phase_0b_readiness_rollup.py")

REQUIRED_TICKETS = [
    "PRD-0B-DEP-01",
    "PRD-0B-DEP-02",
    "PRD-0B-QA-01",
    *[f"PRD-0B-IMPL-{i:02d}" for i in range(1, 16)],
]

REQUIRED_SECTIONS = [
    "## 1. Purpose and posture",
    "## 2. Phase 0B scope recap",
    "## 3. Ticket evidence matrix",
    "## 4. Phase 0B capability rollup",
    "## 5. Explicit remaining non-approvals",
    "## 6. Phase 0B readiness assessment",
    "## 7. PRD-0A dependency",
    "## 8. Phase 1 / weather bot gating",
    "## 9. Readiness risk register",
    "## 10. Recommended next tickets",
]


def _doc_text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_rollup_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_has_required_sections_and_posture_language() -> None:
    text = _doc_text()
    for section in REQUIRED_SECTIONS:
        assert section in text

    assert "readiness rollup only" in text
    assert "does not implement new behavior" in text
    assert "does not unblock Phase 1 by itself" in text


def test_doc_references_all_required_tickets() -> None:
    text = _doc_text()
    for ticket in REQUIRED_TICKETS:
        assert ticket in text


def test_doc_has_required_gating_and_next_step_language() -> None:
    text = _doc_text()
    assert "PRD-P1-WX remains blocked" in text
    assert "PRD-0B-IMPL-17" in text
    assert "PRD-0A-AUDIT-01" in text


def test_doc_has_required_non_approval_safety_disclaimers() -> None:
    text = _doc_text()
    required = [
        "no production loaders",
        "no production query engine service",
        "no production connectors/API calls",
        "no order placement",
        "no live trading",
        "no autonomous execution",
        "no weather implementation",
        "no Phase 1 weather bot execution",
        "no production latency SLO claim",
        "no final trading readiness claim",
        "no full archive import",
        "no recursive full-archive scan",
        "no generated dictionary commit",
        "no committed fixtures",
        "no strategy labels",
        "no trade/opportunity labels",
    ]
    for phrase in required:
        assert phrase in text


def test_rollup_test_file_exists() -> None:
    assert TEST_PATH.exists()


def test_dependency_lockfiles_exist_without_timestamp_inference() -> None:
    assert Path("pyproject.toml").exists()
    assert Path("uv.lock").exists()


def test_no_duckdb_files_exist() -> None:
    assert not list(Path(".").rglob("*.duckdb"))


def test_no_generated_output_dirs_exist() -> None:
    forbidden = [
        "tmp/prd_0b/generated_sql",
        "tmp/prd_0b/generated_reports",
        "tmp/prd_0b/generated_dictionary",
        "tmp/prd_0b/fixture_outputs",
    ]
    for rel in forbidden:
        assert not Path(rel).exists()


def test_test_file_has_no_production_runtime_imports() -> None:
    text = Path(__file__).read_text(encoding="utf-8")
    blocked = ["import" + " scripts.prd_0b", "from" + " scripts.prd_0b", "import" + " meg."]
    for token in blocked:
        assert token not in text


def test_no_legacy_identifier_literal_in_new_artifacts() -> None:
    for path in [DOC_PATH, Path(__file__)]:
        legacy = "market" + "_id"
        assert legacy not in path.read_text(encoding="utf-8")
