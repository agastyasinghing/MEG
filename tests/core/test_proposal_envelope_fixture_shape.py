from __future__ import annotations

from copy import deepcopy
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
R10_PATH = REPO_ROOT / "docs/phase0b/0B-R10_CROSS_PLATFORM_OPPORTUNITY_DETECTOR_CONTRACT.md"
R12_PATH = REPO_ROOT / "docs/phase0b/0B-R12_THRESHOLD_RISK_GATE_CONFIG_SPEC.md"
SCREENING_MATRIX_PATH = REPO_ROOT / "tests/core/test_threshold_risk_gate_screening_matrix.py"
LEGACY_ID_FIELD = "market" + "_id"

MISSING_ENVELOPE_ID = "MISSING_ENVELOPE_ID"
MISSING_PROPOSAL_ID = "MISSING_PROPOSAL_ID"
MISSING_OPPORTUNITY_ID = "MISSING_OPPORTUNITY_ID"
MISSING_CONFIG_ID = "MISSING_CONFIG_ID"
MISSING_SOURCE_ID = "MISSING_SOURCE_ID"
MISSING_PROVENANCE = "MISSING_PROVENANCE"
MISSING_AUDIT_REFERENCE = "MISSING_AUDIT_REFERENCE"
MISSING_REVIEWER_METADATA = "MISSING_REVIEWER_METADATA"
MISSING_OPERATOR_APPROVAL = "MISSING_OPERATOR_APPROVAL"
OPERATOR_APPROVAL_NOT_REQUIRED = "OPERATOR_APPROVAL_NOT_REQUIRED"
INVALID_APPROVAL_STATUS = "INVALID_APPROVAL_STATUS"
PREAPPROVED_WITHOUT_OPERATOR = "PREAPPROVED_WITHOUT_OPERATOR"
EXECUTION_ALLOWED_PHASE0B = "EXECUTION_ALLOWED_PHASE0B"
ORDER_AUTHORITY_GRANTED_PHASE0B = "ORDER_AUTHORITY_GRANTED_PHASE0B"
LIVE_TRADING_ENABLED_PHASE0B = "LIVE_TRADING_ENABLED_PHASE0B"
AUTONOMOUS_TRADING_ENABLED_PHASE0B = "AUTONOMOUS_TRADING_ENABLED_PHASE0B"
MISSING_PAYLOAD = "MISSING_PAYLOAD"
ORDER_PAYLOAD_PRESENT_PHASE0B = "ORDER_PAYLOAD_PRESENT_PHASE0B"
MISSING_PROPOSAL_STATUS = "MISSING_PROPOSAL_STATUS"
INVALID_PROPOSAL_STATUS = "INVALID_PROPOSAL_STATUS"
PENDING_DECISION_REASON_PRESENT = "PENDING_DECISION_REASON_PRESENT"

PHASE0B_ALLOWED_PROPOSAL_STATUSES = {
    "pending_operator_approval",
    "rejected_by_operator",
    "expired",
    "cancelled",
}

ORDER_LIKE_KEYS = {
    "order",
    "order_payload",
    "signed_order",
    "order_router_request",
    "execution_request",
    "place_order",
}

VALID_PROPOSAL_ENVELOPE: dict[str, object] = {
    "envelope_id": "env-r16-001",
    "proposal_id": "proposal-r16-001",
    "opportunity_id": "opp-r15-accepted-001",
    "candidate_id": "cand-r10-001",
    "config_id": "cfg-phase0b-r15",
    "source_id": "phase0b-r16-static-envelope-source",
    "provenance": "fixture://phase0b/r16/proposal-envelope",
    "created_at": "2026-01-01T00:00:00Z",
    "proposal_schema_version": "v0b-envelope-1",
    "detector_schema_version": "v0b-detector-1",
    "screening_decision_ref": "decision://phase0b/r15/opp-r15-accepted-001",
    "audit_reference": "audit://phase0b/r16/proposal-r16-001",
    "reviewer_metadata": {
        "review_queue": "telegram_operator_queue",
        "review_scope": "phase0b_preflight",
    },
    "operator_approval": {
        "approval_required": True,
        "approval_status": "pending",
        "approved_by": None,
        "approved_at": None,
        "rejected_by": None,
        "rejected_at": None,
        "decision_reason": None,
    },
    "payload": {
        "candidate_ref": "cand-r10-001",
        "source_market_ref": "market-ref-alpha",
        "opportunity_type": "cross_platform_price_gap",
        "estimated_edge_bps": 12.5,
        "fee_adjusted_edge_bps": 9.5,
        "confidence_score": 0.91,
    },
    "proposal_status": "pending_operator_approval",
    "proposal_allowed": True,
    "execution_allowed": False,
    "order_authority": False,
    "live_trading_enabled": False,
    "autonomous_trading_enabled": False,
}


def _copy_with(obj: dict, **updates) -> dict:
    out = dict(obj)
    out.update(updates)
    return out


def _deep_copy_with(obj: dict, **updates) -> dict:
    out = deepcopy(obj)
    out.update(updates)
    return out


def _validate_proposal_envelope_shape(envelope: dict) -> list[str]:
    reasons: list[str] = []

    required_nonempty = {
        "envelope_id": MISSING_ENVELOPE_ID,
        "proposal_id": MISSING_PROPOSAL_ID,
        "opportunity_id": MISSING_OPPORTUNITY_ID,
        "config_id": MISSING_CONFIG_ID,
        "source_id": MISSING_SOURCE_ID,
        "provenance": MISSING_PROVENANCE,
        "audit_reference": MISSING_AUDIT_REFERENCE,
    }
    for field, reason in required_nonempty.items():
        if not str(envelope.get(field, "")).strip():
            reasons.append(reason)

    reviewer_metadata = envelope.get("reviewer_metadata")
    if not isinstance(reviewer_metadata, dict) or not reviewer_metadata:
        reasons.append(MISSING_REVIEWER_METADATA)

    proposal_status = str(envelope.get("proposal_status", "")).strip()
    if not proposal_status:
        reasons.append(MISSING_PROPOSAL_STATUS)
    elif proposal_status not in PHASE0B_ALLOWED_PROPOSAL_STATUSES:
        reasons.append(INVALID_PROPOSAL_STATUS)

    operator_approval = envelope.get("operator_approval")
    if not isinstance(operator_approval, dict):
        reasons.append(MISSING_OPERATOR_APPROVAL)
    else:
        if operator_approval.get("approval_required") is not True:
            reasons.append(OPERATOR_APPROVAL_NOT_REQUIRED)
        if operator_approval.get("approval_status") != "pending":
            reasons.append(INVALID_APPROVAL_STATUS)

        is_pending_envelope = (
            proposal_status == "pending_operator_approval"
            and operator_approval.get("approval_status") == "pending"
        )
        if is_pending_envelope:
            if operator_approval.get("approved_by") is not None or operator_approval.get("approved_at") is not None:
                reasons.append(PREAPPROVED_WITHOUT_OPERATOR)
            if operator_approval.get("rejected_by") is not None or operator_approval.get("rejected_at") is not None:
                reasons.append(PREAPPROVED_WITHOUT_OPERATOR)
            decision_reason = operator_approval.get("decision_reason")
            if decision_reason not in (None, ""):
                reasons.append(PENDING_DECISION_REASON_PRESENT)

    if envelope.get("execution_allowed") is not False:
        reasons.append(EXECUTION_ALLOWED_PHASE0B)
    if envelope.get("order_authority") is not False:
        reasons.append(ORDER_AUTHORITY_GRANTED_PHASE0B)
    if envelope.get("live_trading_enabled") is not False:
        reasons.append(LIVE_TRADING_ENABLED_PHASE0B)
    if envelope.get("autonomous_trading_enabled") is not False:
        reasons.append(AUTONOMOUS_TRADING_ENABLED_PHASE0B)

    payload = envelope.get("payload")
    if payload is None:
        reasons.append(MISSING_PAYLOAD)
    elif isinstance(payload, dict) and ORDER_LIKE_KEYS & set(payload):
        reasons.append(ORDER_PAYLOAD_PRESENT_PHASE0B)

    return reasons


def _assert_invalid_for(envelope: dict, reason: str) -> None:
    reasons = _validate_proposal_envelope_shape(envelope)
    assert reason in reasons


def _read_text(path: Path) -> str:
    assert path.exists(), f"Missing required path: {path}"
    return path.read_text(encoding="utf-8")


def test_valid_proposal_envelope_fixture_passes_validation() -> None:
    assert _validate_proposal_envelope_shape(VALID_PROPOSAL_ENVELOPE) == []
    assert VALID_PROPOSAL_ENVELOPE["proposal_allowed"] is True
    assert VALID_PROPOSAL_ENVELOPE["execution_allowed"] is False
    assert VALID_PROPOSAL_ENVELOPE["order_authority"] is False
    assert VALID_PROPOSAL_ENVELOPE["live_trading_enabled"] is False
    assert VALID_PROPOSAL_ENVELOPE["autonomous_trading_enabled"] is False
    assert VALID_PROPOSAL_ENVELOPE["operator_approval"]["approval_required"] is True
    assert VALID_PROPOSAL_ENVELOPE["operator_approval"]["approval_status"] == "pending"
    assert str(VALID_PROPOSAL_ENVELOPE["audit_reference"]).strip()
    assert VALID_PROPOSAL_ENVELOPE["reviewer_metadata"]
    assert ORDER_LIKE_KEYS.isdisjoint(set(VALID_PROPOSAL_ENVELOPE["payload"]))


def test_invalid_envelope_cases_emit_expected_reasons() -> None:
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, envelope_id=""), MISSING_ENVELOPE_ID)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, proposal_id=""), MISSING_PROPOSAL_ID)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, opportunity_id=""), MISSING_OPPORTUNITY_ID)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, config_id=""), MISSING_CONFIG_ID)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, source_id=""), MISSING_SOURCE_ID)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, provenance=""), MISSING_PROVENANCE)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, audit_reference=""), MISSING_AUDIT_REFERENCE)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, reviewer_metadata={}), MISSING_REVIEWER_METADATA)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, operator_approval=None), MISSING_OPERATOR_APPROVAL)

    _assert_invalid_for(
        _deep_copy_with(
            VALID_PROPOSAL_ENVELOPE,
            operator_approval=_copy_with(VALID_PROPOSAL_ENVELOPE["operator_approval"], approval_required=False),
        ),
        OPERATOR_APPROVAL_NOT_REQUIRED,
    )
    _assert_invalid_for(
        _deep_copy_with(
            VALID_PROPOSAL_ENVELOPE,
            operator_approval=_copy_with(VALID_PROPOSAL_ENVELOPE["operator_approval"], approval_status="approved"),
        ),
        INVALID_APPROVAL_STATUS,
    )
    _assert_invalid_for(
        _deep_copy_with(
            VALID_PROPOSAL_ENVELOPE,
            operator_approval=_copy_with(VALID_PROPOSAL_ENVELOPE["operator_approval"], approved_by="operator-1"),
        ),
        PREAPPROVED_WITHOUT_OPERATOR,
    )
    _assert_invalid_for(
        _deep_copy_with(
            VALID_PROPOSAL_ENVELOPE,
            operator_approval=_copy_with(VALID_PROPOSAL_ENVELOPE["operator_approval"], rejected_by="operator-2"),
        ),
        PREAPPROVED_WITHOUT_OPERATOR,
    )
    _assert_invalid_for(
        _deep_copy_with(
            VALID_PROPOSAL_ENVELOPE,
            operator_approval=_copy_with(VALID_PROPOSAL_ENVELOPE["operator_approval"], rejected_at="2026-01-01T00:01:00Z"),
        ),
        PREAPPROVED_WITHOUT_OPERATOR,
    )
    _assert_invalid_for(
        _deep_copy_with(
            VALID_PROPOSAL_ENVELOPE,
            operator_approval=_copy_with(VALID_PROPOSAL_ENVELOPE["operator_approval"], decision_reason="premature"),
        ),
        PENDING_DECISION_REASON_PRESENT,
    )

    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, execution_allowed=True), EXECUTION_ALLOWED_PHASE0B)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, order_authority=True), ORDER_AUTHORITY_GRANTED_PHASE0B)
    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, live_trading_enabled=True), LIVE_TRADING_ENABLED_PHASE0B)
    _assert_invalid_for(
        _copy_with(VALID_PROPOSAL_ENVELOPE, autonomous_trading_enabled=True),
        AUTONOMOUS_TRADING_ENABLED_PHASE0B,
    )
    _assert_invalid_for(
        _copy_with(VALID_PROPOSAL_ENVELOPE, proposal_status="operator_approved"),
        INVALID_PROPOSAL_STATUS,
    )
    _assert_invalid_for(
        _copy_with(VALID_PROPOSAL_ENVELOPE, proposal_status="executed"),
        INVALID_PROPOSAL_STATUS,
    )
    _assert_invalid_for(
        _copy_with(VALID_PROPOSAL_ENVELOPE, proposal_status="autonomous_approved"),
        INVALID_PROPOSAL_STATUS,
    )

    _assert_invalid_for(_copy_with(VALID_PROPOSAL_ENVELOPE, payload=None), MISSING_PAYLOAD)
    _assert_invalid_for(
        _copy_with(VALID_PROPOSAL_ENVELOPE, payload=_copy_with(VALID_PROPOSAL_ENVELOPE["payload"], order_payload={})),
        ORDER_PAYLOAD_PRESENT_PHASE0B,
    )


def test_phase0b_proposal_status_allowlist() -> None:
    assert VALID_PROPOSAL_ENVELOPE["proposal_status"] in PHASE0B_ALLOWED_PROPOSAL_STATUSES
    assert "operator_approved" not in PHASE0B_ALLOWED_PROPOSAL_STATUSES
    assert "executed" not in PHASE0B_ALLOWED_PROPOSAL_STATUSES
    assert "autonomous_approved" not in PHASE0B_ALLOWED_PROPOSAL_STATUSES


def test_doc_alignment_for_detector_threshold_and_screening_boundary() -> None:
    r10_text = _read_text(R10_PATH)
    assert "detector output is **not** approval" in r10_text
    assert "detector output is **not** an order" in r10_text
    assert "detector output cannot place orders" in r10_text

    r12_text = _read_text(R12_PATH)
    assert "proposal_allowed" in r12_text
    assert "execution_allowed" in r12_text
    assert "must be `false` in Phase 0B" in r12_text

    matrix_text = _read_text(SCREENING_MATRIX_PATH)
    assert '"proposal_allowed": accepted' in matrix_text
    assert '"execution_allowed": False' in matrix_text


def test_no_literal_legacy_identifier_in_this_test_file() -> None:
    test_text = Path(__file__).read_text(encoding="utf-8")
    assert LEGACY_ID_FIELD not in test_text
