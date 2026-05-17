"""Regression tests for lazy fakeredis loading in the mock_redis fixture."""
from __future__ import annotations

import asyncio
import builtins
import importlib.machinery
import importlib.util
import sys
from types import ModuleType
from typing import Any

import pytest

import tests.conftest as shared_conftest


def test_fakeredis_aioredis_is_not_loaded_at_collection_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Importing tests.conftest must not import the optional fakeredis backend."""
    real_import = builtins.__import__

    def fail_on_fakeredis_import(
        name: str,
        globals: dict[str, object] | None = None,
        locals: dict[str, object] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> object:
        if name == "fakeredis" or name.startswith("fakeredis."):
            raise AssertionError(f"unexpected import at collection time: {name}")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fail_on_fakeredis_import)

    spec = importlib.util.spec_from_file_location(
        "mock_redis_lazy_import_regression_conftest",
        shared_conftest.__file__,
    )
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def test_missing_fakeredis_skips_with_clear_fixture_message(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A missing optional fakeredis package should skip instead of raising on import."""

    def fake_find_spec(name: str) -> object | None:
        if name == "fakeredis":
            return None
        return importlib.machinery.ModuleSpec(name, loader=None)

    monkeypatch.setattr(shared_conftest.importlib.util, "find_spec", fake_find_spec)

    with pytest.raises(pytest.skip.Exception) as skip_info:
        shared_conftest._load_fakeredis_aioredis_or_skip()

    assert "fakeredis" in str(skip_info.value)
    assert "requirements-dev.txt" in str(skip_info.value)
    assert "fakeredis.aioredis" not in sys.modules


def test_fakeredis_aioredis_loads_only_after_availability_check(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When fakeredis is available, the helper imports and returns fakeredis.aioredis."""
    parent_module = ModuleType("fakeredis")
    parent_module.__path__ = []  # mark as a package for fakeredis.aioredis imports
    aioredis_module = ModuleType("fakeredis.aioredis")

    class FakeRedis:
        pass

    aioredis_module.FakeRedis = FakeRedis  # type: ignore[attr-defined]

    def fake_find_spec(name: str) -> object | None:
        if name == "fakeredis":
            return importlib.machinery.ModuleSpec(name, loader=None)
        return None

    monkeypatch.setattr(shared_conftest.importlib.util, "find_spec", fake_find_spec)
    monkeypatch.setitem(sys.modules, "fakeredis", parent_module)
    monkeypatch.setitem(sys.modules, "fakeredis.aioredis", aioredis_module)

    assert shared_conftest._load_fakeredis_aioredis_or_skip() is aioredis_module


def test_mock_redis_fixture_uses_fake_redis_with_decoded_responses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The fixture should keep constructing FakeRedis(decode_responses=True)."""
    fake_clients: list[FakeRedis] = []

    class FakeRedis:
        def __init__(self, **kwargs: Any) -> None:
            self.kwargs = kwargs
            self.closed = False
            fake_clients.append(self)

        async def aclose(self) -> None:
            self.closed = True

    fake_aioredis_module = ModuleType("fakeredis.aioredis")
    fake_aioredis_module.FakeRedis = FakeRedis  # type: ignore[attr-defined]

    monkeypatch.setattr(
        shared_conftest,
        "_load_fakeredis_aioredis_or_skip",
        lambda: fake_aioredis_module,
    )

    async def exercise_fixture() -> FakeRedis:
        fixture_generator = shared_conftest.mock_redis.__wrapped__()
        client = await anext(fixture_generator)

        assert client is fake_clients[0]
        assert client.kwargs == {"decode_responses": True}

        with pytest.raises(StopAsyncIteration):
            await anext(fixture_generator)

        return client

    client = asyncio.run(exercise_fixture())

    assert client.closed is True
