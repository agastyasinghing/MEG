"""Phase 0A-05I test-only TradeProposal envelope safety contract.

These tests only validate shared-event envelope parsing/dispatch behavior.
They do NOT grant approval and do NOT execute orders.
"""
from __future__ import annotations

from typing import Any

import pytest

from meg.core.events import RedisKeys, SUPPORTED_EVENT_SCHEMA_VERSION, TradeProposal
from tests.core.event_fixture_boundary import (
    serialize_test_event_boundary_payload,
    validate_test_event_boundary_json,
    validate_test_redis_envelope,
)

LEGACY_ID_FIELD = "market" + "_id"


def _score_payload() -> dict[str, float]:
    return {
        "lead_lag": 0.82,
        "consensus": 0.71,
        "kelly_confidence": 0.64,
        "divergence": 0.38,
        "conviction_ratio": 0.57,
        "archetype_multiplier": 1.15,
        "ladder_multiplier": 1.0,
    }


def _trade_proposal_payload() -> dict[str, Any]:
    return {
        "event_type": "trade_proposal",
        "proposal_id": "proposal-phase0a-05i-001",
        "signal_id": "sig-phase0a-05i-001",
        LEGACY_ID_FIELD: "polymarket-presidential-election-2028",
        "condition_id": "0xconditionphase0a05i",
        "token_id": "12345678901234567890",
        "market_slug": "presidential-election-winner-2028",
        "outcome": "YES",
        "size_usdc": 225.0,
        "limit_price": 0.66,
        "status": "PENDING_APPROVAL",
        "created_at_ms": 1762819210000,
        "composite_score": 0.79,
        "scores": _score_payload(),
        "saturation_score": 0.18,
        "trap_warning": False,
        "contributing_wallets": ["0x6f4c4f79e79c6d8b3c2e1234567890abcdef1234"],
        "market_price_at_signal": 0.64,
        "estimated_half_life_minutes": 14.5,
        "current_price": 0.65,
        "estimated_slippage": 0.04,
    }


def test_trade_proposal_payload_validates_from_json_boundary() -> None:
    event = validate_test_event_boundary_json(
        serialize_test_event_boundary_payload(_trade_proposal_payload())
    )

    assert isinstance(event, TradeProposal)
    assert event.event_type == "trade_proposal"


@pytest.mark.parametrize("validator", [validate_test_event_boundary_json, lambda p: validate_test_redis_envelope(RedisKeys.CHANNEL_TRADE_PROPOSALS, p)])
def test_trade_proposal_missing_schema_version_defaults_to_one(validator) -> None:
    payload = _trade_proposal_payload()
    payload.pop("schema_version", None)

    event = validator(serialize_test_event_boundary_payload(payload))

    assert isinstance(event, TradeProposal)
    assert event.schema_version == SUPPORTED_EVENT_SCHEMA_VERSION


def test_trade_proposal_unsupported_schema_version_is_rejected() -> None:
    payload = _trade_proposal_payload()
    payload["schema_version"] = SUPPORTED_EVENT_SCHEMA_VERSION + 1

    with pytest.raises(ValueError, match="Unsupported event schema_version"):
        validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))


def _signal_payload() -> dict[str, Any]:
    return {
        "event_type": "signal",
        "signal_id": "sig-phase0a-05i-redis-mismatch",
        LEGACY_ID_FIELD: "polymarket-presidential-election-2028",
        "outcome": "YES",
        "market_slug": "presidential-election-winner-2028",
        "composite_score": 0.79,
        "scores": _score_payload(),
        "recommended_size_usdc": 225.0,
        "kelly_fraction": 0.045,
        "ttl_expires_at_ms": 1762820105123,
        "status": "PENDING",
        "triggering_wallet": "0x6f4c4f79e79c6d8b3c2e1234567890abcdef1234",
    }


def _raw_whale_trade_payload() -> dict[str, Any]:
    return {
        "event_type": "raw_whale_trade",
        "wallet_address": "0x6f4c4f79e79c6d8b3c2e1234567890abcdef1234",
        LEGACY_ID_FIELD: "polymarket-presidential-election-2028",
        "outcome": "YES",
        "size_usdc": 12750.25,
        "timestamp_ms": 1762819205123,
        "tx_hash": "0x8f2a9e1c4b7d6a5f3e2d1c0b9a887766554433221100ffeeddccbbaa99887766",
        "block_number": 73123456,
        "market_price_at_trade": 0.63,
    }


def test_trade_proposal_wrong_event_type_is_rejected() -> None:
    with pytest.raises(ValueError, match="channel/event_type mismatch"):
        validate_test_redis_envelope(
            RedisKeys.CHANNEL_TRADE_PROPOSALS,
            serialize_test_event_boundary_payload(_signal_payload()),
        )


def test_trade_proposal_invalid_json_is_rejected_by_shared_json_helper() -> None:
    with pytest.raises(ValueError, match="Invalid shared event JSON payload"):
        validate_test_event_boundary_json('{"event_type": "trade_proposal"')


def test_trade_proposal_channel_maps_to_trade_proposal_event_type() -> None:
    event = validate_test_redis_envelope(
        RedisKeys.CHANNEL_TRADE_PROPOSALS,
        serialize_test_event_boundary_payload(_trade_proposal_payload()),
    )

    assert isinstance(event, TradeProposal)
    assert event.event_type == "trade_proposal"


def test_trade_proposal_channel_event_type_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="channel/event_type mismatch"):
        validate_test_redis_envelope(
            RedisKeys.CHANNEL_TRADE_PROPOSALS,
            serialize_test_event_boundary_payload(_raw_whale_trade_payload()),
        )


def test_trade_proposal_keeps_canonical_ids_optional() -> None:
    payload = _trade_proposal_payload()
    payload.pop("condition_id")
    payload.pop("token_id")

    event = validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))

    assert isinstance(event, TradeProposal)
    assert event.condition_id is None
    assert event.token_id is None


def test_trade_proposal_preserves_canonical_and_display_identifiers() -> None:
    event = validate_test_event_boundary_json(
        serialize_test_event_boundary_payload(_trade_proposal_payload())
    )

    assert isinstance(event, TradeProposal)
    assert event.condition_id == "0xconditionphase0a05i"
    assert event.token_id == "12345678901234567890"
    assert event.market_slug == "presidential-election-winner-2028"
    assert event.outcome == "YES"


def test_trade_proposal_preserves_legacy_identifier_compatibility() -> None:
    payload = _trade_proposal_payload()
    payload[LEGACY_ID_FIELD] = "legacy-compat-market"

    event = validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))

    assert isinstance(event, TradeProposal)
    assert getattr(event, LEGACY_ID_FIELD) == "legacy-compat-market"


def test_trade_proposal_validation_does_not_imply_approval_or_execution() -> None:
    """Validation contract only: operator approval and execution are separate rails."""
    event = validate_test_redis_envelope(
        RedisKeys.CHANNEL_TRADE_PROPOSALS,
        serialize_test_event_boundary_payload(_trade_proposal_payload()),
    )

    assert isinstance(event, TradeProposal)
    assert event.status == "PENDING_APPROVAL"
    assert event.status != "APPROVED"
    assert event.status != "EXECUTED"
