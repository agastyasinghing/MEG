"""
Hot-reloadable YAML configuration loader for MEG.

Uses watchdog to detect config.yaml writes. On change:
  1. Re-read the file
  2. Validate with MegConfig (Pydantic)
  3. Atomically swap _config if valid
  4. On error: log warning, keep last-good config in memory

  config.yaml ──► FileSystemEventHandler ──► Pydantic validation
       │                  │                        │
    file write         detected                valid → swap _config
    detected         by watchdog              invalid → warn + keep last-good

Design constraints:
  - ConfigLoader.get() must be thread-safe (watchdog runs on a background thread)
  - Race condition: config.yaml may be partially written when inotify fires.
    _load_and_validate() must catch yaml.YAMLError and treat as transient.
  - Never call sys.exit() from _on_config_changed() — only on startup failure.
"""
from __future__ import annotations

import threading  # noqa: F401 — used in implementation for _lock
from pathlib import Path

import yaml  # noqa: F401 — used in implementation for yaml.safe_load / yaml.YAMLError
from pydantic import BaseModel, Field
from watchdog.events import FileSystemEventHandler  # noqa: F401 — used in implementation
from watchdog.observers import Observer  # noqa: F401 — used in implementation


# ── Config sub-models ─────────────────────────────────────────────────────────


class WhaleQualificationConfig(BaseModel):
    min_win_rate: float = 0.55
    min_closed_positions: int = 50
    min_total_volume_usdc: float = 100_000.0
    min_profitable_months: int = 3
    exclude_archetypes: list[str] = Field(default_factory=lambda: ["ARBITRAGE", "MANIPULATOR"])


class SignalConfig(BaseModel):
    composite_score_threshold: float = 0.45
    ttl_seconds: int = 7200
    min_whales_for_consensus: int = 2


class RiskConfig(BaseModel):
    max_position_pct: float = 0.05
    max_daily_loss_usdc: float = 500.0
    max_open_positions: int = 10
    max_market_exposure_pct: float = 0.20
    paper_trading: bool = True


class KellyConfig(BaseModel):
    fraction: float = 0.25
    max_bet_usdc: float = 1000.0


class EntryConfig(BaseModel):
    max_entry_distance_pct: float = 0.05
    max_spread_pct: float = 0.03


class PreFilterConfig(BaseModel):
    min_market_liquidity_usdc: float = 50_000.0
    max_spread_pct: float = 0.05
    min_unique_participants: int = 20


class SignalDecayConfig(BaseModel):
    half_life_seconds: int = 3600
    min_score_after_decay: float = 0.20


class ReputationConfig(BaseModel):
    decay_on_loss: float = 0.05
    boost_on_win: float = 0.03
    min_score: float = 0.10
    max_score: float = 1.00


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0


class PostgresConfig(BaseModel):
    pool_size: int = 10


class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "json"


class MegConfig(BaseModel):
    """Root configuration model. Validated on every hot-reload."""

    whale_qualification: WhaleQualificationConfig = Field(
        default_factory=WhaleQualificationConfig
    )
    signal: SignalConfig = Field(default_factory=SignalConfig)
    risk: RiskConfig = Field(default_factory=RiskConfig)
    kelly: KellyConfig = Field(default_factory=KellyConfig)
    entry: EntryConfig = Field(default_factory=EntryConfig)
    pre_filter: PreFilterConfig = Field(default_factory=PreFilterConfig)
    signal_decay: SignalDecayConfig = Field(default_factory=SignalDecayConfig)
    reputation: ReputationConfig = Field(default_factory=ReputationConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


# ── Config loader ─────────────────────────────────────────────────────────────


class ConfigLoader:
    """
    Loads config/config.yaml and hot-reloads it on file change.

    Usage:
        loader = ConfigLoader()
        await loader.start("/path/to/config/config.yaml")
        cfg = loader.get()   # always returns the last-good MegConfig
        await loader.stop()

    Thread safety: get() is safe to call from any thread or asyncio task.
    The internal _lock protects _config from concurrent reads during a swap.
    """

    def __init__(self) -> None:
        raise NotImplementedError("ConfigLoader.__init__")

    async def start(self, config_path: str | Path) -> None:
        """
        Load config.yaml and start the watchdog observer for hot-reload.
        Raises FileNotFoundError, yaml.YAMLError, or pydantic.ValidationError
        on startup failure — all of which should be treated as fatal.
        """
        raise NotImplementedError("ConfigLoader.start")

    def get(self) -> MegConfig:
        """
        Return the current (last-good) MegConfig. Thread-safe.
        Never raises — if start() succeeded, this always returns a valid config.
        """
        raise NotImplementedError("ConfigLoader.get")

    async def stop(self) -> None:
        """Stop the watchdog observer and clean up resources."""
        raise NotImplementedError("ConfigLoader.stop")

    def _load_and_validate(self, path: Path) -> MegConfig:
        """
        Read YAML from path and return a validated MegConfig.
        Raises yaml.YAMLError on malformed YAML (e.g. partial writes).
        Raises pydantic.ValidationError on schema violations.
        Caller is responsible for handling both.
        """
        raise NotImplementedError("ConfigLoader._load_and_validate")

    def _on_config_changed(self, path: Path) -> None:
        """
        Called by watchdog on file-system change event.
        Attempts reload; on any error, logs a warning and keeps _config unchanged.
        Never raises — must not crash the watchdog observer thread.
        """
        raise NotImplementedError("ConfigLoader._on_config_changed")
