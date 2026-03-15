"""add last_profitable_trade_at to wallets

Revision ID: e2f4a6b8c1d5
Revises: d1e3f5a2b8c4
Create Date: 2026-03-14

Adds last_profitable_trade_at to the wallets table.

Required by lead_lag_scorer.compute_reputation_decay() (PRD §9.3.1):
  decay_factor = exp(-days_since_last_good_trade / tau)

Without this field the reputation decay formula cannot be computed — the scorer
defaults to decay_factor=1.0 (no decay applied) when the column is NULL. This
is a correct conservative fallback for wallets with no profitable trade history.

Populated by the PnL backfill job (TODOS.md: "resolved_pnl_usdc backfill job")
when a position closes with pnl_usdc > 0. Updated in wallet_registry.upsert_wallet()
when the backfill job writes outcome data back to the wallet record.
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "e2f4a6b8c1d5"
down_revision = "d1e3f5a2b8c4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "wallets",
        sa.Column(
            "last_profitable_trade_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("wallets", "last_profitable_trade_at")
