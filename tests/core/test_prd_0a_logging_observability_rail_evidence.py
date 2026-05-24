from __future__ import annotations

from pathlib import Path

DOC_PATH = Path("docs/prd/PRD-0A-FIX-03_LOGGING_OBSERVABILITY_RAIL_EVIDENCE.md")
TEST_PATH = Path("tests/core/test_prd_0a_logging_observability_rail_evidence.py")


def _doc_text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_references_audit_and_rail() -> None:
    text = _doc_text()
    assert "PRD-0A-AUDIT-01" in text
    assert "logging/observability rail" in text


def test_doc_states_docs_only_no_runtime_logging_or_monitoring_addition() -> None:
    text = _doc_text()
    assert "docs/static-test only" in text
    assert "does not implement runtime logging behavior" in text
    assert "does not add monitoring infrastructure" in text
    assert "does not modify runtime behavior" in text


def test_doc_states_phase1_blocked_and_not_unblock_note() -> None:
    text = _doc_text()
    assert "does not unblock Phase 1" in text
    assert "not a Phase 1 unblock note" in text
    assert "PRD-P1-WX remains blocked" in text


def test_doc_includes_required_evidence_list() -> None:
    text = _doc_text()
    required = [
        "Phase 0B smoke/audit harnesses return explicit status fields",
        "Phase 0B summaries include warnings fields where applicable",
        "Phase 0B readiness docs capture risk/register/status posture",
        "Failure modes are surfaced as explicit statuses, not silent success",
        "CLI JSON summary posture exists for bounded local tools where applicable",
        "Phase 1 remains blocked until explicit unblock note",
    ]
    for phrase in required:
        assert phrase in text


def test_doc_includes_observed_repo_backed_evidence_and_decision() -> None:
    text = _doc_text()
    assert "Observed repo-backed evidence" in text
    assert "logging_observability_rail_status: present" in text


def test_doc_includes_future_expectations_and_non_approvals_and_next_ticket() -> None:
    text = _doc_text()
    required = [
        "critical failures must return explicit fail-closed status",
        "warnings must be surfaced in summaries",
        "no silent fallback to success",
        "no production monitoring claim from this ticket",
        "no weather execution without explicit approved observability posture",
        "no Phase 1 weather bot implementation",
        "no weather bot execution",
        "no production loaders",
        "no production query engine service",
        "no order placement",
        "no live trading",
        "no autonomous execution",
        "no runtime behavior change",
        "no production monitoring infrastructure",
        "no production latency SLO claim",
        "no final trading readiness claim",
        "no generated artifact commit",
        "no committed fixtures",
        "PRD-0A-FIX-04 error/result/status rail evidence",
    ]
    for phrase in required:
        assert phrase in text


def test_referenced_prd_0b_readiness_docs_exist() -> None:
    required_paths = [
        Path("docs/prd/PRD-0B-IMPL-16_PHASE_0B_READINESS_ROLLUP.md"),
        Path("docs/prd/PRD-0B-IMPL-17_PHASE_0B_READINESS_DECISION_GATE.md"),
    ]
    for path in required_paths:
        assert path.exists(), f"missing expected evidence doc: {path.as_posix()}"


def test_phase_0b_status_warnings_summary_posture_docs_and_tests_exist() -> None:
    expected = [
        Path("docs/prd/PRD-0B-IMPL-10_BOUNDED_ARCHIVE_QUERY_SMOKE.md"),
        Path("docs/prd/PRD-0B-IMPL-11_BOUNDED_ARCHIVE_LATENCY_COMPARISON.md"),
        Path("docs/prd/PRD-0B-IMPL-13_DATA_DICTIONARY_SAMPLE_ENRICHMENT.md"),
        Path("docs/prd/PRD-0B-IMPL-15_SAMPLE_ENRICHED_DICTIONARY_LATENCY_READINESS_AUDIT.md"),
        Path("tests/core/test_prd_0b_bounded_archive_query_smoke.py"),
        Path("tests/core/test_prd_0b_bounded_archive_latency_comparison.py"),
        Path("tests/core/test_prd_0b_data_dictionary_sample_enrichment.py"),
        Path("tests/core/test_prd_0b_sample_enriched_dictionary_audit.py"),
    ]
    for path in expected:
        assert path.exists(), f"expected evidence file is missing: {path.as_posix()}"


def test_no_duckdb_or_generated_output_directories_exist() -> None:
    assert not list(Path(".").rglob("*.duckdb"))
    forbidden = [
        "tmp/prd_0b/generated_sql",
        "tmp/prd_0b/generated_reports",
        "tmp/prd_0b/generated_dictionary",
        "tmp/prd_0b/fixture_outputs",
    ]
    for rel in forbidden:
        assert not Path(rel).exists(), f"forbidden output path exists: {rel}"


def test_test_file_has_no_production_runtime_imports() -> None:
    text = TEST_PATH.read_text(encoding="utf-8")
    blocked = ["import" + " scripts.", "from" + " scripts.", "import" + " meg.", "from" + " meg."]
    for token in blocked:
        assert token not in text


def test_no_legacy_identifier_literal_in_new_artifacts() -> None:
    legacy = "market" + "_id"
    for path in [DOC_PATH, TEST_PATH]:
        assert legacy not in path.read_text(encoding="utf-8")
