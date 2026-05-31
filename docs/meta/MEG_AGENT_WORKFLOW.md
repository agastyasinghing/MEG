# MEG Agent Workflow

## Default posture

- There is no autonomous builder by default.
- The agent role is advisory/project-ops first.
- This document creates no runtime automation and installs no agent framework.

## Allowed future advisory actions

A future advisory workflow may:

- Read docs.
- Produce context packets.
- Draft next-ticket prompts.
- Draft self-review prompts.
- Review PR diffs.
- Recommend merge/block/next ticket.

## Prohibited actions

A future advisory workflow must not:

- Merge PRs.
- Approve PRs as final authority.
- Deploy.
- Change secrets.
- Alter source-of-truth PRDs without approval.
- Approve connectors, runtime, trading, order placement, or autonomy.
- Reinterpret safety boundaries.
- Invent closed-set values.
- Auto-merge.

## Adoption stages

1. Manual workflow.
2. Repo-native docs/templates.
3. Read-only advisory agent.
4. PR review assistant.
5. Approved progress-log updates only.
6. No full autonomy.

## Safe sandboxing principles

- Read-only clone first.
- No write token initially.
- No secrets.
- No auto-merge.
- No runtime/product behavior permissions.

## Explicit non-approval

This workflow does not approve fixture implementation, ingestion, provider/API connectors, scoring/backtesting, runtime observation, trading, order placement, autonomy, deployment, or production behavior.
