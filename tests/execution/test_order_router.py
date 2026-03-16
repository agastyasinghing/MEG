"""
Tests for meg/execution/order_router.py

Covered:
  place():
    - entry_filter rejects      → accepted=False, order_id=None, slippage=0.0
    - slippage_guard rejects    → accepted=False, order_id=None, slippage from guard
    - paper mode happy path     → accepted=True, order_id set, open_position called
    - correct kwargs forwarded  → open_position receives market_id, outcome, size_usdc,
                                   entry_price, signal_id, contributing_wallets
    - transport error attempt 1 → retry, succeed attempt 2; backoff=1s asserted
    - transport errors 1+2      → retry, succeed attempt 3; backoffs [1s, 2s] asserted
    - all 3 retries exhausted   → re-raises; backoffs [1s, 2s] asserted
    - non-transport error       → re-raises immediately; no retry, no sleep

All tests mock at the module boundary (meg.execution.order_router.*) so that
entry_filter, slippage_guard, clob_client, and position_manager can be tested
independently in their own test files.
"""
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, call, patch

import pytest
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.execution import order_router
from tests.execution.conftest import make_proposal

# Patch paths — these must match the import names used inside order_router.py
_PATCH_EF = "meg.execution.order_router.entry_filter.check"
_PATCH_SG = "meg.execution.order_router.slippage_guard.check"
_PATCH_PO = "meg.execution.order_router.clob_client.place_order"
_PATCH_OP = "meg.execution.order_router.position_manager.open_position"
_PATCH_SLEEP = "meg.execution.order_router.asyncio.sleep"


class TestPlaceGateRejections:
    async def test_entry_filter_rejects_returns_accepted_false(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        proposal = make_proposal()
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(False, "entry_distance_exceeded: ..."))) as mock_ef,
            patch(_PATCH_PO, new=AsyncMock()) as mock_place,
        ):
            result = await order_router.place(proposal, mock_redis, test_config)

        assert result["accepted"] is False
        assert "entry_distance_exceeded" in result["reason"]
        assert result["order_id"] is None
        assert result["estimated_slippage"] == pytest.approx(0.0)
        mock_place.assert_not_called()

    async def test_slippage_guard_rejects_returns_accepted_false(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        proposal = make_proposal()
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(True, ""))),
            patch(_PATCH_SG, new=AsyncMock(return_value=(False, "spread_too_wide: ...", 0.03))),
            patch(_PATCH_PO, new=AsyncMock()) as mock_place,
        ):
            result = await order_router.place(proposal, mock_redis, test_config)

        assert result["accepted"] is False
        assert "spread_too_wide" in result["reason"]
        assert result["order_id"] is None
        assert result["estimated_slippage"] == pytest.approx(0.03)
        mock_place.assert_not_called()


class TestPlaceHappyPath:
    async def test_paper_mode_returns_accepted_true(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        proposal = make_proposal()
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(True, ""))),
            patch(_PATCH_SG, new=AsyncMock(return_value=(True, "", 0.01))),
            patch(_PATCH_PO, new=AsyncMock(return_value="PAPER_abc123")) as mock_place,
            patch(_PATCH_OP, new=AsyncMock()) as mock_open_pos,
        ):
            result = await order_router.place(proposal, mock_redis, test_config)

        assert result["accepted"] is True
        assert result["reason"] == ""
        assert result["order_id"] == "PAPER_abc123"
        assert result["estimated_slippage"] == pytest.approx(0.01)
        mock_place.assert_called_once()
        mock_open_pos.assert_called_once()

    async def test_open_position_called_with_correct_kwargs(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        proposal = make_proposal(
            market_id="mkt_xyz",
            outcome="YES",
            size_usdc=200.0,
            limit_price=0.50,
            signal_id="sig_abc",
            contributing_wallets=["0xWHALE1", "0xWHALE2"],
        )
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(True, ""))),
            patch(_PATCH_SG, new=AsyncMock(return_value=(True, "", 0.01))),
            patch(_PATCH_PO, new=AsyncMock(return_value="PAPER_xyz")),
            patch(_PATCH_OP, new=AsyncMock()) as mock_open_pos,
        ):
            await order_router.place(proposal, mock_redis, test_config)

        kwargs = mock_open_pos.call_args.kwargs
        assert kwargs["market_id"] == "mkt_xyz"
        assert kwargs["outcome"] == "YES"
        assert kwargs["size_usdc"] == pytest.approx(200.0)
        assert kwargs["entry_price"] == pytest.approx(0.50)
        assert kwargs["signal_id"] == "sig_abc"
        assert kwargs["contributing_wallets"] == ["0xWHALE1", "0xWHALE2"]
        assert kwargs["redis"] is mock_redis
        assert kwargs["session"] is None  # default when not passed

    async def test_no_outcome_tp_sl_direction(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # For NO outcome: take_profit_price < entry_price, stop_loss_price > entry_price
        proposal = make_proposal(outcome="NO", limit_price=0.40)
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(True, ""))),
            patch(_PATCH_SG, new=AsyncMock(return_value=(True, "", 0.01))),
            patch(_PATCH_PO, new=AsyncMock(return_value="PAPER_no")),
            patch(_PATCH_OP, new=AsyncMock()) as mock_open_pos,
        ):
            await order_router.place(proposal, mock_redis, test_config)

        kwargs = mock_open_pos.call_args.kwargs
        entry = kwargs["entry_price"]  # 0.40
        # NO: TP when YES falls (TP price < entry), SL when YES rises (SL price > entry)
        assert kwargs["take_profit_price"] < entry
        assert kwargs["stop_loss_price"] > entry


class TestPlaceRetryLogic:
    async def test_transport_error_retries_and_succeeds_attempt_2(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        mock_place = AsyncMock(side_effect=[ConnectionError(), "PAPER_success"])
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(True, ""))),
            patch(_PATCH_SG, new=AsyncMock(return_value=(True, "", 0.01))),
            patch(_PATCH_PO, new=mock_place),
            patch(_PATCH_OP, new=AsyncMock()),
            patch(_PATCH_SLEEP, new=AsyncMock()) as mock_sleep,
        ):
            result = await order_router.place(make_proposal(), mock_redis, test_config)

        assert result["accepted"] is True
        assert result["order_id"] == "PAPER_success"
        assert mock_place.call_count == 2
        mock_sleep.assert_called_once_with(1)  # 2^0 = 1s after attempt 0

    async def test_two_transport_errors_then_success_attempt_3(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        mock_place = AsyncMock(
            side_effect=[ConnectionError(), ConnectionError(), "PAPER_third"]
        )
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(True, ""))),
            patch(_PATCH_SG, new=AsyncMock(return_value=(True, "", 0.01))),
            patch(_PATCH_PO, new=mock_place),
            patch(_PATCH_OP, new=AsyncMock()),
            patch(_PATCH_SLEEP, new=AsyncMock()) as mock_sleep,
        ):
            result = await order_router.place(make_proposal(), mock_redis, test_config)

        assert result["accepted"] is True
        assert result["order_id"] == "PAPER_third"
        assert mock_place.call_count == 3
        assert mock_sleep.call_args_list == [call(1), call(2)]  # 2^0, 2^1

    async def test_all_retries_exhausted_reraises(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        mock_place = AsyncMock(
            side_effect=[OSError("conn refused"), OSError(), OSError()]
        )
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(True, ""))),
            patch(_PATCH_SG, new=AsyncMock(return_value=(True, "", 0.01))),
            patch(_PATCH_PO, new=mock_place),
            patch(_PATCH_SLEEP, new=AsyncMock()) as mock_sleep,
        ):
            with pytest.raises(OSError):
                await order_router.place(make_proposal(), mock_redis, test_config)

        assert mock_place.call_count == 3
        assert mock_sleep.call_args_list == [call(1), call(2)]  # 2^0, 2^1

    async def test_timeout_error_reraises_immediately_no_retry(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # asyncio.TimeoutError is NOT in _RETRYABLE — excluded to prevent duplicate
        # CLOB orders when a read/response timeout fires after the order was accepted.
        mock_place = AsyncMock(side_effect=asyncio.TimeoutError())
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(True, ""))),
            patch(_PATCH_SG, new=AsyncMock(return_value=(True, "", 0.01))),
            patch(_PATCH_PO, new=mock_place),
            patch(_PATCH_SLEEP, new=AsyncMock()) as mock_sleep,
        ):
            with pytest.raises(asyncio.TimeoutError):
                await order_router.place(make_proposal(), mock_redis, test_config)

        assert mock_place.call_count == 1
        mock_sleep.assert_not_called()

    async def test_non_transport_error_reraises_immediately_no_retry(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # ValueError is not in _RETRYABLE → re-raise immediately, no sleep
        mock_place = AsyncMock(side_effect=ValueError("bad request from CLOB"))
        with (
            patch(_PATCH_EF, new=AsyncMock(return_value=(True, ""))),
            patch(_PATCH_SG, new=AsyncMock(return_value=(True, "", 0.01))),
            patch(_PATCH_PO, new=mock_place),
            patch(_PATCH_SLEEP, new=AsyncMock()) as mock_sleep,
        ):
            with pytest.raises(ValueError, match="bad request"):
                await order_router.place(make_proposal(), mock_redis, test_config)

        assert mock_place.call_count == 1
        mock_sleep.assert_not_called()
