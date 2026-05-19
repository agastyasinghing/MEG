from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
R7_PATH = REPO_ROOT / "docs/phase0b/0B-R7_CONNECTOR_INTERFACE_BOUNDARY_SPEC.md"
R8_PATH = REPO_ROOT / "docs/phase0b/0B-R8_CONNECTOR_FIXTURE_TEST_DOUBLE_CONTRACT.md"
R10_PATH = REPO_ROOT / "docs/phase0b/0B-R10_CROSS_PLATFORM_OPPORTUNITY_DETECTOR_CONTRACT.md"
LEGACY_ID_FIELD = "market" + "_id"


def _read_doc(path: Path) -> str:
    assert path.exists(), f"Required doc missing: {path}"
    return path.read_text(encoding="utf-8")


def _assert_contains_all(text: str, required_terms: list[str], label: str) -> None:
    missing = [term for term in required_terms if term not in text]
    assert not missing, f"{label} missing required terms: {missing}"


def test_r10_exists_and_references_r7_r8_r9_relationship() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "Relationship to R7 / R8 / R9",
            "R7",
            "connector/interface output boundaries",
            "R8",
            "fixture/test-double shapes",
            "R9",
            "statically enforces connector-contract",
            "R10 (this doc)",
            "input/output contract",
            "R7/R8 normalized shapes",
        ],
        "R10 relationship chain",
    )


def test_r10_input_contract_fields_present() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "Market metadata records",
            "Price/orderbook snapshot records",
            "Optional trade/fill history records",
            "Optional resolution/outcome metadata records",
            "`platform`",
            "`source_id`",
            "`provenance`",
            "`observed_at`",
            "`fetched_at`",
            "`schema_version`",
            "`condition_id`",
            "`token_id`",
            "`outcome`",
        ],
        "R10 input contract",
    )


def test_r10_normalized_market_pair_candidate_fields_present() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "`pair_id`",
            "`platforms_compared`",
            "`source_ids`",
            "`market_titles`",
            "`market_questions`",
            "`market_slugs`",
            "`category`",
            "`semantic_match_score`",
            "`canonical_match_evidence`",
            "`condition_id_alignment`",
            "`token_id_alignment`",
            "`outcome_alignment`",
            "`mismatch_flags`",
            "`provenance`",
            "`observed_at`",
            "`rejection_reasons`",
        ],
        "R10 market pair candidate fields",
    )


def test_r10_opportunity_candidate_output_shape_present() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "`opportunity_id`",
            "`pair_id`",
            "`opportunity_type`",
            "`cross_platform_price_gap`",
            "`bundle_mispricing`",
            "`stale_price_divergence`",
            "`liquidity_gap`",
            "`research_only_anomaly`",
            "`legs`",
            "`platform` per leg",
            "`outcome` per leg",
            "`side` per leg",
            "`price` and/or `odds` per leg",
            "`estimated_edge_bps`",
            "`fee_adjusted_edge_bps`",
            "`confidence_score`",
            "`liquidity_score`",
            "`data_quality_score`",
            "`source_ids`",
            "`provenance`",
            "`observed_at`",
            "`detector_schema_version`",
            "`fail_closed_reason`",
            "`rejection_reasons`",
        ],
        "R10 opportunity output shape",
    )


def test_r10_candidate_only_opportunity_types_boundary_present() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "candidate detections only",
            "never trade instructions",
            "analysis artifact only",
            "not approval",
            "not execution",
            "not an order instruction",
        ],
        "R10 candidate-only opportunity boundary",
    )


def test_r10_fail_closed_behavior_terms_present() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "missing required platform/source/provenance fields",
            "missing required price/odds fields",
            "unsupported `schema_version`",
            "unsupported `opportunity_type`",
            "invalid timestamp format/value",
            "low `semantic_match_score`",
            "conflicting outcome mapping",
            "missing fee assumptions",
            "missing liquidity assumptions",
            "ToS/jurisdiction not approved for live use",
            "connector mode is `live_blocked`",
            "any requested order authority",
            "any attempt to bypass proposal/approval boundary",
            "`fail_closed_reason`",
            "`rejection_reasons`",
        ],
        "R10 fail-closed terms",
    )


def test_r10_scoring_and_threshold_fields_planning_only_present() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "`semantic_match_score`",
            "`edge_score`",
            "`fee_adjusted_edge_bps`",
            "`liquidity_score`",
            "`data_quality_score`",
            "`confidence_score`",
            "`rejection_thresholds`",
            "`threshold_config_source`",
            "Exact threshold values are **not** set in this ticket",
            "future configuration-spec work",
        ],
        "R10 scoring and threshold planning fields",
    )


def test_r10_output_authority_boundary_present() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "detector output is **not** a trade",
            "detector output is **not** approval",
            "detector output is **not** an order",
            "detector output cannot call connector APIs",
            "detector output cannot place orders",
            "detector output cannot bypass Telegram/operator approval",
            "analysis/proposal-candidate scope only",
        ],
        "R10 authority boundary",
    )


def test_r10_autonomy_wording_and_future_modes_present() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "approve autonomous trading in Phase 0B",
            "Future autonomous operation belongs only to a separate explicit **Phase 6/v3** milestone",
            "paper trading validation",
            "max position limits",
            "max daily loss",
            "market allowlist",
            "confidence/edge thresholds",
            "kill switch",
            "audit logging",
            "drift monitoring",
            "manual override",
            "explicit config flag default off",
            "ToS/jurisdiction approval",
            "dependency/security review",
            "manual review",
            "paper-autonomous mode",
            "limited-autonomous mode",
            "full-autonomous mode",
            "only manual/proposal planning is approved in Phase 0B",
        ],
        "R10 autonomy wording and future modes",
    )


def test_r10_testing_strategy_and_non_goals_present() -> None:
    text = _read_doc(R10_PATH)
    _assert_contains_all(
        text,
        [
            "static contract tests first",
            "tiny deterministic fixtures",
            "R8 test doubles",
            "no network in unit tests",
            "no secrets in CI",
            "invalid/missing data fail-closed tests",
            "no order authority tests",
            "proposal-only boundary tests",
            "implementation",
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
        "R10 testing strategy and non-goals",
    )


def test_r10_uses_canonical_ids_without_legacy_literal() -> None:
    r10_text = _read_doc(R10_PATH)
    r7_text = _read_doc(R7_PATH)
    r8_text = _read_doc(R8_PATH)

    _assert_contains_all(
        r10_text,
        ["`condition_id`", "`token_id`", "`outcome`"],
        "R10 canonical identifiers",
    )

    assert LEGACY_ID_FIELD not in r10_text
    assert LEGACY_ID_FIELD not in r7_text
    assert LEGACY_ID_FIELD not in r8_text
