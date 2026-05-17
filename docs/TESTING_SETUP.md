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

## Troubleshooting

Repo-level pytest collection imports `fakeredis.aioredis` through `tests/conftest.py`. If pytest fails during collection with:

```text
ModuleNotFoundError: No module named 'fakeredis'
```

then the development dependencies were not installed successfully. Re-run:

```bash
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` already includes `fakeredis`, so do not change dependency versions unless a future incompatibility is proven. This collection failure can occur before the targeted test body runs, which makes it an environment/setup issue rather than necessarily a failure in `tests/core/test_canonical_id_contract.py`.
