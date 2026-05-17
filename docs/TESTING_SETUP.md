# Testing Setup

Use this minimal smoke check when creating future Codex or CI test branches. It verifies that the development dependency set installs and that pytest can collect and run the canonical identifier contract tests.

## Local smoke check

From the repository root, install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Then run the targeted pytest smoke check:

```bash
python -m pytest -q tests/core/test_canonical_id_contract.py
```

The targeted test file is intentionally narrow: it exercises the Phase 0A canonical identifier contract around `condition_id`, `token_id`, and `outcome` without requiring broader strategy or service infrastructure.

## CI no-fakeredis smoke target

The `Phase 0A no-fakeredis smoke` GitHub Actions workflow intentionally installs only `requirements.txt`, `pytest`, and `pytest-asyncio`; it does **not** install `requirements-dev.txt` because the development requirements include `fakeredis`. The job first asserts that `fakeredis` is absent, then runs the narrow core smoke group:

```bash
python -m pytest -q tests/core/test_mock_redis_fixture_skip.py
python -m pytest -q tests/core/test_event_schema_versioning.py
python -m pytest -q tests/core/test_canonical_id_normalization.py
python -m pytest -q tests/core/test_redis_key_contract.py
```

This target protects the lazy `mock_redis` fixture behavior: non-Redis core tests and Redis key-contract tests still run without `fakeredis`, while tests that request `mock_redis` skip cleanly instead of failing during collection.

## Troubleshooting

`tests/conftest.py` imports `fakeredis.aioredis` lazily inside the `mock_redis` fixture, so non-Redis tests can still collect and run if `fakeredis` is missing. Tests that request `mock_redis` are skipped with a fixture-level setup message until the development dependencies are installed. Re-run:

```bash
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` already includes `fakeredis`, so do not change dependency versions unless a future incompatibility is proven.
