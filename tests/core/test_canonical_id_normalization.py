from __future__ import annotations

import pytest

from meg.core.canonical_ids import (
    attach_canonical_identifiers,
    canonical_route_from_payload,
    has_canonical_identifiers,
    normalize_boundary_payload,
    require_canonical_identifiers,
)
from meg.core.events import RawWhaleTrade

LEGACY_MARKET_ID = "market" "_id"


def canonical_payload() -> dict[str, str]:
    return {
        "condition_id": "0xcondition",
        "token_id": "123456789",
        "outcome": "YES",
    }


def test_payload_with_canonical_identifiers_passes() -> None:
    payload = canonical_payload()

    assert has_canonical_identifiers(payload) is True
    assert require_canonical_identifiers(payload) == (
        "0xcondition",
        "123456789",
        "YES",
    )
    assert canonical_route_from_payload(payload) == (
        "0xcondition",
        "123456789",
        "YES",
    )


@pytest.mark.parametrize(
    "missing_field",
    ["condition_id", "token_id", "outcome"],
)
def test_missing_canonical_fields_fail(missing_field: str) -> None:
    payload = canonical_payload()
    payload.pop(missing_field)

    with pytest.raises(ValueError, match=missing_field):
        require_canonical_identifiers(payload, context="boundary")

    assert has_canonical_identifiers(payload) is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("condition_id", ""),
        ("condition_id", "   "),
        ("condition_id", None),
        ("token_id", ""),
        ("token_id", None),
        ("outcome", ""),
        ("outcome", None),
        ("outcome", "yes"),
        ("outcome", "MAYBE"),
    ],
)
def test_empty_none_and_invalid_values_fail(field: str, value: object) -> None:
    payload = canonical_payload()
    payload[field] = value  # type: ignore[assignment]

    with pytest.raises(ValueError):
        require_canonical_identifiers(payload)


@pytest.mark.parametrize(
    "payload",
    [
        {LEGACY_MARKET_ID: "legacy-market"},
        {"market_slug": "display-slug"},
        {LEGACY_MARKET_ID: "legacy-market", "market_slug": "display-slug"},
    ],
)
def test_display_or_legacy_only_payloads_fail_canonical_extraction(
    payload: dict[str, str],
) -> None:
    with pytest.raises(ValueError):
        canonical_route_from_payload(payload)

    assert has_canonical_identifiers(payload) is False


def test_attach_canonical_identifiers_returns_copy_without_mutating_original() -> None:
    original = {LEGACY_MARKET_ID: "legacy-market", "other": "value"}

    normalized = attach_canonical_identifiers(
        original,
        condition_id="0xcondition",
        token_id="123456789",
        outcome="NO",
        market_slug="display-slug",
    )

    assert normalized is not original
    assert original == {LEGACY_MARKET_ID: "legacy-market", "other": "value"}
    assert normalized[LEGACY_MARKET_ID] == "legacy-market"
    assert normalized["condition_id"] == "0xcondition"
    assert normalized["token_id"] == "123456789"
    assert normalized["outcome"] == "NO"
    assert normalized["market_slug"] == "display-slug"


def test_market_slug_is_display_metadata_only() -> None:
    payload = canonical_payload()

    normalized = normalize_boundary_payload(
        payload,
        market_slug="display-slug",
        context="test-boundary",
    )

    assert normalized["market_slug"] == "display-slug"
    assert canonical_route_from_payload(normalized) == (
        "0xcondition",
        "123456789",
        "YES",
    )

    with pytest.raises(ValueError, match="condition_id"):
        normalize_boundary_payload({"market_slug": "display-slug"})


def test_normalize_boundary_payload_attaches_explicit_canonical_fields_to_copy() -> None:
    original = {LEGACY_MARKET_ID: "legacy-market"}

    normalized = normalize_boundary_payload(
        original,
        condition_id="0xcondition",
        token_id="123456789",
        outcome="NO",
    )

    assert normalized is not original
    assert original == {LEGACY_MARKET_ID: "legacy-market"}
    assert canonical_route_from_payload(normalized) == (
        "0xcondition",
        "123456789",
        "NO",
    )


def test_normalize_boundary_payload_requires_complete_explicit_route() -> None:
    with pytest.raises(ValueError, match="token_id"):
        normalize_boundary_payload(
            {},
            condition_id="0xcondition",
            outcome="YES",
        )


def test_helpers_never_derive_canonical_identifiers_from_legacy_identifier() -> None:
    payload = {
        LEGACY_MARKET_ID: "0xcondition:123456789:YES",
        "outcome": "YES",
    }

    with pytest.raises(ValueError, match="condition_id"):
        canonical_route_from_payload(payload)


def test_pydantic_event_models_can_provide_canonical_route() -> None:
    event = RawWhaleTrade(
        condition_id="0xcondition",
        token_id="123456789",
        market_slug="display-slug",
        wallet_address="0xwallet",
        **{LEGACY_MARKET_ID: "legacy-market"},
        outcome="YES",
        size_usdc=100.0,
        timestamp_ms=1762819205123,
        tx_hash="0xtx",
        block_number=123,
        market_price_at_trade=0.42,
    )

    assert canonical_route_from_payload(event) == (
        "0xcondition",
        "123456789",
        "YES",
    )
