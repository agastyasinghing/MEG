from __future__ import annotations

from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0A-AUDIT-01_SHARED_RAIL_IMPLEMENTATION_GAP_AUDIT.md")
TEST_PATH = Path("tests/core/test_prd_0a_shared_rail_implementation_gap_audit.py")

REQUIRED_RAILS = [
    "Project/PRD governance rail",
    "Dependency/runtime rail",
    "Configuration/secrets rail",
    "Logging/observability rail",
    "Error/result/status rail",
    "Data/artifact hygiene rail",
    "Import-safety/side-effect rail",
    "CI/quality gate rail",
    "Shared interface/API boundary rail",
    "Phase 1 unblock rail",
]


def _doc_text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_audit_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_has_audit_only_posture_and_required_references() -> None:
    text = _doc_text()
    required = [
        "audit only",
        "does not implement fixes",
        "does not unblock Phase 1",
        "PRD-0B-IMPL-16",
        "PRD-0B-IMPL-17",
        "Phase 1 remains blocked pending this 0A audit and any required 0A fixes",
    ]
    for phrase in required:
        assert phrase in text


def test_doc_contains_matrix_and_all_rails() -> None:
    text = _doc_text()
    assert "## 3. Shared rail audit matrix" in text
    assert "| Rail | Required evidence | Observed evidence | Status | Blocker? | Required follow-up |" in text
    for rail in REQUIRED_RAILS:
        assert rail in text


def test_doc_contains_allowed_statuses_and_blocker_classification() -> None:
    text = _doc_text()
    for status in ["present", "partial", "missing", "unknown"]:
        assert status in text
    for phrase in ["P0 blocker", "P1 blocker", "Non-blocking gap", "Unknown"]:
        assert phrase in text


def test_doc_contains_readiness_decision_and_followup_policy() -> None:
    text = _doc_text()
    assert "## 6. Phase 0A readiness decision" in text
    assert "blocked_requires_0a_fixes" in text
    assert "## 7. Required follow-up ticket policy" in text
    assert "PRD-0A-FIX-*" in text


def test_doc_contains_explicit_non_approvals_and_recommended_next_ticketing() -> None:
    text = _doc_text()
    required_non_approvals = [
        "no Phase 1 weather bot implementation",
        "no weather bot execution",
        "no production loaders",
        "no production query engine service",
        "no production connectors/API calls",
        "no order placement",
        "no live trading",
        "no autonomous execution",
        "no production latency SLO claim",
        "no final trading readiness claim",
        "no generated artifact commit",
        "no committed fixtures",
        "no secrets committed",
        "no runtime behavior change",
    ]
    for phrase in required_non_approvals:
        assert phrase in text
    assert "PRD-0A-FIX-01" in text or "PRD-P1-WX-UNBLOCK" in text


def test_dependency_lockfiles_exist() -> None:
    assert Path("pyproject.toml").exists()
    assert Path("uv.lock").exists()


def test_no_duckdb_files_or_generated_output_dirs_exist() -> None:
    assert not list(Path(".").rglob("*.duckdb"))
    forbidden = [
        "tmp/prd_0b/generated_sql",
        "tmp/prd_0b/generated_reports",
        "tmp/prd_0b/generated_dictionary",
        "tmp/prd_0b/fixture_outputs",
    ]
    for rel in forbidden:
        assert not Path(rel).exists()


def test_test_file_has_no_production_runtime_imports() -> None:
    text = TEST_PATH.read_text(encoding="utf-8")
    blocked = ["import" + " scripts.", "from" + " scripts.", "import" + " meg."]
    for token in blocked:
        assert token not in text


def test_no_legacy_identifier_literal_in_new_artifacts() -> None:
    legacy = "market" + "_id"
    for path in [DOC_PATH, TEST_PATH]:
        assert legacy not in path.read_text(encoding="utf-8")
