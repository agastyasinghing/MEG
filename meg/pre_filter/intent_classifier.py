"""
Pre-filter Gate 3: Intent Classifier.

Classifies a whale trade as one of: SIGNAL, HEDGE, or REBALANCE.
Only SIGNAL trades pass to the signal engine. HEDGE and REBALANCE trades
represent portfolio mechanics, not directional conviction — they are logged
but not acted upon.

NOTE: This module requires Opus + ultrathink per CLAUDE.md model selection
rules. The classification logic directly affects trade execution. Do not
implement with Sonnet.

Gate decision:
  RawWhaleTrade ──► classify() ──► SIGNAL    → emit QualifiedWhaleTrade
                               ├──► HEDGE     → log as FILTERED (intent=HEDGE), discard
                               └──► REBALANCE → log as FILTERED (intent=REBALANCE), discard
"""
from __future__ import annotations

from typing import Literal

from redis.asyncio import Redis

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade, RawWhaleTrade

Intent = Literal["SIGNAL", "HEDGE", "REBALANCE"]


async def classify(
    trade: RawWhaleTrade,
    redis: Redis,
    config: MegConfig,
) -> Intent:
    """
    Classify a whale trade's intent.

    SIGNAL:    Directional conviction — whale is expressing a view on outcome
               probability. Characterised by: new position, significant size
               relative to wallet capital, no opposing position in same market.

    HEDGE:     Risk management — whale is offsetting exposure elsewhere.
               Characterised by: opposing direction to existing position,
               or correlated market positions.

    REBALANCE: Portfolio mechanics — size adjustment, profit-taking, or
               liquidity management. Characterised by: partial exit of existing
               position, or proportional adjustment across multiple markets.

    IMPLEMENT WITH OPUS + ULTRATHINK. See CLAUDE.md model selection rules.
    """
    raise NotImplementedError("intent_classifier.classify")


async def build_qualified_trade(
    trade: RawWhaleTrade,
    intent: Intent,
    redis: Redis,
) -> QualifiedWhaleTrade:
    """
    Construct a QualifiedWhaleTrade from a RawWhaleTrade after classification.
    Enriches with whale_score and archetype from the wallet registry.
    Only call this if intent == SIGNAL.
    """
    raise NotImplementedError("intent_classifier.build_qualified_trade")
