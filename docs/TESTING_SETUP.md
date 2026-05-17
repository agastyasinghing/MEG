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

## Phase 0A targeted test jobs

| Target | Workflow or command | Dependency boundary | Use when |
| --- | --- | --- | --- |
| No-fakeredis core smoke | `.github/workflows/phase0a-smoke.yml` (`Phase 0A no-fakeredis smoke`) | Runtime dependencies from `requirements.txt` plus pinned `pytest==8.1.0` and `pytest-asyncio==0.23.5`; intentionally does **not** install `requirements-dev.txt` or `fakeredis`. | Validating that Phase 0A core contracts collect and run in a runtime-only CI environment, and that Redis fixture users skip cleanly when `fakeredis` is absent. |
| Full local/dev path | `python -m pip install -r requirements-dev.txt` | Full development dependencies, including `fakeredis`, pytest plugins, formatters, type checks, and audit tooling. | Running Redis-backed fixture tests, dashboard/full local test passes, and checks that need the complete developer toolchain. |
| Future integration jobs | To be defined with the job | Explicit external service boundary, such as real Redis, Postgres, dashboard services, or other integration infrastructure. | Adding tests that intentionally depend on live services or service containers rather than in-memory fixtures. |

The current no-fakeredis smoke workflow first asserts that `fakeredis` is absent, then runs this narrow core smoke group:

```bash
python -m pytest -q tests/core/test_mock_redis_fixture_skip.py
python -m pytest -q tests/core/test_event_schema_versioning.py
python -m pytest -q tests/core/test_canonical_id_normalization.py
python -m pytest -q tests/core/test_redis_key_contract.py
```

This target protects the lazy `mock_redis` fixture behavior: non-Redis core tests and Redis key-contract tests still run without `fakeredis`, while tests that request `mock_redis` skip cleanly instead of failing during collection.

Future CI jobs should state their dependency boundary explicitly in the workflow or companion documentation before they are added:

- runtime-only dependencies plus pinned pytest tooling;
- full `requirements-dev.txt`; or
- external service/integration dependencies, if those jobs are introduced later.

## Troubleshooting

`tests/conftest.py` imports `fakeredis.aioredis` lazily inside the `mock_redis` fixture, so non-Redis tests can still collect and run if `fakeredis` is missing. Tests that request `mock_redis` are skipped with a fixture-level setup message until the development dependencies are installed. Re-run:

```bash
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` already includes `fakeredis`, so do not change dependency versions unless a future incompatibility is proven.
