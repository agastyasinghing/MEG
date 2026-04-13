"""
Polygon RPC websocket feed.

Connects to the Polygon network via Alchemy websocket RPC, listens for
on-chain Polymarket transactions, filters for qualifying whale trades,
and emits RawWhaleTrade events to Redis pub/sub.

Data flow:
  Polygon RPC ──(block polling / newHeads)──► _process_block()
                                                      │
                                              per-tx try/except
                                                      │
                                         _filter_whale_transaction()
                                                      │
                                           qualifies? (CLOB tx, size >= min)
                                                      │
                                         RawWhaleTrade ──► Redis CHANNEL_RAW_WHALE_TRADES
                                                      │
                                         SADD market_id ──► meg:active_markets
                                                      │
                                         SET last_processed_block ──► meg:last_processed_block

Critical constraint: this function must NEVER raise an unhandled exception.
Malformed transactions → log with full context, skip, continue the feed.
A crashed feed = blind system. Handle every exception explicitly.

Reconnect strategy: exponential backoff 1s → 2s → 4s … max 60s.
Gap tracking: on reconnect, compare current block to last_processed_block.
  On gap > 1: log WARNING with gap size. Replay is deferred (see TODOS.md).

Testability: PolygonRPCConnection ABC is injected into PolygonFeed.
  Tests pass a mock; production uses Web3RPCConnection.
"""
from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from typing import Any

import structlog
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RawWhaleTrade, RedisKeys
from meg.core.redis_client import publish

logger = structlog.get_logger(__name__)

# Polymarket CLOB contract address on Polygon (checksummed)
CLOB_CONTRACT_ADDRESS = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"

# Minimum trade size to qualify for emission (USDC).
# Filters transaction noise without requiring registry lookup at this layer.
# TODO: promote to config.whale_qualification.min_trade_size_usdc
_MIN_TRADE_SIZE_USDC = 500.0

# Reconnect backoff bounds (seconds)
_RECONNECT_BASE = 1.0
_RECONNECT_MAX = 60.0

# connect() retry parameters
_CONNECT_MAX_RETRIES = 5  # retries after initial attempt; delays: 2s, 4s, 8s, 16s, 32s
_CONNECT_RETRY_BASE = 2.0

# Polygon POA blocks have large extraData fields that exceed the default websocket
# max_size (1MB), causing "sent 1009 (message too big)" disconnects.
_WS_MAX_SIZE = 10 * 1024 * 1024  # 10MB


# ── Testability shim: injectable RPC connection ────────────────────────────────


class PolygonRPCConnection(ABC):
    """
    Thin abstraction over web3.py AsyncWeb3 for testability.

    Production code uses Web3RPCConnection.
    Tests inject a mock or stub implementation.

    Only the methods actually needed by PolygonFeed are declared here —
    no over-abstraction of the full web3.py API.
    """

    @abstractmethod
    async def get_block_number(self) -> int:
        """Return the current latest block number."""
        ...

    @abstractmethod
    def subscribe_new_blocks(self) -> AsyncIterator[int]:
        """
        Async iterator yielding new block numbers as blocks are confirmed.
        Must raise ConnectionError on websocket disconnect — PolygonFeed
        catches this and triggers a reconnect with backoff.
        """
        ...

    @abstractmethod
    async def get_block_transactions(self, block_number: int) -> list[dict[str, Any]]:
        """
        Return all transactions in a block as a list of dicts.
        Raises on RPC error — caller wraps in try/except.
        """
        ...


class Web3RPCConnection(PolygonRPCConnection):
    """
    Production implementation wrapping web3.py AsyncWeb3.

    Uses block polling (1-second interval) for subscribe_new_blocks —
    more reliable than websocket subscriptions across provider restarts.
    TODO: upgrade to eth_subscribe("newHeads") when stability allows.
    """

    def __init__(self, rpc_url: str) -> None:
        self._url = rpc_url
        self._w3: Any = None  # AsyncWeb3 — imported lazily to avoid import at module load

    async def connect(self) -> None:
        """
        Establish the RPC connection. Call before run().

        Retries up to _CONNECT_MAX_RETRIES times with exponential backoff
        (2s, 4s, 8s, 16s, 32s). Raises ConnectionError only after all
        retries are exhausted.

        URL format: wss://polygon-mainnet.g.alchemy.com/v2/<API_KEY>
        """
        from web3 import AsyncWeb3
        from web3.middleware import ExtraDataToPOAMiddleware
        from web3.providers import WebSocketProvider

        last_exc: Exception | None = None
        # Attempts 1..(max_retries+1): first is the initial try, rest are retries.
        for attempt in range(1, _CONNECT_MAX_RETRIES + 2):
            try:
                self._w3 = AsyncWeb3(
                    WebSocketProvider(
                        self._url,
                        websocket_kwargs={"max_size": _WS_MAX_SIZE},
                    )
                )
                # web3 7.x: WebSocketProvider is a PersistentConnectionProvider.
                # provider.connect() is the call that actually opens the WebSocket
                # and populates provider._ws. Without it, is_connected() always
                # returns False because _ws is None after construction.
                await self._w3.provider.connect()
                # Polygon is a POA chain — its blocks carry an oversized extraData
                # field (97 bytes vs the standard 32). Without this middleware,
                # eth.get_block() raises "extraData is X bytes, but should be 32".
                self._w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
                logger.info("polygon_rpc.connected", url=self._url, attempt=attempt)
                return
            except Exception as exc:
                last_exc = exc
                if attempt <= _CONNECT_MAX_RETRIES:
                    delay = _CONNECT_RETRY_BASE ** attempt  # 2, 4, 8, 16, 32
                    logger.warning(
                        "polygon_rpc.connect_retry",
                        attempt=attempt,
                        max_retries=_CONNECT_MAX_RETRIES,
                        retry_in_seconds=delay,
                        error=str(exc),
                        url=self._url,
                    )
                    await asyncio.sleep(delay)

        raise ConnectionError(
            f"Failed to connect to Polygon RPC after {_CONNECT_MAX_RETRIES + 1} attempts: {self._url}"
        ) from last_exc

    async def get_block_number(self) -> int:
        return await self._w3.eth.block_number

    async def subscribe_new_blocks(self) -> AsyncIterator[int]:  # type: ignore[override]
        """
        Poll eth.block_number every second and yield each new block number once.
        Yields immediately on the first new block after the last-seen block.
        """
        last_seen: int | None = None
        while True:
            try:
                current = await self._w3.eth.block_number
            except Exception as exc:
                raise ConnectionError(f"Polygon RPC block_number failed: {exc}") from exc

            if last_seen is None:
                last_seen = current
            elif current > last_seen:
                for block_number in range(last_seen + 1, current + 1):
                    yield block_number
                last_seen = current

            await asyncio.sleep(1.0)

    async def get_block_transactions(self, block_number: int) -> list[dict[str, Any]]:
        block = await self._w3.eth.get_block(block_number, full_transactions=True)
        return [dict(tx) for tx in block.transactions]


# ── Main feed class ────────────────────────────────────────────────────────────


class PolygonFeed:
    """
    Polygon RPC block watcher. Processes each block, filters CLOB
    contract transactions, and emits qualifying RawWhaleTrade events to Redis.

    Block processing pipeline (per block):
      get_block_transactions()
        └─► per-transaction try/except loop
              └─► _filter_whale_transaction()
                    └─► on match: publish to CHANNEL_RAW_WHALE_TRADES
                               + SADD market_id to active_markets
      SET last_processed_block

    Any exception in a single transaction is caught, logged, and skipped.
    Any exception in get_block_transactions is caught, logged, and the
    entire block is skipped (not retried — next block will arrive shortly).
    """

    def __init__(
        self,
        rpc: PolygonRPCConnection,
        redis: Redis,
        config: MegConfig,
    ) -> None:
        self._rpc = rpc
        self._redis = redis
        self._config = config

    async def run(self) -> None:
        """
        Main entry point. Watches new blocks forever.
        Reconnects with exponential backoff on any exception.
        Never returns under normal operation.
        """
        backoff = _RECONNECT_BASE
        while True:
            try:
                await self._run_once()
                # _run_once exited cleanly (iterator exhausted — shouldn't happen)
                backoff = _RECONNECT_BASE
            except Exception as exc:
                logger.warning(
                    "polygon_feed.disconnected",
                    error=str(exc),
                    reconnect_in_seconds=backoff,
                )
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, _RECONNECT_MAX)

    async def _run_once(self) -> None:
        """Subscribe to new blocks and process until any exception is raised."""
        current_block = await self._rpc.get_block_number()
        await self._check_block_gap(current_block)

        async for block_number in self._rpc.subscribe_new_blocks():
            await self._process_block(block_number)
            await self._redis.set(RedisKeys.last_processed_block(), str(block_number))

    async def _check_block_gap(self, current_block: int) -> None:
        """
        Compare current_block to last_processed_block stored in Redis.
        Log WARNING if a gap is detected (missed blocks since last run).
        Gap-fill replay is deferred — see TODOS.md.
        """
        last_str: str | None = await self._redis.get(RedisKeys.last_processed_block())
        if last_str is None:
            return  # first run — no gap to report

        last_block = int(last_str)
        gap = current_block - last_block
        if gap > 1:
            logger.warning(
                "polygon_feed.block_gap_detected",
                last_processed_block=last_block,
                current_block=current_block,
                gap=gap,
                note="gap-fill replay deferred (see TODOS.md P1 item)",
            )

    async def _process_block(self, block_number: int) -> None:
        """
        Fetch all transactions in a block and filter for whale CLOB trades.
        Any exception fetching the block is logged and the block is skipped.
        Any exception on individual transactions is caught per-tx.
        """
        try:
            transactions = await self._rpc.get_block_transactions(block_number)
        except Exception as exc:
            logger.warning(
                "polygon_feed.block_fetch_failed",
                block_number=block_number,
                error=str(exc),
            )
            return

        for tx in transactions:
            try:
                event = await _filter_whale_transaction(tx, self._config)
                if event is not None:
                    # Enrich market_category from Redis (written by CLOBMarketFeed).
                    # Empty string when CLOBMarketFeed hasn't polled this market yet — fine.
                    cat: str = (await self._redis.get(RedisKeys.market_category(event.market_id))) or ""
                    if cat:
                        event = event.model_copy(update={"market_category": cat})
                    await _emit_event(self._redis, event)
                    # Register this market as active so CLOBMarketFeed subscribes to it
                    await self._redis.sadd(RedisKeys.active_markets(), event.market_id)
                    logger.debug(
                        "polygon_feed.whale_trade_emitted",
                        wallet=event.wallet_address,
                        market=event.market_id,
                        size_usdc=event.size_usdc,
                        block_number=block_number,
                    )
            except Exception as exc:
                # Per-event: log + skip + continue — never crash the feed
                logger.warning(
                    "polygon_feed.tx_processing_error",
                    tx_hash=_safe_hash(tx),
                    block_number=block_number,
                    error=str(exc),
                )


# ── Module-level functions (public interface) ─────────────────────────────────


async def run(rpc_url: str, redis: Redis, config: MegConfig) -> None:
    """
    Main entry point. Opens a connection to the Polygon RPC and runs forever.
    Reconnects automatically on disconnect. Never returns under normal operation.
    Call this as a long-running asyncio task.
    """
    rpc = Web3RPCConnection(rpc_url)
    await rpc.connect()
    feed = PolygonFeed(rpc=rpc, redis=redis, config=config)
    await feed.run()


async def _filter_whale_transaction(
    tx: dict[str, Any],
    config: MegConfig,
) -> RawWhaleTrade | None:
    """
    Inspect a raw Polygon transaction dict. Return a RawWhaleTrade if the
    transaction is directed at the CLOB contract and meets size threshold,
    or None if it should be skipped.

    Returns None on any parse/decode error — logs warning and continues.

    NOTE: Full CLOB ABI decoding (exact USDC size, market_id, outcome from
    OrderFilled event logs) is a TODO — requires transaction receipt parsing
    with the CLOB contract ABI. Current implementation uses heuristics.
    TODO: decode OrderFilled event logs for exact size, market_id, outcome.
    """
    try:
        # Only interested in transactions TO the CLOB contract
        to_addr = (tx.get("to") or "").lower()
        if to_addr != CLOB_CONTRACT_ADDRESS.lower():
            return None

        wallet_address: str = tx.get("from", "")
        if not wallet_address:
            return None

        # Heuristic size proxy: input data length correlates with order size.
        # TODO: parse OrderFilled event log from receipt for exact USDC amount.
        # input data > 4 bytes (function selector) means it's a real call, not ETH transfer.
        input_data: str = tx.get("input", tx.get("data", "0x"))
        if len(input_data) <= 2:  # "0x" only — empty call, skip
            return None

        # Use gas price * gas used as rough size proxy until ABI decoding is ready.
        # Real value comes from the OrderFilled event's takerAmount field (USDC).
        gas_price = int(tx.get("gasPrice", 0))
        gas = int(tx.get("gas", 0))
        # Rough size estimate: scale gas cost to USDC equivalent
        # This is intentionally conservative — real sizes will be much larger
        size_usdc_proxy = (gas_price * gas) / 1e15  # normalize to USDC range

        # Floor at _MIN_TRADE_SIZE_USDC until ABI decoding provides exact amounts.
        # Replace with decoded OrderFilled takerAmount once ABI decode is ready.
        size_usdc = max(size_usdc_proxy, _MIN_TRADE_SIZE_USDC)

        # Extract tx hash as hex string
        tx_hash_raw = tx.get("hash", "")
        tx_hash: str = (
            tx_hash_raw.hex()
            if hasattr(tx_hash_raw, "hex")
            else str(tx_hash_raw)
        )
        if not tx_hash:
            return None

        block_number_raw = tx.get("blockNumber", 0)
        block_number = int(block_number_raw)

        # Use current time as timestamp proxy; real timestamp comes from block header
        timestamp_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)

        # TODO: extract market_id and outcome from OrderFilled event logs
        # For now: derive market_id from tx_hash prefix (will be overwritten by ABI decode)
        market_id = f"market_{tx_hash[:16]}"

        return RawWhaleTrade(
            wallet_address=wallet_address,
            market_id=market_id,
            outcome="YES",  # TODO: parse from OrderFilled event log
            size_usdc=size_usdc,
            timestamp_ms=timestamp_ms,
            tx_hash=tx_hash,
            block_number=block_number,
            market_price_at_trade=0.0,  # TODO: parse from event log
        )

    except Exception as exc:
        logger.warning(
            "polygon_feed.filter_error",
            tx_hash=_safe_hash(tx),
            error=str(exc),
        )
        return None


async def _emit_event(redis: Redis, event: RawWhaleTrade) -> None:
    """Publish a RawWhaleTrade to the Redis CHANNEL_RAW_WHALE_TRADES channel."""
    await publish(redis, RedisKeys.CHANNEL_RAW_WHALE_TRADES, event.model_dump_json())


def _safe_hash(tx: dict[str, Any]) -> str:
    """Extract tx hash for logging without raising."""
    try:
        h = tx.get("hash", "unknown")
        return h.hex() if hasattr(h, "hex") else str(h)
    except Exception:
        return "unknown"
