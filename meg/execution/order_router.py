"""
Order router.

The only module in MEG that submits orders to the Polymarket CLOB.
Handles the full entry pipeline: entry_filter → slippage_guard → place order
→ record position. cancel() and handle_fill() are stubbed for Phase 7.5.

Paper trading mode: when config.risk.paper_trading is True, logs the intended
order with a [PAPER] prefix and returns a synthetic result without submitting.

In v1, order_router.place() is only called after human approval via Telegram.
Never call this directly from signal_engine or agent_core.

Execution pipeline:
  ┌────────────────────────────────────────────────────────────────────┐
  │ place(proposal, redis, config, session=None)                        │
  │                                                                      │
  │  entry_filter.check()  ──FAIL──► {accepted: False, reason, ...}    │
  │         │                                                            │
  │        PASS                                                          │
  │         │                                                            │
  │  slippage_guard.check() ──FAIL──► {accepted: False, reason, ...}   │
  │         │                                                            │
  │        PASS                                                          │
  │         │                                                            │
  │  _place_with_retry()                                                 │
  │    clob_client.place_order()  ──transport error──► retry (max 3)   │
  │                               ──other error──────► re-raise         │
  │         │                                                            │
  │  position_manager.open_position() (Redis + DB best-effort)          │
  │         │                                                            │
  │  return {accepted: True, order_id, estimated_slippage, reason: ""}  │
  └────────────────────────────────────────────────────────────────────┘

Retry policy (place_order only):
  Retryable:     ConnectionError, OSError
                 (transport-level: request never reached the CLOB)
                 Note: asyncio.TimeoutError excluded — ambiguous between connect-timeout
                 (safe) and read-timeout (CLOB may have accepted; retry = duplicate order).
  Not retryable: all other exceptions — re-raise immediately.
  Max attempts:  3
  Backoff:       exponential — asyncio.sleep(2 ** attempt) after each failure
                 attempt 0: sleep(1s), attempt 1: sleep(2s), attempt 2: raise

  IMPORTANT: only transport errors are retried to avoid duplicate order
  placement. If the CLOB accepted the order and an error occurred on the
  response path, retrying would place a second order.

TODO: limit timeout (limit_timeout_seconds) — cancel + re-place as taker order
if unfilled after limit_timeout_seconds. Requires fill detection (CLOB websocket
or get_open_orders() polling). Deferred to Phase 7.5. See TODOS.md.
"""
from __future__ import annotations

import asyncio

import structlog
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from meg.agent_core import position_manager
from meg.core.config_loader import MegConfig
from meg.core.events import TradeProposal
from meg.data_layer import clob_client
from meg.execution import entry_filter, slippage_guard

logger = structlog.get_logger(__name__)

# Transport-level errors that are safe to retry — request never reached the CLOB.
# Non-transport errors (bad request, auth failure, CLOB logic error) re-raise immediately.
#
# asyncio.TimeoutError is intentionally excluded: it can fire after the CLOB has
# accepted and processed the order (read/response timeout, not just connect timeout).
# Retrying on asyncio.TimeoutError would place a second order. If connect-phase
# timeout granularity is needed, inspect py-clob-client's exception hierarchy at
# that time (see TODOS.md: "Live order placement auth in clob_client").
_RETRYABLE = (ConnectionError, OSError)


async def place(
    proposal: TradeProposal,
    redis: Redis,
    config: MegConfig,
    session: AsyncSession | None = None,
) -> dict:
    """
    Execute the full order placement sequence (see module docstring).

    Returns a dict:
      accepted:           bool  — False if any gate rejected or all retries failed
      reason:             str   — empty on success; gate/error message on failure
      order_id:           str | None — filled on success
      estimated_slippage: float — from slippage_guard (0.0 if entry_filter rejected)

    Raises on unrecoverable execution error after retries exhausted.
    Never raises on gate rejection — those are returned as accepted=False.
    """
    # ── Gate 1: entry distance ────────────────────────────────────────────
    ef_passed, ef_reason = await entry_filter.check(proposal, redis, config)
    if not ef_passed:
        logger.info(
            "order_router.entry_filter_rejected",
            proposal_id=proposal.proposal_id,
            reason=ef_reason,
        )
        return {
            "accepted": False,
            "reason": ef_reason,
            "order_id": None,
            "estimated_slippage": 0.0,
        }

    # ── Gate 2: spread + price drift ─────────────────────────────────────
    sg_passed, sg_reason, estimated_slippage = await slippage_guard.check(
        proposal, redis, config
    )
    if not sg_passed:
        logger.info(
            "order_router.slippage_guard_rejected",
            proposal_id=proposal.proposal_id,
            reason=sg_reason,
            estimated_slippage=estimated_slippage,
        )
        return {
            "accepted": False,
            "reason": sg_reason,
            "order_id": None,
            "estimated_slippage": estimated_slippage,
        }

    # ── Place order (3x retry on transport errors) ────────────────────────
    order_id = await _place_with_retry(proposal, config)

    # ── Record position ───────────────────────────────────────────────────
    # Compute TP/SL prices from entry price + config percentages.
    # Direction-aware: for YES positions price must rise to hit TP / fall to SL.
    # For NO positions the YES price must fall to hit TP / rise to SL.
    entry_price = proposal.limit_price
    if proposal.outcome == "YES":
        take_profit_price = entry_price * (1.0 + config.position.take_profit_pct)
        stop_loss_price = entry_price * (1.0 - config.position.stop_loss_pct)
    else:
        # NO position: profit when YES price falls (NO price rises)
        take_profit_price = entry_price * (1.0 - config.position.take_profit_pct)
        stop_loss_price = entry_price * (1.0 + config.position.stop_loss_pct)

    await position_manager.open_position(
        market_id=proposal.market_id,
        outcome=proposal.outcome,
        size_usdc=proposal.size_usdc,
        entry_price=entry_price,
        signal_id=proposal.signal_id,
        contributing_wallets=proposal.contributing_wallets,
        # TradeProposal does not carry whale_archetype — defaults to INFORMATION.
        # Forward this field through TradeProposal in a future schema update.
        whale_archetype="INFORMATION",
        saturation_score=proposal.saturation_score,
        take_profit_price=take_profit_price,
        stop_loss_price=stop_loss_price,
        redis=redis,
        session=session,
    )

    logger.info(
        "order_router.placed",
        proposal_id=proposal.proposal_id,
        market_id=proposal.market_id,
        outcome=proposal.outcome,
        order_id=order_id,
        size_usdc=proposal.size_usdc,
        entry_price=entry_price,
        estimated_slippage=estimated_slippage,
        paper=config.risk.paper_trading,
    )

    return {
        "accepted": True,
        "reason": "",
        "order_id": order_id,
        "estimated_slippage": estimated_slippage,
    }


async def cancel(order_id: str, redis: Redis, config: MegConfig) -> bool:
    """
    Cancel an open order. Returns True if successfully cancelled.
    Updates position_manager if position is fully cancelled.
    """
    raise NotImplementedError("order_router.cancel")


async def handle_fill(
    order_id: str,
    fill_size_usdc: float,
    fill_price: float,
    redis: Redis,
) -> None:
    """
    Process an order fill event from the CLOB websocket.
    Updates position_manager with the actual fill details.
    Handles partial fills by tracking remaining open quantity.
    """
    raise NotImplementedError("order_router.handle_fill")


# ── Internal helpers ──────────────────────────────────────────────────────────


async def _place_with_retry(proposal: TradeProposal, config: MegConfig) -> str:
    """
    Call clob_client.place_order() with exponential backoff on transport errors.

    Retryable errors (request never reached CLOB):
      asyncio.TimeoutError, ConnectionError, OSError

    Non-retryable errors (CLOB responded — even with an error): re-raise immediately.
    Re-raising avoids duplicate orders when the CLOB accepted the request but the
    response was lost (retrying would place a second order).

    Backoff: attempt 0 → sleep(1s), attempt 1 → sleep(2s), attempt 2 → raise.
    """
    for attempt in range(3):
        try:
            return await clob_client.place_order(
                market_id=proposal.market_id,
                outcome=proposal.outcome,
                # TODO: validate side mapping for NO outcome against py-clob-client
                # before live mode — "BUY" may not be correct for NO positions.
                side="BUY",
                size_usdc=proposal.size_usdc,
                limit_price=proposal.limit_price,
                config=config,
            )
        except _RETRYABLE as exc:
            # asyncio.TimeoutError is a subclass of OSError in Python 3.11+ —
            # re-raise it immediately. A timeout may fire after the CLOB accepted
            # the order (read timeout); retrying would place a duplicate order.
            if isinstance(exc, asyncio.TimeoutError):
                raise
            if attempt == 2:
                logger.error(
                    "order_router.place_order_failed",
                    proposal_id=proposal.proposal_id,
                    attempt=attempt,
                    error=str(exc),
                    note="max retries exhausted",
                )
                raise
            delay = 2 ** attempt  # 1s after attempt 0, 2s after attempt 1
            logger.warning(
                "order_router.place_order_retrying",
                proposal_id=proposal.proposal_id,
                attempt=attempt,
                delay=delay,
                error=str(exc),
            )
            await asyncio.sleep(delay)

    raise RuntimeError("unreachable")  # pragma: no cover
