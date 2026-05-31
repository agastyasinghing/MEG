# Core Workflow Packet

## MEG workflow summary

MEG uses PRD-driven, gate-aware work. Tickets should be small, explicit about allowed files, and validated with static tests when the change is documentation or metadata. Reviews are advisory and should preserve the current gate instead of expanding scope.

## Opus/GPT-5.5/Codex roles

- Opus/GPT-5.5: high-level planning, ticket drafting, PR review reasoning, and next-gate recommendations when used by the human operator.
- Codex: repository-local edits, static tests, validation commands, commits, and PR preparation when explicitly assigned.
- Human operator: final approval authority for merges, gates, secrets, runtime behavior, connectors, trading, order placement, autonomy, and production decisions.

## How to generate tickets

- Read `AGENTS.md`, active state, context router, ticket style guide, and relevant domain packet.
- State verdict/context, next ticket name, bigger-picture fit, research depth flag, and language/tooling suitability check.
- Provide one copyable Main Codex prompt and one copyable Self-review prompt.
- Include allowed files, do-not-modify files, validation commands, return format, and safety boundaries.

## How to review PRs

- Read the PR review checklist.
- Compare changed files to the ticket scope.
- Check static-test and CI results.
- Confirm source-of-truth consistency and safety boundaries.
- End with advisory merge/block recommendation and recommended next ticket.
- Do not perform an autonomous merge or deploy.

## How to handle blocker/fix prompts

- Keep fixes narrow and tied to the reported failure.
- Preserve do-not-modify restrictions.
- Require a blocker-resolution return format.
- Do not open issues unless the user asks or approves.

## How to preserve closed sets

- Define exact allowed values.
- Parse actual values from dedicated machine-checkable sections.
- Reject hybrid/custom values.
- Avoid optional-missing loopholes unless explicitly approved.

## How to update active state/phase ledger after approval

- Update active state only after the human operator reports a merge or approval.
- Append to the phase ledger with PR number, description, result, and next possible gate.
- Do not fabricate merge SHAs.
- Do not convert planning completion into implementation authority.

## What must never be automated without explicit approval

- PR merges.
- Deployments.
- Secret changes.
- Source-of-truth PRD changes.
- Connector/provider/API integration.
- Ingestion.
- Scoring/backtesting.
- Runtime observation.
- Trading, order placement, or autonomy.
- Production behavior.
