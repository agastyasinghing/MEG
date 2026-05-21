"""Static checks for Phase 1R-07 master PRD realignment and catch-up plan."""

from pathlib import Path

DOC_PATH = Path("docs/phase1/1R-07_MASTER_PRD_REALIGNMENT_CATCHUP_PLAN.md")
PRD_PATH = Path("MEG_MASTER_PRD_v4.1_patched.md")


def _doc_text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def _prd_text() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def test_realignment_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_doc_contains_required_realignment_statements() -> None:
    text = _doc_text().lower()
    assert "1-01 through 1-06" in text
    assert "not the master prd’s real phase 1 weather paper engine" in text
    assert "master prd phase 1 — weather paper engine" in text
    assert "docs/static-preflight only" in text


def test_doc_contains_phase_deliverables() -> None:
    text = _doc_text().lower()
    phase_0a = [
        "canonical identifier migration",
        "event schemas + redis bus contracts",
        "clob market-state cache writer",
        "clob user-stream service",
        "telegram proposal queue infrastructure",
        "postgres journal schema/writers",
        "paper execution simulator",
        "heartbeat emitter",
        "risk envelope skeleton",
    ]
    phase_0b = [
        "duckdb + parquet + becker setup",
        "bronze/silver normalization views",
        "data dictionary",
        "seven sanity queries",
        "query latency gate",
    ]
    phase_0c = [
        "polygon receipt decoder",
        "signal_engine",
        "signal_aggregator",
        "whale-specific redis channels",
    ]
    phase_1 = [
        "weather forecast pipeline",
        "emos calibration module",
        "resolution source registry",
        "weather strategy module",
        "anomaly veto",
        "50 paper trade exit gate",
        "proposal expiry/defer/rejection exercise",
        "paper p&l attribution",
    ]
    for phrase in [*phase_0a, *phase_0b, *phase_0c, *phase_1]:
        assert phrase in text


def test_doc_contains_gap_statuses_and_planning_sections() -> None:
    text = _doc_text().lower()
    for status in [
        "implemented_verified",
        "static_preflight_only",
        "planned_only",
        "missing",
        "unknown_needs_code_audit",
    ]:
        assert status in text
    assert "do not overclaim implementation" in text
    assert "recommended next prd-aligned ticket sequence" in text
    assert "language/tooling planning note" in text


def test_doc_contains_non_approval_posture() -> None:
    text = _doc_text().lower()
    for phrase in [
        "no weather implementation",
        "no research lake implementation",
        "no duckdb query implementation",
        "no fixture derivation",
        "no fixture commit",
        "no data import",
        "no archive payload reads",
        "no loader implementation",
        "no query engine implementation",
        "no connector implementation",
        "no api calls",
        "no order placement",
        "no live trading",
        "no autonomous execution",
    ]:
        assert phrase in text


def test_master_prd_contains_required_anchor_terms() -> None:
    text = _prd_text().lower()
    assert "phase 1 — weather paper engine" in text
    assert "duckdb + parquet + becker setup" in text
    shared_rail_terms = [
        "phase 0a — shared rail",
        "event schemas + redis bus contracts",
        "telegram proposal queue infrastructure",
        "postgres journal schema and writers",
    ]
    assert any(term in text for term in shared_rail_terms)
