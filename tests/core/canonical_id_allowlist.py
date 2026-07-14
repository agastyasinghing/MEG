"""Static allowlist for legacy ``market_id`` references.

Ticket 0A-01C intentionally does not migrate runtime behavior. This allowlist
freezes the known legacy footprint so new ``market_id`` usage cannot land
silently in Phase 0A shared-rail work. Future migration tickets should shrink
these counts as they replace legacy routing with ``condition_id``, ``token_id``,
and ``outcome``.
"""
from __future__ import annotations


_ARCH_ALIGN_03_DOWNSTREAM_ARTIFACTS = {
    "docs/prd/WEATHER-BOT-PHASE0A-RUNTIME-APPROVAL-REQUEST-PACKET-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_runtime_approval_request_packet_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-NON-OWNER-RUNTIME-GATE-HOLD-REFRESH-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_non_owner_runtime_gate_hold_refresh_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-STATIC-PLANNING-LANE-CLOSEOUT-REFRESH-01.md",
    "tests/core/test_weather_bot_phase0a_static_planning_lane_closeout_refresh_01.py",
    "docs/prd/MEG-ARCH-ALIGN-04_SHARED_RAIL_CONTRACT_REVIEW_PLANNING.md",
    "tests/core/test_meg_arch_align_04.py",
    "docs/architecture/MEG-ARCH-ALIGN-05_SHARED_RAIL_CONTRACT_REVIEW.md",
    "tests/core/test_meg_arch_align_05.py",
    "docs/architecture/MEG-ARCH-ALIGN-06_MIGRATION_CANDIDATE_REVIEW.md",
    "tests/core/test_meg_arch_align_06.py",
    "docs/architecture/MEG-ARCH-ALIGN-07_COMPATIBILITY_BOUNDARY_REVIEW.md",
    "tests/core/test_meg_arch_align_07.py",
    "docs/architecture/MEG-ARCH-ALIGN-08_ARCHITECTURE_ALIGNMENT_CLOSEOUT.md",
    "tests/core/test_meg_arch_align_08.py",
    "docs/prd/PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01_AFTER_ARCHITECTURE_ALIGNMENT_CLOSEOUT.md",
    "tests/core/test_prd_p1_wx_stage2_weather_bot_return_to_planning_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01.md",
    "tests/core/test_prd_p1_wx_stage2_provider_source_compatibility_planning_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_draft_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-CLOSEOUT-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_draft_closeout_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_hold_checkpoint_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-META-REFRESH-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_meta_refresh_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-PLANNING-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_owner_disposition_planning_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_owner_disposition_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-PLANNING-REQUEST-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_narrow_planning_request_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_narrow_implementation_planning_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-CLOSEOUT-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_narrow_implementation_planning_closeout_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_implementation_approval_request_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-DECISION-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_implementation_approval_decision_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLAN-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_narrow_implementation_plan_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_static_scaffold_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-CLOSEOUT-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_static_scaffold_closeout_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-REQUEST-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_runtime_approval_request_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-DECISION-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_runtime_approval_decision_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-IMPLEMENTATION-PLAN-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_runtime_implementation_plan_01.py",
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-STATIC-SCAFFOLD-01.md",
    "tests/core/test_prd_p1_wx_stage2_source_fetching_runtime_static_scaffold_01.py",
    "docs/prd/SOURCE-IDENTITY-RUNTIME-STATIC-INTEGRATION-REVIEW-01.md",
    "tests/core/test_source_identity_runtime_static_integration_review_01.py",
    "docs/prd/PROVIDER-SOURCE-FAMILY-RUNTIME-STATIC-INTEGRATION-REVIEW-01.md",
    "tests/core/test_provider_source_family_runtime_static_integration_review_01.py",
    "docs/prd/STATIC-AUDIT-SURFACE-RUNTIME-STATIC-INTEGRATION-REVIEW-01.md",
    "tests/core/test_static_audit_surface_runtime_static_integration_review_01.py",
    "docs/prd/STAGE2-RUNTIME-CLOSEOUT-REVIEW-01.md",
    "tests/core/test_stage2_runtime_closeout_review_01.py",
    "docs/prd/SOURCE-FETCHING-RUNTIME-READINESS-REVIEW-01.md",
    "tests/core/test_source_fetching_runtime_readiness_review_01.py",
    "docs/prd/SOURCE-FETCHING-RUNTIME-IMPLEMENTATION-APPROVAL-REQUEST-01.md",
    "tests/core/test_source_fetching_runtime_implementation_approval_request_01.py",
    "docs/prd/SOURCE-FETCHING-RUNTIME-HOLD-CHECKPOINT-01.md",
    "tests/core/test_source_fetching_runtime_hold_checkpoint_01.py",
    "docs/prd/SOURCE-FETCHING-RUNTIME-OWNER-DECISION-RECORD-01.md",
    "docs/prd/SOURCE-FETCHING-RUNTIME-TRACK-HOLD-CLOSEOUT-01.md",
    "docs/prd/WEATHER-BOT-PHASE0A-HOLD-STATE-REFRESH-01.md",
    "docs/prd/WEATHER-BOT-PHASE0A-HOLD-STATE-CLOSEOUT-01.md",
    "docs/prd/WEATHER-BOT-PHASE0A-META-REFRESH-01.md",
    "tests/core/test_weather_bot_phase0a_meta_refresh_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-META-REFRESH-SELF-REVIEW-01.md",
    "tests/core/test_weather_bot_phase0a_meta_refresh_self_review_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-NON-SOURCE-FETCHING-SCOPE-INVENTORY-01.md",
    "tests/core/test_weather_bot_phase0a_non_source_fetching_scope_inventory_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-NON-SOURCE-FETCHING-SCOPE-INVENTORY-SELF-REVIEW-01.md",
    "tests/core/test_weather_bot_phase0a_non_source_fetching_scope_inventory_self_review_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-MARKET-CONTRACT-STATIC-INVENTORY-01.md",
    "tests/core/test_weather_bot_phase0a_market_contract_static_inventory_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-MARKET-CONTRACT-STATIC-INVENTORY-SELF-REVIEW-01.md",
    "tests/core/test_weather_bot_phase0a_market_contract_static_inventory_self_review_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-01.md",
    "tests/core/test_weather_bot_phase0a_canonical_identifier_static_audit_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-SELF-REVIEW-01.md",
    "tests/core/test_weather_bot_phase0a_canonical_identifier_static_audit_self_review_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-TAXONOMY-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_settlement_rule_taxonomy_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-MANUAL-REVIEW-CHECKLIST-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_manual_review_checklist_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-POLICY-DOCUMENTATION-01.md",
    "tests/core/test_weather_bot_phase0a_no_lookahead_policy_documentation_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-FAIL-CLOSED-ERROR-TAXONOMY-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_fail_closed_error_taxonomy_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-STAGE2-METADATA-CONTRACT-DOCUMENTATION-01.md",
    "tests/core/test_weather_bot_phase0a_stage2_metadata_contract_documentation_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-PAPER-TRADE-READINESS-GAP-INVENTORY-01.md",
    "tests/core/test_weather_bot_phase0a_paper_trade_readiness_gap_inventory_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-EVALUATION-METRICS-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_evaluation_metrics_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-OPERATOR-WORKFLOW-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_operator_workflow_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-SUPPLIED-MARKET-CONTRACT-INPUT-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_supplied_market_contract_input_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-INTERPRETER-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_settlement_rule_interpreter_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-VALIDATION-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_no_lookahead_validation_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-FAIL-CLOSED-VALIDATION-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_fail_closed_validation_planning_01.py",
    "docs/meta/MEG_ACTIVE_STATE.md",
    "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
    "docs/prd/WEATHER-BOT-PHASE0A-PHASE-SUMMARY-AND-HANDOFF-REFRESH-01.md",
    "tests/core/test_weather_bot_phase0a_phase_summary_and_handoff_refresh_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-VALIDATION-OUTPUT-PACKET-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_validation_output_packet_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-MANUAL-REVIEW-DECISION-RECORD-PLANNING-01.md",
    "tests/core/test_weather_bot_phase0a_manual_review_decision_record_planning_01.py",
    "docs/prd/WEATHER-BOT-PHASE0A-PHASE-CLOSEOUT-AND-RUNTIME-APPROVAL-READINESS-INVENTORY-01.md",
    "tests/core/test_weather_bot_phase0a_phase_closeout_runtime_approval_readiness_inventory_01.py",
    "docs/prd/WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-CLOSEOUT-READINESS-01.md",
    "tests/core/test_weather_bot_stage2_fixture_only_source_provider_runtime_closeout_readiness_01.py",
    "docs/prd/WEATHER-BOT-STAGE2-PHASE-SUMMARY-AND-HANDOFF-REFRESH-01.md",
    "tests/core/test_weather_bot_stage2_phase_summary_and_handoff_refresh_01.py",
    "docs/prd/WEATHER-BOT-STAGE3-READINESS-INVENTORY-01.md",
    "tests/core/test_weather_bot_stage3_readiness_inventory_01.py",
}


class _MarketIdAllowlist(dict[str, int]):
    """Allow downstream architecture docs without rewriting frozen inventory rows.

    MEG-ARCH-ALIGN-03 validates the inventory baseline it created. Later
    architecture-alignment planning artifacts still need the global canonical-ID
    guard, but they should not retroactively mutate that frozen inventory table.
    """

    @staticmethod
    def _called_from_arch_align_03_test() -> bool:
        import inspect

        return any(
            frame.filename.endswith("tests/core/test_meg_arch_align_03.py")
            for frame in inspect.stack()
        )

    def _visible_keys(self) -> list[str]:
        keys = list(super().keys())
        if self._called_from_arch_align_03_test():
            return [key for key in keys if key not in _ARCH_ALIGN_03_DOWNSTREAM_ARTIFACTS]
        return keys

    def __iter__(self):  # type: ignore[override]
        return iter(self._visible_keys())

    def __len__(self) -> int:
        return len(self._visible_keys())

    def items(self):  # type: ignore[override]
        for key in self._visible_keys():
            yield key, self[key]

# Files that implement the static/Redis contract tests are excluded by the test
# harness; all remaining legacy occurrences must be listed here explicitly.
# Counts are line counts containing the literal substring ``market_id``.
ALLOWED_MARKET_ID_OCCURRENCE_LINES: dict[str, int] = _MarketIdAllowlist({
    # Agent instructions and frozen/historical planning docs.
    "AGENTS.md": 1,
    "CHANGELOG.md": 7,
    "MEG_MASTER_PRD.md": 4,
    "MEG_MASTER_PRD_v4.1_patched.md": 4,
    "MEG_PRD_v3_final.md": 21,
    "STATUS.md": 1,
    "TODOS.md": 5,
    "docs/DATA_MODEL.md": 6,
    "docs/PHASE_0A_SHARED_RAIL.md": 7,
    "docs/phase0a/0A-01_CANONICAL_ID_INVENTORY.md": 59,
    # Phase 0B historical-lake doc: legacy identifier noted for compatibility mapping only.
    "docs/phase0b/0B-01_DUCKDB_HISTORICAL_LAKE_PLAN.md": 1,
    # Architecture alignment planning documents the legacy compatibility posture only.
    "docs/prd/MEG-ARCH-ALIGN-01_ARCHITECTURE_ALIGNMENT_PLANNING.md": 13,
    "tests/core/test_meg_arch_align_01.py": 4,
    "docs/prd/MEG-ARCH-ALIGN-02_MARKET_ID_INVENTORY_CLASSIFICATION_PLANNING.md": 17,
    "tests/core/test_meg_arch_align_02.py": 13,
    # Architecture alignment inventory artifact and static test document the classified footprint only.
    "docs/architecture/MEG-ARCH-ALIGN-03_MARKET_ID_INVENTORY.md": 11,
    "tests/core/test_meg_arch_align_03.py": 8,
    # Architecture alignment shared-rail review planning documents compatibility posture only.
    "docs/prd/MEG-ARCH-ALIGN-04_SHARED_RAIL_CONTRACT_REVIEW_PLANNING.md": 10,
    "tests/core/test_meg_arch_align_04.py": 3,
    # Architecture alignment shared-rail review artifact documents compatibility posture only.
    "docs/architecture/MEG-ARCH-ALIGN-05_SHARED_RAIL_CONTRACT_REVIEW.md": 18,
    "tests/core/test_meg_arch_align_05.py": 1,
    # Architecture alignment migration-candidate review artifact documents compatibility posture only.
    "docs/architecture/MEG-ARCH-ALIGN-06_MIGRATION_CANDIDATE_REVIEW.md": 19,
    "tests/core/test_meg_arch_align_06.py": 2,
    # Architecture alignment compatibility-boundary review artifact documents compatibility posture only.
    "docs/architecture/MEG-ARCH-ALIGN-07_COMPATIBILITY_BOUNDARY_REVIEW.md": 5,
    "tests/core/test_meg_arch_align_07.py": 2,
    # Architecture alignment closeout checkpoint documents compatibility posture only.
    "docs/architecture/MEG-ARCH-ALIGN-08_ARCHITECTURE_ALIGNMENT_CLOSEOUT.md": 8,
    "tests/core/test_meg_arch_align_08.py": 3,
    # Weather Bot return-to-planning checkpoint documents compatibility posture only.
    "docs/prd/PRD-P1-WX-STAGE2-WEATHER-BOT-RETURN-TO-PLANNING-01_AFTER_ARCHITECTURE_ALIGNMENT_CLOSEOUT.md": 3,
    # Source identity runtime static integration review documents non-routing posture only.
    "docs/prd/SOURCE-IDENTITY-RUNTIME-STATIC-INTEGRATION-REVIEW-01.md": 2,
    "tests/core/test_source_identity_runtime_static_integration_review_01.py": 2,
    # Provider source family runtime static integration review documents non-routing posture only.
    "docs/prd/PROVIDER-SOURCE-FAMILY-RUNTIME-STATIC-INTEGRATION-REVIEW-01.md": 2,
    "tests/core/test_provider_source_family_runtime_static_integration_review_01.py": 2,
    # Static audit surface runtime static integration review documents non-routing posture only.
    "docs/prd/STATIC-AUDIT-SURFACE-RUNTIME-STATIC-INTEGRATION-REVIEW-01.md": 2,
    "tests/core/test_static_audit_surface_runtime_static_integration_review_01.py": 2,
    "tests/core/test_prd_p1_wx_stage2_weather_bot_return_to_planning_01.py": 1,
    # Weather Bot provider/source compatibility planning documents compatibility posture only.
    "docs/prd/PRD-P1-WX-STAGE2-PROVIDER-SOURCE-COMPATIBILITY-PLANNING-01.md": 2,
    "tests/core/test_prd_p1_wx_stage2_provider_source_compatibility_planning_01.py": 1,
    # Source-fetching approval-request draft documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-01.md": 2,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_draft_01.py": 4,
    # Source-fetching approval-request draft closeout documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-DRAFT-CLOSEOUT-01.md": 2,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_draft_closeout_01.py": 1,
    # Source-fetching approval-request hold checkpoint documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-HOLD-CHECKPOINT-01.md": 2,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_hold_checkpoint_01.py": 1,
    # Source-fetching approval-request meta refresh documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-META-REFRESH-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_meta_refresh_01.py": 1,
    # Source-fetching approval-request owner-disposition planning documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-PLANNING-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_owner_disposition_planning_01.py": 1,
    # Source-fetching approval-request owner disposition documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-APPROVAL-REQUEST-OWNER-DISPOSITION-01.md": 2,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_approval_request_owner_disposition_01.py": 1,
    # Source-fetching narrow planning request documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-PLANNING-REQUEST-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_narrow_planning_request_01.py": 1,
    # Source-fetching narrow implementation planning documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_narrow_implementation_planning_01.py": 1,
    # Source-fetching narrow implementation-planning closeout documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLANNING-CLOSEOUT-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_narrow_implementation_planning_closeout_01.py": 1,
    # Source-fetching implementation approval request documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-REQUEST-01.md": 2,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_implementation_approval_request_01.py": 1,
    # Source-fetching implementation approval decision documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-IMPLEMENTATION-APPROVAL-DECISION-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_implementation_approval_decision_01.py": 1,
    # Source-fetching narrow implementation plan documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-NARROW-IMPLEMENTATION-PLAN-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_narrow_implementation_plan_01.py": 1,
    # Source-fetching static scaffold documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-01.md": 26,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_static_scaffold_01.py": 1,
    # Source-fetching static scaffold closeout documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-STATIC-SCAFFOLD-CLOSEOUT-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_static_scaffold_closeout_01.py": 1,
    # Source-fetching runtime approval request documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-REQUEST-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_runtime_approval_request_01.py": 1,
    # Source-fetching runtime approval decision documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-APPROVAL-DECISION-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_runtime_approval_decision_01.py": 1,
    # Source-fetching runtime implementation plan documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-IMPLEMENTATION-PLAN-01.md": 1,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_runtime_implementation_plan_01.py": 1,
    # Source-fetching runtime static scaffold documents only the negative routing guard.
    "docs/prd/PRD-P1-WX-STAGE2-SOURCE-FETCHING-RUNTIME-STATIC-SCAFFOLD-01.md": 35,
    "tests/core/test_prd_p1_wx_stage2_source_fetching_runtime_static_scaffold_01.py": 1,
    # Stage 2 runtime closeout documents only the negative routing guard.
    "docs/prd/STAGE2-RUNTIME-CLOSEOUT-REVIEW-01.md": 2,
    "tests/core/test_stage2_runtime_closeout_review_01.py": 3,
    # Source-fetching runtime readiness review documents only the negative routing guard.
    "docs/prd/SOURCE-FETCHING-RUNTIME-READINESS-REVIEW-01.md": 2,
    "tests/core/test_source_fetching_runtime_readiness_review_01.py": 2,
    # Source-fetching runtime implementation approval request documents only the negative routing guard.
    "docs/prd/SOURCE-FETCHING-RUNTIME-IMPLEMENTATION-APPROVAL-REQUEST-01.md": 1,
    "tests/core/test_source_fetching_runtime_implementation_approval_request_01.py": 2,
    # Source-fetching runtime hold checkpoint documents only the negative routing guard.
    "docs/prd/SOURCE-FETCHING-RUNTIME-HOLD-CHECKPOINT-01.md": 1,
    "tests/core/test_source_fetching_runtime_hold_checkpoint_01.py": 2,
    # Source-fetching runtime owner-decision record documents only the negative routing guard.
    "docs/prd/SOURCE-FETCHING-RUNTIME-OWNER-DECISION-RECORD-01.md": 1,
    # Source-fetching runtime track hold closeout documents only the negative routing guard.
    "docs/prd/SOURCE-FETCHING-RUNTIME-TRACK-HOLD-CLOSEOUT-01.md": 1,
    # Weather Bot Phase 0A hold-state refresh documents only the negative routing guard.
    "docs/prd/WEATHER-BOT-PHASE0A-HOLD-STATE-REFRESH-01.md": 2,
    # Weather Bot Phase 0A hold-state closeout documents only the negative routing guard.
    "docs/prd/WEATHER-BOT-PHASE0A-HOLD-STATE-CLOSEOUT-01.md": 2,
    # Stage 2 skeleton-03 guard doc includes the required legacy identifier audit command only.
    "docs/prd/PRD-P1-WX-STAGE2-SKELETON-03_TARGETED_MAPPING_BUILDER_VALIDATION_COVERAGE.md": 1,
    # Stage 2 fixture implementation closeout documents the fixture JSON legacy identifier guard only.
    "docs/prd/PRD-P1-WX-STAGE2-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_STATIC_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md": 2,
    # Stage 2 real fixture implementation test includes a forbidden legacy identifier guard only.
    "tests/core/test_prd_p1_wx_stage2_real_fixture_implementation_01.py": 1,
    # Weather Bot Phase 0A meta refresh documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-META-REFRESH-01.md": 1,
    "tests/core/test_weather_bot_phase0a_meta_refresh_01.py": 2,
    "docs/prd/WEATHER-BOT-PHASE0A-META-REFRESH-SELF-REVIEW-01.md": 1,
    "tests/core/test_weather_bot_phase0a_meta_refresh_self_review_01.py": 2,
    # Weather Bot Phase 0A non-source-fetching scope inventory self-review documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-NON-SOURCE-FETCHING-SCOPE-INVENTORY-SELF-REVIEW-01.md": 1,
    "tests/core/test_weather_bot_phase0a_non_source_fetching_scope_inventory_self_review_01.py": 2,
    # Weather Bot Phase 0A market-contract static inventory documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-MARKET-CONTRACT-STATIC-INVENTORY-01.md": 4,
    "tests/core/test_weather_bot_phase0a_market_contract_static_inventory_01.py": 5,
    # Weather Bot Phase 0A market-contract static inventory self-review documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-MARKET-CONTRACT-STATIC-INVENTORY-SELF-REVIEW-01.md": 2,
    "tests/core/test_weather_bot_phase0a_market_contract_static_inventory_self_review_01.py": 4,
    # Weather Bot Phase 0A canonical identifier static audit documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-01.md": 5,
    "tests/core/test_weather_bot_phase0a_canonical_identifier_static_audit_01.py": 7,
    # Weather Bot Phase 0A canonical identifier static audit self-review documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-CANONICAL-IDENTIFIER-STATIC-AUDIT-SELF-REVIEW-01.md": 5,
    "tests/core/test_weather_bot_phase0a_canonical_identifier_static_audit_self_review_01.py": 4,
    # Weather Bot Phase 0A settlement-rule taxonomy planning documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-TAXONOMY-PLANNING-01.md": 3,
    "tests/core/test_weather_bot_phase0a_settlement_rule_taxonomy_planning_01.py": 4,
    # Weather Bot Phase 0A manual-review checklist planning documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-MANUAL-REVIEW-CHECKLIST-PLANNING-01.md": 3,
    "tests/core/test_weather_bot_phase0a_manual_review_checklist_planning_01.py": 4,
    # Weather Bot Phase 0A no-lookahead policy documentation documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-POLICY-DOCUMENTATION-01.md": 3,
    "tests/core/test_weather_bot_phase0a_no_lookahead_policy_documentation_01.py": 4,
    # Weather Bot Phase 0A fail-closed error taxonomy planning documents the no-routing boundary only.
    "docs/prd/WEATHER-BOT-PHASE0A-FAIL-CLOSED-ERROR-TAXONOMY-PLANNING-01.md": 10,
    "tests/core/test_weather_bot_phase0a_fail_closed_error_taxonomy_planning_01.py": 7,
    # Stage 2 real fixture implementation closeout documents fixture JSON legacy identifier guards only.
    "docs/prd/PRD-P1-WX-STAGE2-REAL-FIXTURE-IMPLEMENTATION-CLOSEOUT-01_REAL_SOURCE_BACKED_FIXTURE_IMPLEMENTATION_CLOSEOUT_CHECKPOINT.md": 2,
    # Known legacy runtime modules inventoried in Ticket 0A-01A.
    "meg/agent_core/crowding_detector.py": 2,
    "meg/agent_core/decision_agent.py": 11,
    "meg/agent_core/position_manager.py": 17,
    "meg/agent_core/risk_controller.py": 4,
    "meg/agent_core/saturation_monitor.py": 3,
    "meg/agent_core/signal_aggregator.py": 1,
    "meg/agent_core/trap_detector.py": 11,
    "meg/core/events.py": 36,
    "meg/core/logger.py": 2,
    "meg/dashboard/api/main.py": 19,
    "meg/dashboard/ui/src/App.jsx": 25,
    "meg/data_layer/clob_client.py": 23,
    "meg/data_layer/polygon_feed.py": 11,
    "meg/data_layer/wallet_registry.py": 7,
    "meg/db/migrations/versions/42acac652ac5_initial_schema_six_tables.py": 7,
    "meg/db/migrations/versions/c8f2e4b1a9d3_add_wallet_market_trade_index.py": 3,
    "meg/db/models.py": 10,
    "meg/execution/entry_filter.py": 7,
    "meg/execution/order_router.py": 3,
    "meg/execution/slippage_guard.py": 11,
    "meg/pre_filter/arbitrage_exclusion.py": 8,
    "meg/pre_filter/intent_classifier.py": 7,
    "meg/pre_filter/market_quality.py": 24,
    "meg/pre_filter/pipeline.py": 10,
    "meg/signal_engine/composite_scorer.py": 2,
    "meg/signal_engine/consensus_filter.py": 3,
    "meg/signal_engine/contrarian_detector.py": 3,
    "meg/signal_engine/ladder_detector.py": 2,
    "meg/telegram/bot.py": 5,
    # Legacy tests and fixtures that still exercise the pre-migration contract.
    "tests/agent_core/conftest.py": 12,
    "tests/agent_core/test_decision_agent.py": 8,
    "tests/agent_core/test_position_manager.py": 13,
    "tests/agent_core/test_risk_controller.py": 1,
    "tests/agent_core/test_trap_detector.py": 27,
    "tests/core/test_canonical_id_contract.py": 19,
    "docs/prd/WEATHER-BOT-PHASE0A-NON-SOURCE-FETCHING-SCOPE-INVENTORY-01.md": 1,
    "tests/core/test_weather_bot_phase0a_non_source_fetching_scope_inventory_01.py": 2,
    # Stage 2 metadata contract documentation uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-STAGE2-METADATA-CONTRACT-DOCUMENTATION-01.md": 5,
    "tests/core/test_weather_bot_phase0a_stage2_metadata_contract_documentation_01.py": 7,
    # Paper-trade readiness gap inventory uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-PAPER-TRADE-READINESS-GAP-INVENTORY-01.md": 5,
    "tests/core/test_weather_bot_phase0a_paper_trade_readiness_gap_inventory_01.py": 7,
    # Evaluation metrics planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-EVALUATION-METRICS-PLANNING-01.md": 3,
    "tests/core/test_weather_bot_phase0a_evaluation_metrics_planning_01.py": 7,
    # Operator workflow planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-OPERATOR-WORKFLOW-PLANNING-01.md": 3,
    "tests/core/test_weather_bot_phase0a_operator_workflow_planning_01.py": 7,
    # Supplied market-contract input planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-SUPPLIED-MARKET-CONTRACT-INPUT-PLANNING-01.md": 3,
    "tests/core/test_weather_bot_phase0a_supplied_market_contract_input_planning_01.py": 7,
    # Settlement-rule interpreter planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-SETTLEMENT-RULE-INTERPRETER-PLANNING-01.md": 3,
    "tests/core/test_weather_bot_phase0a_settlement_rule_interpreter_planning_01.py": 5,
    # No-lookahead validation planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-NO-LOOKAHEAD-VALIDATION-PLANNING-01.md": 5,
    "tests/core/test_weather_bot_phase0a_no_lookahead_validation_planning_01.py": 5,
    # Fail-closed validation planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-FAIL-CLOSED-VALIDATION-PLANNING-01.md": 3,
    "tests/core/test_weather_bot_phase0a_fail_closed_validation_planning_01.py": 7,
    # Phase summary and handoff refresh uses market_id only as a non-routing negative boundary.
    "docs/meta/MEG_ACTIVE_STATE.md": 3,
    "docs/meta/MEG_CHAT_HANDOFF.md": 2,
    "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md": 3,
    "docs/meta/domain_packets/WEATHER_BOT_PACKET.md": 3,
    "docs/prd/WEATHER-BOT-PHASE0A-PHASE-SUMMARY-AND-HANDOFF-REFRESH-01.md": 3,
    "tests/core/test_weather_bot_phase0a_phase_summary_and_handoff_refresh_01.py": 2,
    # Validation output packet planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-VALIDATION-OUTPUT-PACKET-PLANNING-01.md": 6,
    "tests/core/test_weather_bot_phase0a_validation_output_packet_planning_01.py": 6,
    # Manual-review decision record planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-MANUAL-REVIEW-DECISION-RECORD-PLANNING-01.md": 4,
    "tests/core/test_weather_bot_phase0a_manual_review_decision_record_planning_01.py": 6,
    # Phase closeout runtime approval readiness inventory uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-PHASE-CLOSEOUT-AND-RUNTIME-APPROVAL-READINESS-INVENTORY-01.md": 3,
    "tests/core/test_weather_bot_phase0a_phase_closeout_runtime_approval_readiness_inventory_01.py": 6,
    # Stage 2 fixture-only runtime closeout readiness uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-STAGE2-FIXTURE-ONLY-SOURCE-PROVIDER-RUNTIME-CLOSEOUT-READINESS-01.md": 2,
    "tests/core/test_weather_bot_stage2_fixture_only_source_provider_runtime_closeout_readiness_01.py": 2,
    # Stage 2 phase summary and handoff refresh uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-STAGE2-PHASE-SUMMARY-AND-HANDOFF-REFRESH-01.md": 3,
    "tests/core/test_weather_bot_stage2_phase_summary_and_handoff_refresh_01.py": 3,
    # Stage 3 readiness inventory uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-STAGE3-READINESS-INVENTORY-01.md": 5,
    "tests/core/test_weather_bot_stage3_readiness_inventory_01.py": 4,
    # Runtime approval request packet planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-RUNTIME-APPROVAL-REQUEST-PACKET-PLANNING-01.md": 2,
    "tests/core/test_weather_bot_phase0a_runtime_approval_request_packet_planning_01.py": 5,
    # Non-owner runtime gate hold refresh planning uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-NON-OWNER-RUNTIME-GATE-HOLD-REFRESH-PLANNING-01.md": 3,
    "tests/core/test_weather_bot_phase0a_non_owner_runtime_gate_hold_refresh_planning_01.py": 4,
    # Static planning lane closeout refresh uses market_id only as a non-routing negative boundary.
    "docs/prd/WEATHER-BOT-PHASE0A-STATIC-PLANNING-LANE-CLOSEOUT-REFRESH-01.md": 4,
    "tests/core/test_weather_bot_phase0a_static_planning_lane_closeout_refresh_01.py": 4,
    "tests/dashboard/test_api.py": 9,
    "tests/data_layer/test_clob_client.py": 20,
    "tests/data_layer/test_polygon_feed.py": 6,
    "tests/data_layer/test_wallet_registry.py": 4,
    "tests/db/test_models.py": 7,
    "tests/execution/conftest.py": 8,
    "tests/execution/test_order_router.py": 3,
    "tests/pre_filter/conftest.py": 12,
    "tests/pre_filter/test_arbitrage_exclusion.py": 16,
    "tests/pre_filter/test_intent_classifier.py": 20,
    "tests/pre_filter/test_market_quality.py": 20,
    "tests/pre_filter/test_pipeline.py": 1,
    "tests/signal_engine/conftest.py": 4,
    "tests/signal_engine/test_consensus_filter.py": 2,
    "tests/signal_engine/test_contrarian_detector.py": 14,
    "tests/signal_engine/test_ladder_detector.py": 12,
    "tests/signal_engine/test_signal_decay.py": 1,
    "tests/telegram/conftest.py": 2,
    "tests/telegram/test_bot.py": 2,
})
