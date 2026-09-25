"""Static oracle for the Stage 3 historical-corpus implementation plan."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/prd/WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-IMPLEMENTATION-PLAN-01.md"
TEXT = DOC.read_text(encoding="utf-8")

HEADINGS = [
    "Status and scope", "Immediate predecessor and actual merge verification",
    "Decision authority inherited from #388", "Current blocker/state", "Research findings",
    "Candidate first-slice comparison", "Selected first acquisition slice", "Source-role matrix",
    "Access-method matrix", "Source-specific unresolved blockers", "Corpus storage/data-plane design",
    "Raw/normalized/manifest boundaries", "Point-in-time timestamp contract",
    "Archive/revision/finality contract", "Corpus record/disposition design",
    "Reproducibility/checksum/versioning design", "First implementation file/scope boundary",
    "Validation/reconciliation plan", "Security/terms posture", "Sample-sufficiency separation",
    "Explicit non-approvals", "Stage 3 / Stage 4 separation", "Canonical routing posture",
    "Recommended next ticket", "Machine-checkable assignments", "Acceptance criteria",
]
EXPECTED = [
    "ticket_id: WEATHER-BOT-STAGE3-HISTORICAL-CORPUS-CONSTRUCTION-AND-ACQUISITION-IMPLEMENTATION-PLAN-01",
    "immediate_predecessor_pr: pr_388",
    "actual_merge_sha: 62bbeadbfee3707fac316e9eab7f0ca20d254b48",
    "artifact_scope: docs_static_test_only",
    "plan_posture: implementation_contract_only_no_execution",
    "approved_path_source: pr_388_narrow_implementation_planning_only",
    "current_corpus: five_static_stage2_examples_only",
    "corpus_coverage: not_established", "sample_sufficiency: not_established",
    "strict_oos_feasibility: not_demonstrated", "stage3_scoring_readiness: not_ready",
    "selected_first_slice: polymarket_central_park_nyc_calendar_month_total_precipitation_range_contracts_naming_noaa_ncei_finalized_monthly_summary",
    "venue_source_role: polymarket_contemporaneous_contract_rules_and_resolution_evidence",
    "settlement_source_role: polymarket_resolver_proposal_dispute_and_final_outcome_evidence",
    "archive_source_role: exact_noaa_ncei_monthly_summary_product_and_central_park_station_mapping_unresolved_fail_closed",
    "forecast_source_role: not_applicable_first_slice",
    "polymarket_access_posture: manual_source_review",
    "polymarket_access_posture: static_public_reference",
    "noaa_observation_access_posture: manual_source_review",
    "noaa_station_access_posture: static_public_reference",
    "credential_access_posture: source_specific_credentials_required",
    "scraping_access_posture: scraping_requires_separate_approval",
    "live_provider_access_posture: live_runtime_provider_requires_separate_approval",
    "publication_availability_access_posture: manual_source_review",
    "revision_finality_access_posture: manual_source_review",
    "reviewer_access_posture: manual_source_review",
    "observation_acquisition_method_selection: blocked_pending_source_access_storage_approval",
    "consideration_access_posture: manual_source_review",
    "consideration_access_posture: static_public_reference",
    "consideration_access_posture: offline_public_file_acquisition",
    "consideration_access_posture: offline_public_api_acquisition",
    "consideration_access_posture: source_specific_credentials_required",
    "consideration_access_posture: scraping_requires_separate_approval",
    "consideration_access_posture: live_runtime_provider_requires_separate_approval",
    "raw_storage_posture: immutable_content_addressed_external_artifacts_with_sha256_no_destructive_overwrite",
    "normalized_storage_posture: versioned_parquet_silver_records_for_duckdb_research_queries",
    "manifest_storage_posture: append_only_jsonl_or_parquet_audit_manifest_all_dispositions",
    "research_gold_posture: not_created_without_separate_approval",
    "git_large_data_posture: prohibited_only_tiny_deterministic_license_cleared_fixtures_allowed",
    "correction_posture: append_new_versions_preserve_as_of_views_link_supersession_no_overwrite",
    "point_in_time_missing_evidence_posture: blocked_missing_point_in_time_evidence",
    "record_dispositions: usable_blocked_excluded_all_reconciled",
    "primary_sample_roles: train_calibration_test",
    "acquisition_execution_authority: not_approved", "scraping_authority: not_approved",
    "live_provider_runtime_authority: not_approved",
    "canonical_routing_field: condition_id", "canonical_routing_field: token_id",
    "canonical_routing_field: outcome", "non_routing_legacy_identifier: market_id",
    "derived_identifier: token_outcome_pair",
    "recommended_next_ticket: WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01",
]


def section(name: str, following: str) -> str:
    return TEXT.split(f"## {name}\n", 1)[1].split(f"## {following}\n", 1)[0]


MACHINE_SECTION = section("Machine-checkable assignments", "Acceptance criteria")
MATCH = re.fullmatch(r"\n```text\n(?P<body>[^`]*)```\n\n", MACHINE_SECTION)
assert MATCH is not None
MACHINE = MATCH.group("body")
LINES = MACHINE.splitlines()


def values(key: str) -> list[str]:
    return re.findall(rf"^{re.escape(key)}: (\S+)$", MACHINE, re.MULTILINE)


def test_exact_heading_order_and_complete_machine_block() -> None:
    assert re.findall(r"^## (.+)$", TEXT, re.MULTILINE) == HEADINGS
    assert LINES == EXPECTED
    assert values("actual_merge_sha") == ["62bbeadbfee3707fac316e9eab7f0ca20d254b48"]


def test_selected_slice_roles_and_access_are_frozen() -> None:
    assert values("selected_first_slice") == [
        "polymarket_central_park_nyc_calendar_month_total_precipitation_range_contracts_naming_noaa_ncei_finalized_monthly_summary"
    ]
    assert values("forecast_source_role") == ["not_applicable_first_slice"]
    assert values("polymarket_access_posture") == ["manual_source_review", "static_public_reference"]
    assert values("noaa_observation_access_posture") == ["manual_source_review"]
    assert values("observation_acquisition_method_selection") == [
        "blocked_pending_source_access_storage_approval"
    ]
    for method in ("manual_source_review", "static_public_reference", "offline_public_file_acquisition",
                   "offline_public_api_acquisition", "source_specific_credentials_required",
                   "scraping_requires_separate_approval", "live_runtime_provider_requires_separate_approval"):
        assert method in section("Access-method matrix", "Source-specific unresolved blockers")


def test_external_unknowns_are_blocked_and_acquisition_unapproved() -> None:
    assert values("publication_availability_access_posture") == ["manual_source_review"]
    assert values("revision_finality_access_posture") == ["manual_source_review"]
    assert values("acquisition_execution_authority") == ["not_approved"]
    assert values("scraping_authority") == ["not_approved"]
    assert values("live_provider_runtime_authority") == ["not_approved"]
    assert values("consideration_access_posture") == [
        "manual_source_review", "static_public_reference", "offline_public_file_acquisition",
        "offline_public_api_acquisition", "source_specific_credentials_required",
        "scraping_requires_separate_approval", "live_runtime_provider_requires_separate_approval",
    ]
    blockers = section("Source-specific unresolved blockers", "Corpus storage/data-plane design")
    for item in ("exact venue-defined NOAA/NCEI product", "first-posted", "historical Polymarket",
                 "attribution", "redistribution", "source-specific and storage approval"):
        assert item in blockers
    for forbidden in ("actual acquisition", "API calls", "downloads", "scraping", "credentials/secrets",
                      "scoring/diagnostics/evaluation", "Stage 4", "trading", "autonomy"):
        assert forbidden in section("Explicit non-approvals", "Stage 3 / Stage 4 separation")


def test_storage_corrections_and_disposition_accounting() -> None:
    assert values("raw_storage_posture") == ["immutable_content_addressed_external_artifacts_with_sha256_no_destructive_overwrite"]
    assert values("normalized_storage_posture") == ["versioned_parquet_silver_records_for_duckdb_research_queries"]
    assert values("manifest_storage_posture") == ["append_only_jsonl_or_parquet_audit_manifest_all_dispositions"]
    assert values("correction_posture") == ["append_new_versions_preserve_as_of_views_link_supersession_no_overwrite"]
    assert values("record_dispositions") == ["usable_blocked_excluded_all_reconciled"]
    disposition = section("Corpus record/disposition design", "Reproducibility/checksum/versioning design")
    assert "candidate totals not" not in disposition
    assert "Blocked/excluded candidates remain auditable" in disposition


def test_semantic_clocks_and_no_lookahead_are_distinct() -> None:
    clock_section = section("Point-in-time timestamp contract", "Archive/revision/finality contract")
    clocks = ["market_event_start_at", "market_close_at", "evaluation_cutoff_at", "observation_valid_at",
              "source_published_at", "source_available_at", "forecast_initialized_at",
              "forecast_published_at", "forecast_available_at", "venue_resolution_proposed_at",
              "venue_resolution_final_at", "archive_revised_at", "source_final_at", "acquired_at",
              "station_source_selected_at", "reviewed_at"]
    assert all(clock in clock_section for clock in clocks)
    assert "No timestamp substitutes for another" in clock_section
    assert "source_available_at <= evaluation_cutoff_at" in clock_section
    assert values("point_in_time_missing_evidence_posture") == ["blocked_missing_point_in_time_evidence"]
    archive = section("Archive/revision/finality contract", "Corpus record/disposition design")
    assert all(layer in archive for layer in ("first_posted", "preliminary", "revised", "final", "superseded"))


def test_sample_separation_canonical_routing_and_one_successor() -> None:
    assert values("sample_sufficiency") == ["not_established"]
    assert values("primary_sample_roles") == ["train_calibration_test"]
    sample = section("Sample-sufficiency separation", "Explicit non-approvals")
    assert "No universal sample N" in sample and "test outcomes cannot drive corpus membership" in sample
    assert "sparse strata cannot be silently pooled" in sample
    assert values("canonical_routing_field") == ["condition_id", "token_id", "outcome"]
    assert values("non_routing_legacy_identifier") == ["market_id"]
    assert values("derived_identifier") == ["token_outcome_pair"]
    successors = values("recommended_next_ticket")
    assert successors == ["WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01"]
    successor_section = section("Recommended next ticket", "Machine-checkable assignments")
    assert successor_section.count("**WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01**") == 1
