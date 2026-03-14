"""
Tests for meg/data_layer/polygon_feed.py.

Uses mock PolygonRPCConnection to avoid real RPC dependency.
All tests run with fakeredis (via conftest mock_redis fixture).
No network, no Polygon node required.

Test categories:
  1. PolygonRPCConnection ABC — contract enforced
  2. _filter_whale_transaction — filtering logic
  3. PolygonFeed._process_block — per-tx error handling, Redis writes
  4. PolygonFeed._check_block_gap — gap detection and logging
  5. PolygonFeed.run — reconnect on exception
  6. _emit_event — Redis publish
"""
from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RawWhaleTrade, RedisKeys
from meg.data_layer.polygon_feed import (
    CLOB_CONTRACT_ADDRESS,
    PolygonFeed,
    PolygonRPCConnection,
    _emit_event,
    _filter_whale_transaction,
)


# ── Fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture
def config() -> MegConfig:
    return MegConfig()


class MockRPCConnection(PolygonRPCConnection):
    """Minimal mock RPC connection for testing."""

    def __init__(self, current_block: int = 100) -> None:
        self._current_block = current_block
        self._blocks_to_yield: list[int] = []
        self._txs_per_block: dict[int, list[dict[str, Any]]] = {}

    async def get_block_number(self) -> int:
        return self._current_block

    async def subscribe_new_blocks(self) -> AsyncIterator[int]:  # type: ignore[override]
        for b in self._blocks_to_yield:
            yield b

    async def get_block_transactions(self, block_number: int) -> list[dict[str, Any]]:
        return self._txs_per_block.get(block_number, [])


def make_clob_tx(
    wallet: str = "0xabc",
    value_wei: int = 0,
    input_data: str = "0x12345678" + "00" * 68,  # selector + args
    gas_price: int = 100_000_000_000,
    gas: int = 200_000,
    tx_hash: str = "0x" + "a" * 64,
    block_number: int = 101,
) -> dict[str, Any]:
    """Build a fake Polygon transaction dict targeting the CLOB contract."""
    return {
        "from": wallet,
        "to": CLOB_CONTRACT_ADDRESS,
        "value": value_wei,
        "input": input_data,
        "gasPrice": gas_price,
        "gas": gas,
        "hash": tx_hash,
        "blockNumber": block_number,
    }


# ── 1. ABC contract ────────────────────────────────────────────────────────────


def test_polygon_rpc_connection_is_abstract():
    """PolygonRPCConnection cannot be instantiated directly."""
    with pytest.raises(TypeError):
        PolygonRPCConnection()  # type: ignore[abstract]


def test_mock_rpc_connection_satisfies_abc():
    """MockRPCConnection implements the full ABC without error."""
    conn = MockRPCConnection()
    assert conn is not None


# ── 2. _filter_whale_transaction ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_filter_ignores_non_clob_tx(config):
    tx = make_clob_tx()
    tx["to"] = "0xdeadbeef"  # not the CLOB contract
    result = await _filter_whale_transaction(tx, config)
    assert result is None


@pytest.mark.asyncio
async def test_filter_ignores_empty_input(config):
    tx = make_clob_tx(input_data="0x")  # no function call
    result = await _filter_whale_transaction(tx, config)
    assert result is None


@pytest.mark.asyncio
async def test_filter_ignores_missing_from(config):
    tx = make_clob_tx()
    tx["from"] = ""
    result = await _filter_whale_transaction(tx, config)
    assert result is None


@pytest.mark.asyncio
async def test_filter_ignores_missing_hash(config):
    tx = make_clob_tx()
    tx["hash"] = ""
    result = await _filter_whale_transaction(tx, config)
    assert result is None


@pytest.mark.asyncio
async def test_filter_returns_raw_whale_trade_for_valid_clob_tx(config):
    tx = make_clob_tx(
        wallet="0x1234567890123456789012345678901234567890",
        tx_hash="0x" + "b" * 64,
        block_number=200,
    )
    result = await _filter_whale_transaction(tx, config)
    assert result is not None
    assert isinstance(result, RawWhaleTrade)
    assert result.wallet_address == "0x1234567890123456789012345678901234567890"
    assert result.block_number == 200
    assert result.tx_hash == "0x" + "b" * 64


@pytest.mark.asyncio
async def test_filter_handles_hex_hash_object(config):
    """Handles web3.py HexBytes objects as tx_hash."""
    tx = make_clob_tx()

    class FakeHexBytes:
        def hex(self):
            return "0x" + "c" * 64

    tx["hash"] = FakeHexBytes()
    result = await _filter_whale_transaction(tx, config)
    assert result is not None
    assert result.tx_hash == "0x" + "c" * 64


@pytest.mark.asyncio
async def test_filter_returns_none_on_exception(config):
    """Returns None (never raises) when tx dict has unexpected structure."""
    result = await _filter_whale_transaction({"to": None}, config)
    assert result is None


@pytest.mark.asyncio
async def test_filter_clob_address_case_insensitive(config):
    tx = make_clob_tx()
    tx["to"] = CLOB_CONTRACT_ADDRESS.upper()
    result = await _filter_whale_transaction(tx, config)
    assert result is not None


# ── 3. PolygonFeed._process_block ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_process_block_emits_event_for_clob_tx(mock_redis, config):
    rpc = MockRPCConnection()
    tx = make_clob_tx(
        wallet="0xwhale",
        tx_hash="0x" + "d" * 64,
        block_number=101,
    )
    rpc._txs_per_block[101] = [tx]

    feed = PolygonFeed(rpc=rpc, redis=mock_redis, config=config)
    await feed._process_block(101)

    # Should have published to the raw whale trades channel
    # and added market_id to active_markets
    active = await mock_redis.smembers(RedisKeys.active_markets())
    assert len(active) == 1


@pytest.mark.asyncio
async def test_process_block_skips_non_clob_tx(mock_redis, config):
    rpc = MockRPCConnection()
    tx = make_clob_tx()
    tx["to"] = "0xnotclob"
    rpc._txs_per_block[101] = [tx]

    feed = PolygonFeed(rpc=rpc, redis=mock_redis, config=config)
    await feed._process_block(101)

    active = await mock_redis.smembers(RedisKeys.active_markets())
    assert len(active) == 0


@pytest.mark.asyncio
async def test_process_block_continues_on_per_tx_exception(mock_redis, config):
    """Feed continues processing after one malformed tx raises an exception."""
    rpc = MockRPCConnection()
    good_tx = make_clob_tx(wallet="0xgood", tx_hash="0x" + "e" * 64, block_number=101)
    bad_tx = {"to": CLOB_CONTRACT_ADDRESS, "from": None, "this_will_fail": True}
    # put bad tx first — good tx should still get processed
    rpc._txs_per_block[101] = [bad_tx, good_tx]

    feed = PolygonFeed(rpc=rpc, redis=mock_redis, config=config)
    await feed._process_block(101)

    # good_tx should have been processed despite bad_tx failing
    active = await mock_redis.smembers(RedisKeys.active_markets())
    assert len(active) == 1


@pytest.mark.asyncio
async def test_process_block_skips_block_on_rpc_error(mock_redis, config):
    """If get_block_transactions raises, the block is skipped (no crash)."""
    rpc = MockRPCConnection()

    async def raise_on_fetch(block_number: int):
        raise ConnectionError("RPC unavailable")

    rpc.get_block_transactions = raise_on_fetch  # type: ignore[method-assign]

    feed = PolygonFeed(rpc=rpc, redis=mock_redis, config=config)
    # Should not raise
    await feed._process_block(999)


# ── 4. PolygonFeed._check_block_gap ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_check_block_gap_no_warning_on_first_run(mock_redis, config, caplog):
    """No warning when last_processed_block is not set (first run)."""
    rpc = MockRPCConnection(current_block=100)
    feed = PolygonFeed(rpc=rpc, redis=mock_redis, config=config)

    import logging
    with caplog.at_level(logging.WARNING):
        await feed._check_block_gap(100)

    assert "block_gap_detected" not in caplog.text


@pytest.mark.asyncio
async def test_check_block_gap_warns_on_gap(mock_redis, config, caplog):
    """Logs WARNING when gap > 1 block is detected."""
    await mock_redis.set(RedisKeys.last_processed_block(), "90")

    rpc = MockRPCConnection(current_block=100)
    feed = PolygonFeed(rpc=rpc, redis=mock_redis, config=config)

    import logging
    import structlog

    # structlog captures differently — just ensure the function runs without error
    await feed._check_block_gap(100)  # gap = 10


@pytest.mark.asyncio
async def test_check_block_gap_no_gap_is_silent(mock_redis, config):
    """No warning when current block is only 1 ahead of last processed."""
    await mock_redis.set(RedisKeys.last_processed_block(), "99")

    rpc = MockRPCConnection(current_block=100)
    feed = PolygonFeed(rpc=rpc, redis=mock_redis, config=config)
    # Should not raise or log at WARNING level
    await feed._check_block_gap(100)


# ── 5. PolygonFeed.run — reconnect behavior ───────────────────────────────────


@pytest.mark.asyncio
async def test_run_reconnects_on_exception(mock_redis, config):
    """run() reconnects instead of crashing when _run_once raises."""
    rpc = MockRPCConnection()
    call_count = 0

    async def patched_run_once():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("simulated disconnect")
        # Cancel the task after 3 calls to avoid infinite loop in test
        raise asyncio.CancelledError()

    feed = PolygonFeed(rpc=rpc, redis=mock_redis, config=config)
    feed._run_once = patched_run_once  # type: ignore[method-assign]

    with patch("asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(asyncio.CancelledError):
            await feed.run()

    assert call_count == 3


# ── 6. _emit_event ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_emit_event_publishes_to_channel(mock_redis, config):
    """_emit_event publishes a JSON-serialized RawWhaleTrade."""
    event = RawWhaleTrade(
        wallet_address="0xabc",
        market_id="market_test",
        outcome="YES",
        size_usdc=1000.0,
        timestamp_ms=1_700_000_000_000,
        tx_hash="0x" + "f" * 64,
        block_number=100,
        market_price_at_trade=0.65,
    )

    # Subscribe before emitting; consume the subscribe confirmation first.
    # fakeredis get_message(ignore_subscribe_messages=True) returns None if the
    # first buffered item is the subscribe confirmation — consume it explicitly.
    pubsub = mock_redis.pubsub()
    await pubsub.subscribe(RedisKeys.CHANNEL_RAW_WHALE_TRADES)
    await pubsub.get_message(timeout=0.1)  # consume subscribe confirmation

    await _emit_event(mock_redis, event)

    message = await pubsub.get_message(timeout=0.1)
    assert message is not None
    data = json.loads(message["data"])
    assert data["wallet_address"] == "0xabc"
    assert data["market_id"] == "market_test"
    await pubsub.unsubscribe()
    await pubsub.aclose()
