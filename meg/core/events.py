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
  any_layer     →  AlertMessage          → CHANNEL_BOT_ALERTS (consumed by telegram/bot._alert_loop)

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

SignalType = Literal[
    "WHALE_REACTION",        # Direct response to a whale entry. Half-life: ~15 min.
    "EVENT_CASCADE",         # Information spreading across related markets. Half-life: ~90 min.
    "BEHAVIORAL_DRIFT",      # Sustained directional pressure from whale accumulation. Half-life: ~8 h.
    "RESOLUTION_ASYMMETRY",  # Structural edge from contract design / resolution timing. Half-life: days.
]


# ── Exceptions ────────────────────────────────────────────────────────────────


class SignalDroppedError(Exception):
    """
    Raised by composite_scorer._gather_component_scores() when a trade must be
    dropped before composite scoring is complete.

    Two trigger conditions:
      1. wallet_data unavailable in Redis (cache miss on pre-fetch)
      2. lead_lag_score < config.signal.lead_lag_min_gate after decay

    The caller (composite_scorer.score()) catches this exception, writes
    status=FILTERED to signal_outcomes, and returns without publishing.

    reason: short string describing why the signal was dropped.
    score:  the partial score at the time of drop (0.0 for data-miss cases).
    """

    def __init__(self, reason: str, score: float = 0.0) -> None:
        self.reason = reason
        self.score = score
        super().__init__(f"Signal dropped: {reason} (score={score:.3f})")


# ── Event schemas ─────────────────────────────────────────────────────────────


class RawWhaleTrade(BaseModel):
    """
    Emitted by data_layer when a whale wallet executes a trade on Polymarket.
    Published to: RedisKeys.CHANNEL_RAW_WHALE_TRADES

    market_category: populated by polygon_feed from market:{id}:category Redis key.
    Defaults to "" (empty string) when not yet available — this happens on the first
    trade in a new market before CLOBMarketFeed has polled it. Signal engine modules
    fall back to wallet.win_rate (overall) when market_category is empty.
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
    market_category: str = ""  # e.g. "politics", "crypto", "sports"; "" = unknown


class QualifiedWhaleTrade(BaseModel):
    """
    Emitted by pre_filter after a RawWhaleTrade passes all three gates:
      Gate 1: market quality check
      Gate 2: arbitrage whale exclusion
      Gate 3: intent classification (must be SIGNAL or SIGNAL_LADDER)
    Published to: RedisKeys.CHANNEL_QUALIFIED_WHALE_TRADES

    market_category: forwarded from RawWhaleTrade. Used by signal_engine for
    category-weighted lead_lag scoring and Kelly win_prob lookup. "" = unknown.
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
    market_category: str = ""  # forwarded from RawWhaleTrade; "" = unknown


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
    # Signal type — all v1 signals are WHALE_REACTION. Used by signal_decay for
    # per-type half-life baselines (v1.5). Set by composite_scorer.
    signal_type: SignalType = "WHALE_REACTION"
    # Estimated half-life in minutes. Populated by signal_decay.set_signal_ttl().
    # 0.0 = not yet computed (signal_decay has not run).
    estimated_half_life_minutes: float = 0.0
    # Archetype of the triggering whale. Forwarded from QualifiedWhaleTrade
    # for dashboard display and agent_core trap detection.
    whale_archetype: Archetype = "INFORMATION"
    # Market category at signal time. Forwarded from QualifiedWhaleTrade.
    # Used by dashboard for category-level P&L attribution.
    market_category: str = ""


class TradeProposal(BaseModel):
    """
    Emitted by agent_core after a SignalEvent passes all risk gates.
    In v1, all proposals require human approval via Telegram before execution.
    Published to: RedisKeys.CHANNEL_TRADE_PROPOSALS

    Fields are a superset of what execution layer needs plus what the dashboard
    approval queue and Telegram bot display (PRD §9.6 Trade Approval Queue):
      - composite_score + scores: full score breakdown shown at approval time
      - saturation_score: how crowded the market is right now
      - trap_warning: prominent red flag if whale trap pattern detected
      - contributing_wallets: which whales contributed (info panel)
      - market_price_at_signal: reference price for entry distance display
      - estimated_half_life_minutes: decay context for operator
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

    # ── Score context (forwarded from SignalEvent for dashboard display) ───────
    composite_score: float = 0.0
    scores: SignalScores | None = None  # full per-module breakdown
    saturation_score: float = 0.0
    trap_warning: bool = False
    contributing_wallets: list[str] = Field(default_factory=list)
    market_price_at_signal: float = 0.0       # whale's fill price; base for entry distance
    estimated_half_life_minutes: float = 0.0  # edge decay estimate shown at approval
    # Fields populated by decision_agent at proposal-build time for operator display:
    current_price: float = 0.0        # live market mid-price when proposal was created
    estimated_slippage: float = 0.0   # proxy: size_usdc / liquidity_usdc (fail-closed at 1.0)


class AlertMessage(BaseModel):
    """
    Alert published to CHANNEL_BOT_ALERTS by any layer that needs to notify operators.
    Consumed by telegram/bot._alert_loop() which calls send_alert() on receipt.

    Publishers (all in agent_core — no layer coupling: just a Redis publish to a known channel):
      decision_agent  → "circuit_breaker"  when daily loss gate fires
      trap_detector   → "trap"             when a whale trap is detected on a signal
      position_manager → "position_closed" when a position is closed with P&L result
      position_manager → "whale_exit"      when a contributing whale starts selling

    urgent: True prefixes the Telegram message with "🚨 URGENT:" — reserved for
    circuit_breaker and trap (capital at risk). position_closed and whale_exit are INFO.
    """

    alert_type: Literal["circuit_breaker", "trap", "position_closed", "whale_exit"]
    message: str
    urgent: bool = False


class PositionState(BaseModel):
    """
    Runtime position state stored in Redis (meg:open_positions hash).

    Mirrors PRD §9.4.4 position state schema. Serialized as JSON via
    model_dump_json() / model_validate_json(). Separate from the Position
    ORM model (meg/db/models.py) which handles DB persistence.

    Written by position_manager on open/close. Read by:
      - risk_controller (exposure checks via position_manager helpers)
      - monitor loop (TP/SL/whale exit checking)
      - dashboard API (current positions view)

    Position lifecycle (v1):
      OPEN → TP/SL/whale exit flagged → operator approves exit → CLOSED/EXITED
    """

    position_id: str
    market_id: str
    outcome: Outcome
    entry_price: float
    current_price: float
    size_usdc: float
    shares: float
    unrealized_pnl_usdc: float = 0.0
    unrealized_pnl_pct: float = 0.0
    entry_signal_id: str
    contributing_wallets: list[str] = Field(default_factory=list)
    whale_archetype: Archetype = "INFORMATION"
    opened_at_ms: int
    take_profit_price: float
    stop_loss_price: float
    whale_exit_detected: bool = False
    whale_exit_detected_at_ms: int | None = None
    saturation_score_at_entry: float = 0.0
    status: Literal["OPEN", "CLOSED", "EXITED"] = "OPEN"


# ── Market state model ────────────────────────────────────────────────────────


class MarketState(BaseModel):
    """
    Current market state as cached by CLOBMarketFeed in Redis.

    Serialized as JSON and stored per-market key. Consumed by:
      - pre_filter.market_quality (liquidity, spread, participants, days_to_resolution)
      - signal_engine.contrarian_detector (bid/ask, volume)
      - signal_engine.saturation_monitor (volume, participants)
      - execution.slippage_guard (bid, ask, spread)

    price_history is NOT in this model — it lives in a separate Redis sorted
    set (key: RedisKeys.market_price_history) scored by timestamp_ms.

    days_to_resolution: calendar days until market end_date. None for indefinite
    markets or when end_date cannot be parsed from the CLOB API response.
    Gate 1 checks: days_to_resolution >= config.pre_filter.min_days_to_resolution.
    If None, the check is skipped (conservative — allows trade to proceed).
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
    # None when market has no end date (indefinite) or date parse fails.
    # Gate 1 skips the days_to_resolution check when None.
    days_to_resolution: int | None = None


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
    CHANNEL_WALLET_PENALTIES: str = "wallet_penalties"
    # Operator alert channel: AlertMessage JSON published by any layer, consumed by bot._alert_loop.
    CHANNEL_BOT_ALERTS: str = "bot_alerts"

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

    # Full wallet JSON blob written by wallet_registry dual-write (TTL 300s).
    # Read by Gate 3 (intent_classifier) for total_capital_usdc and conviction data.
    @staticmethod
    def wallet_data(address: str) -> str:
        return f"wallet:{address}:data"

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

    # Sorted set window for consensus_filter: member=wallet_address, score=timestamp_ms.
    # Scoped by outcome so YES and NO consensus windows are tracked independently.
    # Key: market:{market_id}:consensus:{outcome}  (e.g. "market:abc:consensus:YES")
    @staticmethod
    def consensus_window(market_id: str, outcome: str) -> str:
        return f"market:{market_id}:consensus:{outcome}"

    # Market category string written by CLOBMarketFeed from CLOB /markets/{id} response.
    # Read by polygon_feed when enriching RawWhaleTrade. "" when not yet polled.
    @staticmethod
    def market_category(market_id: str) -> str:
        return f"market:{market_id}:category"

    # Serialized MegConfig JSON — set by config_loader after each hot-reload
    @staticmethod
    def meg_config() -> str:
        return "meg:config"

    # Gate 1: markets that failed quality check cached here with 1-hour TTL.
    # CLOBMarketFeed is NOT responsible for writing this key — Gate 1 writes it
    # on every rejection so subsequent events on the same market skip the check.
    @staticmethod
    def market_quality_failed(market_id: str) -> str:
        return f"market:{market_id}:quality_failed"

    # Written by CLOBMarketFeed on every poll. Value is int string (calendar days
    # until market end_date) or "" (empty string) when end_date is None/unparseable.
    # Gate 1 skips the days check when the value is absent or empty (conservative).
    @staticmethod
    def market_days_to_resolution(market_id: str) -> str:
        return f"market:{market_id}:days_to_resolution"

    # ── Position tracking keys (written by position_manager) ──────────────────

    # Hash of all open positions: field=position_id, value=JSON-serialised position state.
    # position_manager uses HSET/HDEL/HGETALL. Single hash keeps all positions accessible
    # with one HGETALL call for risk_controller gate checks.
    @staticmethod
    def open_positions() -> str:
        return "meg:open_positions"

    # JSON-serialised position state for a single position.
    # Redundant with the open_positions hash field but used for direct lookup by ID.
    # TTL is set to 0 (no expiry) — positions must be explicitly closed by position_manager.
    @staticmethod
    def position(position_id: str) -> str:
        return f"position:{position_id}"

    # Running net P&L for the current UTC day in USDC (float string).
    # Reset to "0" at midnight UTC by position_manager daily reset task.
    # risk_controller reads this for the circuit breaker (Gate 2).
    @staticmethod
    def daily_pnl_usdc() -> str:
        return "meg:daily_pnl_usdc"

    # Current portfolio value in USDC (float string).
    # Written by position_manager after every open/close. Initialised from
    # kelly.portfolio_value_usdc config on first start. Used by risk_controller
    # for max_portfolio_exposure_pct and max_position_pct gate checks.
    @staticmethod
    def portfolio_value_usdc() -> str:
        return "meg:portfolio_value_usdc"

    # Total USDC currently deployed in a specific market (float string).
    # Written by position_manager on open/close. Read by risk_controller
    # for max_market_exposure_pct gate check (Gate 4).
    @staticmethod
    def market_exposure_usdc(market_id: str) -> str:
        return f"market:{market_id}:exposure_usdc"

    # Emergency pause flag. SET "1" to pause, DEL to resume.
    # Written by Telegram /pause and /resume commands.
    # Read by decision_agent on every signal — bypasses hot-reload latency.
    # NOT in config.yaml: runtime state must be mutable by Telegram bot atomically.
    @staticmethod
    def system_paused() -> str:
        return "meg:system_paused"

    # Pending approval proposal. Stored by telegram/bot.send_approval_request()
    # when a TradeProposal is sent to the approval chat. Deleted by
    # handle_approval_callback() on first approve/reject (double-click guard).
    # TTL = config.signal.ttl_seconds — proposal auto-expires when signal edge is gone.
    # Value: TradeProposal.model_dump_json()
    @staticmethod
    def pending_proposal(proposal_id: str) -> str:
        return f"proposal:{proposal_id}:pending"

    # Manual exit request flag. SET by dashboard POST /positions/{id}/exit.
    # Consumed by position_manager monitoring loop: when present, initiates close
    # flow on next tick then DELs this key. Using Redis ensures the request survives
    # an API restart and is processed even if the request arrives between monitor ticks.
    # TTL: none (persists until position_manager processes it).
    @staticmethod
    def exit_requested(position_id: str) -> str:
        return f"position:{position_id}:exit_requested"
