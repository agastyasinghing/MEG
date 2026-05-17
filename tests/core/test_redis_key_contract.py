"""Redis key contract tests for Phase 0A canonical routing.

The target contract is documented before production Redis key builders are
migrated: token-scoped market-state/book keys, condition/outcome-scoped
cross-token semantics, and no routing by legacy ``market_id`` or display slug.
"""
from __future__ import annotations

import inspect

import pytest

from meg.core.events import RedisKeys

CONDITION_ID = "0xcondition000000000000000000000000000000000000000000000000000000000001"
TOKEN_ID = "1234567890123456789012345678901234567890"
OUTCOME = "YES"
MARKET_SLUG = "will-btc-be-above-120k-on-june-30"
LEGACY_MARKET_ID = "legacy-market-id-must-not-route"


def test_redis_key_builders_do_not_route_on_market_slug() -> None:
    """Display slugs must not appear in Redis routing key builder signatures."""
    for name, member in inspect.getmembers(RedisKeys, predicate=inspect.isfunction):
        signature = inspect.signature(member)
        assert "market_slug" not in signature.parameters, name
        assert "slug" not in signature.parameters, name


@pytest.mark.xfail(
    reason="RedisKeys still exposes market_id-scoped market-state builders until the 0A-03 migration.",
    strict=True,
)
def test_market_state_keys_are_token_scoped_after_migration() -> None:
    """Target market-state keys are token scoped, not market:{market_id}:..."""
    assert RedisKeys.market_state(TOKEN_ID) == f"market:{TOKEN_ID}:state"
    assert RedisKeys.market_book(TOKEN_ID) == f"market:{TOKEN_ID}:book"

    forbidden_key = f"market:{LEGACY_MARKET_ID}:state"
    assert RedisKeys.market_state(TOKEN_ID) != forbidden_key


@pytest.mark.xfail(
    reason="Consensus windows currently accept market_id; target contract scopes them by condition_id and outcome.",
    strict=True,
)
def test_consensus_window_uses_condition_id_and_outcome_after_migration() -> None:
    """Cross-token consensus semantics should be keyed by condition and outcome."""
    key = RedisKeys.consensus_window(condition_id=CONDITION_ID, outcome=OUTCOME)

    assert CONDITION_ID in key
    assert OUTCOME in key
    assert TOKEN_ID not in key
    assert LEGACY_MARKET_ID not in key
    assert MARKET_SLUG not in key


@pytest.mark.xfail(
    reason="Market exposure keys currently accept market_id; target contract uses condition/token/outcome semantics.",
    strict=True,
)
def test_exposure_keys_use_canonical_identity_after_migration() -> None:
    """Exposure must use explicit canonical granularity instead of market_id."""
    token_key = RedisKeys.token_exposure_usdc(TOKEN_ID)
    outcome_key = RedisKeys.outcome_exposure_usdc(CONDITION_ID, OUTCOME)

    assert token_key == f"token:{TOKEN_ID}:exposure_usdc"
    assert outcome_key == f"condition:{CONDITION_ID}:outcome:{OUTCOME}:exposure_usdc"
    assert LEGACY_MARKET_ID not in token_key
    assert LEGACY_MARKET_ID not in outcome_key
