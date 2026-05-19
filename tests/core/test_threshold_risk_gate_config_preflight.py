from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
R10_PATH = REPO_ROOT / "docs/phase0b/0B-R10_CROSS_PLATFORM_OPPORTUNITY_DETECTOR_CONTRACT.md"
R12_PATH = REPO_ROOT / "docs/phase0b/0B-R12_THRESHOLD_RISK_GATE_CONFIG_SPEC.md"
LEGACY_ID_FIELD = "market" + "_id"


def _read_doc(path: Path) -> str:
    assert path.exists(), f"Required doc missing: {path}"
    return path.read_text(encoding="utf-8")


def _assert_contains_all(text: str, required_terms: list[str], label: str) -> None:
    missing = [term for term in required_terms if term not in text]
    assert not missing, f"{label} missing required terms: {missing}"


def test_r12_exists_and_relationship_to_r10_r11_is_present() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "Relationship to prior docs",
            "R10",
            "opportunity candidate input/output contract fields",
            "R11",
            "statically enforces the R10 detector contract language",
            "R12 (this doc)",
            "configuration semantics for screening or rejecting candidates",
            "does not set production runtime defaults",
            "does not implement runtime behavior",
        ],
        "R12 relationship chain",
    )


def test_r12_configuration_groups_are_documented() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "edge thresholds",
            "spread thresholds",
            "confidence thresholds",
            "semantic match thresholds",
            "liquidity thresholds",
            "data quality thresholds",
            "exposure caps",
            "loss caps",
            "market allowlists/blocklists",
            "mode controls",
            "audit/logging controls",
            "kill-switch controls (future phases only)",
        ],
        "R12 configuration groups",
    )


def test_r12_required_config_fields_are_documented() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "`config_id`",
            "`config_version`",
            "`mode`",
            "`planning`",
            "`fixture`",
            "`paper`",
            "`read_only_live_blocked`",
            "`live_blocked`",
            "`source_id`",
            "`provenance`",
            "`created_at`",
            "`updated_at`",
            "`min_edge_bps`",
            "`min_fee_adjusted_edge_bps`",
            "`min_spread_bps`",
            "`min_confidence_score`",
            "`min_semantic_match_score`",
            "`min_liquidity_score`",
            "`min_data_quality_score`",
            "`max_per_market_exposure`",
            "`max_global_exposure`",
            "`max_daily_loss`",
            "`market_allowlist`",
            "`market_blocklist`",
            "`platform_allowlist`",
            "`platform_blocklist`",
            "`dry_run_default`",
            "`require_operator_approval`",
            "`live_trading_enabled`",
            "`autonomous_trading_enabled`",
            "`kill_switch_enabled`",
            "`audit_log_required`",
            "`rejection_reason_required`",
        ],
        "R12 required config fields",
    )


def test_r12_phase_0b_default_posture_is_fail_closed() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "`dry_run_default` must be `true`",
            "`require_operator_approval` must be `true`",
            "`live_trading_enabled` must be `false`",
            "`autonomous_trading_enabled` must be `false`",
            "missing config must fail closed",
            "invalid config must fail closed",
            "unknown mode must fail closed",
        ],
        "R12 Phase 0B posture",
    )


def test_r12_candidate_screening_and_rejection_coverage_is_present() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "edge below `min_edge_bps`",
            "fee-adjusted edge below `min_fee_adjusted_edge_bps`",
            "spread below `min_spread_bps`",
            "confidence below `min_confidence_score`",
            "semantic match below `min_semantic_match_score`",
            "liquidity below `min_liquidity_score`",
            "data quality below `min_data_quality_score`",
            "market or platform not in allowlist",
            "market or platform present in blocklist",
            "per-market or global exposure cap exceeded",
            "daily loss cap exceeded",
            "missing fee assumptions",
            "missing liquidity assumptions",
            "missing `provenance` or missing `source_id`",
            "missing operator approval requirement",
            "`live_trading_enabled` or `autonomous_trading_enabled` set true in Phase 0B",
        ],
        "R12 screening/rejection coverage",
    )


def test_r12_output_and_rejection_contract_fields_are_present() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "`candidate_id` or `opportunity_id`",
            "`config_id`",
            "`accepted` (`true`/`false`)",
            "`rejection_reasons`",
            "`fail_closed_reason`",
            "`thresholds_evaluated`",
            "`observed_values`",
            "`decision_timestamp`",
            "`audit_log_reference`",
            "`proposal_allowed` (`true`/`false`)",
            "`execution_allowed` (must be `false` in Phase 0B)",
        ],
        "R12 output/rejection contract",
    )


def test_r12_fail_closed_requirements_are_present() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "missing config",
            "invalid type/range",
            "unknown `config_version`",
            "unknown mode",
            "missing required threshold",
            "negative exposure cap",
            "`live_trading_enabled: true` in Phase 0B",
            "`autonomous_trading_enabled: true` in Phase 0B",
            "`dry_run_default: false` in Phase 0B",
            "`require_operator_approval: false` in Phase 0B",
            "missing audit/rejection reason policy",
        ],
        "R12 fail-closed requirements",
    )


def test_r12_future_autonomy_compatibility_wording_is_present() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "Future Phase 6/v3 autonomy compatibility",
            "`paper_autonomous`",
            "`limited_autonomous`",
            "`full_autonomous`",
            "separate explicit approval",
            "risk, approval, ToS/jurisdiction, monitoring, kill-switch, and execution-gate reviews",
            "paper trading validation",
            "position limits",
            "daily loss limits",
            "market allowlist",
            "confidence/edge thresholds",
            "kill switch",
            "audit logging",
            "drift monitoring",
            "manual override",
            "explicit config flag default off",
            "ToS/jurisdiction approval",
            "dependency/security review",
            "None of the future autonomy modes are approved by this ticket",
            "config semantics remain proposal-screening/planning only",
        ],
        "R12 future autonomy compatibility",
    )


def test_r12_testing_strategy_terms_are_present() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "static config contract tests first",
            "tiny deterministic config fixtures",
            "invalid config fail-closed tests",
            "no network in unit tests",
            "no secrets in CI",
            "no live connector requirement",
            "no order authority tests",
            "proposal-only boundary tests",
            "future runtime tests must prove live/autonomous flags cannot enable execution in Phase 0B",
        ],
        "R12 testing strategy",
    )


def test_r12_non_goals_block_is_present() -> None:
    text = _read_doc(R12_PATH)
    _assert_contains_all(
        text,
        [
            "implementation",
            "config loader changes",
            "risk engine changes",
            "detector implementation changes",
            "runtime/trading changes",
            "live API calls",
            "connector calls",
            "order placement",
            "execution/approval changes",
            "dependency changes",
            "dataset import",
            "loader expansion",
            "real fixture data commits in this ticket",
            "legal conclusion",
            "live API/trading approval",
            "Phase 0B autonomous trading approval",
        ],
        "R12 non-goals",
    )


def test_no_legacy_identifier_literal_in_r12_doc() -> None:
    text = _read_doc(R12_PATH)
    assert LEGACY_ID_FIELD not in text


def test_r10_and_r12_contract_chain_is_consistent() -> None:
    r10_text = _read_doc(R10_PATH)
    r12_text = _read_doc(R12_PATH)
    _assert_contains_all(
        r10_text,
        [
            "opportunity candidate",
            "input/output contract",
            "Scoring fields and thresholds (planning-only)",
        ],
        "R10 detector contract baseline",
    )
    _assert_contains_all(
        r12_text,
        [
            "configuration semantics",
            "screening or rejecting candidates",
            "planning-only",
        ],
        "R12 config semantics baseline",
    )
