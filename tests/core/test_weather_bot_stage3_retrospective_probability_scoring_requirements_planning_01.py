"""Static tests for Weather Bot Stage 3 retrospective scoring requirements."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-STAGE3-RETROSPECTIVE-PROBABILITY-SCORING-REQUIREMENTS-PLANNING-01"
ARTIFACT = REPO_ROOT / "docs/prd" / f"{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_stage3_retrospective_probability_scoring_requirements_planning_01.py"
MACHINE_HEADING = "Machine-checkable assignments"

REQUIRED_SECTIONS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Controlling settlement-probability target",
    "Stage 3 prediction-record requirements",
    "Source-compatible label requirements",
    "Point-in-time and availability requirements",
    "Strict OOS split requirements",
    "Baseline requirements",
    "Scoring-rule applicability matrix",
    "Calibration and diagnostic requirements",
    "Threshold-bucket and stratification requirements",
    "Sample-sufficiency and uncertainty requirements",
    "Fail-closed and no-lookahead requirements",
    "Human-review and auditability requirements",
    "Explicit non-approvals",
    "Canonical routing posture",
    "Recommended next ticket",
    MACHINE_HEADING,
    "Acceptance criteria",
]

REQUIRED_ASSIGNMENTS = {
    ("weather bot planning stage", "weather_bot_stage3_retrospective_probability_scoring_requirements_planning"),
    ("immediate predecessor pr", "pr_357"),
    ("ticket lifecycle status", "docs_static_test_only"),
    ("ticket lifecycle status", "requirements_planning_only"),
    ("scoring target posture", "venue_defined_settlement_outcome"),
    ("scoring target posture", "generic_weather_target_rejected"),
    ("stage3 gate definition", "retrospective_probability_scoring_strict_oos"),
    ("prediction record status", "requirements_defined"),
    ("prediction record status", "runtime_schema_not_created"),
    ("label requirement status", "source_compatible_point_in_time_required"),
    ("split requirement status", "rolling_origin_or_walk_forward_required"),
    ("split requirement status", "random_shuffle_primary_split_rejected"),
    ("baseline requirement", "climatology"),
    ("baseline requirement", "persistence"),
    ("scoring execution posture", "not_approved"),
    ("probability generation posture", "not_approved"),
    ("backtesting posture", "not_approved"),
    ("persistence posture", "not_approved"),
    ("canonical routing field", "condition_id"),
    ("canonical routing field", "token_id"),
    ("canonical routing field", "outcome"),
    ("non routing field", "market_id"),
    ("derived identifier field", "token_outcome_pair"),
    ("next ticket recommendation", "stage3_probability_record_contract_planning"),
    ("evidence status", "requirements_planning_recorded"),
    ("label confidence", "confirmed"),
}

CLOSED_SETS = {
    "weather bot planning stage": {"weather_bot_stage3_retrospective_probability_scoring_requirements_planning"},
    "immediate predecessor pr": {"pr_357"},
    "ticket lifecycle status": {"docs_static_test_only", "requirements_planning_only"},
    "scoring target posture": {"venue_defined_settlement_outcome", "generic_weather_target_rejected"},
    "stage3 gate definition": {"retrospective_probability_scoring_strict_oos"},
    "prediction record status": {"requirements_defined", "runtime_schema_not_created"},
    "label requirement status": {"source_compatible_point_in_time_required"},
    "split requirement status": {"rolling_origin_or_walk_forward_required", "random_shuffle_primary_split_rejected"},
    "baseline requirement": {"climatology", "persistence"},
    "scoring execution posture": {"not_approved"},
    "probability generation posture": {"not_approved"},
    "backtesting posture": {"not_approved"},
    "persistence posture": {"not_approved"},
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "derived identifier field": {"token_outcome_pair"},
    "next ticket recommendation": {"stage3_probability_record_contract_planning"},
    "evidence status": {"requirements_planning_recorded"},
    "label confidence": {"confirmed"},
}

ASSIGNMENT_RE = re.compile(r"^- (?P<field>[a-z0-9 ][a-z0-9 -]*): (?P<value>[a-z0-9_]+)$", re.MULTILINE)


def _read() -> str:
    return ARTIFACT.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, heading
    body = match.group("body").strip()
    assert body, heading
    return body


def _actual_assignment_text(text: str) -> str:
    machine = _section(text, MACHINE_HEADING)
    marker = "Actual assignments:"
    assert marker in machine
    return machine.split(marker, 1)[1].split("Hybrid/custom values", 1)[0]


def _assignment_pairs(text: str) -> set[tuple[str, str]]:
    return {(m.group("field"), m.group("value")) for m in ASSIGNMENT_RE.finditer(_actual_assignment_text(text))}


def test_document_exists_canonical_id_and_required_sections() -> None:
    text = _read()
    assert text.startswith(f"# {CANONICAL_ID}")
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for heading in REQUIRED_SECTIONS:
        _section(text, heading)


def test_test_file_uses_only_stdlib_plus_pytest_and_no_production_imports() -> None:
    tree = ast.parse(TEST_PATH.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert set(imports) <= {"__future__", "ast", "re", "pathlib"}
    assert all(not name.startswith("meg") for name in imports)


def test_predecessor_merge_commit_and_no_superseding_state_are_recorded() -> None:
    text = _read()
    for phrase in [
        "PR #357 merged",
        "3ede1b5e2eb019e3195ff3abf023442a69a3f23b",
        "not a preview merge SHA",
        "no newer controlling Weather Bot state superseding PR #357",
        "immediate merged predecessor as `pr_357`",
    ]:
        assert phrase in text


def test_target_is_venue_defined_settlement_not_generic_weather() -> None:
    text = _read()
    for phrase in [
        "venue-defined settlement outcome",
        "canonical token/outcome route",
        "does not score generic weather",
        "generic_weather_target_rejected",
        "retrospective_probability_scoring_strict_oos",
    ]:
        assert phrase in text


def test_prediction_record_fields_are_requirements_only() -> None:
    section = _section(_read(), "Stage 3 prediction-record requirements")
    for phrase in [
        "condition_id",
        "token_id",
        "outcome",
        "prediction as-of timestamp",
        "target settlement-rule identity",
        "market family",
        "source and station compatibility",
        "threshold, unit, comparator, and measurement window",
        "archive/finality layer",
        "forecast or input publication availability",
        "probability value and the outcome it refers to",
        "method/version identity",
        "provenance needed for later scoring",
        "planning requirements only",
        "does not create a runtime schema, dataclass",
    ]:
        assert phrase in section


def test_label_availability_revision_and_no_lookahead_rules_are_present() -> None:
    text = _read()
    for phrase in [
        "source-compatible",
        "resolver-accurate",
        "archive-layer explicit",
        "revision-aware",
        "unavailable before their legitimate publication or resolution time",
        "as-of joins",
        "publication time rather than forecast initialization time",
        "future forecast cycles",
        "final-archive leakage",
        "hindsight station/source/provider selection",
        "blocked, conflicted",
        "must not be scored as ordinary usable labels",
    ]:
        assert phrase in text


def test_split_and_baseline_requirements_are_complete() -> None:
    text = _read()
    for phrase in [
        "rolling-origin or walk-forward OOS evaluation",
        "leave-station-out validation",
        "leave-year-out validation",
        "family-stratified evaluation",
        "immutable train/calibration/test boundaries",
        "predeclared split and tuning rules",
        "Shuffled random validation is rejected as the primary time-series split",
        "climatology",
        "persistence",
        "Market prices must not be treated as frictionless truth",
        "does not introduce Stage 4 executable-cost analysis",
    ]:
        assert phrase in text


def test_scoring_applicability_is_conditional_and_non_executing() -> None:
    section = _section(_read(), "Scoring-rule applicability matrix")
    rows = {}
    for line in section.splitlines():
        if not line.startswith("| ") or "---" in line or "Prediction representation" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(cells) == 3
        representation, diagnostics, boundary = cells
        rows[representation] = {"diagnostics": diagnostics, "boundary": boundary}

    assert rows == {
        "binary outcome probabilities": {
            "diagnostics": "Brier score, log score, reliability diagrams",
            "boundary": "Applies only when the prediction is a probability for the canonical venue-defined binary settlement outcome.",
        },
        "binary calibration analysis": {
            "diagnostics": "Brier decomposition",
            "boundary": "Applies only to binary probability records with enough predeclared samples for decomposition claims.",
        },
        "full predictive distributions": {
            "diagnostics": "CRPS and PIT diagnostics",
            "boundary": "Applies only when a full predictive distribution is explicitly represented.",
        },
        "finite ensembles": {
            "diagnostics": "rank histograms where appropriate",
            "boundary": "Applies only when finite ensemble members are represented and comparable to the verifying observation.",
        },
        "rare-event or near-threshold distributional evaluation": {
            "diagnostics": "threshold-weighted CRPS where justified",
            "boundary": "Applies only when the future design justifies rare-event or near-threshold weighting before evaluation.",
        },
    }
    assert "Not every metric applies to every prediction representation" in section
    assert "No metric may be calculated by this ticket" in section


def test_calibration_sample_and_stratification_requirements_are_present() -> None:
    text = _read()
    for phrase in [
        "reproducible bins",
        "sample counts",
        "uncertainty intervals",
        "empty or sparse buckets",
        "market family",
        "threshold distance",
        "forecast horizon",
        "station/source compatibility",
        "trap category",
        "season/regime when supported",
        "archive layer",
        "predeclare sample-sufficiency thresholds",
        "fabricates no numeric minimum sample threshold",
        "Insufficient samples must block claims rather than be silently pooled",
    ]:
        assert phrase in text


def test_no_fabricated_sample_minimum_exists() -> None:
    text = _read().lower()
    forbidden_patterns = [
        r"minimum sample(?: size)?(?: is|:) \d+",
        r"at least \d+ samples",
        r"n\s*>=\s*\d+",
        r"\bmin(?:imum)?[_ -]n\s*[:=]\s*\d+",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text), pattern


def test_no_scoring_runtime_or_persistence_approval_exists() -> None:
    text = _read()
    for phrase in [
        "does not approve probability generation",
        "does not approve owner-decision capture",
        "runtime schemas, dataclasses",
        "scoring execution posture: not_approved",
        "probability generation posture: not_approved",
        "backtesting posture: not_approved",
        "persistence posture: not_approved",
    ]:
        assert phrase in text
    assert "scoring output is approved" not in text
    assert "runtime behavior is approved" not in text


def test_assignments_are_section_scoped_exact_complete_and_closed() -> None:
    text = _read()
    assignment_text = _actual_assignment_text(text)
    observed = _assignment_pairs(text)
    assert observed == REQUIRED_ASSIGNMENTS
    for field, values in CLOSED_SETS.items():
        closed_line = f"- {field}: "
        assert closed_line in _section(text, MACHINE_HEADING)
        assigned_values = {value for assigned_field, value in observed if assigned_field == field}
        assert assigned_values <= values
    assert "Hybrid/custom values and missing required assignments are rejected" in assignment_text or "Hybrid/custom values" in _section(text, MACHINE_HEADING)


def test_canonical_identifier_posture_is_exact() -> None:
    section = _section(_read(), "Canonical routing posture")
    assert section.count("condition_id") == 2
    assert section.count("token_id") == 2
    assert section.count("outcome") == 3
    assert "`market_id` is non-routing only" in section
    assert "`token_outcome_pair` is derived only" in section
    assert "not an input replacement" in section


def test_next_ticket_is_exact() -> None:
    text = _read()
    assert "Recommended next ticket: WEATHER-BOT-STAGE3-PROBABILITY-RECORD-CONTRACT-PLANNING-01" in text
    assert "stage3_probability_record_contract_planning" in text
    assert "must remain docs/static-test-only/planning-only" in text
