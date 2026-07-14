"""Static tests for Weather Bot Stage 3 strict OOS split contract planning."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = REPO_ROOT / "docs/prd/WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01.md"
CANONICAL_ID = "WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01"
MERGE_COMMIT = "8083a842e58da3e4b7573c2e1c7439254d275397"
NEXT_TICKET = "WEATHER-BOT-STAGE3-BASELINE-CONTRACTS-PLANNING-01"

REQUIRED_SECTIONS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Contract purpose and Stage 3 evidence gate",
    "Eligible-record preconditions",
    "Split unit and leakage-group requirements",
    "Split roles and temporal boundaries",
    "Primary rolling-origin or walk-forward contract",
    "Secondary generalization-mode matrix",
    "Training, calibration, tuning, and test isolation",
    "Overlap, gap, and embargo requirements",
    "Stratification and sample-sufficiency requirements",
    "Baseline parity requirements",
    "Split identity, provenance, and immutability",
    "Fail-closed and no-lookahead requirements",
    "Human-review and auditability requirements",
    "Explicit non-approvals",
    "Canonical routing posture",
    "Recommended next ticket",
    "Machine-checkable assignments",
    "Acceptance criteria",
]


def _read() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
    assert match, f"missing section {heading}"
    return match.group("body")


def _bullets(section: str) -> list[str]:
    return [line[2:].strip() for line in section.splitlines() if line.startswith("- ")]


def _closed_sets_and_actual_assignments(section: str) -> tuple[dict[str, list[str]], list[str]]:
    closed_part, actual_part = section.split("Actual assignments:", 1)
    sets: dict[str, list[str]] = {}
    current_key: str | None = None
    for raw_line in closed_part.splitlines():
        line = raw_line.strip()
        if line.startswith("Closed set for ") and line.endswith(":"):
            current_key = line.removeprefix("Closed set for ").removesuffix(":")
            sets[current_key] = []
        elif line.startswith("- ") and current_key is not None:
            sets[current_key].append(line[2:])
        elif line == "":
            current_key = None
    actual = []
    for line in _bullets(actual_part):
        if ": " not in line:
            continue
        actual.append(line)
    return sets, actual


def test_canonical_id_required_sections_and_scope() -> None:
    text = _read()
    assert f"Canonical ID: {CANONICAL_ID}" in text
    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text
    status = _section(text, "Status and scope")
    for phrase in [
        "docs/static-test-only/contract-planning-only",
        "defines requirements only and executes no split",
        "creates no split files, datasets, probability records, scorers, metrics",
        "weather_bot_stage3_strict_oos_split_contract_planning",
        "docs_static_test_only",
        "contract_planning_only",
    ]:
        assert phrase in status


def test_actual_pr_359_merge_commit_and_no_superseding_state() -> None:
    section = _section(_read(), "Immediate predecessor and merge verification")
    assert "PR #359" in section
    assert MERGE_COMMIT in section
    assert "not a preview merge SHA" in section
    assert "based on the local current main-equivalent history containing merge commit" in section
    assert "no newer controlling Weather Bot state superseding PR #359" in section
    assert "pr_359" in section


def test_eligible_record_requirements_and_fail_closed() -> None:
    section = _section(_read(), "Eligible-record preconditions")
    for phrase in [
        "satisfy the probability-record contract",
        "exact canonical routing fields",
        "exact venue-defined settlement rule",
        "legitimate prediction/input availability evidence",
        "compatible source, station, threshold, unit, comparator, window, and archive/finality posture",
        "non-blocked compatible label",
        "eligible as of the declared split cutoff",
        "Ineligible, conflicted, unavailable, or leakage-risk records must fail closed",
    ]:
        assert phrase in section


def test_exact_split_roles_and_secondary_generalization_matrix() -> None:
    roles = _section(_read(), "Split roles and temporal boundaries")
    rows = {}
    for line in roles.splitlines():
        if line.startswith("| ") and "---" not in line and "Split role" not in line:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            assert len(cells) == 2
            rows[cells[0]] = cells[1]
    assert rows == {
        "train": "fitting and feature-selection role using only information permitted before the applicable fold cutoff",
        "calibration": "separate calibration role when the method or diagnostic requires calibration, using only isolated permitted information",
        "test": "strict holdout role whose records are never used for fitting, feature selection, threshold selection, calibration tuning, hyperparameter tuning, bin selection, or split redesign",
    }

    modes = _section(_read(), "Secondary generalization-mode matrix")
    mode_rows = {}
    for line in modes.splitlines():
        if line.startswith("| ") and "---" not in line and "Applicability mode" not in line:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            mode_rows[cells[0]] = cells[1]
    assert mode_rows == {
        "leave_station_out": "required when claiming transfer to unseen stations or station contexts",
        "leave_year_out": "required when claiming interannual generalization and sufficient multi-year evidence exists",
        "family_stratified": "required when making market-family-specific or cross-family claims",
        "season_or_regime_stratified": "applicable only when supported by predeclared, sample-sufficient evidence",
    }
    assert "supplement rather than replace the primary temporal split" in modes


def test_rolling_origin_walk_forward_primary_and_random_shuffle_rejected() -> None:
    section = _section(_read(), "Primary rolling-origin or walk-forward contract")
    for phrase in [
        "rolling-origin or walk-forward evaluation",
        "monotonically advancing cutoffs",
        "training information available before the fold cutoff",
        "calibration information isolated where required",
        "test targets occurring strictly after permitted fitting information",
        "immutable, predeclared fold boundaries",
        "no shuffled-random primary time-series split",
        "no post-hoc boundary changes based on test outcomes",
    ]:
        assert phrase in section


def test_test_boundary_immutability_and_tuning_isolation() -> None:
    text = _read()
    section = _section(text, "Training, calibration, tuning, and test isolation")
    for phrase in [
        "Calibration is separate when the method or diagnostic requires calibration",
        "Test records must never be used for fitting",
        "feature selection",
        "threshold selection",
        "calibration tuning",
        "hyperparameter tuning",
        "bin selection",
        "split redesign",
        "train_or_calibration_only",
    ]:
        assert phrase in section
    assert "Accepted split definitions and test assignments must be immutable" in text


def test_leakage_group_conditional_gap_embargo_and_no_numeric_fabrication() -> None:
    text = _read()
    leakage = _section(text, "Split unit and leakage-group requirements")
    overlap = _section(text, "Overlap, gap, and embargo requirements")
    sufficiency = _section(text, "Stratification and sample-sufficiency requirements")
    assert "same settlement event or overlapping target episode" in leakage
    assert "Canonical route identity alone must not be assumed" in leakage
    assert "does not prescribe a database key, hash, UUID, or implementation" in leakage
    assert "predeclared gap or embargo is required" in overlap
    assert "overlapping measurement windows, forecast horizons, delayed publication, revisions, or shared target episodes" in overlap
    assert "does not fabricate a default gap duration" in overlap
    assert "No numeric window size, fold count, fixed duration, or sample minimum is prescribed" in text
    assert "Numeric minimums are not invented" in sufficiency
    assert "Insufficient or empty strata must block claims" in sufficiency
    assert not re.search(r"\b\d+\s*(day|days|week|weeks|month|months|year|years|fold|folds|record|records|sample|samples)\b", text, re.I)


def test_baseline_parity_split_identity_superseding_version_no_lookahead() -> None:
    text = _read()
    baseline = _section(text, "Baseline parity requirements")
    identity = _section(text, "Split identity, provenance, and immutability")
    fail_closed = _section(text, "Fail-closed and no-lookahead requirements")
    assert "same folds, cutoffs, availability rules, eligibility rules, and test records" in baseline
    for phrase in [
        "split identity and version",
        "fold identity",
        "split role",
        "cutoff and relevant temporal boundaries",
        "eligible-record identity",
        "leakage-group identity",
        "applicability mode",
        "exclusion/block reason",
        "provenance needed for audit",
        "superseding version, not silent mutation",
    ]:
        assert phrase in identity
    for phrase in [
        "must fail closed",
        "No-lookahead requirements prohibit use of future inputs",
        "final archives unavailable at the relevant as-of time",
        "settlement labels before legitimate resolution availability",
        "test outcomes during split design and tuning",
    ]:
        assert phrase in fail_closed


def test_explicit_non_approvals_and_canonical_routing_posture() -> None:
    text = _read()
    non_approvals = _section(text, "Explicit non-approvals")
    for phrase in [
        "Split execution is not approved",
        "Scoring execution is not approved",
        "Backtesting is not approved",
        "Probability generation is not approved",
        "Model training is not approved",
        "Dataset creation is not approved",
        "Split-file creation is not approved",
        "Corpus expansion is not approved",
        "trading, execution, autonomy",
        "production behavior are not approved",
    ]:
        assert phrase in non_approvals
    routing = _section(text, "Canonical routing posture")
    assert _bullets(routing)[:3] == ["`condition_id`", "`token_id`", "`outcome`"]
    assert "`market_id` is non-routing only" in routing
    assert "`token_outcome_pair` is derived only" in routing


def test_machine_checkable_closed_sets_and_assignments_exact() -> None:
    section = _section(_read(), "Machine-checkable assignments")
    expected_closed_sets = {
        "weather bot planning stage": ["weather_bot_stage3_strict_oos_split_contract_planning"],
        "immediate predecessor pr": ["pr_359"],
        "ticket lifecycle status": ["docs_static_test_only", "contract_planning_only"],
        "split contract status": ["requirements_defined", "split_files_not_created"],
        "primary split posture": ["rolling_origin_or_walk_forward_required"],
        "random shuffle posture": ["primary_split_rejected"],
        "split role": ["train", "calibration", "test"],
        "test boundary posture": ["immutable"],
        "tuning posture": ["train_or_calibration_only"],
        "calibration posture": ["separate_when_required"],
        "leakage group posture": ["settlement_event_or_target_episode_required"],
        "overlap control posture": ["gap_or_embargo_when_required"],
        "leave station posture": ["required_when_unseen_station_transfer_claimed"],
        "leave year posture": ["required_when_interannual_claimed"],
        "family stratification posture": ["required_for_family_claims"],
        "sample sufficiency posture": ["insufficient_samples_block_claims"],
        "baseline parity posture": ["same_folds_and_eligibility_required"],
        "split execution posture": ["not_approved"],
        "scoring execution posture": ["not_approved"],
        "backtesting posture": ["not_approved"],
        "canonical routing field": ["condition_id", "token_id", "outcome"],
        "non routing field": ["market_id"],
        "derived identifier field": ["token_outcome_pair"],
        "next ticket recommendation": ["stage3_baseline_contracts_planning"],
        "evidence status": ["strict_oos_split_contract_planning_recorded"],
        "label confidence": ["confirmed"],
    }
    expected_assignments = [
        f"{key}: {value}"
        for key, values in expected_closed_sets.items()
        for value in values
    ]
    declared_sets, actual_assignments = _closed_sets_and_actual_assignments(section)

    assert declared_sets == expected_closed_sets
    assert actual_assignments == expected_assignments
    assert set(actual_assignments) == {
        f"{key}: {value}"
        for key, values in declared_sets.items()
        for value in values
    }
    assert len(actual_assignments) == sum(len(values) for values in declared_sets.values())
    assert "Missing, hybrid, or custom values outside these closed sets are rejected." in section


def test_exact_observed_market_id_counts_for_changed_files() -> None:
    changed_counts = {
        "docs/prd/WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01.md": 3,
        "tests/core/test_weather_bot_stage3_strict_oos_split_contract_planning_01.py": 4,
    }
    for relative_path, expected_count in changed_counts.items():
        observed_count = sum(
            1
            for line in (REPO_ROOT / relative_path).read_text(encoding="utf-8").splitlines()
            if "market_id" in line
        )
        assert observed_count == expected_count


def test_exact_next_ticket_and_acceptance_criteria() -> None:
    text = _read()
    next_section = _section(text, "Recommended next ticket")
    assert f"Recommended next ticket: {NEXT_TICKET}." in next_section
    assert "docs/static-test-only/planning-only" in next_section
    assert "must not calculate baselines, create datasets, execute scoring, persist metrics" in next_section
    acceptance = _section(text, "Acceptance criteria")
    assert NEXT_TICKET in acceptance
    assert CANONICAL_ID in acceptance
    assert MERGE_COMMIT in acceptance
