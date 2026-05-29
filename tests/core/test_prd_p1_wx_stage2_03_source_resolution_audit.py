from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-03_SOURCE_RESOLUTION_AUDIT_CHECKLIST_DESIGN.md")
STANDALONE_PRD_PATH = Path("docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md")
STAGE1_CLOSEOUT_PATH = Path(
    "docs/prd/PRD-P1-WX-STAGE1-CLOSEOUT-01_STAGE_1_CLOSURE_GATES_AND_STAGE_2_READINESS_REVIEW.md"
)
STAGE2_01_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-01_SOURCE_COMPATIBLE_HISTORICAL_LABEL_DESIGN.md")
STAGE2_02_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-02_POINT_IN_TIME_PROVENANCE_EXAMPLE_DESIGN.md")
CANONICAL_ID = "PRD-P1-WX-STAGE2-03"
MACHINE_HEADING = "## Machine-checkable Stage 2 source-resolution audit assignments"

ASSIGNMENT_LINE_PATTERN = re.compile(
    r"^\s*-\s*(source-resolution audit stage|audit checklist category|audit item decision|"
    r"source-resolution status|station/source selection status|archive/finality status|"
    r"provenance blocker status|label usability posture|evidence status|label confidence):"
    r"\s*([a-z0-9_/-]+)\s*$",
    flags=re.MULTILINE,
)

ALLOWED = {
    "source-resolution audit stage": {"stage_2_source_resolution_audit_design"},
    "audit checklist category": {
        "resolver_source_identity",
        "source_role",
        "station_source_selection",
        "publication_timestamp",
        "observation_availability",
        "archive_finality_layer",
        "revision_handling",
        "classification_authority",
        "source_conflict",
        "provenance_blocker",
        "label_usability",
        "reviewer_escalation",
        "other_unclear",
    },
    "audit item decision": {
        "pass",
        "caution",
        "block",
        "needs_more_evidence",
        "not_applicable",
    },
    "source-resolution status": {
        "source_resolved",
        "source_unresolved",
        "source_conflicting",
        "source_unknown",
        "requires_adjudication",
    },
    "station/source selection status": {
        "explicit_pre_result",
        "inferred_pre_result",
        "hindsight_risk",
        "unresolved",
        "not_applicable",
    },
    "archive/finality status": {
        "preliminary_layer",
        "final_layer",
        "revised_layer",
        "conflicting_layers",
        "unknown_layer",
        "not_applicable",
    },
    "provenance blocker status": {
        "none_identified",
        "missing_publication_timestamp",
        "missing_observation_availability",
        "missing_station_selection_time",
        "missing_archive_revision_record",
        "unresolved_source_conflict",
        "final_archive_leakage_risk",
        "hindsight_selection_risk",
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
    "- source-resolution audit stage: stage_2_source_resolution_audit_design",
    "- audit checklist category: resolver_source_identity",
    "- audit checklist category: source_role",
    "- audit checklist category: station_source_selection",
    "- audit checklist category: publication_timestamp",
    "- audit checklist category: observation_availability",
    "- audit checklist category: archive_finality_layer",
    "- audit checklist category: revision_handling",
    "- audit checklist category: classification_authority",
    "- audit checklist category: source_conflict",
    "- audit checklist category: provenance_blocker",
    "- audit checklist category: label_usability",
    "- audit checklist category: reviewer_escalation",
    "- audit checklist category: other_unclear",
    "- audit item decision: pass",
    "- audit item decision: caution",
    "- audit item decision: block",
    "- audit item decision: needs_more_evidence",
    "- audit item decision: not_applicable",
    "- source-resolution status: source_resolved",
    "- source-resolution status: source_unresolved",
    "- source-resolution status: source_conflicting",
    "- source-resolution status: source_unknown",
    "- source-resolution status: requires_adjudication",
    "- station/source selection status: explicit_pre_result",
    "- station/source selection status: inferred_pre_result",
    "- station/source selection status: hindsight_risk",
    "- station/source selection status: unresolved",
    "- station/source selection status: not_applicable",
    "- archive/finality status: preliminary_layer",
    "- archive/finality status: final_layer",
    "- archive/finality status: revised_layer",
    "- archive/finality status: conflicting_layers",
    "- archive/finality status: unknown_layer",
    "- archive/finality status: not_applicable",
    "- provenance blocker status: none_identified",
    "- provenance blocker status: missing_publication_timestamp",
    "- provenance blocker status: missing_observation_availability",
    "- provenance blocker status: missing_station_selection_time",
    "- provenance blocker status: missing_archive_revision_record",
    "- provenance blocker status: unresolved_source_conflict",
    "- provenance blocker status: final_archive_leakage_risk",
    "- provenance blocker status: hindsight_selection_risk",
    "- provenance blocker status: other_unclear",
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

REQUIRED_TERMS = [
    "source-resolution audit checklist design",
    "resolver source",
    "station/source selection",
    "publication timestamp",
    "archive/finality layer",
    "provenance blockers",
    "audit item decision rules",
    "source-resolution audit template",
    "representative synthetic audit scenario",
    "relationship to stage 2 historical-label design",
    "relationship to stage 3 scoring",
    "language/tooling posture",
    "machine-checkable stage 2 source-resolution audit assignments",
    "non-approval boundaries",
]

REQUIRED_SCENARIOS = [
    "resolver_source_identity",
    "station_source_selection",
    "publication_timestamp",
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
    assert start != -1, "Missing machine-checkable Stage 2 source-resolution audit assignments section"
    after_heading = text[start + len(MACHINE_HEADING) :]
    next_heading = re.search(r"^##\s+", after_heading, flags=re.MULTILINE)
    return after_heading if next_heading is None else after_heading[: next_heading.start()]


def _parsed_assignments(section: str) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {field: [] for field in ALLOWED}
    for match in ASSIGNMENT_LINE_PATTERN.finditer(section):
        field, value = match.groups()
        parsed[field].append(value.strip())
    return parsed


def test_required_source_documents_remain_present() -> None:
    required_paths = [STANDALONE_PRD_PATH, STAGE1_CLOSEOUT_PATH, STAGE2_01_PATH, STAGE2_02_PATH]
    missing = [path.as_posix() for path in required_paths if not path.exists()]
    assert not missing, f"Missing required source documents: {missing}"


def test_stage2_source_resolution_audit_prd_presence_and_core_terms() -> None:
    text = _text()
    lower = text.lower()

    assert CANONICAL_ID in text
    assert "standalone meg weather bot prd" in lower
    assert "prd-p1-wx-stage1-closeout-01" in lower
    assert "prd-p1-wx-stage2-01" in lower
    assert "prd-p1-wx-stage2-02" in lower
    assert "stage 2 source-resolution audit checklist design only" in lower
    assert "stage 2 design" in lower

    missing = [term for term in REQUIRED_TERMS if term not in lower]
    assert not missing, f"Missing required planning concepts: {missing}"


def test_representative_audit_scenarios_are_bounded_and_required_types_exist() -> None:
    text = _text().lower()

    scenario_count = len(re.findall(r"^###\s+representative audit scenario\b", text, flags=re.MULTILINE))
    assert 4 <= scenario_count <= 6

    missing = [scenario for scenario in REQUIRED_SCENARIOS if scenario not in text]
    assert not missing, f"Missing required audit scenario types: {missing}"

    assert text.count("representative synthetic audit scenario, not historical label data") >= scenario_count


def test_machine_checkable_section_contains_expected_assignment_lines() -> None:
    section = _machine_section(_text())
    missing = [line for line in EXPECTED_ASSIGNMENT_LINES if line not in section]
    assert not missing, f"Missing assignment lines: {missing}"


def test_machine_checkable_section_has_no_unexpected_assignment_lines() -> None:
    section = _machine_section(_text())
    parsed_lines = [
        line.strip()
        for line in section.splitlines()
        if ASSIGNMENT_LINE_PATTERN.match(line)
    ]

    assert parsed_lines == EXPECTED_ASSIGNMENT_LINES


def test_machine_checkable_assignments_use_only_allowed_values() -> None:
    section = _machine_section(_text())
    parsed = _parsed_assignments(section)

    for field, values in parsed.items():
        assert values, f"No machine-checkable assignments found for {field}"
        bad = sorted({value for value in values if value not in ALLOWED[field]})
        assert not bad, f"Invalid parsed values for {field}: {bad}"
        missing_values = sorted(ALLOWED[field] - set(values))
        assert not missing_values, f"Machine-checkable assignments missing {field} values: {missing_values}"


def test_machine_checkable_value_validation_is_scoped_to_assignment_section() -> None:
    text = _text().lower()
    section = _machine_section(_text()).lower()

    assert "pass/caution" in text
    assert "partial" in text
    assert "mixed" in text
    assert "live" in text
    assert "production" in text
    assert "c++" in text
    assert "rust" in text

    forbidden_actual_values = {
        "pass/caution",
        "source_resolved/source_unresolved",
        "explicit_pre_result/inferred_pre_result",
        "preliminary_layer/final_layer",
        "source_backed/reviewer_inferred",
        "confirmed/unclear",
        "design_only/usable_after_stage_2_approval",
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
    }
    parsed_values = {
        value
        for values in _parsed_assignments(section).values()
        for value in values
    }
    assert parsed_values.isdisjoint(forbidden_actual_values)


def test_non_approval_boundaries_are_explicit_without_approval_language() -> None:
    lower = _text().lower()

    missing = [term for term in REQUIRED_NON_APPROVAL_TERMS if term not in lower]
    assert not missing, f"Missing non-approval boundary terms: {missing}"

    bad_approval_phrases = [phrase for phrase in FORBIDDEN_APPROVAL_PHRASES if phrase in lower]
    assert not bad_approval_phrases, f"Forbidden approval language found: {bad_approval_phrases}"
