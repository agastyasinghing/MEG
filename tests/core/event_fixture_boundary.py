"""Test-only shared-event fixture boundary for Phase 0A validation trials.

This module intentionally lives under tests/core so production publishers,
subscribers, and routing behavior remain unchanged while tests exercise the
shared event dispatch validator at one realistic boundary seam.
"""
from __future__ import annotations

import json
from json import JSONDecodeError
from typing import Any, Mapping

from pydantic import BaseModel

from meg.core.events import RedisKeys, validate_shared_event_payload


REDIS_ENVELOPE_EVENT_TYPES: dict[str, str] = {
    RedisKeys.CHANNEL_RAW_WHALE_TRADES: "raw_whale_trade",
    RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES: "qualified_whale_trade",
    RedisKeys.CHANNEL_SIGNAL_EVENTS: "signal",
    RedisKeys.CHANNEL_TRADE_PROPOSALS: "trade_proposal",
}


def validate_test_event_boundary_payload(payload: Mapping[str, Any]) -> BaseModel:
    """Validate a shared-event payload as it crosses a test-only boundary."""
    return validate_shared_event_payload(payload)


def serialize_test_event_boundary_payload(event_or_payload: BaseModel | Mapping[str, Any]) -> str:
    """Serialize a shared-event model or payload through the test-only JSON seam."""
    if isinstance(event_or_payload, BaseModel):
        return event_or_payload.model_dump_json()

    return json.dumps(dict(event_or_payload))


def validate_test_event_boundary_json(payload_json: str) -> BaseModel:
    """Decode JSON from the test-only seam, then run shared dispatch validation."""
    try:
        payload = json.loads(payload_json)
    except JSONDecodeError as exc:
        raise ValueError("Invalid shared event JSON payload") from exc

    if not isinstance(payload, dict):
        raise ValueError("Shared event JSON payload must decode to an object")

    return validate_test_event_boundary_payload(payload)


def validate_test_redis_envelope(channel: str, payload_json: str) -> BaseModel:
    """Validate a test-only Redis channel + JSON payload envelope seam."""
    try:
        expected_event_type = REDIS_ENVELOPE_EVENT_TYPES[channel]
    except KeyError as exc:
        raise ValueError(f"Unknown shared event Redis channel: {channel}") from exc

    event = validate_test_event_boundary_json(payload_json)
    actual_event_type = getattr(event, "event_type", None)
    if actual_event_type != expected_event_type:
        raise ValueError(
            "Shared event Redis channel/event_type mismatch: "
            f"channel={channel} expects {expected_event_type}, got {actual_event_type}"
        )

    return event
