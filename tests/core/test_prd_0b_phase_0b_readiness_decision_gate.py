from __future__ import annotations

from pathlib import Path

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


ALLOWED_CHANGE_PATHS = {
    "docs/prd/PRD-0B-IMPL-17_PHASE_0B_READINESS_DECISION_GATE.md",
    "docs/prd/PRD-P1-WX-KICKOFF_PHASE_1_WEATHER_BOT_TICKET_PLAN.md",
    "docs/prd/PRD-P1-WX-01_WEATHER_BOT_REQUIREMENTS_AND_MARKET_TAXONOMY_PLANNING.md",
    "docs/prd/PRD-P1-WX-02_WEATHER_DATA_PROVIDER_RESEARCH_AND_CONNECTOR_APPROVAL_GATE.md",
    "docs/prd/PRD-P1-WX-03_WEATHER_BOT_CONFIG_SECRETS_FAIL_CLOSED_CONTRACT.md",
    "docs/prd/PRD-P1-WX-04_WEATHER_BOT_RESULT_STATUS_OBSERVABILITY_SUMMARY_CONTRACT.md",
    "tests/core/test_prd_0b_phase_0b_readiness_decision_gate.py",
    "tests/core/test_prd_p1_wx_kickoff_ticket_plan.py",
    "tests/core/test_prd_p1_wx_unblock_note.py",
    "tests/core/test_prd_p1_wx_01_weather_taxonomy.py",
    "tests/core/test_prd_p1_wx_02_weather_provider_research_gate.py",
    "tests/core/test_prd_p1_wx_03_weather_config_secrets_contract.py",
    "tests/core/test_prd_p1_wx_04_weather_status_observability_contract.py",
    "tests/core/test_meta_handoff_roadmap_docs.py",
    "tests/core/canonical_id_allowlist.py",
}


def _is_allowed_docs_or_static_test_change(path: str) -> bool:
    return path in ALLOWED_CHANGE_PATHS


def test_allowlist_accepts_weather_planning_docs_and_static_tests() -> None:
    changed = {
        "docs/prd/PRD-P1-WX-01_WEATHER_BOT_REQUIREMENTS_AND_MARKET_TAXONOMY_PLANNING.md",
        "docs/prd/PRD-P1-WX-04_WEATHER_BOT_RESULT_STATUS_OBSERVABILITY_SUMMARY_CONTRACT.md",
        "tests/core/test_prd_p1_wx_04_weather_status_observability_contract.py",
        "tests/core/test_meta_handoff_roadmap_docs.py",
    }
    disallowed = {path for path in changed if not _is_allowed_docs_or_static_test_change(path)}
    assert not disallowed


def test_allowlist_rejects_production_and_runtime_paths() -> None:
    changed = {
        "src/runtime/main.py",
        "connectors/weather/noaa.py",
        "scripts/build_weather.py",
        "pyproject.toml",
    }
    disallowed = {path for path in changed if not _is_allowed_docs_or_static_test_change(path)}
    assert disallowed == changed


def test_test_file_has_no_production_runtime_imports() -> None:
    text = TEST_PATH.read_text(encoding="utf-8")
    blocked = ["import" + " scripts.prd_0b", "from" + " scripts.prd_0b", "import" + " meg."]
    for token in blocked:
        assert token not in text


def test_no_legacy_identifier_literal_in_new_artifacts() -> None:
    legacy = "market" + "_id"
    for path in [DOC_PATH, TEST_PATH]:
        assert legacy not in path.read_text(encoding="utf-8")
