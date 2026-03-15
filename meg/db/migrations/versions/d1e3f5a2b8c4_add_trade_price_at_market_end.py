"""add price_at_market_end to trades

Revision ID: d1e3f5a2b8c4
Revises: c8f2e4b1a9d3
Create Date: 2026-03-14

Adds price_at_market_end to the trades table. PRD §12 requires this column
for lead-lag calibration (comparing whale entry price to where the market
actually resolved) and PnL backfill attribution.

NULL until the PnL backfill job runs post-resolution. The backfill job
(TODOS.md: "resolved_pnl_usdc backfill job") populates this alongside
pnl_usdc and pnl_pct.
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "d1e3f5a2b8c4"
down_revision = "c8f2e4b1a9d3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "trades",
        sa.Column("price_at_market_end", sa.Numeric(6, 4), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("trades", "price_at_market_end")
