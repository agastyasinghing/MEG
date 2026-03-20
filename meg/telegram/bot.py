"""
Telegram bot — trade approval flow, alerts, and emergency controls.

Responsibilities:
  - Receive TradeProposal notifications and send approval requests to the
    configured TELEGRAM_APPROVAL_CHAT_ID
  - Route APPROVED / REJECTED responses back to order_router
  - Send alerts for: signal events, risk gate rejections, position opens/closes,
    daily P&L summaries, and system health warnings
  - Provide /pause and /resume commands that halt / resume new proposal execution

In v1, every TradeProposal requires approval before execution. The bot is
the only interface for that approval flow.

Module state (set once in start(), shared across all functions):
  _app            — PTB Application (polling + update dispatcher)
  _chat_id        — TELEGRAM_APPROVAL_CHAT_ID env var value
  _authorized_ids — set of int user IDs allowed to /pause and /resume
                    (empty = no restriction; anyone in the chat may use commands)

Concurrent loops in start():
  ┌──────────────────────────────────────────────────────────────┐
  │ asyncio event loop                                            │
  │                                                               │
  │  PTB updater (background task, non-blocking after await)      │
  │    polls Telegram API → dispatches to handler closures        │
  │                                                               │
  │  _subscriber_loop() (foreground — blocks until cancelled)     │
  │    redis pub/sub → send_approval_request()                    │
  └──────────────────────────────────────────────────────────────┘

PTB handler closures (defined in start(), capture redis + config):
  _cb(update, ctx)      → handle_approval_callback(query, redis, config)
  _pause(update, ctx)   → handle_pause_command(redis, config, user_id)
  _resume(update, ctx)  → handle_resume_command(redis, config, user_id)

Pending proposal lifecycle:
  send_approval_request(proposal, redis, config)
    │
    ├── redis.set("proposal:{id}:pending", json, ex=ttl_seconds)
    └── bot.send_message() with InlineKeyboard [Approve] [Reject]
                │
           operator clicks
                │
  handle_approval_callback(query, redis, config)
    ├── redis.get("proposal:{id}:pending")  ← None? → "expired" reply
    ├── redis.delete(...)                   ← double-click guard (atomic DEL first)
    ├── action == "approve"
    │     order_router.place() → edit message with result
    └── action == "reject"
          edit message "REJECTED"

Env vars:
  TELEGRAM_BOT_TOKEN             — required; bot API token from @BotFather
  TELEGRAM_APPROVAL_CHAT_ID      — required; chat/channel ID for all messages
  TELEGRAM_AUTHORIZED_USER_IDS   — optional; comma-separated int user IDs for
                                   /pause and /resume. Empty = no restriction.
"""
from __future__ import annotations

import asyncio
import os
from typing import Final

import structlog
from pydantic import ValidationError
from redis.asyncio import Redis
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from meg.core import redis_client as _redis_client
from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys, TradeProposal
from meg.execution import order_router

logger = structlog.get_logger(__name__)

# ── Module-level state (set once in start()) ──────────────────────────────────

_app: Application | None = None
_chat_id: str | None = None
_authorized_ids: set[int] = set()

# Reconnect backoff cap for the Redis subscriber loop (seconds).
_MAX_RECONNECT_SLEEP: Final[int] = 60


# ── Public API ────────────────────────────────────────────────────────────────


async def start(redis: Redis, config: MegConfig) -> None:
    """
    Start the Telegram bot and subscribe to CHANNEL_TRADE_PROPOSALS.
    Runs forever as a long-running asyncio task. Call as asyncio.create_task(start(...)).

    Startup sequence:
      1. Read and validate env vars (raises ValueError if required vars are missing)
      2. Build PTB Application with callback + command handlers
      3. initialize() + start() + updater.start_polling() (all non-blocking)
      4. Run _subscriber_loop() — blocks here until task is cancelled

    Raises:
      ValueError   if TELEGRAM_BOT_TOKEN or TELEGRAM_APPROVAL_CHAT_ID are unset
    """
    global _app, _chat_id, _authorized_ids

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

    chat_id = os.environ.get("TELEGRAM_APPROVAL_CHAT_ID")
    if not chat_id:
        raise ValueError("TELEGRAM_APPROVAL_CHAT_ID environment variable not set")
    _chat_id = chat_id

    auth_ids_raw = os.environ.get("TELEGRAM_AUTHORIZED_USER_IDS", "")
    _authorized_ids = {
        int(uid.strip()) for uid in auth_ids_raw.split(",") if uid.strip().isdigit()
    }

    _app = Application.builder().token(token).build()

    # Closures capture redis + config — handlers always operate on current state.
    async def _cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        q = update.callback_query
        if q is None:
            return
        await q.answer()
        await handle_approval_callback(q, redis, config)

    async def _pause(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        uid = update.effective_user.id if update.effective_user else None
        await handle_pause_command(redis, config, user_id=uid)

    async def _resume(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        uid = update.effective_user.id if update.effective_user else None
        await handle_resume_command(redis, config, user_id=uid)

    async def _error_handler(
        update: object, ctx: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.error("bot.telegram_error", error=str(ctx.error))

    _app.add_handler(CallbackQueryHandler(_cb))
    _app.add_handler(CommandHandler("pause", _pause))
    _app.add_handler(CommandHandler("resume", _resume))
    _app.add_error_handler(_error_handler)

    # async with _app calls initialize() on entry and shutdown() on exit.
    # app.start() / app.stop() manage the update processor.
    # updater.start_polling() / updater.stop() manage the Telegram polling task.
    async with _app:
        await _app.start()
        await _app.updater.start_polling(drop_pending_updates=True)
        logger.info(
            "bot.started",
            chat_id=_chat_id,
            authorized_ids=sorted(_authorized_ids),
        )
        try:
            await _subscriber_loop(redis, config)
        finally:
            await _app.updater.stop()
            await _app.stop()


async def send_approval_request(
    proposal: TradeProposal,
    redis: Redis,
    config: MegConfig,
) -> None:
    """
    Store proposal in Redis and send a formatted approval request to the approval chat.

    Attaches APPROVE / REJECT inline keyboard buttons. The proposal is stored
    in Redis so handle_approval_callback() can retrieve it by proposal_id when
    the operator clicks a button.

    Redis key: RedisKeys.pending_proposal(proposal.proposal_id)
    TTL: config.signal.ttl_seconds (default 7200s = 2h)

    Raises RuntimeError if called before start().
    """
    if _app is None or _chat_id is None:
        raise RuntimeError("send_approval_request called before bot.start()")

    await redis.set(
        RedisKeys.pending_proposal(proposal.proposal_id),
        proposal.model_dump_json(),
        ex=config.signal.ttl_seconds,
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Approve",
                    callback_data=f"approve:{proposal.proposal_id}",
                ),
                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject:{proposal.proposal_id}",
                ),
            ]
        ]
    )

    await _app.bot.send_message(
        chat_id=_chat_id,
        text=_format_proposal(proposal),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    logger.info(
        "bot.approval_request_sent",
        proposal_id=proposal.proposal_id,
        market_id=proposal.market_id,
        outcome=proposal.outcome,
        size_usdc=proposal.size_usdc,
    )


async def handle_approval_callback(
    query: CallbackQuery,
    redis: Redis,
    config: MegConfig,
) -> None:
    """
    Handle an APPROVE or REJECT button press from the Telegram inline keyboard.

    callback_data format: "approve:{proposal_id}" | "reject:{proposal_id}"

    Sequence:
      1. Parse callback_data — invalid format → edit message, return
      2. Fetch proposal from Redis — missing/expired → "expired" reply, return
      3. DEL pending key (double-click guard — atomic, before any action)
      4. action=approve → order_router.place() → edit message with result
         action=reject  → edit message "REJECTED"

    Never raises. All exceptions from order_router are caught, logged, and
    shown to the operator via message edit.
    """
    data: str = query.data or ""

    if ":" not in data:
        logger.warning("bot.invalid_callback_data", data=data)
        await query.edit_message_text("⚠️ Invalid callback — unknown format.")
        return

    action, proposal_id = data.split(":", 1)

    # Atomic get+delete: eliminates the TOCTOU race between get and delete.
    # Two concurrent PTB tasks both calling getdel() will see one get the value
    # and one get None — only one proceeds to order_router.place().
    raw = await redis.getdel(RedisKeys.pending_proposal(proposal_id))
    if raw is None:
        logger.info("bot.proposal_expired_or_handled", proposal_id=proposal_id)
        await query.edit_message_text("⏱ Proposal expired or already handled.")
        return

    try:
        proposal = TradeProposal.model_validate_json(raw)
    except (ValidationError, ValueError) as exc:
        logger.error(
            "bot.proposal_deserialization_error",
            proposal_id=proposal_id,
            error=str(exc),
        )
        await query.edit_message_text("❌ Internal error: could not parse proposal.")
        return

    if action == "approve":
        await _execute_approved_proposal(query, proposal, redis, config)
    elif action == "reject":
        logger.info(
            "bot.proposal_rejected",
            proposal_id=proposal_id,
            market_id=proposal.market_id,
        )
        await query.edit_message_text("❌ REJECTED by operator.")
    else:
        logger.warning(
            "bot.unknown_callback_action",
            action=action,
            proposal_id=proposal_id,
        )
        await query.edit_message_text("⚠️ Unknown action.")


async def handle_pause_command(
    redis: Redis,
    config: MegConfig,
    user_id: int | None = None,
) -> None:
    """
    Handle the /pause command. Sets RedisKeys.system_paused() = "1".
    decision_agent reads this key on every signal — bypasses hot-reload latency.

    If TELEGRAM_AUTHORIZED_USER_IDS is non-empty, user_id must be in the set.
    Sends a confirmation alert on success; authorization failure alert on reject.
    """
    if _authorized_ids and (user_id is None or user_id not in _authorized_ids):
        logger.warning("bot.pause_unauthorized", user_id=user_id)
        await send_alert(
            f"⛔ Unauthorized /pause attempt (user {user_id}).", config
        )
        return

    await redis.set(RedisKeys.system_paused(), "1")
    logger.info("bot.system_paused", user_id=user_id)
    await send_alert("⏸ MEG paused — no new proposals will be executed.", config)


async def handle_resume_command(
    redis: Redis,
    config: MegConfig,
    user_id: int | None = None,
) -> None:
    """
    Handle the /resume command. Deletes RedisKeys.system_paused() from Redis.
    decision_agent will resume routing proposals on the next signal event.

    If TELEGRAM_AUTHORIZED_USER_IDS is non-empty, user_id must be in the set.
    Sends a confirmation alert on success; authorization failure alert on reject.
    """
    if _authorized_ids and (user_id is None or user_id not in _authorized_ids):
        logger.warning("bot.resume_unauthorized", user_id=user_id)
        await send_alert(
            f"⛔ Unauthorized /resume attempt (user {user_id}).", config
        )
        return

    await redis.delete(RedisKeys.system_paused())
    logger.info("bot.system_resumed", user_id=user_id)
    await send_alert("▶ MEG resumed — proposals will execute normally.", config)


async def send_alert(message: str, config: MegConfig) -> None:
    """
    Send a plain-text alert to the approval chat.
    Used for: risk rejections, P&L updates, position closures, execution results.

    Safe to call before start() — logs a warning and returns without crashing.
    Exceptions from the Telegram API are caught and logged (never raises).
    """
    if _app is None or _chat_id is None:
        logger.warning("bot.send_alert_before_start", message=message)
        return

    try:
        await _app.bot.send_message(chat_id=_chat_id, text=message)
    except Exception as exc:
        logger.error("bot.send_alert_failed", error=str(exc), message=message[:200])


# ── Internal helpers ──────────────────────────────────────────────────────────


def _format_proposal(proposal: TradeProposal) -> str:
    """
    Format a TradeProposal as an HTML Telegram message for the approval request.

    Trap warning is displayed prominently at the top when present.
    Sub-scores are shown only when the full scores breakdown is available.
    """
    trap_flag = "🚨 <b>TRAP WARNING</b>\n\n" if proposal.trap_warning else ""

    score_lines = ""
    if proposal.scores:
        s = proposal.scores
        score_lines = (
            f"  Lead-lag:    {s.lead_lag:.2f}\n"
            f"  Consensus:   {s.consensus:.2f}\n"
            f"  Kelly conf:  {s.kelly_confidence:.2f}\n"
            f"  Divergence:  {s.divergence:.2f}\n"
            f"  Conviction:  {s.conviction_ratio:.2f}\n"
            f"  Arch. mult:  {s.archetype_multiplier:.2f}×\n"
            f"  Ladder mult: {s.ladder_multiplier:.2f}×\n"
        )

    half_life = (
        f"{proposal.estimated_half_life_minutes:.0f} min"
        if proposal.estimated_half_life_minutes > 0
        else "unknown"
    )

    wallets = proposal.contributing_wallets
    wallets_str = (
        ", ".join(f"<code>{w[:10]}…</code>" for w in wallets[:3])
        + ("…" if len(wallets) > 3 else "")
        if wallets
        else "—"
    )

    return (
        f"{trap_flag}"
        f"📋 <b>Trade Proposal</b>\n\n"
        f"Market:     <code>{proposal.market_id}</code>\n"
        f"Outcome:    <b>{proposal.outcome}</b>\n"
        f"Size:       <b>{proposal.size_usdc:.2f} USDC</b>\n"
        f"Entry:      {proposal.limit_price:.4f}\n"
        f"Whale fill: {proposal.market_price_at_signal:.4f}\n"
        f"Score:      <b>{proposal.composite_score:.3f}</b>\n"
        f"Saturation: {proposal.saturation_score:.2f}\n"
        f"Half-life:  {half_life}\n"
        f"\n<b>Sub-scores:</b>\n{score_lines}"
        f"Whales: {wallets_str}\n"
        f"\n<i>Proposal {proposal.proposal_id[:8]}…</i>"
    )


async def _execute_approved_proposal(
    query: CallbackQuery,
    proposal: TradeProposal,
    redis: Redis,
    config: MegConfig,
) -> None:
    """
    Call order_router.place() for an approved proposal and edit the Telegram message.

    Outcomes:
      accepted=True  → edit to ✅ APPROVED with order_id + slippage
      accepted=False → edit to ⚠️ gate rejected with reason (no crash)
      raises         → log error + edit to ❌ error message (no crash)

    Sends a follow-up send_alert on successful placement for audit trail.
    """
    try:
        result = await order_router.place(proposal, redis, config, session=None)
    except Exception as exc:
        logger.error(
            "bot.order_router_exception",
            proposal_id=proposal.proposal_id,
            error=str(exc),
        )
        await query.edit_message_text(
            f"❌ Execution error — check logs.\n"
            f"<i>Proposal {proposal.proposal_id[:8]}…</i>",
            parse_mode="HTML",
        )
        return

    if result["accepted"]:
        text = (
            f"✅ <b>APPROVED</b> — order <code>{result['order_id']}</code> placed.\n"
            f"Slippage: {result['estimated_slippage']:.4f}\n"
            f"<i>Proposal {proposal.proposal_id[:8]}…</i>"
        )
        await send_alert(
            f"Order placed: {result['order_id']} | "
            f"{proposal.market_id} | {proposal.outcome} "
            f"{proposal.size_usdc:.0f} USDC",
            config,
        )
    else:
        text = (
            f"⚠️ Approved but gate rejected: {result['reason']}\n"
            f"<i>Proposal {proposal.proposal_id[:8]}…</i>"
        )
        logger.info(
            "bot.order_gate_rejected",
            proposal_id=proposal.proposal_id,
            reason=result["reason"],
        )

    await query.edit_message_text(text, parse_mode="HTML")


async def _subscriber_loop(redis: Redis, config: MegConfig) -> None:
    """
    Subscribe to CHANNEL_TRADE_PROPOSALS and forward proposals to send_approval_request().

    Reconnect loop:
      - ConnectionError: log warning, wait with exponential backoff (cap 60s), retry
      - ValidationError / bad JSON: log error, skip message, continue (loop never crashes)
      - asyncio.CancelledError: re-raise (clean shutdown signal)

    Backoff resets to 0 on each successfully received message.
    """
    from redis.exceptions import ConnectionError as RedisConnectionError

    attempt = 0
    while True:
        try:
            async for message in _redis_client.subscribe(
                redis, RedisKeys.CHANNEL_TRADE_PROPOSALS
            ):
                attempt = 0  # reset backoff on successful delivery
                try:
                    proposal = TradeProposal.model_validate_json(message)
                except (ValidationError, ValueError) as exc:
                    logger.error(
                        "bot.invalid_proposal_message",
                        error=str(exc),
                        raw=message[:200] if isinstance(message, str) else repr(message[:200]),
                    )
                    continue

                try:
                    await send_approval_request(proposal, redis, config)
                except Exception as exc:
                    logger.error(
                        "bot.send_approval_request_failed",
                        proposal_id=proposal.proposal_id,
                        error=str(exc),
                    )

        except asyncio.CancelledError:
            raise
        except RedisConnectionError as exc:
            delay = min(2 ** attempt, _MAX_RECONNECT_SLEEP)
            logger.warning(
                "bot.redis_subscriber_disconnected",
                error=str(exc),
                reconnect_in_seconds=delay,
                attempt=attempt,
            )
            await asyncio.sleep(delay)
            attempt += 1
