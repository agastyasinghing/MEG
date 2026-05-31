# MEG Ticket Style Guide

## Required assistant response structure

Every ticket-generation answer must use this order:

1. Brief verdict/context
2. Next ticket name
3. Bigger-picture fit
4. Research depth flag
5. Language/tooling suitability check
6. Main Codex prompt in one code block
7. Self-review prompt in one code block

## Required Main Codex prompt components

A Main Codex prompt must include:

- Branch/dependency instructions.
- Read list.
- Task/goal.
- Allowed files.
- Do-not-modify list.
- Document/implementation/test requirements.
- Closed-set rules if applicable.
- Static canonical-ID guard if applicable.
- Blocker workflow if applicable.
- Validation commands.
- Return format.

## Required Codex return format

The Main Codex prompt must require this return format:

- Files changed
- Scope summary
- Safety/non-approval summary
- Test command results
- Final merge recommendation
- Recommended next ticket

## Required blocker/fix return format

A blocker/fix prompt must require this return format:

- Files changed
- Scope summary
- Safety/non-approval summary
- Test command results
- Whether blocker is resolved
- Whether related issue can be closed, if any
- Final merge recommendation
- Recommended next ticket

## Closed-set discipline

- Define the exact allowed value set before asking for static validation.
- A document must use only exact values as actual machine-checkable values.
- Tests must reject hybrid/custom actual values.
- Forbidden examples may appear in prose when needed for documentation or tests.
- Tests must parse actual values only from dedicated machine-checkable sections.
- There are no optional-missing exceptions unless explicitly approved.
- Do not use global forbidden-word scans when section-scoped parsing is the right contract.

## Prompt-size discipline

- Prefer repo-pattern references when safe.
- Avoid giant inline validators unless necessary.
- Keep compact Codex-safe prompts while preserving MEG rigor.
- Include exact validation commands even when the prose is compact.

## Static canonical-ID guard

When a ticket can touch shared rail identifiers, require preservation of `condition_id`, `token_id`, and `outcome`; reject new legacy routing unless the ticket explicitly authorizes a migration plan and matching static-test update.

## Safety language discipline

- Planning, approval-request, and docs/static-test tickets must state what they do not approve.
- Never let a future-phase list become implementation permission.
- Keep final recommendations advisory unless the user explicitly makes the final human decision.
