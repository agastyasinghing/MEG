"""Tests for the Phase 0A test-only JSON shared-event boundary."""
from __future__ import annotations

from typing import Any

import pytest

from meg.core.events import (
    SUPPORTED_EVENT_SCHEMA_VERSION,
    RawWhaleTrade,
    SignalEvent,
    validate_raw_whale_trade_channel_payload,
    validate_shared_event_json,
)
from tests.core.event_fixture_boundary import (
    serialize_test_event_boundary_payload,
    validate_test_event_boundary_json,
)

LEGACY_ID_FIELD = "market" + "_id"
LEGACY_ID_VALUE = "polymarket-presidential-election-2028"
CONDITION_ID_VALUE = "0xconditionphase0a02d"
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


def _signal_payload() -> dict[str, Any]:
    return {
        "event_type": "signal",
        "signal_id": "sig-phase0a-02d-001",
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


def test_raw_whale_trade_dict_round_trips_through_json_boundary() -> None:
    payload_json = serialize_test_event_boundary_payload(_raw_whale_trade_payload())

    event = validate_test_event_boundary_json(payload_json)

    assert isinstance(event, RawWhaleTrade)
    assert event.event_type == "raw_whale_trade"
    assert event.condition_id == CONDITION_ID_VALUE
    assert event.token_id == TOKEN_ID_VALUE


def test_signal_dict_round_trips_through_json_boundary() -> None:
    payload_json = serialize_test_event_boundary_payload(_signal_payload())

    event = validate_test_event_boundary_json(payload_json)

    assert isinstance(event, SignalEvent)
    assert event.event_type == "signal"
    assert event.signal_id == "sig-phase0a-02d-001"
    assert event.scores.lead_lag == pytest.approx(0.82)


def test_model_instance_round_trips_from_model_dump_and_model_dump_json() -> None:
    model = RawWhaleTrade.model_validate(_raw_whale_trade_payload())

    from_dump = validate_test_event_boundary_json(
        serialize_test_event_boundary_payload(model.model_dump())
    )
    from_dump_json = validate_test_event_boundary_json(model.model_dump_json())
    from_model = validate_test_event_boundary_json(serialize_test_event_boundary_payload(model))

    assert isinstance(from_dump, RawWhaleTrade)
    assert isinstance(from_dump_json, RawWhaleTrade)
    assert isinstance(from_model, RawWhaleTrade)
    assert from_dump.model_dump() == from_dump_json.model_dump() == from_model.model_dump()


def test_missing_schema_version_defaults_to_one_after_json_decode() -> None:
    payload = _raw_whale_trade_payload()
    payload.pop("schema_version", None)

    event = validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))

    assert event.schema_version == SUPPORTED_EVENT_SCHEMA_VERSION
    assert event.model_dump()["schema_version"] == SUPPORTED_EVENT_SCHEMA_VERSION


def test_explicit_schema_version_one_round_trips_after_json_decode() -> None:
    payload = _signal_payload()
    payload["schema_version"] = SUPPORTED_EVENT_SCHEMA_VERSION

    event = validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))

    assert event.schema_version == SUPPORTED_EVENT_SCHEMA_VERSION
    assert event.model_dump()["schema_version"] == SUPPORTED_EVENT_SCHEMA_VERSION


def test_unsupported_schema_version_is_rejected_after_json_decode() -> None:
    payload = _raw_whale_trade_payload()
    payload["schema_version"] = SUPPORTED_EVENT_SCHEMA_VERSION + 1

    with pytest.raises(ValueError, match="Unsupported event schema_version"):
        validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))


def test_missing_event_type_is_rejected_after_json_decode() -> None:
    payload = _raw_whale_trade_payload()
    payload.pop("event_type")

    with pytest.raises(ValueError, match="missing event_type"):
        validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))


def test_unknown_event_type_is_rejected_after_json_decode() -> None:
    payload = _raw_whale_trade_payload()
    payload["event_type"] = "unknown_shared_event"

    with pytest.raises(ValueError, match="Unknown event_type"):
        validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))


def test_invalid_json_is_rejected_clearly() -> None:
    with pytest.raises(ValueError, match="Invalid shared event JSON payload"):
        validate_test_event_boundary_json('{"event_type": "raw_whale_trade"')


@pytest.mark.parametrize("payload_json", ['[]', '"raw_whale_trade"', '1', 'null'])
def test_non_object_json_values_are_rejected_clearly(payload_json: str) -> None:
    with pytest.raises(ValueError, match="must decode to an object"):
        validate_test_event_boundary_json(payload_json)


def test_json_boundary_dispatches_by_event_type_not_legacy_identifier() -> None:
    payload = _raw_whale_trade_payload()
    payload[LEGACY_ID_FIELD] = "signal"

    event = validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))

    assert isinstance(event, RawWhaleTrade)
    assert getattr(event, LEGACY_ID_FIELD) == "signal"


def test_json_boundary_preserves_legacy_compatibility_fields() -> None:
    event = validate_test_event_boundary_json(
        serialize_test_event_boundary_payload(_signal_payload())
    )

    assert isinstance(event, SignalEvent)
    assert getattr(event, LEGACY_ID_FIELD) == LEGACY_ID_VALUE
    assert event.market_category == "politics"
    assert event.triggering_wallet.startswith("0x")


def test_json_boundary_keeps_canonical_identifiers_optional() -> None:
    payload = _signal_payload()
    payload.pop("condition_id")
    payload.pop("token_id")
    payload.pop("market_slug")

    event = validate_test_event_boundary_json(serialize_test_event_boundary_payload(payload))

    assert isinstance(event, SignalEvent)
    assert event.condition_id is None
    assert event.token_id is None
    assert event.market_slug is None
    assert getattr(event, LEGACY_ID_FIELD) == LEGACY_ID_VALUE


def test_production_shared_event_json_helper_matches_test_boundary_behavior() -> None:
    payload_json = serialize_test_event_boundary_payload(_raw_whale_trade_payload())

    event = validate_shared_event_json(payload_json)

    assert isinstance(event, RawWhaleTrade)
    assert event.condition_id == CONDITION_ID_VALUE
    assert event.token_id == TOKEN_ID_VALUE


def test_production_raw_whale_trade_helper_accepts_missing_schema_version() -> None:
    payload = _raw_whale_trade_payload()
    payload.pop("schema_version", None)

    event = validate_raw_whale_trade_channel_payload(
        serialize_test_event_boundary_payload(payload)
    )

    assert event.schema_version == SUPPORTED_EVENT_SCHEMA_VERSION
    assert event.event_type == "raw_whale_trade"


def test_production_raw_whale_trade_helper_rejects_wrong_supported_event_type() -> None:
    with pytest.raises(ValueError, match="expects event_type=raw_whale_trade"):
        validate_raw_whale_trade_channel_payload(
            serialize_test_event_boundary_payload(_signal_payload())
        )


def test_production_shared_event_json_helper_rejects_non_object_json() -> None:
    with pytest.raises(ValueError, match="must decode to an object"):
        validate_shared_event_json("[]")
