from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "docs/prd/WEATHER-BOT-STAGE3-READINESS-INVENTORY-01.md"
TEST_PATH = ROOT / "tests/core/test_weather_bot_stage3_readiness_inventory_01.py"
CANONICAL_ID = "WEATHER-BOT-STAGE3-READINESS-INVENTORY-01"
MACHINE_HEADING = "Machine-checkable Weather Bot Stage 3 readiness assignments"

REQUIRED_SECTIONS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Stage 2 completion boundary",
    "Stage 2 runtime completion versus evidence-gate passage",
    "Controlling Stage 3 evidence-ladder definition",
    "Quantitative-roadmap Stage 3 distinction",
    "Current reusable prerequisite inventory",
    "Current Stage 2 evidence sufficiency review",
    "Stage 3 required-input inventory",
    "Stage 3 probability-output contract gap",
    "Baseline and comparator requirements",
    "Strict out-of-sample split requirements",
    "Point-in-time replay and no-lookahead requirements",
    "Scoring-rule and calibration-diagnostic requirements",
    "Threshold-bucket and stratification requirements",
    "Sample-sufficiency and family-coverage risks",
    "Human-review and auditability requirements",
    "Approval and non-approval boundaries",
    "Canonical routing posture",
    "Overall readiness conclusion",
    "Recommended next ticket",
    MACHINE_HEADING,
    "Acceptance criteria",
]

REQUIRED_DOMAINS = [
    "controlling Stage 3 definition",
    "source-defined settlement target",
    "canonical routing preservation",
    "source-compatible historical-label corpus",
    "point-in-time provenance coverage",
    "publication-time availability evidence",
    "revision/finality handling",
    "family coverage",
    "station/source coverage",
    "threshold/comparator coverage",
    "probability-prediction input/record contract",
    "climatology baseline contract",
    "persistence baseline contract",
    "strict rolling-origin or walk-forward split contract",
    "leave-station-out validation where applicable",
    "leave-year-out validation where applicable",
    "no-lookahead/as-of replay contract",
    "forecast-run publication-time treatment",
    "Brier-score output contract",
    "log-score output contract",
    "CRPS applicability contract",
    "threshold-weighted CRPS applicability contract",
    "Brier-decomposition contract",
    "reliability-diagram contract",
    "PIT/rank-histogram contract",
    "threshold-bucket calibration contract",
    "sample-size histogram and uncertainty reporting",
    "family/horizon/station/source/trap/season/archive-layer stratification",
    "human-review interpretation",
    "metric persistence",
    "report/export behavior",
    "Stage 3 approval",
    "scoring execution",
    "evaluation execution",
    "backtesting execution",
]

ALLOWED_ROW_STATUSES = {
    "present_and_reusable",
    "present_but_insufficient",
    "missing",
    "not_applicable",
}

REQUIRED_ASSIGNMENTS = {
    ("weather bot planning stage", "weather_bot_stage3_readiness_inventory"),
    ("immediate predecessor pr", "pr_356"),
    ("ticket lifecycle status", "docs_static_test_only"),
    ("ticket lifecycle status", "planning_readiness_only"),
    ("stage2 runtime scope status", "fixture_only_runtime_chain_complete"),
    ("stage2 runtime scope status", "eighteen_runtime_objects_landed"),
    ("stage2 evidence sufficiency status", "not_confirmed_for_stage3_transition"),
    ("stage3 evidence ladder definition", "retrospective_probability_scoring_strict_oos"),
    ("stage3 quant roadmap definition", "ensemble_and_postprocessing_layer"),
    ("stage3 definition precedence", "evidence_ladder_controls_gate"),
    ("stage3 readiness status", "readiness_inventory_complete"),
    ("stage3 readiness status", "ready_for_requirements_planning_only"),
    ("stage3 readiness status", "not_ready_for_scoring_execution"),
    ("probability generation posture", "probability_generation_not_approved"),
    ("scoring posture", "scoring_not_approved"),
    ("evaluation execution posture", "evaluation_execution_not_approved"),
    ("backtesting posture", "backtesting_not_approved"),
    ("live source posture", "live_source_fetching_not_approved"),
    ("persistence posture", "no_metric_persistence"),
    ("persistence posture", "no_report_or_export_writing"),
    ("canonical routing field", "condition_id"),
    ("canonical routing field", "token_id"),
    ("canonical routing field", "outcome"),
    ("non routing field", "market_id"),
    ("derived identifier field", "token_outcome_pair"),
    ("next ticket recommendation", "stage3_retrospective_probability_scoring_requirements_planning"),
    ("evidence status", "stage3_readiness_inventory_recorded"),
    ("label confidence", "confirmed"),
}

CLOSED_SETS = {
    "weather bot planning stage": {"weather_bot_stage3_readiness_inventory"},
    "immediate predecessor pr": {"pr_356"},
    "ticket lifecycle status": {"docs_static_test_only", "planning_readiness_only"},
    "stage2 runtime scope status": {"fixture_only_runtime_chain_complete", "eighteen_runtime_objects_landed"},
    "stage2 evidence sufficiency status": {"not_confirmed_for_stage3_transition"},
    "stage3 evidence ladder definition": {"retrospective_probability_scoring_strict_oos"},
    "stage3 quant roadmap definition": {"ensemble_and_postprocessing_layer"},
    "stage3 definition precedence": {"evidence_ladder_controls_gate"},
    "stage3 readiness status": {"readiness_inventory_complete", "ready_for_requirements_planning_only", "not_ready_for_scoring_execution"},
    "probability generation posture": {"probability_generation_not_approved"},
    "scoring posture": {"scoring_not_approved"},
    "evaluation execution posture": {"evaluation_execution_not_approved"},
    "backtesting posture": {"backtesting_not_approved"},
    "live source posture": {"live_source_fetching_not_approved"},
    "persistence posture": {"no_metric_persistence", "no_report_or_export_writing"},
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "derived identifier field": {"token_outcome_pair"},
    "next ticket recommendation": {"stage3_retrospective_probability_scoring_requirements_planning"},
    "evidence status": {"stage3_readiness_inventory_recorded"},
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
    return machine.split(marker, 1)[1].split("Readiness matrix:", 1)[0]


def _assignment_pairs(text: str) -> set[tuple[str, str]]:
    return {(m.group("field"), m.group("value")) for m in ASSIGNMENT_RE.finditer(_actual_assignment_text(text))}


def test_document_exists_canonical_id_and_required_sections() -> None:
    assert ARTIFACT.exists()
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


def test_predecessor_merge_and_stage2_boundary_are_recorded() -> None:
    text = _read()
    for phrase in [
        "PR #356 as the immediate merged predecessor",
        "ad985300cd1ad5dfd887114c4f3dd26ab152a941",
        "not a preview merge SHA",
        "fixture-only/local-static/caller-supplied Stage 2 runtime chain is complete and closed",
        "All 18 approved Stage 2 runtime-chain objects are landed",
        "Positive full-chain representation and expected-negative fail-closed representation are landed",
        "exactly 5 Stage 2 JSON fixture files",
        "3 synthetic historical-label JSON files",
        "2 real source-backed JSON files",
        "pass candidate and a blocked conflict candidate",
    ]:
        assert phrase in text


def test_runtime_completion_is_not_evidence_gate_passage() -> None:
    text = _read()
    for phrase in [
        "runtime completion is not evidence-ladder passage",
        "does not by itself prove evidence-ladder Stage 2 sufficiency for transition into Stage 3",
        "not established merely by the runtime closeout",
        "tiny fixture corpus is useful for static validation but insufficient by itself for strict OOS retrospective scoring",
        "Stage 3 readiness must not be inferred from Stage 2 runtime object count",
    ]:
        assert phrase in text


def test_stage3_definitions_are_distinguished_and_evidence_ladder_controls() -> None:
    text = _read()
    for phrase in [
        "retrospective probability scoring on strict out-of-sample splits",
        "ensemble and postprocessing method-maturity layer",
        "EMOS/NGR/MOS",
        "BMA",
        "analog ensembles",
        "selected distributional methods",
        "distinct from evidence-ladder Stage 3",
        "Gate sequencing is controlled by this evidence-ladder definition",
        "does not grant evidence-gate passage",
    ]:
        assert phrase in text


def test_readiness_matrix_domains_and_closed_statuses() -> None:
    matrix = _section(_read(), MACHINE_HEADING).split("Readiness matrix:", 1)[1]
    rows = re.findall(r"^\| (?P<domain>[^|]+) \| (?P<status>[^|]+) \| (?P<rationale>[^|]+) \|$", matrix, re.MULTILINE)
    observed = {domain.strip(): status.strip() for domain, status, _ in rows if domain.strip() not in {"---", "Domain"}}
    for domain in REQUIRED_DOMAINS:
        assert domain in observed
    assert set(observed.values()) <= ALLOWED_ROW_STATUSES
    assert "optional_missing" not in matrix
    assert not any("/" in status or " " in status for status in observed.values())


def test_requirements_are_present_without_calculation_or_execution_approval() -> None:
    text = _read()
    required = [
        "Brier score", "log score", "CRPS", "threshold-weighted CRPS", "Brier decomposition",
        "reliability diagrams with reproducible bins, sample counts, and uncertainty",
        "PIT or rank histograms", "calibration and ranking comparisons",
        "climatology and persistence baselines", "rolling-origin or walk-forward evaluation",
        "leave-station-out and leave-year-out evaluation", "threshold-bucket calibration",
        "market family, threshold distance, horizon, station/source compatibility, trap category, season/regime when supported, and archive layer",
        "These are requirements or future evidence categories only; this artifact calculates none of them",
        "No calculation, calibration output, reliability output, PIT/rank output, persisted metric, or Stage 3 report is created",
    ]
    for phrase in required:
        assert phrase in text
    forbidden_approvals = [
        "probability generation is approved", "scoring execution is approved", "evaluation execution is approved",
        "backtesting is approved", "source fetching is approved", "paper simulation is approved",
        "trading is approved", "autonomy is approved", "persistence is approved", "export writing is approved",
    ]
    lowered = text.lower()
    for phrase in forbidden_approvals:
        assert phrase not in lowered


def test_non_approval_boundaries_and_canonical_routing_are_explicit() -> None:
    text = _read()
    for phrase in [
        "Stage 3 implementation is not approved",
        "Probability generation is not approved",
        "Scoring execution is not approved",
        "Evaluation execution is not approved",
        "Backtesting is not approved",
        "Data acquisition or corpus expansion is not approved",
        "Metric persistence and export are not approved",
        "Weather Bot models the market settlement rule, not generic weather",
        "Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`",
        "`market_id` remains non-routing only",
        "`token_outcome_pair` remains derived only",
        "does not introduce the legacy `market_id` as a routing or bridge input",
        "does not introduce `token_outcome_pair` as an input",
    ]:
        assert phrase in text


def test_assignments_are_section_scoped_complete_and_closed_set() -> None:
    text = _read()
    pairs = _assignment_pairs(text)
    assert REQUIRED_ASSIGNMENTS <= pairs
    fields = {field for field, _ in pairs}
    assert fields == set(CLOSED_SETS)
    for field, value in pairs:
        assert value in CLOSED_SETS[field]
        assert "/" not in value and " " not in value and "optional" not in value
    for field, values in CLOSED_SETS.items():
        closed_heading = f"Closed set for {field}:"
        assert closed_heading in _section(text, MACHINE_HEADING)
        for value in values:
            assert f"- {value}" in _section(text, MACHINE_HEADING)


def test_exact_next_ticket_and_no_forbidden_lane_created() -> None:
    text = _read()
    assert "WEATHER-BOT-STAGE3-RETROSPECTIVE-PROBABILITY-SCORING-REQUIREMENTS-PLANNING-01" in text
    assert "docs/static-test-only/requirements-planning-only" in text
    forbidden = [
        "Recommended next ticket: standalone self-review",
        "Recommended next ticket: closeout",
        "Recommended next ticket: owner-decision",
        "Recommended next ticket: approval-decision",
        "Recommended next ticket: implementation",
        "owner-decision capture lane",
        "source-fetching approval is introduced",
        "scoring approval is introduced",
        "backtesting approval is introduced",
        "paper-simulation approval is introduced",
        "trading approval is introduced",
        "persistence approval is introduced",
        "export approval is introduced",
        "autonomy approval is introduced",
    ]
    for phrase in forbidden:
        assert phrase not in text
