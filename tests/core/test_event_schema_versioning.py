"""Phase 0A compatibility tests for shared event schema versions."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest
from pydantic import ValidationError

import meg.core.events as events
from meg.core.events import (
    AlertMessage,
    MarketState,
    PositionState,
    QualifiedWhaleTrade,
    RawWhaleTrade,
    SignalEvent,
    SignalScores,
    TradeProposal,
)

LEGACY_MARKET_FIELD = "market" + "_id"
LEGACY_MARKET_VALUE = "legacy-market-id-compat"
CANONICAL_IDS = {
    "condition_id": "0xcondition000000000000000000000000000000000000000000000000000000000002",
    "token_id": "2234567890123456789012345678901234567890",
    "outcome": "YES",
}


def _base_raw_whale_trade_payload() -> dict[str, Any]:
    return {
        "event_type": "raw_whale_trade",
        "wallet_address": "0xwallet",
        LEGACY_MARKET_FIELD: LEGACY_MARKET_VALUE,
        "outcome": "YES",
        "size_usdc": 453.60,
        "timestamp_ms": 1762819205123,
        "tx_hash": "0xtx",
        "block_number": 73123456,
        "market_price_at_trade": 0.63,
    }


def _base_qualified_whale_trade_payload() -> dict[str, Any]:
    payload = _base_raw_whale_trade_payload()
    payload.update(
        {
            "event_type": "qualified_whale_trade",
            "whale_score": 0.82,
            "archetype": "INFORMATION",
            "intent": "SIGNAL",
        }
    )
    return payload


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


def _base_signal_event_payload() -> dict[str, Any]:
    return {
        "event_type": "signal",
        "signal_id": "sig-1",
        LEGACY_MARKET_FIELD: LEGACY_MARKET_VALUE,
        "outcome": "YES",
        "composite_score": 0.78,
        "scores": _score_payload(),
        "recommended_size_usdc": 25.0,
        "kelly_fraction": 0.05,
        "ttl_expires_at_ms": 1762819510000,
        "triggering_wallet": "0xwallet",
    }


def _base_trade_proposal_payload() -> dict[str, Any]:
    return {
        "event_type": "trade_proposal",
        "proposal_id": "proposal-1",
        "signal_id": "sig-1",
        LEGACY_MARKET_FIELD: LEGACY_MARKET_VALUE,
        "outcome": "YES",
        "size_usdc": 25.0,
        "limit_price": 0.64,
        "status": "PENDING_APPROVAL",
        "created_at_ms": 1762819210000,
        "scores": _score_payload(),
    }


def _base_alert_message_payload() -> dict[str, Any]:
    return {
        "alert_type": "trap",
        "message": "Trap detected for operator review.",
        "urgent": True,
    }


def _base_position_state_payload() -> dict[str, Any]:
    return {
        "position_id": "position-1",
        LEGACY_MARKET_FIELD: LEGACY_MARKET_VALUE,
        "outcome": "YES",
        "entry_price": 0.62,
        "current_price": 0.65,
        "size_usdc": 25.0,
        "shares": 40.32,
        "entry_signal_id": "sig-1",
        "opened_at_ms": 1762819210000,
        "take_profit_price": 0.74,
        "stop_loss_price": 0.54,
    }


def _base_market_state_payload() -> dict[str, Any]:
    return {
        LEGACY_MARKET_FIELD: LEGACY_MARKET_VALUE,
        "outcome": "YES",
        "bid": 0.62,
        "ask": 0.64,
        "mid_price": 0.63,
        "spread": 0.02,
        "liquidity_usdc": 2500.0,
        "volume_24h_usdc": 12500.0,
        "participants": 85,
        "last_updated_at": "2026-05-17T12:00:00Z",
    }


SCHEMA_VERSIONED_MODEL_CASES = [
    pytest.param(RawWhaleTrade, _base_raw_whale_trade_payload, id="raw_whale_trade"),
    pytest.param(QualifiedWhaleTrade, _base_qualified_whale_trade_payload, id="qualified_whale_trade"),
    pytest.param(SignalEvent, _base_signal_event_payload, id="signal_event"),
    pytest.param(TradeProposal, _base_trade_proposal_payload, id="trade_proposal"),
    pytest.param(AlertMessage, _base_alert_message_payload, id="alert_message"),
    pytest.param(PositionState, _base_position_state_payload, id="position_state"),
    pytest.param(MarketState, _base_market_state_payload, id="market_state"),
]


@pytest.mark.parametrize("model,payload_factory", SCHEMA_VERSIONED_MODEL_CASES)
def test_shared_event_models_default_schema_version_to_one(
    model: type[Any], payload_factory: Any
) -> None:
    payload = payload_factory()

    event = model.model_validate(payload)
    dumped = event.model_dump()

    assert event.schema_version == 1
    assert dumped["schema_version"] == 1


@pytest.mark.parametrize("model,payload_factory", SCHEMA_VERSIONED_MODEL_CASES)
def test_shared_event_models_preserve_schema_version_one_when_supplied(
    model: type[Any], payload_factory: Any
) -> None:
    payload = payload_factory()
    payload["schema_version"] = 1

    event = model.model_validate(payload)

    assert event.schema_version == 1
    assert event.model_dump()["schema_version"] == 1


@pytest.mark.parametrize("model,payload_factory", SCHEMA_VERSIONED_MODEL_CASES)
def test_legacy_payloads_without_schema_version_still_validate(
    model: type[Any], payload_factory: Any
) -> None:
    payload = payload_factory()
    payload.pop("schema_version", None)

    event = model.model_validate(payload)

    assert event.model_dump()["schema_version"] == 1


@pytest.mark.parametrize("model,payload_factory", SCHEMA_VERSIONED_MODEL_CASES)
def test_schema_version_round_trips_with_existing_payload_fields(
    model: type[Any], payload_factory: Any
) -> None:
    payload = payload_factory()
    payload["schema_version"] = 1
    payload_with_canonical_ids = deepcopy(payload)
    if issubclass(model, events.CanonicalIdentifiers):
        payload_with_canonical_ids.update(CANONICAL_IDS)

    event = model.model_validate(payload_with_canonical_ids)
    reparsed = model.model_validate(event.model_dump())

    assert reparsed.schema_version == 1
    if LEGACY_MARKET_FIELD in payload:
        assert getattr(reparsed, LEGACY_MARKET_FIELD) == LEGACY_MARKET_VALUE
    if issubclass(model, events.CanonicalIdentifiers):
        assert reparsed.condition_id == CANONICAL_IDS["condition_id"]
        assert reparsed.token_id == CANONICAL_IDS["token_id"]


def test_schema_version_is_not_part_of_redis_routing_contract() -> None:
    redis_route_values = [
        value
        for name, value in vars(events.RedisKeys).items()
        if name.startswith("CHANNEL_") or isinstance(value, str)
    ]

    assert all("schema_version" not in value for value in redis_route_values)


@pytest.mark.parametrize("model,payload_factory", SCHEMA_VERSIONED_MODEL_CASES)
@pytest.mark.xfail(
    reason="Future target: restrict schema_version to the explicitly supported version set.",
    strict=True,
)
def test_shared_event_models_reject_unsupported_schema_versions(
    model: type[Any], payload_factory: Any
) -> None:
    payload = payload_factory()
    payload["schema_version"] = 0

    with pytest.raises(ValidationError):
        model.model_validate(payload)
