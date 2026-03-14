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

Schema authority: PRD §12 is the source of truth for all field names and types.
This file must stay in sync with meg/db/models.py — any field added here
must have a corresponding column in the ORM model (or be intentionally excluded
with a comment explaining why).
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# ── Shared type aliases ────────────────────────────────────────────────────────

Outcome = Literal["YES", "NO"]
Archetype = Literal["INFORMATION", "MOMENTUM", "ARBITRAGE", "MANIPULATOR"]
# SIGNAL_LADDER: whale is building a position across multiple trades (escalating conviction)
Intent = Literal["SIGNAL", "SIGNAL_LADDER", "HEDGE", "REBALANCE"]
SignalStatus = Literal[
    "PENDING",
    "APPROVED",
    "REJECTED",
    "FILTERED",
    "BLOCKED",
    "EXECUTED",
    "EXPIRED",
    "TRAP_DETECTED",
]


# ── Event schemas ─────────────────────────────────────────────────────────────


class RawWhaleTrade(BaseModel):
    """
    Emitted by data_layer when a whale wallet executes a trade on Polymarket.
    Published to: RedisKeys.CHANNEL_RAW_WHALE_TRADES
    """

    event_type: Literal["raw_whale_trade"] = "raw_whale_trade"
    wallet_address: str
    market_id: str
    outcome: Outcome
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
      Gate 3: intent classification (must be SIGNAL or SIGNAL_LADDER)
    Published to: RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES
    """

    event_type: Literal["qualified_whale_trade"] = "qualified_whale_trade"
    wallet_address: str
    market_id: str
    outcome: Outcome
    size_usdc: float
    timestamp_ms: int
    tx_hash: str
    block_number: int
    market_price_at_trade: float
    whale_score: float
    archetype: Archetype
    intent: Intent


class SignalScores(BaseModel):
    """
    Per-module sub-scores that compose into the final composite_score.
    Stored as JSONB in signal_outcomes.scores_json — adding a new module
    field here requires no DB migration, only a new signal_engine module.

    All scores are in [0, 1] except multipliers which can exceed 1.
    """

    lead_lag: float = Field(ge=0, le=1)
    consensus: float = Field(ge=0, le=1)
    kelly_confidence: float = Field(ge=0, le=1)
    divergence: float = Field(ge=0, le=1)
    conviction_ratio: float = Field(ge=0, le=1)
    archetype_multiplier: float = Field(ge=0, le=2)
    ladder_multiplier: float = Field(ge=1, le=2)


class SignalEvent(BaseModel):
    """
    Emitted by signal_engine after composite scoring.
    Only events with composite_score >= config.signal.composite_score_threshold
    are published. Sub-threshold events are still logged to signal_outcomes with
    status=FILTERED — they are the training data moat.
    Published to: RedisKeys.CHANNEL_SIGNAL_EVENTS

    Field authority: PRD §12 SignalEvent. Mirrors signal_outcomes ORM columns.
    """

    event_type: Literal["signal"] = "signal"
    signal_id: str
    market_id: str
    outcome: Outcome
    composite_score: float
    scores: SignalScores
    recommended_size_usdc: float
    kelly_fraction: float
    ttl_expires_at_ms: int
    status: SignalStatus = "PENDING"
    triggering_wallet: str
    # All wallets whose trades contributed to this signal (includes triggering_wallet)
    contributing_wallets: list[str] = Field(default_factory=list)
    whale_count: int = 0
    is_contrarian: bool = False
    is_ladder: bool = False
    ladder_trade_count: int = 0
    market_price_at_signal: float = 0.0
    intent: Intent = "SIGNAL"
    saturation_score: float = 0.0
    saturation_size_multiplier: float = 1.0
    trap_warning: bool = False


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
    outcome: Outcome
    size_usdc: float
    limit_price: float
    status: Literal["PENDING_APPROVAL", "APPROVED", "REJECTED", "EXECUTED", "CANCELLED"]
    created_at_ms: int


# ── Market state model ────────────────────────────────────────────────────────


class MarketState(BaseModel):
    """
    Current market state as cached by CLOBMarketFeed in Redis.

    Serialized as JSON and stored per-market key. Consumed by:
      - pre_filter.market_quality (liquidity, spread, participants)
      - signal_engine.contrarian_detector (bid/ask, volume)
      - signal_engine.saturation_monitor (volume, participants)
      - execution.slippage_guard (bid, ask, spread)

    price_history is NOT in this model — it lives in a separate Redis sorted
    set (key: RedisKeys.market_price_history) scored by timestamp_ms.
    """

    market_id: str
    bid: float  # best bid price (0.0–1.0)
    ask: float  # best ask price (0.0–1.0)
    mid_price: float  # (bid + ask) / 2
    spread: float  # ask - bid
    liquidity_usdc: float  # total USDC depth within 5 ticks
    volume_24h_usdc: float  # 24-hour trading volume in USDC
    participants: int  # unique traders in this market
    last_updated_at: datetime


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

    # ── Market CLOB state keys (written by CLOBMarketFeed) ────────────────────
    @staticmethod
    def market_bid(market_id: str) -> str:
        return f"market:{market_id}:bid"

    @staticmethod
    def market_ask(market_id: str) -> str:
        return f"market:{market_id}:ask"

    @staticmethod
    def market_volume_24h(market_id: str) -> str:
        return f"market:{market_id}:volume_24h"

    @staticmethod
    def market_participants(market_id: str) -> str:
        return f"market:{market_id}:participants"

    @staticmethod
    def market_last_updated_ms(market_id: str) -> str:
        return f"market:{market_id}:last_updated_ms"

    # Sorted set: member=mid_price_str, score=timestamp_ms (ZREMRANGEBYSCORE trims to 1h)
    @staticmethod
    def market_price_history(market_id: str) -> str:
        return f"market:{market_id}:price_history"

    # ── System-level keys (single instance) ───────────────────────────────────
    # Set of all market_ids currently being traded (SADD by polygon_feed)
    @staticmethod
    def active_markets() -> str:
        return "meg:active_markets"

    # Last block number successfully processed by polygon_feed
    @staticmethod
    def last_processed_block() -> str:
        return "meg:last_processed_block"

    # Sorted set window for consensus_filter: member=wallet_address, score=timestamp_ms
    @staticmethod
    def consensus_window(market_id: str) -> str:
        return f"market:{market_id}:consensus_window"

    # Serialized MegConfig JSON — set by config_loader after each hot-reload
    @staticmethod
    def meg_config() -> str:
        return "meg:config"
