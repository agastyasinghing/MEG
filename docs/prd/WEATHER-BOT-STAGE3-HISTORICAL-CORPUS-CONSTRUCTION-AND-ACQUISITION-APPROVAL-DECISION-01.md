# WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-DECISION-01

## Status and scope

This is a decision-only, docs/static-test-only artifact. It records the independently reviewed project decision and changes no implementation or evidence-readiness finding. It does not fetch or acquire data, create a corpus or storage, call an API, scrape, download files, use credentials, select providers, create connectors, or execute Stage 3 scoring.

## Immediate predecessor and merge verification

The immediate predecessor is PR #387 at actual merge SHA `6901845cfea86670b1b7fed82fa2db976fbfa627`. Verification requires that SHA to equal `HEAD` or be an ancestor of `HEAD`; neither `origin/main` nor a local `main` branch is required.

## Decision basis

Stage 3's contract and validation chain exists, but evidence execution is blocked by corpus insufficiency. The repository has exactly five Stage 2 examples: 3 synthetic and 2 real source-backed. Coverage is not established, strict-OOS feasibility is not demonstrated, sample sufficiency is not established, and meaningful Stage 3 scoring is not ready.

PR #385 defined fail-closed corpus-readiness requirements. PR #387 then defined a narrow historical/offline request that separates acquisition from live runtime, preserves point-in-time/no-lookahead requirements, grants no generic API or scraping permission, leaves exact providers, source families, endpoints, access methods, credentials, and storage to a later contract, and leaves scoring, runtime, and trading unapproved. Approval therefore advances the corpus lane; it is not evidence that a corpus exists or Stage 3 has passed.

## Selected decision

The source request's complete closed decision set was exactly:

- `approve_narrow_historical_corpus_construction_and_acquisition`
- `request_approval_request_revision`
- `hold`
- `block`

The selected decision is exactly `approve_narrow_historical_corpus_construction_and_acquisition`. No hybrid or custom decision is selected.

## Decision effect

The narrow historical corpus path and narrow historical acquisition path are approved only to proceed to implementation planning. This decision does not approve arbitrary acquisition, a provider, an API endpoint, credentials, scraping, live-provider runtime, or construction execution. It grants no data-movement or execution authority. Before any data movement, the subsequent plan must select and freeze exact source, access, and storage boundaries. Unknown requirements fail closed.

## Approved future path

A later narrow implementation plan may define only: historical market and venue-rule collection; official resolver/source historical evidence; station/observation-point metadata; historical resolution-label construction; archive/finality layers; publication and availability timestamps; required historical forecast/model inputs; point-in-time provenance; source/station-selection provenance; trap/reviewer/adjudication evidence; `usable`, `blocked`, or `excluded` dispositions; corpus manifest/audit metadata; offline validation; and coverage/support reporting. Every item remains future implementation-plan scope and none is performed by this ticket.

## Historical/offline acquisition boundary

Historical/offline work remains separate from live provider integration. This artifact does not acquire, fetch, download, or construct anything and is not generic permission for APIs, scraping, credentials, connectors, or data movement. Exact providers, source families, endpoints, access methods, credentials, and storage boundaries must be proposed and frozen in the later plan.

## Access-method posture

PR #387's consideration set remains exactly:

- `manual_source_review`
- `static_public_reference`
- `offline_public_file_acquisition`
- `offline_public_api_acquisition`
- `source_specific_credentials_required`
- `scraping_requires_separate_approval`
- `live_runtime_provider_requires_separate_approval`

No access method in this set is individually authorized by this decision. The next plan must identify each specific proposed method. Scraping and live runtime providers continue to require separate approval. Source-specific credentials cannot be used until explicitly defined and approved in the later contract.

## Point-in-time/no-lookahead requirements

The approval is conditional on preserving fail-closed point-in-time behavior. A later implementation must not substitute final archives into earlier as-of views, use future revisions before availability, expose labels before legitimate resolution availability, use future forecasts, choose a station/source/rule interpretation with hindsight, select corpus membership based on test outcomes, replace unavailable historical evidence with modern values, or silently mix archive/finality layers. Observation/event time and publication/availability time must remain distinct.

## Storage/artifact posture

This decision selects no storage path, file format, database, dataset size, or Git-commit policy for corpus data. The later plan must decide raw evidence, normalized corpus, and provenance/manifest storage; repository/artifact-size policy; reproducibility; immutable/versioned corrections; and treatment of large external source artifacts. Large datasets are not authorized for Git by default.

## Current corpus/evidence posture

The current corpus remains `five_static_stage2_examples_only`: exactly 3 synthetic examples and 2 real source-backed examples. These five examples remain examples only and are not promoted into a historical corpus. Corpus coverage is `not_established`, sample sufficiency is `not_established`, strict-OOS feasibility is `not_demonstrated`, and Stage 3 scoring readiness is `not_ready`. This decision approves a path for addressing the blocker; it does not resolve the blocker.

## Explicit non-approvals

Still not approved are live provider runtime integration; live weather observation; production connectors; scheduler/service/worker behavior; continuous ingestion; runtime polling; arbitrary scraping or API access; unreviewed credentials/config; model training; probability generation; split or baseline execution; score computation; calibration/diagnostic or evaluation execution; result or claim generation; evidence-gate execution/passage; paper simulation; trading; order placement; production runtime; and autonomy.

## Stage 3 / Stage 4 separation

This decision does not execute Stage 3 scoring or establish Stage 3 readiness or passage. Stage 4 remains separate and not approved. Runtime, paper simulation, trading, order placement, production, and autonomy remain outside this decision.

## Canonical routing posture

Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`. The legacy `market_id` remains non-routing only. `token_outcome_pair` remains derived only. No alternate routing identity is introduced.

## Recommended next ticket

The exactly one recommended successor is `WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-IMPLEMENTATION-PLAN-01`. It should define exact source families, access methods, corpus/storage design, the first acquisition slice, reproducibility requirements, and implementation file boundaries without assuming arbitrary provider, API, or scraping authority.

## Machine-checkable assignments

```text
ticket_id: WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-DECISION-01
immediate_predecessor_pr: pr_387
actual_merge_sha: 6901845cfea86670b1b7fed82fa2db976fbfa627
artifact_scope: docs_static_test_only
decision_artifact_posture: decision_only
decision_status: decision_recorded
decision_option: approve_narrow_historical_corpus_construction_and_acquisition
decision_option: request_approval_request_revision
decision_option: hold
decision_option: block
selected_decision: approve_narrow_historical_corpus_construction_and_acquisition
historical_corpus_path: approved_for_narrow_implementation_planning
historical_acquisition_path: approved_for_narrow_implementation_planning
execution_authority: not_granted_by_decision_artifact
access_method_authority: none_individually_approved
live_provider_runtime_authority: not_approved
current_corpus: five_static_stage2_examples_only
synthetic_example_count: 3
real_source_backed_example_count: 2
corpus_coverage: not_established
sample_sufficiency: not_established
strict_oos_feasibility: not_demonstrated
stage3_scoring_readiness: not_ready
storage_path: not_selected
file_format: not_selected
database: not_selected
dataset_size: not_selected
canonical_routing_field: condition_id
canonical_routing_field: token_id
canonical_routing_field: outcome
non_routing_legacy_identifier: market_id
derived_identifier: token_outcome_pair
recommended_next_ticket: WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-IMPLEMENTATION-PLAN-01
```

## Acceptance criteria

- PR #387 and its actual merge SHA are exact, and the artifact remains decision-only and docs/static-test-only.
- The complete four-value source decision set is preserved and exactly the approved value is selected without a hybrid.
- Only narrow implementation planning paths open; acquisition, construction, and every access method remain unauthorized here.
- The five-example baseline and unresolved coverage, sufficiency, strict-OOS, and scoring findings remain frozen.
- Point-in-time/no-lookahead and unresolved storage/artifact boundaries remain fail closed.
- Stage 4, live runtime, execution, trading, production, and autonomy remain unapproved.
- Canonical routing remains exactly the three declared fields; the legacy identifier is non-routing and the pair is derived.
- Exactly one successor is recommended: the narrow implementation-plan ticket.
