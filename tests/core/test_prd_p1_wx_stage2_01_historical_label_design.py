from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-01_SOURCE_COMPATIBLE_HISTORICAL_LABEL_DESIGN.md")
STANDALONE_PRD_PATH = Path("docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md")
STAGE1_PRD_PATHS = [
    Path("docs/prd/PRD-P1-WX-STAGE1-01_STATIC_CANONICAL_WEATHER_EVENT_MANUAL_LABEL_SCHEMA.md"),
    Path("docs/prd/PRD-P1-WX-STAGE1-02_STATIC_TRAP_LABEL_FIXTURE_TEMPLATE.md"),
    Path("docs/prd/PRD-P1-WX-STAGE1-03_REVIEWER_CHECKLIST_ADJUDICATION_PROTOCOL.md"),
    Path("docs/prd/PRD-P1-WX-STAGE1-04_STATIC_MANUALLY_LABELED_SEED_EXAMPLES.md"),
    Path("docs/prd/PRD-P1-WX-STAGE1-CLOSEOUT-01_STAGE_1_CLOSURE_GATES_AND_STAGE_2_READINESS_REVIEW.md"),
]
CANONICAL_ID = "PRD-P1-WX-STAGE2-01"
MACHINE_HEADING = "## Machine-checkable Stage 2 historical-label design assignments"
ASSIGNMENT_LINE_PATTERN = re.compile(r"^\s*-\s*([^:]+):\s*([a-z0-9_/-]+)\s*$", flags=re.MULTILINE)

ALLOWED = {
    "historical label design stage": {"stage_2_historical_label_design"},
    "historical label target type": {
        "source_compatible_resolution_label",
        "source_compatible_nonresolution_label",
        "resolver_source_reference",
        "station_metadata_reference",
        "point_in_time_provenance_reference",
        "revision_finality_reference",
        "trap_annotation_reference",
        "other_unclear",
    },
    "provenance requirement": {
        "required",
        "optional_for_context",
        "not_applicable",
        "missing_blocks_label",
        "unclear",
    },
    "point-in-time status": {
        "required_before_label_use",
        "unavailable",
        "ambiguous",
        "not_applicable",
        "design_only",
    },
    "source compatibility status": {
        "compatible",
        "incompatible",
        "unresolved",
        "requires_adjudication",
        "unknown",
    },
    "label usability posture": {
        "design_only",
        "usable_after_stage_2_approval",
        "blocked_pending_source_match",
        "blocked_pending_provenance",
        "blocked_pending_adjudication",
    },
    "no-lookahead risk": {
        "none_identified",
        "possible",
        "likely",
        "blocking",
        "unknown",
    },
    "stage 2 readiness posture": {
        "design_only",
        "ready_for_future_label_planning",
        "blocked",
        "unclear",
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
    "- historical label design stage: stage_2_historical_label_design",
    "- historical label target type: source_compatible_resolution_label",
    "- historical label target type: source_compatible_nonresolution_label",
    "- historical label target type: resolver_source_reference",
    "- historical label target type: station_metadata_reference",
    "- historical label target type: point_in_time_provenance_reference",
    "- historical label target type: revision_finality_reference",
    "- historical label target type: trap_annotation_reference",
    "- historical label target type: other_unclear",
    "- provenance requirement: required",
    "- provenance requirement: optional_for_context",
    "- provenance requirement: not_applicable",
    "- provenance requirement: missing_blocks_label",
    "- provenance requirement: unclear",
    "- point-in-time status: required_before_label_use",
    "- point-in-time status: unavailable",
    "- point-in-time status: ambiguous",
    "- point-in-time status: not_applicable",
    "- point-in-time status: design_only",
    "- source compatibility status: compatible",
    "- source compatibility status: incompatible",
    "- source compatibility status: unresolved",
    "- source compatibility status: requires_adjudication",
    "- source compatibility status: unknown",
    "- label usability posture: design_only",
    "- label usability posture: usable_after_stage_2_approval",
    "- label usability posture: blocked_pending_source_match",
    "- label usability posture: blocked_pending_provenance",
    "- label usability posture: blocked_pending_adjudication",
    "- no-lookahead risk: none_identified",
    "- no-lookahead risk: possible",
    "- no-lookahead risk: likely",
    "- no-lookahead risk: blocking",
    "- no-lookahead risk: unknown",
    "- stage 2 readiness posture: design_only",
    "- stage 2 readiness posture: ready_for_future_label_planning",
    "- stage 2 readiness posture: blocked",
    "- stage 2 readiness posture: unclear",
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
    start = text.find(MACHINE_HEADING)
    assert start != -1, "Missing machine-checkable Stage 2 historical-label design assignments section"
    after_heading_start = start + len(MACHINE_HEADING)
    after_heading = text[after_heading_start:]
    next_heading = re.search(r"^##\s+", after_heading, flags=re.MULTILINE)
    return after_heading if next_heading is None else after_heading[: next_heading.start()]


def test_required_source_documents_remain_present() -> None:
    required_paths = [STANDALONE_PRD_PATH, *STAGE1_PRD_PATHS]
    missing = [path.as_posix() for path in required_paths if not path.exists()]
    assert not missing, f"Missing required source documents: {missing}"


def test_stage2_design_prd_presence_and_core_terms() -> None:
    text = _text().lower()
    required = [
        "prd-p1-wx-stage2-01",
        "standalone meg weather bot prd",
        "prd-p1-wx-stage1-closeout-01",
        "prd-p1-wx-stage1-01",
        "prd-p1-wx-stage1-02",
        "prd-p1-wx-stage1-03",
        "prd-p1-wx-stage1-04",
        "stage 2 design",
        "stage 2 source-compatible historical-label design only",
        "source-compatible historical-label design",
        "source-defined settlement objects",
        "point-in-time provenance",
        "source-compatible truth requirements",
        "no-lookahead and leakage controls",
        "label usability and blocking rules",
        "relationship to stage 1 artifacts",
        "relationship to stage 3 scoring",
        "language/tooling posture",
        "machine-checkable stage 2 historical-label design assignments",
        "non-approval boundaries",
    ]
    missing = [term for term in required if term not in text]
    assert not missing, f"Missing required terms: {missing}"


def test_canonical_id_is_exact() -> None:
    text = _text()
    assert CANONICAL_ID in text
    forbidden_alias_patterns = [
        r"(?<!PRD-P1-)WX-STAGE2-01",
        r"P1-WX-S2-01",
        r"PRD-WX-STAGE2-01",
        r"PRD-P1-WEATHER-STAGE2-01",
        r"PRD-P1-WX-STAGE-2-01",
    ]
    forbidden_found = [
        pattern for pattern in forbidden_alias_patterns if re.search(pattern, text)
    ]
    assert not forbidden_found, f"Forbidden canonical ID aliases found: {forbidden_found}"


def test_machine_checkable_assignments_use_only_allowed_values() -> None:
    section = _machine_section(_text()).lower()

    actual_assignment_lines = [
        match.group(0).strip() for match in ASSIGNMENT_LINE_PATTERN.finditer(section)
    ]
    assert actual_assignment_lines == EXPECTED_ASSIGNMENT_LINES

    for field, allowed_values in ALLOWED.items():
        pattern = rf"^\s*-\s*{re.escape(field)}:\s*([a-z0-9_/-]+)\s*$"
        values = [m.group(1).strip() for m in re.finditer(pattern, section, flags=re.MULTILINE)]
        assert values, f"No machine-checkable assignments found for {field}"

        bad = sorted({value for value in values if value not in allowed_values})
        assert not bad, f"Invalid parsed values for {field}: {bad}"

        missing = sorted(allowed_values - set(values))
        assert not missing, f"Machine-checkable assignments missing {field} values: {missing}"


def test_forbidden_examples_are_documented_but_not_globally_rejected() -> None:
    text = _text().lower()
    forbidden_examples = [
        "compatible/incompatible",
        "required/optional",
        "source_backed/reviewer_inferred",
        "confirmed/unclear",
        "possible/likely",
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
    ]
    missing = [item for item in forbidden_examples if item not in text]
    assert not missing, f"Forbidden examples section missing examples: {missing}"


def test_non_approval_boundary_terms_present() -> None:
    text = _text().lower()
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
    missing = [term for term in required_terms if term not in text]
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
    bad = [phrase for phrase in forbidden_approval_phrases if phrase in text]
    assert not bad, f"Forbidden approval language found: {bad}"
