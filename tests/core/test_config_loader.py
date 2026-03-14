"""
Tests for meg/core/config_loader.py.

Test categories:
  1. _load_and_validate — file parsing and Pydantic validation
  2. start() — initial load, observer startup, fatal error paths
  3. get() — thread-safe reads, before-start guard
  4. _on_config_changed() — hot-reload: valid swap, invalid YAML keep-last-good
  5. stop() — observer teardown
  6. Concurrency — get() is safe during a concurrent _on_config_changed() swap

All tests use tmp_path (pytest built-in) to write real YAML files — no mocking
of file I/O. This ensures the watchdog path exercises real filesystem semantics.
The concurrency test uses threading.Thread to simulate the watchdog background
thread racing against a main-thread get() call.
"""
from __future__ import annotations

import asyncio
import threading
import time
from pathlib import Path

import pytest
import yaml

from meg.core.config_loader import ConfigLoader, MegConfig


# ── Helpers ────────────────────────────────────────────────────────────────────


def _write_yaml(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        yaml.safe_dump(data, f)


MINIMAL_VALID_CONFIG = {
    "whale_qualification": {"min_win_rate": 0.60},
    "risk": {"max_daily_loss_usdc": 300.0},
}


# ── 1. _load_and_validate ──────────────────────────────────────────────────────


def test_load_and_validate_parses_valid_yaml(tmp_path: Path) -> None:
    """Valid YAML with partial overrides returns a MegConfig with correct values."""
    cfg_path = tmp_path / "config.yaml"
    _write_yaml(cfg_path, MINIMAL_VALID_CONFIG)

    loader = ConfigLoader()
    config = loader._load_and_validate(cfg_path)

    assert isinstance(config, MegConfig)
    assert config.whale_qualification.min_win_rate == 0.60
    assert config.risk.max_daily_loss_usdc == 300.0
    # Unspecified fields use defaults
    assert config.signal.composite_score_threshold == 0.45


def test_load_and_validate_empty_file_uses_defaults(tmp_path: Path) -> None:
    """An empty config.yaml is valid — all fields default."""
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text("")

    loader = ConfigLoader()
    config = loader._load_and_validate(cfg_path)

    assert isinstance(config, MegConfig)
    assert config.whale_qualification.min_win_rate == 0.55  # default


def test_load_and_validate_missing_file_raises(tmp_path: Path) -> None:
    """FileNotFoundError is raised for a non-existent path — fatal at startup."""
    loader = ConfigLoader()
    with pytest.raises(FileNotFoundError):
        loader._load_and_validate(tmp_path / "does_not_exist.yaml")


def test_load_and_validate_invalid_yaml_raises(tmp_path: Path) -> None:
    """Malformed YAML raises yaml.YAMLError — treated as transient on hot-reload."""
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text("whale_qualification: {\n  broken yaml")

    loader = ConfigLoader()
    with pytest.raises(yaml.YAMLError):
        loader._load_and_validate(cfg_path)


# ── 2. start() ─────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_start_loads_config_and_get_works(tmp_path: Path) -> None:
    """After start(), get() returns the loaded config."""
    cfg_path = tmp_path / "config.yaml"
    _write_yaml(cfg_path, MINIMAL_VALID_CONFIG)

    loader = ConfigLoader()
    await loader.start(cfg_path)
    try:
        config = loader.get()
        assert config.whale_qualification.min_win_rate == 0.60
    finally:
        await loader.stop()


@pytest.mark.asyncio
async def test_start_missing_file_raises_fatal(tmp_path: Path) -> None:
    """start() with a missing file raises FileNotFoundError — must not swallow it."""
    loader = ConfigLoader()
    with pytest.raises(FileNotFoundError):
        await loader.start(tmp_path / "missing.yaml")


@pytest.mark.asyncio
async def test_start_invalid_yaml_raises_fatal(tmp_path: Path) -> None:
    """start() with malformed YAML raises yaml.YAMLError — must not swallow it."""
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(": broken")

    loader = ConfigLoader()
    with pytest.raises(yaml.YAMLError):
        await loader.start(cfg_path)


# ── 3. get() ───────────────────────────────────────────────────────────────────


def test_get_before_start_raises() -> None:
    """get() before start() raises RuntimeError with a clear message."""
    loader = ConfigLoader()
    with pytest.raises(RuntimeError, match="called before start"):
        loader.get()


@pytest.mark.asyncio
async def test_get_returns_megconfig_instance(tmp_path: Path) -> None:
    """get() returns a MegConfig, not a raw dict."""
    cfg_path = tmp_path / "config.yaml"
    _write_yaml(cfg_path, {})

    loader = ConfigLoader()
    await loader.start(cfg_path)
    try:
        assert isinstance(loader.get(), MegConfig)
    finally:
        await loader.stop()


# ── 4. _on_config_changed() ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_on_config_changed_swaps_to_new_config(tmp_path: Path) -> None:
    """_on_config_changed() with valid YAML updates the config returned by get()."""
    cfg_path = tmp_path / "config.yaml"
    _write_yaml(cfg_path, {"risk": {"max_daily_loss_usdc": 100.0}})

    loader = ConfigLoader()
    await loader.start(cfg_path)
    try:
        assert loader.get().risk.max_daily_loss_usdc == 100.0

        # Simulate hot-reload: write new values and trigger manually
        _write_yaml(cfg_path, {"risk": {"max_daily_loss_usdc": 999.0}})
        loader._on_config_changed(cfg_path)

        assert loader.get().risk.max_daily_loss_usdc == 999.0
    finally:
        await loader.stop()


@pytest.mark.asyncio
async def test_on_config_changed_invalid_yaml_keeps_last_good(tmp_path: Path) -> None:
    """_on_config_changed() with bad YAML keeps the previous valid config."""
    cfg_path = tmp_path / "config.yaml"
    _write_yaml(cfg_path, {"risk": {"max_daily_loss_usdc": 100.0}})

    loader = ConfigLoader()
    await loader.start(cfg_path)
    try:
        original = loader.get()
        assert original.risk.max_daily_loss_usdc == 100.0

        # Overwrite with broken YAML (simulates editor mid-write)
        cfg_path.write_text("risk: {\n  broken")
        loader._on_config_changed(cfg_path)  # must not raise

        # Config unchanged
        assert loader.get().risk.max_daily_loss_usdc == 100.0
    finally:
        await loader.stop()


@pytest.mark.asyncio
async def test_on_config_changed_pydantic_error_keeps_last_good(tmp_path: Path) -> None:
    """_on_config_changed() with a schema violation keeps the previous config."""
    cfg_path = tmp_path / "config.yaml"
    _write_yaml(cfg_path, {"risk": {"max_daily_loss_usdc": 100.0}})

    loader = ConfigLoader()
    await loader.start(cfg_path)
    try:
        # Write a Pydantic-invalid config (wrong type for a numeric field)
        _write_yaml(cfg_path, {"risk": {"max_daily_loss_usdc": "not_a_number"}})
        loader._on_config_changed(cfg_path)  # must not raise

        assert loader.get().risk.max_daily_loss_usdc == 100.0
    finally:
        await loader.stop()


# ── 5. stop() ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_stop_is_idempotent(tmp_path: Path) -> None:
    """stop() can be called multiple times without raising."""
    cfg_path = tmp_path / "config.yaml"
    _write_yaml(cfg_path, {})

    loader = ConfigLoader()
    await loader.start(cfg_path)
    await loader.stop()
    await loader.stop()  # second call must not raise


# ── 6. Concurrency ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_concurrent_get_during_reload_never_raises(tmp_path: Path) -> None:
    """
    get() called concurrently with _on_config_changed() must never raise or
    return a partially-constructed config. This test exercises the threading.Lock
    that protects _config from race conditions between the watchdog background
    thread and the asyncio event loop.

    Strategy: launch a background thread that rapidly calls _on_config_changed()
    in a tight loop while the main thread calls get() 500 times. If the lock is
    missing or incorrect, this will intermittently raise AttributeError or return
    a None config under CPython's GIL — and will reliably fail under free-threaded
    Python or PyPy.
    """
    cfg_path = tmp_path / "config.yaml"
    _write_yaml(cfg_path, {"risk": {"max_daily_loss_usdc": 100.0}})

    loader = ConfigLoader()
    await loader.start(cfg_path)

    reload_errors: list[Exception] = []
    get_errors: list[Exception] = []
    stop_event = threading.Event()

    def reload_loop() -> None:
        """Simulate watchdog thread: rapid config reloads."""
        alt_configs = [
            {"risk": {"max_daily_loss_usdc": 100.0}},
            {"risk": {"max_daily_loss_usdc": 200.0}},
        ]
        i = 0
        while not stop_event.is_set():
            try:
                _write_yaml(cfg_path, alt_configs[i % 2])
                loader._on_config_changed(cfg_path)
                i += 1
            except Exception as exc:
                reload_errors.append(exc)

    thread = threading.Thread(target=reload_loop, daemon=True)
    thread.start()

    try:
        # Main thread: rapid get() calls while reload_loop races
        for _ in range(500):
            try:
                cfg = loader.get()
                assert isinstance(cfg, MegConfig), "get() returned non-MegConfig"
                # Config must have a valid numeric value (not partial state)
                assert cfg.risk.max_daily_loss_usdc in (100.0, 200.0)
            except Exception as exc:
                get_errors.append(exc)
    finally:
        stop_event.set()
        thread.join(timeout=5.0)
        await loader.stop()

    assert not get_errors, f"get() raised during concurrent reload: {get_errors}"
    assert not reload_errors, f"reload_loop raised: {reload_errors}"
