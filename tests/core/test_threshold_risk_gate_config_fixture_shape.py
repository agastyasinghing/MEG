from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
R12_PATH = REPO_ROOT / "docs/phase0b/0B-R12_THRESHOLD_RISK_GATE_CONFIG_SPEC.md"
LEGACY_ID_FIELD = "market" + "_id"


VALID_PHASE0B_CONFIG: dict[str, object] = {
    "config_id": "cfg-phase0b-r14-valid",
    "config_version": "v0b-fixture-1",
    "mode": "fixture",
    "source_id": "static-fixture-source",
    "provenance": "phase0b-r14-static-test-fixture",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
    "min_edge_bps": 0,
    "min_fee_adjusted_edge_bps": 0,
    "min_spread_bps": 0,
    "min_confidence_score": 0.0,
    "min_semantic_match_score": 0.0,
    "min_liquidity_score": 0.0,
    "min_data_quality_score": 0.0,
    "max_per_market_exposure": 100.0,
    "max_global_exposure": 250.0,
    "max_daily_loss": 50.0,
    "market_allowlist": ["market-alpha"],
    "market_blocklist": [],
    "platform_allowlist": ["platform-a", "platform-b"],
    "platform_blocklist": [],
    "dry_run_default": True,
    "require_operator_approval": True,
    "live_trading_enabled": False,
    "autonomous_trading_enabled": False,
    "kill_switch_enabled": True,
    "audit_log_required": True,
    "rejection_reason_required": True,
}


VALID_REJECTION_DECISION: dict[str, object] = {
    "candidate_id": "cand-001",
    "config_id": "cfg-phase0b-r14-valid",
    "accepted": False,
    "rejection_reasons": ["edge below min_edge_bps"],
    "fail_closed_reason": "threshold_not_met",
    "thresholds_evaluated": ["min_edge_bps", "min_confidence_score"],
    "observed_values": {"min_edge_bps": -1, "min_confidence_score": 0.25},
    "decision_timestamp": "2026-01-01T00:00:00Z",
    "audit_log_reference": "audit://phase0b/r14/cand-001",
    "proposal_allowed": False,
    "execution_allowed": False,
}


def _required_fields() -> set[str]:
    return {
        "config_id",
        "config_version",
        "mode",
        "source_id",
        "provenance",
        "created_at",
        "updated_at",
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
        "market_allowlist",
        "market_blocklist",
        "platform_allowlist",
        "platform_blocklist",
        "dry_run_default",
        "require_operator_approval",
        "live_trading_enabled",
        "autonomous_trading_enabled",
        "kill_switch_enabled",
        "audit_log_required",
        "rejection_reason_required",
    }


def _copy_with(config: dict, **updates) -> dict:
    updated = dict(config)
    updated.update(updates)
    return updated


def _validate_phase0b_config_shape(config: dict) -> list[str]:
    reasons: list[str] = []
    missing = sorted(field for field in _required_fields() if field not in config)
    if missing:
        reasons.append(f"missing required fields: {', '.join(missing)}")
        return reasons

    valid_modes = {"planning", "fixture", "paper", "read_only_live_blocked", "live_blocked"}
    if config["mode"] not in valid_modes:
        reasons.append("unknown mode")

    if not isinstance(config["source_id"], str) or not config["source_id"].strip():
        reasons.append("missing source_id")
    if not isinstance(config["provenance"], str) or not config["provenance"].strip():
        reasons.append("missing provenance")

    for timestamp_field in ("created_at", "updated_at"):
        value = config[timestamp_field]
        if not isinstance(value, str) or not value.strip():
            reasons.append(f"missing {timestamp_field}")

    for numeric_field in (
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
    ):
        value = config[numeric_field]
        if not isinstance(value, (int, float)):
            reasons.append(f"{numeric_field} must be numeric")
        elif value < 0:
            reasons.append(f"{numeric_field} must be non-negative")

    for list_field in ("market_allowlist", "market_blocklist", "platform_allowlist", "platform_blocklist"):
        if not isinstance(config[list_field], list):
            reasons.append(f"{list_field} must be a list")

    if config["dry_run_default"] is not True:
        reasons.append("dry_run_default must be true in phase 0b")
    if config["require_operator_approval"] is not True:
        reasons.append("require_operator_approval must be true in phase 0b")
    if config["live_trading_enabled"] is not False:
        reasons.append("live_trading_enabled must be false in phase 0b")
    if config["autonomous_trading_enabled"] is not False:
        reasons.append("autonomous_trading_enabled must be false in phase 0b")
    if config["audit_log_required"] is not True:
        reasons.append("audit_log_required must be true in phase 0b")
    if config["rejection_reason_required"] is not True:
        reasons.append("rejection_reason_required must be true in phase 0b")

    return reasons


INVALID_LIVE_TRADING_CONFIG = _copy_with(VALID_PHASE0B_CONFIG, live_trading_enabled=True)
INVALID_AUTONOMOUS_TRADING_CONFIG = _copy_with(VALID_PHASE0B_CONFIG, autonomous_trading_enabled=True)
INVALID_MISSING_REQUIRED_FIELD_CONFIG = {
    key: value for key, value in VALID_PHASE0B_CONFIG.items() if key != "min_edge_bps"
}
INVALID_NEGATIVE_EXPOSURE_CONFIG = _copy_with(
    VALID_PHASE0B_CONFIG,
    max_per_market_exposure=-1.0,
    max_global_exposure=-2.0,
    max_daily_loss=-3.0,
)
INVALID_OPERATOR_APPROVAL_DISABLED_CONFIG = _copy_with(
    VALID_PHASE0B_CONFIG,
    require_operator_approval=False,
)


def _read_r12_doc() -> str:
    assert R12_PATH.exists(), f"Required doc missing: {R12_PATH}"
    return R12_PATH.read_text(encoding="utf-8")


def test_valid_fixture_contains_all_required_fields() -> None:
    assert _required_fields() <= set(VALID_PHASE0B_CONFIG)


def test_valid_fixture_passes_shape_validation_and_phase0b_posture() -> None:
    reasons = _validate_phase0b_config_shape(VALID_PHASE0B_CONFIG)
    assert reasons == []
    assert VALID_PHASE0B_CONFIG["mode"] in {"planning", "fixture"}
    assert VALID_PHASE0B_CONFIG["dry_run_default"] is True
    assert VALID_PHASE0B_CONFIG["require_operator_approval"] is True
    assert VALID_PHASE0B_CONFIG["live_trading_enabled"] is False
    assert VALID_PHASE0B_CONFIG["autonomous_trading_enabled"] is False
    assert VALID_PHASE0B_CONFIG["audit_log_required"] is True
    assert VALID_PHASE0B_CONFIG["rejection_reason_required"] is True


def test_valid_fixture_does_not_grant_execution_authority() -> None:
    reasons = _validate_phase0b_config_shape(VALID_PHASE0B_CONFIG)
    assert "live_trading_enabled must be false in phase 0b" not in reasons
    assert "autonomous_trading_enabled must be false in phase 0b" not in reasons


def test_invalid_live_trading_enabled_true_fails_closed() -> None:
    reasons = _validate_phase0b_config_shape(INVALID_LIVE_TRADING_CONFIG)
    assert "live_trading_enabled must be false in phase 0b" in reasons


def test_invalid_autonomous_trading_enabled_true_fails_closed() -> None:
    reasons = _validate_phase0b_config_shape(INVALID_AUTONOMOUS_TRADING_CONFIG)
    assert "autonomous_trading_enabled must be false in phase 0b" in reasons


def test_invalid_operator_approval_disabled_fails_closed() -> None:
    reasons = _validate_phase0b_config_shape(INVALID_OPERATOR_APPROVAL_DISABLED_CONFIG)
    assert "require_operator_approval must be true in phase 0b" in reasons


def test_invalid_dry_run_disabled_fails_closed() -> None:
    reasons = _validate_phase0b_config_shape(_copy_with(VALID_PHASE0B_CONFIG, dry_run_default=False))
    assert "dry_run_default must be true in phase 0b" in reasons


def test_invalid_missing_required_field_fails_closed() -> None:
    reasons = _validate_phase0b_config_shape(INVALID_MISSING_REQUIRED_FIELD_CONFIG)
    assert any(reason.startswith("missing required fields:") for reason in reasons)


def test_invalid_negative_exposure_caps_fail_closed() -> None:
    reasons = _validate_phase0b_config_shape(INVALID_NEGATIVE_EXPOSURE_CONFIG)
    assert "max_per_market_exposure must be non-negative" in reasons
    assert "max_global_exposure must be non-negative" in reasons
    assert "max_daily_loss must be non-negative" in reasons


def test_invalid_missing_provenance_fails_closed() -> None:
    reasons = _validate_phase0b_config_shape(_copy_with(VALID_PHASE0B_CONFIG, provenance=""))
    assert "missing provenance" in reasons


def test_invalid_missing_source_id_fails_closed() -> None:
    reasons = _validate_phase0b_config_shape(_copy_with(VALID_PHASE0B_CONFIG, source_id=""))
    assert "missing source_id" in reasons


def test_invalid_unknown_mode_fails_closed() -> None:
    reasons = _validate_phase0b_config_shape(_copy_with(VALID_PHASE0B_CONFIG, mode="unknown_mode"))
    assert "unknown mode" in reasons


def test_rejection_decision_fixture_shape_and_fail_closed_posture() -> None:
    decision = VALID_REJECTION_DECISION
    assert ("candidate_id" in decision) or ("opportunity_id" in decision)
    assert decision["accepted"] is False
    assert decision["proposal_allowed"] is False
    assert decision["execution_allowed"] is False
    assert isinstance(decision["rejection_reasons"], list) and decision["rejection_reasons"]
    assert isinstance(decision["fail_closed_reason"], str) and decision["fail_closed_reason"]
    assert isinstance(decision["thresholds_evaluated"], list) and decision["thresholds_evaluated"]
    assert "observed_values" in decision


def test_r12_doc_mentions_all_required_fields_and_required_posture_terms() -> None:
    text = _read_r12_doc()
    missing_fields = [field for field in _required_fields() if f"`{field}`" not in text]
    assert not missing_fields, f"R12 missing required config fields: {missing_fields}"

    assert "`dry_run_default` must be `true`" in text
    assert "`require_operator_approval` must be `true`" in text
    assert "`live_trading_enabled` must be `false`" in text
    assert "`autonomous_trading_enabled` must be `false`" in text


def test_no_legacy_identifier_literal_in_new_test_or_r12_doc() -> None:
    test_text = Path(__file__).read_text(encoding="utf-8")
    r12_text = _read_r12_doc()
    assert LEGACY_ID_FIELD not in test_text
    assert LEGACY_ID_FIELD not in r12_text
