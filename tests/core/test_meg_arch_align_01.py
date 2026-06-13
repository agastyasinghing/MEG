"""Static checks for MEG-ARCH-ALIGN-01 architecture alignment planning.

These tests validate a planning-only document that freezes the boundary between
legacy whale-runtime identifiers and the newer canonical Phase 0A rail. They do
not create migrations, refactors, runtime behavior, connectors, source fetching,
scoring, backtesting, execution, trading, autonomy, or production behavior.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRD_PATH = REPO_ROOT / "docs/prd/MEG-ARCH-ALIGN-01_ARCHITECTURE_ALIGNMENT_PLANNING.md"
CANONICAL_ID = "MEG-ARCH-ALIGN-01"
MACHINE_HEADING = "## Machine-checkable architecture alignment assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Why this alignment pass is needed",
    "Current dual-architecture state",
    "Legacy whale runtime boundary",
    "New Phase 0A canonical rail boundary",
    "Weather Bot boundary",
    "Canonical identifier contract",
    "`market_id` compatibility window",
    "Strategy-agnostic proposal/event target",
    "Runtime/pubsub/journaling concerns",
    "Database and persistence concerns",
    "README/onboarding concerns",
    "Explicit non-implementation boundaries",
    "Recommended alignment sequence",
    "Blocked future work until alignment",
    "Machine-checkable architecture alignment assignments",
    "Acceptance criteria",
)

REQUIRED_SCOPE_STATEMENTS = (
    "This document is a planning-only architecture alignment artifact",
    "This planning pass implements no product behavior.",
    "No runtime refactor is implemented.",
    "No database schema change is implemented.",
    "No database migration is implemented.",
    "No source-fetching work is implemented.",
    "No provider/API connector work is implemented.",
    "No scoring or backtesting work is implemented.",
    "No execution, trading, order placement, autonomy, live behavior, or production behavior is implemented.",
    "This ticket is planning only.",
    "No source-fetching implementation is created.",
    "No provider/API connector implementation is created.",
    "No scoring/backtesting implementation is created.",
    "No execution, trading, order-placement, or autonomy implementation is created.",
    "No production behavior is created.",
)

REQUIRED_ARCHITECTURE_MARKERS = (
    "MEG is in a dual architecture in transition.",
    "The legacy whale runtime remains present",
    "the Phase 0A canonical rail is also present",
    "The older whale reaction bot runtime can be summarized as:",
    "Polygon RPC",
    "Telegram approval",
    "Order router",
    "The Phase 0A canonical rail expects the canonical identifier contract",
    "`condition_id`",
    "`token_id`",
    "`outcome`",
    "`market_id` remains a legacy/compatibility identifier",
    "not the target shared-rail identifier",
    "Weather Bot remains at a hold/checkpoint posture after Stage 2 offline ingestion closeout.",
    "Weather Bot provider connectors are not approved.",
    "Weather Bot source fetching is not approved.",
    "Weather Bot scoring is not approved.",
    "Weather Bot runtime behavior is not approved.",
    "Weather Bot trading, execution, order placement, autonomy, live behavior, and production behavior are not approved.",
)

RECOMMENDED_SEQUENCE = (
    "1. Inventory current `market_id` usage.",
    "2. Classify each usage as legacy runtime, compatibility boundary, or target-migration candidate.",
    "3. Define true shared-rail boundary contracts.",
    "4. Define strategy-agnostic event/proposal contract.",
    "5. Define allowed whale-runtime compatibility shim behavior.",
    "6. Define DB/persistence migration planning requirements without implementing them.",
    "7. Define README/onboarding update requirements.",
    "8. Define later implementation tickets.",
)

ALLOWED_ASSIGNMENTS = {
    "architecture alignment stage": {
        "architecture_alignment_planning",
    },
    "current architecture state": {
        "dual_architecture_in_transition",
        "legacy_whale_runtime_present",
        "phase0a_canonical_rail_present",
        "weather_stage2_offline_ingestion_skeleton_closed_out",
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
    },
    "legacy runtime posture": {
        "whale_runtime_existing",
        "whale_runtime_must_not_expand_without_alignment",
        "whale_runtime_candidate_for_strategy_agnostic_wrapping",
    },
    "weather bot posture": {
        "weather_bot_hold_checkpoint_after_offline_ingestion_closeout",
        "weather_bot_provider_connectors_not_approved",
        "weather_bot_source_fetching_not_approved",
        "weather_bot_scoring_runtime_trading_not_approved",
    },
    "implementation posture": {
        "planning_only",
        "no_runtime_refactor",
        "no_database_migration",
        "no_source_fetching",
        "no_provider_connector",
        "no_scoring_backtesting",
        "no_execution_trading",
        "no_production_behavior",
    },
    "later gate posture": {
        "architecture_alignment_review",
        "market_id_inventory_ticket",
        "shared_rail_contract_planning_ticket",
        "strategy_agnostic_event_contract_planning_ticket",
        "readme_onboarding_refresh_ticket",
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
    assert match, "Machine-checkable architecture alignment assignment section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable architecture alignment assignment section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_architecture_alignment_prd_exists_and_contains_canonical_id() -> None:
    assert PRD_PATH.exists(), f"Missing architecture alignment PRD: {PRD_PATH}"
    assert CANONICAL_ID in _read_prd()


def test_required_sections_appear() -> None:
    text = _read_prd()
    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text, f"Missing required section: {section}"


def test_planning_only_and_non_implementation_scope_is_explicit() -> None:
    text = _read_prd()
    for statement in REQUIRED_SCOPE_STATEMENTS:
        assert statement in text, f"Missing required scope statement: {statement}"


def test_dual_architecture_identifier_and_weather_boundaries_are_explicit() -> None:
    text = _read_prd()
    for marker in REQUIRED_ARCHITECTURE_MARKERS:
        assert marker in text, f"Missing architecture marker: {marker}"


def test_recommended_alignment_sequence_appears_in_order() -> None:
    text = _read_prd()
    positions = []
    for step in RECOMMENDED_SEQUENCE:
        position = text.find(step)
        assert position != -1, f"Missing recommended alignment step: {step}"
        positions.append(position)
    assert positions == sorted(positions), "Recommended alignment sequence is out of order"


def test_machine_checkable_assignment_section_is_section_scoped() -> None:
    text = _read_prd()
    section = _machine_section(text)
    assert "## Acceptance criteria" not in section
    assert "- architecture alignment stage: architecture_alignment_planning" in section


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
