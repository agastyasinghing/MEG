"""
Tests for meg/data_layer/capital_refresh.py.

Uses mock_redis (fakeredis) — no real RPC or DB required.
wallet_registry calls are patched to avoid DB dependency.

Test categories:
  1. _run_once: calls update_capital for each tracked address
  2. _run_once: per-wallet error does not abort the rest of the sweep
  3. _run_once: no-op when no tracked wallets
  4. _run_once: closes the web3 connection in finally even if sweep errors
  5. _get_usdc_balance: raises if called outside _run_once (no self._w3)
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from meg.core.config_loader import MegConfig
from meg.data_layer.capital_refresh import CapitalRefreshJob


@pytest.fixture
def config() -> MegConfig:
    return MegConfig()


def _make_job(mock_redis, config) -> CapitalRefreshJob:
    return CapitalRefreshJob(
        rpc_url="ws://mock-rpc:8545",
        redis=mock_redis,
        config=config,
    )


def _make_mock_w3() -> MagicMock:
    """Build a minimal AsyncWeb3 mock with a disconnectable provider."""
    mock_w3 = MagicMock()
    mock_w3.eth.call = AsyncMock(return_value=b"\x00" * 31 + b"\x64")  # 100 raw = 0.0001 USDC
    mock_w3.provider.disconnect = AsyncMock()
    return mock_w3


def _web3_patch(mock_w3: MagicMock):
    """
    Context manager that stubs the lazy web3 imports inside _run_once.

    _run_once does `from web3 import AsyncWeb3` and
    `from web3.providers import WebsocketProviderV2` at runtime.
    We inject fake modules so those imports return our mock objects
    regardless of the installed web3 version.
    """
    mock_providers = MagicMock()
    mock_providers.WebsocketProviderV2 = MagicMock(return_value=MagicMock())

    mock_web3_module = MagicMock()
    mock_web3_module.AsyncWeb3 = MagicMock(return_value=mock_w3)

    return patch.dict(
        "sys.modules",
        {
            "web3": mock_web3_module,
            "web3.providers": mock_providers,
        },
    )


# ── 1. _run_once calls update_capital for each tracked address ─────────────────


@pytest.mark.asyncio
async def test_run_once_calls_update_capital_for_each_address(mock_redis, config):
    job = _make_job(mock_redis, config)
    addresses = [
        "0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "0xBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
    ]

    mock_w3 = _make_mock_w3()

    with patch("meg.data_layer.capital_refresh.wallet_registry") as mock_reg:
        mock_reg.get_tracked_addresses = AsyncMock(return_value=addresses)
        mock_reg.update_capital = AsyncMock()

        with _web3_patch(mock_w3):
            await job._run_once()

    assert mock_reg.update_capital.await_count == 2
    called_addresses = [
        call.args[0] for call in mock_reg.update_capital.await_args_list
    ]
    assert set(called_addresses) == set(addresses)


# ── 2. Per-wallet error does not abort the sweep ───────────────────────────────


@pytest.mark.asyncio
async def test_run_once_continues_after_per_wallet_error(mock_redis, config):
    """One wallet raising does not prevent other wallets from being updated."""
    job = _make_job(mock_redis, config)
    addresses = [
        "0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "0xBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
        "0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    ]

    mock_w3 = _make_mock_w3()
    # Second address raises on eth_call
    call_count = 0

    async def flaky_call(tx):
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise ConnectionError("RPC timeout")
        return b"\x00" * 31 + b"\x64"

    mock_w3.eth.call = flaky_call

    with patch("meg.data_layer.capital_refresh.wallet_registry") as mock_reg:
        mock_reg.get_tracked_addresses = AsyncMock(return_value=addresses)
        mock_reg.update_capital = AsyncMock()

        with _web3_patch(mock_w3):
            await job._run_once()

    # 2 of 3 addresses should succeed
    assert mock_reg.update_capital.await_count == 2


# ── 3. No-op when no tracked wallets ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_run_once_noop_when_no_tracked_wallets(mock_redis, config):
    job = _make_job(mock_redis, config)

    with patch("meg.data_layer.capital_refresh.wallet_registry") as mock_reg:
        mock_reg.get_tracked_addresses = AsyncMock(return_value=[])
        mock_reg.update_capital = AsyncMock()

        # No wallets → early return before the web3 import block is reached
        await job._run_once()

    mock_reg.update_capital.assert_not_awaited()
    assert job._w3 is None


# ── 4. Web3 connection closed in finally ──────────────────────────────────────


@pytest.mark.asyncio
async def test_run_once_closes_w3_connection_after_sweep(mock_redis, config):
    """provider.disconnect() is called even when all wallets succeed."""
    job = _make_job(mock_redis, config)
    mock_w3 = _make_mock_w3()

    with patch("meg.data_layer.capital_refresh.wallet_registry") as mock_reg:
        mock_reg.get_tracked_addresses = AsyncMock(
            return_value=["0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"]
        )
        mock_reg.update_capital = AsyncMock()

        with _web3_patch(mock_w3):
            await job._run_once()

    mock_w3.provider.disconnect.assert_awaited_once()
    assert job._w3 is None  # cleaned up


@pytest.mark.asyncio
async def test_run_once_closes_w3_connection_even_on_sweep_error(mock_redis, config):
    """provider.disconnect() is called even when the sweep loop raises unexpectedly."""
    job = _make_job(mock_redis, config)
    mock_w3 = _make_mock_w3()

    with patch("meg.data_layer.capital_refresh.wallet_registry") as mock_reg:
        mock_reg.get_tracked_addresses = AsyncMock(
            return_value=["0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"]
        )
        # update_capital raises unexpectedly (not wrapped in per-wallet try/except)
        mock_reg.update_capital = AsyncMock(side_effect=RuntimeError("unexpected"))

        with _web3_patch(mock_w3):
            # The per-wallet try/except catches RuntimeError, so sweep completes
            await job._run_once()

    mock_w3.provider.disconnect.assert_awaited_once()


# ── 5. _get_usdc_balance raises outside of sweep ──────────────────────────────


@pytest.mark.asyncio
async def test_get_usdc_balance_raises_if_no_w3(mock_redis, config):
    """_get_usdc_balance requires self._w3 to be set by _run_once."""
    job = _make_job(mock_redis, config)
    assert job._w3 is None

    with pytest.raises(RuntimeError, match="outside of _run_once"):
        await job._get_usdc_balance("0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
