from pathlib import Path
import re


PRD_PATH = Path(
    "docs/prd/PRD-P1-WX-STAGE2-SKELETON-APPROVAL-01_NARROW_IMPLEMENTATION_SKELETON_APPROVAL_REQUEST.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-SKELETON-APPROVAL-01"
MACHINE_HEADING = "## Machine-checkable Stage 2 skeleton approval-request assignments"

ALLOWED = {
    "skeleton approval stage": {"stage_2_skeleton_approval_request"},
    "request status": {
        "request_prepared",
        "skeleton_not_approved",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "requested skeleton scope": {
        "domain_model_skeleton",
        "static_schema_skeleton",
        "source_resolution_validator_skeleton",
        "provenance_validator_skeleton",
        "label_usability_validator_skeleton",
        "static_test_skeleton",
        "no_ingestion_no_runtime_no_scoring",
    },
    "approval boundary status": {
        "not_approved",
        "separate_human_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future skeleton permission": {
        "may_request_skeleton_ticket",
        "must_not_create_code_now",
        "must_not_create_ingestion",
        "must_not_create_runtime",
        "must_not_create_scoring",
        "must_not_create_trading",
        "blocked_until_human_decision",
    },
    "non-approval category": {
        "implementation_code_now",
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
    "- skeleton approval stage: stage_2_skeleton_approval_request",
    "- request status: request_prepared",
    "- request status: skeleton_not_approved",
    "- request status: human_review_required",
    "- request status: blocked_pending_fix",
    "- request status: unclear",
    "- requested skeleton scope: domain_model_skeleton",
    "- requested skeleton scope: static_schema_skeleton",
    "- requested skeleton scope: source_resolution_validator_skeleton",
    "- requested skeleton scope: provenance_validator_skeleton",
    "- requested skeleton scope: label_usability_validator_skeleton",
    "- requested skeleton scope: static_test_skeleton",
    "- requested skeleton scope: no_ingestion_no_runtime_no_scoring",
    "- approval boundary status: not_approved",
    "- approval boundary status: separate_human_approval_required",
    "- approval boundary status: explicitly_out_of_scope",
    "- approval boundary status: blocked",
    "- future skeleton permission: may_request_skeleton_ticket",
    "- future skeleton permission: must_not_create_code_now",
    "- future skeleton permission: must_not_create_ingestion",
    "- future skeleton permission: must_not_create_runtime",
    "- future skeleton permission: must_not_create_scoring",
    "- future skeleton permission: must_not_create_trading",
    "- future skeleton permission: blocked_until_human_decision",
    "- non-approval category: implementation_code_now",
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
    CANONICAL_ID.lower(),
    "standalone meg weather bot prd",
    "prd-p1-wx-stage1-closeout-01",
    "prd-p1-wx-stage2-01",
    "prd-p1-wx-stage2-02",
    "prd-p1-wx-stage2-03",
    "prd-p1-wx-stage2-04",
    "prd-p1-wx-stage2-gate-01",
    "prd-p1-wx-stage2-approval-01",
    "prd-p1-wx-stage2-plan-01",
    "this is a skeleton approval request only",
    "skeleton implementation is not approved by this document",
    "implementation code is not created",
    "implementation has not started",
    "historical labels are not created",
    "fixtures/generated data are not created",
    "ingestion is not created",
    "provider/api connectors are not created",
    "external api calls are not created",
    "forecast pulls are not created",
    "scoring/backtesting/runtime/trading/order placement/autonomy remain unapproved",
    "a later skeleton implementation ticket requires separate explicit human approval",
    "proposed future skeleton components",
    "proposed future changed-file allowlist",
    "proposed future static-test requirements",
]

REQUIRED_SECTIONS = [
    "## Status and scope",
    "## Strategic framing",
    "## Stage ladder position",
    "## Skeleton approval-request boundary",
    "## Requested future skeleton scope",
    "## Explicitly excluded future skeleton scope",
    "## Source-document dependency map",
    "## Proposed future skeleton components",
    "## Proposed future changed-file allowlist",
    "## Proposed future static-test requirements",
    "## Human approval checklist",
    "## Skeleton approval decision options",
    "## Explicit non-approval boundaries",
    "## Closed Stage 2 skeleton approval-request vocabulary",
    "## Forbidden Stage 2 skeleton approval-request values",
    MACHINE_HEADING,
    "## Skeleton approval-request matrix",
    "## If approved later, next-ticket boundaries",
    "## Relationship to future implementation",
    "## Relationship to future Stage 3 scoring",
    "## Later-ticket handoff",
    "## Acceptance criteria",
]

REQUIRED_FUTURE_SCOPE = [
    "domain model skeleton for historical-label metadata",
    "static schema skeleton for closed sets and required fields",
    "source-resolution validator skeleton for supplied metadata only",
    "point-in-time provenance validator skeleton for supplied metadata only",
    "label-usability validator skeleton for supplied metadata only",
    "static tests for non-approval boundaries and closed sets",
]

REQUIRED_EXCLUSIONS = [
    "ingestion",
    "provider/api connectors",
    "external api calls",
    "credentials/secrets/config loading",
    "forecast pulls",
    "historical label data",
    "json/yaml/csv/parquet fixtures or generated data",
    "scoring",
    "backtesting",
    "paper simulation",
    "runtime observation",
    "trading",
    "order placement",
    "autonomy",
    "c++/rust runtime components",
]

FORBIDDEN_APPROVAL_PHRASES = [
    "skeleton implementation is approved",
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
    r"^\s*-\s*(skeleton approval stage|request status|requested skeleton scope|"
    r"approval boundary status|future skeleton permission|non-approval category|"
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


def test_stage2_skeleton_approval_request_prd_exists_and_references_required_sources() -> None:
    text = _text()
    lowered = text.lower()

    for term in REQUIRED_TERMS:
        assert term in lowered, f"Missing required term: {term}"


def test_stage2_skeleton_approval_request_has_required_sections_in_order() -> None:
    text = _text()
    cursor = -1

    for section in REQUIRED_SECTIONS:
        position = text.find(section)
        assert position > cursor, f"Missing or out-of-order section: {section}"
        cursor = position


def test_stage2_skeleton_approval_request_scope_and_exclusions_are_explicit() -> None:
    text = _text().lower()

    for phrase in REQUIRED_FUTURE_SCOPE:
        assert phrase in text, f"Missing requested future skeleton scope phrase: {phrase}"

    for phrase in REQUIRED_EXCLUSIONS:
        assert phrase in text, f"Missing explicit exclusion phrase: {phrase}"


def test_stage2_skeleton_approval_request_rejects_forbidden_approval_phrases() -> None:
    text = _text().lower()

    offenders = [phrase for phrase in FORBIDDEN_APPROVAL_PHRASES if phrase in text]
    assert offenders == [], f"Forbidden approval/implementation phrase found: {offenders}"


def test_stage2_skeleton_approval_request_machine_section_exists_and_is_section_scoped() -> None:
    text = _text()
    section = _machine_section(text)

    assert section.strip(), "Machine-checkable section is empty"
    assert "## Skeleton approval-request matrix" not in section
    assert "request_prepared/skeleton_not_approved" not in section
    assert "domain_model_skeleton/static_schema_skeleton" not in section


def test_stage2_skeleton_approval_request_machine_assignments_match_expected_lines() -> None:
    section = _machine_section(_text())
    actual_lines = [line.strip() for line in section.splitlines() if line.strip()]

    assert actual_lines == EXPECTED_ASSIGNMENT_LINES


def test_stage2_skeleton_approval_request_closed_sets_are_enforced_in_machine_section_only() -> None:
    section = _machine_section(_text())
    parsed: dict[str, list[str]] = {field: [] for field in ALLOWED}
    unexpected_lines = []

    for line in section.splitlines():
        if not line.strip():
            continue
        match = ASSIGNMENT_PATTERN.match(line)
        if not match:
            unexpected_lines.append(line)
            continue
        field, value = match.groups()
        parsed[field].append(value)

    assert unexpected_lines == []
    assert set(parsed) == set(ALLOWED)

    for field, values in parsed.items():
        observed = set(values)
        assert observed == ALLOWED[field], f"Unexpected values for {field}: {sorted(observed)}"
        assert len(values) == len(observed), f"Duplicate values for {field}: {values}"


def test_stage2_skeleton_approval_request_forbidden_examples_are_not_actual_values() -> None:
    section = _machine_section(_text())
    values = [value for _, value in ASSIGNMENT_PATTERN.findall(section)]

    assert "request_prepared/skeleton_not_approved" not in values
    assert "not_approved/separate_human_approval_required" not in values
    assert "domain_model_skeleton/static_schema_skeleton" not in values
    assert "source_backed/reviewer_inferred" not in values
    assert "confirmed/unclear" not in values
    assert "approved" not in values
    assert "skeleton_approved" not in values
    assert "approved_for_implementation" not in values
