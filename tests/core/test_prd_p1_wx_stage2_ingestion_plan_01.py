"""Static checks for PRD-P1-WX-STAGE2-INGESTION-PLAN-01.

These tests validate the Weather Bot Stage 2 ingestion boundary planning
artifact without creating ingestion, connectors, source fetching, scoring,
runtime behavior, or data artifacts.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-INGESTION-PLAN-01_INGESTION_BOUNDARY_PLANNING.md"
THIS_TEST_PATH = Path(__file__)
CANONICAL_ID = "PRD-P1-WX-STAGE2-INGESTION-PLAN-01"
ASSIGNMENT_HEADING = "## Machine-checkable ingestion boundary planning assignments"
FORBIDDEN_HEADING = "Forbidden ingestion boundary planning values"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Strategic framing",
    "Stage ladder position",
    "Human approval context",
    "Planning-only boundary",
    "Ingestion boundary vocabulary",
    "Allowed future source categories for planning",
    "Prohibited source categories",
    "Source identity and provenance requirements",
    "No-lookahead safeguards",
    "Fixture-to-ingestion separation rules",
    "Static-loader-to-ingestion separation rules",
    "Fail-closed ingestion blocker taxonomy",
    "Provider/source connector handoff rules",
    "Scoring/backtesting handoff rules",
    "Runtime/trading handoff rules",
    "What this planning document confirms",
    "What remains unbuilt",
    "Explicit non-approval boundaries",
    "Future gates",
    "Closed ingestion boundary planning vocabulary",
    "Forbidden ingestion boundary planning values",
    "Machine-checkable ingestion boundary planning assignments",
    "Acceptance criteria",
    "Later-ticket handoff",
)

ALLOWED_ASSIGNMENTS = {
    "ingestion planning stage": {"stage_2_ingestion_boundary_planning"},
    "planning status": {
        "planning_prepared",
        "implementation_not_approved",
        "source_fetching_not_approved",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "planned ingestion boundary category": {
        "ingestion_boundary_vocabulary",
        "source_category_boundary",
        "source_identity_requirement",
        "source_provenance_requirement",
        "access_date_requirement",
        "no_lookahead_requirement",
        "fixture_ingestion_separation",
        "loader_ingestion_separation",
        "fail_closed_blocker_taxonomy",
        "provider_connector_handoff",
        "scoring_backtesting_handoff",
        "runtime_trading_handoff",
    },
    "allowed future source category": {
        "human_reviewed_fixture_source",
        "official_resolution_source",
        "venue_rule_source",
        "weather_station_source",
        "market_metadata_source",
        "manual_research_note",
        "not_applicable",
    },
    "prohibited source category": {
        "unattributed_social_post",
        "unverified_ai_summary",
        "live_market_feed",
        "broker_execution_feed",
        "private_credentials_source",
        "runtime_scrape",
        "unreviewed_bulk_dataset",
        "unknown_source",
        "not_applicable",
    },
    "planned blocker category": {
        "missing_source_identity",
        "missing_access_date",
        "missing_venue_rule",
        "missing_resolver_source",
        "unsupported_source_category",
        "unknown_source_category",
        "source_conflict",
        "time_window_conflict",
        "fixture_ingestion_confusion",
        "loader_ingestion_confusion",
        "runtime_drift",
        "connector_drift",
        "scoring_drift",
        "trading_drift",
        "other_unclear",
    },
    "boundary status": {
        "preserved",
        "not_approved",
        "explicitly_out_of_scope",
        "separate_human_approval_required",
        "blocked",
        "unclear",
    },
    "future ticket permission": {
        "may_request_ingestion_implementation_approval_later",
        "may_request_provider_connector_planning_later",
        "may_request_scoring_backtesting_planning_later",
        "may_request_runtime_observation_planning_later",
        "must_not_create_ingestion_now",
        "must_not_create_connectors",
        "must_not_create_source_fetching",
        "must_not_create_external_api_calls",
        "must_not_create_runtime",
        "must_not_create_scoring",
        "must_not_create_trading",
        "blocked_until_human_decision",
    },
    "data posture": {
        "no_fixture_files_created",
        "no_fixture_files_modified",
        "no_historical_label_data_created",
        "no_generated_data_created",
        "no_loader_expansion_created",
        "no_ingestion_artifacts_created",
        "no_runtime_data_access",
        "no_source_fetching",
        "planning_only",
    },
    "non-approval category": {
        "ingestion_implementation",
        "provider_integration",
        "connectors",
        "source_fetching",
        "external_api_calls",
        "credentials_secrets_config",
        "forecast_pulls",
        "scraping_polling_streaming",
        "scheduling_queues_jobs",
        "model_scoring",
        "probability_scoring",
        "backtesting",
        "paper_simulation",
        "runtime_observation",
        "trading_order_autonomy",
        "production_behavior",
        "cplusplus_rust_runtime",
        "other_unclear",
    },
    "evidence status": {
        "source_backed",
        "reviewer_inferred",
        "missing",
        "conflicting",
        "not_applicable",
    },
    "label confidence": {"confirmed", "unclear", "unknown"},
}

FORBIDDEN_EXAMPLES = {
    "planning_prepared/implementation_not_approved",
    "preserved/not_approved",
    "source_backed/reviewer_inferred",
    "confirmed/unclear",
    "partial",
    "mixed",
    "likely_confirmed",
    "maybe",
    "approved",
    "configured",
    "available",
    "ingestion_ready",
    "connector_ready",
    "provider_ready",
    "source_ready",
    "scoring_ready",
    "runtime_ready",
    "trading_ready",
    "production_ready",
    "model_ready",
    "back" + "test_ready",
    "ready_for_ingestion",
    "ready_for_connectors",
    "ready_for_source_fetching",
    "ready_for_scoring",
    "ready_for_runtime",
    "ready_for_trading",
    "approved_for_ingestion",
    "approved_for_connectors",
    "approved_for_source_fetching",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
    "trade_ready",
    "auto" + "_execute",
    "aut" + "onomous",
    "live",
    "production",
}

REQUIRED_REFERENCES = (
    "docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
    "MEG_ACTIVE_STATE",
    "WEATHER_BOT_PACKET",
    "PRD-P1-WX-STAGE2-INGESTION-PLANNING-APPROVAL-01",
    "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01",
    "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
    "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
)

REQUIRED_SCOPE_PHRASES = (
    "This is ingestion boundary planning only.",
    "ingestion implementation is not approved",
    "Provider/API connector implementation is not approved",
    "Source fetching is not approved",
    "External API calls are not approved",
    "Credentials/secrets/config loading is not approved",
    "Forecast pulls are not approved",
    "Scoring/probability scoring is not approved",
    "Backtesting/paper simulation is not approved",
    "Runtime observation is not approved",
    "Trading, order placement, position sizing, and autonomy are not approved",
    "Production behavior is not approved",
    "C++/Rust runtime components are not approved",
    "No loader expansion is created or approved",
    "No fixture JSON files are read by new source/runtime code",
    "No fixture JSON files are created or modified",
    "No fixture README files are created or modified",
    "no historical-label data files are created",
    "no generated data is created",
    "Future ingestion implementation requires a later separate approval chain",
    "Future provider/API connector implementation requires a later separate approval chain",
    "Future provider/source connector implementation requires a later separate approval chain",
    "Future source fetching requires a later separate approval chain",
    "scraping, polling, streaming, scheduling, queues, jobs, and background tasks are not approved",
    "current fixture, loading, loader, and ingestion-planning documents do not imply ingestion readiness, provider readiness, scoring readiness, runtime readiness, production readiness, or trading readiness",
)

FORBIDDEN_IMPLEMENTATION_FRAGMENTS = (
    "os." + "environ",
    "load_" + "dot" + "env",
    "dot" + "env",
    "requests" + ".",
    "http" + "x.",
    "aio" + "http",
    "urllib." + "request",
    "api_" + "key",
    "secret_" + "key",
    "weather_" + "api_" + "key",
    "fast" + "api",
    "fl" + "ask",
    "sql" + "alchemy",
    "pan" + "das",
    "pol" + "ars",
    "duck" + "db",
    "read_" + "csv",
    "to_" + "csv",
    "json." + "load",
    "json" + "lines",
    "par" + "quet",
    "pre" + "dict",
)


def _prd_text() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    marker = "## " + heading + "\n"
    assert marker in text
    section_start = text.index(marker) + len(marker)
    next_heading = text.find("\n## ", section_start)
    if next_heading == -1:
        return text[section_start:]
    return text[section_start:next_heading]


def _assignment_section(text: str) -> str:
    marker = ASSIGNMENT_HEADING + "\n"
    assert marker in text
    section_start = text.index(marker) + len(marker)
    next_heading = text.find("\n## ", section_start)
    if next_heading == -1:
        return text[section_start:]
    return text[section_start:next_heading]


def _parsed_assignments() -> dict[str, set[str]]:
    parsed = {prefix: set() for prefix in ALLOWED_ASSIGNMENTS}
    for raw_line in _assignment_section(_prd_text()).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        assert line.startswith("- "), line
        body = line[2:]
        prefix, separator, value = body.partition(": ")
        assert separator == ": ", line
        assert prefix in ALLOWED_ASSIGNMENTS, line
        assert value in ALLOWED_ASSIGNMENTS[prefix], line
        parsed[prefix].add(value)
    return parsed


def test_planning_prd_exists_and_has_required_sections() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    assert CANONICAL_ID in text
    for section in REQUIRED_SECTIONS:
        assert "## " + section in text


def test_required_context_references_are_present() -> None:
    text = _prd_text()
    for reference in REQUIRED_REFERENCES:
        assert reference in text


def test_planning_only_non_approval_scope_is_stated() -> None:
    text = _prd_text()
    for phrase in REQUIRED_SCOPE_PHRASES:
        assert phrase in text


def test_vocabulary_includes_required_source_and_blocker_categories() -> None:
    text = _prd_text()
    for value in ALLOWED_ASSIGNMENTS["allowed future source category"]:
        assert value in text
    for value in ALLOWED_ASSIGNMENTS["prohibited source category"]:
        assert value in text
    for value in ALLOWED_ASSIGNMENTS["planned blocker category"]:
        assert value in text


def test_machine_checkable_assignment_section_exists() -> None:
    section = _assignment_section(_prd_text())
    assert "- ingestion planning stage: stage_2_ingestion_boundary_planning" in section
    assert "## Acceptance criteria" not in section


def test_closed_set_assignments_use_only_allowed_values() -> None:
    parsed = _parsed_assignments()
    assert set(parsed) == set(ALLOWED_ASSIGNMENTS)


def test_every_allowed_value_appears_in_machine_checkable_assignments() -> None:
    parsed = _parsed_assignments()
    assert parsed == ALLOWED_ASSIGNMENTS


def test_forbidden_examples_are_documented_but_not_actual_assignments() -> None:
    text = _prd_text()
    forbidden_section = _section(text, FORBIDDEN_HEADING)
    assignment_section = _assignment_section(text)

    for value in FORBIDDEN_EXAMPLES:
        assert "`" + value + "`" in forbidden_section
        assert not re.search(r": " + re.escape(value) + r"$", assignment_section, re.MULTILINE)


def test_forbidden_implementation_fragments_are_absent_from_new_files() -> None:
    for path in (PRD_PATH, THIS_TEST_PATH):
        text = path.read_text(encoding="utf-8")
        unexpected = [fragment for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS if fragment in text]
        assert unexpected == []


def test_static_test_uses_standard_library_only() -> None:
    tree = ast.parse(THIS_TEST_PATH.read_text(encoding="utf-8"))
    import_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            import_roots.add(node.module.split(".")[0])

    assert import_roots <= {"__future__", "ast", "pathlib", "re"}
