from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/prd/PRD-0A-CLOSE-01_PHASE_0A_READINESS_CLOSURE.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_closure_doc_exists() -> None:
    assert DOC.exists()


def test_closure_doc_required_content() -> None:
    text = _text(DOC)
    required_substrings = [
        "PRD-0A-AUDIT-01",
        "PRD-0B-IMPL-16",
        "PRD-0B-IMPL-17",
        "docs/static-test only",
        "does not implement runtime behavior",
        "does not unblock Phase 1 by itself",
        "not a Phase 1 unblock note",
        "does not start weather bot work",
        "Phase 0A fix evidence matrix",
        "PRD-0A-FIX-01",
        "PRD-0A-FIX-02",
        "PRD-0A-FIX-03",
        "PRD-0A-FIX-04",
        "phase_0a_shared_rail_closure_status: closed_for_phase_1_unblock_review",
        "phase_1_weather_bot_status: blocked_pending_explicit_unblock_note",
        "prd_p1_wx_status: blocked",
        "production_readiness_status: not_approved",
        "final_trading_readiness_status: not_approved",
        "Remaining blocker assessment",
        "Conditions for PRD-P1-WX-UNBLOCK",
        "What this closure approves",
        "What this closure does not approve",
        "Recommended next tickets",
        "PRD-P1-WX-UNBLOCK",
    ]
    for needle in required_substrings:
        assert needle in text


def test_referenced_docs_exist() -> None:
    expected = [
        ROOT / "docs/prd/PRD-0A-AUDIT-01_SHARED_RAIL_IMPLEMENTATION_GAP_AUDIT.md",
        ROOT / "docs/prd/PRD-0A-FIX-01_CI_QUALITY_GATE_EVIDENCE.md",
        ROOT / "docs/prd/PRD-0A-FIX-02_CONFIGURATION_SECRETS_RAIL_EVIDENCE.md",
        ROOT / "docs/prd/PRD-0A-FIX-03_LOGGING_OBSERVABILITY_RAIL_EVIDENCE.md",
        ROOT / "docs/prd/PRD-0A-FIX-04_ERROR_RESULT_STATUS_RAIL_EVIDENCE.md",
        ROOT / "docs/prd/PRD-0B-IMPL-16_PHASE_0B_READINESS_ROLLUP.md",
        ROOT / "docs/prd/PRD-0B-IMPL-17_PHASE_0B_READINESS_DECISION_GATE.md",
    ]
    for path in expected:
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
    ]
    for path in forbidden_dirs:
        assert not path.exists()


def test_no_deprecated_literal_identifier_introduced() -> None:
    text = _text(DOC) + "\n" + _text(Path(__file__))
    legacy_identifier = "market" + "_id"
    assert legacy_identifier not in text
