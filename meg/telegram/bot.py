"""
Telegram bot — trade approval flow, alerts, and emergency controls.

Responsibilities:
  - Receive TradeProposal notifications and send approval requests to the
    configured TELEGRAM_APPROVAL_CHAT_ID
  - Route APPROVED / REJECTED responses back to order_router
  - Send alerts for: signal events, risk gate rejections, position opens/closes,
    daily P&L summaries, and system health warnings
  - Provide an emergency PAUSE command that halts all new proposals instantly

In v1, every TradeProposal requires approval before execution. The bot is
the only interface for that approval flow.
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import TradeProposal


async def start(redis: Redis, config: MegConfig) -> None:
    """
    Start the Telegram bot and subscribe to CHANNEL_TRADE_PROPOSALS.
    Runs forever as a long-running asyncio task.
    """
    raise NotImplementedError("bot.start")


async def send_approval_request(proposal: TradeProposal, config: MegConfig) -> None:
    """
    Send a formatted approval request message to the approval chat.
    Message includes: market, outcome, size, signal score, entry price, rationale.
    Attaches APPROVE / REJECT inline keyboard buttons.
    """
    raise NotImplementedError("bot.send_approval_request")


async def send_alert(message: str, config: MegConfig) -> None:
    """
    Send a plain-text alert to the approval chat.
    Used for: risk rejections, P&L updates, position closures, errors.
    """
    raise NotImplementedError("bot.send_alert")


async def handle_approval_callback(
    callback_data: str,
    proposal_id: str,
    redis: Redis,
    config: MegConfig,
) -> None:
    """
    Handle an APPROVE or REJECT button press from the Telegram inline keyboard.
    On APPROVE: trigger order_router.place().
    On REJECT: update proposal status and log.
    """
    raise NotImplementedError("bot.handle_approval_callback")


async def handle_pause_command(redis: Redis, config: MegConfig) -> None:
    """
    Handle the /pause command. Sets a global pause flag in Redis that prevents
    new TradeProposals from being generated until /resume is called.
    """
    raise NotImplementedError("bot.handle_pause_command")
