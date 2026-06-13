"""Static checks for MEG-ARCH-ALIGN-08 closeout checkpoint artifact.

These tests use only the Python standard library and validate docs/static-test-only
closeout posture. They do not create or approve runtime refactors, database
migrations, source-code migrations, provider connectors, source fetching,
scoring, backtesting, runtime behavior, execution, trading, autonomy, production
behavior, compatibility shims, schema changes, generated data, fixtures,
workflows, or dependencies.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/architecture/MEG-ARCH-ALIGN-08_ARCHITECTURE_ALIGNMENT_CLOSEOUT.md"
CANONICAL_ID = "MEG-ARCH-ALIGN-08"
MACHINE_HEADING = "## Machine-checkable architecture alignment closeout assignments"
RECOMMENDED_NEXT_ACTIONS_HEADING = "Recommended next actions"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Alignment sequence summary",
    "MEG-ARCH-ALIGN-01 summary",
    "MEG-ARCH-ALIGN-02 summary",
    "MEG-ARCH-ALIGN-03 summary",
    "MEG-ARCH-ALIGN-04 summary",
    "MEG-ARCH-ALIGN-05 summary",
    "MEG-ARCH-ALIGN-06 summary",
    "MEG-ARCH-ALIGN-07 summary",
    "Final architecture posture",
    "Canonical identifier posture",
    "market_id compatibility posture",
    "Weather Bot return posture",
    "Explicit non-implementation boundaries",
    "Remaining architecture risks",
    "Recommended next actions",
    "Machine-checkable architecture alignment closeout assignments",
    "Acceptance criteria",
)

ALLOWED_ASSIGNMENTS = {
    "architecture alignment stage": {"architecture_alignment_closeout_checkpoint"},
    "closeout status": {
        "alignment_sequence_reviewed",
        "align_01_complete",
        "align_02_complete",
        "align_03_complete",
        "align_04_complete",
        "align_05_complete",
        "align_06_complete",
        "align_07_complete",
        "ready_to_return_to_weather_bot_planning",
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
    "migration posture": {
        "migration_not_approved",
        "target_migration_candidates_are_review_labels_only",
        "later_human_review_required",
    },
    "compatibility posture": {
        "compatibility_boundaries_are_review_labels_only",
        "compatibility_shim_not_approved",
        "later_human_review_required",
    },
    "implementation posture": {
        "closeout_only",
        "no_runtime_refactor",
        "no_database_migration",
        "no_source_code_migration",
        "no_source_fetching",
        "no_provider_connector",
        "no_scoring_backtesting",
        "no_execution_trading",
        "no_production_behavior",
        "no_compatibility_shim",
        "no_schema_change",
    },
    "weather bot posture": {
        "weather_bot_return_to_planning_allowed",
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
    assert match, "Machine-checkable architecture alignment closeout assignment section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable architecture alignment closeout assignment section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def test_closeout_artifact_exists_and_canonical_id_appears() -> None:
    assert ARTIFACT_PATH.exists()
    assert CANONICAL_ID in _read_artifact()


def test_all_required_sections_appear() -> None:
    text = _read_artifact()
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_alignment_sequence_tickets_are_referenced() -> None:
    text = _read_artifact()
    for number in range(1, 8):
        ticket = f"MEG-ARCH-ALIGN-{number:02d}"
        assert ticket in text
        assert ticket in _section(text, f"{ticket} summary")


def test_closeout_and_docs_static_only_scope_are_stated() -> None:
    text = _read_artifact()
    assert "closeout/checkpoint only" in text
    assert "docs/static-test-only" in text
    assert "complete enough to return to Weather Bot planning work" in text


def test_weather_bot_return_is_limited_to_gated_planning() -> None:
    text = _read_artifact()
    assert "return to Weather Bot planning work" in text
    assert "Returning to Weather Bot means returning to gated planning/approval work" in text
    assert "not live/provider/runtime/trading implementation" in text


def test_target_identifier_contract_and_market_id_compatibility_are_stated() -> None:
    text = _read_artifact()
    assert "condition_id" in text
    assert "token_id" in text
    assert "outcome" in text
    assert "remain the target shared-rail identifier contract" in text
    assert "`market_id` remains legacy/compatibility" in text
    assert "not the target shared-rail identifier" in text


def test_review_label_postures_are_stated() -> None:
    text = _read_artifact()
    assert "Target-migration candidates remain review labels only." in text
    assert "Compatibility boundaries remain review labels only." in text


def test_no_implementation_or_approval_boundary_is_crossed() -> None:
    text = _read_artifact()
    required_phrases = (
        "No runtime refactor is implemented.",
        "No database migration is implemented.",
        "No source-code migration is implemented.",
        "No provider connector is implemented.",
        "No source fetching is implemented.",
        "No scoring/backtesting is implemented.",
        "No runtime behavior is implemented.",
        "No execution/trading/autonomy is implemented.",
        "No production behavior is implemented.",
        "No compatibility shim is implemented.",
        "No schema change is implemented.",
        "does not approve migration work",
        "does not approve compatibility shims",
        "does not approve DB/schema changes",
        "does not approve provider connectors",
        "does not approve source fetching",
        "does not approve Weather Bot provider/source/scoring/runtime/trading expansion",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_recommended_next_actions_do_not_recommend_forbidden_work() -> None:
    section = _section(_read_artifact(), RECOMMENDED_NEXT_ACTIONS_HEADING)
    assert "planning/approval ticket only" in section
    forbidden_recommendations = (
        "Recommend runtime refactor",
        "Recommend DB migration",
        "Recommend provider connectors",
        "Recommend source fetching",
        "Recommend scoring",
        "Recommend backtesting",
        "Recommend runtime behavior",
        "Recommend trading",
        "Recommend autonomy",
        "Recommend production behavior",
    )
    for phrase in forbidden_recommendations:
        assert phrase not in section


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _read_artifact()
    section = _machine_section(text)
    assert "## Acceptance criteria" not in section
    assert "- architecture alignment stage: architecture_alignment_closeout_checkpoint" in section

    synthetic_text = (
        f"{MACHINE_HEADING}\n"
        "- architecture alignment stage: architecture_alignment_closeout_checkpoint\n"
        "\n## Acceptance criteria\n"
        "- architecture alignment stage: unapproved_value\n"
    )
    synthetic_assignments = _assignments(synthetic_text)
    assert synthetic_assignments == {
        "architecture alignment stage": {"architecture_alignment_closeout_checkpoint"}
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
