"""
MEG Dashboard API — FastAPI application.

Endpoints:
  GET /api/v1/positions          — open positions (Redis-first, meg:open_positions hash)
  GET /api/v1/signals            — recent signal outcomes (PostgreSQL, last 50)
  GET /api/v1/whales             — qualified whale wallets (PostgreSQL, top 20 by score)
  GET /api/v1/markets            — active market states (Redis, meg:active_markets set)
  GET /api/v1/status             — system health (Redis + PAPER_TRADING env var)
  GET /api/v1/feed/signals       — SSE stream of real-time signal events (Redis pub/sub)

Design:
  - Redis is authoritative for live state (positions, markets, system flags).
  - PostgreSQL is authoritative for history (signals, whales).
  - A single module-level Redis client handles all non-SSE requests.
    SSE subscribers get their own client (pub/sub requires a dedicated connection).
  - DB sessions use the get_session() async context manager from meg.db.session.
    FastAPI dependency wraps it in an async generator for proper cleanup.
  - No bare `except`. Errors are logged and propagated as HTTP 500 unless the
    caller should receive a partial response (e.g. markets: bad market is skipped).
"""
from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.events import PositionState, RedisKeys
from meg.core.redis_client import close as close_redis
from meg.core.redis_client import create_redis_client
from meg.db.models import SignalOutcome, Wallet
from meg.db.session import close_db, get_session, init_db

logger = structlog.get_logger(__name__)

# ── Module-level Redis client (non-SSE use) ───────────────────────────────────
# Set during lifespan startup, cleared on shutdown. Never access directly outside
# this module — use get_redis() dependency instead.

_redis: Redis | None = None


# ── Lifespan: startup + shutdown ──────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global _redis
    db_url = os.environ["DATABASE_URL"]
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    await init_db(db_url)
    _redis = await create_redis_client(url=redis_url)
    logger.info("dashboard.api.started")

    yield

    await close_db()
    if _redis is not None:
        await close_redis(_redis)
    logger.info("dashboard.api.stopped")


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="MEG Dashboard API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ── Dependencies ──────────────────────────────────────────────────────────────


def get_redis() -> Redis:
    """Return the module-level Redis client. Raises if not yet initialised."""
    if _redis is None:
        raise RuntimeError("Redis client not initialised — lifespan not complete")
    return _redis


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield a transactional AsyncSession.
    Commits on clean exit; rolls back on exception. Mirrors get_session() contract.
    """
    async with get_session() as session:
        yield session


# ── GET /api/v1/positions ────────────────────────────────────────────────────


@app.get("/api/v1/positions")
async def get_positions(redis: Redis = Depends(get_redis)) -> dict:
    """
    Return all currently open positions from Redis (meg:open_positions hash).

    Redis is authoritative for live position state. The hash is maintained by
    position_manager: HSET on open, HDEL on close.
    """
    raw: dict[str, str] = await redis.hgetall(RedisKeys.open_positions())
    positions = []
    for position_json in raw.values():
        try:
            state = PositionState.model_validate_json(position_json)
            positions.append(state.model_dump())
        except Exception as exc:
            logger.warning(
                "dashboard.positions.parse_error",
                error=str(exc),
                snippet=position_json[:80],
            )
    return {"positions": positions}


# ── GET /api/v1/signals ───────────────────────────────────────────────────────


@app.get("/api/v1/signals")
async def get_signals(session: AsyncSession = Depends(db_session)) -> dict:
    """
    Return the 50 most recent signal outcomes from PostgreSQL, newest first.

    Includes both FILTERED and EXECUTED signals — the full event log.
    """
    result = await session.execute(
        select(SignalOutcome).order_by(SignalOutcome.fired_at.desc()).limit(50)
    )
    rows = result.scalars().all()
    return {
        "signals": [
            {
                "signal_id": r.signal_id,
                "market_id": r.market_id,
                "outcome": r.outcome,
                "composite_score": r.composite_score,
                "status": r.status,
                "fired_at": r.fired_at.isoformat(),
                "trap_warning": r.trap_warning,
                "is_contrarian": r.is_contrarian,
                "is_ladder": r.is_ladder,
                "whale_count": r.whale_count,
                "recommended_size_usdc": float(r.recommended_size_usdc),
                "saturation_score": r.saturation_score,
            }
            for r in rows
        ]
    }


# ── GET /api/v1/whales ────────────────────────────────────────────────────────


@app.get("/api/v1/whales")
async def get_whales(session: AsyncSession = Depends(db_session)) -> dict:
    """
    Return the top 20 qualified whale wallets ordered by composite score descending.
    """
    result = await session.execute(
        select(Wallet)
        .where(Wallet.is_qualified == True)  # noqa: E712 — SQLAlchemy requires ==
        .order_by(Wallet.composite_whale_score.desc())
        .limit(20)
    )
    rows = result.scalars().all()
    return {
        "whales": [
            {
                "address": r.address,
                "archetype": r.archetype,
                "composite_whale_score": r.composite_whale_score,
                "win_rate": r.win_rate,
                "avg_lead_time_hours": r.avg_lead_time_hours,
                "roi_30d": r.roi_30d,
                "roi_90d": r.roi_90d,
                "total_trades": r.total_trades,
                "last_seen_at": r.last_seen_at.isoformat(),
            }
            for r in rows
        ]
    }


# ── GET /api/v1/markets ───────────────────────────────────────────────────────


@app.get("/api/v1/markets")
async def get_markets(redis: Redis = Depends(get_redis)) -> dict:
    """
    Return state for all active markets from Redis.

    Active markets are registered by polygon_feed via SADD to meg:active_markets.
    Per-market state keys are written by CLOBMarketFeed on every poll (every 5s).
    Markets with unreadable state are skipped with a warning log.
    """
    market_ids: set[str] = await redis.smembers(RedisKeys.active_markets())
    markets = []

    for market_id in market_ids:
        try:
            pipe = redis.pipeline()
            pipe.get(RedisKeys.market_mid_price(market_id))
            pipe.get(RedisKeys.market_bid(market_id))
            pipe.get(RedisKeys.market_ask(market_id))
            pipe.get(RedisKeys.market_spread(market_id))
            pipe.get(RedisKeys.market_volume_24h(market_id))
            pipe.get(RedisKeys.market_liquidity(market_id))
            pipe.get(RedisKeys.market_participants(market_id))
            pipe.get(RedisKeys.market_last_updated_ms(market_id))
            mid, bid, ask, spread, vol, liq, participants, last_ms = await pipe.execute()

            markets.append(
                {
                    "market_id": market_id,
                    "mid_price": float(mid) if mid is not None else None,
                    "bid": float(bid) if bid is not None else None,
                    "ask": float(ask) if ask is not None else None,
                    "spread": float(spread) if spread is not None else None,
                    "volume_24h_usdc": float(vol) if vol is not None else None,
                    "liquidity_usdc": float(liq) if liq is not None else None,
                    "participants": int(participants) if participants is not None else None,
                    "last_updated_ms": int(last_ms) if last_ms is not None else None,
                }
            )
        except Exception as exc:
            logger.warning(
                "dashboard.markets.read_error",
                market_id=market_id,
                error=str(exc),
            )

    return {"markets": markets}


# ── GET /api/v1/status ────────────────────────────────────────────────────────


@app.get("/api/v1/status")
async def get_status(redis: Redis = Depends(get_redis)) -> dict:
    """
    Return MEG system health from Redis.

    is_paused:            set by Telegram /pause; cleared by /resume.
    paper_trading:        from PAPER_TRADING env var (default: true).
    daily_pnl_usdc:       running net P&L for today; reset at midnight UTC.
    last_block_processed: latest Polygon block successfully parsed.
    portfolio_value_usdc: current portfolio value written by position_manager.
    """
    pipe = redis.pipeline()
    pipe.exists(RedisKeys.system_paused())
    pipe.get(RedisKeys.daily_pnl_usdc())
    pipe.get(RedisKeys.last_processed_block())
    pipe.get(RedisKeys.portfolio_value_usdc())
    is_paused_flag, daily_pnl, last_block, portfolio_val = await pipe.execute()

    paper_trading = os.environ.get("PAPER_TRADING", "true").lower() != "false"

    return {
        "is_paused": bool(is_paused_flag),
        "paper_trading": paper_trading,
        "daily_pnl_usdc": float(daily_pnl) if daily_pnl is not None else 0.0,
        "last_block_processed": int(last_block) if last_block is not None else None,
        "portfolio_value_usdc": (
            float(portfolio_val) if portfolio_val is not None else None
        ),
    }


# ── GET /api/v1/feed/signals (SSE) ───────────────────────────────────────────


@app.get("/api/v1/feed/signals")
async def feed_signals() -> StreamingResponse:
    """
    Server-Sent Events stream of real-time signal events.

    Subscribes to the Redis CHANNEL_SIGNAL_EVENTS pub/sub channel and forwards
    each event as an SSE `data:` frame. A heartbeat comment is emitted every 15s
    so proxies and browsers don't kill idle connections.

    Each SSE frame carries the raw SignalEvent JSON string published by
    signal_engine.composite_scorer. The client can parse it with:
        const signal = JSON.parse(event.data)

    Design note: pub/sub requires a dedicated Redis connection — it cannot share
    the module-level client. A fresh connection is created per SSE subscriber and
    closed when the client disconnects.
    """
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    async def event_stream() -> AsyncGenerator[str, None]:
        yield ": connected\n\n"

        sub_client: Redis | None = None
        pubsub = None
        try:
            sub_client = await create_redis_client(url=redis_url)
            pubsub = sub_client.pubsub()
            await pubsub.subscribe(RedisKeys.CHANNEL_SIGNAL_EVENTS)

            while True:
                try:
                    msg = await asyncio.wait_for(
                        pubsub.get_message(ignore_subscribe_messages=True),
                        timeout=15.0,
                    )
                except asyncio.TimeoutError:
                    # No signal in 15s — emit heartbeat to keep connection alive
                    yield ": heartbeat\n\n"
                    continue

                if msg is None:
                    pass  # no message available right now — loop back
                elif msg["type"] == "message":
                    yield f"data: {msg['data']}\n\n"
                else:
                    logger.debug(
                        "dashboard.feed.signals.unexpected_msg_type",
                        msg_type=msg["type"],
                    )

        except Exception as exc:
            logger.warning("dashboard.feed.signals.error", error=str(exc))
        finally:
            if pubsub is not None:
                try:
                    await pubsub.unsubscribe(RedisKeys.CHANNEL_SIGNAL_EVENTS)
                    await pubsub.aclose()
                except Exception:
                    pass
            if sub_client is not None:
                try:
                    await close_redis(sub_client)
                except Exception:
                    pass

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx response buffering
        },
    )
