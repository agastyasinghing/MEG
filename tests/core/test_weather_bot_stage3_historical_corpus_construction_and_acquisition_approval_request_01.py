"""Independent static oracle for the Stage 3 historical-corpus approval request."""
from __future__ import annotations

from pathlib import Path


DOC = Path("docs/prd/WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-REQUEST-01.md")
TICKET = "WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-REQUEST-01"
SUCCESSOR = "WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-DECISION-01"
EXPECTED_HEADINGS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Current corpus/readiness state",
    "Approval-request purpose",
    "Requested future corpus scope",
    "Historical/offline acquisition boundary",
    "Source/evidence requirements",
    "Point-in-time/no-lookahead boundary",
    "Data storage and artifact boundary",
    "Corpus inclusion/exclusion boundary",
    "Sample-support/predeclaration boundary",
    "Provider/access-method boundary",
    "Explicit non-approvals",
    "Human decision options",
    "Current request status",
    "Human approval requirement",
    "Canonical routing posture",
    "Recommended next ticket",
    "Machine-checkable assignments",
    "Acceptance criteria",
]
EXPECTED_ASSIGNMENTS = [
    f"ticket_id: {TICKET}",
    "immediate_predecessor_pr: pr_385",
    "actual_merge_sha: dc52bb3c3e2241880a3d1bb850c755804740810f",
    "artifact_scope: docs_static_test_only",
    "request_posture: approval_request_only",
    "approval_decision_posture: approval_decision_not_recorded",
    "current_corpus: five_static_stage2_examples_only",
    "synthetic_example_count: 3",
    "real_source_backed_example_count: 2",
    "corpus_coverage: not_established",
    "sample_sufficiency: not_established",
    "strict_oos_feasibility: not_demonstrated",
    "stage3_scoring_readiness: not_ready",
    "corpus_construction_authority: not_approved",
    "data_acquisition_authority: not_approved",
    "live_provider_runtime_authority: not_approved",
    "canonical_routing_field: condition_id",
    "canonical_routing_field: token_id",
    "canonical_routing_field: outcome",
    "non_routing_legacy_identifier: market_id",
    "derived_identifier: token_outcome_pair",
    "decision_option: approve_narrow_historical_corpus_construction_and_acquisition",
    "decision_option: request_approval_request_revision",
    "decision_option: hold",
    "decision_option: block",
    f"recommended_next_ticket: {SUCCESSOR}",
]
EXPECTED_DECISIONS = [
    "approve_narrow_historical_corpus_construction_and_acquisition",
    "request_approval_request_revision",
    "hold",
    "block",
]
EXPECTED_ACCESS_POSTURES = [
    "manual_source_review",
    "static_public_reference",
    "offline_public_file_acquisition",
    "offline_public_api_acquisition",
    "source_specific_credentials_required",
    "scraping_requires_separate_approval",
    "live_runtime_provider_requires_separate_approval",
]


def _text() -> str:
    assert DOC.as_posix() == (
        "docs/prd/WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-"
        "APPROVAL-REQUEST-01.md"
    )
    return DOC.read_text(encoding="utf-8")


def _sections(text: str) -> dict[str, str]:
    headings = [line[3:] for line in text.splitlines() if line.startswith("## ")]
    assert headings == EXPECTED_HEADINGS
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:]
            sections[current] = []
        elif current:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def _code_block_lines(section: str) -> list[str]:
    return section.split("```text\n", 1)[1].split("\n```", 1)[0].splitlines()


def _literal_bullets(section: str) -> list[str]:
    return [line[3:-1] for line in section.splitlines() if line.startswith("- `") and line.endswith("`")]


def test_exact_path_predecessor_headings_and_assignments() -> None:
    text = _text()
    sections = _sections(text)
    predecessor = sections["Immediate predecessor and merge verification"]
    assert "PR #385" in predecessor
    assert "dc52bb3c3e2241880a3d1bb850c755804740810f" in predecessor
    assert _code_block_lines(sections["Machine-checkable assignments"]) == EXPECTED_ASSIGNMENTS


def test_request_only_scope_and_five_example_baseline_are_frozen() -> None:
    sections = _sections(_text())
    scope = sections["Status and scope"]
    assert "approval-request-only, docs/static-test-only" in scope
    assert "not the approval decision" in scope
    assert "does not authorize implementation" in scope
    assert "does not acquire, download, fetch, scrape, generate, create, or expand data" in scope
    assert "No corpus pipeline is implemented" in scope
    baseline = sections["Current corpus/readiness state"]
    assert "exactly five Stage 2 static weather JSON examples" in baseline
    assert "exactly 3 synthetic historical-label examples" in baseline
    assert "exactly 2 real source-backed examples" in baseline
    assert "not promoted into a historical corpus" in baseline
    assert "Corpus coverage is not established" in baseline
    assert "strict-OOS feasibility is not demonstrated" in baseline
    assert "sample sufficiency is not established" in baseline
    assert "Stage 3 scoring is not ready" in baseline


def test_future_scope_is_narrow_historical_offline_work_only() -> None:
    section = _sections(_text())["Requested future corpus scope"]
    requested = (
        "historical market and venue-rule collection",
        "official resolver/source historical evidence collection",
        "station or observation-point metadata collection",
        "historical resolution-label construction",
        "first-posted, preliminary, revised, and final archive-layer preservation",
        "publication and availability timestamp capture",
        "historical forecast/model input collection",
        "point-in-time provenance capture",
        "station/source-selection provenance",
        "trap/reviewer/adjudication evidence",
        "`usable`, `blocked`, or `excluded` dispositioning",
        "corpus manifest and audit metadata",
        "offline corpus validation",
        "corpus coverage/support reporting",
    )
    assert all(value in section for value in requested)
    assert "requested future capability only" in section
    assert "None is performed or authorized now" in section


def test_acquisition_live_provider_and_access_boundaries_are_distinct() -> None:
    sections = _sections(_text())
    acquisition = sections["Historical/offline acquisition boundary"]
    assert "distinct from live runtime provider integration" in acquisition
    assert "would not grant permission to call arbitrary APIs, scrape arbitrary sites" in acquisition
    assert "only access methods expressly allowed by the later human decision" in acquisition
    assert "Unknown source or access requirements fail closed" in acquisition
    assert "no provider, endpoint, API key, credential, or storage path" in acquisition
    access = sections["Provider/access-method boundary"]
    assert _literal_bullets(access) == EXPECTED_ACCESS_POSTURES
    assert "grants none of these execution authorities" in access
    assert "cannot be interpreted as live-source runtime approval" in access


def test_evidence_point_in_time_and_inclusion_requirements_fail_closed() -> None:
    sections = _sections(_text())
    evidence = sections["Source/evidence requirements"]
    for value in (
        "venue-defined settlement truth", "historical contract/rule identity",
        "rule version effective at the relevant time", "resolver/source identity",
        "source publication time and source availability time",
        "observation valid time and observation availability time",
        "forecast/input publication and availability time",
        "archive/revision/finality layer", "station/source-selection provenance",
        "trap/adjudication evidence and reviewer evidence", "corpus disposition and reason",
    ):
        assert value in evidence
    point_in_time = sections["Point-in-time/no-lookahead boundary"]
    for protection in (
        "observation/event time and legitimate publication/availability time",
        "final archive information substituted into an earlier as-of view",
        "future revisions used before availability",
        "labels used before legitimate resolution availability",
        "future forecasts", "hindsight station selection", "hindsight source selection",
        "hindsight rule interpretation", "test-outcome-informed corpus inclusion",
        "silently replacing unavailable historical evidence with modern values",
        "silently collapsing incompatible archive layers",
    ):
        assert protection in point_in_time
    inclusion = sections["Corpus inclusion/exclusion boundary"]
    assert "`usable`, `blocked`, or `excluded`" in inclusion
    assert "Eventual test outcomes must not determine" in inclusion
    assert "fails closed" in inclusion


def test_storage_and_sample_support_decisions_remain_later_and_predeclared() -> None:
    sections = _sections(_text())
    storage = sections["Data storage and artifact boundary"]
    assert "selects no final storage path, file format, repository-commit policy, database, or dataset size" in storage
    assert "Large datasets are not authorized for Git by default" in storage
    support = sections["Sample-support/predeclaration boundary"]
    assert "No universal numeric minimum is selected here" in support
    assert "predeclared before test inspection" in support
    assert "sparse or insufficient strata fail closed" in support
    assert "pooling rules must be predeclared" in support
    assert "uncertainty method and interval level must be predeclared" in support
    assert "exact primary split roles are `train`, `calibration`, and `test`" in support
    assert "train/validation/test" not in support


def test_decision_options_are_exact_unselected_and_authorities_are_not_approved() -> None:
    sections = _sections(_text())
    decisions = sections["Human decision options"]
    assert _literal_bullets(decisions) == EXPECTED_DECISIONS
    assert "does not select an option" in decisions
    status = sections["Current request status"]
    assert "`approval_decision_not_recorded`" in status
    assert "each `not_approved`" in status
    assert "remain blocked pending an explicit human selection" in status
    human = sections["Human approval requirement"]
    assert "Only a human may choose" in human
    assert "implementation would require its own subsequent, narrowly bounded contract" in human


def test_execution_stage4_runtime_and_trading_remain_unapproved() -> None:
    text = _text()
    non_approvals = _sections(text)["Explicit non-approvals"]
    for boundary in (
        "model training", "probability generation", "split execution", "baseline execution",
        "Brier/log/CRPS/twCRPS computation", "calibration/diagnostic execution",
        "evaluation execution", "result generation", "claim generation",
        "evidence-gate execution or passage", "Stage 4", "live provider runtime integration",
        "production runtime", "trading", "order placement", "autonomy",
    ):
        assert boundary in non_approvals
    forbidden_authority = (
        "corpus construction is approved", "data acquisition is approved",
        "live provider runtime is approved", "probability generation is approved",
        "scoring is approved", "evaluation is approved", "Stage 4 is approved",
        "trading is approved", "order placement is approved", "autonomy is approved",
    )
    assert not any(value in text for value in forbidden_authority)


def test_canonical_route_and_only_successor_are_exact() -> None:
    sections = _sections(_text())
    routing = sections["Canonical routing posture"]
    assert "exactly `condition_id`, `token_id`, and `outcome`" in routing
    assert "legacy `market_id` identifier is non-routing only" in routing
    assert "`token_outcome_pair` is derived only" in routing
    assert "no alternate routing identity is introduced" in routing
    recommendation = sections["Recommended next ticket"]
    assert recommendation.count(SUCCESSOR) == 1
    assert "exactly one recommended successor" in recommendation
    assert "Corpus implementation must not be recommended until a decision is explicitly recorded" in recommendation
