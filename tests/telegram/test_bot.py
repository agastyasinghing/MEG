"""
Tests for meg/telegram/bot.py.

Coverage map:
  send_approval_request         — message content, chat_id, keyboard, Redis TTL
  handle_approval_callback      — approve success, gate rejection, exception,
                                   reject, expired key, double-click guard
  handle_pause_command          — sets Redis key, auth check
  handle_resume_command         — deletes Redis key, auth check
  send_alert                    — delegates to bot.send_message
  send_alert before start()     — no crash, just logs
  _subscriber_loop              — invalid JSON skip, ConnectionError reconnect
"""
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

import meg.telegram.bot as bot_module
from meg.core.events import RedisKeys

from .conftest import make_mock_query, make_proposal


# ── send_approval_request ─────────────────────────────────────────────────────


async def test_send_approval_request_message_contains_key_fields(
    mock_redis, test_config, mock_bot_app
):
    """Message body must include market_id, outcome, size, composite score."""
    proposal = make_proposal(
        market_id="mkt_abc123",
        outcome="YES",
        size_usdc=250.0,
        composite_score=0.81,
    )

    await bot_module.send_approval_request(proposal, mock_redis, test_config)

    call_kwargs = mock_bot_app.bot.send_message.call_args.kwargs
    text: str = call_kwargs["text"]
    assert "mkt_abc123" in text
    assert "YES" in text
    assert "250.00" in text
    assert "0.810" in text


async def test_send_approval_request_sends_to_correct_chat(
    mock_redis, test_config, mock_bot_app
):
    """Message must be sent to TELEGRAM_APPROVAL_CHAT_ID (bot._chat_id)."""
    proposal = make_proposal()

    await bot_module.send_approval_request(proposal, mock_redis, test_config)

    call_kwargs = mock_bot_app.bot.send_message.call_args.kwargs
    assert call_kwargs["chat_id"] == "test_chat_id"


async def test_send_approval_request_attaches_two_button_keyboard(
    mock_redis, test_config, mock_bot_app
):
    """Inline keyboard must have exactly 2 buttons: Approve and Reject."""
    proposal = make_proposal()

    await bot_module.send_approval_request(proposal, mock_redis, test_config)

    call_kwargs = mock_bot_app.bot.send_message.call_args.kwargs
    keyboard = call_kwargs["reply_markup"]
    buttons = keyboard.inline_keyboard[0]
    assert len(buttons) == 2
    assert buttons[0].callback_data == f"approve:{proposal.proposal_id}"
    assert buttons[1].callback_data == f"reject:{proposal.proposal_id}"


async def test_send_approval_request_stores_proposal_in_redis_with_ttl(
    mock_redis, test_config, mock_bot_app
):
    """Proposal JSON must be stored in Redis with the correct TTL."""
    proposal = make_proposal()
    await bot_module.send_approval_request(proposal, mock_redis, test_config)

    raw = await mock_redis.get(RedisKeys.pending_proposal(proposal.proposal_id))
    assert raw is not None

    ttl = await mock_redis.ttl(RedisKeys.pending_proposal(proposal.proposal_id))
    assert ttl > 0
    assert ttl <= test_config.signal.ttl_seconds


async def test_send_approval_request_raises_before_start(mock_redis, test_config):
    """Calling send_approval_request before start() must raise RuntimeError."""
    bot_module._app = None
    bot_module._chat_id = None
    proposal = make_proposal()

    with pytest.raises(RuntimeError, match="before bot.start"):
        await bot_module.send_approval_request(proposal, mock_redis, test_config)


# ── handle_approval_callback — APPROVE ───────────────────────────────────────


async def test_handle_approval_callback_approve_success(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Approve path: calls order_router.place, edits message to APPROVED."""
    proposal = make_proposal()
    await mock_redis.set(
        RedisKeys.pending_proposal(proposal.proposal_id),
        proposal.model_dump_json(),
        ex=3600,
    )
    mock_place = AsyncMock(
        return_value={
            "accepted": True,
            "order_id": "order-xyz-001",
            "estimated_slippage": 0.005,
            "reason": "",
        }
    )
    mocker.patch("meg.telegram.bot.order_router.place", mock_place)

    query = make_mock_query(f"approve:{proposal.proposal_id}")
    await bot_module.handle_approval_callback(query, mock_redis, test_config)

    mock_place.assert_called_once()
    edit_text: str = query.edit_message_text.call_args.args[0]
    assert "APPROVED" in edit_text
    assert "order-xyz-001" in edit_text


async def test_handle_approval_callback_approve_gate_rejected(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Gate rejection: accepted=False → edit shows gate reason, no crash."""
    proposal = make_proposal()
    await mock_redis.set(
        RedisKeys.pending_proposal(proposal.proposal_id),
        proposal.model_dump_json(),
        ex=3600,
    )
    mocker.patch(
        "meg.telegram.bot.order_router.place",
        AsyncMock(
            return_value={
                "accepted": False,
                "order_id": None,
                "estimated_slippage": 0.0,
                "reason": "entry_distance_exceeded",
            }
        ),
    )

    query = make_mock_query(f"approve:{proposal.proposal_id}")
    await bot_module.handle_approval_callback(query, mock_redis, test_config)

    edit_text: str = query.edit_message_text.call_args.args[0]
    assert "gate rejected" in edit_text
    assert "entry_distance_exceeded" in edit_text


async def test_handle_approval_callback_approve_order_router_exception(
    mock_redis, test_config, mock_bot_app, mocker
):
    """order_router raises: edit shows error message, loop does not crash."""
    proposal = make_proposal()
    await mock_redis.set(
        RedisKeys.pending_proposal(proposal.proposal_id),
        proposal.model_dump_json(),
        ex=3600,
    )
    mocker.patch(
        "meg.telegram.bot.order_router.place",
        AsyncMock(side_effect=RuntimeError("clob timeout")),
    )

    query = make_mock_query(f"approve:{proposal.proposal_id}")
    # Must not raise
    await bot_module.handle_approval_callback(query, mock_redis, test_config)

    edit_text: str = query.edit_message_text.call_args.args[0]
    assert "error" in edit_text.lower()


# ── handle_approval_callback — REJECT ────────────────────────────────────────


async def test_handle_approval_callback_reject(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Reject path: does NOT call order_router, edits to REJECTED."""
    proposal = make_proposal()
    await mock_redis.set(
        RedisKeys.pending_proposal(proposal.proposal_id),
        proposal.model_dump_json(),
        ex=3600,
    )
    mock_place = AsyncMock()
    mocker.patch("meg.telegram.bot.order_router.place", mock_place)

    query = make_mock_query(f"reject:{proposal.proposal_id}")
    await bot_module.handle_approval_callback(query, mock_redis, test_config)

    mock_place.assert_not_called()
    edit_text: str = query.edit_message_text.call_args.args[0]
    assert "REJECTED" in edit_text


# ── handle_approval_callback — expired / double-click ────────────────────────


async def test_handle_approval_callback_expired_proposal(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Redis key missing (expired) → reply 'expired', no order_router call."""
    mock_place = AsyncMock()
    mocker.patch("meg.telegram.bot.order_router.place", mock_place)

    query = make_mock_query("approve:nonexistent-proposal-id")
    await bot_module.handle_approval_callback(query, mock_redis, test_config)

    mock_place.assert_not_called()
    edit_text: str = query.edit_message_text.call_args.args[0]
    assert "expired" in edit_text.lower()


async def test_double_click_guard(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Second callback on same proposal_id: key already deleted → no-op."""
    proposal = make_proposal()
    await mock_redis.set(
        RedisKeys.pending_proposal(proposal.proposal_id),
        proposal.model_dump_json(),
        ex=3600,
    )
    mocker.patch(
        "meg.telegram.bot.order_router.place",
        AsyncMock(
            return_value={
                "accepted": True,
                "order_id": "order-001",
                "estimated_slippage": 0.0,
                "reason": "",
            }
        ),
    )

    query1 = make_mock_query(f"approve:{proposal.proposal_id}")
    query2 = make_mock_query(f"approve:{proposal.proposal_id}")

    await bot_module.handle_approval_callback(query1, mock_redis, test_config)
    await bot_module.handle_approval_callback(query2, mock_redis, test_config)

    # order_router called exactly once — second click was a no-op
    place_mock = bot_module.order_router.place  # already patched
    assert place_mock.call_count == 1  # type: ignore[attr-defined]

    # Second query told operator it was already handled
    edit_text: str = query2.edit_message_text.call_args.args[0]
    assert "expired" in edit_text.lower()


async def test_handle_approval_callback_deletes_pending_key(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Pending key must be deleted regardless of approve or reject outcome."""
    proposal = make_proposal()
    await mock_redis.set(
        RedisKeys.pending_proposal(proposal.proposal_id),
        proposal.model_dump_json(),
        ex=3600,
    )
    mocker.patch(
        "meg.telegram.bot.order_router.place",
        AsyncMock(
            return_value={
                "accepted": True,
                "order_id": "order-002",
                "estimated_slippage": 0.0,
                "reason": "",
            }
        ),
    )

    query = make_mock_query(f"approve:{proposal.proposal_id}")
    await bot_module.handle_approval_callback(query, mock_redis, test_config)

    remaining = await mock_redis.get(RedisKeys.pending_proposal(proposal.proposal_id))
    assert remaining is None


# ── handle_pause_command ──────────────────────────────────────────────────────


async def test_handle_pause_command_sets_redis_key(
    mock_redis, test_config, mock_bot_app
):
    """Pause must write '1' to RedisKeys.system_paused()."""
    await bot_module.handle_pause_command(mock_redis, test_config)

    value = await mock_redis.get(RedisKeys.system_paused())
    assert value == "1"


async def test_handle_pause_command_unauthorized(
    mock_redis, test_config, mock_bot_app
):
    """User not in authorized_ids must NOT set the pause flag."""
    bot_module._authorized_ids = {99999}
    try:
        await bot_module.handle_pause_command(mock_redis, test_config, user_id=12345)
    finally:
        bot_module._authorized_ids = set()

    value = await mock_redis.get(RedisKeys.system_paused())
    assert value is None


# ── handle_resume_command ─────────────────────────────────────────────────────


async def test_handle_resume_command_deletes_redis_key(
    mock_redis, test_config, mock_bot_app
):
    """Resume must delete RedisKeys.system_paused() from Redis."""
    await mock_redis.set(RedisKeys.system_paused(), "1")

    await bot_module.handle_resume_command(mock_redis, test_config)

    value = await mock_redis.get(RedisKeys.system_paused())
    assert value is None


async def test_handle_resume_command_unauthorized(
    mock_redis, test_config, mock_bot_app
):
    """User not in authorized_ids must NOT delete the pause flag."""
    await mock_redis.set(RedisKeys.system_paused(), "1")
    bot_module._authorized_ids = {99999}
    try:
        await bot_module.handle_resume_command(mock_redis, test_config, user_id=12345)
    finally:
        bot_module._authorized_ids = set()

    value = await mock_redis.get(RedisKeys.system_paused())
    assert value == "1"


# ── send_alert ────────────────────────────────────────────────────────────────


async def test_send_alert_delegates_to_bot(test_config, mock_bot_app):
    """send_alert must call bot.send_message with the correct chat_id and text."""
    await bot_module.send_alert("test alert message", test_config)

    mock_bot_app.bot.send_message.assert_called_once()
    call_kwargs = mock_bot_app.bot.send_message.call_args.kwargs
    assert call_kwargs["chat_id"] == "test_chat_id"
    assert call_kwargs["text"] == "test alert message"


async def test_send_alert_before_start_does_not_crash(test_config):
    """send_alert called before start() must log a warning and not raise."""
    original_app = bot_module._app
    original_chat_id = bot_module._chat_id
    bot_module._app = None
    bot_module._chat_id = None
    try:
        await bot_module.send_alert("early alert", test_config)  # must not raise
    finally:
        bot_module._app = original_app
        bot_module._chat_id = original_chat_id


# ── _subscriber_loop ──────────────────────────────────────────────────────────


async def test_subscriber_loop_skips_invalid_json(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Invalid JSON in pub/sub message: log + skip, loop continues, no crash."""
    send_mock = AsyncMock()
    mocker.patch.object(bot_module, "send_approval_request", send_mock)

    call_count = 0

    async def mock_subscribe(redis, channel):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            yield "not-valid-json"
        else:
            raise asyncio.CancelledError()

    mocker.patch.object(bot_module, "_redis_client", MagicMock(subscribe=mock_subscribe))

    with pytest.raises(asyncio.CancelledError):
        await bot_module._subscriber_loop(mock_redis, test_config)

    send_mock.assert_not_called()


async def test_subscriber_loop_reconnects_on_connection_error(
    mock_redis, test_config, mock_bot_app, mocker
):
    """ConnectionError in subscribe: sleep with backoff, reconnect, continue."""
    proposal = make_proposal()
    send_mock = AsyncMock()
    mocker.patch.object(bot_module, "send_approval_request", send_mock)

    sleep_mock = AsyncMock()
    mocker.patch("meg.telegram.bot.asyncio.sleep", sleep_mock)

    call_count = 0

    async def mock_subscribe(redis, channel):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RedisConnectionError("test disconnect")
        yield proposal.model_dump_json()
        raise asyncio.CancelledError()

    mocker.patch.object(bot_module, "_redis_client", MagicMock(subscribe=mock_subscribe))

    with pytest.raises(asyncio.CancelledError):
        await bot_module._subscriber_loop(mock_redis, test_config)

    # Backoff sleep was called after the first ConnectionError
    sleep_mock.assert_called_once_with(1)  # 2**0 = 1, attempt=0
    # After reconnect, proposal was forwarded
    send_mock.assert_called_once()
    forwarded_proposal = send_mock.call_args.args[0]
    assert forwarded_proposal.proposal_id == proposal.proposal_id
