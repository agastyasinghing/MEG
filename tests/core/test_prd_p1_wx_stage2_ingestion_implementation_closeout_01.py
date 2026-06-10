"""Static checks for PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01.

These tests validate the Weather Bot Stage 2 static ingestion boundary skeleton
implementation closeout without creating ingestion, connectors, source fetching,
scoring, runtime behavior, or data artifacts.
"""
from __future__ import annotations

import ast
import importlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / (
    "docs/prd/"
    "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01_"
    "STATIC_INGESTION_BOUNDARY_SKELETON_CLOSEOUT_CHECKPOINT.md"
)
MODULE_PATH = REPO_ROOT / "meg/weather/stage2/ingestion_boundary.py"
IMPLEMENTATION_TEST_PATH = REPO_ROOT / "tests/core/test_prd_p1_wx_stage2_ingestion_implementation_01.py"
IMPLEMENTATION_PRD_PATH = REPO_ROOT / (
    "docs/prd/PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01_"
    "STATIC_INGESTION_BOUNDARY_SKELETON.md"
)
THIS_TEST_PATH = Path(__file__)
CANONICAL_ID = "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-CLOSEOUT-01"
ASSIGNMENT_HEADING = "## Machine-checkable static ingestion implementation closeout assignments"
FORBIDDEN_HEADING = "Forbidden static ingestion implementation closeout values"
INVENTORY_HEADING = "Implementation inventory"

EXPECTED_INVENTORY = [
    "meg/weather/stage2/ingestion_boundary.py",
    "docs/prd/PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01_STATIC_INGESTION_BOUNDARY_SKELETON.md",
    "tests/core/test_prd_p1_wx_stage2_ingestion_implementation_01.py",
]

REQUIRED_SECTIONS = (
    "Status and scope",
    "Strategic framing",
    "Stage ladder position",
    "Implementation inventory",
    "Static ingestion skeleton summary",
    "Implemented source module summary",
    "Implemented public API summary",
    "Closed source category vocabulary summary",
    "Evidence and confidence vocabulary summary",
    "Fail-closed blocker taxonomy summary",
    "Validation severity behavior summary",
    "Fixture-to-ingestion separation summary",
    "Static-loader-to-ingestion separation summary",
    "No-lookahead safeguard summary",
    "Static validation test summary",
    "What this closeout confirms",
    "What remains unbuilt",
    "Explicit non-approval boundaries",
    "Future gates",
    "Recommended hold/checkpoint posture",
    "Closed static ingestion implementation closeout vocabulary",
    "Forbidden static ingestion implementation closeout values",
    "Machine-checkable static ingestion implementation closeout assignments",
    "Acceptance criteria",
    "Later-ticket handoff",
)

ALLOWED_ASSIGNMENTS = {
    "static ingestion implementation closeout stage": {
        "stage_2_static_ingestion_boundary_skeleton_closeout_checkpoint",
    },
    "closeout status": {
        "v1_complete",
        "hold_for_review",
        "blocked_pending_gap",
        "unclear",
    },
    "implementation artifact status": {
        "present",
        "missing",
        "not_applicable",
    },
    "implementation boundary status": {
        "preserved",
        "violated",
        "unclear",
    },
    "implemented coverage": {
        "static_ingestion_boundary_module_present",
        "closed_source_category_vocabulary_present",
        "evidence_confidence_vocabulary_present",
        "validation_severity_vocabulary_present",
        "source_descriptor_dataclass_present",
        "validation_result_dataclass_present",
        "mapping_builder_present",
        "descriptor_validator_present",
        "mapping_validator_present",
        "fail_closed_blocker_taxonomy_present",
        "no_lookahead_validation_present",
        "fixture_loader_separation_validation_present",
        "drift_language_blockers_present",
        "static_tests_present",
    },
    "data posture": {
        "no_fixture_files_created",
        "no_fixture_files_modified",
        "no_historical_label_data_created",
        "no_generated_data_created",
        "no_loader_expansion_created",
        "no_real_ingestion_created",
        "no_runtime_data_access",
        "no_source_fetching",
        "static_closeout_only",
    },
    "next gate category": {
        "hold",
        "targeted_static_ingestion_skeleton_refinement_if_gap_found",
        "active_state_update_if_needed",
        "real_ingestion_approval_request_if_chosen",
        "provider_connector_planning_approval_request_if_chosen",
        "source_fetching_planning_approval_request_if_chosen",
        "scoring_backtesting_planning_approval_request_if_chosen",
        "runtime_observation_planning_approval_request_if_chosen",
        "trading_order_autonomy_later_explicit_approval_only",
    },
    "non-approval category": {
        "real_ingestion",
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
    "socket" + ".",
    "sub" + "process.",
    "url" + "open",
    "write_" + "text",
    "write_" + "bytes",
    "touch" + "(",
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
        "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-01",
        "PRD-P1-WX-STAGE2-INGESTION-IMPLEMENTATION-APPROVAL-01",
        "PRD-P1-WX-STAGE2-INGESTION-PLAN-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-INGESTION-PLAN-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01",
        "MEG-OPS-WX-ACTIVE-STATE-05",
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


def test_expected_artifacts_exist() -> None:
    assert MODULE_PATH.is_file()
    assert IMPLEMENTATION_TEST_PATH.is_file()
    assert IMPLEMENTATION_PRD_PATH.is_file()


def test_implementation_inventory_lists_exactly_expected_artifacts() -> None:
    inventory = _section(_prd_text(), INVENTORY_HEADING)
    observed = [
        line.removeprefix("- `").removesuffix("`")
        for line in inventory.splitlines()
        if line.startswith("- `")
    ]
    assert observed == EXPECTED_INVENTORY


def test_closeout_scope_and_static_completion_language_are_present() -> None:
    text = _prd_text()
    lower_text = text.lower()
    for required in (
        "This is static ingestion boundary skeleton implementation closeout/checkpoint only.",
        "Static ingestion boundary skeleton v1 is complete for now.",
        "recommended posture is hold/checkpoint unless a concrete static ingestion skeleton gap is found",
        "does not create, approve, or imply any real ingestion",
    ):
        assert required in text or required.lower() in lower_text


def test_source_module_boundary_language_is_present() -> None:
    text = _prd_text()
    for required in (
        "`meg/weather/stage2/ingestion_boundary.py` exists",
        "validates caller-supplied already-human-reviewed descriptor mappings only",
        "uses closed vocabularies",
        "returns pass, caution, or blocked validation results",
        "It is stdlib-only",
        "The source module does not read files.",
        "The source module does not write files.",
        "The source module does not call services.",
        "The source module does not open network connections.",
        "The source module does not load credentials/secrets/config.",
        "The source module does not create schemas or start jobs.",
    ):
        assert required in text


def test_non_approval_and_unbuilt_scope_language_is_present() -> None:
    text = _prd_text()
    for required in (
        "no real ingestion was created",
        "no provider/API connectors were created",
        "no source fetching was created",
        "no external API calls were created",
        "no credentials/secrets/config loading was created",
        "no forecast pulls were created",
        "no scraping/polling/streaming/scheduling/queues/jobs were created",
        "no scoring/probability scoring was created",
        "no backtesting/paper simulation was created",
        "no runtime observation was created",
        "no trading/order placement/position sizing/autonomy was created",
        "no production behavior was created",
        "no C++/Rust runtime components were created",
        "no loader expansion was created",
        "no fixture JSON/README files were created or modified",
        "no historical-label data/generated data was created",
    ):
        assert required in text


def test_future_gates_and_readiness_disclaimers_are_present() -> None:
    text = _prd_text()
    lower_text = text.lower()
    for required in (
        "Future real ingestion requires later separate approval.",
        "Future provider/API connector implementation requires later separate approval.",
        "Future source fetching requires later separate approval.",
        "Future scoring/backtesting requires later separate approval.",
        "Future runtime/trading requires later separate approval.",
        "This implementation does not imply ingestion readiness, provider readiness, source readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.",
    ):
        assert required in text or required.lower() in lower_text


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


def test_new_files_contain_no_forbidden_implementation_fragments() -> None:
    for path in (PRD_PATH, THIS_TEST_PATH):
        text = path.read_text(encoding="utf-8")
        for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS:
            assert fragment not in text, (path, fragment)


def test_source_module_contains_no_forbidden_implementation_fragments() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    offenders = [fragment for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS if fragment.lower() in source.lower()]
    assert offenders == []


def test_source_module_exposes_required_dataclasses_and_functions() -> None:
    module = importlib.import_module("meg.weather.stage2.ingestion_boundary")
    for name in (
        "StaticIngestionSourceDescriptor",
        "StaticIngestionValidationResult",
        "static_ingestion_source_descriptor_from_mapping",
        "validate_static_ingestion_source_descriptor",
        "validate_static_ingestion_source_mapping",
    ):
        assert hasattr(module, name)
    assert module.VALIDATION_SEVERITIES == {"pass", "caution", "blocked"}


def test_static_test_uses_python_standard_library_only() -> None:
    assert _source_import_roots(THIS_TEST_PATH) <= {"ast", "importlib", "pathlib"}
