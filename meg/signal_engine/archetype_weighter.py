"""
Archetype weighter.

Applies a multiplier to a whale's signal based on their archetype.
INFORMATION whales (genuine edge) get a full multiplier (1.0).
MOMENTUM whales (trend followers) get a reduced multiplier — their trades
are less predictive and more likely to already be priced in.
ARBITRAGE and MANIPULATOR whales should never reach this module (excluded
at Gate 2). A warning is logged and 0.0 is returned as defense-in-depth.

Multipliers are config-driven (config.signal.archetype_weights) and
hot-reloadable. No restart required to adjust weights.
"""
from __future__ import annotations

from typing import Literal

import structlog

from meg.core.config_loader import MegConfig

logger = structlog.get_logger(__name__)

Archetype = Literal["INFORMATION", "MOMENTUM", "ARBITRAGE", "MANIPULATOR"]


def weight(archetype: Archetype, config: MegConfig) -> float:
    """
    Return the weight multiplier for the given archetype.

    Reads live values from config.signal.archetype_weights (hot-reloadable).
    Returns 0.0 for ARBITRAGE and MANIPULATOR — logs a WARNING because these
    archetypes should have been excluded at Gate 2 before reaching this module.
    Unknown archetypes default to 0.0 (safe — do not amplify unknown signals).
    """
    w = config.signal.archetype_weights
    multipliers: dict[str, float] = {
        "INFORMATION": w.INFORMATION,
        "MOMENTUM": w.MOMENTUM,
        "ARBITRAGE": w.ARBITRAGE,
        "MANIPULATOR": w.MANIPULATOR,
    }

    multiplier = multipliers.get(archetype, 0.0)

    if archetype in ("ARBITRAGE", "MANIPULATOR"):
        logger.warning(
            "archetype_weighter.excluded_archetype_reached",
            archetype=archetype,
            multiplier=multiplier,
            note="defense-in-depth: archetype should have been excluded at Gate 2",
        )

    return multiplier
