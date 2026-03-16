"""
Entry distance filter.

Final re-check immediately before order submission. Between human approval
and order placement, the market may have moved. If the current price has
drifted too far from the whale's entry price, abort the trade.

This is the last line of defence before money leaves the account.

Direction-aware check against config.entry.max_entry_distance_pct.
Reference price: proposal.market_price_at_signal (whale's fill price —
documented in events.py as "base for entry distance").

  YES (buy): current_price <= signal_price * (1 + max_entry_distance_pct)
             Rejects if YES price has risen too far above whale's entry
             (we'd be chasing a move that's already happened).

  NO  (buy): current_price >= signal_price * (1 - max_entry_distance_pct)
             Rejects if YES price has dropped too far below whale's entry
             (the YES correction already happened; our NO edge is gone).

Decision tree:
  ┌─────────────────────────────────────────────────────────────┐
  │ get_current_price(market_id, redis)                          │
  │   key present → float                                        │
  │   key absent  → ValueError("no_price_data:...")             │
  │                                                              │
  │ check(proposal, redis, config)                               │
  │   Redis miss      → (False, "no_price_data:...")            │
  │   signal_price=0  → (False, "no_signal_price:...")          │
  │   YES, within     → (True,  "")                             │
  │   YES, too far    → (False, "entry_distance_exceeded:...")  │
  │   YES, boundary   → (True,  "")  [inclusive]                │
  │   NO,  within     → (True,  "")                             │
  │   NO,  too far    → (False, "entry_distance_exceeded:...")  │
  └─────────────────────────────────────────────────────────────┘
"""
from __future__ import annotations

import structlog
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, TradeProposal

logger = structlog.get_logger(__name__)


async def get_current_price(market_id: str, redis: Redis) -> float:
    """
    Return the current mid price for a market from the Redis cache.

    Raises ValueError if the key is absent — CLOBMarketFeed has not yet
    polled this market, or the key has expired. Callers must handle this
    explicitly: unknown price = fail closed.
    """
    raw = await redis.get(RedisKeys.market_mid_price(market_id))
    if raw is None:
        raise ValueError(f"no_price_data: market:{market_id}:mid_price absent")
    return float(raw)


async def check(
    proposal: TradeProposal,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """
    Return (True, "") if current price is within config.entry.max_entry_distance_pct
    of proposal.market_price_at_signal (the whale's fill price).
    Return (False, reason) if the market has drifted beyond the threshold.

    Called immediately before order_router.place(), not before Telegram approval.
    Fail-closed: missing Redis data → rejection.
    """
    try:
        current_price = await get_current_price(proposal.market_id, redis)
    except ValueError as exc:
        logger.warning(
            "entry_filter.no_price_data",
            market_id=proposal.market_id,
            proposal_id=proposal.proposal_id,
        )
        return False, str(exc)

    signal_price = proposal.market_price_at_signal
    threshold = config.entry.max_entry_distance_pct

    # Fail-closed: signal_price=0.0 means market_price_at_signal was never set.
    # Without a reference price the distance check is undefined — reject.
    if signal_price <= 0.0:
        return False, "no_signal_price: market_price_at_signal unset or zero"

    if proposal.outcome == "YES":
        # Buying YES: reject if price has risen too far above whale's entry
        passed = current_price <= signal_price * (1.0 + threshold)
    else:
        # Buying NO: reject if YES price has dropped too far below whale's entry
        passed = current_price >= signal_price * (1.0 - threshold)

    if not passed:
        reason = (
            f"entry_distance_exceeded: current={current_price:.4f} "
            f"signal={signal_price:.4f} threshold={threshold:.4f} "
            f"outcome={proposal.outcome}"
        )
        logger.warning(
            "entry_filter.rejected",
            market_id=proposal.market_id,
            proposal_id=proposal.proposal_id,
            current_price=current_price,
            signal_price=signal_price,
            threshold=threshold,
            outcome=proposal.outcome,
        )
        return False, reason

    return True, ""
