"""Static tests for the Stage 2 historical-label loading implementation closeout."""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01"
PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-CLOSEOUT-01_STATIC_HISTORICAL_LABEL_LOADING_VALIDATION_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md"
LOADER_PATH = REPO_ROOT / "meg/weather/stage2/historical_label_loader.py"
VALIDATOR_PATH = REPO_ROOT / "meg/weather/stage2/historical_label.py"
IMPLEMENTATION_TEST_PATH = REPO_ROOT / "tests/core/test_prd_p1_wx_stage2_historical_label_loading_implementation_01.py"
IMPLEMENTATION_PRD_PATH = REPO_ROOT / "docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01_STATIC_HISTORICAL_LABEL_LOADING_VALIDATION_IMPLEMENTATION.md"
SYNTHETIC_DIR = REPO_ROOT / "tests/fixtures/weather/stage2_historical_labels"
REAL_DIR = REPO_ROOT / "tests/fixtures/weather/stage2_real_source_backed_labels"
ASSIGNMENT_HEADING = "## Machine-checkable historical-label loading implementation closeout assignments"

SYNTHETIC_FIXTURE_FILES = {
    "synthetic_blocked_missing_provenance.json",
    "synthetic_unclear_requires_adjudication.json",
    "synthetic_valid_source_backed_confirmed.json",
}
REAL_FIXTURE_FILES = {
    "polymarket_nyc_may_12_2026_temperature_conflict.json",
    "polymarket_nyc_may_2026_precipitation_less_than_2_no.json",
}

ALLOWED_ASSIGNMENTS = {
    "historical label loading implementation closeout stage": {
        "stage_2_static_historical_label_loading_validation_implementation_closeout_checkpoint",
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
    "loader boundary status": {
        "preserved",
        "violated",
        "unclear",
    },
    "implemented contract coverage": {
        "static_loader_module_present",
        "explicit_repo_root_required",
        "allowlisted_fixture_directory_reads_only",
        "nonrecursive_directory_loading",
        "fixture_json_parse_via_read_text_and_json_loads",
        "stage2_metadata_validator_reused",
        "expected_observed_posture_match_required",
        "fail_closed_negative_cases_tested",
        "no_network_no_env_no_writes",
    },
    "fixture coverage": {
        "three_synthetic_fixtures_load",
        "two_real_source_backed_fixtures_load",
        "fixture_hashes_pinned",
        "fixture_files_unchanged",
        "fixture_readmes_unchanged",
    },
    "data posture": {
        "no_fixture_files_created",
        "no_fixture_files_modified",
        "no_historical_label_data_created",
        "no_generated_data_created",
        "no_runtime_data_access",
        "no_source_fetching",
        "static_validation_only",
    },
    "next gate category": {
        "hold",
        "targeted_loader_validation_refinement_if_gap_found",
        "active_state_update_if_needed",
        "ingestion_planning_approval_request_if_chosen",
        "provider_connector_planning_approval_request_if_chosen",
        "scoring_backtesting_planning_approval_request_if_chosen",
        "runtime_observation_planning_approval_request_if_chosen",
        "trading_order_autonomy_later_explicit_approval_only",
    },
    "non-approval category": {
        "ingestion",
        "provider_integration",
        "connectors",
        "external_api_calls",
        "credentials_secrets_config",
        "forecast_pulls",
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
    "label confidence": {
        "confirmed",
        "unclear",
        "unknown",
    },
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
    "scoring_ready",
    "runtime_ready",
    "trading_ready",
    "production_ready",
    "provider_ready",
    "model_ready",
    "back" + "test_ready",
    "ready_for_ingestion",
    "ready_for_scoring",
    "ready_for_runtime",
    "ready_for_trading",
    "approved_for_ingestion",
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


def _assignment_section(text: str) -> str:
    marker = ASSIGNMENT_HEADING + "\n"
    assert marker in text
    section_start = text.index(marker) + len(marker)
    next_heading = text.find("\n## ", section_start)
    if next_heading == -1:
        return text[section_start:]
    return text[section_start:next_heading]


def _section(text: str, heading: str) -> str:
    marker = "## " + heading + "\n"
    assert marker in text
    section_start = text.index(marker) + len(marker)
    next_heading = text.find("\n## ", section_start)
    assert next_heading != -1
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


def _source_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    import_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            import_roots.add(node.module.split(".")[0])
    return import_roots


def test_closeout_prd_exists_with_canonical_id_and_required_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    for required in (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-APPROVAL-01",
        "PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-PLAN-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
        "Stage 2 skeleton closeout",
    ):
        assert required in text


def test_required_sections_exist() -> None:
    text = _prd_text()
    required_headings = (
        "Status and scope",
        "Strategic framing",
        "Stage ladder position",
        "Implementation inventory",
        "Loader boundary summary",
        "Implemented public API summary",
        "Allowlisted fixture directory summary",
        "Fail-closed behavior summary",
        "Synthetic fixture validation summary",
        "Real source-backed fixture validation summary",
        "Fixture immutability confirmation",
        "Relationship to Stage 2 metadata validator",
        "Static validation test summary",
        "What this closeout confirms",
        "What remains unbuilt",
        "Explicit non-approval boundaries",
        "Future gates",
        "Recommended hold/checkpoint posture",
        "Allowed future next-step categories",
        "Forbidden future next-step categories",
        "Closed historical-label loading implementation closeout vocabulary",
        "Forbidden historical-label loading implementation closeout values",
        "Machine-checkable historical-label loading implementation closeout assignments",
        "Acceptance criteria",
        "Later-ticket handoff",
    )
    for heading in required_headings:
        assert "## " + heading in text


def test_implementation_inventory_lists_exactly_required_artifacts() -> None:
    observed = [line.strip() for line in _section(_prd_text(), "Implementation inventory").splitlines() if line.strip()]
    assert observed == [
        "- meg/weather/stage2/historical_label_loader.py",
        "- tests/core/test_prd_p1_wx_stage2_historical_label_loading_implementation_01.py",
        "- docs/prd/PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01_STATIC_HISTORICAL_LABEL_LOADING_VALIDATION_IMPLEMENTATION.md",
    ]


def test_closeout_scope_completion_loader_boundary_and_fail_closed_language() -> None:
    text = _prd_text()
    required_phrases = (
        "This is a static historical-label loading/validation implementation closeout/checkpoint only",
        "Static historical-label loading/validation implementation v1 is complete for now",
        "meg/weather/stage2/historical_label_loader.py` exists",
        "historical_label_loader.py` is limited to explicit static fixture validation",
        "The loader reads only caller-supplied paths under the two allowlisted fixture directories",
        "The directory loader is non-recursive",
        "The loader reuses `historical_label_metadata_from_mapping` and `validate_historical_label_metadata`",
        "The loader fails closed for missing files, malformed JSON, non-object JSON, missing fields, unexpected closed-set values, non-allowlisted paths, empty directories, and posture mismatches",
        "All three synthetic fixtures load through the static loader",
        "Both real source-backed fixtures load through the static loader",
        "Fixture README/JSON files were not created or modified",
        "No historical-label data files or generated data were created",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_existing_implementation_artifacts_and_fixture_files_exist() -> None:
    assert LOADER_PATH.is_file()
    assert VALIDATOR_PATH.is_file()
    assert IMPLEMENTATION_TEST_PATH.is_file()
    assert IMPLEMENTATION_PRD_PATH.is_file()
    assert (SYNTHETIC_DIR / "README.md").is_file()
    assert (REAL_DIR / "README.md").is_file()
    assert {path.name for path in SYNTHETIC_DIR.glob("*.json")} == SYNTHETIC_FIXTURE_FILES
    assert {path.name for path in REAL_DIR.glob("*.json")} == REAL_FIXTURE_FILES


def test_loader_source_still_avoids_forbidden_fragments_except_static_parse() -> None:
    source_text = LOADER_PATH.read_text(encoding="utf-8")
    allowed_static_parse_fragment = "json." + "loads"
    blocked = [
        fragment
        for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS
        if fragment in source_text and fragment != "json." + "load"
    ]
    assert allowed_static_parse_fragment in source_text
    assert blocked == []


def test_loader_source_import_boundary_is_standard_library_plus_existing_validator() -> None:
    assert _source_import_roots(LOADER_PATH) <= {"__future__", "dataclasses", "json", "pathlib", "typing", "meg"}


def test_loader_implementation_test_still_pins_fixtures_and_exercises_loader() -> None:
    test_text = IMPLEMENTATION_TEST_PATH.read_text(encoding="utf-8")
    for required in (
        "EXPECTED_FIXTURE_HASHES",
        "tests/fixtures/weather/stage2_historical_labels/README.md",
        "tests/fixtures/weather/stage2_real_source_backed_labels/README.md",
        "test_loader_reads_all_synthetic_fixtures",
        "test_loader_reads_both_real_source_backed_fixtures",
        "test_loaded_fixtures_include_expected_fields_and_matching_postures",
        "test_non_allowlisted_missing_and_non_json_paths_fail_closed",
        "test_malformed_and_non_object_json_fail_closed",
        "test_missing_required_and_unexpected_closed_values_fail_closed",
        "test_directory_loader_fails_closed_for_non_allowlisted_empty_and_nonrecursive_dirs",
        "expected_posture_path",
    ):
        assert required in test_text
    for fixture_name in sorted(SYNTHETIC_FIXTURE_FILES | REAL_FIXTURE_FILES):
        assert fixture_name in test_text


def test_required_non_approval_and_future_approval_language() -> None:
    text = _prd_text()
    required_phrases = (
        "No ingestion was created or approved",
        "No provider/API connectors were created or approved",
        "No external API calls were created or approved",
        "No credentials/secrets/config loading was created or approved",
        "No forecast pulls were created or approved",
        "No scoring/probability scoring was created or approved",
        "No backtesting/paper simulation was created or approved",
        "No runtime observation was created or approved",
        "No trading/order placement/position sizing/autonomy was created or approved",
        "No production behavior was created or approved",
        "No C++/Rust runtime components were created",
        "Future ingestion requires separate explicit approval",
        "Future scoring/backtesting requires separate explicit approval",
        "Future runtime/trading requires separate explicit approval",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_recommended_hold_checkpoint_posture_is_documented() -> None:
    text = _prd_text()
    assert (
        "The recommended posture is hold/checkpoint unless a concrete loader-validation gap is found "
        "or the user explicitly chooses a later approval/request/planning gate"
    ) in text
    assert "Do not recommend ingestion, scoring, backtesting, runtime observation, trading" in text


def test_machine_checkable_assignments_are_section_scoped_and_closed_set() -> None:
    parsed = _parsed_assignments()
    assert parsed == ALLOWED_ASSIGNMENTS


def test_forbidden_examples_are_documented_but_not_parsed_as_assignments() -> None:
    text = _prd_text()
    forbidden_section = _section(text, "Forbidden historical-label loading implementation closeout values")
    for forbidden in FORBIDDEN_EXAMPLES:
        assert "- " + forbidden in forbidden_section

    assignment_values = set().union(*_parsed_assignments().values())
    assert assignment_values.isdisjoint(FORBIDDEN_EXAMPLES)


def test_closeout_prd_and_test_avoid_implementation_fragments() -> None:
    for path in (PRD_PATH, Path(__file__)):
        text = path.read_text(encoding="utf-8")
        blocked = [fragment for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS if fragment in text]
        assert blocked == []
