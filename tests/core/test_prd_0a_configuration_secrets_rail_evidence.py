from __future__ import annotations

from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0A-FIX-02_CONFIGURATION_SECRETS_RAIL_EVIDENCE.md")
TEST_PATH = Path("tests/core/test_prd_0a_configuration_secrets_rail_evidence.py")


def _doc_text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_references_audit_and_configuration_secrets_rail() -> None:
    text = _doc_text()
    assert "PRD-0A-AUDIT-01" in text
    assert "configuration/secrets rail" in text


def test_doc_states_docs_only_and_no_runtime_behavior_change() -> None:
    text = _doc_text()
    assert "docs/static-test only" in text
    assert "does not add secrets" in text
    assert "does not modify runtime behavior" in text


def test_doc_states_phase1_blocked_and_no_weather_start() -> None:
    text = _doc_text()
    assert "does not unblock Phase 1" in text
    assert "not a Phase 1 unblock note" in text
    assert "PRD-P1-WX remains blocked" in text
    assert "does not start weather bot work" in text


def test_doc_includes_required_evidence_section_items() -> None:
    text = _doc_text()
    required = [
        ".env.example` exists or equivalent configuration template evidence exists",
        "no `.env` is committed",
        "no obvious secret/credential files are committed",
        "no production connector/API credentials are committed",
        "configuration/secrets posture is explicitly documented",
        "missing required runtime configuration must fail closed in future implementation",
        "Phase 1 remains blocked until an explicit unblock note is merged",
    ]
    for phrase in required:
        assert phrase in text


def test_doc_includes_observed_evidence_and_gap_resolution_decision() -> None:
    text = _doc_text()
    assert "Observed repository-backed evidence" in text
    assert "configuration_secrets_rail_status: present" in text


def test_doc_includes_fail_closed_expectations_secret_hygiene_and_non_approvals() -> None:
    text = _doc_text()
    required = [
        "missing required configuration should return explicit fail-closed status",
        "no silent fallback to production behavior",
        "no default real API keys",
        "no network calls without explicit configuration",
        "no trading/weather execution without explicit approved configuration",
        ".env.local",
        "secrets.json",
        "credentials.json",
        "no autonomous execution",
        "no generated artifact commit",
    ]
    for phrase in required:
        assert phrase in text


def test_doc_recommends_fix_03_next() -> None:
    assert "PRD-0A-FIX-03 logging/observability rail evidence" in _doc_text()


def test_env_template_exists_or_is_explicitly_documented() -> None:
    if Path(".env.example").exists():
        assert True
        return
    assert "equivalent configuration template evidence exists" in _doc_text()


def test_prohibited_secret_files_not_committed_in_expected_paths() -> None:
    banned_names = {".env", ".env.local", "secrets.json", "credentials.json"}
    scan_dirs = [Path("."), Path("config"), Path("configs"), Path("secrets"), Path(".secrets")]
    for base in scan_dirs:
        if not base.exists():
            continue
        for name in banned_names:
            assert not (base / name).exists(), f"prohibited file present: {(base / name).as_posix()}"


def test_no_duckdb_or_generated_output_directories_exist() -> None:
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
    blocked = ["import" + " scripts.", "from" + " scripts.", "import" + " meg.", "from" + " meg."]
    for token in blocked:
        assert token not in text


def test_no_legacy_identifier_literal_in_new_artifacts() -> None:
    legacy = "market" + "_id"
    for path in [DOC_PATH, TEST_PATH]:
        assert legacy not in path.read_text(encoding="utf-8")
