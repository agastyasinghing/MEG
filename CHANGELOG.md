# Changelog

All notable changes to MEG (Megalodon) are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.0.0] - 2026-03-13

### Added
- Full repo scaffold: `meg/` Python package at root with `pip install -e .` via `pyproject.toml`
- `meg/core/` shared kernel: `events.py` (full Pydantic schemas for `RawWhaleTrade`,
  `QualifiedWhaleTrade`, `SignalEvent`, `TradeProposal`, and `RedisKeys` constants),
  `config_loader.py` (hot-reloadable YAML config via watchdog + `MegConfig` Pydantic model),
  `redis_client.py` (injected async factory, no global state), `logger.py` (structlog JSON)
- Complete stub tree for all 5 layers: `meg/data_layer/`, `meg/pre_filter/`,
  `meg/signal_engine/`, `meg/agent_core/`, `meg/execution/` — typed signatures +
  `raise NotImplementedError` throughout; no bare `pass`
- `meg/db/` inside the package for consistent import paths (`from meg.db.models import ...`)
- `meg/telegram/bot.py` and `meg/dashboard/` stubs
- `docker-compose.yml` with profiles: `infra` (Postgres + Redis), `bot`, `dashboard`, `all`
- `config/config.yaml`: full schema with all known parameters (whale qualification, signal,
  risk, Kelly, entry, pre-filter, signal decay, reputation, logging)
- `.env.example`: all required environment variables documented
- `requirements.txt` (exact pins) and `requirements-dev.txt` (dev/test deps, split)
- `.python-version` pinning Python 3.11 for pyenv/mise
- `tests/conftest.py` with `asyncio_mode=auto`, `mock_redis` (fakeredis), `test_config` stub
- `tests/` mirror structure with `__init__.py` markers in every layer directory
- `TODOS.md` seeded with deferred items (pip-audit in CI, P2)
- `.gitignore` expanded to cover `.env`, `__pycache__`, venvs, pytest cache, mypy, ruff
