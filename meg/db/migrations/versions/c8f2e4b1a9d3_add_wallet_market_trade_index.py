"""add compound index ix_trades_wallet_market_time for Gate 3 hot path

This index covers the query pattern in wallet_registry.get_recent_trades()
and get_recent_same_direction():

    SELECT * FROM trades
    WHERE wallet_address = ?
      AND market_id = ?
      AND traded_at >= ?
    ORDER BY traded_at

Without this index, PostgreSQL uses ix_trades_wallet_address and scans all
trades for the wallet in memory before filtering by market_id and time.
For a whale with 500+ trades across many markets that is an O(500) scan
per Gate 3 evaluation. This index reduces it to O(log N + results).

Revision ID: c8f2e4b1a9d3
Revises: b4e2f9a1c3d7
Create Date: 2026-03-14
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "c8f2e4b1a9d3"
down_revision = "b4e2f9a1c3d7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "ix_trades_wallet_market_time",
        "trades",
        ["wallet_address", "market_id", "traded_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_trades_wallet_market_time", table_name="trades")
