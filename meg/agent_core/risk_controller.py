"""
Risk controller — 5-gate risk framework.

All 5 gates must pass for a signal to proceed to execution. Any failure
immediately rejects the signal with a logged reason. Gates are evaluated
in order of computational cost (cheapest first).

Gate order:
  1. Paper trading mode check  — PASS in paper mode (TradeProposal still generated,
                                 Telegram approval still runs, CLOB mock handles no-op).
                                 REJECT only if live mode is misconfigured (safety backstop).
  2. Daily loss limit          — reject if daily P&L loss >= max_daily_loss_usdc
  3. Max open positions        — reject if open positions >= max_open_positions
  4. Market exposure limit     — reject if market exposure >= max_market_exposure_pct
  5. Position size limit       — reject if proposed size > max_position_pct * portfolio

NOTE: Implement with Opus + ultrathink. Risk gate bugs = real financial loss.
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import SignalEvent


async def check(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """
    Run all 5 risk gates. Return (True, "") if all pass.
    Return (False, reason) with a descriptive reason string if any gate fails.
    """
    raise NotImplementedError("risk_controller.check")


async def _check_paper_trading(config: MegConfig) -> tuple[bool, str]:
    """
    Gate 1: PASS in paper trading mode (paper_trading=True).
    TradeProposals still flow to Telegram and clob_client handles the mock.
    This gate is a safety backstop for misconfigured live mode only —
    it does NOT block the paper trading simulation pipeline.
    """
    raise NotImplementedError("risk_controller._check_paper_trading")


async def _check_daily_loss(redis: Redis, config: MegConfig) -> tuple[bool, str]:
    """Gate 2: reject if today's losses have hit the daily limit."""
    raise NotImplementedError("risk_controller._check_daily_loss")


async def _check_max_positions(redis: Redis, config: MegConfig) -> tuple[bool, str]:
    """Gate 3: reject if we're already at the max open position count."""
    raise NotImplementedError("risk_controller._check_max_positions")


async def _check_market_exposure(
    market_id: str,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """Gate 4: reject if this market already has too much exposure."""
    raise NotImplementedError("risk_controller._check_market_exposure")


async def _check_position_size(
    proposed_size_usdc: float,
    redis: Redis,
    config: MegConfig,
) -> tuple[bool, str]:
    """Gate 5: reject if the proposed size exceeds max_position_pct of portfolio."""
    raise NotImplementedError("risk_controller._check_position_size")
