"""
Execution layer test fixtures and factory helpers.

No DB fixtures needed — execution modules only interact with Redis and mock
the CLOB client + position_manager at the function level.

Factory helpers:
  make_proposal()         — TradeProposal with sensible defaults
  set_market_redis_data() — pre-populate all Redis keys execution modules read:
                            mid_price, bid, ask, spread, liquidity
"""
from __future__ import annotations

import time
import uuid

import fakeredis.aioredis
import pytest
import pytest_asyncio
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, TradeProposal


# ── Redis fixture ─────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def mock_redis() -> Redis:
    """Fakeredis instance — in-memory, no real Redis needed."""
    return fakeredis.aioredis.FakeRedis()


# ── Config fixture ────────────────────────────────────────────────────────────


@pytest.fixture
def test_config() -> MegConfig:
    """Default MegConfig — uses updated EntryConfig defaults from Phase 7."""
    return MegConfig()


# ── Factory helpers ───────────────────────────────────────────────────────────


def make_proposal(
    *,
    proposal_id: str | None = None,
    signal_id: str = "sig_test001",
    market_id: str = "market_001",
    outcome: str = "YES",
    size_usdc: float = 100.0,
    limit_price: float = 0.45,
    market_price_at_signal: float = 0.42,
    saturation_score: float = 0.0,
    contributing_wallets: list[str] | None = None,
) -> TradeProposal:
    """
    Return a TradeProposal with sensible defaults. Override as needed.

    Defaults set for entry_filter / slippage_guard pass scenarios:
      market_price_at_signal=0.42, limit_price=0.45
      → entry distance = (0.45 - 0.42) / 0.42 ≈ 7.1% (near max_entry_distance_pct=6%)
      Use a lower current_price in set_market_redis_data to test pass cases.
    """
    return TradeProposal(
        proposal_id=proposal_id or f"prop_{uuid.uuid4().hex[:8]}",
        signal_id=signal_id,
        market_id=market_id,
        outcome=outcome,
        size_usdc=size_usdc,
        limit_price=limit_price,
        status="APPROVED",
        created_at_ms=int(time.time() * 1000),
        market_price_at_signal=market_price_at_signal,
        saturation_score=saturation_score,
        contributing_wallets=contributing_wallets or ["0xWHALE001"],
    )


async def set_market_redis_data(
    redis: Redis,
    *,
    market_id: str = "market_001",
    mid_price: float = 0.44,
    bid: float = 0.435,
    ask: float = 0.445,
    spread: float = 0.01,
    liquidity: float = 10_000.0,
) -> None:
    """
    Write all market state keys that execution modules read.
    CLOBMarketFeed writes these in production; this helper simulates it.

    Keys written:
      market:{id}:mid_price   — used by entry_filter
      market:{id}:bid         — used by slippage_guard
      market:{id}:ask         — used by slippage_guard
      market:{id}:spread      — informational (not read by execution modules directly)
      market:{id}:liquidity   — used by slippage_guard.estimate_slippage()
    """
    await redis.set(RedisKeys.market_mid_price(market_id), str(mid_price))
    await redis.set(RedisKeys.market_bid(market_id), str(bid))
    await redis.set(RedisKeys.market_ask(market_id), str(ask))
    await redis.set(RedisKeys.market_spread(market_id), str(spread))
    await redis.set(RedisKeys.market_liquidity(market_id), str(liquidity))
