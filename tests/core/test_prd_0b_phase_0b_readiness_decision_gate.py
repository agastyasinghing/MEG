from __future__ import annotations

from pathlib import Path
import subprocess

DOC_PATH = Path("docs/prd/PRD-0B-IMPL-17_PHASE_0B_READINESS_DECISION_GATE.md")
TEST_PATH = Path("tests/core/test_prd_0b_phase_0b_readiness_decision_gate.py")

REQUIRED_SECTIONS = [
    "## 1. Purpose and posture",
    "## 2. Decision summary",
    "## 3. Required evidence checklist",
    "## 4. Decision matrix",
    "## 5. Pass/fail criteria",
    "## 6. What this decision approves",
    "## 7. What this decision does not approve",
    "## 8. PRD-0A dependency and blocker policy",
    "## 9. Conditions for Phase 1 unblock note",
    "## 10. Recommended next tickets",
]


def _doc_text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_decision_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_has_required_sections_and_readiness_posture() -> None:
    text = _doc_text()
    for section in REQUIRED_SECTIONS:
        assert section in text
    assert "readiness decision gate only" in text
    assert "does not implement new behavior" in text
    assert "does not unblock Phase 1 by itself" in text


def test_doc_includes_required_decision_summary_values() -> None:
    text = _doc_text()
    required = [
        "conditionally_ready_for_local_research_rail",
        "blocked_pending_0a_audit",
        "PRD-P1-WX status: `blocked`",
        "PRD-0A-AUDIT-01 status: `required_before_phase_1`",
        "Final trading readiness: `not_approved`",
        "Production readiness: `not_approved`",
    ]
    for phrase in required:
        assert phrase in text


def test_doc_references_required_tickets_and_rollup() -> None:
    text = _doc_text()
    assert "PRD-0B-IMPL-16" in text
    assert "PRD-0B-DEP-01" in text
    assert "PRD-0B-DEP-02" in text
    assert "PRD-0B-QA-01" in text
    for i in range(1, 17):
        assert f"PRD-0B-IMPL-{i:02d}" in text


def test_doc_has_required_gate_language_and_safety_disclaimers() -> None:
    text = _doc_text()
    assert "PRD-0A-AUDIT-01 shared rail implementation gap audit" in text
    assert "PRD-P1-WX status: `blocked`" in text
    required = [
        "no production connectors/API calls",
        "no order placement",
        "no live trading",
    ]
    for phrase in required:
        assert phrase in text


def test_no_duckdb_files_or_generated_output_dirs_exist() -> None:
    assert not list(Path(".").rglob("*.duckdb"))
    forbidden_dirs = [
        "tmp/prd_0b/generated_sql",
        "tmp/prd_0b/generated_reports",
        "tmp/prd_0b/generated_dictionary",
        "tmp/prd_0b/fixture_outputs",
    ]
    for rel in forbidden_dirs:
        assert not Path(rel).exists()


def test_only_allowed_files_are_changed_in_worktree() -> None:
    allowed = {
        "docs/prd/PRD-0B-IMPL-17_PHASE_0B_READINESS_DECISION_GATE.md",
        "tests/core/test_prd_0b_phase_0b_readiness_decision_gate.py",
        "tests/core/canonical_id_allowlist.py",
    }
    out = subprocess.check_output(["git", "status", "--short"], text=True)
    changed = {line.split()[-1] for line in out.splitlines() if line.strip()}
    assert changed <= allowed


def test_test_file_has_no_production_runtime_imports() -> None:
    text = TEST_PATH.read_text(encoding="utf-8")
    blocked = ["import" + " scripts.prd_0b", "from" + " scripts.prd_0b", "import" + " meg."]
    for token in blocked:
        assert token not in text


def test_no_legacy_identifier_literal_in_new_artifacts() -> None:
    legacy = "market" + "_id"
    for path in [DOC_PATH, TEST_PATH]:
        assert legacy not in path.read_text(encoding="utf-8")
