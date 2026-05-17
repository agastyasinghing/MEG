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


## Future full-dev CI proposal

TEST-04 proposes a separate full-dev CI job for Redis-backed fixture coverage, dashboard API coverage, full local fixture paths, and Phase 0A contract tests that require development-only dependencies. This proposal is documentation-only and does not change the existing no-fakeredis smoke workflow or any CI behavior.

The proposed dependency boundary is the complete developer environment:

```bash
python -m pip install -r requirements-dev.txt
```

That boundary intentionally includes `fakeredis` from `requirements-dev.txt` so tests that request the `mock_redis` fixture exercise the in-memory Redis path instead of taking the no-fakeredis skip path. The job should also include an explicit import check, such as `python -c "import fakeredis"`, before pytest runs so a dependency-resolution issue fails early.

Suggested initial command group for the future job:

```bash
python -m pip install -r requirements-dev.txt
python -c "import fakeredis"
python -m pytest -q tests/core
python -m pytest -q tests/dashboard/test_api.py
```

Broader layer tests should be added only after this initial group has measured runtime in CI. The expected runtime and cost should remain low enough for normal PR gating because the initial target uses in-memory fixtures and focused core/dashboard tests rather than external service containers. If measured runtime becomes too high for routine pull requests, the job should be made non-blocking, scheduled, or manually triggered before it is broadened.

Acceptance criteria for adding the future full-dev CI job:

- `requirements-dev.txt` installs successfully.
- `fakeredis` imports successfully before pytest runs.
- Redis fixture tests, dashboard API tests, full local fixture tests, and Phase 0A contract tests that need dev dependencies collect and run without collection errors.
- The job fails on real test failures.
- Redis fixture tests are not silently skipped when `fakeredis` should be installed.
- Runtime stays low enough for PR gating, or the job is explicitly marked non-blocking/manual if runtime is too high.

Non-goals for TEST-04:

- Do not add the full-dev CI workflow in this ticket.
- Do not change `.github/workflows/phase0a-smoke.yml`.
- Do not change `requirements.txt` or `requirements-dev.txt`.
- Do not change pytest fixtures.
- Do not broaden the existing no-fakeredis smoke job.

## Troubleshooting

`tests/conftest.py` imports `fakeredis.aioredis` lazily inside the `mock_redis` fixture, so non-Redis tests can still collect and run if `fakeredis` is missing. Tests that request `mock_redis` are skipped with a fixture-level setup message until the development dependencies are installed. Re-run:

```bash
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` already includes `fakeredis`, so do not change dependency versions unless a future incompatibility is proven.
