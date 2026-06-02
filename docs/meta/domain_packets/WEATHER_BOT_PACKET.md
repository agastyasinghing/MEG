# Weather Bot Context Packet

## Purpose

Provide compact Weather Bot context for fresh chats, ticket generation, and PR review without granting new implementation authority.

## Source-of-truth hierarchy

1. `AGENTS.md`
2. `docs/meta/MEG_ACTIVE_STATE.md`
3. Weather Bot PRDs, especially `docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`
4. Stage 2 skeleton and fixture PRDs
5. `docs/meta/MEG_TICKET_STYLE_GUIDE.md` and `docs/meta/MEG_PR_REVIEW_CHECKLIST.md`

## Current phase/status

- Stage 2 skeleton v1 complete.
- Static fixture planning completed by PR #194.
- Static fixture implementation v1 is complete and closed out by PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01.
- The fixture set is exactly three synthetic, hand-authored JSON fixtures under `tests/fixtures/weather/stage2_historical_labels/`.
- The next default posture is hold/checkpoint.

## Recent completed artifacts

- PR #191 covered targeted Stage 2 skeleton mapping-builder validation gaps.
- PR #192 closed out/checkpointed the Stage 2 skeleton and listed future gates without approval.
- PR #193 created the static fixture/data approval-request posture that allowed fixture planning to be requested after human approval.
- PR #194 completed static historical-label fixture planning.
- PR #198 / PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01 closed out static fixture implementation v1.

## Current approved gate

- Stage 2 skeleton v1 is complete.
- Static fixture planning is complete.
- Static fixture implementation v1 is complete and closed out.
- Exactly three static synthetic, hand-authored JSON fixtures are the complete fixture set for the closed-out subphase.
- Completion of this fixture subphase does not authorize ingestion, scoring, backtesting, runtime, trading, order placement, autonomy, production behavior, or later Weather Bot gates.

## Next possible gate

- The next default Weather Bot posture is hold/checkpoint unless a concrete fixture validation gap is found or the user explicitly chooses a later approval gate.
- If the user explicitly chooses to continue, the next work must be a separate approval/request/planning gate.
- Separately approved later work may include targeted fixture validation refinement if a concrete gap exists, or planning/approval-request work for real source-backed fixtures or historical-label loading.
- Do not proceed directly to ingestion, scoring, runtime, trading, order placement, autonomy, or production behavior.

## Explicitly not approved

- Real historical-label data is not approved.
- Generated data is not approved.
- Ingestion is not approved.
- Provider/source integration and provider/API connectors are not approved.
- External API calls are not approved.
- Credentials/secrets/config loading is not approved.
- Forecast pulls are not approved.
- Scoring and backtesting are not approved.
- Paper simulation is not approved.
- Runtime observation is not approved.
- Trading, order placement, and autonomy are not approved.
- Production behavior is not approved.
- C++/Rust runtime components are not approved.

## Stage 2 skeleton summary

- The Stage 2 skeleton v1 is complete.
- The skeleton accepts supplied metadata and preserves static review boundaries.
- It must remain fail-closed around required metadata and closed-set values.
- Do not modify Weather Bot behavior while handling docs/static-test operations tickets.

## Fixture track summary

- Static fixture implementation v1 is complete and closed out.
- Exactly three synthetic, hand-authored JSON fixtures exist under `tests/fixtures/weather/stage2_historical_labels/`.
- The three synthetic fixtures remain the complete fixture set for this subphase.
- No real historical-label data or generated data is approved by the fixture closeout.
- Hold/checkpoint is the recommended posture unless a concrete fixture validation gap is found or the user explicitly chooses a later approval gate.

## Closed-set/static-test pitfalls

- Define exact allowed values.
- Parse actual values only from bounded machine-checkable sections.
- Reject hybrid/custom values.
- Do not use optional-missing exceptions unless explicitly approved.
- Do not treat forbidden prose examples as actual values.

## Weather Bot ticket conventions

- State current gate and next possible gate.
- Include allowed files and do-not-modify lists.
- Keep docs/static-test tickets separate from implementation tickets.
- Preserve non-approval language for later phases.
- Treat any continued work after fixture closeout as a separately approved later gate, not as direct implementation authority.

## Weather Bot PR review additions

- Confirm no Weather Bot runtime/source behavior changed in docs/static-test tickets.
- Confirm no real historical-label data, generated data, ingestion, connectors, external API calls, scoring/backtesting, runtime observation, trading, order placement, autonomy, or production behavior was added.
- Confirm closed-set/static-test parsing is section-scoped.

## Relationship to future phases

- Targeted fixture validation refinement: only if a concrete gap is found and scoped as a separate gate.
- Real source-backed fixtures or historical-label loading: not approved unless separately requested/planned/approved.
- Ingestion: not approved by Stage 2 skeleton, fixture planning, fixture implementation, or fixture closeout.
- Provider/source integration: not approved.
- Scoring/backtesting: not approved.
- Paper simulation: not approved.
- Runtime observation: not approved.
- Trading/order/autonomy: not approved.
