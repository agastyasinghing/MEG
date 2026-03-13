"""
Whale wallet registry — PostgreSQL reads/writes and Redis score cache.

Maintains the database of tracked whale wallets, their scores, archetypes,
and historical performance. The registry is the source of truth for wallet
qualification. Redis caches hot-path score lookups (TTL: 5 minutes).

  PostgreSQL (wallet_scores table)
       ↑↓ writes/reads via SQLAlchemy
  wallet_registry.py
       ↑↓ caches scores
  Redis (wallet:{address}:score keys)
"""
from __future__ import annotations

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig


async def get_wallet(address: str, redis: Redis) -> dict | None:
    """
    Return wallet data for the given address, or None if not in registry.
    Checks Redis cache first; falls back to PostgreSQL on cache miss.
    """
    raise NotImplementedError("wallet_registry.get_wallet")


async def upsert_wallet(address: str, data: dict, redis: Redis) -> None:
    """
    Insert or update a wallet record in PostgreSQL.
    Invalidates the Redis cache for this address.
    """
    raise NotImplementedError("wallet_registry.upsert_wallet")


async def get_qualified_whale_wallets(
    config: MegConfig,
    redis: Redis,
) -> list[dict]:
    """
    Return all wallets that meet current whale qualification thresholds
    (win_rate, closed_positions, volume, profitable_months, archetype exclusions).
    Thresholds are read from config — hot-reloadable.
    """
    raise NotImplementedError("wallet_registry.get_qualified_whale_wallets")


async def is_qualified_whale(
    address: str,
    config: MegConfig,
    redis: Redis,
) -> bool:
    """
    Return True if the wallet meets all whale qualification thresholds.
    Fast path: checks cached score in Redis before hitting PostgreSQL.
    """
    raise NotImplementedError("wallet_registry.is_qualified_whale")


async def update_wallet_score(
    address: str,
    score: float,
    redis: Redis,
) -> None:
    """
    Persist an updated score to PostgreSQL and refresh the Redis cache.
    Called by the reputation decay system after each trade outcome.
    """
    raise NotImplementedError("wallet_registry.update_wallet_score")


async def get_wallet_archetype(address: str, redis: Redis) -> str | None:
    """
    Return the archetype string for a wallet (INFORMATION/MOMENTUM/ARBITRAGE/MANIPULATOR),
    or None if unknown. Cached in Redis.
    """
    raise NotImplementedError("wallet_registry.get_wallet_archetype")
