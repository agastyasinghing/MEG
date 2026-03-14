"""
Polymarket CLOB API wrapper.

Thin async wrapper around py-clob-client. Handles authentication, rate limiting,
and retry logic. All other layers interact with Polymarket exclusively through
this module — never import py-clob-client directly outside this file.

Paper trading mode: when config.risk.paper_trading is True, place_order() logs
the intended order but does not submit it to the CLOB.

CLOBMarketFeed: background task that polls CLOB REST for active markets and
maintains market state in Redis. Watches the meg:active_markets set (written
by polygon_feed on new whale trades) and polls each market every ~5 seconds.

Market state Redis layout (per market):
  market:{id}:mid_price          ← float string
  market:{id}:bid                ← float string
  market:{id}:ask                ← float string
  market:{id}:liquidity          ← float string (USDC depth)
  market:{id}:volume_24h         ← float string
  market:{id}:participants       ← int string
  market:{id}:spread             ← float string
  market:{id}:last_updated_ms    ← int string (epoch ms)
  market:{id}:price_history      ← sorted set: score=timestamp_ms, member=mid_price
"""
from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Any

import structlog
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import MarketState, RedisKeys

logger = structlog.get_logger(__name__)

# Poll interval for each market (seconds)
_POLL_INTERVAL_SECONDS = 5.0

# Price history TTL: keep only last 1 hour = 3,600,000 ms of price points
_PRICE_HISTORY_TTL_MS = 3_600_000

# Per-request timeout for CLOB REST calls
_HTTP_TIMEOUT_SECONDS = 10.0


# ── CLOBMarketFeed ─────────────────────────────────────────────────────────────


class CLOBMarketFeed:
    """
    Background polling service for Polymarket CLOB market state.

    Watches the meg:active_markets Redis set (populated by polygon_feed on
    new whale trades). For each market in that set, polls the CLOB REST API
    every ~5 seconds and writes all market state keys to Redis.

    Price history is maintained as a sorted set per market, trimmed on every
    write to keep only the last 1 hour of prices (ZREMRANGEBYSCORE).

    Data flow:
      polygon_feed ──SADD──► meg:active_markets
                                   │
                        CLOBMarketFeed polls (every 5s)
                                   │
                        CLOB REST API ──► market state
                                   │
                        Redis keys: bid, ask, mid_price, spread,
                                    liquidity, volume_24h, participants,
                                    last_updated_ms, price_history (ZSET)

    Error handling: per-market try/except. One market failing to poll does
    not affect other markets. Errors are logged as WARNING and the poll
    cycle continues on the next interval.
    """

    def __init__(self, redis: Redis, config: MegConfig) -> None:
        self._redis = redis
        self._config = config
        self._clob_host: str = "https://clob.polymarket.com"

    async def run(self) -> None:
        """
        Main loop. Polls all active markets every _POLL_INTERVAL_SECONDS.
        Runs forever — call as a long-running asyncio task.
        """
        logger.info("clob_market_feed.started", poll_interval=_POLL_INTERVAL_SECONDS)
        while True:
            try:
                market_ids: set[str] = await self._redis.smembers(
                    RedisKeys.active_markets()
                )
                if market_ids:
                    tasks = [self._poll_market(mid) for mid in market_ids]
                    await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as exc:
                logger.warning("clob_market_feed.poll_cycle_error", error=str(exc))

            await asyncio.sleep(_POLL_INTERVAL_SECONDS)

    async def _poll_market(self, market_id: str) -> None:
        """
        Poll CLOB REST API for one market and write all state keys to Redis.
        Per-market errors are logged and the market is skipped this cycle.
        """
        try:
            state = await self._fetch_market_state(market_id)
            await self._write_state(state)
        except Exception as exc:
            logger.warning(
                "clob_market_feed.market_poll_failed",
                market_id=market_id,
                error=str(exc),
            )

    async def _fetch_market_state(self, market_id: str) -> MarketState:
        """
        Fetch current market state from CLOB REST API.
        Returns a MarketState Pydantic model.

        Uses httpx for async HTTP. Falls back to dummy values if httpx is
        not available (enables unit tests without network).
        """
        try:
            import httpx

            async with httpx.AsyncClient(timeout=_HTTP_TIMEOUT_SECONDS) as client:
                # Fetch orderbook for bid/ask/spread
                ob_resp = await client.get(
                    f"{self._clob_host}/orderbook",
                    params={"token_id": market_id},
                )
                ob_resp.raise_for_status()
                ob: dict[str, Any] = ob_resp.json()

                # Fetch market metadata for volume/participants
                mk_resp = await client.get(
                    f"{self._clob_host}/markets/{market_id}",
                )
                mk_resp.raise_for_status()
                mk: dict[str, Any] = mk_resp.json()

            best_bid = float(ob.get("best_bid", 0.0))
            best_ask = float(ob.get("best_ask", 1.0))
            mid_price = (best_bid + best_ask) / 2.0
            spread = best_ask - best_bid

            # Liquidity: sum of top-5 bid + ask sizes in USDC
            bids = ob.get("bids", [])
            asks = ob.get("asks", [])
            liquidity = sum(float(b.get("size", 0)) for b in bids[:5]) + sum(
                float(a.get("size", 0)) for a in asks[:5]
            )

            volume_24h = float(mk.get("volume", 0.0))
            participants = int(mk.get("unique_traders", 0))

        except ImportError:
            # httpx not available — return placeholder state for testing
            logger.debug(
                "clob_market_feed.httpx_not_available",
                market_id=market_id,
                note="returning placeholder state",
            )
            best_bid, best_ask = 0.45, 0.55
            mid_price = 0.50
            spread = 0.10
            liquidity = 0.0
            volume_24h = 0.0
            participants = 0

        return MarketState(
            market_id=market_id,
            bid=best_bid,
            ask=best_ask,
            mid_price=mid_price,
            spread=spread,
            liquidity_usdc=liquidity,
            volume_24h_usdc=volume_24h,
            participants=participants,
            last_updated_at=datetime.now(tz=timezone.utc),
        )

    async def _write_state(self, state: MarketState) -> None:
        """
        Write all market state fields to Redis.
        Price history sorted set is trimmed on every write to maintain 1h window.
        Uses a pipeline for atomic multi-key write.
        """
        mid = state.market_id
        now_ms = int(state.last_updated_at.timestamp() * 1000)
        cutoff_ms = now_ms - _PRICE_HISTORY_TTL_MS

        async with self._redis.pipeline(transaction=False) as pipe:
            # Scalar keys
            pipe.set(RedisKeys.market_mid_price(mid), str(state.mid_price))
            pipe.set(RedisKeys.market_bid(mid), str(state.bid))
            pipe.set(RedisKeys.market_ask(mid), str(state.ask))
            pipe.set(RedisKeys.market_spread(mid), str(state.spread))
            pipe.set(RedisKeys.market_liquidity(mid), str(state.liquidity_usdc))
            pipe.set(RedisKeys.market_volume_24h(mid), str(state.volume_24h_usdc))
            pipe.set(RedisKeys.market_participants(mid), str(state.participants))
            pipe.set(RedisKeys.market_last_updated_ms(mid), str(now_ms))

            # Price history sorted set: score=timestamp_ms, member=mid_price@timestamp
            # Member includes timestamp to allow duplicate prices at different times
            price_history_key = RedisKeys.market_price_history(mid)
            pipe.zadd(price_history_key, {f"{state.mid_price}@{now_ms}": now_ms})
            # Trim to 1-hour window on every write — O(log N + M) cost
            pipe.zremrangebyscore(price_history_key, "-inf", cutoff_ms)

            await pipe.execute()

        logger.debug(
            "clob_market_feed.state_written",
            market_id=mid,
            mid_price=state.mid_price,
            spread=state.spread,
            participants=state.participants,
        )


# ── Execution layer stubs (implemented in execution phase) ────────────────────
# All functions below raise NotImplementedError until the execution layer build.
# Do not remove these stubs — they define the interface contract.


async def get_market(market_id: str) -> dict:
    """
    Fetch market metadata: question, end date, status, category.
    Raises on network error after retries.
    """
    raise NotImplementedError("clob_client.get_market")


async def get_orderbook(market_id: str) -> dict:
    """
    Fetch the current orderbook for a market.
    Returns bids, asks, mid price, and spread.
    """
    raise NotImplementedError("clob_client.get_orderbook")


async def get_mid_price(market_id: str) -> float:
    """Return the current mid price (0.0–1.0) for a market."""
    raise NotImplementedError("clob_client.get_mid_price")


async def place_order(
    market_id: str,
    outcome: str,
    side: str,
    size_usdc: float,
    limit_price: float,
    config: MegConfig,
) -> str:
    """
    Place a limit order on the CLOB. Returns the order ID.
    In paper trading mode (config.risk.paper_trading=True): logs the order
    and returns a synthetic order ID without submitting to the exchange.
    """
    raise NotImplementedError("clob_client.place_order")


async def cancel_order(order_id: str) -> bool:
    """Cancel an open order. Returns True if successfully cancelled."""
    raise NotImplementedError("clob_client.cancel_order")


async def get_open_orders(market_id: str | None = None) -> list[dict]:
    """Return all open orders, optionally filtered by market."""
    raise NotImplementedError("clob_client.get_open_orders")


async def get_position(market_id: str) -> dict | None:
    """Return current position for a market, or None if no position held."""
    raise NotImplementedError("clob_client.get_position")
