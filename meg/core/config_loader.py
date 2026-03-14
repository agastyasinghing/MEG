"""
Hot-reloadable YAML configuration loader for MEG.

Uses watchdog to detect config.yaml writes. On change:
  1. Re-read the file
  2. Validate with MegConfig (Pydantic)
  3. Atomically swap _config under threading.Lock if valid
  4. On error: log warning, keep last-good config in memory

  config.yaml ──► FileSystemEventHandler ──► Pydantic validation
       │                  │                        │
    file write         detected                valid → Lock ──► swap _config
    detected         by watchdog              invalid → warn + keep last-good

Design constraints:
  - ConfigLoader.get() must be thread-safe: watchdog runs on a background OS
    thread. _config is swapped under threading.Lock; get() acquires the same
    lock. Lock contention is negligible — held for one reference assignment.
  - Race condition: config.yaml may be partially written when inotify fires.
    _load_and_validate() catches yaml.YAMLError and treats as transient.
  - Never call sys.exit() from _on_config_changed() — only on startup failure.
  - start() is async for signature compatibility; the sync work inside is fast
    (file I/O + thread start) and does not block the event loop meaningfully.

Thread-safety diagram:

  asyncio event loop (main thread)          watchdog observer (background thread)
  ────────────────────────────────          ──────────────────────────────────────
  ConfigLoader.get()                        _ConfigFileHandler.on_modified()
       │                                            │
  acquire threading.Lock ◄──────────── contends ──►acquire threading.Lock
       │                                            │
  read self._config                           self._config = new_config
       │                                            │
  release lock                                release lock
"""
from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

import structlog
import yaml
from pydantic import BaseModel, Field
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

logger = structlog.get_logger(__name__)


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
    # Minimum calendar days until market resolution. None-valued days_to_resolution
    # on MarketState skips this check (conservative — allows trade to proceed).
    min_days_to_resolution: int = 3
    # Gate 2: window for YES+NO same-market behavioral arb detection (hours).
    arb_detection_window_hours: int = 24
    # Gate 3: window for SIGNAL_LADDER same-direction trade detection (hours).
    ladder_window_hours: int = 6
    # Gate 3: minimum prior same-direction trades within ladder_window_hours
    # to classify a trade as SIGNAL_LADDER rather than SIGNAL.
    ladder_min_trades: int = 2
    # Gate 3: minimum trade size as a fraction of wallet total_capital_usdc
    # to qualify as a directional SIGNAL. Below this → REBALANCE.
    min_signal_size_pct: float = 0.02


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


# ── Watchdog event handler ─────────────────────────────────────────────────────


class _ConfigFileHandler(FileSystemEventHandler):
    """
    Watchdog handler that calls ConfigLoader._on_config_changed() when the
    tracked config file is modified. Filters all other filesystem events.
    """

    def __init__(self, loader: ConfigLoader, config_path: Path) -> None:
        super().__init__()
        self._loader = loader
        # Resolve once at construction so on_modified comparisons are cheap.
        self._resolved_path = config_path.resolve()

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        if Path(event.src_path).resolve() == self._resolved_path:
            self._loader._on_config_changed(self._resolved_path)


# ── Config loader ─────────────────────────────────────────────────────────────


class ConfigLoader:
    """
    Loads config/config.yaml and hot-reloads it on file change.

    Usage:
        loader = ConfigLoader()
        await loader.start("/path/to/config/config.yaml")
        cfg = loader.get()   # always returns the last-good MegConfig
        await loader.stop()

    Thread safety: get() acquires _lock before reading _config.
    _on_config_changed() acquires the same lock before swapping _config.
    Lock contention is negligible — held for a single reference assignment.
    """

    def __init__(self) -> None:
        self._config: MegConfig | None = None
        self._lock: threading.Lock = threading.Lock()
        self._observer: Observer | None = None

    async def start(self, config_path: str | Path) -> None:
        """
        Load config.yaml and start the watchdog observer for hot-reload.
        Raises FileNotFoundError, yaml.YAMLError, or pydantic.ValidationError
        on startup failure — all of which should be treated as fatal.
        """
        path = Path(config_path).resolve()

        # Initial load — raises on any failure (fatal at startup)
        initial_config = self._load_and_validate(path)

        with self._lock:
            self._config = initial_config

        # Start watchdog observer watching the config file's parent directory.
        # We watch the directory (not the file directly) because some editors
        # replace files atomically, which watchdog detects as directory events.
        handler = _ConfigFileHandler(self, path)
        self._observer = Observer()
        self._observer.schedule(handler, str(path.parent), recursive=False)
        self._observer.start()

        logger.info("config_loader.started", path=str(path))

    def get(self) -> MegConfig:
        """
        Return the current (last-good) MegConfig. Thread-safe.
        Never raises — if start() succeeded, this always returns a valid config.
        Raises RuntimeError if called before start().
        """
        with self._lock:
            if self._config is None:
                raise RuntimeError(
                    "ConfigLoader.get() called before start(). "
                    "Call await loader.start(path) first."
                )
            return self._config

    async def stop(self) -> None:
        """Stop the watchdog observer and clean up resources."""
        if self._observer is not None:
            self._observer.stop()
            self._observer.join()
            self._observer = None
        logger.info("config_loader.stopped")

    def _load_and_validate(self, path: Path) -> MegConfig:
        """
        Read YAML from path and return a validated MegConfig.
        Raises yaml.YAMLError on malformed YAML (e.g. partial writes).
        Raises pydantic.ValidationError on schema violations.
        Raises FileNotFoundError if path does not exist.
        Caller is responsible for handling all three.
        """
        with open(path) as f:
            raw: Any = yaml.safe_load(f)
        # safe_load returns None for an empty file — treat as empty config
        return MegConfig(**(raw or {}))

    def _on_config_changed(self, path: Path) -> None:
        """
        Called by watchdog on file-system change event (background thread).
        Attempts reload; on any error, logs a warning and keeps _config unchanged.
        Never raises — must not crash the watchdog observer thread.
        """
        try:
            new_config = self._load_and_validate(path)
            with self._lock:
                self._config = new_config
            logger.info("config_loader.hot_reloaded", path=str(path))
        except yaml.YAMLError as exc:
            # Transient — file may be mid-write. Keep last-good config.
            logger.warning(
                "config_loader.yaml_error_on_reload",
                path=str(path),
                error=str(exc),
                note="keeping last-good config",
            )
        except Exception as exc:
            logger.warning(
                "config_loader.reload_failed",
                path=str(path),
                error=str(exc),
                note="keeping last-good config",
            )
