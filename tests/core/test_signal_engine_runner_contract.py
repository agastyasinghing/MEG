"""Phase 0A-05C test-only contract for future signal-engine runner wiring.

These tests intentionally describe the expected runner API and channel behavior
without implementing production runtime wiring yet.
"""
from __future__ import annotations

import importlib

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from meg.core.events import (
    QualifiedWhaleTrade,
    RedisKeys,
    SignalEvent,
    validate_qualified_whale_trade_for_publish,
)
from tests.core.event_fixture_boundary import serialize_test_event_boundary_payload

LEGACY_ID_FIELD = "market" + "_id"


@pytest.mark.xfail(strict=True, reason="signal-engine runner not implemented yet")
def test_future_runner_module_exposes_run_callable_contract() -> None:
    runner = importlib.import_module("meg.signal_engine.runner")
    assert hasattr(runner, "run")
    assert callable(runner.run)


def test_runner_channel_contract_constants_are_defined() -> None:
    assert RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES == "qualified_whale_trades"
    assert RedisKeys.CHANNEL_SIGNAL_EVENTS == "signal_events"


@pytest.mark.xfail(strict=True, reason="signal-engine runner not implemented yet")
def test_future_runner_consumes_qualified_channel_and_publishes_signal_channel() -> None:
    runner = importlib.import_module("meg.signal_engine.runner")

    assert getattr(runner, "CONSUME_CHANNEL", None) == RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES
    assert getattr(runner, "PUBLISH_CHANNEL", None) == RedisKeys.CHANNEL_SIGNAL_EVENTS


@pytest.mark.xfail(strict=True, reason="signal-engine runner not implemented yet")
def test_future_runner_contract_behaviors_documented() -> None:
    """Contract checklist for future implementation.

    Expected behavior:
    - valid QualifiedWhaleTrade payload is accepted.
    - malformed JSON / wrong event_type / unsupported schema_version fails closed.
    - score() returning SignalEvent results in one SignalEvent publish.
    - score() returning None/drop does not publish.
    - Redis disconnect propagation is preserved.
    - decision_agent.evaluate is never called by runner.
    """

    runner = importlib.import_module("meg.signal_engine.runner")
    assert callable(runner.run)


def _qualified_trade_payload() -> dict[str, object]:
    return {
        "event_type": "qualified_whale_trade",
        "wallet_address": "0x6f4c4f79e79c6d8b3c2e1234567890abcdef1234",
        LEGACY_ID_FIELD: "polymarket-presidential-election-2028",
        "condition_id": "0xconditionphase0a05c",
        "token_id": "12345678901234567890",
        "market_slug": "presidential-election-winner-2028",
        "outcome": "YES",
        "size_usdc": 12750.25,
        "timestamp_ms": 1762819205123,
        "tx_hash": "0x8f2a9e1c4b7d6a5f3e2d1c0b9a887766554433221100ffeeddccbbaa99887766",
        "block_number": 73123456,
        "market_price_at_trade": 0.63,
        "market_category": "politics",
        "whale_score": 0.84,
        "archetype": "INFORMATION",
        "intent": "SIGNAL",
    }


def _signal_event_payload() -> dict[str, object]:
    return {
        "event_type": "signal",
        "signal_id": "sig-phase0a-05c-001",
        LEGACY_ID_FIELD: "polymarket-presidential-election-2028",
        "condition_id": "0xconditionphase0a05c",
        "token_id": "12345678901234567890",
        "market_slug": "presidential-election-winner-2028",
        "outcome": "YES",
        "composite_score": 0.79,
        "scores": {
            "lead_lag": 0.82,
            "consensus": 0.71,
            "kelly_confidence": 0.64,
            "divergence": 0.38,
            "conviction_ratio": 0.57,
            "archetype_multiplier": 1.15,
            "ladder_multiplier": 1.0,
        },
        "recommended_size_usdc": 225.0,
        "kelly_fraction": 0.045,
        "ttl_expires_at_ms": 1762820105123,
        "status": "PENDING",
        "triggering_wallet": "0x6f4c4f79e79c6d8b3c2e1234567890abcdef1234",
    }


def test_contract_fixture_valid_qualified_trade_payload_round_trip() -> None:
    event = validate_qualified_whale_trade_for_publish(_qualified_trade_payload())

    assert isinstance(event, QualifiedWhaleTrade)
    assert event.event_type == "qualified_whale_trade"
    assert event.condition_id == "0xconditionphase0a05c"
    assert event.token_id == "12345678901234567890"


def test_contract_fixture_signal_payload_round_trip() -> None:
    payload_json = serialize_test_event_boundary_payload(_signal_event_payload())

    event = SignalEvent.model_validate_json(payload_json)

    assert isinstance(event, SignalEvent)
    assert event.event_type == "signal"
    assert event.signal_id == "sig-phase0a-05c-001"


def test_contract_fixture_invalid_payload_examples_fail_closed() -> None:
    malformed_json = '{"event_type": "qualified_whale_trade"'
    with pytest.raises(ValueError):
        QualifiedWhaleTrade.model_validate_json(malformed_json)

    wrong_type = _qualified_trade_payload()
    wrong_type["event_type"] = "signal"
    with pytest.raises(ValueError, match="signal"):
        validate_qualified_whale_trade_for_publish(wrong_type)

    wrong_schema = _qualified_trade_payload()
    wrong_schema["schema_version"] = 999
    with pytest.raises(ValueError, match="Unsupported event schema_version"):
        validate_qualified_whale_trade_for_publish(wrong_schema)


def test_contract_documents_redis_disconnect_exception_type() -> None:
    assert issubclass(RedisConnectionError, Exception)
