"""
Bootstrap script: seed the wallet registry from public leaderboard data.

Sources:
  - Dune Analytics Polymarket dashboards (see CLAUDE.md Key Resources)
  - Polymarket public leaderboard API

Usage:
    python scripts/bootstrap_wallets.py --source dune --limit 500

This script is run once (or periodically) to populate wallet_scores with
historical performance data for known high-volume wallets. It is NOT part
of the live trading pipeline.
"""
from __future__ import annotations


def main() -> None:
    """Fetch wallet data from configured sources and upsert into wallet registry."""
    raise NotImplementedError("bootstrap_wallets.main")


def fetch_from_dune(query_id: str, limit: int) -> list[dict]:
    """Execute a Dune Analytics query and return wallet rows."""
    raise NotImplementedError("bootstrap_wallets.fetch_from_dune")


def fetch_from_leaderboard(limit: int) -> list[dict]:
    """Fetch top wallets from the Polymarket public leaderboard API."""
    raise NotImplementedError("bootstrap_wallets.fetch_from_leaderboard")


if __name__ == "__main__":
    main()
