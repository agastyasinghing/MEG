"""
Tests for meg.agent_core.signal_aggregator — pure router.

Tests cover:
  - Valid signal → routed to decision_agent.evaluate()
  - Malformed JSON → logged and skipped
  - Expired signal (TTL) → logged and skipped
  - Duplicate signal (seen set) → logged and skipped
  - decision_agent exception → logged and skipped (never crash)
"""
from __future__ import annotations

import json
import time
from unittest.mock import AsyncMock, patch

import pytest

from meg.agent_core import signal_aggregator
from meg.core.events import SignalEvent, SignalScores

from .conftest import make_signal_event


# ── _validate_and_route ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_valid_signal_routes_to_decision_agent(mock_redis, test_config, db_session):
    """Valid signal → decision_agent.evaluate() called."""
    signal = make_signal_event(signal_id="sig_route1")
    raw = signal.model_dump_json()

    # Clear dedup set for test isolation
    signal_aggregator._seen_signal_ids.clear()

    with patch(
        "meg.agent_core.signal_aggregator.decision_agent.evaluate",
        new_callable=AsyncMock,
    ) as mock_eval:
        await signal_aggregator._validate_and_route(
            raw, mock_redis, test_config, db_session
        )

    mock_eval.assert_called_once()
    call_args = mock_eval.call_args
    assert call_args[0][0].signal_id == "sig_route1"


@pytest.mark.asyncio
async def test_malformed_json_skipped(mock_redis, test_config, db_session):
    """Malformed JSON → skipped, no exception raised."""
    signal_aggregator._seen_signal_ids.clear()

    with patch(
        "meg.agent_core.signal_aggregator.decision_agent.evaluate",
        new_callable=AsyncMock,
    ) as mock_eval:
        await signal_aggregator._validate_and_route(
            "not-valid-json{{{", mock_redis, test_config, db_session
        )

    mock_eval.assert_not_called()


@pytest.mark.asyncio
async def test_expired_signal_skipped(mock_redis, test_config, db_session):
    """Signal with expired TTL → skipped."""
    signal_aggregator._seen_signal_ids.clear()

    # Signal expired 1 hour ago
    expired_ms = int(time.time() * 1000) - 3_600_000
    signal = make_signal_event(signal_id="sig_expired", ttl_expires_at_ms=expired_ms)
    raw = signal.model_dump_json()

    with patch(
        "meg.agent_core.signal_aggregator.decision_agent.evaluate",
        new_callable=AsyncMock,
    ) as mock_eval:
        await signal_aggregator._validate_and_route(
            raw, mock_redis, test_config, db_session
        )

    mock_eval.assert_not_called()


@pytest.mark.asyncio
async def test_duplicate_signal_skipped(mock_redis, test_config, db_session):
    """Same signal_id received twice → second is skipped."""
    signal_aggregator._seen_signal_ids.clear()

    signal = make_signal_event(signal_id="sig_dedup")
    raw = signal.model_dump_json()

    with patch(
        "meg.agent_core.signal_aggregator.decision_agent.evaluate",
        new_callable=AsyncMock,
    ) as mock_eval:
        # First call — should route
        await signal_aggregator._validate_and_route(
            raw, mock_redis, test_config, db_session
        )
        # Second call — should skip
        await signal_aggregator._validate_and_route(
            raw, mock_redis, test_config, db_session
        )

    assert mock_eval.call_count == 1


@pytest.mark.asyncio
async def test_decision_agent_exception_caught(mock_redis, test_config, db_session):
    """Exception in decision_agent.evaluate() → logged, not re-raised."""
    signal_aggregator._seen_signal_ids.clear()

    signal = make_signal_event(signal_id="sig_err")
    raw = signal.model_dump_json()

    with patch(
        "meg.agent_core.signal_aggregator.decision_agent.evaluate",
        new_callable=AsyncMock,
        side_effect=RuntimeError("decision agent exploded"),
    ):
        # Should not raise
        await signal_aggregator._validate_and_route(
            raw, mock_redis, test_config, db_session
        )


@pytest.mark.asyncio
async def test_no_session_logs_warning(mock_redis, test_config):
    """No DB session provided → logs warning, does not route."""
    signal_aggregator._seen_signal_ids.clear()

    signal = make_signal_event(signal_id="sig_nosess")
    raw = signal.model_dump_json()

    with patch(
        "meg.agent_core.signal_aggregator.decision_agent.evaluate",
        new_callable=AsyncMock,
    ) as mock_eval:
        await signal_aggregator._validate_and_route(
            raw, mock_redis, test_config, session=None
        )

    mock_eval.assert_not_called()


@pytest.mark.asyncio
async def test_dedup_set_bounded(mock_redis, test_config, db_session):
    """Dedup set doesn't grow beyond _MAX_SEEN_SIGNALS."""
    signal_aggregator._seen_signal_ids.clear()

    # Add MAX_SEEN_SIGNALS + 100 entries
    for i in range(signal_aggregator._MAX_SEEN_SIGNALS + 100):
        signal_aggregator._seen_signal_ids.add(f"sig_{i}")

    # Validate a new signal — should trigger pruning
    signal = make_signal_event(signal_id="sig_bounded")
    raw = signal.model_dump_json()

    with patch(
        "meg.agent_core.signal_aggregator.decision_agent.evaluate",
        new_callable=AsyncMock,
    ):
        await signal_aggregator._validate_and_route(
            raw, mock_redis, test_config, db_session
        )

    assert len(signal_aggregator._seen_signal_ids) <= signal_aggregator._MAX_SEEN_SIGNALS + 1

    # Cleanup
    signal_aggregator._seen_signal_ids.clear()


@pytest.mark.asyncio
async def test_ttl_zero_treated_as_no_expiry(mock_redis, test_config, db_session):
    """Signal with ttl_expires_at_ms=0 → no TTL check, routed normally."""
    signal_aggregator._seen_signal_ids.clear()

    signal = make_signal_event(signal_id="sig_ttl0", ttl_expires_at_ms=0)
    raw = signal.model_dump_json()

    with patch(
        "meg.agent_core.signal_aggregator.decision_agent.evaluate",
        new_callable=AsyncMock,
    ) as mock_eval:
        await signal_aggregator._validate_and_route(
            raw, mock_redis, test_config, db_session
        )

    mock_eval.assert_called_once()
