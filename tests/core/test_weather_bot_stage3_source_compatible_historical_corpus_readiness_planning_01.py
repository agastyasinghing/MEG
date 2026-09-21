"""Static oracle for the Stage 3 historical-corpus readiness plan."""
from __future__ import annotations

from pathlib import Path


DOC = Path("docs/prd/WEATHER-BOT-STAGE3-SOURCE-COMPATIBLE-HISTORICAL-CORPUS-READINESS-PLANNING-01.md")
SUCCESSOR = "WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-REQUEST-01"
HEADINGS = [
    "Status and scope", "Immediate predecessor and merge verification",
    "Current five-example corpus baseline", "Per-record usability requirements",
    "Corpus-readiness dimensions", "Point-in-time and no-lookahead requirements",
    "Coverage and stratification plan", "Sample-sufficiency assessment method",
    "Strict-OOS feasibility requirements", "Baseline-feasibility requirements",
    "Blocked and excluded data accounting", "Acquisition and corpus-build boundary",
    "Explicit current readiness finding", "Stage 3 execution separation",
    "Stage 4 separation", "Canonical routing posture", "Explicit non-approvals",
    "Recommended next ticket", "Machine-checkable assignments", "Acceptance criteria",
]
RECORD_REQUIREMENTS = [
    "canonical route", "historical identity and rules", "market family",
    "resolver/source", "observation authority", "measurement semantics",
    "resolution label", "observation timing", "input timing", "archive layer",
    "point-in-time provenance", "selection provenance", "traps and adjudication",
    "disposition",
]
READINESS_DIMENSIONS = [
    "source/resolver compatibility", "point-in-time provenance coverage",
    "publication-time availability coverage", "revision/finality coverage",
    "market-family coverage", "station/source coverage", "temporal/year coverage",
    "threshold/comparator coverage", "forecast-horizon coverage where applicable",
    "trap-category coverage", "blocked/excluded-example accounting",
    "strict temporal OOS feasibility", "leave-station-out feasibility where applicable",
    "leave-year-out feasibility where applicable", "climatology baseline feasibility",
    "persistence baseline feasibility", "calibration/threshold-bucket feasibility",
    "sample-size and uncertainty reporting",
]
ASSIGNMENTS = [
    "ticket_id: WEATHER-BOT-STAGE3-SOURCE-COMPATIBLE-HISTORICAL-CORPUS-READINESS-PLANNING-01",
    "immediate_predecessor_pr: pr_384",
    "actual_merge_sha: b374dbc1c726abf6d3e167ce215229ac47fbf98c",
    "artifact_scope: docs_static_test_only",
    "conceptual_unit: source_compatible_historical_market_evaluation_example_tied_to_venue_defined_settlement_outcome",
    "current_corpus: five_static_stage2_examples_only",
    "synthetic_fixture_count: 3", "real_source_backed_fixture_count: 2",
    "per_record_contract: defined_planning_only", "coverage_readiness: not_established",
    "strict_oos_feasibility: not_demonstrated", "sample_sufficiency: not_established",
    "stage3_scoring_readiness: not_ready", "acquisition_authority: not_approved",
    "stage3_execution_authority: not_approved", "stage4_posture: separate_and_unapproved",
    "canonical_routing_field: condition_id", "canonical_routing_field: token_id",
    "canonical_routing_field: outcome", "non_routing_field: market_id",
    "derived_identifier_field: token_outcome_pair",
    f"recommended_next_ticket: {SUCCESSOR}",
]


def _sections() -> dict[str, str]:
    text = DOC.read_text(encoding="utf-8")
    headings = [line[3:] for line in text.splitlines() if line.startswith("## ")]
    assert headings == HEADINGS
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:]
            sections[current] = []
        elif current:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def _first_column(section: str) -> list[str]:
    rows = [line for line in section.splitlines() if line.startswith("| ")][1:]
    return [line.strip("|").split("|")[0].strip() for line in rows]


def test_predecessor_scope_and_five_example_baseline_are_frozen() -> None:
    sections = _sections()
    predecessor = sections["Immediate predecessor and merge verification"]
    assert "PR #384" in predecessor
    assert "b374dbc1c726abf6d3e167ce215229ac47fbf98c" in predecessor
    scope = sections["Status and scope"]
    assert "(1) per-record usability, (2) corpus-level coverage, and (3) sample-sufficiency assessment" in scope
    assert "does not perform (4) data acquisition or creation or (5) Stage 3 scoring execution" in scope
    assert "source-compatible venue settlement truth, not generic weather truth" in scope
    assert "controlling resolver, source chain, rule version, measurement semantics, and finality treatment" in scope
    baseline = sections["Current five-example corpus baseline"]
    assert "exactly five Stage 2 static JSON fixtures" in baseline
    assert "three synthetic historical-label examples and two real source-backed examples" in baseline
    assert "not sufficient for meaningful strict-OOS retrospective scoring" in baseline


def test_record_contract_and_readiness_dimensions_are_exact() -> None:
    sections = _sections()
    assert _first_column(sections["Per-record usability requirements"]) == RECORD_REQUIREMENTS
    assert _first_column(sections["Corpus-readiness dimensions"]) == READINESS_DIMENSIONS
    record = sections["Per-record usability requirements"]
    assert "Exactly one of `usable`, `blocked`, or `excluded`" in record
    assert "conceptual review requirements, not fields for a production schema" in record


def test_sufficiency_oos_baselines_and_accounting_fail_closed() -> None:
    sections = _sections()
    sufficiency = sections["Sample-sufficiency assessment method"]
    required_diagnostics = (
        "counts by relevant family/source/station/year/horizon/threshold stratum",
        "usable versus blocked/excluded counts", "provenance-complete versus incomplete counts",
        "temporal coverage", "split/fold feasibility", "baseline-history availability",
        "sparse-stratum identification", "uncertainty/sample-support visibility",
    )
    assert all(value in sufficiency for value in required_diagnostics)
    assert "There is no universal numeric minimum sample count" in sufficiency
    assert "No universal numeric minimum is selected here" in sufficiency
    assert "Before test outcomes are inspected" in sufficiency
    assert "sample-support/sufficiency policy" in sufficiency
    assert "thresholds or decision rules" in sufficiency
    for support_axis in ("metric", "diagnostic", "split", "baseline", "claim", "fold", "role", "stratum"):
        assert support_axis in sufficiency
    assert "sparse-bucket handling" in sufficiency
    assert "pooling rules" in sufficiency
    assert "may not be changed after seeing test outcomes" in sufficiency
    assert "uncertainty method" in sufficiency
    assert "uncertainty interval level" in sufficiency
    assert "Sparse or insufficient strata remain blocked or insufficient rather than being silently pooled" in sufficiency
    assert 'post-hoc declaration that observed sample counts are "good enough."' in sufficiency
    assert "The five current examples do not establish sample sufficiency" in sufficiency
    assert "fails closed" in sufficiency
    oos = sections["Strict-OOS feasibility requirements"]
    assert "no overlap or leakage" in oos
    dimensions = sections["Corpus-readiness dimensions"]
    assert "train/calibration/test roles" in dimensions
    assert "train/validation/test roles" not in dimensions
    assert "leave-station-out feasibility where applicable" in dimensions
    assert "leave-year-out feasibility where applicable" in dimensions
    assert "The predeclared persisted quantity and conversion rule have a compatible prior state legitimately available before `prediction_as_of` and the applicable cutoff" in dimensions
    baseline = sections["Baseline-feasibility requirements"]
    assert "held-out data" in baseline
    assert "already-predeclared persisted quantity identity, conversion-rule identity, compatible prior state, and point-in-time availability" in baseline
    assert "before `prediction_as_of` and the applicable cutoff" in baseline
    assert "A previous observation existing somewhere in history is not enough" in baseline
    assert "This plan does not define either policy" in baseline
    accounting = sections["Blocked and excluded data accounting"]
    assert "silently dropping failures" in accounting
    assert "cannot inflate usable sample support" in accounting


def test_acquisition_execution_and_stage4_boundaries_are_frozen() -> None:
    sections = _sections()
    acquisition = sections["Acquisition and corpus-build boundary"]
    possible_inputs = (
        "venue market and rule history", "official resolver/archive observations",
        "station metadata", "first-posted, preliminary, revised, and final archive layers",
        "historical forecast/model products", "publication and availability metadata",
        "reviewer/adjudication evidence",
    )
    assert all(value in acquisition for value in possible_inputs)
    assert "Corpus building requires a separate explicit approval boundary" in acquisition
    non_approvals = sections["Explicit non-approvals"]
    forbidden = (
        "corpus construction or expansion", "external acquisition", "source fetching",
        "provider/API connectors", "scraping/downloads", "credentials", "probability generation",
        "model training/calibration", "split execution", "baseline execution",
        "score/diagnostic computation", "evaluation execution", "result generation",
        "claim generation", "evidence-gate execution/passage", "persistence",
        "reports/exports", "paper simulation", "runtime observation", "trading",
        "order placement", "production runtime", "autonomy",
    )
    assert all(value in non_approvals for value in forbidden)
    assert "does not approve or implement" in non_approvals
    assert not any(
        affirmative in DOC.read_text(encoding="utf-8")
        for affirmative in (
            "data acquisition is approved", "source fetching is approved",
            "scoring execution is approved", "evaluation execution is approved",
            "Stage 4 is approved", "trading is approved", "autonomy is approved",
        )
    )
    assert "remains separate and unapproved" in sections["Stage 4 separation"]


def test_current_finding_routing_assignments_and_single_successor_are_exact() -> None:
    sections = _sections()
    finding = sections["Explicit current readiness finding"]
    for value in ("Coverage readiness: `not_established`", "Strict-OOS feasibility: `not_demonstrated`", "Sample sufficiency: `not_established`", "Stage 3 strict-OOS retrospective scoring is `not_ready`"):
        assert value in finding
    routing = sections["Canonical routing posture"]
    assert "exactly `condition_id`, `token_id`, and `outcome`" in routing
    assert "legacy `market_id` identifier remains non-routing only" in routing
    assert "`token_outcome_pair` remains derived only" in routing
    assignment_lines = sections["Machine-checkable assignments"].split("```text\n", 1)[1].split("\n```", 1)[0].splitlines()
    assert assignment_lines == ASSIGNMENTS
    recommendation = sections["Recommended next ticket"]
    assert recommendation.count(SUCCESSOR) == 1
    assert "exactly one recommended successor" in recommendation
    assert "before any data is fetched, acquired, created, downloaded, scraped, generated, or expanded" in recommendation
