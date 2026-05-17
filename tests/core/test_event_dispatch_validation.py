"""Focused tests for Phase 0A shared event dispatch validation helpers."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest
from pydantic import BaseModel

from meg.core.events import (
    SHARED_EVENT_MODEL_REGISTRY,
    SUPPORTED_EVENT_SCHEMA_VERSION,
    QualifiedWhaleTrade,
    RawWhaleTrade,
    SignalEvent,
    TradeProposal,
    get_event_model_for_type,
    validate_shared_event_payload,
)

LEGACY_ID_FIELD = "market" + "_id"
LEGACY_ID_VALUE = "legacy-market-for-dispatch"


def _score_payload() -> dict[str, float]:
    return {
        "lead_lag": 0.8,
        "consensus": 0.7,
        "kelly_confidence": 0.6,
        "divergence": 0.4,
        "conviction_ratio": 0.5,
        "archetype_multiplier": 1.1,
        "ladder_multiplier": 1.0,
    }


def _raw_whale_trade_payload() -> dict[str, Any]:
    return {
        "event_type": "raw_whale_trade",
        "wallet_address": "0xwallet",
        LEGACY_ID_FIELD: LEGACY_ID_VALUE,
        "outcome": "YES",
        "size_usdc": 453.60,
        "timestamp_ms": 1762819205123,
        "tx_hash": "0xtx",
        "block_number": 73123456,
        "market_price_at_trade": 0.63,
    }


def _qualified_whale_trade_payload() -> dict[str, Any]:
    payload = _raw_whale_trade_payload()
    payload.update(
        {
            "event_type": "qualified_whale_trade",
            "whale_score": 0.82,
            "archetype": "INFORMATION",
            "intent": "SIGNAL",
        }
    )
    return payload


def _signal_event_payload() -> dict[str, Any]:
    return {
        "event_type": "signal",
        "signal_id": "sig-1",
        LEGACY_ID_FIELD: LEGACY_ID_VALUE,
        "outcome": "YES",
        "composite_score": 0.78,
        "scores": _score_payload(),
        "recommended_size_usdc": 25.0,
        "kelly_fraction": 0.05,
        "ttl_expires_at_ms": 1762819510000,
        "triggering_wallet": "0xwallet",
    }


def _trade_proposal_payload() -> dict[str, Any]:
    return {
        "event_type": "trade_proposal",
        "proposal_id": "proposal-1",
        "signal_id": "sig-1",
        LEGACY_ID_FIELD: LEGACY_ID_VALUE,
        "outcome": "YES",
        "size_usdc": 25.0,
        "limit_price": 0.64,
        "status": "PENDING_APPROVAL",
        "created_at_ms": 1762819210000,
        "scores": _score_payload(),
    }


EVENT_PAYLOAD_CASES: list[tuple[str, type[BaseModel], Callable[[], dict[str, Any]]]] = [
    ("raw_whale_trade", RawWhaleTrade, _raw_whale_trade_payload),
    ("qualified_whale_trade", QualifiedWhaleTrade, _qualified_whale_trade_payload),
    ("signal", SignalEvent, _signal_event_payload),
    ("trade_proposal", TradeProposal, _trade_proposal_payload),
]


def test_registry_contains_expected_shared_event_types() -> None:
    assert SHARED_EVENT_MODEL_REGISTRY == {
        event_type: model for event_type, model, _payload_factory in EVENT_PAYLOAD_CASES
    }


def test_registry_event_types_are_unique() -> None:
    event_type_values = [
        model.model_fields["event_type"].default
        for _event_type, model, _payload_factory in EVENT_PAYLOAD_CASES
    ]

    assert len(event_type_values) == len(set(event_type_values))
    assert len(SHARED_EVENT_MODEL_REGISTRY) == len(event_type_values)


@pytest.mark.parametrize("event_type,model,_payload_factory", EVENT_PAYLOAD_CASES)
def test_get_event_model_for_type_returns_expected_model(
    event_type: str, model: type[BaseModel], _payload_factory: Callable[[], dict[str, Any]]
) -> None:
    assert get_event_model_for_type(event_type) is model


@pytest.mark.parametrize("_event_type,model,payload_factory", EVENT_PAYLOAD_CASES)
def test_validate_shared_event_payload_returns_expected_model_class(
    _event_type: str, model: type[BaseModel], payload_factory: Callable[[], dict[str, Any]]
) -> None:
    event = validate_shared_event_payload(payload_factory())

    assert isinstance(event, model)


@pytest.mark.parametrize("_event_type,_model,payload_factory", EVENT_PAYLOAD_CASES)
def test_missing_schema_version_defaults_to_supported_version_during_dispatch(
    _event_type: str, _model: type[BaseModel], payload_factory: Callable[[], dict[str, Any]]
) -> None:
    payload = payload_factory()
    payload.pop("schema_version", None)

    event = validate_shared_event_payload(payload)

    assert event.schema_version == SUPPORTED_EVENT_SCHEMA_VERSION


@pytest.mark.parametrize("_event_type,_model,payload_factory", EVENT_PAYLOAD_CASES)
def test_explicit_supported_schema_version_is_accepted_and_round_tripped(
    _event_type: str, _model: type[BaseModel], payload_factory: Callable[[], dict[str, Any]]
) -> None:
    payload = payload_factory()
    payload["schema_version"] = SUPPORTED_EVENT_SCHEMA_VERSION

    event = validate_shared_event_payload(payload)

    assert event.schema_version == SUPPORTED_EVENT_SCHEMA_VERSION
    assert event.model_dump()["schema_version"] == SUPPORTED_EVENT_SCHEMA_VERSION


@pytest.mark.parametrize("_event_type,_model,payload_factory", EVENT_PAYLOAD_CASES)
def test_unsupported_schema_version_is_rejected_by_dispatch_helper(
    _event_type: str, _model: type[BaseModel], payload_factory: Callable[[], dict[str, Any]]
) -> None:
    payload = payload_factory()
    payload["schema_version"] = SUPPORTED_EVENT_SCHEMA_VERSION + 1

    with pytest.raises(ValueError, match="Unsupported event schema_version"):
        validate_shared_event_payload(payload)


def test_missing_event_type_is_rejected_by_dispatch_helper() -> None:
    payload = _raw_whale_trade_payload()
    payload.pop("event_type")

    with pytest.raises(ValueError, match="missing event_type"):
        validate_shared_event_payload(payload)


def test_unknown_event_type_is_rejected_by_dispatch_helper() -> None:
    payload = _raw_whale_trade_payload()
    payload["event_type"] = "not_a_shared_event"

    with pytest.raises(ValueError, match="Unknown event_type"):
        validate_shared_event_payload(payload)


def test_dispatch_uses_event_type_not_legacy_identifier() -> None:
    payload = _raw_whale_trade_payload()
    payload[LEGACY_ID_FIELD] = "trade_proposal"

    event = validate_shared_event_payload(payload)

    assert isinstance(event, RawWhaleTrade)
    assert getattr(event, LEGACY_ID_FIELD) == "trade_proposal"


@pytest.mark.parametrize("_event_type,model,payload_factory", EVENT_PAYLOAD_CASES)
def test_model_level_legacy_payload_behavior_remains_compatible(
    _event_type: str, model: type[BaseModel], payload_factory: Callable[[], dict[str, Any]]
) -> None:
    event = model.model_validate(payload_factory())

    assert event.schema_version == SUPPORTED_EVENT_SCHEMA_VERSION
    assert getattr(event, LEGACY_ID_FIELD) == LEGACY_ID_VALUE
