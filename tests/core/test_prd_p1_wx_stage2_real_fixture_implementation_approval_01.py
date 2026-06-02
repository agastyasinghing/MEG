from __future__ import annotations

from pathlib import Path


PRD_PATH = Path(
    "docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-APPROVAL-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION_APPROVAL_REQUEST.md"
)
PLANNED_REAL_FIXTURE_DIR = Path("tests/fixtures/weather/stage2_real_source_backed_labels")
SUCCESSOR_IMPLEMENTATION_PRD = Path(
    "docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION.md"
)
SUCCESSOR_IMPLEMENTATION_TEST = Path(
    "tests/core/test_prd_p1_wx_stage2_real_fixture_implementation_01.py"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-APPROVAL-01"
ASSIGNMENT_HEADING = "## Machine-checkable Stage 2 real-fixture implementation approval-request assignments"
ASSIGNMENT_PREFIXES = {
    "real fixture implementation approval stage",
    "request status",
    "requested future implementation scope",
    "approval boundary status",
    "future ticket permission",
    "fixture data posture",
    "non-approval category",
    "evidence status",
    "label confidence",
}

ALLOWED_VALUES = {
    "real fixture implementation approval stage": {
        "stage_2_real_source_backed_fixture_implementation_approval_request",
    },
    "request status": {
        "request_prepared",
        "implementation_not_approved",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "requested future implementation scope": {
        "real_fixture_files_only_if_later_approved",
        "create_real_fixture_directory_if_later_approved",
        "at_most_3_real_fixture_candidates",
        "source_backed_candidates_only",
        "provenance_notes_required",
        "access_date_required",
        "venue_rule_reference_required",
        "resolver_source_identity_required",
        "no_lookahead_notes_required",
        "reviewer_adjudication_notes_required",
        "static_validation_only",
        "no_ingestion_no_runtime_no_scoring",
    },
    "approval boundary status": {
        "not_approved",
        "separate_human_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future ticket permission": {
        "may_request_real_fixture_implementation_ticket",
        "must_not_create_real_fixtures_now",
        "must_not_create_ingestion",
        "must_not_create_runtime",
        "must_not_create_scoring",
        "must_not_create_trading",
        "blocked_until_human_decision",
    },
    "fixture data posture": {
        "no_real_fixture_data_created",
        "no_historical_label_data_created",
        "no_generated_data_created",
        "existing_synthetic_fixtures_unchanged",
        "planned_real_fixture_directory_not_created",
        "source_backing_required_before_real_use",
        "review_required_before_real_use",
        "no_lookahead_required_before_real_use",
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
    "request_prepared/implementation_not_approved",
    "not_approved/separate_human_approval_required",
    "source_backed/reviewer_inferred",
    "confirmed/unclear",
    "partial",
    "mixed",
    "likely_confirmed",
    "maybe",
    "approved",
    "configured",
    "available",
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
    "approved_for_real_fixtures",
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
    "trade" + "_ready",
    "auto" + "_execute",
    "aut" + "onomous",
)


def _assert_planned_directory_posture_is_successor_aware() -> None:
    if not PLANNED_REAL_FIXTURE_DIR.exists():
        return

    assert SUCCESSOR_IMPLEMENTATION_PRD.is_file()
    assert SUCCESSOR_IMPLEMENTATION_TEST.is_file()
    assert (PLANNED_REAL_FIXTURE_DIR / "README.md").is_file()
    fixture_paths = sorted(PLANNED_REAL_FIXTURE_DIR.glob("*.json"))
    assert 1 <= len(fixture_paths) <= 3


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


def test_prd_exists_with_canonical_id_and_required_references() -> None:
    assert PRD_PATH.is_file()
    text = _prd_text()
    required_fragments = (
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "MEG_ACTIVE_STATE",
        "WEATHER_BOT_PACKET",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01",
        "PRD-P1-WX-STAGE2-REAL-FIXTURE-APPROVAL-01",
        "PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01",
    )
    for fragment in required_fragments:
        assert fragment in text


def test_required_sections_are_present() -> None:
    text = _prd_text()
    required_headings = (
        "## Status and scope",
        "## Strategic framing",
        "## Stage ladder position",
        "## Real source-backed fixture implementation approval-request boundary",
        "## Dependency on real source-backed fixture planning",
        "## Why real source-backed fixture implementation may be useful later",
        "## Requested future implementation scope",
        "## Explicitly excluded scope",
        "## Human approval checklist",
        "## Approval decision options",
        "## Implementation risk controls",
        "## Source/provenance prerequisites",
        "## No-lookahead prerequisites",
        "## Reviewer/adjudication prerequisites",
        "## Fixture count cap",
        "## Future directory/file allowlist",
        "## Relationship to historical-label loading",
        "## Relationship to ingestion",
        "## Relationship to scoring/" + "back" + "testing",
        "## Relationship to runtime/trading",
        "## Explicit non-approval boundaries",
        "## Closed Stage 2 real-fixture implementation approval-request vocabulary",
        "## Forbidden Stage 2 real-fixture implementation approval-request values",
        ASSIGNMENT_HEADING,
        "## Later-ticket handoff",
        "## Acceptance criteria",
    )
    for heading in required_headings:
        assert heading in text


def test_required_scope_and_non_approval_wording() -> None:
    text = _prd_text()
    required_phrases = (
        "This is a real source-backed fixture implementation approval request only",
        "Real source-backed fixture implementation is not approved by this document",
        "Real source-backed fixture files are not created",
        "Real historical-label data is not created",
        "Generated data is not created",
        "Existing synthetic fixture files are not modified",
        "The planned real-fixture directory is not created",
        "Ingestion is not created",
        "Provider/API connectors are not created",
        "External API calls are not created",
        "Credentials/secrets/config loading is not created",
        "Forecast pulls are not created",
        "Scoring/" + "back" + "testing/runtime/trading/order " + "placement/autonomy remain unapproved",
        "Historical-label loading remains separate and unapproved",
        "A later real source-backed fixture implementation ticket requires separate explicit human approval",
        "Any future real source-backed fixture must satisfy `PRD-P1-WX-STAGE2-REAL-FIXTURE-PLAN-01` planning requirements",
        "Any future real source-backed fixture must be source-backed, reviewable, and no-lookahead safe",
        "does not imply historical-label loading readiness, ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_future_implementation_scope_and_prerequisites_are_described() -> None:
    text = _prd_text()
    required_fragments = (
        "creating the planned directory: `tests/fixtures/weather/stage2_real_source_backed_labels/`",
        "creating at most 3 real source-backed fixture JSON files",
        "creating a README for the real-fixture directory",
        "source identity",
        "source name",
        "source URL or stable source locator",
        "access date",
        "venue rule reference",
        "resolver source identity",
        "point-in-time availability notes",
        "no-lookahead notes",
        "reviewer/adjudication notes",
        "conflicting-source notes when applicable",
        "expected validation posture",
        "non-approval notes",
        "static validation tests only",
        "avoiding any production/runtime loader",
    )
    for fragment in required_fragments:
        assert fragment in text


def test_future_scope_does_not_request_disallowed_capabilities() -> None:
    text = _prd_text()
    required_fragments = (
        "must not ask for permission to fetch or scrape data",
        "call providers",
        "pull forecasts",
        "ingest live or historical data",
        "score probabilities",
        "run any historical performance evaluation",
        "run paper-only execution rehearsal",
        "run runtime observation",
        "trade",
        "place orders",
        "independent execution authority",
    )
    for fragment in required_fragments:
        assert fragment in text


def test_fixture_count_cap_and_directory_posture_are_enforced() -> None:
    text = _prd_text()
    assert "at most 3 real source-backed fixture candidates" in text
    assert "Any larger fixture set requires a separate expansion approval request" in text
    assert "planned directory `tests/fixtures/weather/stage2_real_source_backed_labels/`" in text
    _assert_planned_directory_posture_is_successor_aware()


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
    assert "## Forbidden Stage 2 real-fixture implementation approval-request values" in text
    for example in FORBIDDEN_EXAMPLES:
        assert example in text
        assert f": {example}\n" not in section


def test_section_scoped_parsing_allows_forbidden_prose_examples() -> None:
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
