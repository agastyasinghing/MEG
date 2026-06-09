# PRD-P1-WX-STAGE2-HISTORICAL-LABEL-LOADING-IMPLEMENTATION-01 — Static Historical-Label Loading / Validation Implementation

## 1. Status and scope

Status: implemented as a narrow static validation skeleton.

This is static historical-label loading/validation implementation only. The implementation is limited to explicit static fixture validation for existing Stage 2 Weather Bot historical-label fixture directories. It exists to load caller-supplied JSON fixture paths, adapt their supplied metadata into the existing Stage 2 validator, and return deterministic validation artifacts for static tests.

## 2. Strategic framing

The standalone MEG Weather Bot PRD frames Weather Bot around venue-defined weather settlement objects, source compatibility, point-in-time evidence, and conservative stage gates. This implementation keeps that framing intact by validating only supplied fixture metadata and by refusing to infer readiness for later Weather Bot capabilities.

## 3. Stage ladder position

This ticket follows the closed Stage 2 skeleton, synthetic fixture, real source-backed fixture, and historical-label loading planning checkpoints. It is a small Stage 2 static-validation implementation step after human approval for this specific loader boundary only.

## 4. Human approval basis

Human approval was granted for historical-label loading/validation implementation only. That approval does not extend to ingestion, provider/source integration, external API calls, forecast pulls, scoring, backtesting, runtime observation, paper simulation, trading, order placement, autonomy, production behavior, or any other later-stage capability.

## 5. Static loader/validator implementation boundary

The boundary is closed around static fixture validation. The loader accepts explicit caller-supplied paths and an explicit repository root, verifies that the target resolves inside an allowlisted fixture directory, reads JSON text, builds Stage 2 metadata from the existing fixture dictionary, validates it with the existing metadata validator, and fails closed when the observed validation posture diverges from the fixture's expected posture.

## 6. Implemented source module

The implemented module is `meg/weather/stage2/historical_label_loader.py`. It uses Python standard library modules plus the existing `meg.weather.stage2.historical_label` validator. It performs no file writes, no external calls, no environment lookup, and no repository auto-discovery beyond the explicit `repo_root` supplied by the caller.

## 7. Implemented public API

The public API is intentionally minimal:

- `ALLOWED_FIXTURE_DIRECTORY_PARTS`
- `FixtureLoadError`
- `LoadedHistoricalLabelFixture`
- `load_historical_label_fixture(path, *, repo_root)`
- `load_historical_label_fixture_directory(directory, *, repo_root)`

The loaded dataclass carries the resolved path, fixture identity, synthetic-or-real classification, expected validation posture, raw fixture mapping, adapted `HistoricalLabelMetadata`, and `ValidationResult`.

## 8. Allowlisted fixture directories

Only these repository-relative directories are allowlisted:

- `tests/fixtures/weather/stage2_historical_labels/`
- `tests/fixtures/weather/stage2_real_source_backed_labels/`

The single-fixture loader requires a `.json` file that resolves under one of those directories. The directory loader requires the directory itself to be exactly one of those two directories and does not recurse.

## 9. Fail-closed behavior

The loader fails closed for:

- paths outside the allowlisted fixture directories;
- missing files;
- non-JSON suffixes;
- malformed JSON;
- non-object JSON roots;
- missing required fields;
- unexpected `synthetic_or_real` values;
- unexpected `expected_validation_posture` values;
- metadata adaptation failures;
- mismatch between expected and observed validation posture;
- non-allowlisted directories;
- allowlisted directories with no JSON files.

## 10. Synthetic fixture handling

Synthetic fixture handling is limited to the three existing JSON files under `tests/fixtures/weather/stage2_historical_labels/`. The loader does not create, update, expand, infer, or collect synthetic fixture content. It only validates the supplied fixture dictionaries against the Stage 2 metadata skeleton.

## 11. Real source-backed fixture handling

Real source-backed fixture handling is limited to the two existing JSON files under `tests/fixtures/weather/stage2_real_source_backed_labels/`. The loader does not fetch source pages, re-adjudicate venue rules, pull provider data, or create additional real historical-label examples.

## 12. Validation posture mapping

The observed posture is mapped as follows:

- if `ValidationResult.passed` is true, the observed posture is `pass`;
- otherwise the observed posture is `ValidationResult.severity.value`.

The observed posture must exactly equal `expected_validation_posture`, which is limited to `pass`, `blocked`, or `caution`.

## 13. Relationship to Stage 2 metadata validator

The loader reuses `historical_label_metadata_from_mapping` and `validate_historical_label_metadata` from `meg/weather/stage2/historical_label.py`. It supplies only the Stage 2 metadata fields needed by that validator: `condition_id`, `token_id`, `outcome`, `source_resolution`, `point_in_time_provenance`, `label_usability`, and `venue_rule_summary`.

## 14. Static validation tests

The static test file is `tests/core/test_prd_p1_wx_stage2_historical_label_loading_implementation_01.py`. It compiles the source module, checks import boundaries, verifies fixture inventories and hashes, loads all synthetic and real source-backed fixtures, checks deterministic sorting, validates expected postures, and verifies fail-closed handling for negative cases.

## 15. Explicit non-approval boundaries

This is static historical-label loading/validation implementation only, and the implementation is limited to explicit static fixture validation.

- no ingestion was created
- no provider/API connectors were created
- no external API calls were created
- no credentials/secrets/config loading was created
- no forecast pulls were created
- no scoring/probability scoring was created
- no backtesting/paper simulation was created
- no runtime observation was created
- no trading/order placement/position sizing/autonomy was created
- no production behavior was created
- no C++/Rust runtime components were created
- no fixture JSON/README files were created or modified
- no historical-label data files or generated data were created

This implementation does not imply ingestion readiness, scoring readiness, runtime readiness, production readiness, or trading readiness.

## 16. What remains unbuilt

The following remain unbuilt: ingestion, source/provider integration, external API access, credential or secret handling, forecast acquisition, scoring, probability scoring, replay systems, simulations, runtime observation, production services, execution paths, order handling, position sizing, and any autonomous behavior.

## 17. Future gates

Future gates preserve that future ingestion requires separate explicit approval, future scoring/backtesting requires separate explicit approval, and future runtime/trading requires separate explicit approval. Any future expansion from fixture validation into data acquisition, evaluation, production behavior, or execution must receive its own planning, approval, implementation, and closeout sequence.

## 18. Acceptance criteria

Acceptance criteria for this ticket:

- the source module exists and compiles;
- the source module uses only the standard library plus the existing Stage 2 metadata validator;
- the loader reads only explicit allowlisted fixture paths;
- all existing synthetic and real source-backed fixtures load with deterministic validation results;
- expected and observed validation postures match;
- negative path, JSON, field, closed-value, and directory cases fail closed;
- no existing fixture JSON or README files are modified;
- static tests document the non-approval boundary.

## 19. Later-ticket handoff

If this ticket is clean, the next appropriate ticket is a historical-label loading/validation implementation closeout/checkpoint. If tests reveal a concrete loader-validation gap, a targeted loader validation refinement may be proposed. The handoff must not recommend ingestion, scoring, backtesting, runtime, trading, or production work as the default next step.

