"""Static checks for PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = (
    REPO_ROOT
    / "docs"
    / "prd"
    / "PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01_STATIC_FIXTURE_DATA_APPROVAL_REQUEST.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01"
MACHINE_HEADING = "## Machine-checkable Stage 2 fixture approval-request assignments"

ALLOWED_ASSIGNMENTS = {
    "fixture approval stage": {"stage_2_static_fixture_data_approval_request"},
    "request status": {
        "request_prepared",
        "fixtures_not_approved",
        "human_review_required",
        "blocked_pending_fix",
        "unclear",
    },
    "requested future scope": {
        "static_fixture_planning_only",
        "fixture_schema_planning",
        "fixture_provenance_planning",
        "fixture_review_adjudication_planning",
        "fixture_static_validation_planning",
        "no_ingestion_no_runtime_no_scoring",
    },
    "approval boundary status": {
        "not_approved",
        "separate_human_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "future ticket permission": {
        "may_request_fixture_planning_ticket",
        "must_not_create_fixtures_now",
        "must_not_create_ingestion",
        "must_not_create_runtime",
        "must_not_create_scoring",
        "must_not_create_trading",
        "blocked_until_human_decision",
    },
    "fixture data posture": {
        "no_fixture_data_created",
        "planning_only",
        "synthetic_or_real_distinction_required",
        "provenance_required_before_use",
        "review_required_before_use",
    },
    "non-approval category": {
        "historical_label_data",
        "fixtures_or_generated_data",
        "ingestion",
        "provider_integration",
        "connectors",
        "external_api_calls",
        "credentials_secrets_config",
        "forecast_pulls",
        "model_scoring",
        "probability_scoring",
        "back" + "testing",
        "paper_simulation",
        "runtime_observation",
        "trading_order_autonomy",
        "production_behavior",
        "cplusplus_rust_runtime",
        "other_unclear",
    },
    "evidence status": {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"},
    "label confidence": {"confirmed", "unclear", "unknown"},
}

FORBIDDEN_EXAMPLES = {
    "request_prepared/fixtures_not_approved",
    "not_approved/separate_human_approval_required",
    "static_fixture_planning_only/fixture_schema_planning",
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
    "trade" + "_ready",
    "auto" + "_execute",
    "auto" + "nomous",
    "live",
    "production",
    "provider_ready",
    "model_ready",
    "back" + "test_ready",
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
    "approved_for_fixtures",
    "approved_for_ingestion",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
}


def _read_prd() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    start = text.index(MACHINE_HEADING)
    remainder = text[start + len(MACHINE_HEADING) :]
    match = re.search(r"\n## ", remainder)
    if match is None:
        return remainder
    return remainder[: match.start()]


def _assignment_values(section: str) -> dict[str, list[str]]:
    observed = {name: [] for name in ALLOWED_ASSIGNMENTS}
    assignment_pattern = re.compile(r"^- (?P<name>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)
    for match in assignment_pattern.finditer(section):
        name = match.group("name")
        value = match.group("value")
        assert name in ALLOWED_ASSIGNMENTS, f"Unexpected assignment name: {name}"
        observed[name].append(value)
    return observed


def test_fixture_approval_prd_exists_with_canonical_id_and_required_references() -> None:
    assert PRD_PATH.is_file()
    text = _read_prd()

    required = [
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01",
        "PRD-P1-WX-STAGE2-SKELETON-01",
        "PRD-P1-WX-STAGE2-SKELETON-02",
        "PRD-P1-WX-STAGE2-SKELETON-03",
    ]
    for expected in required:
        assert expected in text


def test_required_sections_are_present() -> None:
    text = _read_prd()
    sections = [
        "## 1. Status and scope",
        "## 2. Strategic framing",
        "## 3. Stage ladder position",
        "## 4. Fixture/data approval-request boundary",
        "## 5. Why static fixtures may be useful next",
        "## 6. Requested future scope",
        "## 7. Explicitly excluded scope",
        "## 8. Dependency on Stage 2 skeleton closeout",
        "## 9. Human approval checklist",
        "## 10. Approval decision options",
        "## 11. Closed Stage 2 fixture approval-request vocabulary",
        "## 12. Forbidden Stage 2 fixture approval-request values",
        MACHINE_HEADING,
        "## 14. Fixture approval-request matrix",
        "## 15. If approved later, next-ticket boundaries",
        "## 16. Explicit non-approval boundaries",
        "## 17. Relationship to future ingestion",
        "## 18. Relationship to future scoring/" + "back" + "testing",
        "## 19. Relationship to future runtime/trading",
        "## 20. Later-ticket handoff",
        "## 21. Acceptance criteria",
    ]
    for section in sections:
        assert section in text


def test_approval_request_scope_and_non_approvals_are_explicit() -> None:
    text = _read_prd().lower()
    required_phrases = [
        "static fixture/data approval request only",
        "static fixtures are not approved by this document",
        "fixture/data planning has not started",
        "fixture/data implementation has not started",
        "historical-label data is not created",
        "json/yaml/csv/" + "par" + "quet fixtures are not created",
        "generated data is not created",
        "ingestion is not created",
        "provider/api connectors are not created",
        "external api calls are not created",
        "credentials/secrets/config loading is not created",
        "forecast pulls are not created",
        "scoring/" + "back" + "testing/runtime/trading/order " + "placement/auto" + "nomy remain unapproved",
        "a later static fixture/data planning ticket requires separate human approval",
        "a later fixture implementation ticket requires separate explicit approval after planning",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_future_requested_scope_is_planning_only_and_future_gates_are_not_approved() -> None:
    text = _read_prd().lower()
    required = [
        "static fixture purpose and boundaries",
        "static fixture schema/data shape",
        "synthetic-versus-real fixture distinction",
        "fixture provenance requirements",
        "no-lookahead requirements",
        "fixture review/adjudication requirements",
        "fixture file allowlist planning",
        "static validation requirements",
        "fixture non-approval boundaries",
        "none of these options approves fixture/data implementation",
        "no gate is approved here",
    ]
    for phrase in required:
        assert phrase in text


def test_machine_checkable_assignment_section_exists_and_uses_only_closed_sets() -> None:
    text = _read_prd()
    assert MACHINE_HEADING in text
    section = _machine_section(text)
    observed = _assignment_values(section)

    for name, values in observed.items():
        assert values, f"Missing assignment for {name}"
        unexpected = sorted(set(values) - ALLOWED_ASSIGNMENTS[name])
        assert not unexpected, f"Unexpected {name} values: {unexpected}"

    for name, allowed_values in ALLOWED_ASSIGNMENTS.items():
        missing_allowed_values = allowed_values - set(observed[name])
        optional_unassigned = {"blocked_pending_fix", "unclear", "blocked", "missing", "conflicting", "unknown"}
        assert missing_allowed_values <= optional_unassigned, (
            f"Expected every non-error closed-set value for {name}; "
            f"missing {sorted(missing_allowed_values - optional_unassigned)}"
        )


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_assignments() -> None:
    text = _read_prd()
    forbidden_section_start = text.index("## 12. Forbidden Stage 2 fixture approval-request values")
    machine_section_start = text.index(MACHINE_HEADING)
    forbidden_section = text[forbidden_section_start:machine_section_start]
    for example in FORBIDDEN_EXAMPLES:
        assert example in forbidden_section

    actual_values = {
        value
        for values in _assignment_values(_machine_section(text)).values()
        for value in values
    }
    assert actual_values.isdisjoint(FORBIDDEN_EXAMPLES)
