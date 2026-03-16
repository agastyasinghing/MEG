"""
Tests for meg/execution/entry_filter.py

Covered:
  get_current_price():
    - key present  → returns float
    - key absent   → raises ValueError("no_price_data:...")

  check():
    - Redis miss               → (False, "no_price_data:...")
    - YES, within threshold    → (True, "")
    - YES, exceeds threshold   → (False, "entry_distance_exceeded:...")
    - YES, at exact boundary   → (True, "")  [inclusive]
    - NO,  within threshold    → (True, "")
    - NO,  below floor         → (False, "entry_distance_exceeded:...")

All checks use max_entry_distance_pct=0.06 (Phase 7 default).
"""
from __future__ import annotations

import pytest
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.execution import entry_filter
from tests.execution.conftest import make_proposal, set_market_redis_data


class TestGetCurrentPrice:
    async def test_key_present_returns_float(self, mock_redis: Redis) -> None:
        await mock_redis.set("market:market_001:mid_price", "0.44")
        price = await entry_filter.get_current_price("market_001", mock_redis)
        assert price == pytest.approx(0.44)

    async def test_key_absent_raises_value_error(self, mock_redis: Redis) -> None:
        with pytest.raises(ValueError, match="no_price_data"):
            await entry_filter.get_current_price("market_001", mock_redis)


class TestCheck:
    async def test_redis_miss_returns_failure(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # No Redis keys set — mid_price absent
        proposal = make_proposal()
        passed, reason = await entry_filter.check(proposal, mock_redis, test_config)
        assert passed is False
        assert "no_price_data" in reason

    async def test_buy_yes_within_threshold_passes(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # signal=0.42, threshold=0.06 → max current = 0.42 * 1.06 = 0.4452
        # current=0.44 < 0.4452 → passes
        proposal = make_proposal(outcome="YES", market_price_at_signal=0.42)
        await set_market_redis_data(mock_redis, mid_price=0.44)
        passed, reason = await entry_filter.check(proposal, mock_redis, test_config)
        assert passed is True
        assert reason == ""

    async def test_buy_yes_exceeds_threshold_fails(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # signal=0.42, threshold=0.06 → max current = 0.4452
        # current=0.50 > 0.4452 → price has risen too far above whale's entry
        proposal = make_proposal(outcome="YES", market_price_at_signal=0.42)
        await set_market_redis_data(mock_redis, mid_price=0.50)
        passed, reason = await entry_filter.check(proposal, mock_redis, test_config)
        assert passed is False
        assert "entry_distance_exceeded" in reason
        assert "YES" in reason

    async def test_buy_yes_at_exact_boundary_passes(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # signal=0.42, threshold=0.06 → boundary = 0.42 * 1.06 = 0.4452
        # current=0.4452 → exactly at boundary → passes (check is <=, inclusive)
        proposal = make_proposal(outcome="YES", market_price_at_signal=0.42)
        await set_market_redis_data(mock_redis, mid_price=0.4452)
        passed, reason = await entry_filter.check(proposal, mock_redis, test_config)
        assert passed is True

    async def test_buy_no_within_threshold_passes(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # NO: current_price >= signal_price * (1 - threshold)
        # signal=0.42, threshold=0.06 → floor = 0.42 * 0.94 = 0.3948
        # current=0.40 > 0.3948 → passes (YES hasn't corrected too far)
        proposal = make_proposal(outcome="NO", market_price_at_signal=0.42)
        await set_market_redis_data(mock_redis, mid_price=0.40)
        passed, reason = await entry_filter.check(proposal, mock_redis, test_config)
        assert passed is True
        assert reason == ""

    async def test_buy_no_below_floor_fails(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # signal=0.42, threshold=0.06 → floor = 0.42 * 0.94 = 0.3948
        # current=0.35 < 0.3948 → YES correction already happened; NO edge gone
        proposal = make_proposal(outcome="NO", market_price_at_signal=0.42)
        await set_market_redis_data(mock_redis, mid_price=0.35)
        passed, reason = await entry_filter.check(proposal, mock_redis, test_config)
        assert passed is False
        assert "entry_distance_exceeded" in reason
        assert "NO" in reason
