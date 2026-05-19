# Phase 0A-05E — Main Startup Wiring Preflight (Signal-Engine Runner)

## 1) Status and scope

**Status:** Documentation-first preflight with optional static contract test only.  
**Ticket type:** Phase 0A shared-rail startup wiring preflight.  
**Runtime impact:** None in this ticket.

This ticket prepares the future startup wiring of the signal-engine runner into `meg/main.py` without changing production startup behavior yet.

---

## 2) Current startup task graph in `meg/main.py`

Current `_main()` startup sequence:

1. Initialize logging.
2. Register shutdown signal handlers.
3. Require environment values (`DATABASE_URL`, `REDIS_URL`, `POLYGON_RPC_URL`).
4. Load config (`ConfigLoader`).
5. Initialize Postgres connectivity (`init_db`).
6. Create Redis client (`create_redis_client`).
7. Start TaskGroup workers:
   - `polygon_feed.run(...)` as task name `polygon_feed`
   - `pre_filter_pipeline.run(...)` as task name `pre_filter_pipeline`
   - `signal_aggregator.run(...)` as task name `signal_aggregator`
   - `position_manager.monitor_positions(...)` as task name `position_monitor`
   - `telegram_bot.start(...)` as task name `telegram_bot`

### Current signal_aggregator channel/route clarification

- `meg/main.py` starts `signal_aggregator` as a long-running task, but `meg/main.py` itself does not document the exact Redis channel consumed by that worker.
- Current runtime channel ownership is in `meg/agent_core/signal_aggregator.py`: `signal_aggregator` consumes `RedisKeys.CHANNEL_SIGNAL_EVENTS`.
- In that consumer path, valid `SignalEvent` payloads may route toward `decision_agent.evaluate(...)`.
- `qualified_whale_trades` should be consumed by the future `signal_engine_runner`, not by `signal_aggregator`.

### Current signal-engine status

- `meg.signal_engine.runner` is **currently absent** from `meg/main.py` startup task registration.
- Therefore, the dedicated signal-engine runner is not currently started by main.

### Known startup-wiring wording mismatch (deferred)

- There is stale/misleading architecture wording in `meg/main.py` module commentary about `signal_aggregator` flow.
- Per this ticket scope, that production-file wording is not edited here.
- The wording cleanup should be included in the future production startup-wiring implementation ticket.

---

## 3) Proposed future startup wiring (not implemented in this ticket)

Future wiring should add a signal-engine runner import and one TaskGroup registration.

### Proposed import

```python
from meg.signal_engine import runner as signal_engine_runner
```

### Proposed TaskGroup addition

```python
tg.create_task(signal_engine_runner.run(redis, config), name="signal_engine_runner")
```

This preserves channel ownership separation:
- runner: subscribe `qualified_whale_trades` -> `composite_scorer.score(...)` -> publish `signal_events`
- signal_aggregator: consume `signal_events` and route toward decision flow

---

## 4) Ordering expectations

1. Signal-engine runner startup should happen **after** Redis and config creation.
2. Runner should operate concurrently with existing long-running workers.
3. Runner can run alongside:
   - `pre_filter_pipeline`
   - `signal_aggregator`
4. No `decision_agent` startup or behavioral changes are required to wire the runner task.

---

## 5) Failure semantics preflight

Future wiring should preserve existing main worker semantics:

1. Worker failures remain fail-fast under `asyncio.TaskGroup`.
2. Redis disconnects from the runner should propagate like other long-running workers.
3. Do not add broad exception catches that hide worker death.
4. Existing `except* Exception` logging in main remains the common failure reporting path.

---

## 6) Required tests for future implementation ticket

Future production wiring ticket must include tests proving:

1. `meg.main` imports `meg.signal_engine.runner` (aliased as `signal_engine_runner`).
2. `meg.main` creates a TaskGroup task named `signal_engine_runner`.
3. Existing tasks still start (`polygon_feed`, `pre_filter_pipeline`, `signal_aggregator`, `position_monitor`, `telegram_bot`).
4. Runner is not started twice.
5. No behavior changes in decision-agent / execution / Telegram-approval semantics.

---

## 7) Non-goals

This ticket does **not**:

1. Add production startup wiring in `meg/main.py`.
2. Change strategy/scoring formulas or behavior.
3. Change order placement, approval handling, or execution flow.
4. Add or alter DB models/migrations.
5. Change workflows or dependencies.

---

## 8) Kill criteria

Stop and re-scope if either occurs:

1. Wiring requires changes to decision/execution/approval semantics.
2. Wiring requires a broader task lifecycle/supervisor refactor in main.

---

## 9) Implementation readiness summary

- A runner seam already exists in `meg/signal_engine/runner.py`.
- Main startup registration is the remaining explicit wiring step.
- This preflight keeps scope tight and preserves Phase 0A shared-rail boundaries.
