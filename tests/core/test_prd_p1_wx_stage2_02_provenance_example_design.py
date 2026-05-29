from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-02_POINT_IN_TIME_PROVENANCE_EXAMPLE_DESIGN.md")
STANDALONE_PRD_PATH = Path("docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md")
STAGE1_CLOSEOUT_PATH = Path(
    "docs/prd/PRD-P1-WX-STAGE1-CLOSEOUT-01_STAGE_1_CLOSURE_GATES_AND_STAGE_2_READINESS_REVIEW.md"
)
STAGE2_01_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-01_SOURCE_COMPATIBLE_HISTORICAL_LABEL_DESIGN.md")
CANONICAL_ID = "PRD-P1-WX-STAGE2-02"
MACHINE_HEADING = "## Machine-checkable Stage 2 provenance example assignments"

ALLOWED = {
    "provenance example design stage": {"stage_2_provenance_example_design"},
    "provenance example type": {
        "source_availability",
        "observation_availability",
        "market_timing",
        "archive_revision",
        "station_selection",
        "forecast_publication_time",
        "advisory_publication_time",
        "reviewer_label_time",
        "as_of_join",
        "finality_revision",
        "other_unclear",
    },
    "timestamp role": {
        "decision_time",
        "market_open_time",
        "market_close_time",
        "resolution_time",
        "source_publication_time",
        "observation_valid_time",
        "observation_available_time",
        "archive_revision_time",
        "station_selection_time",
        "reviewer_label_time",
        "not_applicable",
    },
    "point-in-time availability status": {
        "available_as_of",
        "unavailable_as_of",
        "ambiguous_as_of",
        "not_applicable",
        "design_only",
    },
    "leakage risk": {"none_identified", "possible", "likely", "blocking", "unknown"},
    "provenance blocking reason": {
        "none_identified",
        "missing_source_timestamp",
        "missing_observation_availability",
        "missing_archive_revision_record",
        "hindsight_station_selection",
        "final_archive_leakage",
        "future_forecast_cycle",
        "post_resolution_label_leakage",
        "unresolved_source_conflict",
        "other_unclear",
    },
    "label usability posture": {
        "design_only",
        "usable_after_stage_2_approval",
        "blocked_pending_source_match",
        "blocked_pending_provenance",
        "blocked_pending_adjudication",
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

EXPECTED_ASSIGNMENT_LINES = [
    "- provenance example design stage: stage_2_provenance_example_design",
    "- provenance example type: source_availability",
    "- provenance example type: observation_availability",
    "- provenance example type: market_timing",
    "- provenance example type: archive_revision",
    "- provenance example type: station_selection",
    "- provenance example type: forecast_publication_time",
    "- provenance example type: advisory_publication_time",
    "- provenance example type: reviewer_label_time",
    "- provenance example type: as_of_join",
    "- provenance example type: finality_revision",
    "- provenance example type: other_unclear",
    "- timestamp role: decision_time",
    "- timestamp role: market_open_time",
    "- timestamp role: market_close_time",
    "- timestamp role: resolution_time",
    "- timestamp role: source_publication_time",
    "- timestamp role: observation_valid_time",
    "- timestamp role: observation_available_time",
    "- timestamp role: archive_revision_time",
    "- timestamp role: station_selection_time",
    "- timestamp role: reviewer_label_time",
    "- timestamp role: not_applicable",
    "- point-in-time availability status: available_as_of",
    "- point-in-time availability status: unavailable_as_of",
    "- point-in-time availability status: ambiguous_as_of",
    "- point-in-time availability status: not_applicable",
    "- point-in-time availability status: design_only",
    "- leakage risk: none_identified",
    "- leakage risk: possible",
    "- leakage risk: likely",
    "- leakage risk: blocking",
    "- leakage risk: unknown",
    "- provenance blocking reason: none_identified",
    "- provenance blocking reason: missing_source_timestamp",
    "- provenance blocking reason: missing_observation_availability",
    "- provenance blocking reason: missing_archive_revision_record",
    "- provenance blocking reason: hindsight_station_selection",
    "- provenance blocking reason: final_archive_leakage",
    "- provenance blocking reason: future_forecast_cycle",
    "- provenance blocking reason: post_resolution_label_leakage",
    "- provenance blocking reason: unresolved_source_conflict",
    "- provenance blocking reason: other_unclear",
    "- label usability posture: design_only",
    "- label usability posture: usable_after_stage_2_approval",
    "- label usability posture: blocked_pending_source_match",
    "- label usability posture: blocked_pending_provenance",
    "- label usability posture: blocked_pending_adjudication",
    "- evidence status: source_backed",
    "- evidence status: reviewer_inferred",
    "- evidence status: missing",
    "- evidence status: conflicting",
    "- evidence status: not_applicable",
    "- label confidence: confirmed",
    "- label confidence: unclear",
    "- label confidence: unknown",
]


def _text() -> str:
    assert PRD_PATH.exists(), f"Missing PRD file: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    assert text.count(MACHINE_HEADING) == 1, "Expected exactly one machine-checkable section heading"
    start = text.find(MACHINE_HEADING)
    after_heading = text[start + len(MACHINE_HEADING) :]
    next_heading = re.search(r"^##\s+", after_heading, flags=re.MULTILINE)
    return after_heading if next_heading is None else after_heading[: next_heading.start()]


def _parsed_assignments(section: str) -> dict[str, list[str]]:
    parsed = {}
    for field in ALLOWED:
        pattern = rf"^\s*-\s*{re.escape(field)}:\s*([a-z0-9_/-]+)\s*$"
        parsed[field] = [match.group(1) for match in re.finditer(pattern, section, flags=re.MULTILINE)]
    return parsed


def test_required_source_documents_remain_present() -> None:
    required_paths = [STANDALONE_PRD_PATH, STAGE1_CLOSEOUT_PATH, STAGE2_01_PATH]
    missing = [path.as_posix() for path in required_paths if not path.exists()]
    assert not missing, f"Missing required source documents: {missing}"


def test_stage2_02_prd_presence_and_core_terms() -> None:
    text = _text()
    lower = text.lower()
    assert CANONICAL_ID in text

    required = [
        "standalone meg weather bot prd",
        "prd-p1-wx-stage1-closeout-01",
        "prd-p1-wx-stage2-01",
        "stage 2 design",
        "stage 2 point-in-time provenance example design only",
        "point-in-time provenance example design",
        "provenance timestamp model",
        "representative provenance example format",
        "representative synthetic scenario",
        "no-lookahead leakage examples",
        "relationship to stage 2 historical-label design",
        "relationship to stage 3 scoring",
        "language/tooling posture",
        "machine-checkable stage 2 provenance example assignments",
        "non-approval boundaries",
    ]
    missing = [token for token in required if token not in lower]
    assert not missing, f"Missing required planning terms: {missing}"


def test_representative_scenario_count_and_required_types() -> None:
    text = _text().lower()
    scenario_count = len(re.findall(r"^###\s+representative provenance scenario\b", text, flags=re.MULTILINE))
    assert 4 <= scenario_count <= 6

    required_types = {
        "source_availability",
        "observation_availability",
        "archive_revision",
        "station_selection",
    }
    missing = sorted(item for item in required_types if item not in text)
    assert not missing, f"Missing required provenance scenario types: {missing}"


def test_machine_checkable_section_contains_expected_lines() -> None:
    section = _machine_section(_text())
    missing = [line for line in EXPECTED_ASSIGNMENT_LINES if line not in section]
    assert not missing, f"Missing machine-checkable assignment lines: {missing}"


def test_machine_checkable_values_use_closed_sets_only() -> None:
    section = _machine_section(_text())
    parsed = _parsed_assignments(section)

    for field, values in parsed.items():
        assert values, f"No machine-checkable assignments found for {field}"
        invalid = sorted({value for value in values if value not in ALLOWED[field]})
        assert not invalid, f"Invalid parsed values for {field}: {invalid}"
        missing_values = sorted(ALLOWED[field] - set(values))
        assert not missing_values, f"Machine-checkable assignments missing {field} values: {missing_values}"


def test_machine_checkable_validation_is_scoped_to_assignment_section() -> None:
    text = _text().lower()
    section = _machine_section(_text()).lower()

    forbidden_examples = [
        "available_as_of/unavailable_as_of",
        "possible/likely",
        "source_backed/reviewer_inferred",
        "confirmed/unclear",
        "design_only/usable_after_stage_2_approval",
        "missing_source_timestamp/final_archive_leakage",
        "partial",
        "mixed",
        "likely_confirmed",
        "maybe",
        "approved",
        "configured",
        "available",
        "trade_ready",
        "auto_execute",
        "autonomous",
        "live",
        "production",
        "provider_ready",
        "model_ready",
        "backtest_ready",
        "ready_for_ingestion",
        "ready_for_scoring",
        "ready_for_runtime",
        "ready_for_trading",
        "implementation_ready",
        "ingestion_ready",
    ]
    missing_examples = [item for item in forbidden_examples if item not in text]
    assert not missing_examples, f"Forbidden examples section missing examples: {missing_examples}"

    parsed_values = [value for values in _parsed_assignments(section).values() for value in values]
    invalid_forbidden_values = sorted({value for value in parsed_values if value in forbidden_examples})
    assert not invalid_forbidden_values


def test_non_approval_boundaries_are_explicit() -> None:
    lower = _text().lower()
    required_terms = [
        "provider integration",
        "connectors",
        "external api calls",
        "provider credentials",
        "config loading",
        "secret reading",
        "data ingestion",
        "historical labels",
        "historical label implementation",
        "json/yaml/csv/parquet fixtures",
        "forecast pulls",
        "model scoring",
        "probability scoring",
        "backtesting",
        "paper simulation",
        "runtime observation",
        "trading",
        "order placement",
        "autonomy",
        "c++/rust runtime components",
    ]
    missing = [term for term in required_terms if term not in lower]
    assert not missing, f"Missing non-approval boundary terms: {missing}"

    forbidden_approval_phrases = [
        "provider integration is approved",
        "connectors are approved",
        "connector implementation is approved",
        "external api calls are approved",
        "provider credentials are approved",
        "config loading is approved",
        "secret reading is approved",
        "data ingestion is approved",
        "historical labels are approved",
        "historical label implementation is approved",
        "forecast pulls are approved",
        "model scoring is approved",
        "probability scoring is approved",
        "backtesting is approved",
        "paper simulation is approved",
        "runtime observation is approved",
        "trading is approved",
        "order placement is approved",
        "autonomy is approved",
        "c++ runtime components are approved",
        "rust runtime components are approved",
    ]
    bad_phrases = [phrase for phrase in forbidden_approval_phrases if phrase in lower]
    assert not bad_phrases, f"Forbidden approval language found: {bad_phrases}"
