"""
Pre-filter Gate 3: Intent Classifier.

Classifies a whale trade as one of: SIGNAL, SIGNAL_LADDER, HEDGE, or REBALANCE.
Only SIGNAL and SIGNAL_LADDER trades pass to the signal engine. HEDGE and
REBALANCE represent portfolio mechanics, not directional conviction — they are
logged via structlog but not acted upon.

Gate decision:
  RawWhaleTrade ──► classify() ──► SIGNAL        → build_qualified_trade() → emit
                               ├──► SIGNAL_LADDER → build_qualified_trade() → emit
                               ├──► HEDGE         → log FILTERED, discard
                               └──► REBALANCE     → log FILTERED, discard

⚠️  OPUS + ULTRATHINK REQUIRED
This module's classify() and build_qualified_trade() implementations must be
written in an Opus session. The classification logic directly determines what
reaches the signal engine — getting SIGNAL vs HEDGE/REBALANCE wrong means
either signal starvation (false HEDGEs) or noise injection (REBALANCEs reaching
the signal engine). The test spec is in tests/pre_filter/test_intent_classifier.py
— read that file first, then implement against the tests.

Architecture note: This module reads wallet data directly from Redis (no import
of meg.data_layer.wallet_registry — layer coupling violation). Trade table queries
use meg.db.models (shared infrastructure, not a layer).

Intent definitions:
  SIGNAL:        New directional position. Whale is expressing a view on outcome
                 probability. Characterised by: first or fresh position in this
                 market, size >= config.pre_filter.min_signal_size_pct * capital,
                 no opposing position in the same market.

  SIGNAL_LADDER: Whale is building conviction — multiple same-direction trades in
                 the same market within config.pre_filter.ladder_window_hours.
                 Requires >= config.pre_filter.ladder_min_trades prior same-direction
                 trades within the window. Higher conviction than a single SIGNAL.

  HEDGE:         Risk management. Whale is offsetting exposure elsewhere.
                 Characterised by: opposing direction to an existing position
                 in the same market (YES position + buys NO, or vice versa).

  REBALANCE:     Portfolio mechanics. Size adjustment, profit-taking, or
                 liquidity management. Characterised by: trade size below
                 min_signal_size_pct threshold, or trade reducing/closing
                 an existing same-direction position.
"""
from __future__ import annotations

from typing import Literal

import structlog
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from meg.core.config_loader import MegConfig
from meg.core.events import QualifiedWhaleTrade, RawWhaleTrade

logger = structlog.get_logger(__name__)

Intent = Literal["SIGNAL", "SIGNAL_LADDER", "HEDGE", "REBALANCE"]


async def classify(
    trade: RawWhaleTrade,
    redis: Redis,
    config: MegConfig,
    session: AsyncSession | None = None,
) -> Intent:
    """
    Classify a whale trade's intent. Returns one of: SIGNAL, SIGNAL_LADDER,
    HEDGE, REBALANCE.

    Reads wallet data from Redis:
      wallet:{addr}:data  → JSON blob with composite_whale_score, archetype,
                            total_capital_usdc, avg_conviction_ratio
    Queries Trade table (via session) for:
      - Recent same-direction trades (SIGNAL_LADDER detection, ladder_window_hours)
      - Existing opposing positions (HEDGE detection, arb_detection_window_hours)
      - Existing same-direction positions (REBALANCE detection)

    session=None: Trade table queries are skipped. Behavioral classification
    (HEDGE, REBALANCE, SIGNAL_LADDER) falls back to SIGNAL — conservative
    direction (never filters a trade that could be a SIGNAL).

    IMPLEMENT WITH OPUS + ULTRATHINK. See CLAUDE.md model selection rules.
    Read tests/pre_filter/test_intent_classifier.py first — tests are the spec.
    """
    raise NotImplementedError("intent_classifier.classify")


async def build_qualified_trade(
    trade: RawWhaleTrade,
    intent: Intent,
    redis: Redis,
) -> QualifiedWhaleTrade | None:
    """
    Construct a QualifiedWhaleTrade from a RawWhaleTrade after classification.

    Enriches with whale_score and archetype read directly from Redis keys:
      wallet:{addr}:score     → float string (composite_whale_score)
      wallet:{addr}:archetype → archetype string

    Returns None if wallet data is unavailable in Redis (cache miss with no
    DB fallback). The pipeline logs ERROR and skips the trade in this case —
    never emit a QualifiedWhaleTrade with whale_score=0.0.

    Only call this function if intent is SIGNAL or SIGNAL_LADDER. The pipeline
    guarantees this invariant — build_qualified_trade is never called for
    HEDGE or REBALANCE intents.

    IMPLEMENT WITH OPUS + ULTRATHINK. See CLAUDE.md model selection rules.
    Read tests/pre_filter/test_intent_classifier.py first — tests are the spec.
    """
    raise NotImplementedError("intent_classifier.build_qualified_trade")
