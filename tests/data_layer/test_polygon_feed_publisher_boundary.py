"""Publisher-boundary validation tests for the data-layer raw whale rail."""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from meg.core.events import (
    RawWhaleTrade,
    RedisKeys,
    SUPPORTED_EVENT_SCHEMA_VERSION,
    validate_raw_whale_trade_channel_payload,
)
from meg.data_layer.polygon_feed import _emit_event

LEGACY_ID_FIELD = "market" + "_id"


def _raw_payload(**updates: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": SUPPORTED_EVENT_SCHEMA_VERSION,
        "event_type": "raw_whale_trade",
        "wallet_address": "0xabc",
        LEGACY_ID_FIELD: "legacy-market-001",
        "outcome": "YES",
        "size_usdc": 750.0,
        "timestamp_ms": 1_700_000_000_000,
        "tx_hash": "0x" + "a" * 64,
        "block_number": 123,
        "market_price_at_trade": 0.42,
        "market_category": "crypto",
    }
    payload.update(updates)
    return payload


@pytest.mark.asyncio
async def test_emit_event_valid_current_raw_trade_publishes_once(mock_redis) -> None:
    event = RawWhaleTrade.model_validate(_raw_payload())

    with patch("meg.data_layer.polygon_feed.publish", new_callable=AsyncMock) as publish_mock:
        await _emit_event(mock_redis, event)

    publish_mock.assert_awaited_once()
    assert publish_mock.await_args.args[0] is mock_redis
    assert publish_mock.await_args.args[1] == RedisKeys.CHANNEL_RAW_WHALE_TRADES

    published = validate_raw_whale_trade_channel_payload(publish_mock.await_args.args[2])
    assert published == event


@pytest.mark.asyncio
async def test_emit_event_defaults_missing_schema_version_before_publish(mock_redis) -> None:
    payload = _raw_payload()
    payload.pop("schema_version")

    with patch("meg.data_layer.polygon_feed.publish", new_callable=AsyncMock) as publish_mock:
        await _emit_event(mock_redis, payload)  # type: ignore[arg-type]

    publish_mock.assert_awaited_once()
    published = validate_raw_whale_trade_channel_payload(publish_mock.await_args.args[2])
    assert published.schema_version == SUPPORTED_EVENT_SCHEMA_VERSION


@pytest.mark.asyncio
async def test_emit_event_preserves_canonical_ids_and_legacy_identifier(mock_redis) -> None:
    payload = _raw_payload(
        condition_id="cond-001",
        token_id="token-yes-001",
        market_slug="example-market",
    )

    with patch("meg.data_layer.polygon_feed.publish", new_callable=AsyncMock) as publish_mock:
        await _emit_event(mock_redis, RawWhaleTrade.model_validate(payload))

    published = validate_raw_whale_trade_channel_payload(publish_mock.await_args.args[2])
    assert published.condition_id == "cond-001"
    assert published.token_id == "token-yes-001"
    assert published.market_slug == "example-market"
    assert getattr(published, LEGACY_ID_FIELD) == "legacy-market-001"


@pytest.mark.asyncio
async def test_emit_event_keeps_canonical_ids_optional_when_absent(mock_redis) -> None:
    payload = _raw_payload()
    payload.pop("condition_id", None)
    payload.pop("token_id", None)
    payload.pop("market_slug", None)

    with patch("meg.data_layer.polygon_feed.publish", new_callable=AsyncMock) as publish_mock:
        await _emit_event(mock_redis, payload)  # type: ignore[arg-type]

    published = validate_raw_whale_trade_channel_payload(publish_mock.await_args.args[2])
    assert published.condition_id is None
    assert published.token_id is None
    assert published.market_slug is None
    assert getattr(published, LEGACY_ID_FIELD) == "legacy-market-001"


@pytest.mark.asyncio
async def test_emit_event_rejects_wrong_event_type_before_publish(mock_redis) -> None:
    payload = _raw_payload(event_type="signal")

    with patch("meg.data_layer.polygon_feed.publish", new_callable=AsyncMock) as publish_mock:
        with pytest.raises(ValueError):
            await _emit_event(mock_redis, payload)  # type: ignore[arg-type]

    publish_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_emit_event_rejects_unsupported_schema_version_before_publish(mock_redis) -> None:
    payload = _raw_payload(schema_version=SUPPORTED_EVENT_SCHEMA_VERSION + 1)

    with patch("meg.data_layer.polygon_feed.publish", new_callable=AsyncMock) as publish_mock:
        with pytest.raises(ValueError, match="Unsupported event schema_version"):
            await _emit_event(mock_redis, payload)  # type: ignore[arg-type]

    publish_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_emit_event_invalid_payload_does_not_publish(mock_redis) -> None:
    payload = _raw_payload(wallet_address=None)

    with patch("meg.data_layer.polygon_feed.publish", new_callable=AsyncMock) as publish_mock:
        with pytest.raises(ValueError):
            await _emit_event(mock_redis, payload)  # type: ignore[arg-type]

    publish_mock.assert_not_awaited()
