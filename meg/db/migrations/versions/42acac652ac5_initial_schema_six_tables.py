"""initial_schema_six_tables

Revision ID: 42acac652ac5
Revises:
Create Date: 2026-03-13

Creates all six MEG tables:
  - wallets            (whale wallet registry)
  - trades             (raw on-chain trade observations)
  - wallet_scores      (time-series reputation scores)
  - signal_outcomes    (every signal: FILTERED or EXECUTED — training data moat)
  - whale_trap_events  (detected pump-and-exit patterns)
  - positions          (open and closed trading positions)

Index strategy locked in plan-eng-review:
  - Leaderboard, score history, signal log, market activity, dedup all covered.
  - No PG native enums — VARCHAR avoids ALTER TYPE on future status additions.
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "42acac652ac5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── wallets ────────────────────────────────────────────────────────────────
    op.create_table(
        "wallets",
        sa.Column("address", sa.String(42), primary_key=True, nullable=False),
        sa.Column("archetype", sa.String(20), nullable=False),
        sa.Column("is_qualified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("composite_whale_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("win_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("avg_lead_time_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("roi_30d", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("roi_90d", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("roi_all_time", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_closed_positions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("consistency_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("avg_conviction_ratio", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("reputation_decay_factor", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("category_scores", JSONB, nullable=False, server_default="{}"),
        sa.Column(
            "first_seen_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index(
        "ix_wallets_qualified_score",
        "wallets",
        ["is_qualified", sa.text("composite_whale_score DESC")],
    )
    op.create_index("ix_wallets_archetype", "wallets", ["archetype"])

    # ── trades ─────────────────────────────────────────────────────────────────
    # No FK on wallet_address — soft reference by design. See models.py docstring.
    op.create_table(
        "trades",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("wallet_address", sa.String(42), nullable=False),
        sa.Column("market_id", sa.String(), nullable=False),
        sa.Column("outcome", sa.String(3), nullable=False),
        sa.Column("size_usdc", sa.Numeric(18, 6), nullable=False),
        sa.Column("traded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("tx_hash", sa.String(66), nullable=False),
        sa.Column("block_number", sa.BigInteger(), nullable=False),
        sa.Column("market_price_at_trade", sa.Numeric(10, 6), nullable=False),
        sa.Column("is_qualified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("intent", sa.String(20), nullable=True),
        sa.Column("whale_score_at_trade", sa.Float(), nullable=True),
        sa.UniqueConstraint("tx_hash", name="uq_trades_tx_hash"),
    )
    op.create_index("ix_trades_wallet_address", "trades", ["wallet_address"])
    op.create_index(
        "ix_trades_market_traded_at",
        "trades",
        ["market_id", sa.text("traded_at DESC")],
    )

    # ── wallet_scores ──────────────────────────────────────────────────────────
    op.create_table(
        "wallet_scores",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column(
            "wallet_address",
            sa.String(42),
            sa.ForeignKey("wallets.address", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "computed_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("win_rate", sa.Float(), nullable=False),
        sa.Column("avg_lead_time_hours", sa.Float(), nullable=False),
        sa.Column("lead_time_score", sa.Float(), nullable=False),
        sa.Column("roi_30d", sa.Float(), nullable=False),
        sa.Column("roi_90d", sa.Float(), nullable=False),
        sa.Column("roi_all_time", sa.Float(), nullable=False),
        sa.Column("total_closed_positions", sa.Integer(), nullable=False),
        sa.Column("consistency_score", sa.Float(), nullable=False),
        sa.Column("avg_conviction_ratio", sa.Float(), nullable=False),
        sa.Column("reputation_decay_factor", sa.Float(), nullable=False),
        sa.Column("composite_whale_score", sa.Float(), nullable=False),
        sa.Column("is_qualified", sa.Boolean(), nullable=False),
        sa.Column("archetype", sa.String(20), nullable=False),
        sa.Column("category_scores", JSONB, nullable=False, server_default="{}"),
    )
    op.create_index(
        "ix_wallet_scores_address_computed_at",
        "wallet_scores",
        ["wallet_address", sa.text("computed_at DESC")],
    )

    # ── signal_outcomes ────────────────────────────────────────────────────────
    op.create_table(
        "signal_outcomes",
        sa.Column("signal_id", sa.String(64), primary_key=True, nullable=False),
        sa.Column("market_id", sa.String(), nullable=False),
        sa.Column("outcome", sa.String(3), nullable=False),
        sa.Column("composite_score", sa.Float(), nullable=False),
        sa.Column("recommended_size_usdc", sa.Numeric(18, 6), nullable=False),
        sa.Column("kelly_fraction", sa.Float(), nullable=False),
        sa.Column("scores_json", JSONB, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("triggering_wallet", sa.String(42), nullable=False),
        sa.Column("contributing_wallets", JSONB, nullable=False, server_default="[]"),
        sa.Column("whale_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_contrarian", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_ladder", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("intent", sa.String(20), nullable=False, server_default="SIGNAL"),
        sa.Column("market_price_at_signal", sa.Numeric(10, 6), nullable=False),
        sa.Column("saturation_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("trap_warning", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "fired_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_pnl_usdc", sa.Numeric(18, 6), nullable=True),
    )
    op.create_index(
        "ix_signal_outcomes_status_fired_at",
        "signal_outcomes",
        ["status", sa.text("fired_at DESC")],
    )
    op.create_index(
        "ix_signal_outcomes_market_fired_at",
        "signal_outcomes",
        ["market_id", sa.text("fired_at DESC")],
    )
    op.create_index(
        "ix_signal_outcomes_composite_score",
        "signal_outcomes",
        ["composite_score"],
    )

    # ── whale_trap_events ──────────────────────────────────────────────────────
    op.create_table(
        "whale_trap_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column(
            "wallet_address",
            sa.String(42),
            sa.ForeignKey("wallets.address", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("market_id", sa.String(), nullable=False),
        sa.Column(
            "detected_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("pump_size_usdc", sa.Numeric(18, 6), nullable=False),
        sa.Column("exit_size_usdc", sa.Numeric(18, 6), nullable=True),
        sa.Column("time_between_ms", sa.BigInteger(), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index(
        "ix_whale_trap_wallet_detected_at",
        "whale_trap_events",
        ["wallet_address", sa.text("detected_at DESC")],
    )
    op.create_index("ix_whale_trap_market_id", "whale_trap_events", ["market_id"])

    # ── positions ──────────────────────────────────────────────────────────────
    # No FK on entry_signal_id — soft reference by design. See models.py docstring.
    op.create_table(
        "positions",
        sa.Column("position_id", sa.String(64), primary_key=True, nullable=False),
        sa.Column("market_id", sa.String(), nullable=False),
        sa.Column("outcome", sa.String(3), nullable=False),
        sa.Column("entry_price", sa.Numeric(10, 6), nullable=False),
        sa.Column("current_price", sa.Numeric(10, 6), nullable=False),
        sa.Column("size_usdc", sa.Numeric(18, 6), nullable=False),
        sa.Column("shares", sa.Numeric(18, 8), nullable=False),
        sa.Column("unrealized_pnl_usdc", sa.Numeric(18, 6), nullable=False, server_default="0.0"),
        sa.Column("unrealized_pnl_pct", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("entry_signal_id", sa.String(64), nullable=False),
        sa.Column("contributing_wallets", JSONB, nullable=False, server_default="[]"),
        sa.Column("whale_archetype", sa.String(20), nullable=False),
        sa.Column(
            "opened_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("take_profit_price", sa.Numeric(10, 6), nullable=False),
        sa.Column("stop_loss_price", sa.Numeric(10, 6), nullable=False),
        sa.Column("whale_exit_detected", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("whale_exit_detected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("saturation_score_at_entry", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(10), nullable=False, server_default="OPEN"),
        sa.Column("resolved_pnl_usdc", sa.Numeric(18, 6), nullable=True),
    )
    op.create_index("ix_positions_status", "positions", ["status"])
    op.create_index("ix_positions_entry_signal_id", "positions", ["entry_signal_id"])
    op.create_index(
        "ix_positions_opened_at",
        "positions",
        [sa.text("opened_at DESC")],
    )


def downgrade() -> None:
    op.drop_table("positions")
    op.drop_table("whale_trap_events")
    op.drop_table("signal_outcomes")
    op.drop_table("wallet_scores")
    op.drop_table("trades")
    op.drop_table("wallets")
