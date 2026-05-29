from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-APPROVAL-01_EXPLICIT_IMPLEMENTATION_APPROVAL_REQUEST.md")
CANONICAL_ID = "PRD-P1-WX-STAGE2-APPROVAL-01"
SOURCE_DOC_PATHS = {
    "standalone Weather Bot PRD": Path("docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md"),
    "Stage 1 closeout": Path(
        "docs/prd/PRD-P1-WX-STAGE1-CLOSEOUT-01_STAGE_1_CLOSURE_GATES_AND_STAGE_2_READINESS_REVIEW.md"
    ),
    "Stage2-01": Path("docs/prd/PRD-P1-WX-STAGE2-01_SOURCE_COMPATIBLE_HISTORICAL_LABEL_DESIGN.md"),
    "Stage2-02": Path("docs/prd/PRD-P1-WX-STAGE2-02_POINT_IN_TIME_PROVENANCE_EXAMPLE_DESIGN.md"),
    "Stage2-03": Path("docs/prd/PRD-P1-WX-STAGE2-03_SOURCE_RESOLUTION_AUDIT_CHECKLIST_DESIGN.md"),
    "Stage2-04": Path("docs/prd/PRD-P1-WX-STAGE2-04_LABEL_USABILITY_BLOCKING_MATRIX_DESIGN.md"),
    "Stage2 gate": Path("docs/prd/PRD-P1-WX-STAGE2-GATE-01_STAGE_2_READINESS_IMPLEMENTATION_GATE_REVIEW.md"),
}
MACHINE_HEADING = "## Machine-checkable Stage 2 approval-request assignments"

ALLOWED = {
    "approval request stage": {"stage_2_explicit_implementation_approval_request"},
    "request status": {
        "request_prepared",
        "approval_not_granted",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "requested future scope": {
        "implementation_planning_only",
        "historical_label_schema_to_code_planning",
        "static_fixture_planning",
        "source_resolution_validation_planning",
        "point_in_time_provenance_validation_planning",
        "label_usability_validation_planning",
        "no_runtime_no_ingestion_no_scoring",
    },
    "approval boundary status": {
        "not_approved",
        "separate_human_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future ticket permission": {
        "may_request_next_planning_ticket",
        "must_not_create_implementation_code",
        "must_not_create_ingestion",
        "must_not_create_runtime",
        "must_not_create_scoring",
        "must_not_create_trading",
        "blocked_until_human_decision",
    },
    "non-approval category": {
        "implementation",
        "ingestion",
        "provider_integration",
        "connectors",
        "external_api_calls",
        "credentials_secrets_config",
        "forecast_pulls",
        "historical_label_data",
        "fixtures_or_generated_data",
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

EXPECTED_ASSIGNMENT_LINES = [
    "- approval request stage: stage_2_explicit_implementation_approval_request",
    "- request status: request_prepared",
    "- request status: approval_not_granted",
    "- request status: human_review_required",
    "- request status: blocked_pending_fix",
    "- request status: unclear",
    "- requested future scope: implementation_planning_only",
    "- requested future scope: historical_label_schema_to_code_planning",
    "- requested future scope: static_fixture_planning",
    "- requested future scope: source_resolution_validation_planning",
    "- requested future scope: point_in_time_provenance_validation_planning",
    "- requested future scope: label_usability_validation_planning",
    "- requested future scope: no_runtime_no_ingestion_no_scoring",
    "- approval boundary status: not_approved",
    "- approval boundary status: separate_human_approval_required",
    "- approval boundary status: explicitly_out_of_scope",
    "- approval boundary status: blocked",
    "- future ticket permission: may_request_next_planning_ticket",
    "- future ticket permission: must_not_create_implementation_code",
    "- future ticket permission: must_not_create_ingestion",
    "- future ticket permission: must_not_create_runtime",
    "- future ticket permission: must_not_create_scoring",
    "- future ticket permission: must_not_create_trading",
    "- future ticket permission: blocked_until_human_decision",
    "- non-approval category: implementation",
    "- non-approval category: ingestion",
    "- non-approval category: provider_integration",
    "- non-approval category: connectors",
    "- non-approval category: external_api_calls",
    "- non-approval category: credentials_secrets_config",
    "- non-approval category: forecast_pulls",
    "- non-approval category: historical_label_data",
    "- non-approval category: fixtures_or_generated_data",
    "- non-approval category: model_scoring",
    "- non-approval category: probability_scoring",
    "- non-approval category: backtesting",
    "- non-approval category: paper_simulation",
    "- non-approval category: runtime_observation",
    "- non-approval category: trading_order_autonomy",
    "- non-approval category: production_behavior",
    "- non-approval category: cplusplus_rust_runtime",
    "- non-approval category: other_unclear",
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
    "prd-p1-wx-stage2-approval-01",
    "standalone meg weather bot prd",
    "prd-p1-wx-stage1-closeout-01",
    "prd-p1-wx-stage2-01",
    "prd-p1-wx-stage2-02",
    "prd-p1-wx-stage2-03",
    "prd-p1-wx-stage2-04",
    "prd-p1-wx-stage2-gate-01",
    "approval request only",
    "approval-request scope",
    "approval has not been granted",
    "implementation is not approved",
    "implementation planning has not started",
    "requested future planning scope",
    "explicit non-approval boundaries",
    "human approval checklist",
    "approval decision options",
    "approval-request matrix",
    "if approved later, next-ticket boundaries",
    "relationship to future implementation planning",
    "relationship to future stage 3 scoring",
    "language/tooling posture",
    "machine-checkable stage 2 approval-request assignments",
]

NON_APPROVAL_TERMS = [
    "implementation code",
    "historical label implementation",
    "data ingestion",
    "provider integration",
    "connectors",
    "external api calls",
    "credentials",
    "secret configuration",
    "forecast pulls",
    "historical label data",
    "json/yaml/csv/parquet fixtures",
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
    "implementation is approved",
    "historical label implementation is approved",
    "data ingestion is approved",
    "provider integration is approved",
    "connectors are approved",
    "scoring is approved",
    "backtesting is approved",
    "runtime observation is approved",
    "trading is approved",
    "autonomy is approved",
    "approval has been granted",
]

FORBIDDEN_EXAMPLES = [
    "request_prepared/approval_not_granted",
    "not_approved/separate_human_approval_required",
    "implementation_planning_only/static_fixture_planning",
    "source_backed/reviewer_inferred",
    "confirmed/unclear",
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
    "scoring_ready",
    "simulation_ready",
    "runtime_ready",
    "trading_ready",
    "approved_for_implementation",
    "approved_for_ingestion",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
]

ASSIGNMENT_PATTERN = re.compile(
    r"^\s*-\s*(approval request stage|request status|requested future scope|"
    r"approval boundary status|future ticket permission|non-approval category|"
    r"evidence status|label confidence):\s*([a-z0-9_/-]+)\s*$",
    flags=re.MULTILINE,
)


def _text() -> str:
    assert PRD_PATH.exists(), f"Missing PRD document: {PRD_PATH}"
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    pattern = re.compile(rf"^{re.escape(MACHINE_HEADING)}\s*$", flags=re.MULTILINE)
    match = pattern.search(text)
    assert match, f"Missing exact machine-checkable section heading: {MACHINE_HEADING}"
    after_heading = text[match.end() :]
    next_heading = re.search(r"^##\s+", after_heading, flags=re.MULTILINE)
    return after_heading[: next_heading.start()] if next_heading else after_heading


def test_stage2_approval_request_prd_exists_and_references_required_sources() -> None:
    text = _text()
    lower = text.lower()

    assert CANONICAL_ID in text
    missing = [term for term in REQUIRED_TERMS if term not in lower]
    assert not missing, f"Missing required terms: {missing}"

    missing_source_docs = [name for name, path in SOURCE_DOC_PATHS.items() if not path.exists()]
    assert not missing_source_docs, f"Missing source-of-truth docs: {missing_source_docs}"

    missing_source_filenames = [
        path.name for path in SOURCE_DOC_PATHS.values() if path.name.lower() not in lower
    ]
    assert not missing_source_filenames, f"Missing exact source document filenames: {missing_source_filenames}"


def test_non_approval_boundaries_and_forbidden_approval_phrases() -> None:
    lower = _text().lower()

    missing = [term for term in NON_APPROVAL_TERMS if term not in lower]
    assert not missing, f"Missing non-approval boundary terms: {missing}"

    bad = [phrase for phrase in FORBIDDEN_APPROVAL_PHRASES if phrase in lower]
    assert not bad, f"Forbidden approval language found: {bad}"


def test_forbidden_examples_are_documented_but_not_globally_rejected() -> None:
    lower = _text().lower()

    missing = [example for example in FORBIDDEN_EXAMPLES if example not in lower]
    assert not missing, f"Forbidden examples section missing examples: {missing}"


def test_machine_checkable_assignments_are_section_scoped_and_allowed() -> None:
    section = _machine_section(_text())
    assert "## Approval-request matrix" not in section
    assert "approval-request matrix" not in section.lower()
    parsed: dict[str, list[str]] = {field: [] for field in ALLOWED}

    for match in ASSIGNMENT_PATTERN.finditer(section):
        field = match.group(1)
        value = match.group(2)
        parsed[field].append(value)

    missing_fields = [field for field, values in parsed.items() if not values]
    assert not missing_fields, f"No machine-checkable assignments found for: {missing_fields}"

    for expected_line in EXPECTED_ASSIGNMENT_LINES:
        assert expected_line in section

    for field, values in parsed.items():
        bad = sorted({value for value in values if value not in ALLOWED[field]})
        assert not bad, f"Invalid parsed values for {field}: {bad}"

        missing_values = sorted(ALLOWED[field] - set(values))
        assert not missing_values, f"Machine-checkable assignments missing {field} values: {missing_values}"

    actual_assignment_count = len(ASSIGNMENT_PATTERN.findall(section))
    assert actual_assignment_count == len(EXPECTED_ASSIGNMENT_LINES)
