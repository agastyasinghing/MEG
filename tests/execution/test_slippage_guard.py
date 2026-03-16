"""
Tests for meg/execution/slippage_guard.py

Covered:
  estimate_slippage():
    - normal: returns min(size / liquidity, 1.0)
    - size > liquidity: capped at 1.0
    - liquidity = 0: returns 1.0 (fail closed)
    - key absent: returns 1.0 (fail closed)

  check() — returns (bool, str, float):
    - bid/ask absent     → (False, "no_market_data",       slippage)
    - spread too wide    → (False, "spread_too_wide:...",  slippage)
                            drift gate NOT evaluated after spread failure
    - drift exceeded     → (False, "price_drift_exceeded:...", slippage)
    - both gates pass    → (True,  "",                     slippage)
    - signal_price = 0   → drift gate skipped; only spread gate runs
    - slippage always returned regardless of gate outcome

All checks use max_spread_pct=0.04, max_price_drift_since_signal=0.08
(Phase 7 defaults).
"""
from __future__ import annotations

import pytest
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.execution import slippage_guard
from tests.execution.conftest import make_proposal, set_market_redis_data


class TestEstimateSlippage:
    async def test_normal_returns_size_over_liquidity(self, mock_redis: Redis) -> None:
        await mock_redis.set("market:market_001:liquidity", "10000.0")
        result = await slippage_guard.estimate_slippage(
            "market_001", 100.0, mock_redis
        )
        assert result == pytest.approx(0.01)  # 100 / 10_000 = 0.01

    async def test_size_greater_than_liquidity_capped_at_one(
        self, mock_redis: Redis
    ) -> None:
        await mock_redis.set("market:market_001:liquidity", "50.0")
        result = await slippage_guard.estimate_slippage(
            "market_001", 200.0, mock_redis
        )
        assert result == pytest.approx(1.0)  # 200/50 = 4.0 → capped

    async def test_zero_liquidity_returns_one(self, mock_redis: Redis) -> None:
        await mock_redis.set("market:market_001:liquidity", "0.0")
        result = await slippage_guard.estimate_slippage(
            "market_001", 100.0, mock_redis
        )
        assert result == pytest.approx(1.0)

    async def test_key_absent_returns_one(self, mock_redis: Redis) -> None:
        # No liquidity key set — unknown market depth
        result = await slippage_guard.estimate_slippage(
            "market_001", 100.0, mock_redis
        )
        assert result == pytest.approx(1.0)


class TestCheck:
    async def test_no_market_data_returns_failure(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # No Redis keys set at all
        proposal = make_proposal()
        passed, reason, slippage = await slippage_guard.check(
            proposal, mock_redis, test_config
        )
        assert passed is False
        assert "no_market_data" in reason

    async def test_spread_too_wide_returns_failure(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # spread = (0.60 - 0.40) / 0.50 = 0.40  >> max_spread_pct=0.04
        proposal = make_proposal(market_price_at_signal=0.42)
        await set_market_redis_data(
            mock_redis, mid_price=0.50, bid=0.40, ask=0.60, spread=0.20
        )
        passed, reason, slippage = await slippage_guard.check(
            proposal, mock_redis, test_config
        )
        assert passed is False
        assert "spread_too_wide" in reason

    async def test_spread_fails_drift_gate_not_evaluated(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # Spread=0.40 fails (> 0.04). signal_price=0.42, mid=0.50 →
        # drift=0.19 would also fail if evaluated. Verify only spread reason returned.
        proposal = make_proposal(market_price_at_signal=0.42)
        await set_market_redis_data(
            mock_redis, mid_price=0.50, bid=0.40, ask=0.60, spread=0.20
        )
        passed, reason, _ = await slippage_guard.check(
            proposal, mock_redis, test_config
        )
        assert passed is False
        assert "spread_too_wide" in reason
        assert "drift" not in reason  # drift gate was never reached

    async def test_price_drift_exceeded_returns_failure(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # spread = (0.465 - 0.459) / 0.462 = 0.013 < 0.04  → passes
        # drift  = |0.462 - 0.42| / 0.42  = 0.10 > 0.08     → fails
        proposal = make_proposal(market_price_at_signal=0.42)
        await set_market_redis_data(
            mock_redis,
            mid_price=0.462,
            bid=0.459,
            ask=0.465,
            spread=0.006,
            liquidity=10_000.0,
        )
        passed, reason, slippage = await slippage_guard.check(
            proposal, mock_redis, test_config
        )
        assert passed is False
        assert "price_drift_exceeded" in reason

    async def test_both_gates_pass(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # spread = (0.445 - 0.435) / 0.44 = 0.023 < 0.04   → passes
        # drift  = |0.44 - 0.42| / 0.42  = 0.048 < 0.08    → passes
        proposal = make_proposal(market_price_at_signal=0.42)
        await set_market_redis_data(
            mock_redis,
            mid_price=0.44,
            bid=0.435,
            ask=0.445,
            spread=0.01,
            liquidity=10_000.0,
        )
        passed, reason, slippage = await slippage_guard.check(
            proposal, mock_redis, test_config
        )
        assert passed is True
        assert reason == ""
        assert 0.0 <= slippage <= 1.0

    async def test_signal_price_zero_skips_drift_gate(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # market_price_at_signal=0.0 (default unset) → drift gate skipped.
        # Spread is narrow → passes. Large mid movement does not block.
        proposal = make_proposal(market_price_at_signal=0.0)
        await set_market_redis_data(
            mock_redis,
            mid_price=0.90,
            bid=0.895,
            ask=0.905,
            spread=0.01,
            liquidity=10_000.0,
        )
        passed, reason, _ = await slippage_guard.check(
            proposal, mock_redis, test_config
        )
        assert passed is True

    async def test_slippage_always_returned_on_gate_failure(
        self, mock_redis: Redis, test_config: MegConfig
    ) -> None:
        # Spread fails but slippage should still be computed from liquidity key.
        proposal = make_proposal(size_usdc=100.0)
        await set_market_redis_data(
            mock_redis,
            mid_price=0.50,
            bid=0.40,
            ask=0.60,
            spread=0.20,
            liquidity=10_000.0,
        )
        _, _, slippage = await slippage_guard.check(proposal, mock_redis, test_config)
        assert slippage == pytest.approx(0.01)  # 100 / 10_000 = 0.01
