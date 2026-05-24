from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/prd/PRD-P1-WX-KICKOFF_PHASE_1_WEATHER_BOT_TICKET_PLAN.md"
TEST_FILE = ROOT / "tests/core/test_prd_p1_wx_kickoff_ticket_plan.py"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_kickoff_doc_exists() -> None:
    assert DOC.exists()


def test_kickoff_doc_required_content() -> None:
    text = _text(DOC)
    required = [
        "Phase 1 weather bot kickoff and ticket plan",
        "PRD-P1-WX-UNBLOCK",
        "docs/static-test planning only",
        "does not implement weather bot behavior",
        "does not execute weather bot behavior",
        "does not add external weather/API connector behavior",
        "does not modify runtime behavior",
        "does not add production connectors/API calls",
        "does not add order placement, live trading, or autonomy",
        "PRD-0A-CLOSE-01",
        "PRD-0B-IMPL-17",
        "PRD-0A-AUDIT-01",
        "PRD-0A-FIX-01",
        "PRD-0A-FIX-02",
        "PRD-0A-FIX-03",
        "PRD-0A-FIX-04",
        "Phase 1 weather bot scope",
        "Phase 1 non-goals",
        "Proposed Phase 1 ticket sequence",
        "PRD-P1-WX-01 Weather bot requirements and market taxonomy planning",
        "First implementation ticket recommendation",
        "Approval gates",
        "Phase 1 safety rules",
        "CI/test posture",
        "What this kickoff approves",
        "What this kickoff does not approve",
        "Recommended next tickets",
    ]
    for needle in required:
        assert needle in text


def test_referenced_docs_exist() -> None:
    required_docs = [
        ROOT / "docs/prd/PRD-P1-WX-UNBLOCK_EXPLICIT_PHASE_1_WEATHER_BOT_UNBLOCK_NOTE.md",
        ROOT / "docs/prd/PRD-0A-CLOSE-01_PHASE_0A_READINESS_CLOSURE.md",
        ROOT / "docs/prd/PRD-0B-IMPL-17_PHASE_0B_READINESS_DECISION_GATE.md",
        ROOT / "docs/prd/PRD-0A-AUDIT-01_SHARED_RAIL_IMPLEMENTATION_GAP_AUDIT.md",
        ROOT / "docs/prd/PRD-0A-FIX-01_CI_QUALITY_GATE_EVIDENCE.md",
        ROOT / "docs/prd/PRD-0A-FIX-02_CONFIGURATION_SECRETS_RAIL_EVIDENCE.md",
        ROOT / "docs/prd/PRD-0A-FIX-03_LOGGING_OBSERVABILITY_RAIL_EVIDENCE.md",
        ROOT / "docs/prd/PRD-0A-FIX-04_ERROR_RESULT_STATUS_RAIL_EVIDENCE.md",
    ]
    for path in required_docs:
        assert path.exists()


def test_no_duckdb_files_exist() -> None:
    assert not any(ROOT.rglob("*.duckdb"))


def test_no_generated_output_directories_exist() -> None:
    forbidden_dirs = [
        ROOT / "sql/prd_0b/generated",
        ROOT / "reports/generated",
        ROOT / "reports/prd_0b/generated",
        ROOT / "dictionaries/generated",
        ROOT / "fixtures/output",
        ROOT / "tests/fixtures/output",
        ROOT / "tmp/prd_0b/generated_sql",
        ROOT / "tmp/prd_0b/generated_reports",
        ROOT / "tmp/prd_0b/generated_dictionary",
        ROOT / "tmp/prd_0b/fixture_outputs",
    ]
    for path in forbidden_dirs:
        assert not path.exists()


def test_test_file_has_no_production_runtime_imports() -> None:
    text = _text(TEST_FILE)
    blocked = ["import" + " scripts.", "from" + " scripts.", "import" + " meg.", "from" + " meg."]
    for token in blocked:
        assert token not in text


def test_no_deprecated_literal_identifier_introduced() -> None:
    legacy_identifier = "market" + "_id"
    combined = _text(DOC) + "\n" + _text(TEST_FILE)
    assert legacy_identifier not in combined
