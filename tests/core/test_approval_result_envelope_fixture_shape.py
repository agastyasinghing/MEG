from __future__ import annotations

from copy import deepcopy
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
R10_PATH = REPO_ROOT / "docs/phase0b/0B-R10_CROSS_PLATFORM_OPPORTUNITY_DETECTOR_CONTRACT.md"
R12_PATH = REPO_ROOT / "docs/phase0b/0B-R12_THRESHOLD_RISK_GATE_CONFIG_SPEC.md"
R16_PENDING_PATH = REPO_ROOT / "tests/core/test_proposal_envelope_fixture_shape.py"
LEGACY_ID_FIELD = "market" + "_id"

MISSING_ENVELOPE_ID = "MISSING_ENVELOPE_ID"
MISSING_PROPOSAL_ID = "MISSING_PROPOSAL_ID"
MISSING_OPPORTUNITY_ID = "MISSING_OPPORTUNITY_ID"
MISSING_CONFIG_ID = "MISSING_CONFIG_ID"
MISSING_SOURCE_ID = "MISSING_SOURCE_ID"
MISSING_PROVENANCE = "MISSING_PROVENANCE"
MISSING_PRIOR_PENDING_ENVELOPE_REF = "MISSING_PRIOR_PENDING_ENVELOPE_REF"
MISSING_AUDIT_REFERENCE = "MISSING_AUDIT_REFERENCE"
MISSING_REVIEWER_METADATA = "MISSING_REVIEWER_METADATA"
MISSING_OPERATOR_APPROVAL = "MISSING_OPERATOR_APPROVAL"
OPERATOR_APPROVAL_NOT_REQUIRED = "OPERATOR_APPROVAL_NOT_REQUIRED"
INVALID_PROPOSAL_STATUS = "INVALID_PROPOSAL_STATUS"
INVALID_APPROVAL_STATUS = "INVALID_APPROVAL_STATUS"
MISSING_APPROVED_BY = "MISSING_APPROVED_BY"
MISSING_APPROVED_AT = "MISSING_APPROVED_AT"
APPROVED_RESULT_HAS_REJECTION_METADATA = "APPROVED_RESULT_HAS_REJECTION_METADATA"
REJECTED_RESULT_HAS_APPROVAL_METADATA = "REJECTED_RESULT_HAS_APPROVAL_METADATA"
MISSING_REJECTED_BY = "MISSING_REJECTED_BY"
MISSING_REJECTED_AT = "MISSING_REJECTED_AT"
MISSING_DECISION_REASON = "MISSING_DECISION_REASON"
EXECUTION_ALLOWED_PHASE0B = "EXECUTION_ALLOWED_PHASE0B"
ORDER_AUTHORITY_GRANTED_PHASE0B = "ORDER_AUTHORITY_GRANTED_PHASE0B"
LIVE_TRADING_ENABLED_PHASE0B = "LIVE_TRADING_ENABLED_PHASE0B"
AUTONOMOUS_TRADING_ENABLED_PHASE0B = "AUTONOMOUS_TRADING_ENABLED_PHASE0B"
MISSING_PAYLOAD = "MISSING_PAYLOAD"
ORDER_PAYLOAD_PRESENT_PHASE0B = "ORDER_PAYLOAD_PRESENT_PHASE0B"
MISSING_AUDIT_LINEAGE = "MISSING_AUDIT_LINEAGE"

ORDER_LIKE_KEYS = {
    "order",
    "order_payload",
    "signed_order",
    "order_router_request",
    "execution_request",
    "place_order",
}

_ALLOWED_PROPOSAL_STATUSES = {"operator_approved", "rejected_by_operator", "expired", "cancelled"}
_ALLOWED_APPROVAL_STATUSES = {"approved", "rejected", "expired", "cancelled", "pending"}

_BASE_ENVELOPE = {
    "envelope_id": "env-r17-001",
    "proposal_id": "proposal-r16-001",
    "opportunity_id": "opp-r15-accepted-001",
    "candidate_id": "cand-r10-001",
    "config_id": "cfg-phase0b-r15",
    "source_id": "phase0b-r17-static-approval-result",
    "provenance": "fixture://phase0b/r17/approval-result-envelope",
    "created_at": "2026-01-02T00:00:00Z",
    "decision_at": "2026-01-02T00:02:00Z",
    "proposal_schema_version": "v0b-envelope-1",
    "detector_schema_version": "v0b-detector-1",
    "screening_decision_ref": "decision://phase0b/r15/opp-r15-accepted-001",
    "prior_pending_envelope_ref": "envelope://phase0b/r16/pending/proposal-r16-001",
    "audit_reference": "audit://phase0b/r17/proposal-r16-001",
    "reviewer_metadata": {"queue": "telegram_operator_queue", "review_scope": "phase0b_preflight"},
    "payload": {
        "candidate_ref": "cand-r10-001",
        "proposal_ref": "proposal-r16-001",
        "source_market_ref": "market-ref-alpha",
        "summary": "operator terminal decision fixture",
    },
    "proposal_allowed": False,
    "execution_allowed": False,
    "order_authority": False,
    "live_trading_enabled": False,
    "autonomous_trading_enabled": False,
}

APPROVED_RESULT_ENVELOPE = {
    **_BASE_ENVELOPE,
    "envelope_id": "env-r17-approved-001",
    "operator_approval": {
        "approval_required": True,
        "approval_status": "approved",
        "approved_by": "operator-alpha",
        "approved_at": "2026-01-02T00:02:00Z",
        "rejected_by": None,
        "rejected_at": None,
        "decision_reason": "manual approval for Phase 0B proposal persistence",
    },
    "proposal_status": "operator_approved",
    "proposal_allowed": True,
}

REJECTED_RESULT_ENVELOPE = {
    **_BASE_ENVELOPE,
    "envelope_id": "env-r17-rejected-001",
    "operator_approval": {
        "approval_required": True,
        "approval_status": "rejected",
        "approved_by": None,
        "approved_at": None,
        "rejected_by": "operator-beta",
        "rejected_at": "2026-01-02T00:03:00Z",
        "decision_reason": "insufficient confidence for operator acceptance",
    },
    "proposal_status": "rejected_by_operator",
}

EXPIRED_RESULT_ENVELOPE = {
    **_BASE_ENVELOPE,
    "envelope_id": "env-r17-expired-001",
    "operator_approval": {
        "approval_required": True,
        "approval_status": "expired",
        "approved_by": None,
        "approved_at": None,
        "rejected_by": None,
        "rejected_at": None,
        "decision_reason": "approval window expired",
    },
    "proposal_status": "expired",
}

CANCELLED_RESULT_ENVELOPE = {
    **_BASE_ENVELOPE,
    "envelope_id": "env-r17-cancelled-001",
    "operator_approval": {
        "approval_required": True,
        "approval_status": "cancelled",
        "approved_by": None,
        "approved_at": None,
        "rejected_by": None,
        "rejected_at": None,
        "decision_reason": "proposal cancelled by operator workflow",
    },
    "proposal_status": "cancelled",
}


def _copy_with(obj: dict, **updates) -> dict:
    out = dict(obj)
    out.update(updates)
    return out


def _deep_copy_with(obj: dict, **updates) -> dict:
    out = deepcopy(obj)
    out.update(updates)
    return out


def _validate_approval_result_envelope_shape(envelope: dict) -> list[str]:
    reasons: list[str] = []
    req = {
        "envelope_id": MISSING_ENVELOPE_ID,
        "proposal_id": MISSING_PROPOSAL_ID,
        "opportunity_id": MISSING_OPPORTUNITY_ID,
        "config_id": MISSING_CONFIG_ID,
        "source_id": MISSING_SOURCE_ID,
        "provenance": MISSING_PROVENANCE,
        "prior_pending_envelope_ref": MISSING_PRIOR_PENDING_ENVELOPE_REF,
        "audit_reference": MISSING_AUDIT_REFERENCE,
    }
    for field, reason in req.items():
        if not str(envelope.get(field, "")).strip():
            reasons.append(reason)

    reviewer_metadata = envelope.get("reviewer_metadata")
    if not isinstance(reviewer_metadata, dict) or not reviewer_metadata:
        reasons.append(MISSING_REVIEWER_METADATA)

    operator_approval = envelope.get("operator_approval")
    if not isinstance(operator_approval, dict):
        reasons.append(MISSING_OPERATOR_APPROVAL)
        return reasons

    if operator_approval.get("approval_required") is not True:
        reasons.append(OPERATOR_APPROVAL_NOT_REQUIRED)

    proposal_status = envelope.get("proposal_status")
    if proposal_status not in _ALLOWED_PROPOSAL_STATUSES:
        reasons.append(INVALID_PROPOSAL_STATUS)

    approval_status = operator_approval.get("approval_status")
    if approval_status not in _ALLOWED_APPROVAL_STATUSES:
        reasons.append(INVALID_APPROVAL_STATUS)

    decision_reason = str(operator_approval.get("decision_reason") or "").strip()
    if not decision_reason:
        reasons.append(MISSING_DECISION_REASON)

    if proposal_status == "operator_approved":
        if approval_status != "approved":
            reasons.append(INVALID_APPROVAL_STATUS)
        if not str(operator_approval.get("approved_by") or "").strip():
            reasons.append(MISSING_APPROVED_BY)
        if not str(operator_approval.get("approved_at") or "").strip():
            reasons.append(MISSING_APPROVED_AT)
        if operator_approval.get("rejected_by") is not None or operator_approval.get("rejected_at") is not None:
            reasons.append(APPROVED_RESULT_HAS_REJECTION_METADATA)

    if proposal_status == "rejected_by_operator":
        if approval_status != "rejected":
            reasons.append(INVALID_APPROVAL_STATUS)
        if operator_approval.get("approved_by") is not None or operator_approval.get("approved_at") is not None:
            reasons.append(REJECTED_RESULT_HAS_APPROVAL_METADATA)
        if not str(operator_approval.get("rejected_by") or "").strip():
            reasons.append(MISSING_REJECTED_BY)
        if not str(operator_approval.get("rejected_at") or "").strip():
            reasons.append(MISSING_REJECTED_AT)

    if proposal_status in {"expired", "cancelled"} and approval_status == "approved":
        reasons.append(INVALID_APPROVAL_STATUS)

    if envelope.get("execution_allowed") is not False:
        reasons.append(EXECUTION_ALLOWED_PHASE0B)
    if envelope.get("order_authority") is not False:
        reasons.append(ORDER_AUTHORITY_GRANTED_PHASE0B)
    if envelope.get("live_trading_enabled") is not False:
        reasons.append(LIVE_TRADING_ENABLED_PHASE0B)
    if envelope.get("autonomous_trading_enabled") is not False:
        reasons.append(AUTONOMOUS_TRADING_ENABLED_PHASE0B)

    payload = envelope.get("payload")
    if not isinstance(payload, dict) or not payload:
        reasons.append(MISSING_PAYLOAD)
    else:
        if any(key in payload for key in ORDER_LIKE_KEYS):
            reasons.append(ORDER_PAYLOAD_PRESENT_PHASE0B)

    if not str(envelope.get("prior_pending_envelope_ref", "")).strip() or not str(
        envelope.get("screening_decision_ref", "")
    ).strip():
        reasons.append(MISSING_AUDIT_LINEAGE)

    return reasons


def _assert_invalid_for(envelope: dict, reason: str) -> None:
    assert reason in _validate_approval_result_envelope_shape(envelope)


def test_terminal_result_envelopes_pass_shape_validation() -> None:
    for envelope in [
        APPROVED_RESULT_ENVELOPE,
        REJECTED_RESULT_ENVELOPE,
        EXPIRED_RESULT_ENVELOPE,
        CANCELLED_RESULT_ENVELOPE,
    ]:
        assert _validate_approval_result_envelope_shape(envelope) == []


def test_terminal_result_posture_guards() -> None:
    assert APPROVED_RESULT_ENVELOPE["execution_allowed"] is False
    assert APPROVED_RESULT_ENVELOPE["order_authority"] is False
    assert REJECTED_RESULT_ENVELOPE["proposal_allowed"] is False
    assert REJECTED_RESULT_ENVELOPE["execution_allowed"] is False


def test_terminal_result_lineage_and_decision_reason_presence() -> None:
    for envelope in [
        APPROVED_RESULT_ENVELOPE,
        REJECTED_RESULT_ENVELOPE,
        EXPIRED_RESULT_ENVELOPE,
        CANCELLED_RESULT_ENVELOPE,
    ]:
        assert str(envelope["audit_reference"]).strip()
        assert str(envelope["prior_pending_envelope_ref"]).strip()
        assert str(envelope["operator_approval"]["decision_reason"]).strip()


def test_terminal_results_payload_contains_no_order_keys() -> None:
    for envelope in [
        APPROVED_RESULT_ENVELOPE,
        REJECTED_RESULT_ENVELOPE,
        EXPIRED_RESULT_ENVELOPE,
        CANCELLED_RESULT_ENVELOPE,
    ]:
        assert not (ORDER_LIKE_KEYS & set(envelope["payload"]))


def test_invalid_terminal_result_variants() -> None:
    _assert_invalid_for(
        _deep_copy_with(
            APPROVED_RESULT_ENVELOPE,
            operator_approval=_copy_with(APPROVED_RESULT_ENVELOPE["operator_approval"], approved_by=None),
        ),
        MISSING_APPROVED_BY,
    )
    _assert_invalid_for(
        _deep_copy_with(
            APPROVED_RESULT_ENVELOPE,
            operator_approval=_copy_with(APPROVED_RESULT_ENVELOPE["operator_approval"], approved_at=None),
        ),
        MISSING_APPROVED_AT,
    )
    _assert_invalid_for(
        _deep_copy_with(
            APPROVED_RESULT_ENVELOPE,
            operator_approval=_copy_with(APPROVED_RESULT_ENVELOPE["operator_approval"], rejected_by="operator-zeta"),
        ),
        APPROVED_RESULT_HAS_REJECTION_METADATA,
    )

    _assert_invalid_for(
        _deep_copy_with(
            REJECTED_RESULT_ENVELOPE,
            operator_approval=_copy_with(REJECTED_RESULT_ENVELOPE["operator_approval"], rejected_by=None),
        ),
        MISSING_REJECTED_BY,
    )
    _assert_invalid_for(
        _deep_copy_with(
            REJECTED_RESULT_ENVELOPE,
            operator_approval=_copy_with(REJECTED_RESULT_ENVELOPE["operator_approval"], rejected_at=None),
        ),
        MISSING_REJECTED_AT,
    )
    _assert_invalid_for(
        _deep_copy_with(
            REJECTED_RESULT_ENVELOPE,
            operator_approval=_copy_with(REJECTED_RESULT_ENVELOPE["operator_approval"], approved_by="operator-zeta"),
        ),
        REJECTED_RESULT_HAS_APPROVAL_METADATA,
    )

    _assert_invalid_for(_copy_with(APPROVED_RESULT_ENVELOPE, prior_pending_envelope_ref=""), MISSING_PRIOR_PENDING_ENVELOPE_REF)
    _assert_invalid_for(_copy_with(APPROVED_RESULT_ENVELOPE, audit_reference=""), MISSING_AUDIT_REFERENCE)
    _assert_invalid_for(
        _deep_copy_with(
            APPROVED_RESULT_ENVELOPE,
            operator_approval=_copy_with(APPROVED_RESULT_ENVELOPE["operator_approval"], decision_reason=""),
        ),
        MISSING_DECISION_REASON,
    )
    _assert_invalid_for(_copy_with(APPROVED_RESULT_ENVELOPE, execution_allowed=True), EXECUTION_ALLOWED_PHASE0B)
    _assert_invalid_for(_copy_with(APPROVED_RESULT_ENVELOPE, order_authority=True), ORDER_AUTHORITY_GRANTED_PHASE0B)
    _assert_invalid_for(_copy_with(APPROVED_RESULT_ENVELOPE, live_trading_enabled=True), LIVE_TRADING_ENABLED_PHASE0B)
    _assert_invalid_for(
        _copy_with(APPROVED_RESULT_ENVELOPE, autonomous_trading_enabled=True), AUTONOMOUS_TRADING_ENABLED_PHASE0B
    )
    _assert_invalid_for(
        _deep_copy_with(APPROVED_RESULT_ENVELOPE, payload=_copy_with(APPROVED_RESULT_ENVELOPE["payload"], order_payload={})),
        ORDER_PAYLOAD_PRESENT_PHASE0B,
    )
    _assert_invalid_for(_copy_with(APPROVED_RESULT_ENVELOPE, proposal_status="pending_operator_approval"), INVALID_PROPOSAL_STATUS)
    _assert_invalid_for(
        _deep_copy_with(
            APPROVED_RESULT_ENVELOPE,
            operator_approval=_copy_with(APPROVED_RESULT_ENVELOPE["operator_approval"], approval_status="pending"),
        ),
        INVALID_APPROVAL_STATUS,
    )


def test_doc_and_prior_test_alignment_contract_guards() -> None:
    pending_text = R16_PENDING_PATH.read_text(encoding="utf-8")
    assert "pending_operator_approval" in pending_text
    assert "operator_approved" in pending_text
    assert "EXECUTION_ALLOWED_PHASE0B" in pending_text
    assert "execution_allowed" in pending_text

    r10_text = R10_PATH.read_text(encoding="utf-8")
    assert "detector output is **not** approval" in r10_text
    assert "detector output cannot place orders" in r10_text

    r12_text = R12_PATH.read_text(encoding="utf-8")
    assert "execution_allowed` (must be `false` in Phase 0B)" in r12_text


def test_new_file_contains_no_literal_legacy_identifier_token() -> None:
    text = Path(__file__).read_text(encoding="utf-8")
    assert LEGACY_ID_FIELD not in text
    assert LEGACY_ID_FIELD == "market" + "_id"
