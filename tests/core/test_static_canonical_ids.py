"""Static enforcement for the Phase 0A canonical identifier migration.

These tests do not change production behavior. They freeze the known legacy
``market_id`` footprint and make new usage explicit until future tickets migrate
shared-rail routing to ``condition_id``, ``token_id``, and ``outcome``.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tests.core.canonical_id_allowlist import ALLOWED_MARKET_ID_OCCURRENCE_LINES

REPO_ROOT = Path(__file__).resolve().parents[2]
IGNORED_PARTS = {".git", ".mypy_cache", ".pytest_cache", "__pycache__"}
ENFORCEMENT_HARNESS_FILES = {
    "tests/core/canonical_id_allowlist.py",
    "tests/core/test_static_canonical_ids.py",
    "tests/core/test_redis_key_contract.py",
}
PHASE0A_SHARED_RAIL_MODULES = {
    "meg/core/events.py",
    "meg/data_layer/clob_client.py",
    "meg/agent_core/decision_agent.py",
    "meg/agent_core/risk_controller.py",
    "meg/execution/order_router.py",
    "meg/telegram/bot.py",
}


def _text_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        files.append(path)
    return files


def _market_id_occurrence_lines() -> dict[str, int]:
    occurrences: dict[str, int] = {}
    for path in _text_files():
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        if rel_path in ENFORCEMENT_HARNESS_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        count = sum(1 for line in text.splitlines() if "market_id" in line)
        if count:
            occurrences[rel_path] = count
    return occurrences


def test_market_id_occurrences_match_explicit_allowlist() -> None:
    """New or increased legacy identifier usage must be approved explicitly."""
    observed = _market_id_occurrence_lines()

    unapproved_files = sorted(set(observed) - set(ALLOWED_MARKET_ID_OCCURRENCE_LINES))
    stale_allowlist_files = sorted(set(ALLOWED_MARKET_ID_OCCURRENCE_LINES) - set(observed))
    increased_counts = {
        path: (ALLOWED_MARKET_ID_OCCURRENCE_LINES[path], observed[path])
        for path in sorted(set(observed) & set(ALLOWED_MARKET_ID_OCCURRENCE_LINES))
        if observed[path] > ALLOWED_MARKET_ID_OCCURRENCE_LINES[path]
    }

    assert not unapproved_files, f"Unapproved market_id usage appeared in: {unapproved_files}"
    assert not increased_counts, f"market_id usage increased: {increased_counts}"
    assert not stale_allowlist_files, f"Allowlist entries can be removed: {stale_allowlist_files}"


@pytest.mark.xfail(
    reason="Known Phase 0A shared-rail modules still contain legacy market_id until migration tickets land.",
    strict=True,
)
def test_phase0a_shared_rail_modules_have_no_market_id_after_migration() -> None:
    """Target contract: shared rail code routes by canonical IDs, never market_id."""
    offenders = {
        rel_path: count
        for rel_path, count in _market_id_occurrence_lines().items()
        if rel_path in PHASE0A_SHARED_RAIL_MODULES
    }

    assert offenders == {}
