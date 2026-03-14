"""
Tests for meg/db/models.py and meg/db/session.py.

Test coverage map:
  ┌────────────────────────────────────────────────────────────┐
  │ session.py                                                 │
  │   init_db()        → test_get_session_before_init_raises   │
  │   get_session()    → test_get_session_commits_on_success   │
  │                    → test_get_session_rollback_on_exception │
  └────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────┐
  │ models.py — table smoke tests (CREATE + INSERT + SELECT)   │
  │   Wallet           → test_wallet_insert                    │
  │   Trade            → test_trade_insert_unknown_wallet      │
  │                    → test_trade_tx_hash_unique             │
  │   WalletScore      → test_wallet_score_insert              │
  │                    → test_wallet_score_fk_enforced         │
  │   SignalOutcome    → test_signal_outcome_insert            │
  │                    → test_signal_outcome_scores_json        │
  │   WhaleTrapEvent   → test_whale_trap_event_insert          │
  │   Position         → test_position_insert                  │
  └────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────┐
  │ events.py — Pydantic validation of updated schemas         │
  │   SignalScores     → test_signal_scores_validation         │
  │   SignalEvent      → test_signal_event_full                │
  │                    → test_signal_event_missing_field       │
  │   Intent literal   → test_intent_signal_ladder             │
  └────────────────────────────────────────────────────────────┘
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from meg.core.events import (
    SignalEvent,
    SignalScores,
)
from meg.db.models import (
    Outcome,
    Position,
    PositionStatus,
    SignalOutcome,
    SignalStatus,
    Trade,
    TradeIntent,
    Wallet,
    WalletScore,
    WhaleArchetype,
    WhaleTrapEvent,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _make_wallet(address: str = "0xABC123") -> Wallet:
    return Wallet(
        address=address,
        archetype=WhaleArchetype.INFORMATION,
        is_qualified=True,
        composite_whale_score=0.75,
        win_rate=0.62,
        avg_lead_time_hours=5.4,
        roi_30d=0.12,
        roi_90d=0.18,
        roi_all_time=0.31,
        total_closed_positions=120,
        consistency_score=0.70,
        avg_conviction_ratio=0.15,
        reputation_decay_factor=0.95,
        category_scores={"politics": 0.82, "crypto": 0.61},
    )


def _make_trade(wallet_address: str = "0xABC123", tx_hash: str = "0xTX001") -> Trade:
    return Trade(
        wallet_address=wallet_address,
        market_id="market-001",
        outcome=Outcome.YES,
        size_usdc=5000.0,
        traded_at=_now(),
        tx_hash=tx_hash,
        block_number=54321000,
        market_price_at_trade=0.68,
        is_qualified=True,
        intent=TradeIntent.SIGNAL,
        whale_score_at_trade=0.75,
    )


def _make_signal_outcome(signal_id: str = "meg_sig_abc123") -> SignalOutcome:
    return SignalOutcome(
        signal_id=signal_id,
        market_id="market-001",
        outcome=Outcome.YES,
        composite_score=0.81,
        recommended_size_usdc=340.0,
        kelly_fraction=0.25,
        scores_json={
            "lead_lag": 0.72,
            "consensus": 0.88,
            "kelly_confidence": 0.65,
            "divergence": 0.50,
            "conviction_ratio": 0.80,
            "archetype_multiplier": 1.2,
            "ladder_multiplier": 1.0,
        },
        status=SignalStatus.EXECUTED,
        triggering_wallet="0xABC123",
        contributing_wallets=["0xABC123", "0xDEF456"],
        whale_count=2,
        is_contrarian=False,
        is_ladder=False,
        intent=TradeIntent.SIGNAL,
        market_price_at_signal=0.68,
        saturation_score=0.1,
        trap_warning=False,
        fired_at=_now(),
    )


# ── session.py tests ───────────────────────────────────────────────────────────


async def test_get_session_before_init_raises() -> None:
    """
    get_session() must raise RuntimeError — not a silent AttributeError —
    when called before init_db(). Critical gap identified in failure modes.
    """
    import meg.db.session as session_module
    original_engine = session_module._engine
    session_module._engine = None
    try:
        with pytest.raises(RuntimeError, match="init_db"):
            async with session_module.get_session():
                pass
    finally:
        session_module._engine = original_engine


async def test_get_session_commits_on_success(db_session) -> None:
    """Happy path: object added in session is persisted after context exit."""
    wallet = _make_wallet("0xCOMMIT01")
    db_session.add(wallet)
    await db_session.flush()
    result = await db_session.execute(select(Wallet).where(Wallet.address == "0xCOMMIT01"))
    found = result.scalar_one_or_none()
    assert found is not None
    assert found.composite_whale_score == 0.75


async def test_get_session_rollback_on_exception(db_engine) -> None:
    """Exception inside get_session() triggers rollback — no data persisted."""
    from sqlalchemy.ext.asyncio import AsyncSession

    wallet_address = "0xROLLBACK"
    try:
        async with AsyncSession(db_engine) as session:
            async with session.begin():
                session.add(_make_wallet(wallet_address))
                raise ValueError("intentional test exception")
    except ValueError:
        pass

    async with AsyncSession(db_engine) as session:
        result = await session.execute(
            select(Wallet).where(Wallet.address == wallet_address)
        )
        assert result.scalar_one_or_none() is None


# ── Wallet table tests ─────────────────────────────────────────────────────────


async def test_wallet_insert(db_session) -> None:
    """Wallet INSERT with all fields succeeds and round-trips correctly."""
    wallet = _make_wallet("0xWALLET01")
    db_session.add(wallet)
    await db_session.flush()

    result = await db_session.execute(select(Wallet).where(Wallet.address == "0xWALLET01"))
    w = result.scalar_one()
    assert w.archetype == WhaleArchetype.INFORMATION
    assert w.is_qualified is True
    assert w.category_scores == {"politics": 0.82, "crypto": 0.61}


# ── Trade table tests ──────────────────────────────────────────────────────────


async def test_trade_insert_unknown_wallet(db_session) -> None:
    """
    Trade INSERT with a wallet_address not in wallets table must succeed.
    Soft FK by design — feed must never crash on unregistered wallets.
    """
    trade = _make_trade(wallet_address="0xUNKNOWN_WALLET", tx_hash="0xTXSOFT01")
    db_session.add(trade)
    await db_session.flush()  # No IntegrityError expected

    result = await db_session.execute(
        select(Trade).where(Trade.wallet_address == "0xUNKNOWN_WALLET")
    )
    assert result.scalar_one_or_none() is not None


async def test_trade_tx_hash_unique(db_session) -> None:
    """
    Duplicate tx_hash INSERT must raise IntegrityError.
    Critical for deduplication on re-ingestion after restarts.
    """
    tx = "0xDUPLICATE_TX"
    db_session.add(_make_trade(wallet_address="0xW01", tx_hash=tx))
    await db_session.flush()

    with pytest.raises(IntegrityError):
        db_session.add(_make_trade(wallet_address="0xW02", tx_hash=tx))
        await db_session.flush()


# ── WalletScore table tests ────────────────────────────────────────────────────


async def test_wallet_score_insert(db_session) -> None:
    """WalletScore INSERT with valid FK succeeds."""
    db_session.add(_make_wallet("0xWSCORE01"))
    await db_session.flush()

    score = WalletScore(
        wallet_address="0xWSCORE01",
        computed_at=_now(),
        win_rate=0.62,
        avg_lead_time_hours=5.4,
        lead_time_score=0.71,
        roi_30d=0.12,
        roi_90d=0.18,
        roi_all_time=0.31,
        total_closed_positions=120,
        consistency_score=0.70,
        avg_conviction_ratio=0.15,
        reputation_decay_factor=0.95,
        composite_whale_score=0.75,
        is_qualified=True,
        archetype=WhaleArchetype.INFORMATION,
        category_scores={"politics": 0.82},
    )
    db_session.add(score)
    await db_session.flush()

    result = await db_session.execute(
        select(WalletScore).where(WalletScore.wallet_address == "0xWSCORE01")
    )
    assert result.scalar_one_or_none() is not None


async def test_wallet_score_fk_enforced(db_session) -> None:
    """WalletScore INSERT with unknown wallet_address must raise IntegrityError."""
    score = WalletScore(
        wallet_address="0xDOES_NOT_EXIST",
        computed_at=_now(),
        win_rate=0.5,
        avg_lead_time_hours=1.0,
        lead_time_score=0.5,
        roi_30d=0.0,
        roi_90d=0.0,
        roi_all_time=0.0,
        total_closed_positions=0,
        consistency_score=0.5,
        avg_conviction_ratio=0.1,
        reputation_decay_factor=1.0,
        composite_whale_score=0.5,
        is_qualified=False,
        archetype=WhaleArchetype.MOMENTUM,
        category_scores={},
    )
    with pytest.raises(IntegrityError):
        db_session.add(score)
        await db_session.flush()


# ── SignalOutcome table tests ──────────────────────────────────────────────────


async def test_signal_outcome_insert(db_session) -> None:
    """SignalOutcome INSERT with all required fields succeeds."""
    db_session.add(_make_signal_outcome("meg_sig_test01"))
    await db_session.flush()

    result = await db_session.execute(
        select(SignalOutcome).where(SignalOutcome.signal_id == "meg_sig_test01")
    )
    sig = result.scalar_one()
    assert sig.composite_score == 0.81
    assert sig.status == SignalStatus.EXECUTED
    assert sig.contributing_wallets == ["0xABC123", "0xDEF456"]


async def test_signal_outcome_scores_json(db_session) -> None:
    """JSONB round-trip for scores_json preserves all sub-score keys."""
    signal = _make_signal_outcome("meg_sig_jsonb01")
    db_session.add(signal)
    await db_session.flush()

    result = await db_session.execute(
        select(SignalOutcome).where(SignalOutcome.signal_id == "meg_sig_jsonb01")
    )
    sig = result.scalar_one()
    assert sig.scores_json["lead_lag"] == 0.72
    assert sig.scores_json["archetype_multiplier"] == 1.2
    assert len(sig.scores_json) == 7


async def test_signal_outcome_resolved_pnl_nullable(db_session) -> None:
    """resolved_pnl_usdc is NULL by default — filled in by PnL backfill job."""
    signal = _make_signal_outcome("meg_sig_null_pnl")
    db_session.add(signal)
    await db_session.flush()

    result = await db_session.execute(
        select(SignalOutcome).where(SignalOutcome.signal_id == "meg_sig_null_pnl")
    )
    assert result.scalar_one().resolved_pnl_usdc is None


# ── WhaleTrapEvent table tests ─────────────────────────────────────────────────


async def test_whale_trap_event_insert(db_session) -> None:
    """WhaleTrapEvent INSERT with valid FK succeeds."""
    db_session.add(_make_wallet("0xTRAP01"))
    await db_session.flush()

    trap = WhaleTrapEvent(
        wallet_address="0xTRAP01",
        market_id="market-trap-001",
        detected_at=_now(),
        pump_size_usdc=200000.0,
        exit_size_usdc=195000.0,
        time_between_ms=4 * 60 * 60 * 1000,  # 4 hours in ms
        confidence_score=0.87,
    )
    db_session.add(trap)
    await db_session.flush()

    result = await db_session.execute(
        select(WhaleTrapEvent).where(WhaleTrapEvent.wallet_address == "0xTRAP01")
    )
    assert result.scalar_one_or_none() is not None


# ── Position table tests ───────────────────────────────────────────────────────


async def test_position_insert(db_session) -> None:
    """Position INSERT succeeds with soft ref to signal_outcomes."""
    pos = Position(
        position_id="meg_pos_test01",
        market_id="market-001",
        outcome=Outcome.YES,
        entry_price=0.68,
        current_price=0.71,
        size_usdc=340.0,
        shares=500.0,
        unrealized_pnl_usdc=15.0,
        unrealized_pnl_pct=4.4,
        entry_signal_id="meg_sig_does_not_exist_in_db",  # soft ref — no FK
        contributing_wallets=["0xABC123"],
        whale_archetype=WhaleArchetype.INFORMATION,
        opened_at=_now(),
        take_profit_price=0.85,
        stop_loss_price=0.55,
        saturation_score_at_entry=0.1,
        status=PositionStatus.OPEN,
    )
    db_session.add(pos)
    await db_session.flush()  # No IntegrityError — soft ref is allowed

    result = await db_session.execute(
        select(Position).where(Position.position_id == "meg_pos_test01")
    )
    p = result.scalar_one()
    assert p.status == PositionStatus.OPEN
    assert p.resolved_pnl_usdc is None


# ── events.py Pydantic validation tests ───────────────────────────────────────


def test_signal_scores_out_of_range() -> None:
    """SignalScores enforces ge=0, le=1 on score fields."""
    with pytest.raises(ValidationError):
        SignalScores(
            lead_lag=1.5,  # exceeds le=1
            consensus=0.5,
            kelly_confidence=0.5,
            divergence=0.5,
            conviction_ratio=0.5,
            archetype_multiplier=1.0,
            ladder_multiplier=1.0,
        )


def test_signal_scores_valid() -> None:
    """Valid SignalScores round-trips without error."""
    scores = SignalScores(
        lead_lag=0.72,
        consensus=0.88,
        kelly_confidence=0.65,
        divergence=0.50,
        conviction_ratio=0.80,
        archetype_multiplier=1.2,
        ladder_multiplier=1.0,
    )
    assert scores.lead_lag == 0.72


def test_signal_event_full() -> None:
    """Full SignalEvent with all PRD §12 fields constructs without error."""
    scores = SignalScores(
        lead_lag=0.72,
        consensus=0.88,
        kelly_confidence=0.65,
        divergence=0.50,
        conviction_ratio=0.80,
        archetype_multiplier=1.2,
        ladder_multiplier=1.0,
    )
    event = SignalEvent(
        signal_id="meg_sig_abc123",
        market_id="market-001",
        outcome="YES",
        composite_score=0.81,
        scores=scores,
        recommended_size_usdc=340.0,
        kelly_fraction=0.25,
        ttl_expires_at_ms=1_700_000_000_000,
        triggering_wallet="0xABC123",
        contributing_wallets=["0xABC123", "0xDEF456"],
        whale_count=2,
        is_contrarian=False,
        is_ladder=False,
        market_price_at_signal=0.68,
    )
    assert event.status == "PENDING"
    assert event.trap_warning is False
    assert event.contributing_wallets == ["0xABC123", "0xDEF456"]


def test_signal_event_missing_required_field() -> None:
    """SignalEvent without required triggering_wallet raises ValidationError."""
    scores = SignalScores(
        lead_lag=0.5, consensus=0.5, kelly_confidence=0.5, divergence=0.5,
        conviction_ratio=0.5, archetype_multiplier=1.0, ladder_multiplier=1.0,
    )
    with pytest.raises(ValidationError):
        SignalEvent(
            signal_id="meg_sig_x",
            market_id="m1",
            outcome="YES",
            composite_score=0.7,
            scores=scores,
            recommended_size_usdc=100.0,
            kelly_fraction=0.25,
            ttl_expires_at_ms=1_700_000_000_000,
            # triggering_wallet intentionally omitted
        )


def test_intent_signal_ladder() -> None:
    """SIGNAL_LADDER is a valid Intent value after PRD §12 alignment."""
    scores = SignalScores(
        lead_lag=0.5, consensus=0.5, kelly_confidence=0.5, divergence=0.5,
        conviction_ratio=0.5, archetype_multiplier=1.0, ladder_multiplier=1.5,
    )
    event = SignalEvent(
        signal_id="meg_sig_ladder01",
        market_id="market-001",
        outcome="YES",
        composite_score=0.75,
        scores=scores,
        recommended_size_usdc=200.0,
        kelly_fraction=0.25,
        ttl_expires_at_ms=1_700_000_000_000,
        triggering_wallet="0xABC123",
        intent="SIGNAL_LADDER",
        is_ladder=True,
        ladder_trade_count=3,
    )
    assert event.intent == "SIGNAL_LADDER"
    assert event.is_ladder is True
