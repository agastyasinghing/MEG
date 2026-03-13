"""
Structured JSON logging setup for MEG using structlog.

Call setup_logging() exactly once at process startup, before any module
calls get_logger(). Each module gets its own logger via get_logger(__name__).
Bind per-event context fields with log.bind() — do not pass context as kwargs
to every log call.

Usage:
    # In your main entrypoint:
    from meg.core.logger import setup_logging
    setup_logging(level="INFO")

    # In every module:
    from meg.core.logger import get_logger
    log = get_logger(__name__)

    # Logging events:
    log.info("whale_trade_received", wallet=addr, size_usdc=size, market_id=mid)
    log.warning("config_reload_failed", error=str(e), fallback="last_good_config")
    log.error("redis_connection_failed", url=url, attempt=n, max_attempts=3)

    # Binding context for a request/event scope:
    bound = log.bind(market_id=market_id, signal_id=signal_id)
    bound.info("signal_scored", score=0.72)
    bound.info("signal_published")
"""
from __future__ import annotations

import structlog


def setup_logging(level: str = "INFO") -> None:
    """
    Configure structlog for JSON output. Call exactly once at process startup.
    Sets up the processor chain:
      - Add log level, timestamp, caller info
      - Render as JSON for log aggregators
    The level parameter maps to Python's stdlib logging level names.
    """
    raise NotImplementedError("logger.setup_logging")


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Return a bound structlog logger for the given module name.
    Convention: always call as get_logger(__name__) at module level.

        log = get_logger(__name__)

    The returned logger is safe to call from async and sync code.
    """
    raise NotImplementedError("logger.get_logger")
