"""Canonical identifier helpers for shared-rail boundary payloads.

These helpers validate and attach the Phase 0A canonical route tuple without
migrating existing producers or consumers. The route tuple is always
``(condition_id, token_id, outcome)``. ``market_slug`` is optional display
metadata only.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

_CANONICAL_FIELDS = ("condition_id", "token_id", "outcome")
_VALID_OUTCOMES = frozenset({"YES", "NO"})

def _payload_to_dict(payload: Any) -> dict[str, Any]:
    """Return a shallow dict copy for mapping or Pydantic-like payloads."""
    if isinstance(payload, Mapping):
        return dict(payload)

    model_dump = getattr(payload, "model_dump", None)
    if callable(model_dump):
        return dict(model_dump())

    legacy_dict = getattr(payload, "dict", None)
    if callable(legacy_dict):
        return dict(legacy_dict())

    raise TypeError("payload must be a mapping or Pydantic model instance")


def _context_prefix(context: str) -> str:
    return f"{context}: " if context else ""


def _validate_text(value: Any, *, field_name: str, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{_context_prefix(context)}missing canonical identifier: {field_name}")
    return value.strip()


def _validate_outcome(value: Any, *, context: str) -> str:
    outcome = _validate_text(value, field_name="outcome", context=context)
    if outcome not in _VALID_OUTCOMES:
        raise ValueError(
            f"{_context_prefix(context)}invalid outcome: expected YES or NO"
        )
    return outcome


def has_canonical_identifiers(payload: Any) -> bool:
    """Return True when payload contains a valid canonical route tuple."""
    try:
        require_canonical_identifiers(payload)
    except (TypeError, ValueError):
        return False
    return True


def require_canonical_identifiers(
    payload: Any, *, context: str = ""
) -> tuple[str, str, str]:
    """Validate and return ``(condition_id, token_id, outcome)``.

    The values must be explicit payload fields. No legacy identifier or display
    metadata is ever used to derive canonical route identity.
    """
    data = _payload_to_dict(payload)
    missing_fields = [field for field in _CANONICAL_FIELDS if data.get(field) is None]
    if missing_fields:
        joined = ", ".join(missing_fields)
        raise ValueError(f"{_context_prefix(context)}missing canonical identifier(s): {joined}")

    condition_id = _validate_text(
        data.get("condition_id"), field_name="condition_id", context=context
    )
    token_id = _validate_text(data.get("token_id"), field_name="token_id", context=context)
    outcome = _validate_outcome(data.get("outcome"), context=context)
    return condition_id, token_id, outcome


def canonical_route_from_payload(
    payload: Any, *, context: str = ""
) -> tuple[str, str, str]:
    """Return the canonical routing tuple from a boundary payload."""
    return require_canonical_identifiers(payload, context=context)


def attach_canonical_identifiers(
    payload: Any,
    *,
    condition_id: str,
    token_id: str,
    outcome: str,
    market_slug: str | None = None,
) -> dict[str, Any]:
    """Return a payload copy with explicit canonical identifiers attached."""
    canonical_values = {
        "condition_id": condition_id,
        "token_id": token_id,
        "outcome": outcome,
    }
    condition_id, token_id, outcome = require_canonical_identifiers(canonical_values)

    data = _payload_to_dict(payload)
    data.update(
        {
            "condition_id": condition_id,
            "token_id": token_id,
            "outcome": outcome,
        }
    )
    if market_slug is not None:
        data["market_slug"] = _validate_text(
            market_slug, field_name="market_slug", context=""
        )
    return data


def normalize_boundary_payload(
    payload: Any,
    *,
    condition_id: str | None = None,
    token_id: str | None = None,
    outcome: str | None = None,
    market_slug: str | None = None,
    context: str = "",
) -> dict[str, Any]:
    """Return a validated payload copy normalized for canonical routing.

    If any canonical route argument is supplied, all three route values must be
    supplied explicitly and are attached to a copy of the payload. Otherwise,
    existing payload fields are validated in place. ``market_slug`` may be added
    as display metadata, but it cannot satisfy canonical route validation.
    """
    supplied = {
        "condition_id": condition_id,
        "token_id": token_id,
        "outcome": outcome,
    }
    if any(value is not None for value in supplied.values()):
        missing = [field for field, value in supplied.items() if value is None]
        if missing:
            joined = ", ".join(missing)
            raise ValueError(
                f"{_context_prefix(context)}missing canonical argument(s): {joined}"
            )
        return attach_canonical_identifiers(
            payload,
            condition_id=condition_id or "",
            token_id=token_id or "",
            outcome=outcome or "",
            market_slug=market_slug,
        )

    data = _payload_to_dict(payload)
    if market_slug is not None:
        data["market_slug"] = _validate_text(
            market_slug, field_name="market_slug", context=context
        )
    require_canonical_identifiers(data, context=context)
    return data
