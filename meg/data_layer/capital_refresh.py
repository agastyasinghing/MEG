"""
Daily capital refresh job.

Queries Polygon RPC for the USDC balance of every tracked whale wallet,
and writes total_capital_usdc to the wallet registry (DB + Redis).

Capital is required for the conviction ratio calculation:
  conviction_ratio = trade_size_usdc / total_capital_usdc

Without an up-to-date capital value, conviction_ratio defaults to 0, which
sets its sub-score to 0 and reduces the composite signal score.

Schedule: run once per day via asyncio task sleep loop.
The job is started by the main entrypoint alongside polygon_feed and CLOBMarketFeed.

Data flow:
  wallet_registry.get_tracked_addresses()
    └─► for each address:
          Polygon RPC → USDC balanceOf(address)
          wallet_registry.update_capital(address, balance, redis)
              └─► PostgreSQL UPDATE wallets SET total_capital_usdc = ...
              └─► Redis INVALIDATE wallet:{address}:data
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

import structlog
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.data_layer import wallet_registry

logger = structlog.get_logger(__name__)

# USDC token contract on Polygon (ERC-20)
USDC_CONTRACT_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

# USDC has 6 decimal places
USDC_DECIMALS = 6

# How often to refresh capital (seconds). 86400 = 24 hours.
_REFRESH_INTERVAL_SECONDS = 86_400

# ERC-20 balanceOf function selector: keccak256("balanceOf(address)")[:4]
_BALANCE_OF_SELECTOR = "0x70a08231"


class CapitalRefreshJob:
    """
    Daily job: query USDC balance for all tracked wallets via Polygon RPC,
    write total_capital_usdc to wallet registry.

    A single AsyncWeb3 connection is created once per sweep (not per wallet)
    to avoid opening/leaking hundreds of websocket connections per run.

    Usage:
        job = CapitalRefreshJob(rpc_url, redis, config)
        asyncio.create_task(job.run())
    """

    def __init__(
        self,
        rpc_url: str,
        redis: Redis,
        config: MegConfig,
    ) -> None:
        self._rpc_url = rpc_url
        self._redis = redis
        self._config = config
        self._w3: Any | None = None  # AsyncWeb3 — created once per sweep

    async def run(self) -> None:
        """
        Run forever: refresh all tracked wallet capitals once per day.
        Sleeps _REFRESH_INTERVAL_SECONDS between full sweeps.
        Logs errors per-wallet and continues — never crashes the whole job.
        """
        logger.info(
            "capital_refresh.started",
            interval_hours=_REFRESH_INTERVAL_SECONDS / 3600,
        )
        while True:
            await self._run_once()
            await asyncio.sleep(_REFRESH_INTERVAL_SECONDS)

    async def _run_once(self) -> None:
        """
        Fetch and update capital for all tracked wallet addresses.
        Any failure on a single wallet is logged and skipped.

        A single web3 connection is created for the sweep and reused across
        all wallet calls — avoids opening one websocket per wallet.
        """
        started_at = datetime.now(tz=timezone.utc)
        logger.info("capital_refresh.sweep_started", started_at=started_at.isoformat())

        addresses = await wallet_registry.get_tracked_addresses(self._redis)
        if not addresses:
            logger.info("capital_refresh.no_tracked_wallets")
            return

        # Create one connection for the whole sweep; reused by _get_usdc_balance.
        from web3 import AsyncWeb3
        from web3.providers import WebsocketProviderV2

        self._w3 = AsyncWeb3(WebsocketProviderV2(self._rpc_url))

        success_count = 0
        error_count = 0

        try:
            for address in addresses:
                try:
                    balance_usdc = await self._get_usdc_balance(address)
                    await wallet_registry.update_capital(address, balance_usdc, self._redis)
                    success_count += 1
                except Exception as exc:
                    error_count += 1
                    logger.warning(
                        "capital_refresh.wallet_failed",
                        address=address,
                        error=str(exc),
                    )
        finally:
            # Always close the connection regardless of errors.
            try:
                await self._w3.provider.disconnect()
            except Exception:
                pass
            self._w3 = None

        logger.info(
            "capital_refresh.sweep_complete",
            total=len(addresses),
            success=success_count,
            errors=error_count,
            duration_seconds=(
                datetime.now(tz=timezone.utc) - started_at
            ).total_seconds(),
        )

    async def _get_usdc_balance(self, address: str) -> float:
        """
        Call ERC-20 balanceOf(address) on the USDC contract via Polygon RPC.
        Returns USDC balance as a float with human-readable units (not wei).

        Uses web3.py's eth_call (read-only, no gas cost).
        Requires self._w3 to be set (done by _run_once before calling this).
        """
        if self._w3 is None:
            raise RuntimeError("_get_usdc_balance called outside of _run_once sweep")

        # ABI-encode balanceOf(address): selector + left-padded address (32 bytes)
        padded_address = address.lower().replace("0x", "").zfill(64)
        call_data = f"{_BALANCE_OF_SELECTOR}{padded_address}"

        result = await self._w3.eth.call(
            {
                "to": USDC_CONTRACT_ADDRESS,
                "data": call_data,
            }
        )

        # Result is a 32-byte hex string representing the uint256 balance
        balance_raw = int(result.hex(), 16)
        balance_usdc = balance_raw / (10 ** USDC_DECIMALS)
        return balance_usdc
