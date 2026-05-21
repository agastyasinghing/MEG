from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FIELDS = {
    "code",
    "category",
    "severity",
    "decision_effect",
    "blocks_equivalence",
    "blocks_opportunity_label",
    "requires_human_review",
    "description",
    "evidence_required",
    "source_doc_refs",
}

ALLOWED_CATEGORIES = {
    "semantic",
    "rules_resolution",
    "temporal",
    "outcome_model",
    "mapping",
    "price_liquidity_fee",
    "platform_mode",
    "regulatory_geo",
    "evidence_quality",
    "phase0b_posture",
}
ALLOWED_SEVERITIES = {"blocker", "review_required", "informational"}
ALLOWED_DECISION_EFFECTS = {"reject", "defer", "require_manual_review", "annotate_only"}

REQUIRED_CODES = {
    "TITLE_ONLY_MATCH",
    "RULE_TEXT_MISMATCH",
    "RULE_SOURCE_HIERARCHY_MISMATCH",
    "MISSING_RULE_EVIDENCE",
    "RESOLUTION_CRITERIA_NOT_COMPARED",
    "TEMPORAL_WINDOW_MISMATCH",
    "OUTCOME_MODEL_MISMATCH",
    "NEGATIVE_RISK_OR_MULTI_OUTCOME_DEPENDENCY",
    "UNRESOLVED_POLYMARKET_MAPPING",
    "UNRESOLVED_KALSHI_MAPPING",
    "NON_EXECUTABLE_MARKET_STATE",
    "MAINTENANCE_PAUSE_OR_RESTART_MODE",
    "SPORTS_MARKET_START_MODE_RISK",
    "GEO_OR_REGULATORY_MODE_MISMATCH",
    "US_VS_INTL_POLYMARKET_AMBIGUITY",
    "INSUFFICIENT_FEE_OR_LIQUIDITY_EVIDENCE",
    "DISPLAY_OR_MIDPOINT_PRICE_ONLY",
    "MISSING_EXECUTABLE_PRICE_BASIS",
    "MISSING_HUMAN_REVIEW",
    "EXECUTION_POSTURE_REQUESTED_IN_PHASE0B",
    "AUTONOMY_POSTURE_REQUESTED_IN_PHASE0B",
}
FORBIDDEN_CODES = {
    "PROFITABLE_SO_APPROVE",
    "TITLE_SIMILARITY_AUTO_APPROVE",
    "EQUIVALENT_WITHOUT_RULES",
    "EXECUTION_READY",
    "LIVE_TRADE_READY",
    "AUTONOMOUS_APPROVED",
    "BYPASS_GEO_RESTRICTION",
    "IGNORE_FEES",
    "IGNORE_LIQUIDITY",
    "IGNORE_UNRESOLVED_MAPPING",
}

REJECTION_REASON_TAXONOMY = [
    {"code": "TITLE_ONLY_MATCH", "category": "semantic", "severity": "blocker", "decision_effect": "reject", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Title similarity alone is insufficient for equivalence.", "evidence_required": ["rule_text_comparison"], "source_doc_refs": ["0B-20C"]},
    {"code": "RULE_TEXT_MISMATCH", "category": "rules_resolution", "severity": "blocker", "decision_effect": "reject", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Resolution rule text conflicts across venues.", "evidence_required": ["both_rule_snapshots"], "source_doc_refs": ["0B-20C"]},
    {"code": "RULE_SOURCE_HIERARCHY_MISMATCH", "category": "rules_resolution", "severity": "review_required", "decision_effect": "require_manual_review", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Rule source precedence differs and needs manual adjudication.", "evidence_required": ["source_precedence_notes"], "source_doc_refs": ["0B-20C"]},
    {"code": "MISSING_RULE_EVIDENCE", "category": "evidence_quality", "severity": "blocker", "decision_effect": "defer", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Rule or resolution evidence is missing.", "evidence_required": ["rule_snapshot_refs"], "source_doc_refs": ["0B-20C"]},
    {"code": "RESOLUTION_CRITERIA_NOT_COMPARED", "category": "rules_resolution", "severity": "review_required", "decision_effect": "require_manual_review", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Resolution criteria have not yet been compared.", "evidence_required": ["criteria_comparison_record"], "source_doc_refs": ["0B-20C"]},
    {"code": "TEMPORAL_WINDOW_MISMATCH", "category": "temporal", "severity": "blocker", "decision_effect": "reject", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Close/end windows are materially different.", "evidence_required": ["normalized_time_window_diff"], "source_doc_refs": ["0B-20C"]},
    {"code": "OUTCOME_MODEL_MISMATCH", "category": "outcome_model", "severity": "blocker", "decision_effect": "reject", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Outcome models are not compatible.", "evidence_required": ["outcome_model_analysis"], "source_doc_refs": ["0B-20C"]},
    {"code": "NEGATIVE_RISK_OR_MULTI_OUTCOME_DEPENDENCY", "category": "outcome_model", "severity": "review_required", "decision_effect": "require_manual_review", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Negative-risk or multi-outcome dependency introduces ambiguity.", "evidence_required": ["dependency_analysis"], "source_doc_refs": ["0B-20C"]},
    {"code": "UNRESOLVED_POLYMARKET_MAPPING", "category": "mapping", "severity": "blocker", "decision_effect": "defer", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Polymarket mapping unresolved; cannot assert opportunity.", "evidence_required": ["mapping_gap_note"], "source_doc_refs": ["0B-21"]},
    {"code": "UNRESOLVED_KALSHI_MAPPING", "category": "mapping", "severity": "blocker", "decision_effect": "defer", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Kalshi mapping unresolved; cannot assert opportunity.", "evidence_required": ["mapping_gap_note"], "source_doc_refs": ["0B-22"]},
    {"code": "NON_EXECUTABLE_MARKET_STATE", "category": "platform_mode", "severity": "blocker", "decision_effect": "defer", "blocks_equivalence": False, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Market state not executable at review time.", "evidence_required": ["market_state_snapshot"], "source_doc_refs": ["0B-20C", "0B-24"]},
    {"code": "MAINTENANCE_PAUSE_OR_RESTART_MODE", "category": "platform_mode", "severity": "review_required", "decision_effect": "require_manual_review", "blocks_equivalence": False, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Venue maintenance/pause mode requires deferment.", "evidence_required": ["venue_mode_snapshot"], "source_doc_refs": ["0B-20C"]},
    {"code": "SPORTS_MARKET_START_MODE_RISK", "category": "platform_mode", "severity": "review_required", "decision_effect": "require_manual_review", "blocks_equivalence": False, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Sports start-mode behavior creates activation risk.", "evidence_required": ["mode_transition_notes"], "source_doc_refs": ["0B-20C"]},
    {"code": "GEO_OR_REGULATORY_MODE_MISMATCH", "category": "regulatory_geo", "severity": "blocker", "decision_effect": "defer", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Regulatory/geo access mode mismatch.", "evidence_required": ["geo_mode_evidence"], "source_doc_refs": ["0B-20C"]},
    {"code": "US_VS_INTL_POLYMARKET_AMBIGUITY", "category": "regulatory_geo", "severity": "review_required", "decision_effect": "require_manual_review", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Ambiguous US vs international Polymarket context.", "evidence_required": ["market_context_notes"], "source_doc_refs": ["0B-20C"]},
    {"code": "INSUFFICIENT_FEE_OR_LIQUIDITY_EVIDENCE", "category": "price_liquidity_fee", "severity": "review_required", "decision_effect": "require_manual_review", "blocks_equivalence": False, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Fee/liquidity evidence is insufficient.", "evidence_required": ["fee_liquidity_snapshot"], "source_doc_refs": ["0B-20C"]},
    {"code": "DISPLAY_OR_MIDPOINT_PRICE_ONLY", "category": "price_liquidity_fee", "severity": "review_required", "decision_effect": "defer", "blocks_equivalence": False, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Only display or midpoint prices available.", "evidence_required": ["executable_quote_evidence"], "source_doc_refs": ["0B-20C"]},
    {"code": "MISSING_EXECUTABLE_PRICE_BASIS", "category": "price_liquidity_fee", "severity": "blocker", "decision_effect": "defer", "blocks_equivalence": False, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Executable price basis is missing.", "evidence_required": ["executable_price_basis_record"], "source_doc_refs": ["0B-24"]},
    {"code": "MISSING_HUMAN_REVIEW", "category": "evidence_quality", "severity": "blocker", "decision_effect": "defer", "blocks_equivalence": True, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Human review has not been completed.", "evidence_required": ["review_envelope"], "source_doc_refs": ["0B-20C"]},
    {"code": "EXECUTION_POSTURE_REQUESTED_IN_PHASE0B", "category": "phase0b_posture", "severity": "blocker", "decision_effect": "reject", "blocks_equivalence": False, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Phase 0B is research-only; execution posture request rejected.", "evidence_required": ["posture_flags"], "source_doc_refs": ["0B-20C", "0B-24"]},
    {"code": "AUTONOMY_POSTURE_REQUESTED_IN_PHASE0B", "category": "phase0b_posture", "severity": "blocker", "decision_effect": "reject", "blocks_equivalence": False, "blocks_opportunity_label": True, "requires_human_review": True, "description": "Phase 0B forbids autonomous execution posture.", "evidence_required": ["posture_flags"], "source_doc_refs": ["0B-20C", "AGENTS.md"]},
    {"code": "SEMANTIC_NOTES_RECORDED", "category": "semantic", "severity": "informational", "decision_effect": "annotate_only", "blocks_equivalence": False, "blocks_opportunity_label": False, "requires_human_review": False, "description": "Informational annotation of semantic notes only.", "evidence_required": ["semantic_notes"], "source_doc_refs": ["0B-20C"]},
]


def _taxonomy_by_code() -> dict[str, dict[str, object]]:
    return {entry["code"]: entry for entry in REJECTION_REASON_TAXONOMY}


def _validate_taxonomy_shape() -> None:
    codes: set[str] = set()
    for entry in REJECTION_REASON_TAXONOMY:
        assert REQUIRED_FIELDS.issubset(entry.keys())
        code = entry["code"]
        assert code not in codes
        codes.add(code)
        assert entry["category"] in ALLOWED_CATEGORIES
        assert entry["severity"] in ALLOWED_SEVERITIES
        assert entry["decision_effect"] in ALLOWED_DECISION_EFFECTS
        assert entry["source_doc_refs"]
        assert entry["evidence_required"]
        if entry["severity"] == "blocker":
            assert entry["decision_effect"] != "annotate_only"
        if entry["blocks_equivalence"]:
            assert entry["requires_human_review"] or entry["decision_effect"] in {"reject", "defer"}
            assert entry["decision_effect"] in {"reject", "defer", "require_manual_review"}
        if entry["blocks_opportunity_label"]:
            assert entry["decision_effect"] != "annotate_only"
        if entry["category"] == "phase0b_posture":
            assert entry["blocks_opportunity_label"] is True
    taxonomy_codes = set(_taxonomy_by_code())
    assert FORBIDDEN_CODES.isdisjoint(taxonomy_codes)
    assert _taxonomy_by_code()["EXECUTION_POSTURE_REQUESTED_IN_PHASE0B"]["severity"] == "blocker"
    assert _taxonomy_by_code()["AUTONOMY_POSTURE_REQUESTED_IN_PHASE0B"]["severity"] == "blocker"


def _validate_rejection_record(record: dict[str, object]) -> None:
    required = {
        "candidate_pair_ref", "rejection_code", "rejection_category", "decision_effect", "reviewer_required",
        "evidence_refs", "rationale", "created_at", "posture",
    }
    assert required.issubset(record.keys())
    taxonomy = _taxonomy_by_code()
    code = record["rejection_code"]
    assert code in taxonomy
    tax = taxonomy[code]
    assert record["rejection_category"] == tax["category"]
    assert record["decision_effect"] == tax["decision_effect"]
    assert record["rationale"]

    posture = record["posture"]
    assert posture["research_only"] is True
    assert posture["execution_allowed"] is False
    assert posture["order_routing_allowed"] is False
    assert posture["live_trading_allowed"] is False
    assert posture["autonomous_execution_allowed"] is False

    if tax["severity"] in {"blocker", "review_required"}:
        assert record["evidence_refs"]


VALID_REJECTION_RECORD = {
    "candidate_pair_ref": "cp_kx_pm_0012",
    "rejection_code": "MISSING_RULE_EVIDENCE",
    "rejection_category": "evidence_quality",
    "decision_effect": "defer",
    "reviewer_required": True,
    "evidence_refs": ["kalshi_rule_ref_missing", "polymarket_resolution_ref_missing"],
    "rationale": "Cannot proceed without rule snapshots from both venues.",
    "created_at": "2026-05-21T00:00:00Z",
    "posture": {
        "research_only": True,
        "execution_allowed": False,
        "order_routing_allowed": False,
        "live_trading_allowed": False,
        "autonomous_execution_allowed": False,
    },
}


def _doc_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8").lower()


def test_taxonomy_shape_validates() -> None:
    _validate_taxonomy_shape()


def test_required_categories_and_codes_covered() -> None:
    categories = {e["category"] for e in REJECTION_REASON_TAXONOMY}
    assert ALLOWED_CATEGORIES.issubset(categories)
    assert REQUIRED_CODES.issubset(set(_taxonomy_by_code()))


def test_forbidden_codes_absent_and_code_uniqueness() -> None:
    codes = [e["code"] for e in REJECTION_REASON_TAXONOMY]
    assert len(codes) == len(set(codes))
    assert FORBIDDEN_CODES.isdisjoint(set(codes))


def test_blocker_and_blocking_semantics_rules() -> None:
    taxonomy = _taxonomy_by_code()
    for entry in REJECTION_REASON_TAXONOMY:
        if entry["severity"] == "blocker":
            assert entry["decision_effect"] != "annotate_only"
        if entry["blocks_equivalence"]:
            assert entry["decision_effect"] in {"reject", "defer", "require_manual_review"}
        if entry["blocks_opportunity_label"]:
            assert entry["decision_effect"] != "annotate_only"

    assert taxonomy["UNRESOLVED_POLYMARKET_MAPPING"]["blocks_opportunity_label"] is True
    assert taxonomy["UNRESOLVED_KALSHI_MAPPING"]["blocks_opportunity_label"] is True
    assert taxonomy["TITLE_ONLY_MATCH"]["blocks_equivalence"] is True
    assert taxonomy["MISSING_RULE_EVIDENCE"]["blocks_equivalence"] is True
    assert taxonomy["MISSING_EXECUTABLE_PRICE_BASIS"]["blocks_opportunity_label"] is True
    us_intl = taxonomy["US_VS_INTL_POLYMARKET_AMBIGUITY"]
    assert us_intl["blocks_equivalence"] is True or us_intl["decision_effect"] == "require_manual_review"


def test_phase0b_posture_guards_and_non_approval_annotations() -> None:
    taxonomy = _taxonomy_by_code()
    for code in {"EXECUTION_POSTURE_REQUESTED_IN_PHASE0B", "AUTONOMY_POSTURE_REQUESTED_IN_PHASE0B"}:
        entry = taxonomy[code]
        assert entry["category"] == "phase0b_posture"
        assert entry["severity"] == "blocker"
        assert entry["blocks_opportunity_label"] is True

    for entry in REJECTION_REASON_TAXONOMY:
        if entry["severity"] in {"review_required", "informational"}:
            assert entry["decision_effect"] in {"defer", "require_manual_review", "annotate_only"}


def test_candidate_rejection_record_valid() -> None:
    _validate_rejection_record(deepcopy(VALID_REJECTION_RECORD))


def test_candidate_rejection_record_invalid_cases() -> None:
    bad = deepcopy(VALID_REJECTION_RECORD)
    bad["rejection_code"] = "UNKNOWN_CODE"
    with pytest.raises(AssertionError):
        _validate_rejection_record(bad)

    bad = deepcopy(VALID_REJECTION_RECORD)
    bad["rejection_category"] = "semantic"
    with pytest.raises(AssertionError):
        _validate_rejection_record(bad)

    bad = deepcopy(VALID_REJECTION_RECORD)
    bad["decision_effect"] = "reject"
    with pytest.raises(AssertionError):
        _validate_rejection_record(bad)

    bad = deepcopy(VALID_REJECTION_RECORD)
    bad["evidence_refs"] = []
    with pytest.raises(AssertionError):
        _validate_rejection_record(bad)

    bad = deepcopy(VALID_REJECTION_RECORD)
    bad["rationale"] = ""
    with pytest.raises(AssertionError):
        _validate_rejection_record(bad)

    for key in ("execution_allowed", "live_trading_allowed", "autonomous_execution_allowed"):
        bad = deepcopy(VALID_REJECTION_RECORD)
        bad["posture"][key] = True
        with pytest.raises(AssertionError):
            _validate_rejection_record(bad)


def test_doc_alignment_phase0b_semantic_and_mapping_guards() -> None:
    doc20c = _doc_text("docs/phase0b/0B-20C_CROSS_PLATFORM_SEMANTIC_MATCHING_RESEARCH_PLAN.md")
    assert "hard blocker" in doc20c or "hard blockers" in doc20c
    assert "rejection" in doc20c
    assert "similar titles/questions are insufficient" in doc20c or "title-level similarity" in doc20c
    assert "rule-aware matching" in doc20c or "rule aware" in doc20c
    assert "non-equivalent until proven equivalent" in doc20c
    assert "human review" in doc20c
    assert "international polymarket" in doc20c or "polymarket us" in doc20c

    doc21 = _doc_text("docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md")
    assert "unresolved" in doc21 and "mapping" in doc21
    assert "block" in doc21 and "opportunity" in doc21

    doc22 = _doc_text("docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md")
    assert "unresolved" in doc22 and "mapping" in doc22
    assert "block" in doc22 and "opportunity" in doc22

    test24 = _doc_text("tests/core/test_cross_platform_candidate_pair_fixture_shape.py")
    assert "unresolved_mapping_risk" in test24
    assert "blocked_executable_price_basis" in test24 or "missing executable price basis" in test24
