"""Static tests for Weather Bot Stage 3 baseline contracts planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = REPO_ROOT / "docs/prd/WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_stage3_baseline_contracts_planning_01.py"
CANONICAL_ID = "WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01"
MERGE_COMMIT = "c0b892c7be00442cf167b09c4cd853605e7bd8a8"
NEXT_TICKET = "WEATHER-BOT-STAGE3-SCORING-AND-DIAGNOSTICS-CONTRACT-PLANNING-01"
MACHINE_HEADING = "Machine-checkable assignments"

REQUIRED_SECTIONS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Contract purpose and baseline role",
    "Common baseline requirements",
    "Exact baseline applicability matrix",
    "Climatology baseline contract",
    "Persistence baseline contract",
    "Point-in-time availability and no-lookahead",
    "Split, eligibility, and test-record parity",
    "Fitting, tuning, and calibration isolation",
    "Conditioning, fallback, and missingness",
    "Probability-record output requirements",
    "Baseline identity, provenance, and immutability",
    "Paired comparison and claim requirements",
    "Fail-closed requirements",
    "Human-review and auditability",
    "Explicit non-approvals",
    "Canonical routing posture",
    "Recommended next ticket",
    MACHINE_HEADING,
    "Acceptance criteria",
]

EXPECTED_BASELINE_MATRIX = [
    ["Baseline type", "Required meaning", "Fail-closed boundary"],
    [
        "climatology",
        "as-of empirical reference for the canonical settlement outcome estimated only from permitted historical train records",
        "block when compatible point-in-time history or a predeclared sufficient fallback is unavailable",
    ],
    [
        "persistence",
        "latest legitimately available compatible prior state under one predeclared persisted quantity and conversion rule",
        "block when no compatible prior state exists or the persisted quantity or conversion rule would change after test inspection",
    ],
]

EXPECTED_CLOSED_SETS = {
    "weather bot planning stage": ["weather_bot_stage3_baseline_contracts_planning"],
    "immediate predecessor pr": ["pr_360"],
    "ticket lifecycle status": ["docs_static_test_only", "contract_planning_only"],
    "baseline contract status": ["requirements_defined", "calculations_not_created"],
    "baseline type": ["climatology", "persistence"],
    "scoring target posture": ["venue_defined_settlement_outcome"],
    "climatology history posture": ["train_only_as_of_history"],
    "persistence input posture": ["latest_legitimately_available_compatible_prior_state"],
    "persistence definition posture": ["predeclared_quantity_and_conversion_required"],
    "split parity posture": ["same_folds_cutoffs_eligibility_and_test_records_required"],
    "paired comparison posture": ["common_test_record_set_required"],
    "availability posture": ["point_in_time_required"],
    "fallback posture": ["predeclared_compatible_or_fail_closed"],
    "tuning posture": ["train_or_calibration_only"],
    "output contract posture": ["probability_record_contract_required"],
    "market price posture": ["not_approved_as_baseline"],
    "baseline execution posture": ["not_approved"],
    "scoring execution posture": ["not_approved"],
    "storage persistence posture": ["not_approved"],
    "canonical routing field": ["condition_id", "token_id", "outcome"],
    "non routing field": ["market_id"],
    "derived identifier field": ["token_outcome_pair"],
    "next ticket recommendation": ["stage3_scoring_and_diagnostics_contract_planning"],
    "evidence status": ["baseline_contracts_planning_recorded"],
    "label confidence": ["confirmed"],
}
EXPECTED_ASSIGNMENTS = [
    f"{field}: {value}"
    for field, values in EXPECTED_CLOSED_SETS.items()
    for value in values
]
def _read() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
    assert match, f"missing section {heading}"
    body = match.group("body")
    assert body.strip(), f"empty section {heading}"
    return body


def _bullets(section: str) -> list[str]:
    return [line[2:].strip() for line in section.splitlines() if line.startswith("- ")]


def _markdown_table(section: str) -> list[list[str]]:
    table_lines = [line for line in section.splitlines() if line.startswith("| ")]
    assert len(table_lines) == 4
    assert table_lines[1] == "| --- | --- | --- |"
    parsed = []
    for line in [table_lines[0], *table_lines[2:]]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(cells) == 3
        parsed.append(cells)
    assert len({tuple(row) for row in parsed[1:]}) == len(parsed[1:])
    return parsed


def _closed_sets_and_actual_assignments(section: str) -> tuple[dict[str, list[str]], list[str]]:
    assert section.index("Closed sets:") < section.index("Actual assignments:")
    closed_part, actual_part = section.split("Actual assignments:", 1)
    sets: dict[str, list[str]] = {}
    current_key: str | None = None
    for raw_line in closed_part.splitlines():
        line = raw_line.strip()
        if line.startswith("Closed set for ") and line.endswith(":"):
            current_key = line.removeprefix("Closed set for ").removesuffix(":")
            assert current_key not in sets
            sets[current_key] = []
        elif line.startswith("- ") and current_key is not None:
            value = line[2:]
            assert value not in sets[current_key]
            sets[current_key].append(value)
        elif line == "":
            current_key = None
    actual = []
    for line in _bullets(actual_part):
        if ": " in line:
            assert line not in actual
            actual.append(line)
    return sets, actual


def test_canonical_id_required_sections_exactly_once_and_scope() -> None:
    text = _read()
    assert text.startswith(f"# {CANONICAL_ID}")
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for heading in REQUIRED_SECTIONS:
        assert len(re.findall(rf"^## {re.escape(heading)}$", text, re.M)) == 1
    all_required = set(REQUIRED_SECTIONS)
    observed = [line.removeprefix("## ") for line in text.splitlines() if line.startswith("## ")]
    assert observed == REQUIRED_SECTIONS
    assert set(observed) == all_required
    status = _section(text, "Status and scope")
    for phrase in [
        "docs/static-test-only/contract-planning-only",
        "calculates no baseline",
        "creates no probability records",
        "executes no splits or scoring",
        "adds no production behavior",
        "weather_bot_stage3_baseline_contracts_planning",
        "docs_static_test_only",
        "contract_planning_only",
    ]:
        assert phrase in status


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


def test_actual_pr_360_merge_commit_and_no_superseding_state() -> None:
    section = _section(_read(), "Immediate predecessor and merge verification")
    assert "PR #360" in section
    assert MERGE_COMMIT in section
    assert "not a preview merge SHA" in section
    assert "based on the local current main-equivalent history containing merge commit" in section
    assert "no newer controlling Weather Bot state superseding PR #360" in section
    assert "pr_360" in section


def test_exact_baseline_applicability_matrix() -> None:
    section = _section(_read(), "Exact baseline applicability matrix")
    assert _markdown_table(section) == EXPECTED_BASELINE_MATRIX


def test_machine_checkable_closed_sets_and_assignments_exact() -> None:
    section = _section(_read(), MACHINE_HEADING)
    declared_sets, actual_assignments = _closed_sets_and_actual_assignments(section)
    assert declared_sets == EXPECTED_CLOSED_SETS
    assert actual_assignments == EXPECTED_ASSIGNMENTS
    assert set(actual_assignments) == {
        f"{field}: {value}"
        for field, values in declared_sets.items()
        for value in values
    }
    assert len(actual_assignments) == sum(len(values) for values in declared_sets.values())
    assert "Missing, duplicate, hybrid, extra, or custom fields and values are rejected." in section


def test_common_baseline_requirements_and_probability_domain() -> None:
    section = _section(_read(), "Common baseline requirements")
    expected_bullets = [
        "target the canonical venue-defined settlement outcome;",
        "preserve `condition_id`, `token_id`, and `outcome`;",
        "satisfy the probability-record contract;",
        "preserve `prediction_as_of` and legitimate input publication availability;",
        "preserve settlement-rule, source, station, threshold, unit, comparator, measurement-window, and archive/finality compatibility;",
        "preserve method identity, version, and provenance;",
        "use only information permitted by the applicable OOS fold;",
        "produce a representation compatible with the metric and candidate comparison;",
        "use the same fold, cutoff, eligibility rules, and test records as the candidate;",
        "fail closed when required compatible information is unavailable.",
    ]
    assert _bullets(section) == expected_bullets
    assert "future baseline probability must be in [0, 1]" in section
    assert "This ticket calculates no value" in section


def test_climatology_and_persistence_contract_requirements() -> None:
    climatology = _section(_read(), "Climatology baseline contract")
    persistence = _section(_read(), "Persistence baseline contract")
    assert _bullets(climatology) == [
        "only labels legitimately available before the applicable fold cutoff;",
        "train history only for estimation;",
        "exact canonical settlement target;",
        "source/station/threshold/unit/comparator/window/finality compatibility;",
        "any conditioning dimensions, smoothing, history window, hierarchy, or fallback declared before test evaluation;",
        "no test record, future label, unavailable revision, or final archive leakage;",
        "no numeric history window, smoothing constant, or sample minimum invented here.",
    ]
    assert "If conditioned climatology is unavailable, use only a predeclared compatible fallback. Otherwise fail closed." in climatology
    assert _bullets(persistence) == [
        "one exact persisted quantity and one conversion rule declared before evaluation;",
        "the latest legitimately available compatible prior state before `prediction_as_of`;",
        "exact target, source, station, unit, threshold, comparator, window, and finality compatibility;",
        "no hindsight switching among providers, stations, quantities, forecasts, observations, or conversion rules;",
        "no future state, unavailable revision, final archive, or test-label knowledge;",
        "fail closed when no compatible prior state exists.",
    ]
    assert "does not decide the persisted quantity or conversion formula" in persistence


def test_point_in_time_split_parity_tuning_and_paired_comparison() -> None:
    text = _read()
    point = _section(text, "Point-in-time availability and no-lookahead")
    split = _section(text, "Split, eligibility, and test-record parity")
    tuning = _section(text, "Fitting, tuning, and calibration isolation")
    paired = _section(text, "Paired comparison and claim requirements")
    for phrase in [
        "prediction_as_of",
        "legitimate input publication availability",
        "fold cutoff availability",
        "availability evidence",
        "future inputs",
        "future labels",
        "unavailable revisions",
        "final archives unavailable at prediction time",
        "settlement outcomes before legitimate resolution availability",
    ]:
        assert phrase in point
    assert _bullets(split) == [
        "the same split identity and version;",
        "the same fold and cutoff;",
        "the same eligibility and no-lookahead rules;",
        "the same compatible labels;",
        "the same test records for comparative claims.",
    ]
    assert "common paired test-record set" in split
    assert "Missing baseline records must not be silently dropped or replaced after test inspection" in split
    assert "Baseline estimation uses train data only" in tuning
    assert "train or isolated calibration information only" in tuning
    assert "Test records and test outcomes must never influence those choices" in tuning
    assert "common paired test-record set" in paired
    assert "blocked or explicitly reported as unavailable" in paired


def test_identity_immutability_fail_closed_market_price_non_approvals_and_no_numeric_fabrication() -> None:
    text = _read()
    identity = _section(text, "Baseline identity, provenance, and immutability")
    fail_closed = _section(text, "Fail-closed requirements")
    non_approvals = _section(text, "Explicit non-approvals")
    for phrase in [
        "baseline type",
        "baseline identity and version",
        "method identity and version",
        "split and fold identity",
        "prediction_as_of",
        "availability evidence",
        "conditioning or persisted-quantity definition",
        "fallback or conversion-rule identity",
        "canonical target and compatibility posture",
        "provenance and exclusion/block reason",
        "immutable",
        "superseding version",
    ]:
        assert phrase in identity
    for phrase in [
        "compatible point-in-time history is unavailable",
        "no predeclared compatible fallback exists",
        "no compatible prior state exists",
        "persisted quantity or conversion rule would change after test inspection",
        "source/station/threshold/unit/comparator/window/finality compatibility cannot be proven",
        "availability evidence is missing",
        "canonical target compatibility fails",
        "probability-record requirements are unmet",
        "paired comparison requirements cannot be satisfied",
    ]:
        assert phrase in fail_closed
    for phrase in [
        "does not approve baseline execution",
        "scoring execution",
        "probability generation",
        "split execution",
        "dataset generation",
        "model training",
        "source fetching",
        "corpus expansion",
        "metric persistence",
        "storage persistence",
        "report creation",
        "market simulation",
        "paper trading",
        "trading, order placement, autonomy, production behavior",
        "Market prices are not approved as climatology, persistence, or frictionless truth",
        "Stage 4 market-price and executable-cost analysis remains outside scope",
    ]:
        assert phrase in non_approvals
    assert not re.search(r"\b\d+\s*(day|days|week|weeks|month|months|year|years|record|records|sample|samples)\b", text, re.I)
    assert not re.search(r"smoothing (constant|value) (of|=) \d", text, re.I)


def test_probability_record_output_human_review_canonical_routing_and_next_ticket() -> None:
    text = _read()
    output = _section(text, "Probability-record output requirements")
    review = _section(text, "Human-review and auditability")
    routing = _section(text, "Canonical routing posture")
    next_section = _section(text, "Recommended next ticket")
    for phrase in [
        "satisfy the probability-record contract",
        "canonical target",
        "prediction_as_of",
        "availability evidence",
        "method identity and version",
        "provenance",
        "source/station/threshold/unit/comparator/window/finality compatibility",
        "fail-closed mismatch posture",
        "Binary-outcome probabilities must be in [0, 1]",
    ]:
        assert phrase in output
    assert "Human review is advisory" in review
    assert "does not approve execution, scoring, storage persistence, trading, autonomy, or production behavior" in review
    assert _bullets(routing)[:3] == ["`condition_id`", "`token_id`", "`outcome`"]
    assert "`market_id` is non-routing only" in routing
    assert "`token_outcome_pair` is derived only" in routing
    assert f"Recommended next ticket: {NEXT_TICKET}." in next_section
    assert "docs/static-test-only/planning-only" in next_section
    assert "must not calculate metrics, execute scoring, persist outputs, create reports, or approve implementation" in next_section


def _allowlist_counts() -> dict[str, int]:
    allowlist_path = REPO_ROOT / "tests/core/canonical_id_allowlist.py"
    module = ast.parse(allowlist_path.read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", None) == "ALLOWED_MARKET_ID_OCCURRENCE_LINES":
            assert isinstance(node.value, ast.Call)
            assert node.value.args
            raw = ast.literal_eval(node.value.args[0])
            assert isinstance(raw, dict)
            return raw
    raise AssertionError("ALLOWED_MARKET_ID_OCCURRENCE_LINES not found")


def test_exact_observed_market_id_counts_match_allowlist_for_new_files() -> None:
    changed_paths = [
        "docs/prd/WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01.md",
        "tests/core/test_weather_bot_stage3_baseline_contracts_planning_01.py",
    ]
    allowlist_counts = _allowlist_counts()
    for relative_path in changed_paths:
        observed_count = sum(
            1
            for line in (REPO_ROOT / relative_path).read_text(encoding="utf-8").splitlines()
            if "market_id" in line
        )
        assert allowlist_counts[relative_path] == observed_count

