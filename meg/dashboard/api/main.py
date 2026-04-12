"""
MEG Dashboard API — FastAPI application.

Endpoints:
  # System
  GET  /api/v1/status                      → health, mode, today P&L, last block
  GET  /api/v1/config                      → all current config values
  PATCH /api/v1/config                     → update one or more values (hot reload via YAML)

  # Signals
  GET  /api/v1/signals                     → signal log (filter: status, score, date, market)
  GET  /api/v1/signals/{id}                → full signal detail with scores_json
  POST /api/v1/signals/{id}/approve        → approve pending trade (id = proposal_id)
  POST /api/v1/signals/{id}/reject         → reject pending trade (id = proposal_id)
  GET  /api/v1/signals/{id}/explain        → human-readable score explanation

  # Positions
  GET  /api/v1/positions                   → all open positions (Redis)
  POST /api/v1/positions/{id}/exit         → flag position for manual exit

  # Performance
  GET  /api/v1/pnl                         → P&L summary (period: day/week/month/all)

  # Whales
  GET  /api/v1/whales                      → top 20 qualified whale wallets

  # Markets
  GET  /api/v1/markets                     → active monitored market states (Redis)

  # Streams
  GET  /api/v1/feed/signals                → SSE: live signal events (Redis pub/sub)

Design:
  - Redis is authoritative for live state (positions, markets, system flags).
  - PostgreSQL is authoritative for history (signals, whales, positions).
  - Config is read from / written to config.yaml (watchdog hot-reload in bot process
    picks up writes within ~1s). PATCH updates _config in-memory immediately as well.
  - A single module-level Redis client handles all non-SSE requests.
    SSE subscribers get their own client (pub/sub requires a dedicated connection).
  - DB sessions use the get_session() async context manager from meg.db.session.
    FastAPI dependency wraps it in an async generator for proper cleanup.
  - No bare `except`. Errors are logged and propagated as HTTP 500 unless the
    caller should receive a partial response (e.g. markets: bad market is skipped).

NOTE — approve/reject path parameter:
  The PRD uses "signal_id" in the path, but pending proposals are keyed by
  proposal_id (proposal:{proposal_id}:pending). The path param is treated as
  proposal_id. The UI sends proposal_id in this slot. A proper signal_id →
  proposal_id mapping (via Redis) is a TODO — see TODOS.md.
"""
from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import structlog
import yaml
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import ValidationError
from redis.asyncio import Redis
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import PositionState, RedisKeys, TradeProposal
from meg.core.redis_client import close as close_redis
from meg.core.redis_client import create_redis_client
from meg.db.models import Position, PositionStatus, SignalOutcome, SignalStatus, Wallet
from meg.db.session import close_db, get_session, init_db
from meg.execution import order_router

logger = structlog.get_logger(__name__)

# ── Module-level state (set during lifespan startup) ──────────────────────────

_redis: Redis | None = None
_config: MegConfig | None = None
_config_path: Path | None = None


# ── Lifespan: startup + shutdown ──────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global _redis, _config, _config_path

    db_url = os.environ["DATABASE_URL"]
    redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    config_file = os.environ.get("MEG_CONFIG_PATH", "config/config.yaml")

    await init_db(db_url)
    _redis = await create_redis_client(url=redis_url)

    _config_path = Path(config_file).resolve()
    try:
        raw: Any = yaml.safe_load(_config_path.read_text()) or {}
        _config = MegConfig(**raw)
    except Exception as exc:
        logger.error("dashboard.api.config_load_failed", path=str(_config_path), error=str(exc))
        _config = MegConfig()  # safe defaults — don't block startup

    logger.info("dashboard.api.started", config_path=str(_config_path))

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
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
)


# ── Dependencies ──────────────────────────────────────────────────────────────


def get_redis() -> Redis:
    """Return the module-level Redis client. Raises if not yet initialised."""
    if _redis is None:
        raise RuntimeError("Redis client not initialised — lifespan not complete")
    return _redis


def get_config() -> MegConfig:
    """Return the current in-memory config. Raises if not yet initialised."""
    if _config is None:
        raise RuntimeError("Config not loaded — lifespan not complete")
    return _config


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield a transactional AsyncSession.
    Commits on clean exit; rolls back on exception. Mirrors get_session() contract.
    """
    async with get_session() as session:
        yield session


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


# ── GET /api/v1/config ────────────────────────────────────────────────────────


@app.get("/api/v1/config")
async def get_config_endpoint(cfg: MegConfig = Depends(get_config)) -> dict:
    """Return all current configuration values as a nested dict."""
    return {"config": cfg.model_dump()}


# ── PATCH /api/v1/config ──────────────────────────────────────────────────────


def _deep_merge(base: dict, patch: dict) -> dict:
    """Recursively merge patch into base. Returns a new dict."""
    result = base.copy()
    for key, value in patch.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


@app.patch("/api/v1/config")
async def patch_config(body: dict) -> dict:
    """
    Update one or more config values. Writes to config.yaml so the bot process
    picks up the change via watchdog within ~1 second. Also updates _config
    in this process immediately.

    Body: nested dict matching the config schema. Example:
      {"signal": {"composite_score_threshold": 0.50}}

    Returns the full updated config.

    Raises 422 if the patch produces an invalid config.
    Raises 500 if config.yaml cannot be read or written.
    """
    global _config

    if _config_path is None or _config is None:
        raise HTTPException(status_code=500, detail="Config not initialised")

    # Deep-merge patch onto current config dict, then validate with Pydantic.
    current_dict = _config.model_dump()
    merged = _deep_merge(current_dict, body)

    try:
        new_config = MegConfig(**merged)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    # Write merged dict back to YAML (preserves all keys; comments are lost on round-trip).
    try:
        _config_path.write_text(yaml.dump(merged, default_flow_style=False, sort_keys=True))
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to write config.yaml: {exc}",
        ) from exc

    _config = new_config
    logger.info(
        "dashboard.config.patched",
        patch_keys=list(body.keys()),
        config_path=str(_config_path),
    )
    return {"updated": body, "config": new_config.model_dump()}


# ── GET /api/v1/signals ───────────────────────────────────────────────────────


@app.get("/api/v1/signals")
async def get_signals(
    status: Optional[str] = Query(default=None, description="Filter by signal status"),
    score_min: Optional[float] = Query(default=None, ge=0.0, le=1.0),
    score_max: Optional[float] = Query(default=None, ge=0.0, le=1.0),
    market_id: Optional[str] = Query(default=None),
    date_from: Optional[str] = Query(default=None, description="ISO datetime (UTC)"),
    date_to: Optional[str] = Query(default=None, description="ISO datetime (UTC)"),
    limit: int = Query(default=50, ge=1, le=500),
    session: AsyncSession = Depends(db_session),
) -> dict:
    """
    Return signal outcomes from PostgreSQL, newest first.

    Filters (all optional, combined with AND):
      status:    exact match against SignalStatus (PENDING, FILTERED, EXECUTED, etc.)
      score_min: composite_score >= value
      score_max: composite_score <= value
      market_id: exact market_id match
      date_from: fired_at >= value (ISO 8601 UTC string)
      date_to:   fired_at <= value (ISO 8601 UTC string)

    Note: market_category and whale_archetype filters are not yet supported —
    these columns are not on signal_outcomes (v1.5 schema addition).
    """
    filters = []

    if status is not None:
        filters.append(SignalOutcome.status == status)
    if score_min is not None:
        filters.append(SignalOutcome.composite_score >= score_min)
    if score_max is not None:
        filters.append(SignalOutcome.composite_score <= score_max)
    if market_id is not None:
        filters.append(SignalOutcome.market_id == market_id)
    if date_from is not None:
        try:
            dt = datetime.fromisoformat(date_from.replace("Z", "+00:00"))
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=f"Invalid date_from: {exc}") from exc
        filters.append(SignalOutcome.fired_at >= dt)
    if date_to is not None:
        try:
            dt = datetime.fromisoformat(date_to.replace("Z", "+00:00"))
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=f"Invalid date_to: {exc}") from exc
        filters.append(SignalOutcome.fired_at <= dt)

    stmt = (
        select(SignalOutcome)
        .where(and_(*filters) if filters else True)
        .order_by(SignalOutcome.fired_at.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    rows = result.scalars().all()

    return {
        "signals": [
            {
                "signal_id": r.signal_id,
                "market_id": r.market_id,
                "outcome": r.outcome,
                "composite_score": r.composite_score,
                "recommended_size_usdc": float(r.recommended_size_usdc),
                "scores_json": r.scores_json,
                "status": r.status,
                "fired_at": r.fired_at.isoformat(),
                "trap_warning": r.trap_warning,
                "is_contrarian": r.is_contrarian,
                "is_ladder": r.is_ladder,
                "whale_count": r.whale_count,
                "saturation_score": r.saturation_score,
                "market_price_at_signal": float(r.market_price_at_signal),
                "triggering_wallet": r.triggering_wallet,
            }
            for r in rows
        ]
    }


# ── GET /api/v1/signals/{signal_id} ───────────────────────────────────────────


@app.get("/api/v1/signals/{signal_id}")
async def get_signal(
    signal_id: str,
    session: AsyncSession = Depends(db_session),
) -> dict:
    """Return full signal detail including scores_json breakdown."""
    result = await session.execute(
        select(SignalOutcome).where(SignalOutcome.signal_id == signal_id)
    )
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Signal {signal_id!r} not found")

    return {
        "signal_id": row.signal_id,
        "market_id": row.market_id,
        "outcome": row.outcome,
        "composite_score": row.composite_score,
        "recommended_size_usdc": float(row.recommended_size_usdc),
        "kelly_fraction": row.kelly_fraction,
        "scores_json": row.scores_json,
        "status": row.status,
        "fired_at": row.fired_at.isoformat(),
        "expires_at": row.expires_at.isoformat() if row.expires_at else None,
        "resolved_at": row.resolved_at.isoformat() if row.resolved_at else None,
        "resolved_pnl_usdc": float(row.resolved_pnl_usdc) if row.resolved_pnl_usdc is not None else None,
        "trap_warning": row.trap_warning,
        "is_contrarian": row.is_contrarian,
        "is_ladder": row.is_ladder,
        "whale_count": row.whale_count,
        "saturation_score": row.saturation_score,
        "market_price_at_signal": float(row.market_price_at_signal),
        "triggering_wallet": row.triggering_wallet,
        "contributing_wallets": row.contributing_wallets,
    }


# ── GET /api/v1/signals/{signal_id}/explain ───────────────────────────────────

# Score label map used by _format_explanation.
_SCORE_LABELS: dict[str, tuple[str, str]] = {
    "lead_lag":            ("Lead-Lag",            "Whale entered early relative to price move"),
    "consensus":           ("Consensus",           "Independent whale agreement on direction"),
    "kelly_confidence":    ("Kelly Confidence",    "Expected-value edge estimate (positive EV)"),
    "divergence":          ("Divergence",          "Signal vs current order flow (contrarian boost)"),
    "conviction_ratio":    ("Conviction Ratio",    "Trade size relative to wallet capital"),
    "archetype_multiplier":("Archetype Multiplier","Score weight by whale classification"),
    "ladder_multiplier":   ("Ladder Multiplier",   "Bonus for multi-rung position building"),
}


def _format_explanation(row: SignalOutcome) -> dict:
    """Build a human-readable score breakdown from a SignalOutcome row."""
    scores = row.scores_json or {}
    breakdown = []
    for key, (label, description) in _SCORE_LABELS.items():
        if key not in scores:
            continue
        val = scores[key]
        # Qualitative tier for operator readability.
        if key.endswith("multiplier"):
            tier = "STRONG" if val >= 1.5 else ("NEUTRAL" if val >= 1.0 else "WEAK")
        else:
            tier = "STRONG" if val >= 0.70 else ("MODERATE" if val >= 0.45 else "WEAK")
        breakdown.append({
            "key": key,
            "label": label,
            "description": description,
            "score": round(val, 4),
            "tier": tier,
        })

    # Overall verdict
    cs = row.composite_score
    if cs >= 0.70:
        verdict = "HIGH CONFIDENCE — strong signal, review trap risk before approving"
    elif cs >= 0.55:
        verdict = "MODERATE CONFIDENCE — signal has merit, check saturation and consensus"
    else:
        verdict = "LOW CONFIDENCE — marginal signal, high bar for approval"

    if row.trap_warning:
        verdict = "⚠ TRAP WARNING — " + verdict

    return {
        "signal_id": row.signal_id,
        "market_id": row.market_id,
        "outcome": row.outcome,
        "composite_score": row.composite_score,
        "verdict": verdict,
        "is_contrarian": row.is_contrarian,
        "is_ladder": row.is_ladder,
        "trap_warning": row.trap_warning,
        "saturation_score": row.saturation_score,
        "breakdown": breakdown,
    }


@app.get("/api/v1/signals/{signal_id}/explain")
async def explain_signal(
    signal_id: str,
    session: AsyncSession = Depends(db_session),
) -> dict:
    """Return a human-readable explanation of a signal's composite score."""
    result = await session.execute(
        select(SignalOutcome).where(SignalOutcome.signal_id == signal_id)
    )
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Signal {signal_id!r} not found")

    return {"explanation": _format_explanation(row)}


# ── POST /api/v1/signals/{signal_id}/approve ─────────────────────────────────
#
# Approve flow — Redis GETDEL is atomic: eliminates TOCTOU race between two
# simultaneous approve clicks (Telegram + dashboard, or double-click).
#
#  Redis GETDEL proposal:{proposal_id}:pending
#       │
#       ├── None ──► 404  "Signal not found or already processed"
#       │
#       └── JSON ──► parse TradeProposal
#                        │
#                        └── order_router.place(proposal, redis, config)
#                                 │
#                                 ├── raises ──► 409 "consumed — cannot re-queue"
#                                 │                    (key is gone; operator must re-evaluate)
#                                 └── ok ──► DB UPDATE status ──► 200


@app.post("/api/v1/signals/{signal_id}/approve")
async def approve_signal(
    signal_id: str,
    redis: Redis = Depends(get_redis),
    cfg: MegConfig = Depends(get_config),
    session: AsyncSession = Depends(db_session),
) -> dict:
    """
    Approve a pending trade proposal.

    Path param: proposal_id (named signal_id per PRD convention; the pending
    proposal is keyed by proposal_id in Redis).

    Uses GETDEL (atomic get+delete) to eliminate the double-click / Telegram+dashboard
    race condition. If two approvals arrive simultaneously, one gets the proposal and
    the other gets 404.

    IMPORTANT: if order_router.place() raises after GETDEL has already consumed
    the key, the proposal is permanently gone. The response body describes this
    so the operator knows not to retry — they must re-evaluate via Telegram.
    """
    raw = await redis.getdel(RedisKeys.pending_proposal(signal_id))
    if raw is None:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found or already processed (expired or handled by Telegram).",
        )

    try:
        proposal = TradeProposal.model_validate_json(raw)
    except (ValidationError, ValueError) as exc:
        logger.error("dashboard.approve.parse_error", proposal_id=signal_id, error=str(exc))
        raise HTTPException(status_code=500, detail="Could not parse proposal from Redis.") from exc

    try:
        result = await order_router.place(proposal, redis, cfg, session=None)
    except Exception as exc:
        logger.error(
            "dashboard.approve.order_router_exception",
            proposal_id=signal_id,
            error=str(exc),
        )
        # Proposal key is already gone (GETDEL). Operator cannot retry — must re-evaluate.
        raise HTTPException(
            status_code=409,
            detail=(
                f"Proposal consumed but execution failed: {exc}. "
                "Signal cannot be re-queued — re-evaluate via Telegram."
            ),
        ) from exc

    logger.info(
        "dashboard.approve.completed",
        proposal_id=signal_id,
        accepted=result["accepted"],
        reason=result.get("reason", ""),
    )
    return {
        "approved": True,
        "accepted": result["accepted"],
        "order_id": result.get("order_id"),
        "reason": result.get("reason", ""),
        "estimated_slippage": result.get("estimated_slippage"),
    }


# ── POST /api/v1/signals/{signal_id}/reject ───────────────────────────────────


@app.post("/api/v1/signals/{signal_id}/reject")
async def reject_signal(
    signal_id: str,
    body: Optional[dict] = None,
    redis: Redis = Depends(get_redis),
) -> dict:
    """
    Reject a pending trade proposal.

    Path param: proposal_id (named signal_id per PRD convention).
    Body: optional {"reason": "price moved"} for audit logging.

    Uses GETDEL for the same double-click guard as approve.
    """
    raw = await redis.getdel(RedisKeys.pending_proposal(signal_id))
    if raw is None:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found or already processed.",
        )

    reason = body.get("reason", "rejected_via_dashboard") if body else "rejected_via_dashboard"
    logger.info(
        "dashboard.reject.completed",
        proposal_id=signal_id,
        rejection_reason=reason,
    )
    return {"rejected": True, "proposal_id": signal_id, "reason": reason}


# ── GET /api/v1/positions ─────────────────────────────────────────────────────


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


# ── POST /api/v1/positions/{position_id}/exit ─────────────────────────────────


@app.post("/api/v1/positions/{position_id}/exit")
async def request_position_exit(
    position_id: str,
    redis: Redis = Depends(get_redis),
) -> dict:
    """
    Flag a position for manual exit.

    Sets RedisKeys.exit_requested(position_id) in Redis. The position_manager
    monitoring loop checks this flag on each tick and initiates the close flow.

    Returns 404 if the position is not in the open_positions hash.
    Returns 200 with a note that exit requires position_manager to be running.
    """
    exists = await redis.hexists(RedisKeys.open_positions(), position_id)
    if not exists:
        raise HTTPException(
            status_code=404,
            detail=f"Position {position_id!r} not found in open positions.",
        )

    await redis.set(RedisKeys.exit_requested(position_id), "1")
    logger.info("dashboard.position_exit.requested", position_id=position_id)
    return {
        "exit_requested": True,
        "position_id": position_id,
        "note": "Exit flag set — requires position_manager to be running to process.",
    }


# ── GET /api/v1/pnl ───────────────────────────────────────────────────────────


@app.get("/api/v1/pnl")
async def get_pnl(
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(db_session),
) -> dict:
    """
    Return P&L summary across time periods.

    today:     from Redis daily_pnl_usdc (maintained by position_manager, reset at midnight UTC).
    week:      sum of resolved_pnl_usdc from positions closed in the last 7 days.
    month:     sum of resolved_pnl_usdc from positions closed in the last 30 days.
    all_time:  sum of all resolved_pnl_usdc on closed positions.

    Counts: total closed positions per period.
    """
    now_utc = datetime.now(tz=timezone.utc)
    week_start = now_utc - timedelta(days=7)
    month_start = now_utc - timedelta(days=30)

    # Today P&L from Redis (authoritative for current day, includes in-progress positions)
    daily_pnl_raw = await redis.get(RedisKeys.daily_pnl_usdc())
    today_pnl = float(daily_pnl_raw) if daily_pnl_raw is not None else 0.0

    # DB aggregates for week / month / all-time
    async def _sum_pnl(after: datetime | None) -> tuple[float, int]:
        """Return (sum_pnl_usdc, count) for closed positions since `after`."""
        filters = [Position.status != PositionStatus.OPEN.value]
        if after is not None:
            filters.append(Position.closed_at >= after)
        result = await session.execute(
            select(
                func.coalesce(func.sum(Position.resolved_pnl_usdc), 0.0),
                func.count(Position.position_id),
            ).where(and_(*filters))
        )
        row = result.one()
        return float(row[0]), int(row[1])

    week_pnl, week_count = await _sum_pnl(week_start)
    month_pnl, month_count = await _sum_pnl(month_start)
    all_pnl, all_count = await _sum_pnl(None)

    return {
        "today": {"pnl_usdc": today_pnl},
        "week": {"pnl_usdc": week_pnl, "closed_positions": week_count},
        "month": {"pnl_usdc": month_pnl, "closed_positions": month_count},
        "all_time": {"pnl_usdc": all_pnl, "closed_positions": all_count},
    }


# ── GET /api/v1/whales ────────────────────────────────────────────────────────


@app.get("/api/v1/whales")
async def get_whales(session: AsyncSession = Depends(db_session)) -> dict:
    """Return the top 20 qualified whale wallets ordered by composite score descending."""
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
                "roi_all_time": r.roi_all_time,
                "avg_conviction_ratio": r.avg_conviction_ratio,
                "reputation_decay_factor": r.reputation_decay_factor,
                "total_trades": r.total_trades,
                "total_volume_usdc": float(r.total_volume_usdc),
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
    redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")

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
