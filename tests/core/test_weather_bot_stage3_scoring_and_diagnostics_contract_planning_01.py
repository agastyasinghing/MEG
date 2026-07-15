"""Static tests for Weather Bot Stage 3 scoring diagnostics planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = REPO_ROOT / "docs/prd/WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01.md"
ALLOWLIST_PATH = REPO_ROOT / "tests/core/canonical_id_allowlist.py"
TEST_PATH = Path(__file__).resolve()

TITLE = "WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01"
CANONICAL_ID = "WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01"
MERGE_COMMIT = "9b0457495db3274ef957ab4c08e0e3cb6fb02fe3"
SUCCESSOR = "WEATHER-BOT-STAGE3-EVALUATION-RESULT-RECORD-CONTRACT-PLANNING-01"

HEADINGS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Contract purpose and controlling target",
    "Input eligibility and representation gates",
    "Exact scoring and diagnostic applicability matrix",
    "Proper scoring-rule requirements",
    "Calibration diagnostic requirements",
    "Distribution and ensemble diagnostic requirements",
    "Aggregation and weighting requirements",
    "Paired baseline comparison requirements",
    "Binning sparse-bucket and sample-sufficiency requirements",
    "Stratification requirements",
    "Uncertainty requirements",
    "Metric identity provenance and immutability",
    "Fail-closed and no-lookahead requirements",
    "Human-review and claim boundaries",
    "Explicit non-approvals",
    "Canonical routing posture",
    "Recommended next ticket",
    "Machine-checkable assignments",
    "Acceptance criteria",
]

EXPECTED_MATRIX = [
    ["Artifact", "Required representation", "Required meaning", "Direction or use", "Fail-closed boundary"],
    ["---", "---", "---", "---", "---"],
    ["brier_score", "binary outcome probability", "mean squared error between the probability assigned to the canonical binary settlement outcome and its compatible binary label", "proper score; lower is better; aggregate only under one predeclared weighting rule", "block when probability, label, canonical target, pairing, or aggregation compatibility is invalid"],
    ["log_score", "binary outcome probability", "negative logarithmic score for the canonical binary settlement outcome and its compatible binary label", "proper score; lower is better; probability-boundary handling must be predeclared without test-informed changes", "block when the boundary policy is absent or probability, label, canonical target, or pairing compatibility is invalid"],
    ["reliability_diagram", "binary outcome probability", "predeclared probability bins containing sample count, mean predicted probability, observed outcome frequency, and uncertainty", "calibration diagnostic only; not a scalar ranking substitute", "block unsupported claims for empty or insufficient bins and never silently merge bins after test inspection"],
    ["brier_decomposition", "binary outcome probability", "reliability, resolution, and uncertainty components under one predeclared decomposition method", "diagnostic decomposition only; not a replacement for the proper score and sample-sufficiency gated", "block when the method, grouping, or sufficient compatible samples were not predeclared"],
    ["crps", "full predictive distribution", "proper score comparing an explicitly represented predictive distribution with a compatible verifying observation", "proper score; lower is better; applicable only to explicit full distributions", "block when only a binary event probability or incomplete distribution is available"],
    ["pit_histogram", "continuous, discrete, or mixed full predictive distribution", "probability-integral-transform diagnostic under one predeclared representation-compatible treatment", "distributional calibration diagnostic only; not a scalar ranking substitute", "block when the predictive representation or PIT treatment is incompatible or undeclared"],
    ["rank_histogram", "finite comparable ensemble", "rank of the compatible verifying observation among explicit ensemble members under one predeclared tie treatment", "ensemble calibration diagnostic only; not a scalar ranking substitute", "block when members are not explicit and comparable or tie treatment is undeclared"],
    ["threshold_weighted_crps", "full predictive distribution with justified threshold weighting", "proper distribution score using one predeclared threshold-weight function for a justified rare-event or near-threshold claim", "proper score; lower is better; weighting must be fixed before test inspection", "block when weighting, full-distribution representation, or claim justification is absent or post-hoc"],
]

EXPECTED_CLOSED_SETS = {
    "weather bot planning stage": ["weather_bot_stage3_scoring_and_diagnostics_contract_planning"],
    "immediate predecessor pr": ["pr_361"],
    "ticket lifecycle status": ["docs_static_test_only", "contract_planning_only"],
    "scoring contract status": ["requirements_defined", "calculations_not_created"],
    "scoring target posture": ["venue_defined_settlement_outcome"],
    "binary proper score": ["brier_score", "log_score"],
    "full distribution proper score": ["crps"],
    "conditional weighted score": ["threshold_weighted_crps"],
    "calibration diagnostic": ["reliability_diagram", "brier_decomposition"],
    "distribution diagnostic": ["pit_histogram"],
    "ensemble diagnostic": ["rank_histogram"],
    "proper score direction posture": ["lower_is_better"],
    "metric applicability posture": ["representation_gated"],
    "binning posture": ["predeclared_reproducible_bins_required"],
    "sparse bucket posture": ["blocked_or_insufficient_not_silently_pooled"],
    "uncertainty posture": ["predeclared_method_required"],
    "comparison posture": ["paired_common_test_record_set_required"],
    "baseline comparison posture": ["climatology_and_persistence_required"],
    "stratification posture": ["predeclared_supported_axes_only"],
    "tuning posture": ["train_or_calibration_only"],
    "market price posture": ["not_approved_as_baseline_or_truth"],
    "scoring execution posture": ["not_approved"],
    "diagnostic execution posture": ["not_approved"],
    "metric persistence posture": ["not_approved"],
    "report export posture": ["not_approved"],
    "canonical routing field": ["condition_id", "token_id", "outcome"],
    "non routing field": ["market_id"],
    "derived identifier field": ["token_outcome_pair"],
    "next ticket recommendation": ["stage3_evaluation_result_record_contract_planning"],
    "evidence status": ["scoring_and_diagnostics_contract_planning_recorded"],
    "label confidence": ["confirmed"],
}

EXPECTED_CLOSED_SET_ITEMS = list(EXPECTED_CLOSED_SETS.items())
EXPECTED_ASSIGNMENTS = [
    f"{field}: {value}"
    for field, values in EXPECTED_CLOSED_SETS.items()
    for value in values
]

EXPECTED_STRATA = [
    "market_family",
    "threshold_distance",
    "forecast_horizon",
    "station_source_compatibility",
    "trap_category",
    "season_or_regime_when_supported",
    "archive_layer",
]


def _doc() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    marker = f"## {heading}\n"
    start = text.index(marker) + len(marker)
    rest = text[start:]
    end = rest.find("\n## ")
    return rest if end == -1 else rest[:end]


def _parse_table(section: str) -> list[list[str]]:
    rows = [line for line in section.splitlines() if line.startswith("| ")]
    assert len(rows) == 10
    parsed = [[cell.strip() for cell in row.strip("|").split("|")] for row in rows]
    assert parsed[0] == EXPECTED_MATRIX[0]
    assert parsed[1] == EXPECTED_MATRIX[1]
    assert len(parsed[2:]) == 8
    assert all(len(row) == 5 for row in parsed)
    assert len({tuple(row) for row in parsed[2:]}) == 8
    return parsed


def _parse_closed_set_items(section: str) -> list[tuple[str, list[str]]]:
    before_actual = section.split("\nActual assignments:\n", 1)[0]
    result: list[tuple[str, list[str]]] = []
    seen_fields: set[str] = set()
    current_field: str | None = None
    current_values: list[str] | None = None
    for line in before_actual.splitlines():
        if line in {"", "Closed sets:"}:
            continue
        if line.startswith("Closed set for ") and line.endswith(":"):
            current_field = line.removeprefix("Closed set for ").removesuffix(":")
            assert current_field not in seen_fields
            seen_fields.add(current_field)
            current_values = []
            result.append((current_field, current_values))
        elif line.startswith("- "):
            assert current_field is not None
            assert current_values is not None
            value = line[2:]
            assert value not in current_values
            current_values.append(value)
        else:
            raise AssertionError(f"Malformed closed-set line: {line}")
    return result


def _flatten_closed_set_items(items: list[tuple[str, list[str]]]) -> list[str]:
    return [f"{field}: {value}" for field, values in items for value in values]


def _parse_assignments(section: str) -> list[str]:
    after_actual = section.split("\nActual assignments:\n", 1)[1]
    assignments_text = after_actual.split("\nMissing, duplicate", 1)[0]
    result: list[str] = []
    seen: set[str] = set()
    for line in assignments_text.splitlines():
        if line == "":
            continue
        assert line.startswith("- "), f"Malformed assignment line: {line}"
        assignment = line[2:]
        assert ": " in assignment, f"Malformed assignment line: {line}"
        field, value = assignment.split(": ", 1)
        assert field
        assert value
        assert assignment not in seen
        seen.add(assignment)
        result.append(assignment)
    return result


def _allowlist_counts() -> dict[str, int]:
    module = ast.parse(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "ALLOWED_MARKET_ID_OCCURRENCE_LINES":
                call = node.value
                assert isinstance(call, ast.Call)
                dict_node = call.args[0]
                assert isinstance(dict_node, ast.Dict)
                return {ast.literal_eval(k): ast.literal_eval(v) for k, v in zip(dict_node.keys, dict_node.values) if k is not None}
    raise AssertionError("allowlist assignment not found")


def _observed_market_id_count(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if "market_id" in line)


def test_title_canonical_id_headings_and_predecessor() -> None:
    text = _doc()
    assert text.startswith(f"# {TITLE}\n")
    assert f"Canonical ID: {CANONICAL_ID}\n" in text
    headings = [line[3:] for line in text.splitlines() if line.startswith("## ")]
    assert headings == HEADINGS
    for heading in HEADINGS:
        assert text.count(f"## {heading}\n") == 1
        assert _section(text, heading).strip()
    assert "Immediate predecessor: pr_361." in text
    assert text.count(MERGE_COMMIT) >= 3
    assert "actual merge commit" in text
    assert "not a preview merge SHA" in text


def test_applicability_matrix_is_exact_structural_contract() -> None:
    matrix = _parse_table(_section(_doc(), "Exact scoring and diagnostic applicability matrix"))
    assert matrix == EXPECTED_MATRIX


def test_closed_sets_equal_actual_assignments_and_expected_constants() -> None:
    section = _section(_doc(), "Machine-checkable assignments")
    closed_set_items = _parse_closed_set_items(section)
    assignments = _parse_assignments(section)
    assert closed_set_items == EXPECTED_CLOSED_SET_ITEMS
    assert _flatten_closed_set_items(closed_set_items) == EXPECTED_ASSIGNMENTS
    assert assignments == EXPECTED_ASSIGNMENTS
    assert "Missing, duplicate, hybrid, extra, or custom fields and values are rejected." in section


def test_stratification_axes_are_exact_ordered_closed_list() -> None:
    section = _section(_doc(), "Stratification requirements")
    bullets = [line[2:] for line in section.splitlines() if line.startswith("- ")]
    assert bullets == EXPECTED_STRATA
    assert "An axis may be used only when predeclared, compatible, and sample-sufficient." in section
    assert "No post-hoc stratum selection is permitted." in section


def test_successor_and_non_approval_boundaries_are_exact() -> None:
    text = _doc()
    successor_section = _section(text, "Recommended next ticket")
    assert f"Recommended next ticket: {SUCCESSOR}." in successor_section
    assert "must remain docs/static-test-only/contract-planning-only" in successor_section
    assert "must not calculate, persist, report, or execute evaluation results" in successor_section
    non_approval = _section(text, "Explicit non-approvals")
    for phrase in [
        "scoring execution",
        "diagnostic execution",
        "probability generation",
        "split execution",
        "baseline execution",
        "model training or calibration",
        "metric persistence",
        "storage persistence",
        "reports or exports",
        "backtesting",
        "simulation",
        "paper trading",
        "trading",
        "order placement",
        "autonomy",
        "runtime behavior",
        "production behavior",
    ]:
        assert f"- {phrase};" in non_approval or f"- {phrase}." in non_approval


def test_section_specific_prohibited_fabricated_numbers_are_absent() -> None:
    text = _doc()
    sections = [
        "Proper scoring-rule requirements",
        "Calibration diagnostic requirements",
        "Distribution and ensemble diagnostic requirements",
        "Aggregation and weighting requirements",
        "Binning sparse-bucket and sample-sufficiency requirements",
        "Uncertainty requirements",
    ]
    numeric_token = re.compile(
        r"(?<![A-Za-z0-9_])(?:\d+(?:\.\d+)?|\.\d+)(?:e[+-]?\d+)?%?(?![A-Za-z0-9_])",
        re.IGNORECASE,
    )
    prohibited_concepts = [
        "epsilon =",
        "epsilon:",
        "tolerance =",
        "tolerance:",
        "confidence level of",
        "fixed bin count of",
        "minimum of ",
        "minimum sample size:",
        "numeric sample minimum of",
        "bootstrap block length of",
        "resampling block length of",
        "tie constant of",
        "weighting constant of",
        "pooling threshold of",
        "numeric pooling threshold of",
    ]
    for section_name in sections:
        section = _section(text, section_name)
        assert not numeric_token.search(section), section_name
        lower_section = section.lower()
        for phrase in prohibited_concepts:
            assert phrase not in lower_section
    assert "does not choose a clipping epsilon" in _section(text, "Proper scoring-rule requirements")
    assert "numeric probability tolerance" in _section(text, "Proper scoring-rule requirements")
    assert "Do not invent a numeric minimum" in _section(text, "Binning sparse-bucket and sample-sufficiency requirements")


def test_no_runtime_or_production_behavior_is_added_by_contract() -> None:
    text = _doc()
    status = _section(text, "Status and scope")
    acceptance = _section(text, "Acceptance criteria")
    assert "This ticket defines requirements only." in status
    assert "does not calculate scores" in status
    assert "add production behavior" in status
    assert "No runtime implementation, scorer, metric calculation, diagram generation, persistence, report, export, or production behavior is added." in acceptance


def test_allowlist_counts_match_observed_market_id_lines_for_new_files() -> None:
    counts = _allowlist_counts()
    expected_paths = {
        "docs/prd/WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01.md": DOC_PATH,
        "tests/core/test_weather_bot_stage3_scoring_and_diagnostics_contract_planning_01.py": TEST_PATH,
    }
    for rel_path, path in expected_paths.items():
        assert counts[rel_path] == _observed_market_id_count(path)
