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

from meg.core.events import validate_shared_event_payload


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
