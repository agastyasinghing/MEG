"""
Telegram bot — trade approval flow, alerts, and emergency controls.

Responsibilities:
  - Receive TradeProposal notifications and send approval requests to the
    configured TELEGRAM_APPROVAL_CHAT_ID
  - Route APPROVED / REJECTED responses back to order_router
  - Receive AlertMessage notifications and forward them as plain-text alerts
  - Provide /pause, /resume, and /reject commands for operator control

In v1, every TradeProposal requires approval before execution. The bot is
the only interface for that approval flow.

Module state (set once in start(), shared across all functions):
  _app            — PTB Application (polling + update dispatcher)
  _chat_id        — TELEGRAM_APPROVAL_CHAT_ID env var value
  _authorized_ids — set of int user IDs allowed to /pause, /resume, /reject,
                    and inline Approve/Reject buttons.
                    (empty = no restriction; anyone in the chat may act)

Concurrent loops in start() — run together via asyncio.TaskGroup:
  ┌──────────────────────────────────────────────────────────────────────┐
  │ asyncio event loop                                                    │
  │                                                                       │
  │  PTB updater (background task, non-blocking after await)              │
  │    polls Telegram API → dispatches to handler closures                │
  │                                                                       │
  │  TaskGroup (two tasks run concurrently, cancel together on shutdown): │
  │    _subscriber_loop()  CHANNEL_TRADE_PROPOSALS → send_approval_request│
  │    _alert_loop()       CHANNEL_BOT_ALERTS      → send_alert()         │
  └──────────────────────────────────────────────────────────────────────┘

PTB handler closures (defined in start(), capture redis + config):
  _cb(update, ctx)      → auth check → handle_approval_callback(query, redis, config)
  _pause(update, ctx)   → handle_pause_command(redis, config, user_id)
  _resume(update, ctx)  → handle_resume_command(redis, config, user_id)
  _reject(update, ctx)  → handle_reject_command(redis, config, user_id, args)

Pending proposal lifecycle:
  send_approval_request(proposal, redis, config)
    │
    ├── redis.set("proposal:{id}:pending", json, ex=ttl_seconds)
    └── bot.send_message() with InlineKeyboard [Approve] [Reject]
                │
           operator clicks (or uses /reject {id} {reason})
                │
  handle_approval_callback(query, redis, config)          ← inline button path
    ├── redis.getdel("proposal:{id}:pending") ← None? → "expired" reply
    ├── action == "approve"
    │     order_router.place() → edit message with result
    └── action == "reject"
          log rejection_reason="rejected_via_button" → edit message "REJECTED"

  handle_reject_command(redis, config, user_id, args)     ← /reject command path
    ├── auth check
    ├── parse proposal_id + reason from args
    ├── redis.getdel("proposal:{id}:pending") ← None? → "not found" alert
    └── log rejection_reason + send confirmation alert

Alert delivery lifecycle:
  any_layer publishes AlertMessage to CHANNEL_BOT_ALERTS
    │
  _alert_loop() receives message
    ├── parse AlertMessage
    ├── urgent=True  → prefix with "🚨 URGENT: "
    └── send_alert(text, config)

Env vars:
  TELEGRAM_BOT_TOKEN             — required; bot API token from @BotFather
  TELEGRAM_APPROVAL_CHAT_ID      — required; chat/channel ID for all messages
  TELEGRAM_AUTHORIZED_USER_IDS   — optional; comma-separated int user IDs for
                                   /pause, /resume, /reject, and inline buttons.
                                   Empty = no restriction.
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
from meg.core.events import AlertMessage, RedisKeys, TradeProposal
from meg.execution import order_router

logger = structlog.get_logger(__name__)

# ── Module-level state (set once in start()) ──────────────────────────────────

_app: Application | None = None
_chat_id: str | None = None
_authorized_ids: set[int] = set()

# Reconnect backoff cap for the Redis subscriber loop (seconds).
_MAX_RECONNECT_SLEEP: Final[int] = 60


def _is_authorized(uid: int | None) -> bool:
    """Return True if uid may take operator actions (approve, reject, pause, resume).

    When _authorized_ids is empty (no restriction configured), everyone is allowed.
    When non-empty, uid must be present and in the set.
    """
    return not _authorized_ids or (uid is not None and uid in _authorized_ids)


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
        # Auth check — effective_user may be None for forwarded messages or
        # channel posts; _is_authorized() treats None as unauthorized when
        # _authorized_ids is non-empty.
        uid = update.effective_user.id if update.effective_user else None
        if not _is_authorized(uid):
            logger.warning("bot.callback_unauthorized", user_id=uid)
            await q.edit_message_text("⛔ Not authorized to approve or reject.")
            return
        await handle_approval_callback(q, redis, config)

    async def _pause(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        uid = update.effective_user.id if update.effective_user else None
        await handle_pause_command(redis, config, user_id=uid)

    async def _resume(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        uid = update.effective_user.id if update.effective_user else None
        await handle_resume_command(redis, config, user_id=uid)

    async def _reject(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        uid = update.effective_user.id if update.effective_user else None
        await handle_reject_command(redis, config, user_id=uid, args=list(ctx.args or []))

    async def _error_handler(
        update: object, ctx: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.error("bot.telegram_error", error=str(ctx.error))

    _app.add_handler(CallbackQueryHandler(_cb))
    _app.add_handler(CommandHandler("pause", _pause))
    _app.add_handler(CommandHandler("resume", _resume))
    _app.add_handler(CommandHandler("reject", _reject))
    _app.add_error_handler(_error_handler)

    # async with _app calls initialize() on entry and shutdown() on exit.
    # app.start() / app.stop() manage the update processor.
    # updater.start_polling() / updater.stop() manage the Telegram polling task.
    # TaskGroup runs _subscriber_loop + _alert_loop concurrently; if either
    # raises (e.g. CancelledError on task cancellation), the other is also
    # cancelled and the finally block cleans up PTB.
    async with _app:
        await _app.start()
        await _app.updater.start_polling(drop_pending_updates=True)
        logger.info(
            "bot.started",
            chat_id=_chat_id,
            authorized_ids=sorted(_authorized_ids),
        )
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(_subscriber_loop(redis, config))
                tg.create_task(_alert_loop(redis, config))
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
            rejection_reason="rejected_via_button",
            via="inline_button",
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


async def handle_reject_command(
    redis: Redis,
    config: MegConfig,
    user_id: int | None = None,
    args: list[str] | None = None,
) -> None:
    """
    Handle the /reject {proposal_id} {reason...} command.

    Usage: /reject abc12345 price moved too far from whale fill

    All text after the proposal_id is joined as the rejection reason.
    If no reason is given, defaults to "no_reason_given".

    The rejection reason is logged via structlog (log-only in v1; durable storage
    in signal_outcomes table is a deferred TODO — see TODOS.md).

    Authorized users only (same gate as /pause and /resume).
    """
    if not _is_authorized(user_id):
        logger.warning("bot.reject_unauthorized", user_id=user_id)
        await send_alert(
            f"⛔ Unauthorized /reject attempt (user {user_id}).", config
        )
        return

    if not args:
        await send_alert("⚠️ Usage: /reject {proposal_id} {reason}", config)
        return

    proposal_id = args[0]
    reason = " ".join(args[1:]) if len(args) > 1 else "no_reason_given"

    raw = await redis.getdel(RedisKeys.pending_proposal(proposal_id))
    if raw is None:
        await send_alert(
            f"⚠️ Proposal {proposal_id[:12]}… not found or already handled.", config
        )
        return

    logger.info(
        "bot.proposal_rejected",
        proposal_id=proposal_id,
        rejection_reason=reason,
        user_id=user_id,
        via="command",
    )
    await send_alert(
        f"❌ Proposal {proposal_id[:8]}… rejected by operator.\nReason: {reason}",
        config,
    )


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

    Fields shown (PRD §9.6 Trade Approval Queue):
      market_id, outcome, size, current_price, entry distance from whale fill,
      composite score + breakdown, estimated slippage, saturation score, trap warning.

    Trap warning is displayed prominently at the top when present.
    Sub-scores are shown only when the full scores breakdown is available.
    entry_distance_pct is computed from existing fields — no schema read needed.
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

    # Entry distance: how far our proposed entry is from the whale's fill price.
    # Non-zero only when market moved between whale fill and our proposal build.
    entry_dist_pct = (
        abs(proposal.limit_price - proposal.market_price_at_signal)
        / proposal.market_price_at_signal
        * 100
        if proposal.market_price_at_signal > 0
        else 0.0
    )

    current_price_str = (
        f"{proposal.current_price:.4f}" if proposal.current_price > 0 else "—"
    )
    slippage_str = (
        f"{proposal.estimated_slippage:.2%}" if proposal.estimated_slippage > 0 else "—"
    )

    return (
        f"{trap_flag}"
        f"📋 <b>Trade Proposal</b>\n\n"
        f"Market:       <code>{proposal.market_id}</code>\n"
        f"Outcome:      <b>{proposal.outcome}</b>\n"
        f"Size:         <b>{proposal.size_usdc:.2f} USDC</b>\n"
        f"Current:      {current_price_str}\n"
        f"Whale fill:   {proposal.market_price_at_signal:.4f}\n"
        f"Entry:        {proposal.limit_price:.4f} "
        f"(<b>{entry_dist_pct:.1f}%</b> from fill)\n"
        f"Est. slip:    {slippage_str}\n"
        f"Score:        <b>{proposal.composite_score:.3f}</b>\n"
        f"Saturation:   {proposal.saturation_score:.2f}\n"
        f"Half-life:    {half_life}\n"
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


async def _alert_loop(redis: Redis, config: MegConfig) -> None:
    """
    Subscribe to CHANNEL_BOT_ALERTS and forward AlertMessages to send_alert().

    Publishers: trap_detector, position_manager, decision_agent (circuit breaker).
    urgent=True alerts are prefixed with "🚨 URGENT:" in the Telegram message.

    Reconnect loop: mirrors _subscriber_loop reconnect pattern.
      - ConnectionError: log warning, exponential backoff (cap 60s), retry
      - ValidationError / bad JSON: log error, skip message, continue (loop never crashes)
      - asyncio.CancelledError: re-raise (clean shutdown signal from TaskGroup)
    """
    from redis.exceptions import ConnectionError as RedisConnectionError

    attempt = 0
    while True:
        try:
            async for message in _redis_client.subscribe(
                redis, RedisKeys.CHANNEL_BOT_ALERTS
            ):
                attempt = 0  # reset backoff on successful delivery
                try:
                    alert = AlertMessage.model_validate_json(message)
                except (ValidationError, ValueError) as exc:
                    logger.error(
                        "bot.invalid_alert_message",
                        error=str(exc),
                        raw=message[:200] if isinstance(message, str) else repr(message[:200]),
                    )
                    continue

                prefix = "🚨 URGENT: " if alert.urgent else ""
                await send_alert(f"{prefix}{alert.message}", config)

        except asyncio.CancelledError:
            raise
        except RedisConnectionError as exc:
            delay = min(2 ** attempt, _MAX_RECONNECT_SLEEP)
            logger.warning(
                "bot.alert_subscriber_disconnected",
                error=str(exc),
                reconnect_in_seconds=delay,
                attempt=attempt,
            )
            await asyncio.sleep(delay)
            attempt += 1


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
