# PRD-P1-WX-KICKOFF — Phase 1 Weather Bot Kickoff and Ticket Plan

## 1. Purpose and posture
This document is the Phase 1 weather bot kickoff and ticket plan.

This kickoff explicitly references `PRD-P1-WX-UNBLOCK` as the prerequisite unblock note.

This kickoff is docs/static-test planning only.

This kickoff does not implement weather bot behavior.

This kickoff does not execute weather bot behavior.

This kickoff does not add external weather/API connector behavior.

This kickoff does not modify runtime behavior.

This kickoff does not add production connectors/API calls.

This kickoff does not add order placement, live trading, or autonomy.

## 2. Prerequisite evidence
This kickoff references the following prerequisite evidence:
- `PRD-P1-WX-UNBLOCK`
- `PRD-0A-CLOSE-01`
- `PRD-0B-IMPL-17`
- `PRD-0A-AUDIT-01`
- `PRD-0A-FIX-01`
- `PRD-0A-FIX-02`
- `PRD-0A-FIX-03`
- `PRD-0A-FIX-04`

Decision posture:
- Phase 1 is unblocked for kickoff/planning only.
- Weather bot implementation is not started by this ticket.
- Weather bot execution is not approved by this ticket.

## 3. Phase 1 weather bot scope
Phase 1 scope is planning-level and constrained to:
- weather event and weather market research posture definition.
- weather data source selection approval path definition.
- config/secrets fail-closed posture definition.
- connector/API approval requirements before any external API calls.
- local-only synthetic fixtures before any real connector scope.
- result/status/observability shape definition.
- no trading/autonomy/order placement.
- human-reviewed outputs only until later explicit approval.
- CI/static-test posture required for every ticket.

## 4. Phase 1 non-goals
Phase 1 kickoff non-goals are explicit:
- no live trading.
- no order placement.
- no autonomous execution.
- no production connector/API calls without approval.
- no production loaders.
- no production query engine service.
- no runtime weather execution in kickoff.
- no secrets committed.
- no generated artifact commit.
- no final trading readiness claim.

## 5. Proposed Phase 1 ticket sequence
| Ticket | Purpose | Allowed scope | Explicit non-approvals | Research depth | Language/tooling suitability | Depends on |
|---|---|---|---|---|---|---|
| PRD-P1-WX-01 Weather bot requirements and market taxonomy planning | Define what the weather bot watches and how outputs are framed | docs/static planning and taxonomy only | No runtime behavior, no connectors/API calls, no order placement/live trading/autonomy | Internal-only planning | docs + Python/pytest static checks only | PRD-P1-WX-KICKOFF |
| PRD-P1-WX-02 Weather data provider research and connector approval gate | Evaluate provider options and define connector approval evidence | research artifact + approval-gate definition only | No connector implementation, no runtime execution, no trading/autonomy | Approval/research ticket | docs + Python/pytest static checks only | PRD-P1-WX-01 |
| PRD-P1-WX-03 Weather bot config contract and fail-closed env posture | Define configuration contract and fail-closed behaviors | docs/tests for config contract shape only | No secrets committed, no runtime execution, no trading/autonomy | Internal planning/spec | docs + Python/pytest static checks only | PRD-P1-WX-01 |
| PRD-P1-WX-04 Weather bot result/status summary contract | Define result/status schema and observability expectations | docs/tests for status contract only | No production execution, no order placement/live trading/autonomy | Internal planning/spec | docs + Python/pytest static checks only | PRD-P1-WX-03 |
| PRD-P1-WX-05 Synthetic weather fixture schema and local-only test harness | Define synthetic weather fixture schema and local harness | local synthetic fixtures + tests only | No external API calls, no production loaders, no trading/autonomy | Internal synthetic-only | docs + Python/pytest static checks only | PRD-P1-WX-04 |
| PRD-P1-WX-06 Weather market candidate model skeleton, synthetic only | Build candidate model skeleton backed by synthetic input | local-only model skeleton + unit tests | No production connectors, no runtime weather execution, no trading/autonomy | Internal synthetic-only | Python/pytest only | PRD-P1-WX-05 |
| PRD-P1-WX-07 Human-review output format and no-trade decision policy | Define operator review outputs and no-trade policy | docs/tests for review format and no-trade policy | No auto execution, no live trading/order placement, no autonomy | Internal policy/spec | docs + Python/pytest static checks only | PRD-P1-WX-06 |
| PRD-P1-WX-08 Connector implementation gate, only if provider approval is complete | Permit connector implementation work only after gate evidence | connector implementation planning gate only | No production runtime execution before runtime approval, no trading/autonomy | Gate-controlled | Python/pytest only | PRD-P1-WX-02 and PRD-P1-WX-07 |
| PRD-P1-WX-RUNTIME-APPROVAL before any runtime execution behavior | Explicit decision gate for runtime weather behavior | approval artifact only | Blocks all runtime execution until approved | Internal approval | docs + Python/pytest static checks only | PRD-P1-WX-08 |
| PRD-P1-WX-TRADING-AUTONOMY-APPROVAL before any trading/autonomy behavior | Explicit decision gate for any trading/autonomy | approval artifact only | Blocks live trading/order placement/autonomy until approved | Internal approval | docs + Python/pytest static checks only | PRD-P1-WX-RUNTIME-APPROVAL |

## 6. First implementation ticket recommendation
The immediate next ticket should be:
- `PRD-P1-WX-01 Weather bot requirements and market taxonomy planning`

Why this should come first:
- before provider/API work, define what the weather bot actually watches.
- define weather market taxonomy before connector decisions.
- define outputs and non-goals before implementation.
- avoid premature connector implementation.
- preserve Phase 0 safety posture while entering Phase 1.

## 7. Approval gates
### Provider/API connector approval gate
- purpose: approve external provider selection and connector constraints before connector implementation.
- minimum evidence: provider comparison artifact, approval decision record, connector contract draft.
- what it blocks: any external weather/API connector implementation or external API calls.
- required tests: static checks proving no connector runtime behavior prior to approval.

### Config/secrets fail-closed gate
- purpose: guarantee missing/invalid config fails closed.
- minimum evidence: config contract doc and fail-closed test cases.
- what it blocks: any ticket that would rely on non-fail-closed configuration behavior.
- required tests: unit/static tests for fail-closed config outcomes.

### Synthetic fixture gate
- purpose: require local synthetic fixtures before real data connectors.
- minimum evidence: documented synthetic schema and local harness test plan.
- what it blocks: real external data connector behavior.
- required tests: local-only fixture schema tests and harness checks.

### Result/status/observability gate
- purpose: standardize result/status/observability outputs before runtime behavior.
- minimum evidence: documented output contract with status fields and observability expectations.
- what it blocks: runtime behavior without reviewable outputs.
- required tests: static/unit tests validating output and status contract.

### Runtime execution approval gate
- purpose: explicit approval before any runtime weather execution behavior.
- minimum evidence: prior gates complete, runtime risk review, operator approval posture retained.
- what it blocks: all runtime weather execution.
- required tests: runtime approval artifact checks plus regression test posture evidence.

### Trading/autonomy approval gate
- purpose: explicit approval before any trading/autonomy behavior.
- minimum evidence: separate trading/autonomy risk decision and governance sign-off.
- what it blocks: order placement, live trading, autonomous execution.
- required tests: policy and control tests proving no autonomous or trading behavior before approval.

## 8. Phase 1 safety rules
- every ticket must include overview and bigger-picture fit.
- every ticket must include research depth flag.
- every ticket must include language/tooling suitability check.
- no implementation before approval gates.
- no external API call without connector approval.
- no secrets committed.
- no weather execution before runtime approval.
- no trading/autonomy/order placement.
- no generated artifacts committed.
- canonical identifier guard preserved.

## 9. CI/test posture
- every Phase 1 ticket should include focused static/unit tests.
- full `tests/core` should remain green.
- canonical identifier guard should remain green.
- docs/static tickets should not import production runtime modules.
- implementation tickets must include fail-closed tests.
- avoid brittle mtime/git-status changed-file unit tests.

## 10. What this kickoff approves
This kickoff approves only:
- Phase 1 planning/ticket sequencing.
- moving to `PRD-P1-WX-01`.
- defining approval gates.
- documenting non-production weather bot scope.

## 11. What this kickoff does not approve
- no weather bot implementation in this ticket.
- no weather bot execution.
- no external weather/API connector implementation.
- no production connectors/API calls.
- no production loaders.
- no production query engine service.
- no order placement.
- no live trading.
- no autonomous execution.
- no runtime behavior change.
- no production latency SLO claim.
- no final trading readiness claim.
- no generated artifact commit.
- no committed fixtures.
- no secrets committed.

## 12. Recommended next tickets
- `PRD-P1-WX-01 Weather bot requirements and market taxonomy planning`
- `PRD-P1-WX-02 Weather data provider research and connector approval gate`
- `PRD-P1-WX-03 Weather bot config contract and fail-closed env posture`
