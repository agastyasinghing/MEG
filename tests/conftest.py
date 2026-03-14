"""
Shared pytest fixtures for MEG.

asyncio_mode = "auto" is set in pyproject.toml — all async test functions
and fixtures run automatically without @pytest.mark.asyncio decorators.

Fixtures defined here:
  mock_redis    — fakeredis async client; zero real network calls
  test_config   — in-memory MegConfig with safe test defaults

Add layer-specific fixtures in tests/<layer>/conftest.py, not here.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import fakeredis.aioredis
from redis.asyncio import Redis

from meg.core.config_loader import MegConfig


@pytest.fixture
async def mock_redis() -> Redis:
    """
    Return a fakeredis async client for unit tests.
    Backed by an in-memory store — no real Redis required.
    Supports pub/sub, key-value ops, and TTLs.
    """
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    yield client
    await client.aclose()


@pytest.fixture
def test_config() -> MegConfig:
    """
    Return a MegConfig with safe defaults for unit tests.
    Uses Pydantic defaults — all thresholds are production values.
    Override individual fields in tests as needed:
        def test_something(test_config):
            test_config.risk.paper_trading = True
    """
    return MegConfig()
