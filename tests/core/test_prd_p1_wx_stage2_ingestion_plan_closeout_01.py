"""Static checks for PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01.

These tests validate the Weather Bot Stage 2 ingestion boundary planning
closeout without creating ingestion, connectors, source fetching, scoring,
runtime behavior, or data artifacts.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / (
    "docs/prd/"
    "PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01_"
    "INGESTION_BOUNDARY_PLANNING_CLOSEOUT_CHECKPOINT.md"
)
THIS_TEST_PATH = Path(__file__)
CANONICAL_ID = "PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01"
ASSIGNMENT_HEADING = "## Machine-checkable ingestion boundary planning closeout assignments"
FORBIDDEN_HEADING = "Forbidden ingestion boundary planning closeout values"
INVENTORY_HEADING = "Ingestion planning inventory"

EXPECTED_INVENTORY = [
    "docs/prd/PRD-P1-WX-STAGE2-INGESTION-PLANNING-APPROVAL-01_INGESTION_PLANNING_APPROVAL_REQUEST.md",
    "docs/prd/PRD-P1-WX-STAGE2-INGESTION-PLAN-01_INGESTION_BOUNDARY_PLANNING.md",
    "tests/core/test_prd_p1_wx_stage2_ingestion_planning_approval_01.py",
    "tests/core/test_prd_p1_wx_stage2_ingestion_plan_01.py",
]

REQUIRED_SECTIONS = (
    "Status and scope",
    "Strategic framing",
    "Stage ladder position",
    "Ingestion planning inventory",
    "Planning artifact summary",
    "Boundary vocabulary summary",
    "Allowed future source category summary",
    "Prohibited source category summary",
    "Source identity and provenance planning summary",
    "No-lookahead safeguard summary",
    "Fixture-to-ingestion separation summary",
    "Static-loader-to-ingestion separation summary",
    "Fail-closed blocker taxonomy summary",
    "Handoff rule summary",
    "What this closeout confirms",
    "What remains unbuilt",
    "Explicit non-approval boundaries",
    "Future gates",
    "Recommended hold/checkpoint posture",
    "Closed ingestion boundary planning closeout vocabulary",
    "Forbidden ingestion boundary planning closeout values",
    "Machine-checkable ingestion boundary planning closeout assignments",
    "Acceptance criteria",
    "Later-ticket handoff",
)

ALLOWED_ASSIGNMENTS = {
    "ingestion planning closeout stage": {
        "stage_2_ingestion_boundary_planning_closeout_checkpoint",
    },
    "closeout status": {
        "v1_complete",
        "hold_for_review",
        "blocked_pending_gap",
        "unclear",
    },
    "planning artifact status": {
        "present",
        "missing",
        "not_applicable",
    },
    "planning boundary status": {
        "preserved",
        "violated",
        "unclear",
    },
    "planned coverage": {
        "ingestion_boundary_vocabulary_planned",
        "source_category_boundary_planned",
        "source_identity_requirement_planned",
        "source_provenance_requirement_planned",
        "access_date_requirement_planned",
        "no_lookahead_requirement_planned",
        "fixture_ingestion_separation_planned",
        "loader_ingestion_separation_planned",
        "fail_closed_blocker_taxonomy_planned",
        "provider_connector_handoff_planned",
        "scoring_backtesting_handoff_planned",
        "runtime_trading_handoff_planned",
    },
    "source category coverage": {
        "allowed_future_source_categories_planned",
        "prohibited_source_categories_planned",
        "unknown_source_category_blocks_later_work",
        "private_credentials_source_blocks_later_work",
        "runtime_scrape_blocks_later_work",
        "live_market_feed_blocks_later_work",
        "not_applicable_supported_as_closed_placeholder",
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
        "planning_closeout_only",
    },
    "next gate category": {
        "hold",
        "targeted_ingestion_planning_refinement_if_gap_found",
        "active_state_update_if_needed",
        "ingestion_implementation_approval_request_if_chosen",
        "provider_connector_planning_approval_request_if_chosen",
        "scoring_backtesting_planning_approval_request_if_chosen",
        "runtime_observation_planning_approval_request_if_chosen",
        "trading_order_autonomy_later_explicit_approval_only",
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
    "v1_complete/hold_for_review",
    "preserved/violated",
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
    return _section(text, ASSIGNMENT_HEADING.removeprefix("## "))


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


def _source_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    import_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            import_roots.add(node.module.split(".")[0])
    return import_roots - {"__future__"}


def test_closeout_prd_exists_with_required_source_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    for required in (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-INGESTION-PLANNING-APPROVAL-01",
        "PRD-P1-WX-STAGE2-INGESTION-PLAN-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
        "Stage 2 skeleton closeout",
    ):
        assert required in text


def test_required_sections_are_present_in_order() -> None:
    text = _prd_text()
    cursor = -1
    for section in REQUIRED_SECTIONS:
        heading = "## " + section
        next_cursor = text.find(heading)
        assert next_cursor > cursor, section
        cursor = next_cursor


def test_closeout_only_safety_language_is_present() -> None:
    text = _prd_text()
    lower_text = text.lower()
    for required in (
        "This is ingestion boundary planning closeout/checkpoint only.",
        "Ingestion boundary planning v1 is complete for now.",
        "Ingestion implementation is not approved.",
        "Provider/API connector implementation is not approved.",
        "Source fetching is not approved.",
        "External API calls are not approved.",
        "Credentials/secrets/config loading is not approved.",
        "Forecast pulls are not approved.",
        "Scoring/probability scoring is not approved.",
        "Backtesting/paper simulation is not approved.",
        "Runtime observation is not approved.",
        "Trading, order placement, position sizing, and autonomy are not approved.",
        "Production behavior is not approved.",
        "C++/Rust runtime components are not approved.",
        "No loader expansion was created or approved.",
        "No fixture JSON files were read by new source/runtime code.",
        "No fixture JSON files were created or modified.",
        "No fixture README files were created or modified.",
        "No historical-label data files were created.",
        "No generated data was created.",
        "Future ingestion implementation requires a later separate approval chain.",
        "Future provider/API connector implementation requires a later separate approval chain.",
        "Future provider/source connector implementation requires a later separate approval chain.",
        "Future source fetching requires a later separate approval chain.",
        "Future scoring/backtesting requires separate explicit approval.",
        "Future runtime/trading requires separate explicit approval.",
        "recommended posture is hold/checkpoint unless a concrete ingestion-planning gap is found",
    ):
        assert required in text or required.lower() in lower_text


def test_readiness_disclaimer_includes_current_planning_stack() -> None:
    text = _prd_text().lower()
    required = (
        "current fixture, loading, loader, ingestion-approval, and ingestion-planning "
        "documents do not imply ingestion readiness, provider readiness, scoring readiness, "
        "runtime readiness, production readiness, or trading readiness"
    )
    assert required in text


def test_planning_inventory_lists_exactly_the_expected_artifacts() -> None:
    inventory = _section(_prd_text(), INVENTORY_HEADING)
    observed = [
        line.removeprefix("- `").removesuffix("`")
        for line in inventory.splitlines()
        if line.startswith("- `")
    ]
    assert observed == EXPECTED_INVENTORY


def test_source_coverage_blocker_taxonomy_and_handoffs_are_summarized() -> None:
    text = _prd_text()
    for required in (
        "Allowed future source category coverage is planning-only",
        "Prohibited source category coverage includes unknown source categories",
        "private credential-dependent sources",
        "runtime scrape categories",
        "live market feed categories",
        "Fail-closed blocker taxonomy summary",
        "A blocker means later work stops until a separate human-approved planning or approval chain resolves the gap.",
        "Handoff rules remain planning-only.",
        "Provider/source connector handoff",
        "scoring/backtesting handoff",
        "runtime observation handoff",
        "trading/order/autonomy handoff",
    ):
        assert required in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    assert section.strip()
    assert "## Acceptance criteria" not in section
    assert "## " not in section
    assert FORBIDDEN_HEADING not in section


def test_closed_set_assignments_use_only_allowed_values_and_include_every_value() -> None:
    parsed = _parsed_assignments()
    assert parsed == ALLOWED_ASSIGNMENTS


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_values() -> None:
    forbidden_section = _section(_prd_text(), FORBIDDEN_HEADING)
    for forbidden in FORBIDDEN_EXAMPLES:
        assert forbidden in forbidden_section

    parsed_values = set().union(*_parsed_assignments().values())
    for forbidden in FORBIDDEN_EXAMPLES:
        assert forbidden not in parsed_values


def test_machine_parser_ignores_forbidden_examples_and_acceptance_criteria_prose() -> None:
    text = _prd_text()
    assert "approved_for_ingestion" in _section(text, FORBIDDEN_HEADING)
    assert "forbidden examples are documented" in _section(text, "Acceptance criteria").lower()
    parsed_values = set().union(*_parsed_assignments().values())
    assert "approved_for_ingestion" not in parsed_values
    assert "v1_complete/hold_for_review" not in parsed_values


def test_no_forbidden_implementation_fragments_appear_in_new_files() -> None:
    for path in (PRD_PATH, THIS_TEST_PATH):
        text = path.read_text(encoding="utf-8")
        for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS:
            assert fragment not in text, (path, fragment)


def test_static_test_uses_python_standard_library_only() -> None:
    assert _source_import_roots(THIS_TEST_PATH) <= {"ast", "re", "pathlib"}


def test_scope_did_not_create_disallowed_artifact_references() -> None:
    text = _prd_text().lower()
    for required in (
        "does not create new fixture files",
        "does not modify real or synthetic fixture json files",
        "does not add source records",
        "does not create historical-label data files",
        "does not create generated data",
        "does not create, approve, or imply any ingestion implementation",
    ):
        assert required in text


def test_safety_audit_phrases_only_appear_as_non_approvals() -> None:
    text = _prd_text().lower()
    approval_drift_phrases = (
        "ingestion implementation " + "approved",
        "connector " + "approved",
        "provider integration " + "approved",
        "source fetching " + "approved",
        "external api calls " + "approved",
        "scoring " + "approved",
        "backtesting " + "approved",
        "runtime " + "approved",
        "trading " + "approved",
        "order placement " + "approved",
        "autonomy " + "approved",
        "production " + "approved",
        "connector implementation " + "approved",
        "provider implementation " + "approved",
    )
    approval_drift_patterns = tuple(r"(?<!not )" + phrase for phrase in approval_drift_phrases)
    for pattern in approval_drift_patterns:
        assert re.search(pattern, text) is None
