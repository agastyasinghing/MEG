"""Static checks for MEG-ARCH-ALIGN-04 shared-rail review planning.

These tests validate a planning/static-test artifact only. They use Python
standard-library imports only and do not create runtime refactors, database
migrations, source-code migrations, provider connectors, source fetching,
scoring, backtesting, execution, trading, autonomy, or production behavior.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/prd/MEG-ARCH-ALIGN-04_SHARED_RAIL_CONTRACT_REVIEW_PLANNING.md"
CANONICAL_ID = "MEG-ARCH-ALIGN-04"
MACHINE_HEADING = "## Machine-checkable shared-rail contract review assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to MEG-ARCH-ALIGN-01",
    "Relationship to MEG-ARCH-ALIGN-02",
    "Relationship to MEG-ARCH-ALIGN-03",
    "Shared-rail contract review objective",
    "Target-migration candidate review objective",
    "Compatibility-boundary review objective",
    "Target canonical identifier contract",
    "market_id compatibility posture",
    "Candidate review method",
    "Compatibility-boundary review method",
    "Future shared-rail contract output format",
    "Future migration-candidate review output format",
    "Explicit non-implementation boundaries",
    "Blocked future work until review",
    "Recommended later ticket sequence",
    "Machine-checkable shared-rail contract review assignments",
    "Acceptance criteria",
)

BOUNDARY_TYPES = {
    "shared_rail_surface",
    "legacy_runtime_surface",
    "compatibility_boundary",
    "documentation_surface",
    "test_harness_surface",
    "unknown_surface",
}

MIGRATION_PRESSURES = {"none", "low", "medium", "high", "blocker", "unknown"}

COMPATIBILITY_PRESSURES = {
    "none",
    "keep_temporarily",
    "shrink_later",
    "shim_later",
    "migrate_later",
    "unknown",
}

REQUIRED_LATER_TICKETS = {
    "no_ticket_required",
    "source_code_migration_planning",
    "database_migration_planning",
    "compatibility_shim_planning",
    "shared_rail_contract_implementation_planning",
    "documentation_refresh_planning",
    "human_review_required",
}

PROPOSED_REVIEW_CATEGORIES = {
    "confirm_target_migration_candidate",
    "reclassify_as_legacy_runtime",
    "reclassify_as_compatibility_boundary",
    "reclassify_as_test_harness_guard",
    "reclassify_as_frozen_doc",
    "requires_more_review",
}

LIKELY_SURFACE_TYPES = {
    "event_contract",
    "journal_contract",
    "approval_gate",
    "risk_gate",
    "execution_intent",
    "dashboard_api",
    "data_layer",
    "database_persistence",
    "runtime_internal",
    "documentation",
    "test_harness",
    "unknown",
}

RECOMMENDED_REVIEW_ACTIONS = {
    "plan_source_code_migration",
    "plan_database_migration",
    "plan_compatibility_shim",
    "keep_as_legacy_runtime",
    "keep_as_test_guard",
    "leave_frozen_doc",
    "request_human_review",
}

RISK_LEVELS = {"low", "medium", "high", "blocker", "unknown"}

ALLOWED_ASSIGNMENTS = {
    "architecture alignment stage": {"shared_rail_contract_review_planning"},
    "review artifact status": {
        "planning_created",
        "no_review_table_created",
        "later_review_ticket_required",
        "migration_not_approved",
    },
    "canonical id posture": {
        "condition_id_token_id_outcome_target_contract",
        "canonical_ids_required_at_true_shared_rail_boundaries",
        "canonical_id_enforcement_not_complete",
    },
    "market id posture": {
        "legacy_compatibility_identifier",
        "allowed_only_at_approved_compatibility_boundaries",
        "not_target_shared_rail_identifier",
        "migration_requires_later_approval",
    },
    "boundary type": BOUNDARY_TYPES,
    "migration pressure": MIGRATION_PRESSURES,
    "compatibility pressure": COMPATIBILITY_PRESSURES,
    "required later ticket": REQUIRED_LATER_TICKETS,
    "proposed review category": PROPOSED_REVIEW_CATEGORIES,
    "likely surface type": LIKELY_SURFACE_TYPES,
    "recommended review action": RECOMMENDED_REVIEW_ACTIONS,
    "risk level": RISK_LEVELS,
    "implementation posture": {
        "planning_only",
        "no_runtime_refactor",
        "no_database_migration",
        "no_source_code_migration",
        "no_source_fetching",
        "no_provider_connector",
        "no_scoring_backtesting",
        "no_execution_trading",
        "no_production_behavior",
    },
    "weather bot posture": {
        "weather_bot_hold_checkpoint_after_offline_ingestion_closeout",
        "weather_bot_provider_connectors_not_approved",
        "weather_bot_source_fetching_not_approved",
        "weather_bot_scoring_runtime_trading_not_approved",
    },
    "evidence status": {"source_backed", "reviewer_inferred", "missing", "conflicting", "not_applicable"},
    "label confidence": {"confirmed", "unclear", "unknown"},
}

ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read_artifact() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing section: {heading}"
    section = match.group("section")
    assert section.strip(), f"Section is empty: {heading}"
    return section


def _machine_section(text: str) -> str:
    match = re.search(
        rf"^{re.escape(MACHINE_HEADING)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, "Machine-checkable shared-rail contract review assignment section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable shared-rail contract review assignment section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_planning_prd_exists_and_contains_canonical_id() -> None:
    assert ARTIFACT_PATH.exists(), f"Missing planning artifact: {ARTIFACT_PATH}"
    assert CANONICAL_ID in _read_artifact()


def test_required_sections_appear() -> None:
    text = _read_artifact()
    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text, f"Missing required section: {section}"
        _section(text, section)


def test_relationships_to_architecture_alignment_artifacts_appear() -> None:
    text = _read_artifact()
    assert "Relationship to MEG-ARCH-ALIGN-01" in text
    assert "`MEG-ARCH-ALIGN-01` established" in text
    assert "Relationship to MEG-ARCH-ALIGN-02" in text
    assert "`MEG-ARCH-ALIGN-02` planned" in text
    assert "Relationship to MEG-ARCH-ALIGN-03" in text
    assert "`MEG-ARCH-ALIGN-03` created" in text


def test_planning_only_scope_and_non_implementation_boundaries_are_explicit() -> None:
    text = _read_artifact()
    required_statements = (
        "This is planning only.",
        "No runtime refactor is implemented.",
        "No database migration is implemented.",
        "No source-code migration is implemented.",
        "No provider connector is implemented.",
        "No source fetching is implemented.",
        "No scoring/backtesting is implemented.",
        "No runtime behavior is implemented.",
        "No execution/trading/autonomy is implemented.",
        "No production behavior is implemented.",
        "This ticket does not approve migration work.",
        "This ticket does not approve compatibility shims.",
        "This ticket does not approve DB/schema changes.",
        "This ticket does not approve provider connectors.",
        "This ticket does not approve source fetching.",
        "This ticket does not approve Weather Bot provider/source/scoring/runtime/trading expansion.",
    )
    for statement in required_statements:
        assert statement in text, f"Missing scope statement: {statement}"


def test_identifier_contract_and_market_id_compatibility_posture_are_explicit() -> None:
    text = _read_artifact()
    assert "`condition_id`, `token_id`, and `outcome` remain the target shared-rail identifier contract" in text
    assert "`market_id` remains legacy/compatibility unless a later explicit boundary approves otherwise" in text
    assert "Target-migration candidates require separate human review before implementation." in text
    assert "Compatibility-boundary candidates require separate human review before implementation." in text
    assert "Future implementation/refactor/migration work requires separate explicit approval." in text


def test_future_output_formats_and_closed_sets_appear() -> None:
    text = _read_artifact()
    shared_section = _section(text, "Future shared-rail contract output format")
    migration_section = _section(text, "Future migration-candidate review output format")

    for column in (
        "surface_name",
        "owning_path_or_module",
        "current_identifier_contract",
        "target_identifier_contract",
        "boundary_type",
        "migration_pressure",
        "compatibility_pressure",
        "required_later_ticket",
        "reviewer_notes",
    ):
        assert f"- {column}" in shared_section

    for column in (
        "path",
        "current_category",
        "proposed_review_category",
        "current_identifier_usage",
        "target_identifier_contract",
        "likely_surface_type",
        "risk_level",
        "recommended_review_action",
        "reviewer_notes",
    ):
        assert f"- {column}" in migration_section

    for allowed_set in (
        BOUNDARY_TYPES,
        MIGRATION_PRESSURES,
        COMPATIBILITY_PRESSURES,
        REQUIRED_LATER_TICKETS,
        PROPOSED_REVIEW_CATEGORIES,
        LIKELY_SURFACE_TYPES,
        RECOMMENDED_REVIEW_ACTIONS,
        RISK_LEVELS,
    ):
        for value in allowed_set:
            assert value in text, f"Missing closed-set value: {value}"



def test_future_output_sections_define_schemas_without_actual_review_tables() -> None:
    text = _read_artifact()
    for heading in (
        "Future shared-rail contract output format",
        "Future migration-candidate review output format",
    ):
        section = _section(text, heading)
        assert "does not create the actual table yet" in section
        table_lines = [line for line in section.splitlines() if line.strip().startswith("|")]
        assert not table_lines, f"{heading} must define schema bullets only, not an actual output table"

def test_weather_bot_hold_checkpoint_posture_appears() -> None:
    text = _read_artifact()
    assert "Weather Bot remains at the hold/checkpoint posture" in text
    assert "weather_bot_hold_checkpoint_after_offline_ingestion_closeout" in text
    assert "weather_bot_provider_connectors_not_approved" in text
    assert "weather_bot_source_fetching_not_approved" in text
    assert "weather_bot_scoring_runtime_trading_not_approved" in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _read_artifact()
    section = _machine_section(text)
    assert "## Acceptance criteria" not in section
    assert "- architecture alignment stage: shared_rail_contract_review_planning" in section

    synthetic_text = (
        f"{MACHINE_HEADING}\n"
        "- architecture alignment stage: shared_rail_contract_review_planning\n"
        "\n## Acceptance criteria\n"
        "- architecture alignment stage: unapproved_value\n"
    )
    synthetic_assignments = _assignments(synthetic_text)
    assert synthetic_assignments == {
        "architecture alignment stage": {"shared_rail_contract_review_planning"}
    }


def test_every_allowed_closed_set_machine_checkable_value_appears() -> None:
    assignments = _assignments(_read_artifact())
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert field in assignments, f"Missing assignment field: {field}"
        missing = allowed_values - assignments[field]
        assert not missing, f"Missing allowed values for {field}: {sorted(missing)}"


def test_no_unapproved_actual_assignment_values_appear() -> None:
    assignments = _assignments(_read_artifact())
    unexpected_fields = set(assignments) - set(ALLOWED_ASSIGNMENTS)
    assert not unexpected_fields, f"Unexpected assignment fields: {sorted(unexpected_fields)}"

    for field, observed_values in assignments.items():
        unapproved = observed_values - ALLOWED_ASSIGNMENTS[field]
        assert not unapproved, f"Unapproved values for {field}: {sorted(unapproved)}"
