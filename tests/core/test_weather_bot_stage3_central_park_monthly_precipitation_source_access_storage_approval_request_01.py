"""Static oracle for the blocked Central Park precipitation approval request."""

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/prd/WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01.md"
TEXT = DOC.read_text(encoding="utf-8")

HEADINGS = [
    "Status and scope", "Immediate predecessor and actual merge verification",
    "Current first-slice state", "Research method and source-quality standard",
    "Verified venue rule/source", "Venue resolution/finality evidence",
    "Archive-equivalence analysis", "Station identity analysis",
    "Revision/finality analysis", "Point-in-time and label-availability analysis",
    "Polymarket historical-evidence mechanism", "NOAA/NWS/NCEI access-method analysis",
    "Authentication/rate/access posture", "Terms/attribution/retention posture",
    "Proposed exact source-role matrix", "Proposed exact access-method matrix",
    "Proposed storage posture", "Reproducibility/checksum posture",
    "Requested future implementation scope", "Remaining blockers", "Human decision options",
    "Current approval posture", "Explicit non-approvals", "Canonical routing posture",
    "Recommended next ticket", "Machine-checkable assignments", "Acceptance criteria",
]
EXPECTED = [
    "ticket_id: WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-REQUEST-01",
    "immediate_predecessor_pr: pr_389",
    "actual_merge_sha: 9073a25cbdce9ba7c67508ee234cfa4d969d9edf",
    "artifact_scope: docs_static_test_only", "request_posture: request_only",
    "approval_decision_posture: approval_decision_not_recorded",
    "selected_first_slice: polymarket_central_park_nyc_calendar_month_total_precipitation_range_contracts_using_noaa_finalized_monthly_summarized_central_park_figure",
    "venue_source_verification_status: blocked_current_first_party_exact_workflow_not_reverified",
    "venue_settlement_source_role: exact_rule_named_noaa_finalized_monthly_summarized_central_park_precipitation_figure",
    "venue_finality_posture: blocked_exact_source_finalization_and_revision_rule_not_reverified",
    "archive_source_role: none_selected_official_candidates_not_proven_equivalent",
    "archive_equivalence_posture: blocked_fail_closed",
    "station_identity_posture: blocked_no_authoritative_product_specific_identifier_frozen",
    "polymarket_rule_evidence_posture: manual_source_review",
    "polymarket_resolution_evidence_posture: manual_source_review",
    "observation_access_method: unresolved", "station_metadata_access_method: manual_source_review",
    "publication_availability_posture: blocked_historical_reconstructability_not_verified",
    "revision_finality_posture: blocked_historical_venue_relevant_state_not_verified",
    "authentication_posture: no_credentials_proposed_exact_external_method_requirements_undocumented",
    "terms_storage_posture: blocked_product_specific_retention_redistribution_attribution_not_verified",
    "raw_storage_posture: requested_future_external_artifact_root_immutable_sha256_content_addressed_no_overwrite",
    "normalized_storage_posture: requested_future_external_artifact_root_versioned_parquet_schema_and_parser_versioned",
    "manifest_storage_posture: requested_future_external_artifact_root_append_only_all_dispositions_and_lineage",
    "git_large_data_posture: prohibited",
    "point_in_time_posture: distinct_semantic_clocks_missing_evidence_blocks_no_inference",
    "label_availability_posture: train_calibration_available_by_fold_cutoff_test_unavailable_by_fold_cutoff_later_scoring_only",
    "historical_truth_posture: later_archive_revision_or_finality_evidence_never_projects_backward_or_rewrites_venue_settlement",
    "source_use_authority: not_approved", "data_acquisition_authority: not_approved",
    "storage_write_authority: not_approved", "credential_use_authority: not_approved",
    "scraping_authority: not_approved", "live_provider_runtime_authority: not_approved",
    "stage3_scoring_readiness: not_ready",
    "human_decision_option: approve_central_park_monthly_precipitation_source_access_storage",
    "human_decision_option: request_approval_request_revision", "human_decision_option: hold",
    "human_decision_option: block", "human_decision_selection: none",
    "canonical_routing_field: condition_id", "canonical_routing_field: token_id",
    "canonical_routing_field: outcome", "non_routing_legacy_identifier: market_id",
    "derived_identifier: token_outcome_pair",
    "recommended_next_ticket: none_blocked_pending_core_external_evidence",
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


def test_exact_path_headings_and_complete_ordered_assignments() -> None:
    assert DOC.is_file()
    assert re.findall(r"^## (.+)$", TEXT, re.MULTILINE) == HEADINGS
    assert LINES == EXPECTED
    assert values("actual_merge_sha") == ["9073a25cbdce9ba7c67508ee234cfa4d969d9edf"]
    predecessor = section("Immediate predecessor and actual merge verification", "Current first-slice state")
    assert "b0b1f46a2c3080b0b1cbd167571903dc849c82a8" in predecessor
    assert "parents are `62bbeadbfee3707fac316e9eab7f0ca20d254b48` and the reviewed head" in predecessor


def test_family_roles_equivalence_station_and_access_fail_closed() -> None:
    assert values("selected_first_slice") == ["polymarket_central_park_nyc_calendar_month_total_precipitation_range_contracts_using_noaa_finalized_monthly_summarized_central_park_figure"]
    assert values("venue_settlement_source_role") != values("archive_source_role")
    assert values("archive_equivalence_posture") == ["blocked_fail_closed"]
    assert values("station_identity_posture")[0].startswith("blocked_")
    assert values("observation_access_method") == ["unresolved"]
    assert values("station_metadata_access_method") == ["manual_source_review"]
    assert values("polymarket_rule_evidence_posture") == ["manual_source_review"]
    assert values("polymarket_resolution_evidence_posture") == ["manual_source_review"]
    roles = section("Proposed exact source-role matrix", "Proposed exact access-method matrix")
    assert all(role in roles for role in ("Venue market/rule", "Venue resolution", "Meteorological settlement", "Historical archive"))


def test_terms_storage_authority_and_no_decision() -> None:
    assert values("terms_storage_posture")[0].startswith("blocked_")
    assert values("git_large_data_posture") == ["prohibited"]
    assert "separately configured external artifact root" in section("Proposed storage posture", "Reproducibility/checksum posture")
    for key in ("source_use_authority", "data_acquisition_authority", "storage_write_authority",
                "credential_use_authority", "scraping_authority", "live_provider_runtime_authority"):
        assert values(key) == ["not_approved"]
    assert values("stage3_scoring_readiness") == ["not_ready"]
    assert values("human_decision_option") == [
        "approve_central_park_monthly_precipitation_source_access_storage",
        "request_approval_request_revision", "hold", "block",
    ]
    assert values("human_decision_selection") == ["none"]


def test_point_in_time_contract_and_canonical_routing() -> None:
    timing = section("Point-in-time and label-availability analysis", "Polymarket historical-evidence mechanism")
    for clock in ("prediction_as_of", "input_publication_available_at", "fold_cutoff", "source_published_at",
                  "source_available_at", "label_available_at", "venue_resolution_proposed_at",
                  "venue_resolution_final_at", "archive_revised_at", "source_final_at", "acquired_at"):
        assert clock in timing
    assert "`input_publication_available_at <= prediction_as_of`" in timing
    assert "`label_available_at <= fold_cutoff`" in timing
    assert "Test labels must not be available by `fold_cutoff`" in timing
    assert "later legitimate test labels" in timing
    finality = section("Revision/finality analysis", "Point-in-time and label-availability analysis")
    assert "must never be projected backward" in finality
    assert "cannot rewrite settlement" in finality
    assert values("historical_truth_posture") == [
        "later_archive_revision_or_finality_evidence_never_projects_backward_or_rewrites_venue_settlement"
    ]
    assert values("canonical_routing_field") == ["condition_id", "token_id", "outcome"]
    assert values("non_routing_legacy_identifier") == ["market_id"]
    assert values("derived_identifier") == ["token_outcome_pair"]


def test_blocked_request_has_exactly_no_successor() -> None:
    assert values("recommended_next_ticket") == ["none_blocked_pending_core_external_evidence"]
    successor = section("Recommended next ticket", "Machine-checkable assignments")
    decision_ticket = "WEATHER-BOT-STAGE3-CENTRAL-PARK-MONTHLY-PRECIPITATION-SOURCE-ACCESS-STORAGE-APPROVAL-DECISION-01"
    assert decision_ticket not in successor
    assert "None." in successor and "BLOCKED" in successor


def test_access_vocabulary_is_closed_and_exact_methods_are_fail_closed() -> None:
    allowed = {
        "manual_source_review", "static_public_reference", "offline_public_file_acquisition",
        "offline_public_api_acquisition", "source_specific_credentials_required",
        "scraping_requires_separate_approval", "live_runtime_provider_requires_separate_approval",
    }
    access = section("Proposed exact access-method matrix", "Proposed storage posture")
    observed = set(re.findall(r"`([a-z_]+)`", access))
    assert observed == allowed
    assert values("observation_access_method") == ["unresolved"]
    assert values("station_metadata_access_method") == ["manual_source_review"]
    assert "Generic NOAA, API, or file permission is not requested" in section(
        "NOAA/NWS/NCEI access-method analysis", "Authentication/rate/access posture"
    )


def test_oracle_has_no_forbidden_runtime_introspection() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".", 1)[0])
    assert imports == {"ast", "re", "pathlib"}
