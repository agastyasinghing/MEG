# MEG Active State

This is the first working-memory file to read after `AGENTS.md`.

## Current active project
- MEG repo-native project operations and Weather Bot gated planning.

## Current active area
- MEG Weather Bot Stage 2 static historical-label fixture track.

## Current active phase
- Post-PR #194 static fixture planning completed; MEG-OPS-01 is the immediate ops-docs handoff ticket until this PR merges.

## Latest merged PR
- PR #194 was merged by the user.

## Latest reviewed PR
- PR #194 is the latest reviewed sequence item recorded in this active state.

## Current approved gate
- Static fixture planning completed for the Stage 2 historical-label fixture track.
- Planning completion does not grant implementation authority.

## Next possible gate
- The next possible gate is static fixture implementation approval request only.
- If continuing Weather Bot work, the current recommended next Weather Bot ticket is a static fixture implementation approval request only.

## Explicitly not approved
- Fixture implementation is not approved.
- Historical-label data is not approved.
- Generated data is not approved.
- Ingestion is not approved.
- Provider/API connectors are not approved.
- External API calls are not approved.
- Credentials/secrets/config loading is not approved.
- Forecast pulls are not approved.
- Scoring is not approved.
- Backtesting is not approved.
- Paper simulation is not approved.
- Runtime observation is not approved.
- Trading is not approved.
- Order placement is not approved.
- Autonomy is not approved.
- Production behavior is not approved.

## Current controlling docs
- `AGENTS.md`
- `docs/meta/MEG_ACTIVE_STATE.md`
- `docs/meta/MEG_CONTEXT_ROUTER.md`
- `docs/meta/MEG_WORKFLOW_PLAYBOOK.md`
- `docs/meta/MEG_TICKET_STYLE_GUIDE.md`
- `docs/meta/MEG_PR_REVIEW_CHECKLIST.md`
- `docs/meta/MEG_PHASE_LEDGER.md`
- `docs/meta/domain_packets/WEATHER_BOT_PACKET.md`
- `docs/meta/domain_packets/CORE_WORKFLOW_PACKET.md`
- `docs/prd/PRD-P1-WX-STANDALONE_WEATHER_BOT_PRD.md`
- `docs/prd/PRD-P1-WX-STAGE2-SKELETON-CLOSEOUT-01_STAGE_2_SKELETON_CLOSEOUT_CHECKPOINT.md`
- `docs/prd/PRD-P1-WX-STAGE2-FIXTURE-APPROVAL-01_STATIC_FIXTURE_DATA_APPROVAL_REQUEST.md`
- `docs/prd/PRD-P1-WX-STAGE2-FIXTURE-PLAN-01_STATIC_HISTORICAL_LABEL_FIXTURE_PLANNING.md`

## Current Weather Bot status summary
- Stage 2 skeleton v1 is complete.
- Static historical-label fixture planning was completed by PR #194.
- The fixture track remains planning/request-gated only.
- Fixture implementation, historical-label fixture data, ingestion, provider/source integration, scoring/backtesting, paper simulation, runtime observation, trading, order placement, autonomy, and production behavior remain outside the approved gate.

## Current ticket style
- Use the MEG ticket format from `docs/meta/MEG_TICKET_STYLE_GUIDE.md`.
- Every ticket response needs verdict/context, next ticket name, bigger-picture fit, research depth flag, language/tooling suitability check, one copyable Main Codex prompt, and one copyable Self-review prompt.

## Current PR review style
- Use `docs/meta/MEG_PR_REVIEW_CHECKLIST.md`.
- Reviews are advisory only and must end with a final merge/block recommendation plus a recommended next ticket.

## Known blockers
- No known blocker is recorded for MEG-OPS-01.
- Weather Bot fixture implementation cannot begin without a separate explicit human approval request and approval.

## Last updated by
- Codex for MEG-OPS-01, after user-reported PR #194 merge.

## How to use this file
- Read this file immediately after `AGENTS.md` in a fresh chat.
- Treat it as current working memory, not as a replacement for controlling PRDs.
- Use it to determine the active phase, approved gate, next possible gate, and forbidden scopes before writing tickets or reviewing PRs.
