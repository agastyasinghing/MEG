"""Static checks for PRD-P1-WX-STAGE2-FIXTURE-PLAN-01."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = (
    REPO_ROOT
    / "docs"
    / "prd"
    / "PRD-P1-WX-STAGE2-FIXTURE-PLAN-01_STATIC_HISTORICAL_LABEL_FIXTURE_PLANNING.md"
)
CANONICAL_ID = "PRD-P1-WX-STAGE2-FIXTURE-PLAN-01"
MACHINE_HEADING = "## Machine-checkable Stage 2 fixture-planning assignments"

ALLOWED_ASSIGNMENTS = {
    "fixture planning stage": {"stage_2_static_historical_label_fixture_planning"},
    "planning status": {
        "planning_only",
        "fixture_implementation_not_started",
        "human_approval_limited_to_planning",
        "blocked_pending_fix",
        "unclear",
    },
    "fixture kind": {
        "synthetic_example",
        "real_example_requires_source_backing",
        "reviewer_edge_case",
        "trap_case",
        "blocked_case",
        "unclear_case",
    },
    "fixture planning scope": {
        "fixture_schema_shape_planning",
        "synthetic_real_distinction_planning",
        "provenance_requirement_planning",
        "no_lookahead_requirement_planning",
        "review_adjudication_planning",
        "static_validation_planning",
        "file_allowlist_planning",
        "no_ingestion_no_runtime_no_scoring",
    },
    "fixture implementation boundary": {
        "not_implemented",
        "separate_approval_required",
        "explicitly_out_of_scope",
        "blocked",
    },
    "fixture data posture": {
        "no_fixture_data_created",
        "no_generated_data_created",
        "planning_only",
        "provenance_required_before_real_use",
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
    "planning_only/fixture_implementation_not_started",
    "not_implemented/separate_approval_required",
    "synthetic_example/real_example_requires_source_backing",
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
    "approved_for_fixtures",
    "approved_for_ingestion",
    "approved_for_runtime",
    "approved_for_scoring",
    "approved_for_trading",
    "trade" + "_ready",
    "auto" + "_execute",
    "auto" + "nomous",
    "live",
    "production",
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


def test_fixture_plan_prd_exists_with_canonical_id_and_required_references() -> None:
    assert PRD_PATH.is_file()
    text = _read_prd()

    required = [
        CANONICAL_ID,
        "standalone MEG Weather Bot PRD",
        "PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md",
        "PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01",
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
        "## 4. Planning authorization boundary",
        "## 5. Static fixture planning goal",
        "## 6. Fixture purpose and non-purpose",
        "## 7. Fixture schema/data-shape planning",
        "## 8. Synthetic-versus-real fixture distinction",
        "## 9. Provenance requirements planning",
        "## 10. No-lookahead requirements planning",
        "## 11. Review/adjudication requirements planning",
        "## 12. Future file allowlist planning",
        "## 13. Static validation requirements planning",
        "## 14. Relationship to Stage 2 skeleton validation",
        "## 15. Explicit non-approval boundaries",
        "## 16. Closed Stage 2 fixture-planning vocabulary",
        "## 17. Forbidden Stage 2 fixture-planning values",
        MACHINE_HEADING,
        "## 19. Fixture planning matrix",
        "## 20. If approved later, fixture implementation boundaries",
        "## 21. Relationship to future ingestion",
        "## 22. Relationship to future scoring/" + "back" + "testing",
        "## 23. Relationship to future runtime/trading",
        "## 24. Later-ticket handoff",
        "## 25. Acceptance criteria",
    ]
    for section in sections:
        assert section in text


def test_planning_only_scope_and_non_approval_wording_are_explicit() -> None:
    text = _read_prd().lower()
    required_phrases = [
        "static historical-label fixture planning only",
        "fixture implementation is not approved",
        "fixture files are not created",
        "historical-label data is not created",
        "json/yaml/csv/" + "par" + "quet fixtures are not created",
        "generated data is not created",
        "ingestion is not created",
        "provider/api connectors are not created",
        "external api calls are not created",
        "credentials/secrets/config loading",
        "forecast pulls are not created",
        "scoring/" + "back" + "testing/runtime/trading/order " + "placement/auto" + "nomy remain unapproved",
        "future fixture implementation requires separate explicit human approval",
        "does not imply ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_planning_concepts_and_future_boundaries_are_present() -> None:
    text = _read_prd().lower()
    required = [
        "fixture_id",
        "fixture_kind",
        "synthetic_or_real",
        "canonical_event_summary",
        "venue_rule_summary",
        "condition_id",
        "token_id",
        "outcome",
        "source_resolution metadata shape",
        "point_in_time_provenance metadata shape",
        "label_usability metadata shape",
        "expected_validation_posture",
        "reviewer_notes",
        "provenance_notes",
        "no_lookahead_notes",
        "synthetic examples are acceptable only",
        "real examples would require source-backed provenance",
        "no-lookahead constraints matter",
        "avoid implying provider/api integration",
        "fixture implementation should remain static, minimal, and file-allowlisted",
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
        assert not missing_allowed_values, (
            f"Expected every closed-set value for {name}; "
            f"missing {sorted(missing_allowed_values)}"
        )


def test_forbidden_examples_are_documented_but_not_parsed_as_actual_assignments() -> None:
    text = _read_prd()
    forbidden_section_start = text.index("## 17. Forbidden Stage 2 fixture-planning values")
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
