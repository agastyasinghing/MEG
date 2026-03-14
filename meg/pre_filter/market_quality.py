"""
Pre-filter Gate 1: Market Quality Filter.

Rejects trades on markets that don't meet minimum liquidity, spread, and
participant thresholds. A signal on a thin or manipulable market is worthless
regardless of the whale's quality.

Gate decision:
  RawWhaleTrade ──► check() ──► True  → pass to Gate 2 (arb exclusion)
                            └──► False → log FILTERED via structlog, discard

State machine for stale/missing market data:

  last_updated_ms absent (UNCHARACTERIZED)
    → fail closed, do NOT write quality_failed cache
    → CLOBMarketFeed may populate within seconds — retry on next trade event

  last_updated_ms present, thresholds fail (BELOW_THRESHOLD)
    → fail closed, SET quality_failed EX 3600
    → cache the rejection so subsequent events skip the full check for 1 hour

  all thresholds pass (PASS)
    → return True

This distinction matters: caching a missing-data failure would block a brand-new
market for 1 hour even if CLOBMarketFeed populates it within the next 5-second
poll cycle. Only confirmed quality failures earn the negative cache entry.

Architecture note: This module reads from Redis only. No imports from data_layer.
All market state keys are written by CLOBMarketFeed (data_layer/clob_client.py)
via the RedisKeys contract in meg/core/events.py.
"""
from __future__ import annotations

import structlog
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import RawWhaleTrade, RedisKeys

logger = structlog.get_logger(__name__)

# How long a confirmed quality failure is cached (seconds).
# After this TTL expires, the next event on the market re-checks all thresholds.
_QUALITY_FAILED_TTL_SECONDS = 3600


async def check(trade: RawWhaleTrade, redis: Redis, config: MegConfig) -> bool:
    """
    Return True if the trade's market meets all quality thresholds:
      - Market liquidity >= config.pre_filter.min_market_liquidity_usdc
      - Bid-ask spread <= config.pre_filter.max_spread_pct
      - Unique participant count >= config.pre_filter.min_unique_participants
      - days_to_resolution >= config.pre_filter.min_days_to_resolution
        (skipped when days_to_resolution is None — indefinite markets pass)

    Fast exit: if market:{id}:quality_failed exists in Redis, return False
    immediately without reading any other keys.

    On missing market data (CLOBMarketFeed hasn't polled yet): fail closed
    without writing the quality_failed cache — the market is UNCHARACTERIZED,
    not BELOW_THRESHOLD. The next trade on the same market will re-check.
    """
    market_id = trade.market_id

    # Fast path: cached rejection from a prior confirmed quality failure.
    if await redis.exists(RedisKeys.market_quality_failed(market_id)):
        logger.debug(
            "market_quality.cached_rejection",
            market_id=market_id,
            tx_hash=trade.tx_hash,
        )
        return False

    # Guard: check whether CLOBMarketFeed has ever polled this market.
    # If last_updated_ms is absent, the market is UNCHARACTERIZED — we fail
    # closed but do NOT write quality_failed so the next event gets a fresh check.
    last_updated_ms = await _get_last_updated_ms(market_id, redis)
    if last_updated_ms is None:
        logger.warning(
            "market_quality.uncharacterized_market",
            market_id=market_id,
            tx_hash=trade.tx_hash,
            reason="last_updated_ms absent — CLOBMarketFeed has not polled this market yet",
        )
        return False

    # Fetch all quality metrics (individual reads — serial at v1 whale frequency).
    liquidity = await _get_market_liquidity(market_id, redis)
    spread = await _get_market_spread(market_id, redis)
    participants = await _get_participants(market_id, redis)
    days_to_resolution = await _get_days_to_resolution(market_id, redis)

    pf = config.pre_filter
    failures: list[str] = []

    if liquidity is None or liquidity < pf.min_market_liquidity_usdc:
        failures.append(f"liquidity={liquidity} < min={pf.min_market_liquidity_usdc}")

    if spread is None or spread > pf.max_spread_pct:
        failures.append(f"spread={spread} > max={pf.max_spread_pct}")

    if participants is None or participants < pf.min_unique_participants:
        failures.append(f"participants={participants} < min={pf.min_unique_participants}")

    # days_to_resolution check: skip when None (indefinite or unparseable market).
    # This is the conservative default — undefined resolution timing should not
    # block a trade, but a confirmed near-expiry market should.
    if days_to_resolution is not None and days_to_resolution < pf.min_days_to_resolution:
        failures.append(
            f"days_to_resolution={days_to_resolution} < min={pf.min_days_to_resolution}"
        )

    if failures:
        # Confirmed BELOW_THRESHOLD — write the negative cache.
        await redis.set(
            RedisKeys.market_quality_failed(market_id),
            "1",
            ex=_QUALITY_FAILED_TTL_SECONDS,
        )
        logger.warning(
            "market_quality.rejected",
            market_id=market_id,
            tx_hash=trade.tx_hash,
            wallet_address=trade.wallet_address,
            filter_reason="GATE_1_BELOW_THRESHOLD",
            failures=failures,
        )
        return False

    return True


async def _get_last_updated_ms(market_id: str, redis: Redis) -> int | None:
    """Return last_updated_ms for a market, or None if not yet populated."""
    raw = await redis.get(RedisKeys.market_last_updated_ms(market_id))
    if raw is None:
        return None
    try:
        return int(raw)
    except (ValueError, TypeError):
        return None


async def _get_market_liquidity(market_id: str, redis: Redis) -> float | None:
    """Return the current liquidity (USDC) for a market from Redis cache."""
    raw = await redis.get(RedisKeys.market_liquidity(market_id))
    if raw is None:
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


async def _get_market_spread(market_id: str, redis: Redis) -> float | None:
    """Return the current bid-ask spread (0.0–1.0) from Redis cache."""
    raw = await redis.get(RedisKeys.market_spread(market_id))
    if raw is None:
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


async def _get_participants(market_id: str, redis: Redis) -> int | None:
    """Return unique participant count for a market from Redis cache."""
    raw = await redis.get(RedisKeys.market_participants(market_id))
    if raw is None:
        return None
    try:
        return int(raw)
    except (ValueError, TypeError):
        return None


async def _get_days_to_resolution(market_id: str, redis: Redis) -> int | None:
    """
    Return calendar days until market resolution from Redis cache.

    Returns None when the key is absent, empty, or unparseable.
    CLOBMarketFeed writes an empty string ("") when days_to_resolution is None
    (indefinite market or end_date parse failure). Gate 1 skips the days check
    when None is returned here (conservative — allows trade to proceed).
    """
    raw = await redis.get(RedisKeys.market_days_to_resolution(market_id))
    if not raw:  # None (key absent) or "" (CLOBMarketFeed writes "" for None)
        return None
    try:
        return int(raw)
    except (ValueError, TypeError):
        return None
