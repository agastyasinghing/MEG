# Phase 0A-04G Dashboard Signal Feed Post-Migration Audit

Status: documentation-only post-migration audit for Phase 0A-04F. This note records the read-only dashboard signal feed boundary migration results and confirms what remained intentionally unchanged.

## 1) Migration summary

### Selected boundary

- File/function seam: `meg/dashboard/api/main.py::feed_signals()`.
- Helper/path at boundary: `_normalize_signal_feed_data(...)` before SSE forwarding.
- Channel/model boundary: `RedisKeys.CHANNEL_SIGNAL_EVENTS` carrying `SignalEvent`-shaped shared-event payloads for the dashboard SSE feed.

### Behavior before 0A-04F

- Dashboard SSE feed subscribed to `CHANNEL_SIGNAL_EVENTS` and forwarded data to clients.
- Feed path had to remain tolerant of mixed/legacy payloads during shared-event compatibility window.
- Canonical identifiers (`condition_id`, `token_id`, `market_slug`) were optional at this boundary.

### Behavior after 0A-04F

- Dashboard SSE feed remains a read-only consumer/forwarder of `CHANNEL_SIGNAL_EVENTS`.
- Feed normalization path explicitly preserves backward-compatible behavior while accepting canonical identifiers when present.
- Invalid payload handling remains fail-safe so malformed messages do not crash the SSE loop.

## 2) Safety confirmations

The following were explicitly confirmed as unchanged by scope and by boundary selection:

- `approve_signal` behavior unchanged.
- Order-router / execution path unchanged.
- `decision_agent` behavior unchanged.
- `signal_aggregator` behavior unchanged.
- Database models/migrations unchanged.
- Workflows/dependencies unchanged.

Shared-event compatibility and robustness expectations remain intact:

- Canonical IDs remain optional at this feed boundary.
- Invalid payloads do not terminate the SSE stream loop.
- Legacy/backward-compatible feed behavior is preserved while allowing canonical IDs to pass through when present.

## 3) Test coverage protecting this boundary

Primary dashboard coverage:

- `tests/dashboard/test_api.py`
  - SSE feed endpoint contract coverage (headers + initial connection behavior).
  - Feed normalization helper coverage, including compatibility with optional canonical identifiers.
  - Guardrails ensuring normalization does not derive canonical identifiers from legacy route fields.

Relevant core shared-event boundary coverage:

- `tests/core/test_event_json_boundary_validation.py`
  - Shared-event JSON validation by `event_type`.
  - Optional canonical identifier compatibility checks.
  - Invalid JSON / invalid shape rejection semantics.

- `tests/core/test_event_redis_envelope_boundary.py`
  - Channel/event-type envelope validation for `CHANNEL_SIGNAL_EVENTS`.
  - Optional canonical identifier compatibility checks.
  - Invalid payload rejection semantics at Redis envelope boundary.

Together, these tests protect the `SignalEvent` compatibility envelope used by dashboard feed consumers even when payload quality varies.

## 4) Known non-goals still deferred

The following remain intentionally deferred after 0A-04F and are not part of this post-migration boundary:

- No signal-engine consumer migration.
- No signal-engine worker wiring changes.
- No strategy/scoring changes.
- No decision-agent proposal behavior changes.
- No approval path / order placement changes.

## 5) Guidance before next runtime migration

Before selecting any additional runtime shared-event migration:

1. Inspect signal-engine and agent-core rail wiring end-to-end to identify a concrete, single seam with explicit ownership.
2. Choose exactly one boundary for the next ticket.
3. Prefer non-execution, non-approval-adjacent seams; avoid execution-adjacent flows until the seam is isolated and testable without touching order placement paths.

Recommended next ticket framing:

- Documentation-first seam selection for one signal-engine/agent-core shared-event boundary with explicit kill criteria if execution-adjacent coupling is discovered.
