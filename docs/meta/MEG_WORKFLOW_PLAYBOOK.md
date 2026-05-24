# MEG Workflow Playbook

## 1) Standard PR review workflow
1. Fetch PR.
2. Inspect changed files.
3. Inspect diff scope.
4. Fetch workflow runs for head SHA.
5. Identify CI state.
6. Compare with ticket allowed scope/files.
7. Identify substantive merge blockers only.
8. Do not open unnecessary issues.
9. Provide final merge recommendation.
10. If merge-ready, provide next ticket prompt.

## 2) Merge blocker definition
### Blockers
- CI failure
- changed forbidden files
- dependency/lockfile drift
- runtime behavior added in docs-only ticket
- external API/network behavior without approval
- secrets/artifacts committed
- production/trading/autonomy behavior without approval
- missing required doc/test sections
- test contract contradiction
- order-dependent brittle CI failure
- safety posture contradiction

### Non-blockers
- audit correctly finding blocked status
- required explicit safety disclaimers
- minor style notes
- future hardening notes
- expected docs-only non-implementation
- local review notes when CI is green and contract is satisfied

## 3) Issue opening policy
- Do not open issues unless user reports a blocker, asks, or current ticket explicitly requires blocker issue creation.
- Prefer preparing issue text rather than opening.
- If an issue is opened accidentally, close as not planned and acknowledge.

## 4) Ticket creation workflow
Each ticket should include: ticket name, bigger-picture fit, research depth flag, language/tooling suitability check, branch name, dependency check, read list, task, goal, allowed files, forbidden files, implementation/doc/test requirements, static canonical-ID guard, blocker tracking workflow, required commands, return format, and self-review prompt.

## 5) Self-review workflow
Check: merge blockers, allowed scope, pyproject/lockfile changes, runtime behavior changes, scripts/workflows/SQL changes, artifacts/secrets/.duckdb/generated outputs, safety posture, doc requirements, test requirements, canonical ID guard, required commands, final merge recommendation.

## 6) Static tests style rules
- Docs/static tickets: pytest + standard library only.
- Avoid git status inside unit tests.
- Avoid mtime changed-file inference.
- Avoid broad secret-string scanning.
- Avoid false-positive forbidden-term scans on safety disclaimers.
- Test existence/content/posture deterministically.
- No production runtime imports in static tests.

## 7) Canonical identifier guard
- Avoid literal legacy identifier if possible.
- Prefer `source_market_ref`, `condition_ref`, `token_ref`, native market reference, source market reference.
- If unavoidable, update `tests/core/canonical_id_allowlist.py` narrowly.
- Do not casually increase legacy identifier count.

## 8) Research depth flag policy
- No outside research needed.
- Light internal planning.
- Deep research required.
- External provider/legal/API research required.
- High-risk domain research required.

## 9) Language/tooling suitability policy
For each ticket, explicitly consider:
- Python/pytest/docs
- DuckDB only for local research/data tickets
- no Rust/C++ unless justified performance-critical need
- no TypeScript unless UI/frontend need
- no dependency changes unless explicitly required

## 10) Phase sequencing policy
- Phase 0 artifacts/gates before Phase 1 runtime behavior.
- connector approval before external API calls.
- runtime approval before execution.
- trading/autonomy approval before order placement/live trading/autonomy.
- weather bot starts with taxonomy/requirements, not provider implementation.
