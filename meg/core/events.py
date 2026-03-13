"""
Core event schemas and Redis key constants for MEG.

All inter-layer communication uses these Pydantic models serialized as JSON
over Redis pub/sub channels. No layer may define its own event schema — all
schemas live here to keep the inter-layer contract in one place.

Event flow:
  data_layer    →  RawWhaleTrade         → CHANNEL_RAW_WHALE_TRADES
  pre_filter    →  QualifiedWhaleTrade   → CHANNEL_QUALIFIED_WHALE_TRADES
  signal_engine →  SignalEvent           → CHANNEL_SIGNAL_EVENTS
  agent_core    →  TradeProposal         → CHANNEL_TRADE_PROPOSALS

Dependency rule: meg.core imports nothing from meg. It is the base of the
dependency tree. All other layers import from meg.core; none import each other.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


# ── Event schemas ─────────────────────────────────────────────────────────────


class RawWhaleTrade(BaseModel):
    """
    Emitted by data_layer when a whale wallet executes a trade on Polymarket.
    Published to: RedisKeys.CHANNEL_RAW_WHALE_TRADES
    """

    event_type: Literal["raw_whale_trade"] = "raw_whale_trade"
    wallet_address: str
    market_id: str
    outcome: Literal["YES", "NO"]
    size_usdc: float
    timestamp_ms: int
    tx_hash: str
    block_number: int
    market_price_at_trade: float


class QualifiedWhaleTrade(BaseModel):
    """
    Emitted by pre_filter after a RawWhaleTrade passes all three gates:
      Gate 1: market quality check
      Gate 2: arbitrage whale exclusion
      Gate 3: intent classification (must be SIGNAL)
    Published to: RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES
    """

    event_type: Literal["qualified_whale_trade"] = "qualified_whale_trade"
    wallet_address: str
    market_id: str
    outcome: Literal["YES", "NO"]
    size_usdc: float
    timestamp_ms: int
    tx_hash: str
    block_number: int
    market_price_at_trade: float
    whale_score: float
    archetype: Literal["INFORMATION", "MOMENTUM", "ARBITRAGE", "MANIPULATOR"]
    intent: Literal["SIGNAL", "HEDGE", "REBALANCE"]


class SignalEvent(BaseModel):
    """
    Emitted by signal_engine after composite scoring.
    Only events with composite_score >= config.signal.composite_score_threshold
    are published. Sub-threshold events are still logged to signal_outcomes with
    status=FILTERED — they are the training data moat.
    Published to: RedisKeys.CHANNEL_SIGNAL_EVENTS
    """

    event_type: Literal["signal"] = "signal"
    signal_id: str
    market_id: str
    outcome: Literal["YES", "NO"]
    composite_score: float
    recommended_size_usdc: float
    ttl_expires_at_ms: int
    status: Literal["PENDING", "FILTERED", "EXECUTED", "EXPIRED"]
    source_wallet_addresses: list[str] = Field(default_factory=list)


class TradeProposal(BaseModel):
    """
    Emitted by agent_core after a SignalEvent passes all risk gates.
    In v1, all proposals require human approval via Telegram before execution.
    Published to: RedisKeys.CHANNEL_TRADE_PROPOSALS
    """

    event_type: Literal["trade_proposal"] = "trade_proposal"
    proposal_id: str
    signal_id: str
    market_id: str
    outcome: Literal["YES", "NO"]
    size_usdc: float
    limit_price: float
    status: Literal["PENDING_APPROVAL", "APPROVED", "REJECTED", "EXECUTED", "CANCELLED"]
    created_at_ms: int


# ── Redis key patterns ────────────────────────────────────────────────────────


class RedisKeys:
    """
    Centralised Redis key and channel constants. Always use these — never
    hardcode key strings in application code. Changing a key pattern here
    changes it everywhere.

    Key pattern convention: <entity>:<id>:<field>

    Examples:
      RedisKeys.market_mid_price("0xabc") → "market:0xabc:mid_price"
      RedisKeys.wallet_score("0x123")     → "wallet:0x123:score"
      RedisKeys.signal_state("sig_42")    → "signal:sig_42:state"
    """

    # ── Pub/sub channels ──────────────────────────────────────────────────────
    CHANNEL_RAW_WHALE_TRADES: str = "raw_whale_trades"
    CHANNEL_QUALIFIED_WHALE_TRADES: str = "qualified_whale_trades"
    CHANNEL_SIGNAL_EVENTS: str = "signal_events"
    CHANNEL_TRADE_PROPOSALS: str = "trade_proposals"

    # ── Key builders ──────────────────────────────────────────────────────────
    @staticmethod
    def market_mid_price(market_id: str) -> str:
        return f"market:{market_id}:mid_price"

    @staticmethod
    def market_liquidity(market_id: str) -> str:
        return f"market:{market_id}:liquidity"

    @staticmethod
    def market_spread(market_id: str) -> str:
        return f"market:{market_id}:spread"

    @staticmethod
    def wallet_score(address: str) -> str:
        return f"wallet:{address}:score"

    @staticmethod
    def wallet_archetype(address: str) -> str:
        return f"wallet:{address}:archetype"

    @staticmethod
    def signal_state(signal_id: str) -> str:
        return f"signal:{signal_id}:state"

    @staticmethod
    def signal_ttl(signal_id: str) -> str:
        return f"signal:{signal_id}:ttl"
