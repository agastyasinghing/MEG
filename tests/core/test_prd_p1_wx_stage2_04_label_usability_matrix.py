from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-04_LABEL_USABILITY_BLOCKING_MATRIX_DESIGN.md")
STANDALONE_PRD_PATH = Path("docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md")
STAGE1_CLOSEOUT_PATH = Path(
    "docs/prd/PRD-P1-WX-STAGE1-CLOSEOUT-01_STAGE_1_CLOSURE_GATES_AND_STAGE_2_READINESS_REVIEW.md"
)
STAGE2_01_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-01_SOURCE_COMPATIBLE_HISTORICAL_LABEL_DESIGN.md")
STAGE2_02_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-02_POINT_IN_TIME_PROVENANCE_EXAMPLE_DESIGN.md")
STAGE2_03_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-03_SOURCE_RESOLUTION_AUDIT_CHECKLIST_DESIGN.md")
CANONICAL_ID = "PRD-P1-WX-STAGE2-04"
FORBIDDEN_ALTERNATE_IDS = {
    "WX-STAGE2-04",
    "P1-WX-S2-04",
    "PRD-WX-STAGE2-04",
    "PRD-P1-WEATHER-STAGE2-04",
    "PRD-P1-WX-STAGE-2-04",
}
MACHINE_HEADING = "## Machine-checkable Stage 2 label-usability matrix assignments"

ASSIGNMENT_LINE_PATTERN = re.compile(
    r"^\s*-\s*(label-usability matrix stage|blocker source|blocker severity|"
    r"label usability posture|matrix decision|escalation requirement|"
    r"no-lookahead risk|evidence status|label confidence):\s*([a-z0-9_/-]+)\s*$",
    flags=re.MULTILINE,
)

ALLOWED = {
    "label-usability matrix stage": {"stage_2_label_usability_blocking_matrix_design"},
    "blocker source": {
        "source_resolution",
        "point_in_time_provenance",
        "station_source_selection",
        "publication_timestamp",
        "observation_availability",
        "archive_finality_layer",
        "revision_handling",
        "classification_authority",
        "source_conflict",
        "trap_annotation",
        "reviewer_adjudication",
        "no_lookahead_control",
        "other_unclear",
    },
    "blocker severity": {"none", "caution", "blocking", "unknown"},
    "label usability posture": {
        "design_only",
        "usable_after_stage_2_approval",
        "blocked_pending_source_match",
        "blocked_pending_provenance",
        "blocked_pending_adjudication",
    },
    "matrix decision": {
        "allow_design_only",
        "allow_after_stage_2_approval",
        "block_source_match",
        "block_provenance",
        "block_adjudication",
        "require_more_evidence",
        "unclear",
    },
    "escalation requirement": {
        "none_required",
        "reviewer_note_required",
        "adjudication_required",
        "source_evidence_required",
        "provenance_evidence_required",
        "blocked_until_resolved",
    },
    "no-lookahead risk": {"none_identified", "possible", "likely", "blocking", "unknown"},
    "evidence status": {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"},
    "label confidence": {"confirmed", "unclear", "unknown"},
}

EXPECTED_ASSIGNMENT_LINES = [
    "- label-usability matrix stage: stage_2_label_usability_blocking_matrix_design",
    "- blocker source: source_resolution",
    "- blocker source: point_in_time_provenance",
    "- blocker source: station_source_selection",
    "- blocker source: publication_timestamp",
    "- blocker source: observation_availability",
    "- blocker source: archive_finality_layer",
    "- blocker source: revision_handling",
    "- blocker source: classification_authority",
    "- blocker source: source_conflict",
    "- blocker source: trap_annotation",
    "- blocker source: reviewer_adjudication",
    "- blocker source: no_lookahead_control",
    "- blocker source: other_unclear",
    "- blocker severity: none",
    "- blocker severity: caution",
    "- blocker severity: blocking",
    "- blocker severity: unknown",
    "- label usability posture: design_only",
    "- label usability posture: usable_after_stage_2_approval",
    "- label usability posture: blocked_pending_source_match",
    "- label usability posture: blocked_pending_provenance",
    "- label usability posture: blocked_pending_adjudication",
    "- matrix decision: allow_design_only",
    "- matrix decision: allow_after_stage_2_approval",
    "- matrix decision: block_source_match",
    "- matrix decision: block_provenance",
    "- matrix decision: block_adjudication",
    "- matrix decision: require_more_evidence",
    "- matrix decision: unclear",
    "- escalation requirement: none_required",
    "- escalation requirement: reviewer_note_required",
    "- escalation requirement: adjudication_required",
    "- escalation requirement: source_evidence_required",
    "- escalation requirement: provenance_evidence_required",
    "- escalation requirement: blocked_until_resolved",
    "- no-lookahead risk: none_identified",
    "- no-lookahead risk: possible",
    "- no-lookahead risk: likely",
    "- no-lookahead risk: blocking",
    "- no-lookahead risk: unknown",
    "- evidence status: source_backed",
    "- evidence status: reviewer_inferred",
    "- evidence status: missing",
    "- evidence status: conflicting",
    "- evidence status: not_applicable",
    "- label confidence: confirmed",
    "- label confidence: unclear",
    "- label confidence: unknown",
]

REQUIRED_TERMS = [
    "standalone meg weather bot prd",
    "prd-p1-wx-stage1-closeout-01",
    "prd-p1-wx-stage2-01",
    "prd-p1-wx-stage2-02",
    "prd-p1-wx-stage2-03",
    "stage 2 design only",
    "label-usability/blocking matrix design",
    "label-usability blocking matrix",
    "matrix decision rules",
    "label-usability matrix template",
    "representative synthetic matrix scenario",
    "blocker source",
    "blocker severity",
    "label usability posture",
    "source-resolution/provenance blockers",
    "relationship to stage 2 historical-label design",
    "relationship to stage 3 scoring",
    "language/tooling posture",
    "machine-checkable stage 2 label-usability matrix assignments",
    "non-approval boundaries",
]

REQUIRED_SCENARIOS = [
    "source_resolution",
    "point_in_time_provenance",
    "station_source_selection",
    "archive_finality_layer",
]

REQUIRED_NON_APPROVAL_TERMS = [
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

FORBIDDEN_APPROVAL_PHRASES = [
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


def _text() -> str:
    assert PRD_PATH.exists(), f"Missing PRD file: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    start = text.find(MACHINE_HEADING)
    assert start != -1, "Missing machine-checkable Stage 2 label-usability matrix assignments section"
    after_heading = text[start + len(MACHINE_HEADING) :]
    next_heading = re.search(r"^##\s+", after_heading, flags=re.MULTILINE)
    return after_heading if next_heading is None else after_heading[: next_heading.start()]


def _parsed_assignments(section: str) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {field: [] for field in ALLOWED}
    for match in ASSIGNMENT_LINE_PATTERN.finditer(section):
        field, value = match.groups()
        parsed[field].append(value.strip())
    return parsed


def _nonblank_machine_lines(section: str) -> list[str]:
    return [line for line in section.splitlines() if line.strip()]


def test_required_source_documents_remain_present() -> None:
    required_paths = [
        STANDALONE_PRD_PATH,
        STAGE1_CLOSEOUT_PATH,
        STAGE2_01_PATH,
        STAGE2_02_PATH,
        STAGE2_03_PATH,
    ]
    missing = [path.as_posix() for path in required_paths if not path.exists()]
    assert not missing, f"Missing required source documents: {missing}"


def test_stage2_label_usability_matrix_prd_presence_and_core_terms() -> None:
    text = _text()
    lower = text.lower()

    assert CANONICAL_ID in text
    forbidden_ids = sorted(
        identifier
        for identifier in FORBIDDEN_ALTERNATE_IDS
        if re.search(rf"(?<![A-Z0-9-]){re.escape(identifier)}(?![A-Z0-9-])", text)
    )
    assert not forbidden_ids, f"Forbidden alternate canonical IDs found: {forbidden_ids}"

    missing = [term for term in REQUIRED_TERMS if term not in lower]
    assert not missing, f"Missing required planning terms: {missing}"


def test_representative_scenario_count_and_required_types() -> None:
    lower = _text().lower()
    scenario_count = len(re.findall(r"^###\s+representative matrix scenario\b", lower, flags=re.MULTILINE))
    assert 4 <= scenario_count <= 6

    missing = [scenario for scenario in REQUIRED_SCENARIOS if scenario not in lower]
    assert not missing, f"Missing required scenario types: {missing}"


def test_machine_checkable_section_contains_expected_lines() -> None:
    section = _machine_section(_text())
    missing = [line for line in EXPECTED_ASSIGNMENT_LINES if line not in section]
    assert not missing, f"Missing machine-checkable assignment lines: {missing}"


def test_machine_checkable_section_contains_only_exact_assignment_lines() -> None:
    section = _machine_section(_text())
    malformed = [
        line
        for line in _nonblank_machine_lines(section)
        if ASSIGNMENT_LINE_PATTERN.fullmatch(line) is None
    ]
    assert not malformed, f"Unexpected non-assignment lines in machine-checkable section: {malformed}"


def test_machine_checkable_values_use_closed_sets_only() -> None:
    section = _machine_section(_text())
    parsed = _parsed_assignments(section)

    for field, values in parsed.items():
        assert values, f"No machine-checkable assignments found for {field}"
        invalid = sorted({value for value in values if value not in ALLOWED[field]})
        assert not invalid, f"Invalid parsed values for {field}: {invalid}"
        duplicated = sorted({value for value in values if values.count(value) > 1})
        assert not duplicated, f"Duplicate machine-checkable assignments for {field}: {duplicated}"
        missing_values = sorted(ALLOWED[field] - set(values))
        assert not missing_values, f"Machine-checkable assignments missing {field} values: {missing_values}"
        unexpected_values = sorted(set(values) - ALLOWED[field])
        assert not unexpected_values, f"Unexpected machine-checkable assignments for {field}: {unexpected_values}"


def test_machine_checkable_parser_ignores_forbidden_examples_outside_section() -> None:
    text = _text().lower()
    assert "caution/blocking" in text
    assert "design_only/usable_after_stage_2_approval" in text
    assert "partial" in text
    assert "mixed" in text
    assert "live" in text
    assert "production" in text

    section = _machine_section(_text())
    parsed_values = {value for values in _parsed_assignments(section).values() for value in values}
    forbidden_actual_values = {
        "caution/blocking",
        "design_only/usable_after_stage_2_approval",
        "partial",
        "mixed",
        "live",
        "production",
    }
    assert parsed_values.isdisjoint(forbidden_actual_values)


def test_non_approval_boundaries_are_explicit_without_forbidden_approval_phrases() -> None:
    lower = _text().lower()
    missing = [term for term in REQUIRED_NON_APPROVAL_TERMS if term not in lower]
    assert not missing, f"Missing non-approval boundary terms: {missing}"

    bad_approvals = [phrase for phrase in FORBIDDEN_APPROVAL_PHRASES if phrase in lower]
    assert not bad_approvals, f"Forbidden approval language found: {bad_approvals}"
