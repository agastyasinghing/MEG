"""
Archetype weighter.

Applies a multiplier to a whale's signal based on their archetype.
INFORMATION whales (genuine edge) get a full multiplier.
MOMENTUM whales (trend followers) get a reduced multiplier — their trades
are less predictive and more likely to already be priced in.
ARBITRAGE whales should never reach this module (excluded at Gate 2).
"""
from __future__ import annotations

from typing import Literal

from meg.core.config_loader import MegConfig

Archetype = Literal["INFORMATION", "MOMENTUM", "ARBITRAGE", "MANIPULATOR"]

# Archetype multipliers — tune these values via config in future
ARCHETYPE_WEIGHTS: dict[Archetype, float] = {
    "INFORMATION": 1.0,
    "MOMENTUM": 0.6,
    "ARBITRAGE": 0.0,   # should never reach this module
    "MANIPULATOR": 0.0, # should never reach this module
}


def weight(archetype: Archetype, config: MegConfig) -> float:
    """
    Return the weight multiplier for the given archetype.
    Returns 0.0 for ARBITRAGE and MANIPULATOR (these should be excluded upstream).
    Logs a warning if ARBITRAGE or MANIPULATOR reaches this function.
    """
    raise NotImplementedError("archetype_weighter.weight")
