# PRD-P1-WX-03: Weather Bot Config/Secrets Fail-Closed Contract

## 1. Status and scope
PRD-P1-WX-03 is **Phase 1 weather bot config/secrets fail-closed contract planning only**.

This ticket does **not** approve config-loading implementation, environment-variable loading, or secret reading.

This ticket does **not** approve connector implementation, external API calls, provider credentials usage, runtime execution, forecast pulls, trading, order placement, or autonomy.

This document defines a **future contract** that later implementation tickets must satisfy before any runtime behavior can be considered.

## 2. Strategic framing
PRD-P1-WX-03 follows PRD-P1-WX-01 and PRD-P1-WX-02 in the weather roadmap.

- PRD-P1-WX-01 established canonical weather event identity, taxonomy, and human-review expectations.
- PRD-P1-WX-02 established provider research discipline and connector approval gate expectations.
- PRD-P1-WX-03 defines config/secrets contract boundaries that keep provider readiness explicit and non-implicit.

Fail-closed config/secrets behavior protects MEG’s canonical event graph by preventing ambiguous or unsafe provider behavior from bypassing the provider approval gate.

## 3. Fail-closed principle
Fail-closed means that if readiness is not explicitly valid and approved, provider operation is blocked.

- missing, disabled, unapproved, or invalid config/secrets states must prevent provider operation.
- Silent defaults are prohibited.
- Fallback providers are prohibited.
- Opportunistic live calls are prohibited.
- Best-effort credential discovery is prohibited.
- No config state may escalate from not-ready to ready without explicit approval and validation.
- Fail-open behavior is prohibited.

## 4. Closed readiness state vocabulary
The exact closed readiness state set is:

- missing
- disabled
- unapproved
- invalid
- ready

No other actual readiness-state values are allowed.
Hybrid, custom, and slash-based actual values are forbidden.
Nuance belongs in prose notes, not custom readiness values.
If a condition is mixed or partial, use the most conservative exact state.

Definitions:

- missing: required config/secrets are absent.
- disabled: provider use is intentionally disabled.
- unapproved: required approval gate is not satisfied.
- invalid: config/secrets are present but malformed, inconsistent, unsafe, or fail validation.
- ready: relevant config/secrets conditions are present, valid, and explicitly approved, while still subject to later connector/runtime approval gates.

Ready does not approve connector implementation, runtime execution, external API calls, trading, order placement, or autonomy.

## 5. Forbidden readiness values
The following are forbidden as actual readiness-state assignments:

- missing/invalid
- disabled/unapproved
- unapproved/invalid
- ready/disabled
- ready/invalid
- partial
- mixed
- ready_with_warnings
- maybe_ready
- approved
- configured
- available
- unknown

These are documented only as forbidden examples. They may appear in explanatory prose but must not be used as actual readiness-state values.

## Machine-checkable readiness-state assignments
- expected readiness state: missing
- expected readiness state: disabled
- expected readiness state: unapproved
- expected readiness state: invalid
- expected readiness state: ready

## 7. Future config contract dimensions
Future implementation (in later explicitly approved tickets) must conceptually account for:

- provider identifier
- provider enablement flag
- provider approval flag
- connector approval flag
- runtime approval flag
- credential presence
- credential validation posture
- environment name or execution context
- network allowance posture
- forecast/pull allowance posture
- human-review mode
- dry-run or non-executing mode
- audit/logging posture
- terms-of-use acknowledgement posture, if applicable
- provider-specific capability flags, if later approved

## 8. Secrets contract
Future work must preserve these constraints:

- no secrets in repo
- no secrets in docs
- no secrets in tests
- no live credentials in fixtures
- no credential-shaped examples that look real
- no default secret names that imply active production use unless later approved
- no secret printing
- no secret persistence in logs
- no auto-discovery of credentials
- missing secrets must fail closed
- malformed secrets must fail closed
- unapproved secrets must fail closed

## 9. Approval gate layering
Future implementation must remain layered:

1. provider selected through PRD-P1-WX-02 or later approved research
2. connector implementation explicitly approved in a future ticket
3. config/secrets contract implemented in a future ticket
4. runtime behavior explicitly approved in a future ticket
5. forecast pulls explicitly approved in a future ticket
6. human-review output approved before any actionability
7. trading/order placement/autonomy remain unapproved unless explicitly gated later

## 10. Non-runtime behavior expectations
This ticket creates no runtime behavior.

Future implementation should be testable without network calls and should use synthetic placeholder values only.
Future config checks should produce safe status summaries rather than performing provider work.

## 11. Failure modes and required outcomes
| Failure mode | Expected readiness state | Expected fail-closed outcome | Human-readable reviewer note |
|---|---|---|---|
| Missing provider identifier | missing | Block provider use and require explicit identifier definition. | Provider identity absent; review cannot proceed. |
| Unsupported provider identifier | invalid | Block provider use until identifier aligns with approved provider set. | Provider identifier not recognized by approved mapping policy. |
| Provider disabled | disabled | Keep provider inactive and prohibit provider operations. | Provider is intentionally disabled by policy/config. |
| Provider not approved | unapproved | Block provider operations pending explicit approval gate outcome. | Provider has no approval decision or is denied. |
| Connector not approved | unapproved | Block any connector-level behavior and keep planning-only posture. | Connector implementation gate not approved yet. |
| Runtime not approved | unapproved | Block runtime activation and keep non-executing status reporting only. | Runtime gate is not approved for this context. |
| Credentials missing | missing | Block provider access and emit missing credential status only. | Required credential material is absent. |
| Credentials malformed | invalid | Block provider access and require credential format correction. | Credential data fails validation posture checks. |
| Credentials present but unapproved | unapproved | Block provider access until credential approval policy is satisfied. | Credentials exist but policy approval is not granted. |
| Environment not approved | unapproved | Block provider behavior in that execution context. | Environment/context lacks explicit approval. |
| Network/API calls not approved | unapproved | Prohibit outbound calls and keep status-only behavior. | Network/API allowance gate is closed. |
| Forecast pulls not approved | unapproved | Prohibit forecast pulls and keep planning-only posture. | Forecast pull gate remains closed. |
| Ambiguous config | invalid | Block provider behavior until ambiguity is resolved deterministically. | Conflicting interpretation risk detected in config semantics. |
| Conflicting config | invalid | Block provider behavior and require explicit conflict resolution. | Inconsistent flags/values violate contract consistency. |
| Terms-of-use acknowledgement missing (if applicable) | unapproved | Block provider use until applicable acknowledgement gate is approved. | Required legal/policy acknowledgement is missing. |

## 12. Human-review and observability handoff
Future status summaries should communicate:

- provider name or provider placeholder
- readiness state
- missing/invalid/unapproved reason
- non-approval boundaries
- whether network/API access is allowed
- whether runtime is allowed
- whether forecast pulls are allowed
- whether trading/order/autonomy are allowed

Detailed result/status/observability output contract is handed off to PRD-P1-WX-04.

## 13. Explicit non-goals and non-approvals
PRD-P1-WX-03 does not approve:

- config-loading implementation
- environment-variable loading
- secret reading
- connector implementation
- external API calls
- provider credentials
- forecast pulls
- forecast modeling
- probability modeling
- runtime scheduling
- production monitoring
- trading strategy
- order placement
- position sizing
- autonomy
- live market execution
- final Weather Bot PRD synthesis

## 14. Later-ticket handoff
This ticket hands off:

- result/status/observability contract details to PRD-P1-WX-04
- deep weather research pack to later weather research docs
- full standalone Weather Bot PRD to later Opus synthesis
- connector implementation to a future ticket only after explicit approval
- config/secrets implementation to a future ticket only after explicit approval
- runtime behavior to a future ticket only after explicit approval

## 15. Acceptance criteria
- [x] PRD-P1-WX-03 canonical ID is present.
- [x] Fail-closed principle is defined.
- [x] Exact closed readiness state set is listed.
- [x] No other actual readiness-state values are allowed.
- [x] Hybrid/custom/slash actual readiness values are forbidden.
- [x] Forbidden examples are documented without being used as actual state assignments.
- [x] Machine-checkable readiness-state assignment section exists.
- [x] Machine-checkable readiness-state assignments use only allowed values.
- [x] Future config dimensions are defined conceptually.
- [x] Secrets contract is defined conceptually.
- [x] Approval layering is defined.
- [x] Failure-mode outcomes use only allowed readiness states.
- [x] Human-review/observability handoff is defined.
- [x] Non-goals and non-approvals are explicit.
- [x] Later-ticket handoff is clear.
- [x] No config-loading/connector/runtime/API/forecast/trading/order/autonomy behavior is introduced.
