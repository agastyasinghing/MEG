# MEG — Deferred TODOs

Items considered during planning and explicitly deferred. Each entry has enough
context to be picked up without re-reading the original planning session.

---

## [P2] pip-audit: dependency vulnerability scanning in CI

**What:** Add `pip-audit -r requirements.txt` as a required CI check on every PR.

**Why:** `requirements.txt` uses exact version pins for reproducibility, which
means security patches do not auto-apply. Without a scanner, a known CVE in a
pinned dependency could go unnoticed indefinitely.

**Pros:** Automated CVE gate. Catches dependency vulnerabilities before they
reach production. Zero false negatives on known CVEs in the advisory database.

**Cons:** Adds a CI step. Requires periodic manual version bumps when alerts
fire. May require triaging false positives on low-severity advisories.

**Context:** When CI is set up (planned post-dashboard phase), add:
```
pip-audit -r requirements.txt --fail-on-cvss 7.0
```
as a required check. Consider pairing with Dependabot or Renovate to auto-open
PRs for dependency updates.

**Effort:** S
**Priority:** P2
**Blocked by:** CI pipeline (no CI pipeline exists yet — planned for after dashboard phase)
