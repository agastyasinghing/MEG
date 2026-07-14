"""Static tests for Weather Bot Stage 3 probability record contract planning."""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ID = "WEATHER-BOT-STAGE3-PROBABILITY-RECORD-CONTRACT-PLANNING-01"
ARTIFACT = REPO_ROOT / "docs/prd" / f"{CANONICAL_ID}.md"
TEST_PATH = REPO_ROOT / "tests/core/test_weather_bot_stage3_probability_record_contract_planning_01.py"
MACHINE_HEADING = "Machine-checkable assignments"

REQUIRED_SECTIONS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Contract purpose and target semantics",
    "Common required record fields",
    "Canonical routing and settlement-rule identity",
    "Temporal and availability fields",
    "Source, station, and target compatibility fields",
    "Prediction-representation applicability matrix",
    "Probability-value requirements",
    "Method, version, and provenance fields",
    "Record identity and immutability requirements",
    "Label-join and scoring-readiness requirements",
    "Missingness and fail-closed requirements",
    "Human-review and auditability requirements",
    "Explicit non-approvals",
    "Recommended next ticket",
    MACHINE_HEADING,
    "Acceptance criteria",
]

REQUIRED_ASSIGNMENTS = {
    ("weather bot planning stage", "weather_bot_stage3_probability_record_contract_planning"),
    ("immediate predecessor pr", "pr_358"),
    ("ticket lifecycle status", "docs_static_test_only"),
    ("ticket lifecycle status", "contract_planning_only"),
    ("record contract status", "requirements_defined"),
    ("record contract status", "runtime_schema_not_created"),
    ("scoring target posture", "venue_defined_settlement_outcome"),
    ("record immutability posture", "immutable_after_accepted_creation_required"),
    ("correction posture", "superseding_record_required"),
    ("probability domain", "closed_unit_interval"),
    ("prediction representation", "binary_outcome_probability"),
    ("prediction representation", "full_predictive_distribution"),
    ("prediction representation", "finite_ensemble"),
    ("time availability posture", "prediction_as_of_required"),
    ("time availability posture", "input_publication_availability_required"),
    ("label join posture", "canonical_route_and_target_rule_required"),
    ("mismatch posture", "fail_closed"),
    ("scoring execution posture", "not_approved"),
    ("probability generation posture", "not_approved"),
    ("persistence posture", "not_approved"),
    ("canonical routing field", "condition_id"),
    ("canonical routing field", "token_id"),
    ("canonical routing field", "outcome"),
    ("non routing field", "market_id"),
    ("derived identifier field", "token_outcome_pair"),
    ("next ticket recommendation", "stage3_strict_oos_split_contract_planning"),
    ("evidence status", "probability_record_contract_planning_recorded"),
    ("label confidence", "confirmed"),
}

CLOSED_SETS = {
    "weather bot planning stage": {"weather_bot_stage3_probability_record_contract_planning"},
    "immediate predecessor pr": {"pr_358"},
    "ticket lifecycle status": {"docs_static_test_only", "contract_planning_only"},
    "record contract status": {"requirements_defined", "runtime_schema_not_created"},
    "scoring target posture": {"venue_defined_settlement_outcome"},
    "record immutability posture": {"immutable_after_accepted_creation_required"},
    "correction posture": {"superseding_record_required"},
    "probability domain": {"closed_unit_interval"},
    "prediction representation": {"binary_outcome_probability", "full_predictive_distribution", "finite_ensemble"},
    "time availability posture": {"prediction_as_of_required", "input_publication_availability_required"},
    "label join posture": {"canonical_route_and_target_rule_required"},
    "mismatch posture": {"fail_closed"},
    "scoring execution posture": {"not_approved"},
    "probability generation posture": {"not_approved"},
    "persistence posture": {"not_approved"},
    "canonical routing field": {"condition_id", "token_id", "outcome"},
    "non routing field": {"market_id"},
    "derived identifier field": {"token_outcome_pair"},
    "next ticket recommendation": {"stage3_strict_oos_split_contract_planning"},
    "evidence status": {"probability_record_contract_planning_recorded"},
    "label confidence": {"confirmed"},
}

ASSIGNMENT_RE = re.compile(r"^- (?P<field>[a-z0-9 ][a-z0-9 -]*): (?P<value>[a-z0-9_]+)$", re.MULTILINE)
CLOSED_SET_RE = re.compile(r"^- (?P<field>[a-z0-9 ][a-z0-9 -]*): (?P<values>[a-z0-9_, ]+)$", re.MULTILINE)


def _read() -> str:
    return ARTIFACT.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(?P<body>.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, heading
    body = match.group("body").strip()
    assert body, heading
    return body


def _assignment_pairs(text: str) -> set[tuple[str, str]]:
    machine = _section(text, MACHINE_HEADING)
    actual = machine.split("Actual assignments:", 1)[1].split("Hybrid/custom values", 1)[0]
    return {(m.group("field"), m.group("value")) for m in ASSIGNMENT_RE.finditer(actual)}


def _declared_closed_sets(text: str) -> dict[str, set[str]]:
    machine = _section(text, MACHINE_HEADING)
    assert "Closed sets:" in machine
    assert machine.index("Closed sets:") < machine.index("Actual assignments:")
    closed = machine.split("Closed sets:", 1)[1].split("Actual assignments:", 1)[0]
    declared: dict[str, set[str]] = {}
    for match in CLOSED_SET_RE.finditer(closed):
        field = match.group("field")
        values = {value.strip() for value in match.group("values").split(",")}
        assert field not in declared
        assert values
        declared[field] = values
    return declared


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


def test_predecessor_merge_commit_and_superseding_state_are_recorded() -> None:
    text = _read()
    for phrase in [
        "PR #358 merged",
        "786a72353bfbdb6e27365c7f6ff6066481a440b5",
        "not a preview merge SHA",
        "no newer controlling Weather Bot state superseding PR #358",
        "immediate merged predecessor as `pr_358`",
    ]:
        assert phrase in text


def test_common_required_fields_are_requirements_only() -> None:
    section = _section(_read(), "Common required record fields")
    for phrase in [
        "prediction record identity",
        "condition_id",
        "token_id",
        "outcome",
        "venue-defined settlement-rule identity and version",
        "prediction as-of timestamp",
        "publication-availability timestamp or evidence",
        "market family",
        "threshold, unit, comparator, and measurement window",
        "source and station compatibility posture",
        "archive/finality layer expected for verification",
        "prediction representation",
        "method identity and version",
        "provenance references required for audit",
        "creation/version metadata needed to establish immutability",
        "requirements only, not a Python or storage schema",
    ]:
        assert phrase in section


def test_representation_matrix_is_exact_and_conditional() -> None:
    section = _section(_read(), "Prediction-representation applicability matrix")
    rows = {}
    for line in section.splitlines():
        if not line.startswith("| ") or "---" in line or "Prediction representation" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(cells) == 3
        rows[cells[0]] = cells[1:]
    assert rows == {
        "binary_outcome_probability": [
            "probability value in the closed interval [0, 1] and explicit identification of the canonical outcome it represents",
            "sufficient to determine binary Brier/log-score/reliability applicability for the canonical venue-defined binary settlement outcome",
        ],
        "full_predictive_distribution": [
            "explicit distribution representation, support/units, method/version identity",
            "sufficient metadata for later CRPS/PIT applicability",
        ],
        "finite_ensemble": [
            "explicit member representation, member count, units, method/version identity",
            "sufficient metadata for later rank-histogram applicability",
        ],
    }
    assert "Do not require one representation's fields for another representation" in section
    assert "does not calculate, normalize, generate, or validate an actual probability" in section


def test_temporal_availability_no_lookahead_and_probability_domain() -> None:
    text = _read()
    for phrase in [
        "closed interval [0, 1]",
        "prediction_as_of",
        "legitimate input publication availability",
        "forecast-cycle identity where applicable",
        "target measurement window",
        "No future input relative to `prediction_as_of`",
        "No final-archive information unavailable at prediction time",
        "No settlement labels may be used before legitimate resolution availability",
        "Forecast initialization time alone must not prove availability",
    ]:
        assert phrase in text


def test_immutability_corrections_label_join_and_fail_closed() -> None:
    text = _read()
    for phrase in [
        "immutable after accepted creation",
        "Corrections must create a new version or superseding record",
        "must not replace canonical routing identity",
        "exact canonical route",
        "exact settlement-rule target",
        "compatible threshold/unit/comparator/window",
        "source/station compatibility",
        "archive/finality compatibility",
        "prediction timestamp before legitimate label availability",
        "representation-specific metric applicability",
        "non-blocked prediction and label posture",
        "Any mismatch must fail closed",
        "Missing required fields",
        "must fail closed and must not be scored as ordinary usable records",
    ]:
        assert phrase in text


def test_non_approvals_canonical_routing_and_next_ticket() -> None:
    text = _read()
    for phrase in [
        "does not approve probability generation",
        "schemas, dataclasses, scoring",
        "persistence",
        "trading, execution, autonomy, production behavior",
        "Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`",
        "`market_id` is non-routing only",
        "`token_outcome_pair` is derived only",
        "WEATHER-BOT-STAGE3-STRICT-OOS-SPLIT-CONTRACT-PLANNING-01",
        "must remain docs/static-test-only/planning-only",
        "must not create split files, datasets, scoring runs, runtime code, persistence, reports, or implementation approval",
    ]:
        assert phrase in text


def test_machine_checkable_assignments_are_exact_closed_sets() -> None:
    text = _read()
    pairs = _assignment_pairs(text)
    assert pairs == REQUIRED_ASSIGNMENTS
    by_field: dict[str, set[str]] = {}
    for field, value in pairs:
        by_field.setdefault(field, set()).add(value)
    assert set(by_field) == set(CLOSED_SETS)
    for field, values in by_field.items():
        assert values == CLOSED_SETS[field]


def test_declared_closed_sets_are_complete_and_precede_actual_assignments() -> None:
    declared = _declared_closed_sets(_read())
    assert declared == CLOSED_SETS
    declared_pairs = {
        (field, value)
        for field, values in declared.items()
        for value in values
    }
    assert declared_pairs == REQUIRED_ASSIGNMENTS
    assert _assignment_pairs(_read()) == declared_pairs
