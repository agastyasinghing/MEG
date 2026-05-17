"""Test-only shared-event fixture boundary for Phase 0A validation trials.

This module intentionally lives under tests/core so production publishers,
subscribers, and routing behavior remain unchanged while tests exercise the
shared event dispatch validator at one realistic boundary seam.
"""
from __future__ import annotations

from typing import Any, Mapping

from pydantic import BaseModel

from meg.core.events import validate_shared_event_payload


def validate_test_event_boundary_payload(payload: Mapping[str, Any]) -> BaseModel:
    """Validate a shared-event payload as it crosses a test-only boundary."""
    return validate_shared_event_payload(payload)
