"""Static checks for MEG-ARCH-ALIGN-03 market_id inventory artifact.

These tests validate a docs/static-inventory artifact only. They use Python
standard-library imports only and do not create migrations, refactors, runtime
behavior, connectors, source fetching, scoring, backtesting, execution,
trading, autonomy, or production behavior.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.core.canonical_id_allowlist import ALLOWED_MARKET_ID_OCCURRENCE_LINES

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_PATH = REPO_ROOT / "docs/architecture/MEG-ARCH-ALIGN-03_MARKET_ID_INVENTORY.md"
CANONICAL_ID = "MEG-ARCH-ALIGN-03"
MACHINE_HEADING = "## Machine-checkable market_id inventory assignments"

REQUIRED_SECTIONS = (
    "Status and scope",
    "Relationship to MEG-ARCH-ALIGN-01",
    "Relationship to MEG-ARCH-ALIGN-02",
    "Inventory method",
    "Classification categories",
    "Inventory table",
    "Summary by category",
    "High-risk target-migration candidates",
    "Compatibility-boundary candidates",
    "Frozen historical docs and test-harness guards",
    "Unknowns requiring review",
    "Explicit non-implementation boundaries",
    "Recommended next actions",
    "Machine-checkable market_id inventory assignments",
    "Acceptance criteria",
)

TABLE_COLUMNS = (
    "path",
    "line_count",
    "current_category",
    "proposed_category",
    "rationale",
    "recommended_next_action",
    "risk_level",
    "reviewer_notes",
)

CLASSIFICATION_CATEGORIES = {
    "legacy_whale_runtime",
    "approved_compatibility_boundary",
    "target_migration_candidate",
    "frozen_historical_doc",
    "test_harness_guard",
    "unknown_requires_review",
}

RECOMMENDED_NEXT_ACTIONS = {
    "keep_as_legacy_boundary",
    "wrap_with_compatibility_shim_later",
    "migrate_to_canonical_ids_later",
    "leave_frozen_doc",
    "keep_test_guard",
    "needs_human_review",
}

RISK_LEVELS = {"low", "medium", "high", "blocker", "unknown"}

ALLOWED_ASSIGNMENTS = {
    "architecture alignment stage": {"market_id_inventory_artifact"},
    "inventory artifact status": {
        "inventory_created",
        "line_counts_match_allowlist",
        "classifications_assigned",
        "human_review_required_before_migration",
    },
    "inventory coverage status": {
        "all_allowlist_paths_included",
        "no_unlisted_market_id_paths_allowed",
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
    "classification category": CLASSIFICATION_CATEGORIES,
    "recommended next action": RECOMMENDED_NEXT_ACTIONS,
    "risk level": RISK_LEVELS,
    "implementation posture": {
        "inventory_only",
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
    assert match, "Machine-checkable inventory assignment section is missing"
    section = match.group("section")
    assert section.strip(), "Machine-checkable inventory assignment section is empty"
    return section


def _assignments(text: str) -> dict[str, set[str]]:
    section = _machine_section(text)
    assignments: dict[str, set[str]] = {}
    for match in ASSIGNMENT_RE.finditer(section):
        assignments.setdefault(match.group("field"), set()).add(match.group("value"))
    return assignments


def _inventory_rows(text: str) -> list[dict[str, str]]:
    section = _section(text, "Inventory table")
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    assert len(lines) >= 3, "Inventory table is missing header, separator, or rows"
    header = tuple(cell.strip() for cell in lines[0].strip("|").split("|"))
    assert header == TABLE_COLUMNS, f"Unexpected inventory table columns: {header}"
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(cells) == len(TABLE_COLUMNS), f"Malformed inventory row: {line}"
        rows.append(dict(zip(TABLE_COLUMNS, cells)))
    return rows


def test_inventory_artifact_exists_and_contains_canonical_id() -> None:
    assert ARTIFACT_PATH.exists(), f"Missing inventory artifact: {ARTIFACT_PATH}"
    assert CANONICAL_ID in _read_artifact()


def test_required_sections_appear() -> None:
    text = _read_artifact()
    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text, f"Missing required section: {section}"


def test_relationships_to_prior_architecture_alignment_docs_appear() -> None:
    text = _read_artifact()
    assert "Relationship to MEG-ARCH-ALIGN-01" in text
    assert "`MEG-ARCH-ALIGN-01` established" in text
    assert "Relationship to MEG-ARCH-ALIGN-02" in text
    assert "`MEG-ARCH-ALIGN-02` planned this repository-level inventory" in text


def test_inventory_only_scope_and_non_implementation_boundaries_are_explicit() -> None:
    text = _read_artifact()
    required_statements = (
        "This is an inventory/classification artifact only.",
        "This is not a migration.",
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
    for statement in required_statements:
        assert statement in text, f"Missing scope statement: {statement}"


def test_identifier_contract_and_market_id_compatibility_posture_are_explicit() -> None:
    text = _read_artifact()
    assert "`condition_id`, `token_id`, and `outcome` remain the target shared-rail identifier contract" in text
    assert "`market_id` remains legacy/compatibility unless explicitly classified" in text
    assert "Future migration/refactor/compatibility-shim work requires separate explicit approval" in text
    assert "Weather Bot remains hold/checkpoint" in text


def test_inventory_table_paths_counts_and_closed_sets_match_allowlist() -> None:
    rows = _inventory_rows(_read_artifact())
    by_path = {row["path"].strip("`"): row for row in rows}
    assert len(by_path) == len(rows), "Inventory table contains duplicate paths"

    missing = sorted(set(ALLOWED_MARKET_ID_OCCURRENCE_LINES) - set(by_path))
    extra = sorted(set(by_path) - set(ALLOWED_MARKET_ID_OCCURRENCE_LINES))
    assert not missing, f"Allowlist paths missing from inventory: {missing}"
    assert not extra, f"Inventory paths missing from allowlist: {extra}"

    for path, expected_count in ALLOWED_MARKET_ID_OCCURRENCE_LINES.items():
        row = by_path[path]
        assert int(row["line_count"]) == expected_count, f"Count mismatch for {path}"
        assert row["current_category"] in CLASSIFICATION_CATEGORIES, path
        assert row["proposed_category"] in CLASSIFICATION_CATEGORIES, path
        assert row["recommended_next_action"] in RECOMMENDED_NEXT_ACTIONS, path
        assert row["risk_level"] in RISK_LEVELS, path


def test_machine_checkable_assignment_section_is_section_scoped() -> None:
    section = _machine_section(_read_artifact())
    assert "## Acceptance criteria" not in section
    assert "- architecture alignment stage: market_id_inventory_artifact" in section


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
