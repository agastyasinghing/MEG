"""
Decision agent.

Gates a signal through all agent_core risk checks before creating a
TradeProposal. In v1, all proposals require human approval via Telegram.

Decision flow:
  SignalEvent
    ↓
  risk_controller.check()        → REJECT if any risk gate fails
    ↓
  trap_detector.check()          → REJECT if whale trap detected
    ↓
  saturation_monitor.check()     → REJECT if market is saturated
    ↓
  crowding_detector.check()      → REJECT if copy followers have closed the window
    ↓
  TradeProposal (PENDING_APPROVAL) → published to CHANNEL_TRADE_PROPOSALS
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import SignalEvent, TradeProposal


async def evaluate(
    signal: SignalEvent,
    redis: Redis,
    config: MegConfig,
) -> TradeProposal | None:
    """
    Run all risk gates against the signal. Return a TradeProposal if all
    gates pass, or None if any gate rejects (logs the rejection reason).
    """
    raise NotImplementedError("decision_agent.evaluate")


async def _build_proposal(
    signal: SignalEvent,
    config: MegConfig,
) -> TradeProposal:
    """Construct a TradeProposal from an approved SignalEvent."""
    raise NotImplementedError("decision_agent._build_proposal")
