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


class CompositeWeightsConfig(BaseModel):
    """
    Weights for the four scored inputs in the composite formula (PRD §9.3.9).

    base_score = lead_lag * lead_lag + consensus * consensus
               + kelly * kelly + divergence * divergence
    Must sum to 1.0. Hot-configurable so weights can be tuned from signal_outcomes data.
    """

    lead_lag: float = 0.35   # Primary: is this whale consistently early?
    consensus: float = 0.30  # Multi-whale independent agreement
    kelly: float = 0.20      # Kelly confidence (positive expected value)
    divergence: float = 0.15 # Contrarian vs order flow


class ArchetypeWeightsConfig(BaseModel):
    """
    Signal weight multipliers by whale archetype (PRD §9.3.7).

    Applied to the post-weights adjusted base score:
      adjusted = base_score * archetype_multiplier * ladder_multiplier

    ARBITRAGE and MANIPULATOR should never reach the signal engine (excluded at
    Gate 2). Their weights are 0.0 as a defense-in-depth backstop.
    """

    INFORMATION: float = 1.0   # Full weight — genuine information edge
    MOMENTUM: float = 0.65     # Discounted — trend follower, likely priced in
    ARBITRAGE: float = 0.0     # Should be excluded at Gate 2; 0.0 as backstop
    MANIPULATOR: float = 0.0   # Should be excluded at Gate 2; 0.0 as backstop


class SignalConfig(BaseModel):
    composite_score_threshold: float = 0.45
    ttl_seconds: int = 7200
    min_whales_for_consensus: int = 2
    # Composite scoring weights (PRD §9.3.9). Hot-tunable from signal_outcomes data.
    composite_weights: CompositeWeightsConfig = Field(
        default_factory=CompositeWeightsConfig
    )
    # Archetype multipliers (PRD §9.3.7). Fixes stub bug: MOMENTUM was 0.6, PRD is 0.65.
    archetype_weights: ArchetypeWeightsConfig = Field(
        default_factory=ArchetypeWeightsConfig
    )
    # Consensus window: how long to look back for other whale trades in the same direction.
    consensus_window_hours: float = 4.0       # PRD §9.3.4 default
    consensus_sensitivity: float = 1.5        # Sigmoid sensitivity parameter (PRD §9.3.4)
    # Ladder: conviction added per rung above the base (2 rungs = 1.0x, 3 = 1.15x, etc.)
    ladder_conviction_per_rung: float = 0.15  # PRD §9.3.6 default; max multiplier 2.0
    # Signal TTL = half_life * ttl_half_life_multiplier.
    # At 3x: edge is ~12% of original at expiry (exp(-3*ln2) = 0.125).
    ttl_half_life_multiplier: float = 3.0     # PRD §9.3.8 default
    # Floor on estimated half-life. No signal expires in less than this time.
    min_half_life_minutes: float = 5.0        # PRD §9.3.8 default
    # Lead-lag minimum gate: scores below this after reputation decay are dropped.
    # Signal is logged FILTERED; does not proceed to consensus/kelly scoring.
    lead_lag_min_gate: float = 0.40           # PRD §9.3.1
    # Contrarian threshold: divergence_score above this → is_contrarian = True on SignalEvent.
    contrarian_threshold: float = 0.55        # PRD §9.3.5


class RiskConfig(BaseModel):
    max_position_pct: float = 0.05
    max_daily_loss_usdc: float = 500.0       # Circuit breaker: halt if daily loss hits this
    max_open_positions: int = 10
    max_market_exposure_pct: float = 0.20    # Gate 4: max fraction of portfolio in one market
    max_portfolio_exposure_pct: float = 0.60 # Gate 3: max fraction of portfolio deployed total
    paper_trading: bool = True
    blacklisted_markets: list[str] = Field(default_factory=list)  # Never trade these market IDs
    # system_paused is NOT here — it lives in Redis (RedisKeys.system_paused()).
    # Telegram /pause writes Redis; decision_agent reads Redis. Config hot-reload
    # latency (~1s) is unacceptable for an emergency stop.


class AgentConfig(BaseModel):
    """
    Agent core behavioral parameters (PRD §9.4).

    saturation_threshold: score above which position size is reduced (PRD §9.4.3).
    saturation_size_reduction_sensitivity: rate at which size shrinks past threshold.
      size_multiplier = clamp(1 - (score - threshold) * sensitivity, 0.25, 1.0)
    trap_window_minutes: lookback window to detect rapid whale entry/exit (PRD §9.4.2).
    trap_exit_threshold: fraction of entry size that must be sold to flag as trap.
    trap_score_penalty: score penalty applied to wallet when trap is detected.
    trap_manipulator_threshold: trap event count before wallet is flagged MANIPULATOR.
    """

    saturation_threshold: float = 0.60
    saturation_size_reduction_sensitivity: float = 2.0  # default: halve size at score=1.0
    trap_window_minutes: int = 30
    trap_exit_threshold: float = 0.50   # ≥50% of entry sold within window = trap
    trap_score_penalty: float = 0.20    # deducted from wallet score on trap detection
    trap_manipulator_threshold: int = 3  # flag MANIPULATOR after this many trap events
    crowding_max_entry_distance_pct: float = 0.08  # max price drift from whale fill before crowding blocks


class PositionConfig(BaseModel):
    """
    Position lifecycle risk parameters (PRD §10 position-level risk).

    In v1, auto_exit_stop_loss and auto_exit_take_profit are False — all exits
    require operator approval via Telegram. The flags are wired in position_manager
    so they can be set True in v2 without code changes.
    """

    take_profit_pct: float = 0.40        # Flag for exit at +40% gain on entry price
    stop_loss_pct: float = 0.25          # Flag for exit at -25% loss on entry price
    trailing_tp_enabled: bool = False    # Trail TP upward during drift continuation
    trailing_tp_floor_pct: float = 0.10  # Lock in new floor 10% below current price
    auto_exit_stop_loss: bool = False    # v1: requires human approval; v2: auto
    auto_exit_take_profit: bool = False  # v1: requires human approval; v2: auto


class KellyConfig(BaseModel):
    fraction: float = 0.25
    max_bet_usdc: float = 1000.0
    # Paper-trading portfolio value used by kelly_sizer for position sizing.
    # agent_core Position Manager recalibrates with real capital before execution.
    # Set this to the paper trading starting balance.
    portfolio_value_usdc: float = 1000.0


class EntryConfig(BaseModel):
    max_entry_distance_pct: float = 0.05
    max_spread_pct: float = 0.03


class PreFilterConfig(BaseModel):
    min_volume_24h_usdc: float = 50_000.0     # Gate 1: min 24h trading volume (PRD §9.1 mq_min_volume_24h)
    min_market_liquidity_usdc: float = 10_000.0  # Gate 1: min liquidity depth within 5 ticks (PRD §9.1 mq_min_liquidity)
    max_spread_pct: float = 0.06              # Gate 1: max bid-ask spread (PRD §9.1 mq_max_spread default)
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
    # Exponential decay time constant for reputation decay formula (PRD §9.3.1):
    #   decay_factor = exp(-days_since_last_good_trade / decay_tau_days)
    # Effect: 0 days → 1.00 (full), 30 days → 0.37, 60 days → 0.14, 90 days → 0.05
    decay_tau_days: float = 30.0


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
    agent: AgentConfig = Field(default_factory=AgentConfig)
    position: PositionConfig = Field(default_factory=PositionConfig)
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
