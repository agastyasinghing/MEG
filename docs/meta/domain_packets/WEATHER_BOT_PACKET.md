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
- The Weather Bot is on the Stage 2 static historical-label fixture track.

## Recent completed artifacts

- PR #191 covered targeted Stage 2 skeleton mapping-builder validation gaps.
- PR #192 closed out/checkpointed the Stage 2 skeleton and listed future gates without approval.
- PR #193 created the static fixture/data approval-request posture that allowed fixture planning to be requested after human approval.
- PR #194 completed static historical-label fixture planning.

## Current approved gate

- Static fixture planning is complete.
- Planning completion does not authorize fixture files, data, ingestion, scoring, runtime, or trading.

## Next possible gate

- The next possible Weather Bot gate is static fixture implementation approval request only.

## Explicitly not approved

- Fixture implementation is not approved.
- Historical-label data is not approved.
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

## Stage 2 skeleton summary

- The skeleton accepts supplied metadata and preserves static review boundaries.
- It must remain fail-closed around required metadata and closed-set values.
- Do not modify Weather Bot behavior while handling docs/static-test operations tickets.

## Fixture track summary

- The fixture track has completed planning only.
- A later request may ask for approval to implement static fixtures.
- No fixture data or generated fixture artifact exists from the planning gate.

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

## Weather Bot PR review additions

- Confirm no Weather Bot runtime/source behavior changed in docs/static-test tickets.
- Confirm no fixture data, generated data, ingestion, connectors, external API calls, scoring/backtesting, runtime observation, trading, order placement, autonomy, or production behavior was added.
- Confirm closed-set/static-test parsing is section-scoped.

## Relationship to future phases

- Fixture implementation: may only be considered through a separate approval request.
- Ingestion: not approved by Stage 2 skeleton or fixture planning.
- Provider/source integration: not approved.
- Scoring/backtesting: not approved.
- Paper simulation: not approved.
- Runtime observation: not approved.
- Trading/order/autonomy: not approved.
