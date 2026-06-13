"""Static checks for MEG-ARCH-ALIGN-06 migration-candidate review artifact.

These tests validate a docs/static-test-only review artifact using only the
Python standard library. They do not create runtime refactors, database
migrations, source-code migrations, provider connectors, source fetching,
scoring, backtesting, execution, trading, autonomy, production behavior,
compatibility shims, schema changes, generated data, fixtures, workflows, or
dependencies.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/architecture/MEG-ARCH-ALIGN-06_MIGRATION_CANDIDATE_REVIEW.md"
CANONICAL_ID = "MEG-ARCH-ALIGN-06"
MACHINE_HEADING = "## Machine-checkable migration-candidate review artifact assignments"
TABLE_HEADING = "Migration-candidate review table"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to MEG-ARCH-ALIGN-01",
    "Relationship to MEG-ARCH-ALIGN-02",
    "Relationship to MEG-ARCH-ALIGN-03",
    "Relationship to MEG-ARCH-ALIGN-04",
    "Relationship to MEG-ARCH-ALIGN-05",
    "Review method",
    "Migration-candidate review table",
    "Summary by likely surface type",
    "High-risk candidates",
    "Human-review-required candidates",
    "Explicit non-implementation boundaries",
    "Recommended next actions",
    "Machine-checkable migration-candidate review artifact assignments",
    "Acceptance criteria",
)

TABLE_COLUMNS = (
    "path",
    "current_category",
    "proposed_review_category",
    "current_identifier_usage",
    "target_identifier_contract",
    "likely_surface_type",
    "risk_level",
    "recommended_review_action",
    "reviewer_notes",
)

REQUIRED_PATHS = {
    "meg/core/events.py",
    "meg/core/logger.py",
    "meg/dashboard/api/main.py",
    "meg/dashboard/ui/src/App.jsx",
    "meg/data_layer/clob_client.py",
    "meg/data_layer/polygon_feed.py",
    "meg/data_layer/wallet_registry.py",
    "meg/db/models.py",
    "meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py",
    "meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py",
    "meg/execution/entry_filter.py",
    "meg/execution/order_router.py",
    "meg/execution/slippage_guard.py",
    "meg/agent_core/risk_controller.py",
    "meg/telegram/bot.py",
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

RISK_LEVELS = {"low", "medium", "high", "blocker", "unknown"}

RECOMMENDED_REVIEW_ACTIONS = {
    "plan_source_code_migration",
    "plan_database_migration",
    "plan_compatibility_shim",
    "keep_as_legacy_runtime",
    "keep_as_test_guard",
    "leave_frozen_doc",
    "request_human_review",
}

ALLOWED_ASSIGNMENTS = {
    "architecture alignment stage": {"migration_candidate_review_artifact"},
    "review artifact status": {
        "review_artifact_created",
        "migration_candidate_table_created",
        "migration_not_approved",
        "compatibility_shim_not_approved",
        "later_implementation_ticket_required",
    },
    "review coverage status": {
        "target_migration_candidates_reviewed_as_planning_inputs",
        "high_risk_candidates_identified",
        "human_review_required_candidates_identified",
        "unknowns_explicitly_marked",
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
    "proposed review category": PROPOSED_REVIEW_CATEGORIES,
    "likely surface type": LIKELY_SURFACE_TYPES,
    "recommended review action": RECOMMENDED_REVIEW_ACTIONS,
    "risk level": RISK_LEVELS,
    "implementation posture": {
        "review_artifact_only",
        "no_runtime_refactor",
        "no_database_migration",
        "no_source_code_migration",
        "no_source_fetching",
        "no_provider_connector",
        "no_scoring_backtesting",
        "no_execution_trading",
        "no_production_behavior",
        "no_compatibility_shim",
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
    assert match, "Machine-checkable migration-candidate review assignment section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable migration-candidate review assignment section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def _table_rows(text: str) -> list[dict[str, str]]:
    section = _section(text, TABLE_HEADING)
    table_lines = [line for line in section.splitlines() if line.startswith("|")]
    assert len(table_lines) >= 3, "Migration-candidate review table is missing rows"

    header = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    assert tuple(header) == TABLE_COLUMNS
    separator = [cell.strip() for cell in table_lines[1].strip("|").split("|")]
    assert len(separator) == len(TABLE_COLUMNS)

    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(cells) == len(TABLE_COLUMNS), f"Unexpected table column count in line: {line}"
        rows.append(dict(zip(TABLE_COLUMNS, cells)))
    return rows


def test_review_artifact_exists_and_canonical_id_appears() -> None:
    assert ARTIFACT_PATH.exists()
    assert CANONICAL_ID in _read_artifact()


def test_all_required_sections_appear() -> None:
    text = _read_artifact()
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_relationship_sections_reference_prior_architecture_alignment_tickets() -> None:
    text = _read_artifact()
    for ticket in (
        "MEG-ARCH-ALIGN-01",
        "MEG-ARCH-ALIGN-02",
        "MEG-ARCH-ALIGN-03",
        "MEG-ARCH-ALIGN-04",
        "MEG-ARCH-ALIGN-05",
    ):
        section = _section(text, f"Relationship to {ticket}")
        assert ticket in section


def test_review_artifact_docs_static_only_scope_is_stated() -> None:
    text = _read_artifact()
    assert "review artifact only" in text
    assert "docs/static-test-only" in text
    assert "documentation/static-evidence level" in text


def test_non_implementation_boundaries_are_stated() -> None:
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


def test_target_identifier_contract_and_legacy_compatibility_posture_are_stated() -> None:
    text = _read_artifact()
    assert "condition_id" in text
    assert "token_id" in text
    assert "outcome" in text
    assert "remain the target shared-rail identifier contract" in text
    assert "market_id` remains legacy/compatibility" in text
    assert "market_id` remains legacy/compatibility unless a later explicit boundary approves otherwise" in text
    assert "Target-migration candidates require separate human review before implementation." in text
    assert "Future implementation/refactor/migration work requires separate explicit approval." in text


def test_migration_candidate_review_table_has_exact_columns_and_required_rows() -> None:
    rows = _table_rows(_read_artifact())
    observed_paths = {row["path"].strip("`") for row in rows}
    missing_paths = REQUIRED_PATHS - observed_paths
    assert not missing_paths, f"Missing required path rows: {sorted(missing_paths)}"


def test_table_closed_set_values_are_allowed() -> None:
    for row in _table_rows(_read_artifact()):
        assert row["proposed_review_category"] in PROPOSED_REVIEW_CATEGORIES
        assert row["likely_surface_type"] in LIKELY_SURFACE_TYPES
        assert row["risk_level"] in RISK_LEVELS
        assert row["recommended_review_action"] in RECOMMENDED_REVIEW_ACTIONS


def test_high_risk_and_human_review_sections_appear() -> None:
    text = _read_artifact()
    high_risk_section = _section(text, "High-risk candidates")
    human_review_section = _section(text, "Human-review-required candidates")
    assert "high-risk" in high_risk_section or "blocker" in high_risk_section
    assert "Human review is required" in human_review_section
    assert "meg/execution/order_router.py" in human_review_section


def test_weather_bot_hold_checkpoint_posture_appears() -> None:
    text = _read_artifact()
    assert "hold/checkpoint posture" in text
    assert "weather_bot_hold_checkpoint_after_offline_ingestion_closeout" in text
    assert "weather_bot_provider_connectors_not_approved" in text
    assert "weather_bot_source_fetching_not_approved" in text
    assert "weather_bot_scoring_runtime_trading_not_approved" in text


def test_machine_checkable_assignment_section_exists_and_is_section_scoped() -> None:
    text = _read_artifact()
    section = _machine_section(text)
    assert "## Acceptance criteria" not in section
    assert "- architecture alignment stage: migration_candidate_review_artifact" in section

    synthetic_text = (
        f"{MACHINE_HEADING}\n"
        "- architecture alignment stage: migration_candidate_review_artifact\n"
        "\n## Acceptance criteria\n"
        "- architecture alignment stage: unapproved_value\n"
    )
    synthetic_assignments = _assignments(synthetic_text)
    assert synthetic_assignments == {
        "architecture alignment stage": {"migration_candidate_review_artifact"}
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
