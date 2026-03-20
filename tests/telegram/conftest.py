"""
Telegram bot test fixtures.

Mocking strategy:
  bot._app is set to a MagicMock with AsyncMock for bot.send_message.
  This avoids any real Telegram API calls while exercising all business logic.

  PTB types (CallbackQuery) are mocked with MagicMock; async methods
  (answer, edit_message_text) are AsyncMock.

  Redis: fakeredis with decode_responses=True to match production client behaviour.
  order_router.place: patched per-test via mocker.patch.
"""
from __future__ import annotations

import time
import uuid
from unittest.mock import AsyncMock, MagicMock

import fakeredis.aioredis
import pytest
import pytest_asyncio
from redis.asyncio import Redis

import meg.telegram.bot as bot_module
from meg.core.config_loader import MegConfig
from meg.core.events import TradeProposal


# ── Redis fixture ──────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def mock_redis() -> Redis:
    """Fakeredis with decode_responses=True — matches production redis_client.py."""
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    yield client
    await client.aclose()


# ── Config fixture ─────────────────────────────────────────────────────────────


@pytest.fixture
def test_config() -> MegConfig:
    return MegConfig()


# ── Bot app mock fixture ───────────────────────────────────────────────────────


@pytest.fixture
def mock_bot_app():
    """
    Inject a mock PTB Application into bot._app and a test chat_id into bot._chat_id.
    Restores originals after the test.

    Usage:
        def test_something(mock_bot_app):
            # bot._app and bot._chat_id are set; use mock_bot_app.bot.send_message
            assert mock_bot_app.bot.send_message.called
    """
    mock_app = MagicMock()
    mock_app.bot = MagicMock()
    mock_app.bot.send_message = AsyncMock()

    original_app = bot_module._app
    original_chat_id = bot_module._chat_id
    original_authorized = bot_module._authorized_ids

    bot_module._app = mock_app
    bot_module._chat_id = "test_chat_id"
    bot_module._authorized_ids = set()

    yield mock_app

    bot_module._app = original_app
    bot_module._chat_id = original_chat_id
    bot_module._authorized_ids = original_authorized


# ── Factory helpers ────────────────────────────────────────────────────────────


def make_proposal(
    *,
    proposal_id: str | None = None,
    market_id: str = "market_001",
    outcome: str = "YES",
    size_usdc: float = 100.0,
    limit_price: float = 0.45,
    composite_score: float = 0.72,
    market_price_at_signal: float = 0.42,
    saturation_score: float = 0.10,
    trap_warning: bool = False,
    contributing_wallets: list[str] | None = None,
    estimated_half_life_minutes: float = 30.0,
) -> TradeProposal:
    return TradeProposal(
        proposal_id=proposal_id or f"prop_{uuid.uuid4().hex[:8]}",
        signal_id=f"sig_{uuid.uuid4().hex[:8]}",
        market_id=market_id,
        outcome=outcome,
        size_usdc=size_usdc,
        limit_price=limit_price,
        status="PENDING_APPROVAL",
        created_at_ms=int(time.time() * 1000),
        composite_score=composite_score,
        market_price_at_signal=market_price_at_signal,
        saturation_score=saturation_score,
        trap_warning=trap_warning,
        contributing_wallets=contributing_wallets or ["0xWHALE001", "0xWHALE002"],
        estimated_half_life_minutes=estimated_half_life_minutes,
    )


def make_mock_query(callback_data: str) -> MagicMock:
    """Return a mock CallbackQuery with async answer + edit_message_text."""
    q = MagicMock()
    q.data = callback_data
    q.answer = AsyncMock()
    q.edit_message_text = AsyncMock()
    return q
