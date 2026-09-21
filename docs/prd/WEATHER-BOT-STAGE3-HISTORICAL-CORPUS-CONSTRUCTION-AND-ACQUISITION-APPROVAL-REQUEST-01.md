# WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-REQUEST-01

## Status and scope

This is an approval-request-only, docs/static-test-only artifact. It requests a human decision about a possible later, separately bounded historical-corpus implementation ticket. It is not the approval decision, does not authorize implementation, and does not acquire, download, fetch, scrape, generate, create, or expand data. No corpus pipeline is implemented.

## Immediate predecessor and merge verification

The required immediate predecessor is PR #385 at actual merge commit `dc52bb3c3e2241880a3d1bb850c755804740810f`. A checkout must verify that this commit is `HEAD` or an ancestor of `HEAD`; neither `origin/main` nor a local `main` branch is required.

## Current corpus/readiness state

The baseline remains exactly five Stage 2 static weather JSON examples: exactly 3 synthetic historical-label examples and exactly 2 real source-backed examples. They are examples only and are not promoted into a historical corpus. Corpus coverage is not established, strict-OOS feasibility is not demonstrated, sample sufficiency is not established, and Stage 3 scoring is not ready.

## Approval-request purpose

This request asks a human to decide whether a later, separately authorized ticket may construct and acquire a source-compatible, point-in-time historical corpus for Stage 3 evidence. It defines a narrow future permission boundary only. Until an explicit decision is recorded in a later approval-decision artifact, construction and acquisition remain blocked and not approved.

## Requested future corpus scope

Subject both to the later human decision and to a subsequent implementation contract, the requested future capabilities are limited to historical/offline work needed for declared Stage 3 evidence:

1. historical market and venue-rule collection;
2. official resolver/source historical evidence collection;
3. station or observation-point metadata collection;
4. historical resolution-label construction;
5. first-posted, preliminary, revised, and final archive-layer preservation;
6. publication and availability timestamp capture;
7. historical forecast/model input collection where needed for a declared Stage 3 evaluation;
8. point-in-time provenance capture;
9. station/source-selection provenance;
10. trap/reviewer/adjudication evidence;
11. `usable`, `blocked`, or `excluded` dispositioning;
12. corpus manifest and audit metadata;
13. offline corpus validation; and
14. corpus coverage/support reporting.

Every item above is a requested future capability only. None is performed or authorized now.

## Historical/offline acquisition boundary

Historical/offline acquisition is distinct from live runtime provider integration. Generic permission to construct a corpus would not grant permission to call arbitrary APIs, scrape arbitrary sites, or use an unreviewed access mechanism. A later implementation may use only access methods expressly allowed by the later human decision and subsequent implementation contract. Unknown source or access requirements fail closed to later review. This request invents no provider, endpoint, API key, credential, or storage path and grants no acquisition execution authority.

## Source/evidence requirements

Every future acquired record intended for the corpus must remain tied to venue-defined settlement truth. Where applicable, future evidence must preserve:

- `condition_id`, `token_id`, and `outcome`;
- historical contract/rule identity and the rule version effective at the relevant time;
- market family and resolver/source identity;
- station, observation point, or authority;
- measurement window, threshold, comparator, unit, and rounding/trace semantics;
- resolution label;
- source publication time and source availability time;
- observation valid time and observation availability time;
- forecast/input publication and availability time;
- archive/revision/finality layer;
- access provenance and station/source-selection provenance;
- trap/adjudication evidence and reviewer evidence; and
- corpus disposition and reason.

These are evidence requirements for a future contract, not a production schema.

## Point-in-time/no-lookahead boundary

A future approved implementation must preserve both observation/event time and legitimate publication/availability time. It must fail closed against final archive information substituted into an earlier as-of view; future revisions used before availability; labels used before legitimate resolution availability; future forecasts; hindsight station selection; hindsight source selection; hindsight rule interpretation; test-outcome-informed corpus inclusion; silently replacing unavailable historical evidence with modern values; and silently collapsing incompatible archive layers.

## Data storage and artifact boundary

This request selects no final storage path, file format, repository-commit policy, database, or dataset size. A later implementation ticket must explicitly decide raw-evidence storage, normalized-corpus storage, provenance/manifest storage, repository size and artifact policy, whether large source files remain external references rather than Git-tracked files, reproducibility requirements, and an immutable/versioned correction posture. Large datasets are not authorized for Git by default.

## Corpus inclusion/exclusion boundary

A future contract must disposition candidates as `usable`, `blocked`, or `excluded`, with reasons and auditable totals. Inclusion may follow only predeclared source compatibility, rule, timing, provenance, and evaluation-population requirements. Eventual test outcomes must not determine which records, stations, years, thresholds, sources, or market families are retained. Missing, ambiguous, incompatible, or unknown evidence fails closed rather than being silently repaired or omitted.

## Sample-support/predeclaration boundary

No universal numeric minimum is selected here. Evaluation-specific sample-support rules must be predeclared before test inspection; sparse or insufficient strata fail closed; pooling rules must be predeclared; and the uncertainty method and interval level must be predeclared. The exact primary split roles are `train`, `calibration`, and `test`. This request executes no split and makes no sufficiency finding.

## Provider/access-method boundary

The closed future access-posture categories presented for approval consideration are exactly:

- `manual_source_review`
- `static_public_reference`
- `offline_public_file_acquisition`
- `offline_public_api_acquisition`
- `source_specific_credentials_required`
- `scraping_requires_separate_approval`
- `live_runtime_provider_requires_separate_approval`

This approval request grants none of these execution authorities. Offline public API acquisition, source-specific credentials, and every other method require explicit later authorization. Scraping requires separate approval, and a live runtime provider requires separate approval; historical/offline corpus permission cannot be interpreted as live-source runtime approval.

## Explicit non-approvals

This request does not request or approve live provider runtime integration, live weather observation, production connectors, scheduler/service/worker behavior, continuous ingestion, runtime source polling, arbitrary scraping, arbitrary API access, unreviewed credential/config loading, model training, probability generation, split execution, baseline execution, Brier/log/CRPS/twCRPS computation, calibration/diagnostic execution, evaluation execution, result generation, claim generation, evidence-gate execution or passage, backtesting or paper simulation, trading, order placement, production runtime, or autonomy. Stage 4 remains separate and unapproved. It creates no implementation or data files.

## Human decision options

The closed set of future human decision options is exactly:

- `approve_narrow_historical_corpus_construction_and_acquisition`
- `request_approval_request_revision`
- `hold`
- `block`

This document does not select an option.

## Current request status

The current posture is `approval_decision_not_recorded`. Corpus construction authority, data acquisition authority, and live-provider runtime authority are each `not_approved`. Implementation and acquisition remain blocked pending an explicit human selection recorded in the later approval-decision artifact.

## Human approval requirement

Only a human may choose one of the four decision options in the later decision artifact. Even an approval would authorize no work in this document: implementation would require its own subsequent, narrowly bounded contract specifying allowed sources and access methods. Silence, ambiguity, and unknown requirements fail closed.

## Canonical routing posture

Canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`. The legacy `market_id` identifier is non-routing only. `token_outcome_pair` is derived only. Historical contract metadata is evidence, not an alternate routing identity, and no alternate routing identity is introduced.

## Recommended next ticket

The exactly one recommended successor is `WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-DECISION-01`. That artifact records the human decision. Corpus implementation must not be recommended until a decision is explicitly recorded.

## Machine-checkable assignments

```text
ticket_id: WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-REQUEST-01
immediate_predecessor_pr: pr_385
actual_merge_sha: dc52bb3c3e2241880a3d1bb850c755804740810f
artifact_scope: docs_static_test_only
request_posture: approval_request_only
approval_decision_posture: approval_decision_not_recorded
current_corpus: five_static_stage2_examples_only
synthetic_example_count: 3
real_source_backed_example_count: 2
corpus_coverage: not_established
sample_sufficiency: not_established
strict_oos_feasibility: not_demonstrated
stage3_scoring_readiness: not_ready
corpus_construction_authority: not_approved
data_acquisition_authority: not_approved
live_provider_runtime_authority: not_approved
canonical_routing_field: condition_id
canonical_routing_field: token_id
canonical_routing_field: outcome
non_routing_legacy_identifier: market_id
derived_identifier: token_outcome_pair
decision_option: approve_narrow_historical_corpus_construction_and_acquisition
decision_option: request_approval_request_revision
decision_option: hold
decision_option: block
recommended_next_ticket: WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-APPROVAL-DECISION-01
```

## Acceptance criteria

- The artifact remains approval-request-only and creates neither data nor implementation behavior.
- PR #385 and its actual merge SHA are exact, and the five-example baseline is not promoted.
- Requested future scope, evidence, point-in-time, inclusion, storage, access, and sample-support boundaries remain fail closed.
- Historical/offline acquisition remains distinct from live runtime integration, with no access category authorized here.
- The four exact decision options are presented without selecting one; all three authorities remain not approved.
- Stage 3 scoring, Stage 4, runtime, trading, production, and autonomy remain unapproved.
- Canonical routing is exactly the three declared fields, while the legacy identifier remains non-routing and the pair identifier remains derived.
- Exactly one successor is recommended, and it is the approval-decision artifact rather than implementation.
