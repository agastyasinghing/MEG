"""
Phase 0A canonical identifier contract tests for shared event models.

These tests intentionally describe the target contract before production models are
migrated away from legacy ``market_id`` routing. Tests marked xfail should become
passing tests in the migration ticket that adds ``condition_id``, ``token_id``,
and display-only ``market_slug`` fields to the shared rail models.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest
from pydantic import ValidationError

import meg.core.events as events
from meg.core.events import QualifiedWhaleTrade, RawWhaleTrade, SignalEvent, SignalScores, TradeProposal


CANONICAL_IDS = {
    "condition_id": "0xcondition000000000000000000000000000000000000000000000000000000000001",
    "token_id": "1234567890123456789012345678901234567890",
    "outcome": "YES",
}
DISPLAY_MARKET_SLUG = "will-btc-be-above-120k-on-june-30"
LEGACY_MARKET_ID = "legacy-market-id-must-not-route"


def _base_raw_whale_fill_payload() -> dict[str, Any]:
    return {
        "event_type": "raw_whale_trade",
        "wallet_address": "0xwallet",
        "market_id": LEGACY_MARKET_ID,
        "outcome": "YES",
        "size_usdc": 453.60,
        "timestamp_ms": 1762819205123,
        "tx_hash": "0xtx",
        "block_number": 73123456,
        "market_price_at_trade": 0.63,
    }


def _base_qualified_whale_fill_payload() -> dict[str, Any]:
    payload = _base_raw_whale_fill_payload()
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


def _base_signal_payload() -> dict[str, Any]:
    return {
        "event_type": "signal",
        "signal_id": "sig-1",
        "market_id": LEGACY_MARKET_ID,
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
        "market_id": LEGACY_MARKET_ID,
        "outcome": "YES",
        "size_usdc": 25.0,
        "limit_price": 0.64,
        "status": "PENDING_APPROVAL",
        "created_at_ms": 1762819210000,
        "scores": _score_payload(),
    }


MODEL_CASES = [
    pytest.param(RawWhaleTrade, _base_raw_whale_fill_payload, id="raw_whale_fill_equivalent"),
    pytest.param(QualifiedWhaleTrade, _base_qualified_whale_fill_payload, id="qualified_whale_fill_equivalent"),
    pytest.param(SignalEvent, _base_signal_payload, id="signal_event_equivalent"),
    pytest.param(TradeProposal, _base_trade_proposal_payload, id="trade_proposal"),
]


@pytest.mark.parametrize("model,payload_factory", MODEL_CASES)
@pytest.mark.parametrize("field", ["condition_id", "token_id"])
@pytest.mark.xfail(
    reason="Ticket 0A-01B documents target contract before production models replace market_id with canonical IDs.",
    strict=True,
)
def test_shared_event_models_reject_missing_condition_id_or_token_id(
    model: type[Any], payload_factory: Any, field: str
) -> None:
    """All shared rail events must require condition_id and token_id after migration."""
    valid_payload = payload_factory()
    valid_payload.update(CANONICAL_IDS)
    valid_payload.pop("market_id", None)

    # Guard the positive side of the contract first: canonical IDs, without
    # legacy market_id, must be sufficient for event construction. Current
    # production models fail here, so this test is intentionally xfail until
    # the migration ticket updates the models.
    model.model_validate(valid_payload)

    invalid_payload = dict(valid_payload)
    invalid_payload.pop(field)
    with pytest.raises(ValidationError):
        model.model_validate(invalid_payload)


@pytest.mark.parametrize("model,payload_factory", MODEL_CASES)
def test_shared_event_models_reject_missing_outcome(model: type[Any], payload_factory: Any) -> None:
    """Existing and future shared rail events must reject missing outcome."""
    payload = payload_factory()
    payload.pop("outcome")

    with pytest.raises(ValidationError):
        model.model_validate(payload)


@pytest.mark.parametrize("model,payload_factory", MODEL_CASES)
@pytest.mark.xfail(
    reason="Legacy models still accept market_id-only routing payloads until the canonical ID migration lands.",
    strict=True,
)
def test_shared_event_models_reject_market_id_only_payloads_outside_named_boundary_shim(
    model: type[Any], payload_factory: Any
) -> None:
    """market_id-only payloads are invalid except at an explicit external boundary shim."""
    payload = payload_factory()
    assert "market_id" in payload
    assert "condition_id" not in payload
    assert "token_id" not in payload

    with pytest.raises(ValidationError):
        model.model_validate(payload)


@pytest.mark.parametrize("model,payload_factory", MODEL_CASES)
@pytest.mark.xfail(
    reason="Production event models do not yet accept canonical IDs without legacy market_id.",
    strict=True,
)
def test_market_slug_is_optional_display_only_and_not_required_for_routing(
    model: type[Any], payload_factory: Any
) -> None:
    """market_slug may vary or be omitted without changing canonical routing identity."""
    without_slug = payload_factory()
    without_slug.update(CANONICAL_IDS)
    without_slug.pop("market_id", None)

    with_slug = deepcopy(without_slug)
    with_slug["market_slug"] = DISPLAY_MARKET_SLUG

    event_without_slug = model.model_validate(without_slug)
    event_with_slug = model.model_validate(with_slug)

    assert _canonical_route(event_without_slug) == _canonical_route(event_with_slug)
    assert _canonical_route(event_with_slug) == (
        CANONICAL_IDS["condition_id"],
        CANONICAL_IDS["token_id"],
        CANONICAL_IDS["outcome"],
    )


def _canonical_route(event: Any) -> tuple[str, str, str]:
    """Target routing identity; intentionally excludes market_id and market_slug."""
    return (event.condition_id, event.token_id, event.outcome)


def test_signal_scores_fixture_still_matches_current_model_contract() -> None:
    """Keep the SignalEvent/TradeProposal fixtures honest while canonical tests are xfail."""
    scores = SignalScores.model_validate(_score_payload())

    assert scores.lead_lag == pytest.approx(0.8)


@pytest.mark.skipif(
    not hasattr(events, "ExecutionRequest"),
    reason="ExecutionRequest model does not exist yet; add the same canonical-id tests when it is introduced.",
)
@pytest.mark.xfail(
    reason="ExecutionRequest canonical contract is a test plan until the model exists and is migrated.",
    strict=True,
)
def test_execution_request_requires_canonical_ids_when_model_exists() -> None:
    """ExecutionRequest must require condition_id, token_id, and outcome once introduced."""
    model = events.ExecutionRequest
    payload = {
        "schema_version": 1,
        "event_type": "execution_request",
        "execution_id": "exec-1",
        "proposal_id": "proposal-1",
        "signal_id": "sig-1",
        "side": "BUY",
        "size_usdc": 25.0,
        "limit_price": 0.64,
        **CANONICAL_IDS,
    }

    for field in CANONICAL_IDS:
        invalid = dict(payload)
        invalid.pop(field)
        with pytest.raises(ValidationError):
            model.model_validate(invalid)
