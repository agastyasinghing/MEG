from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
R12_PATH = REPO_ROOT / "docs/phase0b/0B-R12_THRESHOLD_RISK_GATE_CONFIG_SPEC.md"
LEGACY_ID_FIELD = "market" + "_id"

EDGE_BELOW_MINIMUM = "EDGE_BELOW_MINIMUM"
FEE_ADJUSTED_EDGE_BELOW_MINIMUM = "FEE_ADJUSTED_EDGE_BELOW_MINIMUM"
SPREAD_BELOW_MINIMUM = "SPREAD_BELOW_MINIMUM"
CONFIDENCE_BELOW_MINIMUM = "CONFIDENCE_BELOW_MINIMUM"
SEMANTIC_MATCH_BELOW_MINIMUM = "SEMANTIC_MATCH_BELOW_MINIMUM"
LIQUIDITY_BELOW_MINIMUM = "LIQUIDITY_BELOW_MINIMUM"
DATA_QUALITY_BELOW_MINIMUM = "DATA_QUALITY_BELOW_MINIMUM"
MARKET_NOT_ALLOWED = "MARKET_NOT_ALLOWED"
MARKET_BLOCKED = "MARKET_BLOCKED"
PLATFORM_NOT_ALLOWED = "PLATFORM_NOT_ALLOWED"
PLATFORM_BLOCKED = "PLATFORM_BLOCKED"
PER_MARKET_EXPOSURE_EXCEEDED = "PER_MARKET_EXPOSURE_EXCEEDED"
GLOBAL_EXPOSURE_EXCEEDED = "GLOBAL_EXPOSURE_EXCEEDED"
DAILY_LOSS_EXCEEDED = "DAILY_LOSS_EXCEEDED"
MISSING_FEE_ASSUMPTION = "MISSING_FEE_ASSUMPTION"
MISSING_LIQUIDITY_ASSUMPTION = "MISSING_LIQUIDITY_ASSUMPTION"
MISSING_PROVENANCE = "MISSING_PROVENANCE"
MISSING_SOURCE_ID = "MISSING_SOURCE_ID"
OPERATOR_APPROVAL_NOT_REQUIRED = "OPERATOR_APPROVAL_NOT_REQUIRED"
LIVE_TRADING_ENABLED_PHASE0B = "LIVE_TRADING_ENABLED_PHASE0B"
AUTONOMOUS_TRADING_ENABLED_PHASE0B = "AUTONOMOUS_TRADING_ENABLED_PHASE0B"

STANDARDIZED_REJECTION_REASONS = {
    EDGE_BELOW_MINIMUM,
    FEE_ADJUSTED_EDGE_BELOW_MINIMUM,
    SPREAD_BELOW_MINIMUM,
    CONFIDENCE_BELOW_MINIMUM,
    SEMANTIC_MATCH_BELOW_MINIMUM,
    LIQUIDITY_BELOW_MINIMUM,
    DATA_QUALITY_BELOW_MINIMUM,
    MARKET_NOT_ALLOWED,
    MARKET_BLOCKED,
    PLATFORM_NOT_ALLOWED,
    PLATFORM_BLOCKED,
    PER_MARKET_EXPOSURE_EXCEEDED,
    GLOBAL_EXPOSURE_EXCEEDED,
    DAILY_LOSS_EXCEEDED,
    MISSING_FEE_ASSUMPTION,
    MISSING_LIQUIDITY_ASSUMPTION,
    MISSING_PROVENANCE,
    MISSING_SOURCE_ID,
    OPERATOR_APPROVAL_NOT_REQUIRED,
    LIVE_TRADING_ENABLED_PHASE0B,
    AUTONOMOUS_TRADING_ENABLED_PHASE0B,
}

BASE_PHASE0B_CONFIG: dict[str, object] = {
    "config_id": "cfg-phase0b-r15",
    "mode": "fixture",
    "source_id": "phase0b-r15-config-source",
    "provenance": "phase0b-r15-static-screening-tests",
    "dry_run_default": True,
    "require_operator_approval": True,
    "live_trading_enabled": False,
    "autonomous_trading_enabled": False,
    "audit_log_required": True,
    "rejection_reason_required": True,
    "min_edge_bps": 10.0,
    "min_fee_adjusted_edge_bps": 8.0,
    "min_spread_bps": 2.0,
    "min_confidence_score": 0.70,
    "min_semantic_match_score": 0.80,
    "min_liquidity_score": 0.60,
    "min_data_quality_score": 0.75,
    "max_per_market_exposure": 100.0,
    "max_global_exposure": 250.0,
    "max_daily_loss": 50.0,
    "market_allowlist": ["mkt-alpha", "mkt-beta"],
    "market_blocklist": ["mkt-blocked"],
    "platform_allowlist": ["platform-a", "platform-b"],
    "platform_blocklist": ["platform-blocked"],
}

BASE_OPPORTUNITY_CANDIDATE: dict[str, object] = {
    "opportunity_id": "opp-r15-001",
    "source_id": "op-source-001",
    "provenance": "fixture://phase0b/r15/candidate",
    "platform": "platform-a",
    "market_ref": "mkt-alpha",
    "platforms_compared": ["platform-a", "platform-b"],
    "estimated_edge_bps": 12.0,
    "fee_adjusted_edge_bps": 9.0,
    "spread_bps": 2.5,
    "confidence_score": 0.85,
    "semantic_match_score": 0.95,
    "liquidity_score": 0.80,
    "data_quality_score": 0.90,
    "market": "mkt-alpha",
    "fee_assumption_present": True,
    "liquidity_assumption_present": True,
    "current_per_market_exposure": 40.0,
    "current_global_exposure": 120.0,
    "current_daily_loss": 10.0,
}


def _copy_with(obj: dict, **updates) -> dict:
    out = dict(obj)
    out.update(updates)
    return out


def _screen_candidate_static(config: dict, candidate: dict) -> dict:
    reasons: list[str] = []

    if candidate["estimated_edge_bps"] < config["min_edge_bps"]:
        reasons.append(EDGE_BELOW_MINIMUM)
    if candidate["fee_adjusted_edge_bps"] < config["min_fee_adjusted_edge_bps"]:
        reasons.append(FEE_ADJUSTED_EDGE_BELOW_MINIMUM)
    if candidate["spread_bps"] < config["min_spread_bps"]:
        reasons.append(SPREAD_BELOW_MINIMUM)
    if candidate["confidence_score"] < config["min_confidence_score"]:
        reasons.append(CONFIDENCE_BELOW_MINIMUM)
    if candidate["semantic_match_score"] < config["min_semantic_match_score"]:
        reasons.append(SEMANTIC_MATCH_BELOW_MINIMUM)
    if candidate["liquidity_score"] < config["min_liquidity_score"]:
        reasons.append(LIQUIDITY_BELOW_MINIMUM)
    if candidate["data_quality_score"] < config["min_data_quality_score"]:
        reasons.append(DATA_QUALITY_BELOW_MINIMUM)

    if candidate["market"] not in config["market_allowlist"]:
        reasons.append(MARKET_NOT_ALLOWED)
    if candidate["market"] in config["market_blocklist"]:
        reasons.append(MARKET_BLOCKED)
    if candidate["platform"] not in config["platform_allowlist"]:
        reasons.append(PLATFORM_NOT_ALLOWED)
    if candidate["platform"] in config["platform_blocklist"]:
        reasons.append(PLATFORM_BLOCKED)

    if candidate["current_per_market_exposure"] > config["max_per_market_exposure"]:
        reasons.append(PER_MARKET_EXPOSURE_EXCEEDED)
    if candidate["current_global_exposure"] > config["max_global_exposure"]:
        reasons.append(GLOBAL_EXPOSURE_EXCEEDED)
    if candidate["current_daily_loss"] > config["max_daily_loss"]:
        reasons.append(DAILY_LOSS_EXCEEDED)

    if not candidate["fee_assumption_present"]:
        reasons.append(MISSING_FEE_ASSUMPTION)
    if not candidate["liquidity_assumption_present"]:
        reasons.append(MISSING_LIQUIDITY_ASSUMPTION)
    if not str(candidate.get("provenance", "")).strip():
        reasons.append(MISSING_PROVENANCE)
    if not str(candidate.get("source_id", "")).strip():
        reasons.append(MISSING_SOURCE_ID)

    if config["require_operator_approval"] is not True:
        reasons.append(OPERATOR_APPROVAL_NOT_REQUIRED)
    if config["live_trading_enabled"] is True:
        reasons.append(LIVE_TRADING_ENABLED_PHASE0B)
    if config["autonomous_trading_enabled"] is True:
        reasons.append(AUTONOMOUS_TRADING_ENABLED_PHASE0B)

    accepted = len(reasons) == 0
    decision = {
        "opportunity_id": candidate["opportunity_id"],
        "config_id": config["config_id"],
        "accepted": accepted,
        "rejection_reasons": reasons,
        "fail_closed_reason": "screening_threshold_rejection" if reasons else None,
        "thresholds_evaluated": [
            "min_edge_bps",
            "min_fee_adjusted_edge_bps",
            "min_spread_bps",
            "min_confidence_score",
            "min_semantic_match_score",
            "min_liquidity_score",
            "min_data_quality_score",
            "max_per_market_exposure",
            "max_global_exposure",
            "max_daily_loss",
        ],
        "observed_values": {
            "estimated_edge_bps": candidate["estimated_edge_bps"],
            "fee_adjusted_edge_bps": candidate["fee_adjusted_edge_bps"],
            "spread_bps": candidate["spread_bps"],
            "confidence_score": candidate["confidence_score"],
            "semantic_match_score": candidate["semantic_match_score"],
            "liquidity_score": candidate["liquidity_score"],
            "data_quality_score": candidate["data_quality_score"],
            "current_per_market_exposure": candidate["current_per_market_exposure"],
            "current_global_exposure": candidate["current_global_exposure"],
            "current_daily_loss": candidate["current_daily_loss"],
        },
        "decision_timestamp": "2026-01-01T00:00:00Z",
        "proposal_allowed": accepted,
        "execution_allowed": False,
    }
    assert set(decision["rejection_reasons"]) <= STANDARDIZED_REJECTION_REASONS
    return decision


def _assert_rejected_for(decision: dict, expected_reason: str) -> None:
    assert decision["accepted"] is False
    assert expected_reason in decision["rejection_reasons"]


def test_single_breach_matrix() -> None:
    cases = [
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, estimated_edge_bps=9.0), BASE_PHASE0B_CONFIG, EDGE_BELOW_MINIMUM),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, fee_adjusted_edge_bps=7.0), BASE_PHASE0B_CONFIG, FEE_ADJUSTED_EDGE_BELOW_MINIMUM),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, spread_bps=1.0), BASE_PHASE0B_CONFIG, SPREAD_BELOW_MINIMUM),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, confidence_score=0.60), BASE_PHASE0B_CONFIG, CONFIDENCE_BELOW_MINIMUM),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, semantic_match_score=0.70), BASE_PHASE0B_CONFIG, SEMANTIC_MATCH_BELOW_MINIMUM),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, liquidity_score=0.50), BASE_PHASE0B_CONFIG, LIQUIDITY_BELOW_MINIMUM),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, data_quality_score=0.60), BASE_PHASE0B_CONFIG, DATA_QUALITY_BELOW_MINIMUM),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, market="mkt-unknown"), BASE_PHASE0B_CONFIG, MARKET_NOT_ALLOWED),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, market="mkt-blocked"), BASE_PHASE0B_CONFIG, MARKET_BLOCKED),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, platform="platform-x"), BASE_PHASE0B_CONFIG, PLATFORM_NOT_ALLOWED),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, platform="platform-blocked"), BASE_PHASE0B_CONFIG, PLATFORM_BLOCKED),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, current_per_market_exposure=101.0), BASE_PHASE0B_CONFIG, PER_MARKET_EXPOSURE_EXCEEDED),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, current_global_exposure=251.0), BASE_PHASE0B_CONFIG, GLOBAL_EXPOSURE_EXCEEDED),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, current_daily_loss=51.0), BASE_PHASE0B_CONFIG, DAILY_LOSS_EXCEEDED),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, fee_assumption_present=False), BASE_PHASE0B_CONFIG, MISSING_FEE_ASSUMPTION),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, liquidity_assumption_present=False), BASE_PHASE0B_CONFIG, MISSING_LIQUIDITY_ASSUMPTION),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, provenance=""), BASE_PHASE0B_CONFIG, MISSING_PROVENANCE),
        (_copy_with(BASE_OPPORTUNITY_CANDIDATE, source_id=""), BASE_PHASE0B_CONFIG, MISSING_SOURCE_ID),
        (BASE_OPPORTUNITY_CANDIDATE, _copy_with(BASE_PHASE0B_CONFIG, require_operator_approval=False), OPERATOR_APPROVAL_NOT_REQUIRED),
        (BASE_OPPORTUNITY_CANDIDATE, _copy_with(BASE_PHASE0B_CONFIG, live_trading_enabled=True), LIVE_TRADING_ENABLED_PHASE0B),
        (BASE_OPPORTUNITY_CANDIDATE, _copy_with(BASE_PHASE0B_CONFIG, autonomous_trading_enabled=True), AUTONOMOUS_TRADING_ENABLED_PHASE0B),
    ]
    for candidate, config, expected in cases:
        decision = _screen_candidate_static(config, candidate)
        _assert_rejected_for(decision, expected)


def test_multi_breach_matrix() -> None:
    d1 = _screen_candidate_static(
        BASE_PHASE0B_CONFIG,
        _copy_with(BASE_OPPORTUNITY_CANDIDATE, estimated_edge_bps=0.0, confidence_score=0.10),
    )
    assert {EDGE_BELOW_MINIMUM, CONFIDENCE_BELOW_MINIMUM} <= set(d1["rejection_reasons"])

    d2 = _screen_candidate_static(
        _copy_with(BASE_PHASE0B_CONFIG, live_trading_enabled=True, autonomous_trading_enabled=True),
        BASE_OPPORTUNITY_CANDIDATE,
    )
    assert {LIVE_TRADING_ENABLED_PHASE0B, AUTONOMOUS_TRADING_ENABLED_PHASE0B} <= set(d2["rejection_reasons"])

    d3 = _screen_candidate_static(
        BASE_PHASE0B_CONFIG,
        _copy_with(BASE_OPPORTUNITY_CANDIDATE, provenance="", source_id=""),
    )
    assert {MISSING_PROVENANCE, MISSING_SOURCE_ID} <= set(d3["rejection_reasons"])

    d4 = _screen_candidate_static(
        BASE_PHASE0B_CONFIG,
        _copy_with(BASE_OPPORTUNITY_CANDIDATE, current_global_exposure=300.0, current_daily_loss=80.0),
    )
    assert {GLOBAL_EXPOSURE_EXCEEDED, DAILY_LOSS_EXCEEDED} <= set(d4["rejection_reasons"])


def test_accepted_decision_shape() -> None:
    decision = _screen_candidate_static(BASE_PHASE0B_CONFIG, BASE_OPPORTUNITY_CANDIDATE)
    assert decision["accepted"] is True
    assert decision["proposal_allowed"] is True
    assert decision["execution_allowed"] is False
    assert decision["rejection_reasons"] == []
    assert decision["fail_closed_reason"] in (None, "")
    assert decision["thresholds_evaluated"]
    assert decision["observed_values"]


def test_rejected_decision_shape() -> None:
    decision = _screen_candidate_static(
        BASE_PHASE0B_CONFIG,
        _copy_with(BASE_OPPORTUNITY_CANDIDATE, estimated_edge_bps=0.0),
    )
    assert decision["accepted"] is False
    assert decision["proposal_allowed"] is False
    assert decision["execution_allowed"] is False
    assert decision["rejection_reasons"]
    assert decision["fail_closed_reason"]
    assert decision["thresholds_evaluated"]
    assert decision["observed_values"]


def test_doc_alignment_taxonomy_concepts_present_in_r12() -> None:
    text = R12_PATH.read_text(encoding="utf-8")
    concept_terms = {
        EDGE_BELOW_MINIMUM: "edge below `min_edge_bps`",
        FEE_ADJUSTED_EDGE_BELOW_MINIMUM: "fee-adjusted edge below `min_fee_adjusted_edge_bps`",
        SPREAD_BELOW_MINIMUM: "spread below `min_spread_bps`",
        CONFIDENCE_BELOW_MINIMUM: "confidence below `min_confidence_score`",
        SEMANTIC_MATCH_BELOW_MINIMUM: "semantic match below `min_semantic_match_score`",
        LIQUIDITY_BELOW_MINIMUM: "liquidity below `min_liquidity_score`",
        DATA_QUALITY_BELOW_MINIMUM: "data quality below `min_data_quality_score`",
        MARKET_NOT_ALLOWED: "market or platform not in allowlist",
        MARKET_BLOCKED: "market or platform present in blocklist",
        PLATFORM_NOT_ALLOWED: "market or platform not in allowlist",
        PLATFORM_BLOCKED: "market or platform present in blocklist",
        PER_MARKET_EXPOSURE_EXCEEDED: "per-market or global exposure cap exceeded",
        GLOBAL_EXPOSURE_EXCEEDED: "per-market or global exposure cap exceeded",
        DAILY_LOSS_EXCEEDED: "daily loss cap exceeded",
        MISSING_FEE_ASSUMPTION: "missing fee assumptions",
        MISSING_LIQUIDITY_ASSUMPTION: "missing liquidity assumptions",
        MISSING_PROVENANCE: "missing `provenance` or missing `source_id`",
        MISSING_SOURCE_ID: "missing `provenance` or missing `source_id`",
        OPERATOR_APPROVAL_NOT_REQUIRED: "missing operator approval requirement",
        LIVE_TRADING_ENABLED_PHASE0B: "`live_trading_enabled` or `autonomous_trading_enabled` set true in Phase 0B",
        AUTONOMOUS_TRADING_ENABLED_PHASE0B: "`live_trading_enabled` or `autonomous_trading_enabled` set true in Phase 0B",
    }
    missing = [reason for reason, term in concept_terms.items() if term not in text]
    assert not missing, f"R12 concept terms missing for reasons: {missing}"


def test_canonical_id_guard_no_legacy_literal_in_test_or_r12() -> None:
    literal = LEGACY_ID_FIELD
    test_text = Path(__file__).read_text(encoding="utf-8")
    doc_text = R12_PATH.read_text(encoding="utf-8")
    assert literal not in test_text
    assert literal not in doc_text
