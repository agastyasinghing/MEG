"""
Tests for meg/signal_engine/consensus_filter.py

⚠️  OPUS SPEC — module stubs raise NotImplementedError.
Implement consensus_filter.score() and get_recent_whale_trades() with Opus + ultrathink.

Key implementation constraints:
  - score() returns a float in [0.0, 1.0]
  - Data source: Redis consensus_window sorted set (RedisKeys.consensus_window(market_id, outcome))
  - Sorted set: score=timestamp_ms, member=wallet_address
  - score() ADDS current trade's wallet to the sorted set first (including self)
  - Window is config.signal.consensus_window_hours (default 4h = 14400 seconds)
  - Stale entries (outside window) are trimmed via ZREMRANGEBYSCORE before counting
  - Count distinct wallets in window (excluding current wallet = consensus from OTHERS)
  - Consensus score uses sigmoid: score = sigmoid(n_agreeing_whales * consensus_sensitivity)
    where consensus_sensitivity = config.signal.consensus_sensitivity (default 1.5)
  - 0 agreeing whales → score near 0.0 (single whale, no consensus)
  - config.signal.min_whales_for_consensus or more → score approaches 1.0
  - YES and NO directions are tracked independently (different Redis keys)

Redis key: RedisKeys.consensus_window(market_id, outcome)
  e.g. "market:abc123:consensus:YES"

PRD reference: §9.3.4 Consensus Filter
"""
from __future__ import annotations

import pytest

from meg.core.config_loader import MegConfig
from meg.core.events import RedisKeys
from meg.signal_engine.consensus_filter import score
from tests.signal_engine.conftest import make_qualified_trade

pytestmark = pytest.mark.xfail(
    reason="OPUS SPEC: consensus_filter.score() stub raises NotImplementedError",
    strict=False,
)


# ── Single whale: no consensus ────────────────────────────────────────────────


async def test_single_whale_no_prior_agreement(mock_redis, test_config: MegConfig) -> None:
    """
    First whale on a market with no prior consensus → score near 0.0.
    No other wallets in the YES consensus window.
    """
    trade = make_qualified_trade(wallet_address="0xWHALE001", outcome="YES")
    result = await score(trade, mock_redis, test_config)
    assert result < 0.3  # single whale — low consensus score


# ── Multi-whale consensus ──────────────────────────────────────────────────────


async def test_two_whales_produces_higher_score(mock_redis, test_config: MegConfig) -> None:
    """
    One prior whale already in the YES window → current whale sees 1 agreeing whale.
    Score should be higher than the single-whale case.
    """
    import time

    # Pre-populate: one whale already traded YES on this market
    consensus_key = RedisKeys.consensus_window("market_001", "YES")
    now_ms = int(time.time() * 1000)
    await mock_redis.zadd(consensus_key, {"0xWHALE002": now_ms})

    trade = make_qualified_trade(wallet_address="0xWHALE001", outcome="YES")
    result = await score(trade, mock_redis, test_config)

    # Two whales (0xWHALE001 + 0xWHALE002) = above the zero-whale baseline
    assert result > 0.3


async def test_min_whales_for_consensus_produces_high_score(
    mock_redis, test_config: MegConfig
) -> None:
    """
    min_whales_for_consensus (default 2) other whales in agreement → score near 1.0.
    """
    import time

    consensus_key = RedisKeys.consensus_window("market_001", "YES")
    now_ms = int(time.time() * 1000)

    # Pre-populate with 2 whales (= min_whales_for_consensus)
    await mock_redis.zadd(consensus_key, {
        "0xWHALE002": now_ms,
        "0xWHALE003": now_ms - 1000,
    })

    trade = make_qualified_trade(wallet_address="0xWHALE001", outcome="YES")
    result = await score(trade, mock_redis, test_config)

    assert result > 0.7  # consensus threshold reached


# ── Direction independence ─────────────────────────────────────────────────────


async def test_yes_consensus_does_not_affect_no_score(mock_redis, test_config: MegConfig) -> None:
    """
    Whales in the YES consensus window must not affect the NO direction score.
    YES and NO are tracked independently.
    """
    import time

    # Put 3 whales in the YES window
    yes_key = RedisKeys.consensus_window("market_001", "YES")
    now_ms = int(time.time() * 1000)
    await mock_redis.zadd(yes_key, {
        "0xA": now_ms,
        "0xB": now_ms - 1000,
        "0xC": now_ms - 2000,
    })

    # Score a NO trade — should not see any consensus
    trade = make_qualified_trade(wallet_address="0xWHALE001", outcome="NO")
    result = await score(trade, mock_redis, test_config)

    assert result < 0.3  # YES window doesn't bleed into NO


# ── Stale entry pruning ────────────────────────────────────────────────────────


async def test_stale_entries_outside_window_are_excluded(
    mock_redis, test_config: MegConfig
) -> None:
    """
    A whale trade from 8 hours ago (outside 4-hour window) must not count.
    Only entries within consensus_window_hours contribute to the score.
    """
    import time

    consensus_key = RedisKeys.consensus_window("market_001", "YES")
    eight_hours_ago_ms = int(time.time() * 1000) - (8 * 3600 * 1000)

    await mock_redis.zadd(consensus_key, {"0xSTALE": eight_hours_ago_ms})

    trade = make_qualified_trade(wallet_address="0xWHALE001", outcome="YES")
    result = await score(trade, mock_redis, test_config)

    assert result < 0.3  # stale entry should not produce consensus


# ── State written to Redis ─────────────────────────────────────────────────────


async def test_score_writes_current_wallet_to_consensus_window(
    mock_redis, test_config: MegConfig
) -> None:
    """
    After score() runs, the current trade's wallet should be in the consensus window
    so future calls from other whales on the same market see this one.
    """
    trade = make_qualified_trade(wallet_address="0xWHALE001", outcome="YES")
    await score(trade, mock_redis, test_config)

    consensus_key = RedisKeys.consensus_window("market_001", "YES")
    members = await mock_redis.zrange(consensus_key, 0, -1)

    assert "0xWHALE001" in members


# ── Return bounds ─────────────────────────────────────────────────────────────


async def test_score_always_in_unit_interval(mock_redis, test_config: MegConfig) -> None:
    """Consensus score must always be in [0.0, 1.0]."""
    trade = make_qualified_trade()
    result = await score(trade, mock_redis, test_config)
    assert 0.0 <= result <= 1.0
