# MEG PR Review Checklist

Use this checklist for advisory PR reviews.

## 1. PR metadata check
- Identify PR number, branch, title, author if available, head SHA if available, and stated ticket.
- Confirm the review is advisory and not final approval.

## 2. Changed-file scope check
- List changed files.
- Compare every changed file with the ticket allowed-files list.
- Flag unexpected dependency, lockfile, generated, data, fixture, workflow, script, SQL, migration, secret, or runtime files.

## 3. Allowed-files/do-not-modify check
- Verify allowed files were changed only as authorized.
- Verify do-not-modify files and directories are untouched.

## 4. Source/runtime/connector/ingestion/scoring/trading drift check
- Confirm no product behavior drift when the ticket is docs/static-test only.
- Confirm no ingestion, provider/API connector, external API call, scoring/backtesting, runtime observation, paper simulation, trading, order placement, autonomy, or production behavior was introduced without explicit approval.

## 5. Closed-set completeness check
- Confirm every required closed-set category has an exact allowed value set.
- Confirm actual machine-checkable values use exact allowed values only.
- Confirm tests reject hybrid/custom actual values.

## 6. Machine-checkable section scope check
- Confirm static tests parse actual assignments only from dedicated machine-checkable sections.
- Confirm prose examples do not become actual values.

## 7. No global forbidden-word contradiction check
- Do not block a PR merely because safety prose contains a forbidden term.
- Prefer section-scoped parsing and exact positive-approval drift checks.

## 8. No optional-missing closed-set loophole check
- Confirm missing optional fields are not accepted as a workaround unless explicitly approved by the controlling PRD/ticket.

## 9. Validation command results check
- Record local command results and CI status separately.
- Include failures, skips, xfails, and environment limitations.

## 10. CI/workflow check
- Check CI status when available.
- Do not modify workflows unless the ticket explicitly allows it.

## 11. Docs/source-of-truth consistency check
- Confirm new docs do not contradict `AGENTS.md`, active state, phase ledger, or controlling PRDs.
- Confirm source-of-truth PRDs were not altered without explicit approval.

## 12. Final merge/block recommendation format
- Verdict: merge-ready / blocked / needs human decision.
- Blocking reasons, if any.
- Non-blocking notes, if any.
- Safety/non-approval summary.

## 13. Recommended next ticket format
- Name the next ticket.
- State whether it is approval-request only, planning only, docs/static-test only, or implementation.
- State explicitly what it must not approve.

## 14. Special blocker/fix review procedure
- Reproduce or inspect the blocker.
- Keep the fix prompt narrow.
- Preserve the original ticket scope and file boundaries.
- Require blocker/fix return fields: files changed, scope summary, safety/non-approval summary, test command results, whether blocker is resolved, whether related issue can be closed if any, final merge recommendation, and recommended next ticket.
