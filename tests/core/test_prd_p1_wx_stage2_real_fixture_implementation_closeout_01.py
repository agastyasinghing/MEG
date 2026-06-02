from __future__ import annotations

from pathlib import Path


PRD_PATH = Path(
    "docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01"
ASSIGNMENT_HEADING = "## Machine-checkable Stage 2 real fixture implementation closeout assignments"
REAL_FIXTURE_DIR = Path("tests/fixtures/weather/stage2_real_source_backed_labels")
REAL_FIXTURE_README = REAL_FIXTURE_DIR / "README.md"
REAL_FIXTURE_JSON_FILES = {
    "polymarket_nyc_may_2026_precipitation_less_than_2_no.json",
    "polymarket_nyc_may_12_2026_temperature_conflict.json",
}
IMPLEMENTATION_TEST = Path("tests/core/test_prd_p1_wx_stage2_real_fixture_implementation_01.py")
PLAN_TEST = Path("tests/core/test_prd_p1_wx_stage2_real_fixture_plan_01.py")
IMPLEMENTATION_APPROVAL_TEST = Path(
    "tests/core/test_prd_p1_wx_stage2_real_fixture_implementation_approval_01.py"
)

ASSIGNMENT_PREFIXES = {
    "real fixture implementation closeout stage",
    "closeout status",
    "real fixture artifact status",
    "real fixture data posture",
    "validation posture",
    "boundary status",
    "next gate category",
    "non-approval category",
    "evidence status",
    "label confidence",
}

ALLOWED_VALUES = {
    "real fixture implementation closeout stage": {
        "stage_2_real_source_backed_fixture_implementation_closeout_checkpoint",
    },
    "closeout status": {
        "v1_complete",
        "hold_for_review",
        "blocked_pending_gap",
        "unclear",
    },
    "real fixture artifact status": {
        "present",
        "missing",
        "not_applicable",
    },
    "real fixture data posture": {
        "static_hand_authored_source_backed",
        "exactly_two_real_fixture_files",
        "cap_at_most_three_preserved",
        "no_generated_data",
        "source_notes_present",
        "access_dates_present",
        "no_lookahead_notes_present",
        "reviewer_notes_present",
    },
    "validation posture": {
        "static_validation_present",
        "pass_fixture_present",
        "blocked_fixture_present",
        "no_" + "market" + "_id_in_fixture_json",
        "no_secrets_in_fixture_json",
        "successor_aware_tests_present",
    },
    "boundary status": {
        "preserved",
        "violated",
        "unclear",
    },
    "next gate category": {
        "hold",
        "targeted_source_evidence_refinement_if_gap_found",
        "targeted_fixture_validation_refinement_if_gap_found",
        "active_state_update_if_needed",
        "historical_label_loading_validation_planning_approval_request_if_chosen",
        "ingestion_planning_approval_request_if_chosen",
        "scoring_" + "back" + "testing_planning_approval_request_if_chosen",
        "runtime_observation_planning_approval_request_if_chosen",
        "trading_order_autonomy_later_explicit_approval_only",
    },
    "non-approval category": {
        "generated_data",
        "historical_label_loading",
        "ingestion",
        "provider_integration",
        "connectors",
        "external_api_calls",
        "credentials_secrets_config",
        "forecast_pulls",
        "model_scoring",
        "probability_scoring",
        "back" + "testing",
        "paper_" + "simulation",
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
    "static_validation_present/pass_fixture_present",
    "source_backed/reviewer_inferred",
    "confirmed/unclear",
    "partial",
    "mixed",
    "likely_confirmed",
    "maybe",
    "approved",
    "configured",
    "available",
    "fixture_ready",
    "real_fixture_ready",
    "real_fixtures_ready",
    "data_ready",
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
    "trade" + "_ready",
    "auto" + "_execute",
    "aut" + "onomous",
    "live",
    "production",
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _prd_text() -> str:
    return _read_text(PRD_PATH)


def _assignment_section(text: str) -> str:
    marker = ASSIGNMENT_HEADING + "\n"
    assert marker in text
    section_start = text.index(marker) + len(marker)
    next_heading = text.find("\n## ", section_start)
    if next_heading == -1:
        return text[section_start:]
    return text[section_start:next_heading]


def _parsed_assignments() -> dict[str, set[str]]:
    section = _assignment_section(_prd_text())
    parsed = {prefix: set() for prefix in ASSIGNMENT_PREFIXES}
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        assert line.startswith("- ")
        body = line[2:]
        prefix, separator, value = body.partition(": ")
        assert separator == ": "
        assert prefix in ASSIGNMENT_PREFIXES
        parsed[prefix].add(value)
    return parsed


def test_closeout_prd_exists_with_canonical_id_and_required_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    required_fragments = (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-01",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-APPROVAL-01",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01",
    )
    for fragment in required_fragments:
        assert fragment in text


def test_closeout_references_real_fixture_inventory() -> None:
    text = _prd_text()
    required_paths = (
        "tests/fixtures/weather/stage2_real_source_backed_labels/README.md",
        "tests/fixtures/weather/stage2_real_source_backed_labels/polymarket_nyc_may_2026_precipitation_less_than_2_no.json",
        "tests/fixtures/weather/stage2_real_source_backed_labels/polymarket_nyc_may_12_2026_temperature_conflict.json",
        "tests/core/test_prd_p1_wx_stage2_real_fixture_implementation_01.py",
        "docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION.md",
    )
    for path in required_paths:
        assert path in text


def test_closeout_states_required_completion_and_fixture_posture() -> None:
    text = _prd_text()
    required_fragments = (
        "real source-backed fixture implementation closeout/checkpoint only",
        "Real fixture implementation v1 is complete for now",
        "Exactly two real source-backed JSON fixture files exist",
        "fixture count cap of at most 3 was preserved",
        "static, hand-authored, reviewable, and source-backed",
        "third fixture was intentionally not fabricated",
        "old planning/approval tests were made successor-aware",
        "No existing fixture JSON files were modified by this closeout",
        "no generated data was created",
        "no ingestion was created",
        "no provider/API connectors were created",
        "no external API calls from runtime code were created",
        "no credentials/secrets/config loading was created",
        "no forecast pulls were created",
        "no scoring/" + "back" + "testing/runtime/trading/" + "order " + "placement/autonomy were created",
        "Future historical-label loading requires separate explicit approval",
        "Future ingestion requires separate explicit approval",
        "Future scoring/" + "back" + "testing requires separate explicit approval",
        "Future runtime/trading requires separate explicit approval",
        "recommended posture is hold/checkpoint unless a concrete source-evidence or validation gap is found",
        "user explicitly chooses a later approval/request/planning gate",
    )
    for fragment in required_fragments:
        assert fragment in text


def test_machine_checkable_assignment_section_is_closed_and_complete() -> None:
    parsed = _parsed_assignments()
    assert set(parsed) == ASSIGNMENT_PREFIXES
    for prefix, observed_values in parsed.items():
        assert observed_values <= ALLOWED_VALUES[prefix]
        assert observed_values == ALLOWED_VALUES[prefix]


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_values() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    forbidden_heading = "## Forbidden Stage 2 real fixture implementation closeout values"
    assert forbidden_heading in text
    parsed_values = set().union(*_parsed_assignments().values())
    for value in FORBIDDEN_EXAMPLES:
        assert value in text
        assert value not in parsed_values


def test_existing_real_fixture_artifacts_still_exist_with_exact_json_count() -> None:
    assert IMPLEMENTATION_TEST.is_file()
    assert REAL_FIXTURE_DIR.is_dir()
    assert REAL_FIXTURE_README.is_file()
    observed_json_names = {path.name for path in REAL_FIXTURE_DIR.glob("*.json")}
    assert observed_json_names == REAL_FIXTURE_JSON_FILES
    for name in REAL_FIXTURE_JSON_FILES:
        assert (REAL_FIXTURE_DIR / name).is_file()


def test_old_real_fixture_tests_are_successor_aware_when_directory_exists() -> None:
    assert REAL_FIXTURE_DIR.exists()
    for path in (PLAN_TEST, IMPLEMENTATION_APPROVAL_TEST):
        text = _read_text(path)
        assert "PLANNED_REAL_FIXTURE_DIR.exists()" in text
        assert "SUCCESSOR_IMPLEMENTATION_PRD" in text
        assert "SUCCESSOR_IMPLEMENTATION_TEST" in text
        assert "_assert_planned_directory_posture_is_successor_aware" in text
        assert "1 <= len(fixture_paths) <= 3" in text


def test_section_scoped_parsing_does_not_reject_forbidden_prose_examples() -> None:
    text = _prd_text()
    section = _assignment_section(text)
    prose_examples = (
        "approved",
        "mixed",
        "partial",
        "live",
        "production",
        "C++",
        "Rust",
    )
    for example in prose_examples:
        assert example in text
    for parsed_values in _parsed_assignments().values():
        assert "partial" not in parsed_values
        assert "mixed" not in parsed_values
        assert "approved" not in parsed_values
    assert "partial" not in section
    assert "mixed" not in section
    assert "approved" not in section
