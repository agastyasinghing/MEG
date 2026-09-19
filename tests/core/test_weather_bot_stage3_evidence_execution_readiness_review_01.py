"""Independent static oracle for the Stage 3 evidence-execution readiness review."""
from __future__ import annotations

from pathlib import Path


DOC = Path("docs/prd/WEATHER-BOT-STAGE3-EVIDENCE-EXECUTION-READINESS-REVIEW-01.md")
EXPECTED_HEADINGS = [
    "Status and scope",
    "Immediate predecessor and merge verification",
    "Stage 3 implementation-chain inventory",
    "Contract boundary versus execution boundary",
    "Historical corpus readiness review",
    "Probability-generation readiness",
    "Split/baseline execution readiness",
    "Scoring and diagnostic execution readiness",
    "Result/claim/gate evidence-generation readiness",
    "Exact missing-capability matrix",
    "Stage 3 evidence-status finding",
    "Stage 4 separation",
    "Safety and non-approval boundary",
    "Canonical routing posture",
    "Recommended next ticket",
    "Machine-checkable assignments",
    "Acceptance criteria",
]
EXPECTED_INVENTORY = [
    ["probability record", "`binary_probability_record.py`", "immutable binary-probability record, mapping adaptation, and fail-closed field/time/provenance validation", "validator only; no candidate probability generation"],
    ["strict OOS split assignment", "`strict_oos_split.py`", "immutable assignment records plus individual and collection validation for roles, cutoffs, availability, overlap, folds, and leakage groups", "assignment validator only; no real-corpus split assignment run"],
    ["baseline contract", "`baseline_contracts.py`", "immutable climatology/persistence definitions and fail-closed contract validation", "definition validator only; no baseline values generated"],
    ["scoring/diagnostic definition", "`scoring_and_diagnostics.py`", "immutable metric/diagnostic definitions and representation/applicability validation", "definition validator only; no metric or diagnostic calculation"],
    ["evaluation result record", "`evaluation_result_record.py`", "immutable typed result payloads/records and validation", "record validator only; no result creation from calculated outputs"],
    ["evaluation claim record", "`evaluation_claim.py`", "immutable claim records and validation against supplied result-record context", "claim validator only; no claim creation from actual evidence"],
    ["evidence-gate decision record", "`evidence_gate_decision.py`", "immutable decision records and gate-visible validation against supplied claim context", "decision validator only; no substantive gate-rule execution or decision creation from actual claims"],
]
EXPECTED_ASSIGNMENTS = [
    "ticket_id: WEATHER-BOT-STAGE3-EVIDENCE-EXECUTION-READINESS-REVIEW-01",
    "immediate_predecessor_pr: pr_383",
    "actual_merge_sha: 6243ed95f8c5276338cd4907f1787170ab0a1a64",
    "stage3_definition: retrospective_probability_scoring_strict_oos",
    "implementation_chain_status: contract_validation_chain_complete",
    "corpus_readiness: not_sample_sufficient",
    "sample_sufficiency: not_established",
    "scoring_execution_readiness: not_ready",
    "evidence_generation_status: no_real_stage3_evidence_generated",
    "evidence_gate_status: not_evaluated_not_passed",
    "stage4_posture: separate_and_unapproved",
    "canonical_routing_field: condition_id",
    "canonical_routing_field: token_id",
    "canonical_routing_field: outcome",
    "non_routing_field: market_id",
    "derived_identifier_field: token_outcome_pair",
    "recommended_next_ticket: WEATHER-BOT-STAGE3-SOURCE-COMPATIBLE-HISTORICAL-CORPUS-READINESS-PLANNING-01",
]
NEXT = "WEATHER-BOT-STAGE3-SOURCE-COMPATIBLE-HISTORICAL-CORPUS-READINESS-PLANNING-01"


def _text() -> str:
    assert DOC.as_posix() == "docs/prd/WEATHER-BOT-STAGE3-EVIDENCE-EXECUTION-READINESS-REVIEW-01.md"
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


def test_predecessor_headings_and_exact_inventory() -> None:
    text = _text()
    sections = _sections(text)
    predecessor = sections["Immediate predecessor and merge verification"]
    assert "PR #383" in predecessor
    assert "6243ed95f8c5276338cd4907f1787170ab0a1a64" in predecessor
    inventory = sections["Stage 3 implementation-chain inventory"]
    rows = [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in inventory.splitlines()
        if line.startswith("| ")
    ][2:]
    assert rows == EXPECTED_INVENTORY


def test_contract_execution_corpus_and_evidence_findings_are_explicit() -> None:
    sections = _sections(_text())
    contract = sections["Contract boundary versus execution boundary"]
    assert "contract boundaries, not execution engines" in contract
    assert "do not generate inputs, calculate outputs, orchestrate retrospective evaluation, or create evidence" in contract
    corpus = sections["Historical corpus readiness review"]
    assert "exactly five static JSON examples" in corpus
    assert "Enough source-compatible point-in-time historical examples do **not** currently exist" in corpus
    assert "Sample sufficiency has **not been established**" in corpus
    evidence = sections["Stage 3 evidence-status finding"]
    for literal in (
        "contract_validation_chain_complete",
        "not_sample_sufficient",
        "no_real_stage3_evidence_generated",
        "not_evaluated_not_passed",
        "Stage 3 has not passed",
    ):
        assert literal in evidence


def test_capability_matrix_and_stage4_non_approval() -> None:
    sections = _sections(_text())
    matrix = sections["Exact missing-capability matrix"]
    expected = {
        "seven contract/validation boundaries": "present",
        "source-compatible point-in-time historical corpus": "partial",
        "candidate probability generation": "absent",
        "strict-OOS assignment execution over a real corpus": "absent",
        "climatology baseline generation": "absent",
        "persistence baseline generation": "absent",
        "actual Brier/log/CRPS/twCRPS computation": "absent",
        "calibration/diagnostic computation": "absent",
        "retrospective evaluation orchestration": "absent",
        "evaluation-result creation from calculated outputs": "absent",
        "evaluation-claim creation from actual evidence": "absent",
        "evidence-gate decision creation from actual claims": "absent",
    }
    observed = {}
    for line in matrix.splitlines():
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 3 and cells[1] in {"present", "partial", "absent"}:
            observed[cells[0]] = cells[1]
    assert observed == expected
    stage4 = sections["Stage 4 separation"]
    assert "Stage 4 remains separate and unapproved" in stage4


def test_assignments_routing_and_single_successor_are_exact() -> None:
    sections = _sections(_text())
    assignment_lines = sections["Machine-checkable assignments"].split("```text\n", 1)[1].split("\n```", 1)[0].splitlines()
    assert assignment_lines == EXPECTED_ASSIGNMENTS
    routing = sections["Canonical routing posture"]
    assert "exactly `condition_id`, `token_id`, and `outcome`" in routing
    assert "legacy `market_id` identifier remains non-routing only" in routing
    assert "`token_outcome_pair` remains derived only" in routing
    recommendation = sections["Recommended next ticket"]
    assert recommendation.count(NEXT) == 1
    assert "exactly one recommended substantive successor" in recommendation


def test_no_execution_or_runtime_authority_is_introduced() -> None:
    text = _text()
    non_approvals = _sections(text)["Safety and non-approval boundary"]
    required = (
        "corpus expansion", "source fetching", "provider/API connectors",
        "probability generation", "baseline execution", "scoring execution",
        "diagnostic execution", "evaluation execution", "evidence-gate execution or passage",
        "persistence", "reports/exports", "paper trading", "trading",
        "order placement", "production runtime", "autonomy",
    )
    assert all(item in non_approvals for item in required)
    assert "does not approve or implement" in non_approvals
    forbidden_affirmative_authority = (
        "source fetching is approved",
        "connectors are approved",
        "runtime is approved",
        "paper trading is approved",
        "trading is approved",
        "order placement is approved",
        "autonomy is approved",
        "Stage 4 is approved",
    )
    assert not any(phrase in text for phrase in forbidden_affirmative_authority)
