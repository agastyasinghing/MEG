"""Static checks for MEG-ARCH-ALIGN-02 market_id inventory planning.

These tests validate a planning-only PRD for classifying current legacy
``market_id`` usage. They use only Python standard library modules and do not
create migrations, refactors, runtime behavior, connectors, source fetching,
scoring, backtesting, execution, trading, autonomy, or production behavior.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / "docs/prd/MEG-ARCH-ALIGN-02_MARKET_ID_INVENTORY_CLASSIFICATION_PLANNING.md"
CANONICAL_ID = "MEG-ARCH-ALIGN-02"
MACHINE_HEADING = "## Machine-checkable market_id inventory assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to MEG-ARCH-ALIGN-01",
    "Inventory objective",
    "Classification categories",
    "Legacy whale-runtime usage",
    "Compatibility-boundary usage",
    "Target-migration candidates",
    "Out-of-scope implementation boundaries",
    "Inventory method",
    "Classification method",
    "Expected inventory output format",
    "Review and approval requirements",
    "Blocked future work until classification",
    "Machine-checkable market_id inventory assignments",
    "Acceptance criteria",
)

REQUIRED_SCOPE_STATEMENTS = (
    "This document is a planning-only artifact",
    "This ticket creates only an inventory/classification planning artifact.",
    "It does not create the actual inventory output unless explicitly approved later in a separate ticket.",
    "No migration is implemented.",
    "No runtime refactor is implemented.",
    "No source-code migration is implemented.",
    "No database schema change is implemented.",
    "No database migration is implemented.",
    "No source fetching is implemented.",
    "No provider/API connector is implemented.",
    "No scoring/backtesting is implemented.",
    "No execution/trading/autonomy is implemented.",
    "No production behavior is implemented.",
)

REQUIRED_IDENTIFIER_AND_ARCHITECTURE_MARKERS = (
    "`MEG-ARCH-ALIGN-01` established that MEG is in a dual-architecture transition.",
    "The older whale runtime remains present and still uses `market_id`",
    "the newer Phase 0A canonical rail targets `condition_id`, `token_id`, and `outcome`",
    "`market_id` remains legacy/compatibility unless explicitly classified",
    "The target shared-rail identifier contract remains `condition_id`, `token_id`, and `outcome`.",
    "`market_id` is not the target shared-rail identifier.",
    "Every current `market_id` usage should eventually be classified before shared-rail feature expansion.",
)

CLASSIFICATION_CATEGORIES = (
    "legacy_whale_runtime",
    "approved_compatibility_boundary",
    "target_migration_candidate",
    "frozen_historical_doc",
    "test_harness_guard",
    "unknown_requires_review",
)

FUTURE_INVENTORY_FIELDS = (
    "path",
    "line_count",
    "current_category",
    "proposed_category",
    "rationale",
    "recommended_next_action",
    "risk_level",
    "reviewer_notes",
)

RECOMMENDED_METHOD_MARKERS = (
    "Use a static text scan for the literal `market_id`.",
    "Compare observed files and line counts against `tests/core/canonical_id_allowlist.py`.",
    "Classify each file by path and architectural role.",
    "Do not change runtime code during inventory.",
    "Do not shrink or expand the allowlist without explicit review.",
    "Produce a later inventory artifact only in a separate ticket.",
)

WEATHER_BOT_MARKERS = (
    "Weather Bot remains hold/checkpoint for provider/source/scoring/runtime/trading work.",
    "Weather Bot provider connectors are not approved.",
    "Weather Bot source fetching is not approved.",
    "Weather Bot scoring/runtime/trading work is not approved by this ticket.",
)

ALLOWED_ASSIGNMENTS = {
    "architecture alignment stage": {
        "market_id_inventory_classification_planning",
    },
    "inventory status": {
        "inventory_not_created",
        "inventory_method_defined",
        "classification_schema_defined",
        "later_inventory_ticket_required",
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
        "inventory_required_before_expansion",
    },
    "classification category": set(CLASSIFICATION_CATEGORIES),
    "future inventory field": set(FUTURE_INVENTORY_FIELDS),
    "recommended next action": {
        "keep_as_legacy_boundary",
        "wrap_with_compatibility_shim_later",
        "migrate_to_canonical_ids_later",
        "leave_frozen_doc",
        "keep_test_guard",
        "needs_human_review",
    },
    "risk level": {
        "low",
        "medium",
        "high",
        "blocker",
        "unknown",
    },
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
    "evidence status": {
        "source_backed",
        "reviewer_inferred",
        "missing",
        "conflicting",
        "not_applicable",
    },
    "label confidence": {
        "confirmed",
        "unclear",
        "unknown",
    },
}

ASSIGNMENT_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>\S+)\s*$", re.MULTILINE)


def _read_prd() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def _machine_section(text: str) -> str:
    match = re.search(
        rf"^{re.escape(MACHINE_HEADING)}\n(?P<section>.*?)(?:\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, "Machine-checkable market_id inventory assignment section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable market_id inventory assignment section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_inventory_planning_prd_exists_and_contains_canonical_id() -> None:
    assert PRD_PATH.exists(), f"Missing inventory classification PRD: {PRD_PATH}"
    assert CANONICAL_ID in _read_prd()


def test_required_sections_appear() -> None:
    text = _read_prd()
    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text, f"Missing required section: {section}"


def test_relationship_to_arch_align_01_appears() -> None:
    text = _read_prd()
    assert "Relationship to MEG-ARCH-ALIGN-01" in text
    assert "`MEG-ARCH-ALIGN-01` established" in text
    assert "This document follows `MEG-ARCH-ALIGN-01`" in text


def test_planning_only_and_non_implementation_scope_is_explicit() -> None:
    text = _read_prd()
    for statement in REQUIRED_SCOPE_STATEMENTS:
        assert statement in text, f"Missing required scope statement: {statement}"


def test_identifier_compatibility_and_architecture_markers_are_explicit() -> None:
    text = _read_prd()
    for marker in REQUIRED_IDENTIFIER_AND_ARCHITECTURE_MARKERS:
        assert marker in text, f"Missing identifier/architecture marker: {marker}"


def test_classification_categories_appear() -> None:
    text = _read_prd()
    for category in CLASSIFICATION_CATEGORIES:
        assert category in text, f"Missing classification category: {category}"


def test_expected_future_inventory_output_fields_appear() -> None:
    text = _read_prd()
    for field in FUTURE_INVENTORY_FIELDS:
        assert field in text, f"Missing future inventory field: {field}"


def test_recommended_future_inventory_method_appears() -> None:
    text = _read_prd()
    positions = []
    for marker in RECOMMENDED_METHOD_MARKERS:
        position = text.find(marker)
        assert position != -1, f"Missing inventory method marker: {marker}"
        positions.append(position)
    assert positions == sorted(positions), "Recommended inventory method is out of order"


def test_weather_bot_hold_checkpoint_posture_appears() -> None:
    text = _read_prd()
    for marker in WEATHER_BOT_MARKERS:
        assert marker in text, f"Missing Weather Bot marker: {marker}"


def test_machine_checkable_assignment_section_is_section_scoped() -> None:
    text = _read_prd()
    section = _machine_section(text)
    assert "## Acceptance criteria" not in section
    assert "- architecture alignment stage: market_id_inventory_classification_planning" in section


def test_every_allowed_closed_set_value_appears() -> None:
    assignments = _assignments(_read_prd())
    for field, allowed_values in ALLOWED_ASSIGNMENTS.items():
        assert field in assignments, f"Missing assignment field: {field}"
        missing = allowed_values - assignments[field]
        assert not missing, f"Missing allowed values for {field}: {sorted(missing)}"


def test_no_unapproved_actual_assignment_values_appear() -> None:
    assignments = _assignments(_read_prd())
    unexpected_fields = set(assignments) - set(ALLOWED_ASSIGNMENTS)
    assert not unexpected_fields, f"Unexpected assignment fields: {sorted(unexpected_fields)}"

    for field, observed_values in assignments.items():
        unapproved = observed_values - ALLOWED_ASSIGNMENTS[field]
        assert not unapproved, f"Unapproved values for {field}: {sorted(unapproved)}"
