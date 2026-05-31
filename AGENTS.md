# MEG Agent Rules

## Operating constitution

- MEG is PRD-driven. Treat approved PRDs and repo meta docs as the source-of-truth hierarchy for planning, review, and implementation scope.
- Treat `MEG_MASTER_PRD_v4.1_patched.md` as the frozen source of truth; do not edit it unless explicitly asked.
- Read repo meta docs before generating tickets or reviewing PRs, starting with `docs/meta/MEG_ACTIVE_STATE.md`, `docs/meta/MEG_CONTEXT_ROUTER.md`, `docs/meta/MEG_WORKFLOW_PLAYBOOK.md`, `docs/meta/MEG_TICKET_STYLE_GUIDE.md`, and `docs/meta/MEG_PR_REVIEW_CHECKLIST.md` when present.
- Do not open issues unless explicitly asked or approved.
- Do not merge PRs.
- Do not approve PRs as final authority; provide advisory merge/block recommendations only.
- Do not approve connectors, runtime behavior, trading, order placement, or autonomy.
- Do not change secrets, credentials, environment files, or secret-loading behavior unless explicitly approved.
- Do not alter source-of-truth PRDs without explicit approval.
- Preserve closed-set enum/status/value requirements exactly.
- Do not invent hybrid/custom values unless explicitly allowed by the controlling PRD or ticket.
- Use `tests/core` for static PRD/meta tests unless repo precedent clearly says otherwise.

## Phase and safety boundaries

- Keep Phase 0A work limited to shared rail infrastructure: identifiers, event contracts, Redis channels, market/user streams, Telegram approval queue, Postgres journaling, paper execution, heartbeat, and risk gates.
- Do not add weather strategy, whale strategy, or live-trading strategy implementation while working on Phase 0A documentation.
- Prefer small tickets with explicit acceptance criteria and tests before broad refactors.
- Preserve the canonical identifier contract everywhere: `condition_id`, `token_id`, and `outcome`; never route on `market_id`.
- All execution paths must remain operator-approved through Telegram; no autonomous execution authority.
- Postgres is for operational journaling; DuckDB/Parquet is for historical research data.

## Required ticket response structure

Every ticket response must include:

1. Brief verdict/context
2. Next ticket name
3. Bigger-picture fit
4. Research depth flag
5. Language/tooling suitability check
6. Main Codex prompt in one copyable code block
7. Self-review prompt in one copyable code block

## Required Main Codex prompt return format

Every Main Codex prompt return format must include:

- Files changed
- Scope summary
- Safety/non-approval summary
- Test command results
- Final merge recommendation
- Recommended next ticket

## Required Self-review prompt ending

Every Self-review prompt must also end with:

- Final merge recommendation
- Recommended next ticket
