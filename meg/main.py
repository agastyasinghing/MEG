"""
MEG bot entry point — starts all concurrent pipeline tasks.

Pipeline tasks (run concurrently in a single asyncio.TaskGroup):
  polygon_feed        — Polygon RPC block watcher → raw_whale_trades
  pre_filter_pipeline — raw_whale_trades → qualified_whale_trades
  signal_aggregator   — qualified_whale_trades → decision_agent
  position_monitor    — TP/SL/whale exit monitor loop (every 30s)
  telegram_bot        — approval flow, alerts, /pause /resume /reject

If any task raises an unhandled exception the TaskGroup cancels all remaining
tasks and the process exits non-zero — Docker restart: unless-stopped handles
the relaunch.

Shutdown: SIGTERM / SIGINT cancels the TaskGroup cleanly; all resources are
closed in the finally block before the process exits.
"""
from __future__ import annotations

import asyncio
import os
import signal
import sys
from pathlib import Path

import structlog

from meg.agent_core import position_manager, signal_aggregator
from meg.core.config_loader import ConfigLoader
from meg.core.logger import setup_logging
from meg.core.redis_client import close as close_redis
from meg.core.redis_client import create_redis_client
from meg.data_layer import polygon_feed
from meg.db.session import close_db, init_db
from meg.pre_filter import pipeline as pre_filter_pipeline
from meg.telegram import bot as telegram_bot

_CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.yaml"

logger = structlog.get_logger(__name__)


async def _main() -> None:
    # ── Logging ───────────────────────────────────────────────────────────────
    setup_logging(level=os.environ.get("LOG_LEVEL", "INFO"))
    logger.info("main.starting", version=_read_version())

    # ── Signal handlers (cancel this task on SIGTERM / SIGINT) ────────────────
    loop = asyncio.get_running_loop()
    current = asyncio.current_task()

    def _on_signal(sig_num: int) -> None:
        logger.info("main.signal_received", signal=sig_num)
        if current and not current.done():
            current.cancel("shutdown")

    try:
        loop.add_signal_handler(signal.SIGTERM, _on_signal, signal.SIGTERM)
        loop.add_signal_handler(signal.SIGINT, _on_signal, signal.SIGINT)
    except NotImplementedError:
        # Windows: asyncio signal handlers unsupported; KeyboardInterrupt
        # propagates naturally on Ctrl-C in local dev.
        pass

    # ── Environment ───────────────────────────────────────────────────────────
    database_url = _require_env("DATABASE_URL")
    redis_url = _require_env("REDIS_URL")
    rpc_url = _require_env("POLYGON_RPC_URL")

    # ── Config ────────────────────────────────────────────────────────────────
    loader = ConfigLoader()
    await loader.start(_CONFIG_PATH)
    config = loader.get()
    logger.info("main.config_loaded", path=str(_CONFIG_PATH))

    # ── Database ──────────────────────────────────────────────────────────────
    await init_db(database_url)
    logger.info("main.db_initialized")

    # ── Redis ─────────────────────────────────────────────────────────────────
    redis = await create_redis_client(redis_url)
    logger.info("main.redis_connected")

    # ── Pipeline tasks ────────────────────────────────────────────────────────
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(
                polygon_feed.run(rpc_url, redis, config),
                name="polygon_feed",
            )
            tg.create_task(
                pre_filter_pipeline.run(redis, config),
                name="pre_filter_pipeline",
            )
            tg.create_task(
                signal_aggregator.run(redis, config),
                name="signal_aggregator",
            )
            tg.create_task(
                position_manager.monitor_positions(redis, config),
                name="position_monitor",
            )
            tg.create_task(
                telegram_bot.start(redis, config),
                name="telegram_bot",
            )
    except* Exception as exc_group:
        for exc in exc_group.exceptions:
            logger.error("main.task_failed", error=str(exc), exc_info=exc)
        raise
    finally:
        logger.info("main.shutdown_complete")
        logger.info("main.cleanup_starting")
        await close_redis(redis)
        await close_db()
        await loader.stop()
        logger.info("main.cleanup_complete")


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        sys.exit(f"Fatal: {name} environment variable is required but not set.")
    return value


def _read_version() -> str:
    try:
        return (Path(__file__).parent.parent / "VERSION").read_text().strip()
    except OSError:
        return "unknown"


def main() -> None:
    try:
        asyncio.run(_main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass


if __name__ == "__main__":
    main()
