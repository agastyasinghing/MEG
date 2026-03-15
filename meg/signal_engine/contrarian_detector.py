"""
Contrarian detector.

Detects when a high-quality whale is trading AGAINST the prevailing order
flow. This is a high-conviction signal: an informed whale fading the crowd
often precedes a market correction. Penalises signals that merely follow
momentum (lower score) and boosts signals that go against it.

Score formula:
  divergence = 0.5 * (1 - trade_direction * order_flow_direction)
    trade_direction: +1.0 for YES, -1.0 for NO
    order_flow_direction: from get_order_flow_direction() in [-1.0, 1.0]

  Result: 1.0 = fully contrarian, 0.5 = neutral, 0.0 = fully momentum

PRD reference: §9.3.8 Contrarian Detector
"""
from __future__ import annotations

import math

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade, RedisKeys

# Sensitivity for normalising price changes to [-1, 1] via tanh.
# price_change of ±0.20 maps to ±0.76 direction.
_PRICE_SENSITIVITY: float = 5.0


async def score(
    trade: QualifiedWhaleTrade,
    redis: Redis,
    config: MegConfig,
) -> float:
    """
    Return a divergence score in [0.0, 1.0].
    1.0 = whale is strongly against prevailing order flow (contrarian — high conviction).
    0.5 = neutral / insufficient order flow data.
    0.0 = whale is following the crowd (momentum — lower information content).

    Scores above config.signal.contrarian_threshold mark the signal as is_contrarian=True
    in the composite scorer (used for Telegram alerts and signal attribution).
    """
    flow_direction = await get_order_flow_direction(trade.market_id, redis)

    trade_direction = 1.0 if trade.outcome == "YES" else -1.0

    divergence = 0.5 * (1.0 - trade_direction * flow_direction)

    return max(0.0, min(1.0, divergence))


async def get_order_flow_direction(
    market_id: str,
    redis: Redis,
) -> float:
    """
    Return the net order flow direction for the market as a float in [-1.0, 1.0].
    +1.0 = strong YES buying pressure, -1.0 = strong NO buying pressure, 0.0 = neutral.

    Inferred from price history trend (primary signal). Falls back to 0.0 when
    no price history is available.
    """
    price_key = RedisKeys.market_price_history(market_id)

    # Fetch all price history entries (member format: "price@timestamp_ms")
    entries = await redis.zrange(price_key, 0, -1, withscores=False)

    if not entries:
        return 0.0

    prices: list[float] = []
    for entry in entries:
        entry_str = entry if isinstance(entry, str) else entry.decode("utf-8")
        try:
            price_str = entry_str.split("@")[0]
            prices.append(float(price_str))
        except (ValueError, IndexError):
            continue

    if len(prices) < 2:
        return 0.0

    # Price change from earliest to latest in the sorted set
    price_change = prices[-1] - prices[0]

    # Normalise to [-1, 1] using tanh with sensitivity scaling
    direction = math.tanh(price_change * _PRICE_SENSITIVITY)

    return max(-1.0, min(1.0, direction))
