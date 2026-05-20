from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROPOSAL_FIXTURE_PATH = REPO_ROOT / "tests/core/test_proposal_envelope_fixture_shape.py"
APPROVAL_FIXTURE_PATH = REPO_ROOT / "tests/core/test_approval_result_envelope_fixture_shape.py"
R10_PATH = REPO_ROOT / "docs/phase0b/0B-R10_CROSS_PLATFORM_OPPORTUNITY_DETECTOR_CONTRACT.md"
R12_PATH = REPO_ROOT / "docs/phase0b/0B-R12_THRESHOLD_RISK_GATE_CONFIG_SPEC.md"

PENDING_OPERATOR_APPROVAL = "pending_operator_approval"
OPERATOR_APPROVED = "operator_approved"
REJECTED_BY_OPERATOR = "rejected_by_operator"
EXPIRED = "expired"
CANCELLED = "cancelled"
EXECUTED = "executed"
AUTONOMOUS_APPROVED = "autonomous_approved"

INVALID_FROM_STATUS = "INVALID_FROM_STATUS"
INVALID_TO_STATUS = "INVALID_TO_STATUS"
TRANSITION_NOT_ALLOWED_PHASE0B = "TRANSITION_NOT_ALLOWED_PHASE0B"
EXECUTION_TRANSITION_BLOCKED_PHASE0B = "EXECUTION_TRANSITION_BLOCKED_PHASE0B"
AUTONOMY_TRANSITION_BLOCKED_PHASE0B = "AUTONOMY_TRANSITION_BLOCKED_PHASE0B"
TERMINAL_STATE_REOPEN_BLOCKED = "TERMINAL_STATE_REOPEN_BLOCKED"
MISSING_AUDIT_REFERENCE = "MISSING_AUDIT_REFERENCE"
MISSING_PRIOR_PENDING_ENVELOPE_REF = "MISSING_PRIOR_PENDING_ENVELOPE_REF"
MISSING_DECISION_ACTOR = "MISSING_DECISION_ACTOR"
MISSING_DECISION_TIMESTAMP = "MISSING_DECISION_TIMESTAMP"
ORDER_AUTHORITY_GRANTED_PHASE0B = "ORDER_AUTHORITY_GRANTED_PHASE0B"
LIVE_TRADING_ENABLED_PHASE0B = "LIVE_TRADING_ENABLED_PHASE0B"
AUTONOMOUS_TRADING_ENABLED_PHASE0B = "AUTONOMOUS_TRADING_ENABLED_PHASE0B"

ALL_STATUSES = {
    PENDING_OPERATOR_APPROVAL,
    OPERATOR_APPROVED,
    REJECTED_BY_OPERATOR,
    EXPIRED,
    CANCELLED,
    EXECUTED,
    AUTONOMOUS_APPROVED,
}

ALLOWED_TRANSITIONS = {
    (PENDING_OPERATOR_APPROVAL, OPERATOR_APPROVED),
    (PENDING_OPERATOR_APPROVAL, REJECTED_BY_OPERATOR),
    (PENDING_OPERATOR_APPROVAL, EXPIRED),
    (PENDING_OPERATOR_APPROVAL, CANCELLED),
    (REJECTED_BY_OPERATOR, REJECTED_BY_OPERATOR),
    (EXPIRED, EXPIRED),
    (CANCELLED, CANCELLED),
}

TERMINAL_STATES = {REJECTED_BY_OPERATOR, EXPIRED, CANCELLED}

PENDING_ENVELOPE = {
    "envelope_id": "env-r18-pending-001",
    "proposal_id": "proposal-r18-001",
    "proposal_status": PENDING_OPERATOR_APPROVAL,
    "audit_reference": "audit://phase0b/r18/proposal-r18-001",
    "prior_pending_envelope_ref": "envelope://phase0b/r18/pending/proposal-r18-001",
    "proposal_allowed": True,
    "execution_allowed": False,
    "order_authority": False,
    "live_trading_enabled": False,
    "autonomous_trading_enabled": False,
}

VALID_OPERATOR_DECISION_METADATA = {
    "decision_actor": "operator-r18",
    "decision_timestamp": "2026-01-03T00:00:00Z",
    "decision_reason": "phase0b static lifecycle transition validation",
    "audit_reference": "audit://phase0b/r18/proposal-r18-001",
    "prior_pending_envelope_ref": "envelope://phase0b/r18/pending/proposal-r18-001",
}


def _copy_with(obj: dict, **updates) -> dict:
    out = dict(obj)
    out.update(updates)
    return out


def _transition_decision_static(from_envelope: dict, to_status: str, metadata: dict) -> dict:
    from_status = str(from_envelope.get("proposal_status", "")).strip()
    rejection_reasons: list[str] = []

    if from_status not in ALL_STATUSES:
        rejection_reasons.append(INVALID_FROM_STATUS)
    if to_status not in ALL_STATUSES:
        rejection_reasons.append(INVALID_TO_STATUS)

    if not str(metadata.get("audit_reference", "")).strip():
        rejection_reasons.append(MISSING_AUDIT_REFERENCE)
    if not str(metadata.get("prior_pending_envelope_ref", "")).strip():
        rejection_reasons.append(MISSING_PRIOR_PENDING_ENVELOPE_REF)
    if not str(metadata.get("decision_actor", "")).strip():
        rejection_reasons.append(MISSING_DECISION_ACTOR)
    if not str(metadata.get("decision_timestamp", "")).strip():
        rejection_reasons.append(MISSING_DECISION_TIMESTAMP)

    if from_envelope.get("order_authority") is not False:
        rejection_reasons.append(ORDER_AUTHORITY_GRANTED_PHASE0B)
    if from_envelope.get("live_trading_enabled") is not False:
        rejection_reasons.append(LIVE_TRADING_ENABLED_PHASE0B)
    if from_envelope.get("autonomous_trading_enabled") is not False:
        rejection_reasons.append(AUTONOMOUS_TRADING_ENABLED_PHASE0B)
    if from_envelope.get("execution_allowed") is not False:
        rejection_reasons.append(EXECUTION_TRANSITION_BLOCKED_PHASE0B)

    if to_status == EXECUTED:
        rejection_reasons.append(EXECUTION_TRANSITION_BLOCKED_PHASE0B)
    if to_status == AUTONOMOUS_APPROVED:
        rejection_reasons.append(AUTONOMY_TRANSITION_BLOCKED_PHASE0B)

    if from_status in TERMINAL_STATES and to_status == OPERATOR_APPROVED:
        rejection_reasons.append(TERMINAL_STATE_REOPEN_BLOCKED)

    if (from_status, to_status) not in ALLOWED_TRANSITIONS and to_status not in {EXECUTED, AUTONOMOUS_APPROVED}:
        rejection_reasons.append(TRANSITION_NOT_ALLOWED_PHASE0B)

    decision = {
        "from_status": from_status,
        "to_status": to_status,
        "transition_allowed": len(rejection_reasons) == 0,
        "rejection_reasons": sorted(set(rejection_reasons)),
        "audit_reference": metadata.get("audit_reference"),
        "prior_pending_envelope_ref": metadata.get("prior_pending_envelope_ref"),
        "decision_actor": metadata.get("decision_actor"),
        "decision_timestamp": metadata.get("decision_timestamp"),
        "execution_allowed": False,
        "order_authority": False,
        "live_trading_enabled": False,
        "autonomous_trading_enabled": False,
    }
    return decision


def _assert_transition_rejected(decision: dict, reason: str) -> None:
    assert decision["transition_allowed"] is False
    assert reason in decision["rejection_reasons"]


def _read_text(path: Path) -> str:
    assert path.exists(), f"Missing required path: {path}"
    return path.read_text(encoding="utf-8")


def test_allowed_pending_transitions_are_decision_record_only() -> None:
    for to_status in [OPERATOR_APPROVED, REJECTED_BY_OPERATOR, EXPIRED, CANCELLED]:
        decision = _transition_decision_static(PENDING_ENVELOPE, to_status, VALID_OPERATOR_DECISION_METADATA)
        assert decision["transition_allowed"] is True
        assert decision["from_status"] == PENDING_OPERATOR_APPROVAL
        assert decision["to_status"] == to_status
        assert decision["rejection_reasons"] == []
        assert decision["execution_allowed"] is False
        assert decision["order_authority"] is False
        assert decision["live_trading_enabled"] is False
        assert decision["autonomous_trading_enabled"] is False


def test_blocked_execution_and_autonomy_transitions_in_phase0b() -> None:
    pending_executed = _transition_decision_static(PENDING_ENVELOPE, EXECUTED, VALID_OPERATOR_DECISION_METADATA)
    _assert_transition_rejected(pending_executed, EXECUTION_TRANSITION_BLOCKED_PHASE0B)

    pending_autonomy = _transition_decision_static(PENDING_ENVELOPE, AUTONOMOUS_APPROVED, VALID_OPERATOR_DECISION_METADATA)
    _assert_transition_rejected(pending_autonomy, AUTONOMY_TRANSITION_BLOCKED_PHASE0B)

    approved_from = _copy_with(PENDING_ENVELOPE, proposal_status=OPERATOR_APPROVED)
    approved_to_executed = _transition_decision_static(approved_from, EXECUTED, VALID_OPERATOR_DECISION_METADATA)
    _assert_transition_rejected(approved_to_executed, EXECUTION_TRANSITION_BLOCKED_PHASE0B)

    approved_to_autonomy = _transition_decision_static(approved_from, AUTONOMOUS_APPROVED, VALID_OPERATOR_DECISION_METADATA)
    _assert_transition_rejected(approved_to_autonomy, AUTONOMY_TRANSITION_BLOCKED_PHASE0B)

    for terminal_status in [REJECTED_BY_OPERATOR, EXPIRED, CANCELLED]:
        terminal_from = _copy_with(PENDING_ENVELOPE, proposal_status=terminal_status)
        terminal_to_executed = _transition_decision_static(terminal_from, EXECUTED, VALID_OPERATOR_DECISION_METADATA)
        _assert_transition_rejected(terminal_to_executed, EXECUTION_TRANSITION_BLOCKED_PHASE0B)
        terminal_to_autonomy = _transition_decision_static(
            terminal_from,
            AUTONOMOUS_APPROVED,
            VALID_OPERATOR_DECISION_METADATA,
        )
        _assert_transition_rejected(terminal_to_autonomy, AUTONOMY_TRANSITION_BLOCKED_PHASE0B)


def test_terminal_reopen_to_operator_approved_is_blocked() -> None:
    for terminal_status in [REJECTED_BY_OPERATOR, EXPIRED, CANCELLED]:
        decision = _transition_decision_static(
            _copy_with(PENDING_ENVELOPE, proposal_status=terminal_status),
            OPERATOR_APPROVED,
            VALID_OPERATOR_DECISION_METADATA,
        )
        _assert_transition_rejected(decision, TERMINAL_STATE_REOPEN_BLOCKED)


def test_missing_lineage_and_decision_metadata_rejected() -> None:
    _assert_transition_rejected(
        _transition_decision_static(
            PENDING_ENVELOPE,
            OPERATOR_APPROVED,
            _copy_with(VALID_OPERATOR_DECISION_METADATA, audit_reference=""),
        ),
        MISSING_AUDIT_REFERENCE,
    )
    _assert_transition_rejected(
        _transition_decision_static(
            PENDING_ENVELOPE,
            OPERATOR_APPROVED,
            _copy_with(VALID_OPERATOR_DECISION_METADATA, prior_pending_envelope_ref=""),
        ),
        MISSING_PRIOR_PENDING_ENVELOPE_REF,
    )
    _assert_transition_rejected(
        _transition_decision_static(
            PENDING_ENVELOPE,
            OPERATOR_APPROVED,
            _copy_with(VALID_OPERATOR_DECISION_METADATA, decision_actor=""),
        ),
        MISSING_DECISION_ACTOR,
    )
    _assert_transition_rejected(
        _transition_decision_static(
            PENDING_ENVELOPE,
            OPERATOR_APPROVED,
            _copy_with(VALID_OPERATOR_DECISION_METADATA, decision_timestamp=""),
        ),
        MISSING_DECISION_TIMESTAMP,
    )


def test_authority_flag_guards_reject_non_phase0b_source_envelopes() -> None:
    _assert_transition_rejected(
        _transition_decision_static(
            _copy_with(PENDING_ENVELOPE, execution_allowed=True),
            OPERATOR_APPROVED,
            VALID_OPERATOR_DECISION_METADATA,
        ),
        EXECUTION_TRANSITION_BLOCKED_PHASE0B,
    )
    _assert_transition_rejected(
        _transition_decision_static(
            _copy_with(PENDING_ENVELOPE, order_authority=True),
            OPERATOR_APPROVED,
            VALID_OPERATOR_DECISION_METADATA,
        ),
        ORDER_AUTHORITY_GRANTED_PHASE0B,
    )
    _assert_transition_rejected(
        _transition_decision_static(
            _copy_with(PENDING_ENVELOPE, live_trading_enabled=True),
            OPERATOR_APPROVED,
            VALID_OPERATOR_DECISION_METADATA,
        ),
        LIVE_TRADING_ENABLED_PHASE0B,
    )
    _assert_transition_rejected(
        _transition_decision_static(
            _copy_with(PENDING_ENVELOPE, autonomous_trading_enabled=True),
            OPERATOR_APPROVED,
            VALID_OPERATOR_DECISION_METADATA,
        ),
        AUTONOMOUS_TRADING_ENABLED_PHASE0B,
    )


def test_doc_and_fixture_alignment_for_phase0b_boundaries() -> None:
    proposal_fixture_text = _read_text(PROPOSAL_FIXTURE_PATH)
    assert "pending_operator_approval" in proposal_fixture_text
    assert "EXECUTION_ALLOWED_PHASE0B" in proposal_fixture_text
    assert "AUTONOMOUS_TRADING_ENABLED_PHASE0B" in proposal_fixture_text

    approval_fixture_text = _read_text(APPROVAL_FIXTURE_PATH)
    for status in ["operator_approved", "rejected_by_operator", "expired", "cancelled"]:
        assert status in approval_fixture_text
    assert "execution_allowed" in approval_fixture_text
    assert "False" in approval_fixture_text

    r10_text = _read_text(R10_PATH)
    assert "detector output is **not** approval" in r10_text
    assert "detector output is **not** an order" in r10_text
    assert "detector output cannot place orders" in r10_text

    r12_text = _read_text(R12_PATH)
    assert "execution_allowed" in r12_text
    assert "must be `false` in Phase 0B" in r12_text


def test_no_literal_legacy_identifier_in_this_file() -> None:
    this_text = Path(__file__).read_text(encoding="utf-8")
    legacy_id_field = "market" + "_id"
    assert legacy_id_field not in this_text
