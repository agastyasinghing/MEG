from __future__ import annotations

from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0A-FIX-01_CI_QUALITY_GATE_EVIDENCE.md")
TEST_PATH = Path("tests/core/test_prd_0a_ci_quality_gate_evidence.py")


def _doc_text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_references_audit_and_issue() -> None:
    text = _doc_text()
    assert "PRD-0A-AUDIT-01" in text
    assert "#161" in text


def test_doc_identifies_ci_quality_gate_rail() -> None:
    text = _doc_text()
    assert "CI/quality gate rail" in text


def test_doc_includes_required_evidence_list() -> None:
    text = _doc_text()
    required = [
        "Phase 0A no-fakeredis smoke workflow exists",
        "Phase 0B research smoke workflow exists",
        "full `tests/core` posture is represented",
        "canonical identifier guard is represented",
        "PRD-0B readiness decision gate exists",
        "Phase 1 remains blocked until explicit unblock note",
        "no production/trading/weather implementation is approved by this fix",
    ]
    for phrase in required:
        assert phrase in text


def test_doc_states_phase1_remains_blocked_and_not_unblock() -> None:
    text = _doc_text()
    assert "Phase 1 remains blocked" in text
    assert "not an unblock note" in text


def test_doc_includes_explicit_non_approvals() -> None:
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


def test_required_repo_evidence_paths_exist() -> None:
    assert Path(".github/workflows/phase0a-smoke.yml").exists()
    assert Path(".github/workflows/phase0b-research-smoke.yml").exists()
    assert Path("tests/core").exists()
    assert Path("tests/core/test_static_canonical_ids.py").exists()
    assert Path("docs/prd/PRD-0B-IMPL-17_PHASE_0B_READINESS_DECISION_GATE.md").exists()


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
