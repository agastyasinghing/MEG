"""
SQLAlchemy ORM models for MEG's PostgreSQL database.

Schema authority: PRD §12. Field names and types here must match meg/core/events.py.
Do not alter table definitions without creating a corresponding Alembic migration.
Run: alembic upgrade head

Table relationships:
                        ┌──────────────┐
                        │   wallets    │
                        │  (address PK)│
                        └──────┬───────┘
               ┌───────────────┼───────────────────┐
               │               │                   │
               ▼               ▼                   ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
     │wallet_scores │  │whale_trap_   │  │     trades       │
     │(time-series) │  │   events     │  │ (soft ref only — │
     │FK → wallets  │  │FK → wallets  │  │  wallet may be   │
     └──────────────┘  └──────────────┘  │  unregistered)   │
                                         └──────────────────┘

     ┌────────────────────────────────────────────────────┐
     │                  signal_outcomes                   │
     │  Every signal: FILTERED or EXECUTED. Training moat.│
     │  scores_json JSONB — no migration on new modules.  │
     └──────────────────────┬─────────────────────────────┘
                            │ soft ref (entry_signal_id)
                            ▼
                    ┌──────────────┐
                    │  positions   │
                    │ (open/closed)│
                    └──────────────┘

FK policy:
  wallet_scores.wallet_address  → wallets.address  (hard FK)
  whale_trap_events.wallet_address → wallets.address (hard FK)
  trades.wallet_address         → NO FK (soft ref — feed must never crash on
                                  unknown wallets; app layer logs + queues)
  positions.entry_signal_id     → NO FK (soft ref — signal_outcomes row may
                                  not exist if signal was in-flight on restart)
"""
from __future__ import annotations

import enum
from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# ── Declarative base ──────────────────────────────────────────────────────────


class Base(DeclarativeBase):
    pass


# ── Python enums (stored as VARCHAR via SAEnum(native_enum=False)) ─────────────
# Using VARCHAR avoids ALTER TYPE DDL when adding new values in v1.5/v2.
# Validated at ORM layer; no PG-level type object created.


class WhaleArchetype(str, enum.Enum):
    INFORMATION = "INFORMATION"
    MOMENTUM = "MOMENTUM"
    ARBITRAGE = "ARBITRAGE"
    MANIPULATOR = "MANIPULATOR"


class TradeIntent(str, enum.Enum):
    SIGNAL = "SIGNAL"
    SIGNAL_LADDER = "SIGNAL_LADDER"  # whale building position across multiple trades
    HEDGE = "HEDGE"
    REBALANCE = "REBALANCE"


class SignalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FILTERED = "FILTERED"
    BLOCKED = "BLOCKED"
    EXECUTED = "EXECUTED"
    EXPIRED = "EXPIRED"
    TRAP_DETECTED = "TRAP_DETECTED"


class PositionStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    EXITED = "EXITED"  # closed early via whale exit detection


class Outcome(str, enum.Enum):
    YES = "YES"
    NO = "NO"


# ── Helper: timezone-aware UTC timestamp column ───────────────────────────────

def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


# ── Table: wallets ─────────────────────────────────────────────────────────────


class Wallet(Base):
    """
    Registry of tracked whale wallets.

    Populated by bootstrap_wallets.py (initial seed) and by data_layer
    when new qualifying wallets are discovered.

    Score fields here are the CURRENT snapshot — historical scores are in
    wallet_scores (time-series). When reputation_decay updates a score it
    writes a new wallet_scores row AND updates composite_whale_score here.
    """

    __tablename__ = "wallets"

    address: Mapped[str] = mapped_column(String(42), primary_key=True)

    # Classification
    archetype: Mapped[str] = mapped_column(
        SAEnum(WhaleArchetype, native_enum=False), nullable=False
    )
    is_qualified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Current score snapshot (authoritative — wallet_scores has history)
    composite_whale_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    win_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    avg_lead_time_hours: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    roi_30d: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    roi_90d: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    roi_all_time: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total_closed_positions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    consistency_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    avg_conviction_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reputation_decay_factor: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

    # Per-category scores: {"politics": 0.82, "crypto": 0.61, ...}
    category_scores: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Timestamps
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Tracking stats (updated incrementally by data_layer) ──────────────────
    total_volume_usdc: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0.0)
    total_trades: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Refreshed daily by CapitalRefreshJob (Polygon RPC USDC balance query).
    # NULL until first refresh. Required for conviction ratio calculation.
    total_capital_usdc: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)

    # ── Registry state ────────────────────────────────────────────────────────
    # is_tracked: seen on-chain, not yet evaluated for qualification
    # is_qualified: meets all qualification thresholds (set by wallet_registry.qualify())
    # is_excluded: ARBITRAGE or MANIPULATOR — never used for signals
    is_tracked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_excluded: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    exclusion_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # For archetype classification: avg_lead_time_hours > 4 AND avg_hold_time_hours > 24 = INFORMATION
    avg_hold_time_hours: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        # Leaderboard query: WHERE is_qualified = true ORDER BY composite_whale_score DESC
        Index("ix_wallets_qualified_score", "is_qualified", composite_whale_score.desc()),
        # Filter by archetype
        Index("ix_wallets_archetype", "archetype"),
    )


# ── Table: trades ──────────────────────────────────────────────────────────────


class Trade(Base):
    """
    All whale trades observed on-chain, raw and qualified.

    NOTE: wallet_address has NO FK constraint to wallets.address.
    The data_layer feed writes trades the moment they appear on-chain.
    A wallet may not be registered yet at insert time.
    Referential integrity is enforced at application layer — unknown wallets
    are logged and queued for registration.
    See architecture decision: "soft ref on trades.wallet_address".
    """

    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # No FK — wallet may not be registered yet (see docstring)
    wallet_address: Mapped[str] = mapped_column(String(42), nullable=False)
    market_id: Mapped[str] = mapped_column(String, nullable=False)
    outcome: Mapped[str] = mapped_column(SAEnum(Outcome, native_enum=False), nullable=False)
    size_usdc: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    traded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    tx_hash: Mapped[str] = mapped_column(String(66), nullable=False)
    block_number: Mapped[int] = mapped_column(BigInteger, nullable=False)
    market_price_at_trade: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)

    # Set by pre_filter after qualification
    is_qualified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    intent: Mapped[str | None] = mapped_column(
        SAEnum(TradeIntent, native_enum=False), nullable=True
    )
    whale_score_at_trade: Mapped[float | None] = mapped_column(Float, nullable=True)

    # ── Market metadata (set by clob_client / data layer) ────────────────────
    # e.g. "politics", "crypto", "sports" — used for category-weighted scores
    market_category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Hours before market resolution when trade was entered (lead-lag signal)
    lead_time_hours: Mapped[float | None] = mapped_column(Float, nullable=True)

    # ── Exit tracking (filled by position_manager on close) ──────────────────
    exit_price: Mapped[float | None] = mapped_column(Numeric(6, 4), nullable=True)
    exit_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # "YES" | "NO" — which outcome resolved as winner
    resolution: Mapped[str | None] = mapped_column(String(16), nullable=True)
    # NULL until exit; set by PnL backfill job (see TODOS.md)
    pnl_usdc: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    pnl_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Exit tx hash (CLOB exit order); NULL for paper trades
    tx_hash_exit: Mapped[str | None] = mapped_column(String(66), nullable=True)

    __table_args__ = (
        UniqueConstraint("tx_hash", name="uq_trades_tx_hash"),
        # Whale trade history lookups (single wallet — leaderboard, profile)
        Index("ix_trades_wallet_address", "wallet_address"),
        # Market activity view
        Index("ix_trades_market_traded_at", "market_id", traded_at.desc()),
        # Category-filtered signal analytics
        Index("ix_trades_market_category", "market_category"),
        # Hot-path Gate 3 queries: wallet_registry.get_recent_trades() and
        # get_recent_same_direction() both filter on (wallet_address, market_id,
        # traded_at). Without this compound index, PG scans all trades for a wallet
        # then filters by market_id in memory — O(trades_per_wallet) per Gate 3 call.
        Index("ix_trades_wallet_market_time", "wallet_address", "market_id", traded_at.desc()),
    )


# ── Table: wallet_scores ───────────────────────────────────────────────────────


class WalletScore(Base):
    """
    Append-only time-series of wallet score snapshots.

    Written every time reputation_decay recomputes a wallet's score.
    Used by dashboard /whales/{address}/scores/history endpoint.

    NOTE: This table is unbounded by design in v1.
    TODO(v1.5): add retention policy or migrate to TimescaleDB.
    At 500 wallets x 4 rescores/day = ~730k rows/year. Acceptable for v1.
    """

    __tablename__ = "wallet_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Hard FK — score rows must reference a registered wallet
    wallet_address: Mapped[str] = mapped_column(
        String(42),
        ForeignKey("wallets.address", ondelete="CASCADE"),
        nullable=False,
    )
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    win_rate: Mapped[float] = mapped_column(Float, nullable=False)
    avg_lead_time_hours: Mapped[float] = mapped_column(Float, nullable=False)
    lead_time_score: Mapped[float] = mapped_column(Float, nullable=False)
    roi_30d: Mapped[float] = mapped_column(Float, nullable=False)
    roi_90d: Mapped[float] = mapped_column(Float, nullable=False)
    roi_all_time: Mapped[float] = mapped_column(Float, nullable=False)
    total_closed_positions: Mapped[int] = mapped_column(Integer, nullable=False)
    consistency_score: Mapped[float] = mapped_column(Float, nullable=False)
    avg_conviction_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    reputation_decay_factor: Mapped[float] = mapped_column(Float, nullable=False)
    composite_whale_score: Mapped[float] = mapped_column(Float, nullable=False)
    is_qualified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    archetype: Mapped[str] = mapped_column(
        SAEnum(WhaleArchetype, native_enum=False), nullable=False
    )
    # Per-category scores snapshot: {"politics": 0.82, "crypto": 0.61, ...}
    category_scores: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    __table_args__ = (
        # Score history chart: latest-first per wallet
        Index("ix_wallet_scores_address_computed_at", "wallet_address", computed_at.desc()),
    )


# ── Table: signal_outcomes ─────────────────────────────────────────────────────


class SignalOutcome(Base):
    """
    Every signal event, whether FILTERED or EXECUTED. The training data moat.

    Written by signal_engine for ALL signals — sub-threshold signals get
    status=FILTERED. This is what makes MEG's model trainable over time:
    you have both the signals that fired AND the ones that were suppressed,
    with their eventual market outcomes.

    scores_json stores all SignalScores sub-scores as JSONB. Adding a new
    signal module adds a key to this dict — no migration required.

    resolved_pnl_usdc is NULL until the market resolves. A background job
    (TODO: PnL backfill, blocked by execution layer) fills it in.
    See TODOS.md: "positions.resolved_pnl_usdc backfill job".
    """

    __tablename__ = "signal_outcomes"

    signal_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    market_id: Mapped[str] = mapped_column(String, nullable=False)
    outcome: Mapped[str] = mapped_column(SAEnum(Outcome, native_enum=False), nullable=False)
    composite_score: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_size_usdc: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    kelly_fraction: Mapped[float] = mapped_column(Float, nullable=False)

    # All sub-scores from SignalScores. JSONB avoids migration on new signal modules.
    scores_json: Mapped[dict] = mapped_column(JSONB, nullable=False)

    status: Mapped[str] = mapped_column(
        SAEnum(SignalStatus, native_enum=False), nullable=False, default=SignalStatus.PENDING
    )
    triggering_wallet: Mapped[str] = mapped_column(String(42), nullable=False)
    # List of wallet addresses: ["0xabc", "0xdef", ...]
    contributing_wallets: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    whale_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_contrarian: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_ladder: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    intent: Mapped[str] = mapped_column(
        SAEnum(TradeIntent, native_enum=False), nullable=False, default=TradeIntent.SIGNAL
    )
    market_price_at_signal: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)
    saturation_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    trap_warning: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    fired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Filled in by PnL backfill job when market resolves
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_pnl_usdc: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)

    __table_args__ = (
        # Dashboard signal log: latest first, filtered by status
        Index("ix_signal_outcomes_status_fired_at", "status", fired_at.desc()),
        # Market activity view
        Index("ix_signal_outcomes_market_fired_at", "market_id", fired_at.desc()),
        # Signal performance analytics
        Index("ix_signal_outcomes_composite_score", "composite_score"),
    )


# ── Table: whale_trap_events ───────────────────────────────────────────────────


class WhaleTrapEvent(Base):
    """
    Detected pump-and-exit patterns. Written by trap_detector in agent_core.

    Used to:
    1. Block signals from wallets currently in an active trap pattern.
    2. Train future trap detection models (labeled examples).
    3. Alert operators via Telegram when a high-confidence trap is detected.
    """

    __tablename__ = "whale_trap_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Hard FK — traps are always associated with a registered wallet
    wallet_address: Mapped[str] = mapped_column(
        String(42),
        ForeignKey("wallets.address", ondelete="CASCADE"),
        nullable=False,
    )
    market_id: Mapped[str] = mapped_column(String, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    pump_size_usdc: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    exit_size_usdc: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    time_between_ms: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_whale_trap_wallet_detected_at", "wallet_address", detected_at.desc()),
        Index("ix_whale_trap_market_id", "market_id"),
    )


# ── Table: positions ───────────────────────────────────────────────────────────


class Position(Base):
    """
    Open and closed trading positions.

    Written by execution layer when a trade is filled.
    Updated by position_manager as market prices change and on exit.

    entry_signal_id has NO FK constraint to signal_outcomes — the signal row
    is guaranteed to exist by application logic, but we use a soft ref here
    to avoid FK failures on in-flight restarts.

    resolved_pnl_usdc is NULL while position is OPEN. Set on close/exit.
    """

    __tablename__ = "positions"

    position_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    market_id: Mapped[str] = mapped_column(String, nullable=False)
    outcome: Mapped[str] = mapped_column(SAEnum(Outcome, native_enum=False), nullable=False)

    entry_price: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)
    current_price: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)
    size_usdc: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    shares: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    unrealized_pnl_usdc: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False, default=0.0)
    unrealized_pnl_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Soft ref — no FK (see docstring)
    entry_signal_id: Mapped[str] = mapped_column(String(64), nullable=False)
    # List of wallet addresses that contributed to the originating signal
    contributing_wallets: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    whale_archetype: Mapped[str] = mapped_column(
        SAEnum(WhaleArchetype, native_enum=False), nullable=False
    )

    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    take_profit_price: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)
    stop_loss_price: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)

    whale_exit_detected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    whale_exit_detected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    saturation_score_at_entry: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(
        SAEnum(PositionStatus, native_enum=False),
        nullable=False,
        default=PositionStatus.OPEN,
    )

    # NULL while open; set when position closes
    resolved_pnl_usdc: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)

    __table_args__ = (
        # Open positions filter (most common query)
        Index("ix_positions_status", "status"),
        # Signal → position join (for signal performance attribution)
        Index("ix_positions_entry_signal_id", "entry_signal_id"),
        # Recency sort
        Index("ix_positions_opened_at", opened_at.desc()),
    )
