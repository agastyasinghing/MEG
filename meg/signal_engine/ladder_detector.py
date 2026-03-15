"""
Entry ladder detector.

Detects when a whale is building a position in escalating increments over
time (ladder buying). This pattern indicates growing conviction — the whale
is comfortable adding to their position as they gather more information.

Signal engine role: returns a conviction multiplier in [1.0, 2.0] applied
to the composite score. Each qualifying prior same-direction trade within
the lookback window counts as one "rung" and adds ladder_conviction_per_rung.

  1 rung  → 1.15× (e.g. 3rd trade in a series, ladder_conviction_per_rung=0.15)
  2 rungs → 1.30×
  3 rungs → 1.45×
  ...      → capped at 2.0×

Difference from Gate 3 intent classifier (pre_filter/intent_classifier.py):
  Gate 3 detects SIGNAL_LADDER trade *intent* for filtering/routing decisions.
  This module produces the *multiplier* for score amplification — separate concern.

Data source: trades table (PostgreSQL) via AsyncSession.
  Query: qualified same-wallet, same-market, same-outcome trades within
  config.pre_filter.ladder_window_hours before the current trade's timestamp.
  No Redis dependency — DB is authoritative for historical trade data.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade
from meg.db.models import Trade

logger = structlog.get_logger(__name__)


async def multiplier(
    trade: QualifiedWhaleTrade,
    session: AsyncSession,
    config: MegConfig,
) -> float:
    """
    Return a ladder conviction multiplier in [1.0, 2.0].

    1.0 = no qualified prior same-direction trades within the window (isolated trade).
    >1.0 = prior trades found — each rung adds config.signal.ladder_conviction_per_rung.
    2.0 = hard cap regardless of rung count.

    "Prior trade" = qualified (is_qualified=True) trade by the same wallet in the
    same market and outcome direction, within config.pre_filter.ladder_window_hours,
    with traded_at strictly before the current trade's timestamp.

    Formula: min(1.0 + rungs * ladder_conviction_per_rung, 2.0)
    """
    window_hours = config.pre_filter.ladder_window_hours
    cutoff_dt = datetime.now(tz=timezone.utc) - timedelta(hours=window_hours)
    trade_dt = datetime.fromtimestamp(trade.timestamp_ms / 1000, tz=timezone.utc)

    stmt = (
        select(func.count())
        .select_from(Trade)
        .where(
            Trade.wallet_address == trade.wallet_address,
            Trade.market_id == trade.market_id,
            Trade.outcome == trade.outcome,
            Trade.is_qualified.is_(True),
            Trade.traded_at >= cutoff_dt,
            Trade.traded_at < trade_dt,
        )
    )

    result = await session.execute(stmt)
    rungs: int = result.scalar_one()

    ladder_mult = min(
        1.0 + rungs * config.signal.ladder_conviction_per_rung,
        2.0,
    )

    if rungs > 0:
        logger.debug(
            "ladder_detector.rungs_found",
            wallet=trade.wallet_address,
            market_id=trade.market_id,
            outcome=trade.outcome,
            rungs=rungs,
            multiplier=ladder_mult,
            window_hours=window_hours,
        )

    return ladder_mult
