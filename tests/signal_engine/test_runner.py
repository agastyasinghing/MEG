from __future__ import annotations

import importlib
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from meg.core.events import QualifiedWhaleTrade, RedisKeys, SignalEvent

LEGACY_ID_FIELD = "market" + "_id"


def _config() -> SimpleNamespace:
    return SimpleNamespace()


def _qualified_trade_payload() -> dict[str, object]:
    return {
        "event_type": "qualified_whale_trade",
        "wallet_address": "0x6f4c4f79e79c6d8b3c2e1234567890abcdef1234",
        LEGACY_ID_FIELD: "polymarket-presidential-election-2028",
        "condition_id": "0xconditionphase0a05d",
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
        "signal_id": "sig-phase0a-05d-001",
        LEGACY_ID_FIELD: "polymarket-presidential-election-2028",
        "condition_id": "0xconditionphase0a05d",
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


@pytest.mark.asyncio
async def test_process_valid_payload_calls_score(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = importlib.import_module("meg.signal_engine.runner")

    score_mock = AsyncMock(return_value=None)
    monkeypatch.setattr(runner.composite_scorer, "score", score_mock)

    published = await runner.process_qualified_trade_payload(
        redis=AsyncMock(),
        raw_data=json.dumps(_qualified_trade_payload()),
        config=_config(),
        session=AsyncMock(),
    )

    assert published is False
    assert score_mock.await_count == 1
    trade_arg = score_mock.await_args.args[0]
    assert isinstance(trade_arg, QualifiedWhaleTrade)


@pytest.mark.asyncio
async def test_process_score_signal_event_publishes_once(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = importlib.import_module("meg.signal_engine.runner")
    signal = SignalEvent.model_validate(_signal_event_payload())

    monkeypatch.setattr(runner.composite_scorer, "score", AsyncMock(return_value=signal))
    publish_mock = AsyncMock()
    monkeypatch.setattr(runner, "publish", publish_mock)

    published = await runner.process_qualified_trade_payload(
        redis=AsyncMock(),
        raw_data=json.dumps(_qualified_trade_payload()),
        config=_config(),
        session=AsyncMock(),
    )

    assert published is True
    publish_mock.assert_awaited_once()
    _, channel, payload_json = publish_mock.await_args.args
    assert channel == RedisKeys.CHANNEL_SIGNAL_EVENTS
    parsed = SignalEvent.model_validate_json(payload_json)
    assert parsed.signal_id == signal.signal_id


@pytest.mark.asyncio
async def test_process_invalid_inputs_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = importlib.import_module("meg.signal_engine.runner")
    publish_mock = AsyncMock()
    score_mock = AsyncMock(return_value=None)
    monkeypatch.setattr(runner, "publish", publish_mock)
    monkeypatch.setattr(runner.composite_scorer, "score", score_mock)

    bad_json = '{"event_type": "qualified_whale_trade"'
    wrong_type = _qualified_trade_payload()
    wrong_type["event_type"] = "signal"
    bad_schema = _qualified_trade_payload()
    bad_schema["schema_version"] = 999
    bad_model = _qualified_trade_payload()
    bad_model["wallet_address"] = 42

    for raw in [bad_json, json.dumps(wrong_type), json.dumps(bad_schema), json.dumps(bad_model)]:
        published = await runner.process_qualified_trade_payload(
            redis=AsyncMock(),
            raw_data=raw,
            config=_config(),
            session=AsyncMock(),
        )
        assert published is False

    assert score_mock.await_count == 0
    assert publish_mock.await_count == 0


@pytest.mark.asyncio
async def test_run_propagates_redis_disconnect(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = importlib.import_module("meg.signal_engine.runner")

    async def broken_subscribe(_redis, _channel):
        raise RedisConnectionError("boom")
        yield ""  # pragma: no cover

    monkeypatch.setattr(runner, "subscribe", broken_subscribe)

    class _SessionCtx:
        async def __aenter__(self):
            return AsyncMock()
        async def __aexit__(self, exc_type, exc, tb):
            return None

    with pytest.raises(RedisConnectionError):
        await runner.run(AsyncMock(), _config(), session_factory=lambda: _SessionCtx())


def test_runner_module_does_not_import_decision_agent() -> None:
    runner = importlib.import_module("meg.signal_engine.runner")
    assert "decision_agent" not in runner.__dict__
