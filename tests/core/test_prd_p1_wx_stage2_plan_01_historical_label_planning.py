from pathlib import Path
import re


PRD_PATH = Path("docs/prd/PRD-P1-WX-STAGE2-PLAN-01_HISTORICAL_LABEL_IMPLEMENTATION_PLANNING.md")
CANONICAL_ID = "PRD-P1-WX-STAGE2-PLAN-01"
MACHINE_HEADING = "## Machine-checkable Stage 2 implementation-planning assignments"

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
    "Stage2 approval": Path("docs/prd/PRD-P1-WX-STAGE2-APPROVAL-01_EXPLICIT_IMPLEMENTATION_APPROVAL_REQUEST.md"),
}

ALLOWED = {
    "planning stage": {"stage_2_historical_label_implementation_planning"},
    "planning status": {
        "planning_only",
        "implementation_not_started",
        "human_approval_limited_to_planning",
        "blocked_pending_fix",
        "unclear",
    },
    "planned future scope": {
        "historical_label_schema_mapping",
        "source_resolution_validation",
        "point_in_time_provenance_validation",
        "label_usability_validation",
        "static_test_planning",
        "changed_file_allowlist_planning",
        "no_ingestion_no_runtime_no_scoring",
    },
    "implementation boundary status": {
        "not_implemented",
        "separate_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future component category": {
        "domain_model_planning",
        "static_schema_planning",
        "source_resolution_validator_planning",
        "provenance_validator_planning",
        "label_usability_validator_planning",
        "static_test_planning",
        "fixture_strategy_planning",
        "other_unclear",
    },
    "non-approval category": {
        "implementation_code",
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
    "- planning stage: stage_2_historical_label_implementation_planning",
    "- planning status: planning_only",
    "- planning status: implementation_not_started",
    "- planning status: human_approval_limited_to_planning",
    "- planning status: blocked_pending_fix",
    "- planning status: unclear",
    "- planned future scope: historical_label_schema_mapping",
    "- planned future scope: source_resolution_validation",
    "- planned future scope: point_in_time_provenance_validation",
    "- planned future scope: label_usability_validation",
    "- planned future scope: static_test_planning",
    "- planned future scope: changed_file_allowlist_planning",
    "- planned future scope: no_ingestion_no_runtime_no_scoring",
    "- implementation boundary status: not_implemented",
    "- implementation boundary status: separate_approval_required",
    "- implementation boundary status: explicitly_out_of_scope",
    "- implementation boundary status: blocked",
    "- future component category: domain_model_planning",
    "- future component category: static_schema_planning",
    "- future component category: source_resolution_validator_planning",
    "- future component category: provenance_validator_planning",
    "- future component category: label_usability_validator_planning",
    "- future component category: static_test_planning",
    "- future component category: fixture_strategy_planning",
    "- future component category: other_unclear",
    "- non-approval category: implementation_code",
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
    "prd-p1-wx-stage2-plan-01",
    "standalone meg weather bot prd",
    "prd-p1-wx-stage1-closeout-01",
    "prd-p1-wx-stage2-01",
    "prd-p1-wx-stage2-02",
    "prd-p1-wx-stage2-03",
    "prd-p1-wx-stage2-04",
    "prd-p1-wx-stage2-gate-01",
    "prd-p1-wx-stage2-approval-01",
    "implementation planning only",
    "implementation code is not created",
    "implementation has not started",
    "historical labels are not created",
    "fixtures/generated data are not created",
    "ingestion is not created",
    "connectors are not created",
    "external api calls are not created",
    "scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved",
    "planned future component boundary",
    "planned changed-file allowlist",
    "planned static-test requirements",
]

FORBIDDEN_APPROVAL_PHRASES = [
    "implementation code is approved",
    "historical label implementation is approved",
    "data ingestion is approved",
    "provider integration is approved",
    "connectors are approved",
    "external api calls are approved",
    "scoring is approved",
    "backtesting is approved",
    "runtime observation is approved",
    "trading is approved",
    "autonomy is approved",
    "implementation has started",
    "historical labels are created",
    "fixtures are created",
]

ASSIGNMENT_PATTERN = re.compile(
    r"^\s*-\s*(planning stage|planning status|planned future scope|"
    r"implementation boundary status|future component category|non-approval category|"
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


def test_stage2_plan_prd_exists_and_references_required_sources() -> None:
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


def test_non_approval_boundaries_and_forbidden_phrases() -> None:
    lower = _text().lower()

    required_boundaries = [
        "provider/api connectors are not created",
        "forecast pulls are not created",
        "a later implementation ticket requires separate explicit approval",
        "does not approve implementation code",
        "does not approve historical label implementation",
        "does not approve data ingestion",
        "does not approve provider integration",
        "does not approve connectors",
        "does not approve external api calls",
        "does not approve model scoring",
        "does not approve model scoring, probability scoring, backtesting",
        "does not approve model scoring, probability scoring, backtesting, paper simulation, runtime observation, trading, order placement",
    ]
    missing = [term for term in required_boundaries if term not in lower]
    assert not missing, f"Missing non-approval boundaries: {missing}"

    present = [phrase for phrase in FORBIDDEN_APPROVAL_PHRASES if phrase in lower]
    assert not present, f"Forbidden approval/implementation phrases present: {present}"


def test_future_planning_content_exists_without_implementation() -> None:
    lower = _text().lower()

    expected = [
        "map `prd-p1-wx-stage2-01` to code",
        "without creating implementation code",
        "map `prd-p1-wx-stage2-03` to validation",
        "does not write validators",
        "map `prd-p1-wx-stage2-02` to validation",
        "does not write provenance validators",
        "map `prd-p1-wx-stage2-04` to validation",
        "does not implement label-usability code",
        "clearly marked as future only",
        "proposed future static-test requirements only",
        "remains blocked unless separately approved",
    ]
    missing = [term for term in expected if term not in lower]
    assert not missing, f"Missing future-planning content: {missing}"


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _text()
    section = _machine_section(text)

    assert "## Planning matrix" not in section
    assert "Forbidden Stage 2 implementation-planning values" not in section

    missing_lines = [line for line in EXPECTED_ASSIGNMENT_LINES if line not in section]
    assert not missing_lines, f"Missing assignment lines: {missing_lines}"

    assignments = ASSIGNMENT_PATTERN.findall(section)
    assert assignments, "No machine-checkable assignments parsed"

    invalid = [(field, value) for field, value in assignments if value not in ALLOWED[field]]
    assert not invalid, f"Invalid closed-set assignments: {invalid}"

    observed_by_field = {field: set() for field in ALLOWED}
    for field, value in assignments:
        observed_by_field[field].add(value)

    missing_values = {
        field: sorted(values - observed_by_field[field])
        for field, values in ALLOWED.items()
        if values - observed_by_field[field]
    }
    assert not missing_values, f"Missing closed-set values: {missing_values}"

    unexpected_fields = set(observed_by_field) - set(ALLOWED)
    assert not unexpected_fields, f"Unexpected assignment fields: {unexpected_fields}"


def test_assignment_parser_ignores_prose_forbidden_values_and_matrix_rows() -> None:
    text = _text()
    section = _machine_section(text)
    parsed_values = [value for _, value in ASSIGNMENT_PATTERN.findall(section)]

    forbidden_actual_values = {
        "planning_only/implementation_not_started",
        "not_implemented/separate_approval_required",
        "historical_label_schema_mapping/source_resolution_validation",
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
    }

    assert forbidden_actual_values.isdisjoint(parsed_values)
