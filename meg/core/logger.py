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

Processor chain (JSON output):
    merge_contextvars → filter_by_level → add_logger_name → add_log_level
    → PositionalArgumentsFormatter → TimeStamper(iso)
    → StackInfoRenderer → format_exc_info → UnicodeDecoder → JSONRenderer

Note: existing modules use structlog.get_logger(__name__) directly and bypass
this wrapper — both call patterns produce identical loggers once setup_logging()
has been called. The wrapper is provided for consistency in new modules.
"""
from __future__ import annotations

import logging
import sys

import structlog


def setup_logging(level: str = "INFO") -> None:
    """
    Configure structlog for JSON output. Call exactly once at process startup.

    Sets up Python stdlib logging as the backend (provides level filtering and
    stream routing) and configures structlog's processor chain on top.

    The level parameter maps to Python's stdlib logging level names:
    DEBUG / INFO / WARNING / ERROR / CRITICAL.
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Configure stdlib logging — structlog delegates level filtering and output here.
    # force=True clears any previously installed handlers (e.g. from pytest capture).
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
        force=True,
    )

    structlog.configure(
        processors=[
            # Merge any context variables bound via structlog.contextvars.bind_contextvars()
            structlog.contextvars.merge_contextvars,
            # Respect stdlib log level — drops events below the configured level
            structlog.stdlib.filter_by_level,
            # Add "logger" field (module __name__)
            structlog.stdlib.add_logger_name,
            # Add "level" field (debug / info / warning / error / critical)
            structlog.stdlib.add_log_level,
            # Handle positional format-string arguments (e.g. log.info("msg %s", val))
            structlog.stdlib.PositionalArgumentsFormatter(),
            # Add "timestamp" in ISO-8601 format
            structlog.processors.TimeStamper(fmt="iso"),
            # Render stack_info when passed via stack_info=True
            structlog.processors.StackInfoRenderer(),
            # Render exc_info when passed via exc_info=True or exception= kwarg
            structlog.processors.format_exc_info,
            # Decode any bytes values to str
            structlog.processors.UnicodeDecoder(),
            # Final renderer: emit as JSON for log aggregators
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        # Cache the logger wrapper after first use — safe because the processor
        # chain never changes after setup_logging() is called.
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Return a bound structlog logger for the given module name.
    Convention: always call as get_logger(__name__) at module level.

        log = get_logger(__name__)

    The returned logger is safe to call from async and sync code.
    Thin alias for structlog.get_logger(name) — both produce identical loggers.
    """
    return structlog.get_logger(name)
