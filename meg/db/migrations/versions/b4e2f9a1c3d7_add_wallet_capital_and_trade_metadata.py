"""add_wallet_capital_and_trade_metadata

Revision ID: b4e2f9a1c3d7
Revises: 42acac652ac5
Create Date: 2026-03-13

Adds data-layer-blocking columns to wallets and trades tables.

wallets additions:
  - total_volume_usdc      (Numeric 18,2) — incremented by data_layer on each trade
  - total_trades           (Integer)      — count of observed on-chain trades
  - total_capital_usdc     (Numeric 18,2, nullable) — USDC balance; filled by CapitalRefreshJob
  - is_tracked             (Boolean)      — seen on-chain, not yet evaluated
  - is_excluded            (Boolean)      — ARBITRAGE/MANIPULATOR; never follow
  - exclusion_reason       (Text, nullable)
  - avg_hold_time_hours    (Float, nullable) — used by intent classifier for archetype detection

trades additions:
  - market_category        (String 64, nullable) — e.g. "politics", "crypto"
  - lead_time_hours        (Float, nullable)     — hours before resolution; set post-resolution
  - exit_price             (Numeric 6,4, nullable)
  - exit_at                (TIMESTAMPTZ, nullable)
  - resolved_at            (TIMESTAMPTZ, nullable)
  - resolution             (String 16, nullable) — "YES" or "NO"
  - pnl_usdc               (Numeric 18,6, nullable) — filled by PnL backfill job
  - pnl_pct                (Float, nullable)
  - tx_hash_exit           (String 66, nullable) — CLOB exit tx; NULL for paper trades

Index additions:
  - ix_trades_market_category on trades(market_category)
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "b4e2f9a1c3d7"
down_revision = "42acac652ac5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── wallets: tracking stats ────────────────────────────────────────────────
    op.add_column(
        "wallets",
        sa.Column(
            "total_volume_usdc",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0.0",
        ),
    )
    op.add_column(
        "wallets",
        sa.Column(
            "total_trades",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "wallets",
        sa.Column("total_capital_usdc", sa.Numeric(18, 2), nullable=True),
    )

    # ── wallets: registry state ────────────────────────────────────────────────
    op.add_column(
        "wallets",
        sa.Column(
            "is_tracked",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )
    op.add_column(
        "wallets",
        sa.Column(
            "is_excluded",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )
    op.add_column(
        "wallets",
        sa.Column("exclusion_reason", sa.Text(), nullable=True),
    )

    # ── wallets: archetype classification input ────────────────────────────────
    op.add_column(
        "wallets",
        sa.Column("avg_hold_time_hours", sa.Float(), nullable=True),
    )

    # ── trades: market metadata ────────────────────────────────────────────────
    op.add_column(
        "trades",
        sa.Column("market_category", sa.String(64), nullable=True),
    )
    op.add_column(
        "trades",
        sa.Column("lead_time_hours", sa.Float(), nullable=True),
    )

    # ── trades: exit / resolution data ────────────────────────────────────────
    op.add_column(
        "trades",
        sa.Column("exit_price", sa.Numeric(6, 4), nullable=True),
    )
    op.add_column(
        "trades",
        sa.Column("exit_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "trades",
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "trades",
        sa.Column("resolution", sa.String(16), nullable=True),
    )
    op.add_column(
        "trades",
        sa.Column("pnl_usdc", sa.Numeric(18, 6), nullable=True),
    )
    op.add_column(
        "trades",
        sa.Column("pnl_pct", sa.Float(), nullable=True),
    )
    op.add_column(
        "trades",
        sa.Column("tx_hash_exit", sa.String(66), nullable=True),
    )

    # ── index: trades.market_category ─────────────────────────────────────────
    op.create_index(
        "ix_trades_market_category",
        "trades",
        ["market_category"],
    )


def downgrade() -> None:
    # trades index
    op.drop_index("ix_trades_market_category", table_name="trades")

    # trades columns (reverse order)
    op.drop_column("trades", "tx_hash_exit")
    op.drop_column("trades", "pnl_pct")
    op.drop_column("trades", "pnl_usdc")
    op.drop_column("trades", "resolution")
    op.drop_column("trades", "resolved_at")
    op.drop_column("trades", "exit_at")
    op.drop_column("trades", "exit_price")
    op.drop_column("trades", "lead_time_hours")
    op.drop_column("trades", "market_category")

    # wallets columns (reverse order)
    op.drop_column("wallets", "avg_hold_time_hours")
    op.drop_column("wallets", "exclusion_reason")
    op.drop_column("wallets", "is_excluded")
    op.drop_column("wallets", "is_tracked")
    op.drop_column("wallets", "total_capital_usdc")
    op.drop_column("wallets", "total_trades")
    op.drop_column("wallets", "total_volume_usdc")
