# Phase 0A-05H — TradeProposal boundary ownership and safety preflight

## 1) Status and objective

**Status:** Documentation-only preflight. No production runtime code, tests, workflows, or dependencies are changed in this ticket.

**Objective:** Inspect and map the TradeProposal boundary from SignalEvent routing through proposal publication, approval consumption, and execution-adjacent handoff points, then identify the safest next boundary action without changing runtime behavior.

## 2) Repository inspection commands used

The following commands were run for this preflight:

- `rg -n "TradeProposal|CHANNEL_TRADE_PROPOSALS" meg tests docs`
- `rg -n "decision_agent|evaluate\(" meg tests`
- `rg -n "approve_signal|approval|reject|telegram" meg tests`
- `rg -n "order_router|execute|execution|place_order|submit_order" meg tests`
- `rg -n "publish\(|subscribe\(|listen\(|get_message\(" meg tests`
- `rg -n "model_validate_json|model_validate\(" meg tests`

Plus focused reads of:

- `meg/core/events.py`
- `meg/agent_core/signal_aggregator.py`
- `meg/agent_core/decision_agent.py`
- `meg/dashboard/api/main.py`
- `meg/telegram/bot.py`
- `meg/execution/order_router.py`
- boundary validation tests in `tests/core/` and `tests/dashboard/test_api.py`

## 3) Direct boundary answers

1. **Where does SignalEvent become TradeProposal?**
   - In `meg/agent_core/decision_agent.py::evaluate(...)` after hard blocks + risk/trap/saturation/crowding checks pass, via `_build_proposal(...)` returning `TradeProposal`.

2. **Where is TradeProposal published?**
   - In `decision_agent.evaluate(...)` with `redis.publish(...)` after proposal creation.

3. **What Redis channel is used?**
   - `RedisKeys.CHANNEL_TRADE_PROPOSALS` (`trade_proposals`).

4. **Where is TradeProposal consumed for dashboard/approval?**
   - Dashboard/API approval flow parses pending proposal JSON as `TradeProposal` in `meg/dashboard/api/main.py::approve_signal(...)` before order-router call.
   - Telegram bot consumes `CHANNEL_TRADE_PROPOSALS` in `_subscriber_loop(...)`, validates as `TradeProposal`, and forwards for operator approval request.

5. **Where is Telegram approval involved?**
   - Telegram bot is the operator approval path: proposal notifications, approve/reject handling, pause/resume authority, and approved-proposal execution handoff.

6. **Where is order routing/execution involved?**
   - In dashboard approve and Telegram approve flows that call `order_router.place(...)` after proposal retrieval/validation.

7. **Which boundary is safest to inspect next?**
   - A docs/test-only TradeProposal envelope contract check (no runtime behavior edits), centered on Redis envelope + schema validation and ownership assertions.

8. **Which boundaries are too execution-adjacent to migrate now?**
   - Any boundary that modifies dashboard approve behavior, Telegram approval callbacks, order-router placement behavior, or approval-to-execution state transitions.

9. **What invariants must never be broken?**
   - No autonomous execution.
   - Operator approval required for execution.
   - No TradeProposal auto-approval path.
   - No order placement behavior changes in this phase ticket.
   - No DB migrations for this preflight ticket.
   - No risk sizing/scoring behavior changes.

## 4) Current proposal rail map

Current runtime/approval-adjacent proposal path:

1. `signal_aggregator` receives valid `SignalEvent` and routes to `decision_agent.evaluate(...)`.
2. `decision_agent.evaluate(...)` builds `TradeProposal` (`PENDING_APPROVAL`) when all gates pass.
3. `decision_agent.evaluate(...)` publishes proposal JSON to `CHANNEL_TRADE_PROPOSALS`.
4. Telegram bot subscriber loop consumes `CHANNEL_TRADE_PROPOSALS`, validates payload, sends operator approval request.
5. Approval actions (Telegram callback path and dashboard approve endpoint) retrieve/parse `TradeProposal` and call `order_router.place(...)` only after explicit approval action.

## 5) Candidate boundary table

| Candidate boundary | Current owner/function | Current channel/contract | Risk level | 0A-05H assessment |
|---|---|---|---|---|
| Decision-agent proposal publisher | `meg/agent_core/decision_agent.py::evaluate()` | Publishes `TradeProposal` to `RedisKeys.CHANNEL_TRADE_PROPOSALS` | High | Inspect only; do not migrate runtime behavior. |
| Dashboard approval parser | `meg/dashboard/api/main.py::approve_signal()` | Parses pending proposal as `TradeProposal`, then routes to order router | Very high | Too execution-adjacent for migration now. |
| Telegram approval path | `meg/telegram/bot.py` (`_subscriber_loop`, callback handlers, approved execution helper) | Proposal consumption + operator approval/reject + approved execution handoff | Very high | Too execution-adjacent for migration now. |
| Order router / execution path | `meg/execution/order_router.py::place(...)` | Execution gate + placement after approval | Very high | Defer runtime migration in Phase 0A docs-only preflight. |

## 6) Safety invariants (must hold)

The following invariants are mandatory for any follow-on ticket touching proposal boundaries:

1. **No autonomous execution authority** introduced.
2. **Operator approval remains required** before order placement.
3. **No TradeProposal auto-approval** path added.
4. **No order placement logic changes** (dashboard/telegram/order-router behavior unchanged).
5. **No DB schema/migration changes** in proposal-boundary preflight tickets.
6. **No risk sizing/scoring formula changes** in `decision_agent`/signal chain.

## 7) Recommended next ticket

Recommended next step:

- **0A-05I — TradeProposal envelope contract preflight (docs/test-only)**

Ticket intent:

- Keep runtime behavior unchanged.
- Add/extend test-only coverage that asserts `trade_proposals` envelope/schema ownership and fail-closed parsing behavior for dashboard/Telegram consumers.
- Explicitly avoid approval/execution behavior edits.

Alternative branch decision:

- If proposal-boundary work requires any approval/execution behavior change, **pause Phase 0A runtime-facing boundary migration** and move focus to **Phase 0B DuckDB planning**.

## 8) Kill criteria

Stop and defer runtime migration work immediately if any planned step requires:

1. Changes to approval decision semantics.
2. Changes to Telegram approve/reject execution behavior.
3. Changes to dashboard approve -> order-router behavior.
4. Changes to order placement/execution gating logic.
5. Any DB migration required solely to progress this boundary preflight.

If any kill criterion is triggered, close the preflight as documentation-only and route next effort to Phase 0B planning.

## 9) Documentation-only confirmation

This ticket is documentation-only and intentionally does not modify production source, tests, workflows, dependencies, or frozen PRD content.
