from __future__ import annotations

from pathlib import Path


PRD_PATH = Path(
    "docs/prd/PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_STATIC_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01"
FIXTURE_DIR = Path("tests/fixtures/weather/stage2_historical_labels")
IMPLEMENTATION_TEST_PATH = Path("tests/core/test_prd_p1_wx_stage2_fixture_implementation_01.py")
LEGACY_ID = "market" + "_id"

FIXTURE_JSON_FILES = {
    "synthetic_valid_source_backed_confirmed.json",
    "synthetic_blocked_missing_provenance.json",
    "synthetic_unclear_requires_adjudication.json",
}

ASSIGNMENT_HEADING = "## Machine-checkable Stage 2 fixture implementation closeout assignments"
ASSIGNMENT_PREFIXES = {
    "fixture implementation closeout stage",
    "closeout status",
    "fixture artifact status",
    "fixture data posture",
    "validation posture",
    "boundary status",
    "next gate category",
    "non-approval category",
    "evidence status",
    "label confidence",
}

ALLOWED_VALUES = {
    "fixture implementation closeout stage": {
        "stage_2_static_fixture_implementation_closeout_checkpoint",
    },
    "closeout status": {
        "v1_complete",
        "hold_for_review",
        "blocked_pending_gap",
        "unclear",
    },
    "fixture artifact status": {
        "present",
        "missing",
        "not_applicable",
    },
    "fixture data posture": {
        "static_synthetic_hand_authored",
        "no_real_historical_label_data",
        "no_generated_data",
        "no_extra_fixture_files",
        "provenance_notes_present",
        "no_lookahead_notes_present",
        "reviewer_notes_present",
    },
    "validation posture": {
        "static_validation_present",
        "valid_fixture_passes",
        "blocked_fixture_does_not_pass",
        "unclear_fixture_does_not_pass",
        "no_" + LEGACY_ID + "_in_fixture_json",
        "no_provider_urls_in_fixture_json",
    },
    "boundary status": {
        "preserved",
        "violated",
        "unclear",
    },
    "next gate category": {
        "hold",
        "targeted_fixture_validation_refinement_if_gap_found",
        "real_source_backed_fixture_approval_request_if_chosen",
        "historical_label_loading_validation_planning_approval_request_if_chosen",
        "ingestion_planning_approval_request_if_chosen",
        "scoring_" + "back" + "testing_planning_approval_request_if_chosen",
        "runtime_observation_planning_approval_request_if_chosen",
        "trading_order_autonomy_later_explicit_approval_only",
    },
    "non-approval category": {
        "real_historical_label_data",
        "generated_data",
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
    "static_validation_present/valid_fixture_passes",
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
    "fixtures_ready",
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
    "back" + "test",
    "paper " + "simulation",
    "order " + "placement",
    "auto" + "_execute",
    "aut" + "onomous",
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


def test_closeout_prd_exists_with_canonical_id_and_source_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()

    required_fragments = (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-APPROVAL-01",
        "PRD-P1-WX-STAGE2-FIXTURE-PLAN-01",
    )
    for fragment in required_fragments:
        assert fragment in text


def test_closeout_references_fixture_inventory_and_existing_assets() -> None:
    text = _prd_text()
    required_paths = {
        "tests/fixtures/weather/stage2_historical_labels/README.md",
        "tests/fixtures/weather/stage2_historical_labels/synthetic_valid_source_backed_confirmed.json",
        "tests/fixtures/weather/stage2_historical_labels/synthetic_blocked_missing_provenance.json",
        "tests/fixtures/weather/stage2_historical_labels/synthetic_unclear_requires_adjudication.json",
        "tests/core/test_prd_p1_wx_stage2_fixture_implementation_01.py",
        "docs/prd/PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-01_STATIC_HISTORICAL_LABEL_FIXTURE_IMPLEMENTATION.md",
    }
    for path in required_paths:
        assert path in text

    assert IMPLEMENTATION_TEST_PATH.is_file()
    assert {path.name for path in FIXTURE_DIR.glob("*.json")} == FIXTURE_JSON_FILES


def test_closeout_required_scope_and_non_approval_wording() -> None:
    text = _prd_text()
    required_phrases = (
        "This is a static fixture implementation closeout/checkpoint only",
        "Fixture implementation v1 is complete for now",
        "Exactly three JSON fixture files exist in `tests/fixtures/weather/stage2_historical_labels/`",
        "fixtures are static, synthetic, hand-authored examples",
        "no real historical-label data was created",
        "no generated data was created",
        "no ingestion was created",
        "no provider/API connectors were created",
        "no external API calls were created",
        "no credentials/secrets/config loading was created",
        "no forecast pulls were created",
        "no scoring/" + "back" + "testing/runtime/trading/order " + "placement/autonomy were created",
        "Fixture implementation does not imply ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness",
        "Future ingestion/loading requires separate explicit approval",
        "Future scoring/" + "back" + "testing requires separate explicit approval",
        "Future runtime/trading requires separate explicit approval",
        "Future real source-backed historical-label fixtures, if ever desired, require separate approval and provenance review",
        "The recommended posture is hold/checkpoint unless a concrete fixture validation gap is found or the user explicitly chooses the next gate",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_machine_checkable_assignment_section_uses_only_closed_sets() -> None:
    parsed = _parsed_assignments()
    assert set(parsed) == set(ALLOWED_VALUES)
    for category, values in parsed.items():
        assert values <= ALLOWED_VALUES[category]


def test_machine_checkable_assignment_section_contains_every_allowed_value() -> None:
    parsed = _parsed_assignments()
    for category, values in ALLOWED_VALUES.items():
        assert parsed[category] == values


def test_forbidden_examples_are_documented_but_not_actual_assignments() -> None:
    text = _prd_text()
    section = _assignment_section(text)

    assert "## Forbidden Stage 2 fixture implementation closeout values" in text
    for example in FORBIDDEN_EXAMPLES:
        assert example in text
        assert f": {example}\n" not in section


def test_section_scoped_parsing_does_not_reject_forbidden_prose_examples() -> None:
    text = _prd_text()
    assert "partial" in text
    assert "mixed" in text
    assert "approved" in text
    assert "live" in text
    assert "production" in text
    assert "C++/Rust" in text
    assert _parsed_assignments()


def test_new_test_remains_static_and_avoids_implementation_behavior() -> None:
    text = Path(__file__).read_text(encoding="utf-8")
    assert "Path" in text
    for fragment in FORBIDDEN_IMPLEMENTATION_FRAGMENTS:
        assert fragment not in text
