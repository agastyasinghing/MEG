from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

TOP_LEVEL_REQUIRED_KEYS = {
    "candidate_pair_ref",
    "schema_version",
    "pair_status",
    "created_by",
    "created_at",
    "kalshi_leg",
    "polymarket_leg",
    "semantic_match_evidence",
    "temporal_match_evidence",
    "rule_resolution_evidence",
    "fee_liquidity_evidence",
    "platform_mode_evidence",
    "cross_platform_risk_flags",
    "review_envelope",
    "posture",
}

PAIR_STATUS_ALLOWLIST = {
    "candidate_pending_review",
    "rejected",
    "approved_for_research",
    "deferred",
}
BLOCKED_PAIR_STATUSES = {
    "equivalent_auto_approved",
    "execution_ready",
    "order_ready",
    "live_trade_ready",
    "autonomous_approved",
}

KALSHI_LEG_REQUIRED_KEYS = {
    "source_platform",
    "ticker_ref",
    "event_ticker_ref",
    "title",
    "yes_sub_title",
    "no_sub_title",
    "market_type",
    "status",
    "result_raw",
    "open_time",
    "close_time",
    "fetched_at",
    "source_doc_ref",
}

POLYMARKET_LEG_REQUIRED_KEYS = {
    "source_platform",
    "condition_id",
    "source_market_ref",
    "question",
    "slug",
    "outcome_labels",
    "clob_token_refs",
    "active",
    "closed",
    "end_date",
    "fetched_at",
    "source_doc_ref",
}

SEMANTIC_EVIDENCE_REQUIRED_KEYS = {
    "proposition_match_score",
    "entity_match_score",
    "outcome_compatibility_score",
    "semantic_notes",
    "similar_title_only",
    "title_only_match_blocked",
}

TEMPORAL_EVIDENCE_REQUIRED_KEYS = {
    "kalshi_open_time",
    "kalshi_close_time",
    "polymarket_end_date",
    "time_window_score",
    "timezone_normalization_status",
    "temporal_notes",
}

RULE_EVIDENCE_REQUIRED_KEYS = {
    "kalshi_rule_source_ref",
    "polymarket_resolution_source_ref",
    "rule_snapshot_refs",
    "resolution_criteria_compared",
    "rule_compatibility_score",
    "rule_notes",
}

FEE_LIQUIDITY_REQUIRED_KEYS = {
    "fee_comparison_status",
    "liquidity_comparison_status",
    "slippage_haircut_status",
    "executable_price_basis",
    "fee_liquidity_notes",
}

ALLOWED_EXECUTABLE_PRICE_BASIS = {
    "executable_bid_ask_only",
    "not_evaluated",
}
BLOCKED_EXECUTABLE_PRICE_BASIS = {
    "midpoint_only",
    "display_price_only",
    "last_trade_only",
}

PLATFORM_MODE_REQUIRED_KEYS = {
    "kalshi_status_checked",
    "polymarket_status_checked",
    "geo_or_regulatory_mode_checked",
    "venue_mode_notes",
}

RISK_FLAGS_REQUIRED_KEYS = {
    "rule_mismatch_risk",
    "temporal_mismatch_risk",
    "outcome_model_mismatch_risk",
    "fee_liquidity_gap_risk",
    "platform_mode_risk",
    "geo_regulatory_risk",
    "unresolved_mapping_risk",
    "us_vs_international_polymarket_ambiguity",
}

REVIEW_ENVELOPE_REQUIRED_KEYS = {
    "human_review_required",
    "reviewer_ref",
    "reviewed_at",
    "review_decision",
    "review_rationale",
    "rejection_reasons",
}

REVIEW_DECISION_ALLOWLIST = {
    "pending",
    "approved_for_research",
    "rejected",
    "deferred",
}

POSTURE_REQUIRED_KEYS = {
    "research_only",
    "equivalence_claim_allowed",
    "opportunity_label_allowed",
    "execution_allowed",
    "order_routing_allowed",
    "live_trading_allowed",
    "autonomous_execution_allowed",
}


VALID_PENDING_CANDIDATE_PAIR = {
    "candidate_pair_ref": "cp_kx_pm_0001",
    "schema_version": "0B-24.v1",
    "pair_status": "candidate_pending_review",
    "created_by": "phase0b_static_test",
    "created_at": "2026-05-21T00:00:00Z",
    "kalshi_leg": {
        "source_platform": "kalshi",
        "ticker_ref": "KXTEST-2026-YESNO",
        "event_ticker_ref": "KXTEST-2026",
        "title": "Will Example Event happen by date?",
        "yes_sub_title": "Yes if event happens by end date.",
        "no_sub_title": "No otherwise.",
        "market_type": "binary",
        "status": "open",
        "result_raw": None,
        "open_time": "2026-05-20T00:00:00Z",
        "close_time": "2026-05-30T00:00:00Z",
        "fetched_at": "2026-05-21T00:05:00Z",
        "source_doc_ref": "kalshi://market/KXTEST-2026-YESNO",
    },
    "polymarket_leg": {
        "source_platform": "polymarket",
        "condition_id": "0xconditionexample",
        "source_market_ref": "poly-12345",
        "question": "Will Example Event happen by date?",
        "slug": "will-example-event-happen",
        "outcome_labels": ["Yes", "No"],
        "clob_token_refs": ["0xtokenyes", "0xtokenno"],
        "active": True,
        "closed": False,
        "end_date": "2026-05-30T00:00:00Z",
        "fetched_at": "2026-05-21T00:06:00Z",
        "source_doc_ref": "polymarket://market/poly-12345",
    },
    "semantic_match_evidence": {
        "proposition_match_score": 0.94,
        "entity_match_score": 0.93,
        "outcome_compatibility_score": 0.95,
        "semantic_notes": "Rule-aware candidate with binary-compatible outcomes.",
        "similar_title_only": False,
        "title_only_match_blocked": True,
    },
    "temporal_match_evidence": {
        "kalshi_open_time": "2026-05-20T00:00:00Z",
        "kalshi_close_time": "2026-05-30T00:00:00Z",
        "polymarket_end_date": "2026-05-30T00:00:00Z",
        "time_window_score": 0.98,
        "timezone_normalization_status": "normalized_to_utc",
        "temporal_notes": "Close and end windows aligned after UTC normalization.",
    },
    "rule_resolution_evidence": {
        "kalshi_rule_source_ref": "kalshi://rules/KXTEST-2026-YESNO",
        "polymarket_resolution_source_ref": "polymarket://resolution/poly-12345",
        "rule_snapshot_refs": ["snapshot-kx-001", "snapshot-pm-001"],
        "resolution_criteria_compared": True,
        "rule_compatibility_score": 0.92,
        "rule_notes": "Resolution criteria compared and considered compatible pending human review.",
    },
    "fee_liquidity_evidence": {
        "fee_comparison_status": "not_evaluated",
        "liquidity_comparison_status": "not_evaluated",
        "slippage_haircut_status": "not_evaluated",
        "executable_price_basis": "not_evaluated",
        "fee_liquidity_notes": "Phase 0B candidate remains research-only until reviewed.",
    },
    "platform_mode_evidence": {
        "kalshi_status_checked": True,
        "polymarket_status_checked": True,
        "geo_or_regulatory_mode_checked": True,
        "venue_mode_notes": "Both sides checked for venue/regulatory mode constraints.",
    },
    "cross_platform_risk_flags": {
        "rule_mismatch_risk": False,
        "temporal_mismatch_risk": False,
        "outcome_model_mismatch_risk": False,
        "fee_liquidity_gap_risk": True,
        "platform_mode_risk": False,
        "geo_regulatory_risk": False,
        "unresolved_mapping_risk": True,
        "us_vs_international_polymarket_ambiguity": True,
    },
    "review_envelope": {
        "human_review_required": True,
        "reviewer_ref": None,
        "reviewed_at": None,
        "review_decision": "pending",
        "review_rationale": "Pending manual rule and mapping review.",
        "rejection_reasons": [],
    },
    "posture": {
        "research_only": True,
        "equivalence_claim_allowed": False,
        "opportunity_label_allowed": False,
        "execution_allowed": False,
        "order_routing_allowed": False,
        "live_trading_allowed": False,
        "autonomous_execution_allowed": False,
    },
}


def _validate_required_keys(record: dict[str, object], required_keys: set[str], section_name: str) -> None:
    missing = sorted(required_keys - set(record))
    assert not missing, f"{section_name} missing required keys: {missing}"


def _validate_candidate_pair(record: dict[str, object]) -> None:
    _validate_required_keys(record, TOP_LEVEL_REQUIRED_KEYS, "candidate_pair")

    pair_status = record["pair_status"]
    assert pair_status in PAIR_STATUS_ALLOWLIST
    assert pair_status not in BLOCKED_PAIR_STATUSES

    kalshi_leg = record["kalshi_leg"]
    polymarket_leg = record["polymarket_leg"]
    semantic = record["semantic_match_evidence"]
    temporal = record["temporal_match_evidence"]
    rules = record["rule_resolution_evidence"]
    fee_liquidity = record["fee_liquidity_evidence"]
    platform_mode = record["platform_mode_evidence"]
    risk_flags = record["cross_platform_risk_flags"]
    review = record["review_envelope"]
    posture = record["posture"]

    assert isinstance(kalshi_leg, dict)
    assert isinstance(polymarket_leg, dict)

    _validate_required_keys(kalshi_leg, KALSHI_LEG_REQUIRED_KEYS, "kalshi_leg")
    _validate_required_keys(polymarket_leg, POLYMARKET_LEG_REQUIRED_KEYS, "polymarket_leg")
    _validate_required_keys(semantic, SEMANTIC_EVIDENCE_REQUIRED_KEYS, "semantic_match_evidence")
    _validate_required_keys(temporal, TEMPORAL_EVIDENCE_REQUIRED_KEYS, "temporal_match_evidence")
    _validate_required_keys(rules, RULE_EVIDENCE_REQUIRED_KEYS, "rule_resolution_evidence")
    _validate_required_keys(fee_liquidity, FEE_LIQUIDITY_REQUIRED_KEYS, "fee_liquidity_evidence")
    _validate_required_keys(platform_mode, PLATFORM_MODE_REQUIRED_KEYS, "platform_mode_evidence")
    _validate_required_keys(risk_flags, RISK_FLAGS_REQUIRED_KEYS, "cross_platform_risk_flags")
    _validate_required_keys(review, REVIEW_ENVELOPE_REQUIRED_KEYS, "review_envelope")
    _validate_required_keys(posture, POSTURE_REQUIRED_KEYS, "posture")

    assert semantic["similar_title_only"] is False
    assert semantic["title_only_match_blocked"] is True

    assert fee_liquidity["executable_price_basis"] in ALLOWED_EXECUTABLE_PRICE_BASIS
    assert fee_liquidity["executable_price_basis"] not in BLOCKED_EXECUTABLE_PRICE_BASIS

    assert review["human_review_required"] is True
    assert review["review_decision"] in REVIEW_DECISION_ALLOWLIST

    assert posture["research_only"] is True
    assert posture["execution_allowed"] is False
    assert posture["order_routing_allowed"] is False
    assert posture["live_trading_allowed"] is False
    assert posture["autonomous_execution_allowed"] is False

    if pair_status != "rejected":
        assert rules["resolution_criteria_compared"] is True
        assert platform_mode["kalshi_status_checked"] is True
        assert platform_mode["polymarket_status_checked"] is True
        assert platform_mode["geo_or_regulatory_mode_checked"] is True

    if review["review_decision"] == "approved_for_research":
        assert posture["execution_allowed"] is False
        assert posture["order_routing_allowed"] is False
        assert posture["live_trading_allowed"] is False
        assert posture["autonomous_execution_allowed"] is False

    if posture["equivalence_claim_allowed"]:
        assert review["review_decision"] == "approved_for_research"

    if posture["opportunity_label_allowed"]:
        assert posture["equivalence_claim_allowed"] is True
        assert risk_flags["unresolved_mapping_risk"] is False


def _doc_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").lower()


def test_valid_pending_candidate_shape_passes() -> None:
    _validate_candidate_pair(deepcopy(VALID_PENDING_CANDIDATE_PAIR))


def test_missing_top_level_field_fails() -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate.pop("created_at")
    with pytest.raises(AssertionError, match="candidate_pair missing required keys"):
        _validate_candidate_pair(candidate)


def test_missing_kalshi_leg_field_fails() -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["kalshi_leg"].pop("ticker_ref")
    with pytest.raises(AssertionError, match="kalshi_leg missing required keys"):
        _validate_candidate_pair(candidate)


def test_missing_polymarket_leg_field_fails() -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["polymarket_leg"].pop("condition_id")
    with pytest.raises(AssertionError, match="polymarket_leg missing required keys"):
        _validate_candidate_pair(candidate)


@pytest.mark.parametrize("title_only_flag,blocked_flag", [(True, True), (False, False), (True, False)])
def test_title_only_match_is_blocked(title_only_flag: bool, blocked_flag: bool) -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["semantic_match_evidence"]["similar_title_only"] = title_only_flag
    candidate["semantic_match_evidence"]["title_only_match_blocked"] = blocked_flag
    with pytest.raises(AssertionError):
        _validate_candidate_pair(candidate)


def test_missing_resolution_comparison_fails_for_non_rejected_candidate() -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["rule_resolution_evidence"]["resolution_criteria_compared"] = False
    with pytest.raises(AssertionError):
        _validate_candidate_pair(candidate)


@pytest.mark.parametrize(
    "blocked_basis", ["midpoint_only", "display_price_only", "last_trade_only"]
)
def test_blocked_executable_price_basis_rejected(blocked_basis: str) -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["fee_liquidity_evidence"]["executable_price_basis"] = blocked_basis
    with pytest.raises(AssertionError):
        _validate_candidate_pair(candidate)


@pytest.mark.parametrize("mode_key", [
    "kalshi_status_checked",
    "polymarket_status_checked",
    "geo_or_regulatory_mode_checked",
])
def test_unchecked_platform_modes_fail_for_non_rejected_candidate(mode_key: str) -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["platform_mode_evidence"][mode_key] = False
    with pytest.raises(AssertionError):
        _validate_candidate_pair(candidate)


def test_human_review_required_is_enforced() -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["review_envelope"]["human_review_required"] = False
    with pytest.raises(AssertionError):
        _validate_candidate_pair(candidate)


def test_execution_order_live_and_autonomy_flags_must_be_false() -> None:
    for key in ["execution_allowed", "order_routing_allowed", "live_trading_allowed", "autonomous_execution_allowed"]:
        candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
        candidate["posture"][key] = True
        with pytest.raises(AssertionError):
            _validate_candidate_pair(candidate)


@pytest.mark.parametrize("blocked_status", sorted(BLOCKED_PAIR_STATUSES))
def test_blocked_pair_statuses_are_rejected(blocked_status: str) -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["pair_status"] = blocked_status
    with pytest.raises(AssertionError):
        _validate_candidate_pair(candidate)


def test_approved_for_research_does_not_imply_execution() -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["pair_status"] = "approved_for_research"
    candidate["review_envelope"]["review_decision"] = "approved_for_research"
    candidate["review_envelope"]["reviewer_ref"] = "reviewer-001"
    candidate["review_envelope"]["reviewed_at"] = "2026-05-21T02:00:00Z"
    _validate_candidate_pair(candidate)


def test_opportunity_label_requires_equivalence_claim() -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["posture"]["opportunity_label_allowed"] = True
    candidate["posture"]["equivalence_claim_allowed"] = False
    with pytest.raises(AssertionError):
        _validate_candidate_pair(candidate)


def test_unresolved_mapping_risk_blocks_opportunity_label_phase0b() -> None:
    candidate = deepcopy(VALID_PENDING_CANDIDATE_PAIR)
    candidate["posture"]["equivalence_claim_allowed"] = True
    candidate["review_envelope"]["review_decision"] = "approved_for_research"
    candidate["posture"]["opportunity_label_allowed"] = True
    candidate["cross_platform_risk_flags"]["unresolved_mapping_risk"] = True
    with pytest.raises(AssertionError):
        _validate_candidate_pair(candidate)


def test_doc_alignment_for_cross_platform_matching_and_review_posture() -> None:
    text_20c = _doc_text("docs/phase0b/0B-20C_CROSS_PLATFORM_SEMANTIC_MATCHING_RESEARCH_PLAN.md")
    assert "rule-aware matching, not title-aware matching" in text_20c
    assert "non-equivalent until proven equivalent" in text_20c
    assert "human review" in text_20c


def test_doc_alignment_for_unresolved_mappings_and_fixture_non_approval() -> None:
    text_21 = _doc_text("docs/phase0b/0B-21_POLYMARKET_TOKEN_OUTCOME_NORMALIZATION_PLAN.md")
    text_22 = _doc_text("docs/phase0b/0B-22_KALSHI_NORMALIZED_FILLS_MARKETS_MAPPING_PLAN.md")
    text_23 = _doc_text("docs/phase0b/0B-23_TINY_FIXTURE_DERIVATION_SCRIPT_PLAN.md")

    assert "unresolved polymarket mapping" in text_21
    assert "should block cross-platform opportunity claims" in text_21
    assert "unresolved kalshi mapping" in text_22
    assert "should block cross-platform opportunity claims" in text_22
    assert "fixture derivation remains blocked" in text_23
    assert "fixture derivation" in text_23
    assert "fixture commit" in text_23
