from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
R7_PATH = REPO_ROOT / "docs/phase0b/0B-R7_CONNECTOR_INTERFACE_BOUNDARY_SPEC.md"
R8_PATH = REPO_ROOT / "docs/phase0b/0B-R8_CONNECTOR_FIXTURE_TEST_DOUBLE_CONTRACT.md"
LEGACY_ID_FIELD = "market" + "_id"


def _read_doc(path: Path) -> str:
    assert path.exists(), f"Required doc missing: {path}"
    return path.read_text(encoding="utf-8")


def _assert_contains_all(text: str, required_terms: list[str], label: str) -> None:
    missing = [term for term in required_terms if term not in text]
    assert not missing, f"{label} missing required terms: {missing}"


def test_r7_connector_categories_and_fields_present() -> None:
    text = _read_doc(R7_PATH)
    _assert_contains_all(
        text,
        [
            "Market metadata connector",
            "Price/orderbook snapshot connector",
            "Trade/fill history connector",
            "Account/wallet read-only state connector",
            "Resolution/outcome metadata connector",
            "Proposal emission interface",
            "Paper/simulated connector",
            "Live connector placeholder",
        ],
        "R7 connector categories",
    )
    _assert_contains_all(
        text,
        [
            "`connector_name`",
            "`platform`",
            "`mode`",
            "`source_id`",
            "`provenance`",
            "`fetched_at`",
            "`observed_at`",
            "`schema_version`",
            "`supported_operations`",
            "`blocked_operations`",
            "`error_policy`",
            "`rate_limit_policy`",
            "`secrets_required`",
            "`dependency_status`",
            "`ToS_jurisdiction_status`",
            "`approval_status`",
        ],
        "R7 common connector fields",
    )


def test_r7_canonical_ids_boundary_and_fail_closed_requirements() -> None:
    text = _read_doc(R7_PATH)
    _assert_contains_all(
        text,
        [
            "`condition_id`",
            "`token_id`",
            "`outcome`",
            "proposal emission does **not** equal approval",
            "operator approval remains mandatory",
            "no connector can place orders",
            "no connector can bypass Telegram/operator approval",
            "execution and order-router behavior remain out of scope",
            "fail closed on missing required fields",
            "fail closed on unknown `schema_version`",
            "fail closed on unsupported connector `mode`",
            "fail closed on missing ToS/jurisdiction approval",
            "fail closed on missing dependency/security review",
            "no silent fallback into live behavior",
            "no secret leakage",
        ],
        "R7 canonical IDs, boundary and safety",
    )


def test_r8_categories_fields_and_safety_contract_present() -> None:
    text = _read_doc(R8_PATH)
    _assert_contains_all(
        text,
        [
            "Market metadata fixture connector",
            "Price/orderbook snapshot fixture connector",
            "Trade/fill history fixture connector",
            "Account/wallet read-only state fixture connector",
            "Resolution/outcome fixture connector",
            "Proposal-emission fixture boundary",
            "Error/fail-closed fixture connector",
            "Blocked live connector sentinel",
        ],
        "R8 test-double categories",
    )
    _assert_contains_all(
        text,
        [
            "`test_double_name`",
            "`connector_category`",
            "`platform`",
            "`mode`",
            "`source_id`",
            "`fixture_id`",
            "`fixture_version`",
            "`schema_version`",
            "`deterministic_seed`",
            "`supported_operations`",
            "`blocked_operations`",
            "`expected_failures`",
            "`provenance`",
            "`approval_status`",
            "`live_network_allowed`",
            "`order_authority`",
            "`live_network_allowed` (must be `false`)",
            "`order_authority` (must be `false`)",
            "no secrets",
            "no live credentials",
            "no large datasets",
            "no external repository files copied into MEG",
        ],
        "R8 fields and safety",
    )


def test_r8_fail_closed_and_r7_r8_non_goals_present() -> None:
    r7_text = _read_doc(R7_PATH)
    r8_text = _read_doc(R8_PATH)

    _assert_contains_all(
        r8_text,
        [
            "missing `condition_id` / `token_id` / `outcome` when required",
            "unsupported `schema_version`",
            "unsupported connector `mode`",
            "`live_network_allowed: true`",
            "`order_authority: true`",
            "missing `provenance`",
            "missing `source_id`",
            "missing `fixture_id`",
            "invalid timestamp format/value",
            "attempted proposal-to-approval bypass",
            "attempted order placement operation",
        ],
        "R8 fail-closed scenarios",
    )

    non_goals = [
        "implementation",
        "connector code",
        "runtime/trading changes",
        "live API calls",
        "order placement",
        "execution/approval-path changes",
        "dependency changes",
        "dataset import",
        "loader expansion",
        "legal conclusion",
    ]
    _assert_contains_all(r7_text, non_goals, "R7 non-goals")
    _assert_contains_all(r8_text, non_goals, "R8 non-goals")


def test_no_legacy_identifier_literal_in_r7_or_r8_docs() -> None:
    r7_text = _read_doc(R7_PATH)
    r8_text = _read_doc(R8_PATH)
    assert LEGACY_ID_FIELD not in r7_text
    assert LEGACY_ID_FIELD not in r8_text
