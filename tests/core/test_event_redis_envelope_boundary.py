"""Tests for the Phase 0A test-only Redis envelope validation seam."""
from __future__ import annotations

from typing import Any

import pytest

from meg.core.events import (
    SUPPORTED_EVENT_SCHEMA_VERSION,
    QualifiedWhaleTrade,
    RawWhaleTrade,
    RedisKeys,
    SignalEvent,
    TradeProposal,
)
from tests.core.event_fixture_boundary import (
    serialize_test_event_boundary_payload,
    validate_test_redis_envelope,
)

LEGACY_ID_FIELD = "market" + "_id"
LEGACY_ID_VALUE = "polymarket-presidential-election-2028"
CONDITION_ID_VALUE = "0xconditionphase0a02e"
TOKEN_ID_VALUE = "12345678901234567890"


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


def _raw_whale_trade_payload() -> dict[str, Any]:
    return {
        "event_type": "raw_whale_trade",
        "wallet_address": "0x6f4c4f79e79c6d8b3c2e1234567890abcdef1234",
        LEGACY_ID_FIELD: LEGACY_ID_VALUE,
        "condition_id": CONDITION_ID_VALUE,
        "token_id": TOKEN_ID_VALUE,
        "market_slug": "presidential-election-winner-2028",
        "outcome": "YES",
        "size_usdc": 12750.25,
        "timestamp_ms": 1762819205123,
        "tx_hash": "0x8f2a9e1c4b7d6a5f3e2d1c0b9a887766554433221100ffeeddccbbaa99887766",
        "block_number": 73123456,
        "market_price_at_trade": 0.63,
        "market_category": "politics",
    }


def _qualified_whale_trade_payload() -> dict[str, Any]:
    payload = _raw_whale_trade_payload()
    payload.update(
        {
            "event_type": "qualified_whale_trade",
            "whale_score": 0.84,
            "archetype": "INFORMATION",
            "intent": "SIGNAL",
        }
    )
    return payload


def _signal_payload() -> dict[str, Any]:
    return {
        "event_type": "signal",
        "signal_id": "sig-phase0a-02e-001",
        LEGACY_ID_FIELD: LEGACY_ID_VALUE,
        "condition_id": CONDITION_ID_VALUE,
        "token_id": TOKEN_ID_VALUE,
        "market_slug": "presidential-election-winner-2028",
        "outcome": "YES",
        "composite_score": 0.79,
        "scores": _score_payload(),
        "recommended_size_usdc": 225.0,
        "kelly_fraction": 0.045,
        "ttl_expires_at_ms": 1762820105123,
        "status": "PENDING",
        "triggering_wallet": "0x6f4c4f79e79c6d8b3c2e1234567890abcdef1234",
        "contributing_wallets": [
            "0x6f4c4f79e79c6d8b3c2e1234567890abcdef1234",
            "0x9a5b7c6d8e9f00112233445566778899aabbccdd",
        ],
        "whale_count": 2,
        "is_contrarian": False,
        "is_ladder": False,
        "ladder_trade_count": 0,
        "market_price_at_signal": 0.64,
        "intent": "SIGNAL",
        "saturation_score": 0.18,
        "saturation_size_multiplier": 0.92,
        "trap_warning": False,
        "signal_type": "WHALE_REACTION",
        "estimated_half_life_minutes": 14.5,
        "whale_archetype": "INFORMATION",
        "market_category": "politics",
    }


def _trade_proposal_payload() -> dict[str, Any]:
    return {
        "event_type": "trade_proposal",
        "proposal_id": "proposal-phase0a-02e-001",
        "signal_id": "sig-phase0a-02e-001",
        LEGACY_ID_FIELD: LEGACY_ID_VALUE,
        "condition_id": CONDITION_ID_VALUE,
        "token_id": TOKEN_ID_VALUE,
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


def _payload_json(payload: dict[str, Any]) -> str:
    return serialize_test_event_boundary_payload(payload)


def test_raw_whale_trade_json_validates_on_raw_whale_trade_channel() -> None:
    event = validate_test_redis_envelope(
        RedisKeys.CHANNEL_RAW_WHALE_TRADES,
        _payload_json(_raw_whale_trade_payload()),
    )

    assert isinstance(event, RawWhaleTrade)
    assert event.event_type == "raw_whale_trade"
    assert event.condition_id == CONDITION_ID_VALUE


def test_signal_json_validates_on_signal_events_channel() -> None:
    event = validate_test_redis_envelope(
        RedisKeys.CHANNEL_SIGNAL_EVENTS,
        _payload_json(_signal_payload()),
    )

    assert isinstance(event, SignalEvent)
    assert event.event_type == "signal"
    assert event.signal_id == "sig-phase0a-02e-001"


def test_trade_proposal_json_validates_on_trade_proposals_channel() -> None:
    event = validate_test_redis_envelope(
        RedisKeys.CHANNEL_TRADE_PROPOSALS,
        _payload_json(_trade_proposal_payload()),
    )

    assert isinstance(event, TradeProposal)
    assert event.event_type == "trade_proposal"
    assert event.proposal_id == "proposal-phase0a-02e-001"


def test_qualified_whale_trade_json_validates_on_qualified_channel() -> None:
    event = validate_test_redis_envelope(
        RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES,
        _payload_json(_qualified_whale_trade_payload()),
    )

    assert isinstance(event, QualifiedWhaleTrade)
    assert event.event_type == "qualified_whale_trade"
    assert event.whale_score == pytest.approx(0.84)


def test_unknown_channel_is_rejected_clearly() -> None:
    with pytest.raises(ValueError, match="Unknown shared event Redis channel"):
        validate_test_redis_envelope("unknown_events", _payload_json(_signal_payload()))


def test_channel_event_type_mismatch_is_rejected_clearly() -> None:
    with pytest.raises(ValueError, match="channel/event_type mismatch"):
        validate_test_redis_envelope(
            RedisKeys.CHANNEL_SIGNAL_EVENTS,
            _payload_json(_raw_whale_trade_payload()),
        )


def test_invalid_json_is_rejected_clearly() -> None:
    with pytest.raises(ValueError, match="Invalid shared event JSON payload"):
        validate_test_redis_envelope(RedisKeys.CHANNEL_RAW_WHALE_TRADES, '{"event_type"')


@pytest.mark.parametrize("payload_json", ['[]', '"signal"', '1', 'null'])
def test_non_object_json_is_rejected_clearly(payload_json: str) -> None:
    with pytest.raises(ValueError, match="must decode to an object"):
        validate_test_redis_envelope(RedisKeys.CHANNEL_SIGNAL_EVENTS, payload_json)


def test_missing_event_type_is_rejected() -> None:
    payload = _signal_payload()
    payload.pop("event_type")

    with pytest.raises(ValueError, match="missing event_type"):
        validate_test_redis_envelope(RedisKeys.CHANNEL_SIGNAL_EVENTS, _payload_json(payload))


def test_unsupported_schema_version_is_rejected() -> None:
    payload = _signal_payload()
    payload["schema_version"] = SUPPORTED_EVENT_SCHEMA_VERSION + 1

    with pytest.raises(ValueError, match="Unsupported event schema_version"):
        validate_test_redis_envelope(RedisKeys.CHANNEL_SIGNAL_EVENTS, _payload_json(payload))


def test_legacy_compatibility_fields_are_preserved() -> None:
    event = validate_test_redis_envelope(
        RedisKeys.CHANNEL_SIGNAL_EVENTS,
        _payload_json(_signal_payload()),
    )

    assert isinstance(event, SignalEvent)
    assert getattr(event, LEGACY_ID_FIELD) == LEGACY_ID_VALUE
    assert event.market_category == "politics"
    assert event.triggering_wallet.startswith("0x")


def test_canonical_ids_remain_optional() -> None:
    payload = _signal_payload()
    payload.pop("condition_id")
    payload.pop("token_id")
    payload.pop("market_slug")

    event = validate_test_redis_envelope(RedisKeys.CHANNEL_SIGNAL_EVENTS, _payload_json(payload))

    assert isinstance(event, SignalEvent)
    assert event.condition_id is None
    assert event.token_id is None
    assert event.market_slug is None
    assert getattr(event, LEGACY_ID_FIELD) == LEGACY_ID_VALUE


def test_envelope_dispatch_uses_event_type_and_channel_contract_not_legacy_identifier() -> None:
    payload = _raw_whale_trade_payload()
    payload[LEGACY_ID_FIELD] = "signal"

    event = validate_test_redis_envelope(
        RedisKeys.CHANNEL_RAW_WHALE_TRADES,
        _payload_json(payload),
    )

    assert isinstance(event, RawWhaleTrade)
    assert event.event_type == "raw_whale_trade"
    assert getattr(event, LEGACY_ID_FIELD) == "signal"
