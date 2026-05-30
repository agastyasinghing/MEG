# PRD-P1-WX-STAGE2-SKELETON-03 — Targeted Mapping-Builder Validation Coverage

## Canonical ID

PRD-P1-WX-STAGE2-SKELETON-03

## Status / scope

Status: targeted Stage 2 skeleton validation-coverage guard.

Scope is test-only coverage for supplied metadata mapping-builder validation behavior unless tests reveal a real fail-closed implementation bug. This ticket does not broaden the Stage 2 skeleton beyond the existing supplied-metadata-only contract.

## Review gap source

This guard records the narrow Stage 2 skeleton review gaps found after PR #190 and after these predecessor tickets:

- PRD-P1-WX-STAGE2-SKELETON-01: narrow supplied-metadata-only skeleton implementation.
- PRD-P1-WX-STAGE2-SKELETON-02: validation coverage refinement.

The review pass found only targeted validation coverage gaps in mapping-builder and supplied metadata validation paths.

## Allowed test-only scope

Allowed work is limited to focused Python tests and this guard document. The tests may import the source module, construct supplied in-memory metadata mappings, call existing mapping builders, call existing validation helpers, and assert fail-closed behavior.

No historical label records, provider payloads, market payloads, files, credentials, service clients, or generated datasets are introduced.

## Exact coverage gaps addressed

The targeted tests cover these concrete gaps:

- non-string `outcome` does not pass validation.
- non-string `venue_rule_summary` does not pass validation.
- non-string `resolver_source_identity` does not pass validation.
- whitespace-only `resolver_source_identity` does not pass validation.
- missing nested metadata key `source_resolution` does not pass silently.
- missing nested metadata key `point_in_time_provenance` does not pass silently.
- missing nested metadata key `label_usability` does not pass silently.
- non-mapping nested metadata for `source_resolution` does not pass silently.
- non-mapping nested metadata for `point_in_time_provenance` does not pass silently.
- non-mapping nested metadata for `label_usability` does not pass silently.
- the guard doc exists and contains canonical ID `PRD-P1-WX-STAGE2-SKELETON-03`.
- the source module still imports.
- valid supplied metadata still passes.
- tests do not create files or call network.
- source and new test text avoid forbidden implementation-like tokens.

## Explicit non-approval boundaries

This ticket explicitly approves none of the following:

- no ingestion
- no provider/API connectors
- no external API calls
- no credentials/secrets/config loading
- no forecast pulls
- no historical-label data
- no fixtures/generated data
- no scoring/backtesting/runtime/trading/order placement/autonomy
- no paper simulation
- no provider integration
- no model or probability scoring
- no runtime observation
- no trading, position sizing, execution, or operator-bypassing behavior
- no new dependencies
- no C++/Rust components

## Changed files

Expected changed files for this ticket:

- `docs/prd/PRD-P1-WX-STAGE2-SKELETON-03_TARGETED_MAPPING_BUILDER_VALIDATION_COVERAGE.md`
- `tests/core/test_prd_p1_wx_stage2_skeleton_03_mapping_builder_validation.py`

`meg/weather/stage2/historical_label.py` may only change if the targeted tests reveal a real implementation bug requiring the smallest possible fail-closed fix.

## Validation commands

Required validation commands:

- `python -m py_compile meg/weather/stage2/historical_label.py`
- `python -m py_compile tests/core/test_prd_p1_wx_stage2_skeleton_03_mapping_builder_validation.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_skeleton_03_mapping_builder_validation.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_skeleton_02_validation_coverage.py`
- `python -m pytest -q tests/core/test_prd_p1_wx_stage2_skeleton_01_historical_label.py`
- `python -m pytest -q tests/core/test_static_canonical_ids.py`
- `python -m pytest -q tests/core`
- `rg -n "market_id" docs/prd/PRD-P1-WX-STAGE2-SKELETON-03_TARGETED_MAPPING_BUILDER_VALIDATION_COVERAGE.md tests/core/test_prd_p1_wx_stage2_skeleton_03_mapping_builder_validation.py tests/core/canonical_id_allowlist.py meg/weather/stage2/historical_label.py`
- implementation-token audit command from the ticket prompt.
- `git diff --check`
- `git status --short`
- `git show --name-only --pretty=format: HEAD`

## Later-ticket handoff

Hold for review if the targeted tests pass and no implementation-like behavior is introduced. Only open another narrow validation coverage ticket if reviewers identify a concrete additional supplied-metadata skeleton gap. Ingestion, provider/API connectors, external API calls, forecast pulls, historical-label data creation, scoring, backtesting, runtime observation, trading, order placement, and autonomy remain out of scope until separately approved by a later Stage 2 gate.
