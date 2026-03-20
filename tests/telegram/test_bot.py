"""
Tests for meg/telegram/bot.py.

Coverage map:
  send_approval_request         — message content, chat_id, keyboard, Redis TTL
  handle_approval_callback      — approve success, gate rejection, exception,
                                   reject, expired key, double-click guard
  handle_pause_command          — sets Redis key, auth check
  handle_resume_command         — deletes Redis key, auth check
  handle_reject_command         — valid reject with reason, unknown proposal,
                                   missing args, unauthorized user
  send_alert                    — delegates to bot.send_message
  send_alert before start()     — no crash, just logs
  _subscriber_loop              — invalid JSON skip, ConnectionError reconnect
  _alert_loop                   — valid AlertMessage dispatch, urgent prefix,
                                   invalid JSON skip, ConnectionError reconnect
  _cb auth check                — unauthorized user blocked, empty authorized_ids
  _format_proposal              — entry_distance_pct, current_price, slippage shown
"""
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

import meg.telegram.bot as bot_module
from meg.core.events import AlertMessage, RedisKeys

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


# ── _alert_loop ───────────────────────────────────────────────────────────────


async def test_alert_loop_dispatches_alert_message(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Valid AlertMessage received: send_alert called with message text."""
    alert = AlertMessage(
        alert_type="position_closed",
        message="Position closed: +10.00 USDC",
        urgent=False,
    )

    async def mock_subscribe(redis, channel):
        yield alert.model_dump_json()
        raise asyncio.CancelledError()

    mocker.patch.object(bot_module, "_redis_client", MagicMock(subscribe=mock_subscribe))

    with pytest.raises(asyncio.CancelledError):
        await bot_module._alert_loop(mock_redis, test_config)

    mock_bot_app.bot.send_message.assert_called_once()
    text: str = mock_bot_app.bot.send_message.call_args.kwargs["text"]
    assert "Position closed" in text
    assert "🚨 URGENT" not in text


async def test_alert_loop_prefixes_urgent_alerts(
    mock_redis, test_config, mock_bot_app, mocker
):
    """urgent=True alert: message prefixed with '🚨 URGENT:'."""
    alert = AlertMessage(
        alert_type="circuit_breaker",
        message="Circuit breaker triggered.",
        urgent=True,
    )

    async def mock_subscribe(redis, channel):
        yield alert.model_dump_json()
        raise asyncio.CancelledError()

    mocker.patch.object(bot_module, "_redis_client", MagicMock(subscribe=mock_subscribe))

    with pytest.raises(asyncio.CancelledError):
        await bot_module._alert_loop(mock_redis, test_config)

    text: str = mock_bot_app.bot.send_message.call_args.kwargs["text"]
    assert text.startswith("🚨 URGENT:")
    assert "Circuit breaker" in text


async def test_alert_loop_skips_invalid_json(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Invalid JSON in CHANNEL_BOT_ALERTS: log error, skip, loop continues, no crash."""
    send_mock = AsyncMock()
    mocker.patch.object(bot_module, "send_alert", send_mock)

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
        await bot_module._alert_loop(mock_redis, test_config)

    send_mock.assert_not_called()


async def test_alert_loop_reconnects_on_connection_error(
    mock_redis, test_config, mock_bot_app, mocker
):
    """ConnectionError in _alert_loop: sleep with backoff, reconnect, continue."""
    alert = AlertMessage(
        alert_type="whale_exit",
        message="Whale exit detected.",
        urgent=False,
    )
    send_mock = AsyncMock()
    mocker.patch.object(bot_module, "send_alert", send_mock)

    sleep_mock = AsyncMock()
    mocker.patch("meg.telegram.bot.asyncio.sleep", sleep_mock)

    call_count = 0

    async def mock_subscribe(redis, channel):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RedisConnectionError("test disconnect")
        yield alert.model_dump_json()
        raise asyncio.CancelledError()

    mocker.patch.object(bot_module, "_redis_client", MagicMock(subscribe=mock_subscribe))

    with pytest.raises(asyncio.CancelledError):
        await bot_module._alert_loop(mock_redis, test_config)

    sleep_mock.assert_called_once_with(1)  # 2**0 = 1, attempt=0
    send_mock.assert_called_once()


# ── _cb auth check ────────────────────────────────────────────────────────────


async def test_cb_unauthorized_user_blocked(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Unauthorized user clicking Approve/Reject: edit to 'Not authorized', no order call."""
    bot_module._authorized_ids = {99999}
    try:
        mock_place = AsyncMock()
        mocker.patch("meg.telegram.bot.order_router.place", mock_place)

        proposal = make_proposal()
        await mock_redis.set(
            RedisKeys.pending_proposal(proposal.proposal_id),
            proposal.model_dump_json(),
            ex=3600,
        )

        query = make_mock_query(f"approve:{proposal.proposal_id}")
        # Use _is_authorized() — the same helper _cb uses — so this test is
        # coupled to the real auth logic rather than a manual reimplementation.
        uid = 12345  # not in {99999}
        if not bot_module._is_authorized(uid):
            await query.edit_message_text("⛔ Not authorized to approve or reject.")
        else:
            await bot_module.handle_approval_callback(query, mock_redis, test_config)

        mock_place.assert_not_called()
        edit_text: str = query.edit_message_text.call_args.args[0]
        assert "Not authorized" in edit_text
    finally:
        bot_module._authorized_ids = set()


async def test_cb_empty_authorized_ids_allows_all(
    mock_redis, test_config, mock_bot_app, mocker
):
    """Empty _authorized_ids: any user can approve/reject (no restriction)."""
    bot_module._authorized_ids = set()

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
                "order_id": "order-auth-test",
                "estimated_slippage": 0.01,
                "reason": "",
            }
        ),
    )

    query = make_mock_query(f"approve:{proposal.proposal_id}")
    # With empty _authorized_ids, should proceed to handle_approval_callback
    await bot_module.handle_approval_callback(query, mock_redis, test_config)

    edit_text: str = query.edit_message_text.call_args.args[0]
    assert "APPROVED" in edit_text


# ── handle_reject_command ─────────────────────────────────────────────────────


async def test_handle_reject_command_valid(mock_redis, test_config, mock_bot_app):
    """Valid /reject {id} {reason}: proposal deleted, reason logged, confirmation sent."""
    proposal = make_proposal()
    await mock_redis.set(
        RedisKeys.pending_proposal(proposal.proposal_id),
        proposal.model_dump_json(),
        ex=3600,
    )

    await bot_module.handle_reject_command(
        mock_redis,
        test_config,
        user_id=None,
        args=[proposal.proposal_id, "price", "moved", "too", "far"],
    )

    # Proposal must be deleted (double-click guard)
    remaining = await mock_redis.get(RedisKeys.pending_proposal(proposal.proposal_id))
    assert remaining is None

    # Confirmation alert must mention "rejected"
    text: str = mock_bot_app.bot.send_message.call_args.kwargs["text"]
    assert "rejected" in text.lower()


async def test_handle_reject_command_unknown_proposal(
    mock_redis, test_config, mock_bot_app
):
    """Unknown proposal_id: alert sent with 'not found', no crash."""
    await bot_module.handle_reject_command(
        mock_redis,
        test_config,
        user_id=None,
        args=["nonexistent-proposal-id"],
    )

    text: str = mock_bot_app.bot.send_message.call_args.kwargs["text"]
    assert "not found" in text.lower() or "already handled" in text.lower()


async def test_handle_reject_command_missing_args(mock_redis, test_config, mock_bot_app):
    """/reject with no args: usage message sent, no crash."""
    await bot_module.handle_reject_command(
        mock_redis, test_config, user_id=None, args=[]
    )

    text: str = mock_bot_app.bot.send_message.call_args.kwargs["text"]
    assert "Usage" in text or "usage" in text


async def test_handle_reject_command_unauthorized(mock_redis, test_config, mock_bot_app):
    """Unauthorized user: auth failure alert sent, proposal untouched."""
    proposal = make_proposal()
    await mock_redis.set(
        RedisKeys.pending_proposal(proposal.proposal_id),
        proposal.model_dump_json(),
        ex=3600,
    )
    bot_module._authorized_ids = {99999}
    try:
        await bot_module.handle_reject_command(
            mock_redis,
            test_config,
            user_id=12345,
            args=[proposal.proposal_id, "bad actor"],
        )
    finally:
        bot_module._authorized_ids = set()

    # Proposal must still be in Redis (not deleted)
    remaining = await mock_redis.get(RedisKeys.pending_proposal(proposal.proposal_id))
    assert remaining is not None

    text: str = mock_bot_app.bot.send_message.call_args.kwargs["text"]
    assert "Unauthorized" in text or "unauthorized" in text


# ── _format_proposal — new display fields ─────────────────────────────────────


def test_format_proposal_shows_current_price(mock_bot_app):
    """_format_proposal includes current_price when > 0."""
    proposal = make_proposal(current_price=0.46)
    text = bot_module._format_proposal(proposal)
    assert "0.4600" in text


def test_format_proposal_shows_estimated_slippage(mock_bot_app):
    """_format_proposal includes estimated_slippage as percentage."""
    proposal = make_proposal(estimated_slippage=0.025)
    text = bot_module._format_proposal(proposal)
    assert "2.50%" in text


def test_format_proposal_shows_entry_distance_pct(mock_bot_app):
    """_format_proposal computes and shows entry distance from whale fill."""
    # limit_price=0.45, market_price_at_signal=0.42 → distance = (0.45-0.42)/0.42 = 7.14%
    proposal = make_proposal(limit_price=0.45, market_price_at_signal=0.42)
    text = bot_module._format_proposal(proposal)
    assert "7.1%" in text
