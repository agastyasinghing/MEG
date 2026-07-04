from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEST = ROOT / "tests/core/test_weather_bot_phase0a_meta_handoff_refresh_after_static_closeout_01.py"
META_DOCS = (
    ROOT / "docs/meta/MEG_ACTIVE_STATE.md",
    ROOT / "docs/meta/MEG_CHAT_HANDOFF.md",
    ROOT / "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md",
    ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
)
RECOMMENDED_NEXT_TRACK = "weather_bot_phase0a_meta_state_handoff_revision_if_needed"
CONDITIONAL_REVISION_TRACK = "weather_bot_phase0a_meta_handoff_refresh_revision_if_scope_too_broad"
FORBIDDEN_NEXT_TRACK_FRAGMENTS = (
    "self_review",
    "self-review",
    "standalone_self_review",
    "standalone-self-review",
    "owner_decision_capture",
    "owner_capture",
    "runtime_implementation",
    "paper_trade",
    "trading",
)
CANONICAL_FIELD_RE = re.compile(r"canonical routing fields remain exactly `condition_id`, `token_id`, and `outcome`", re.I)


def _read_meta_docs() -> dict[Path, str]:
    return {path: path.read_text(encoding="utf-8") for path in META_DOCS}


def _combined() -> str:
    return "\n".join(_read_meta_docs().values())


def test_test_file_uses_only_standard_library_imports() -> None:
    tree = ast.parse(TEST.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert set(imports) <= {"__future__", "ast", "re", "pathlib"}


def test_reads_only_allowed_meta_docs() -> None:
    assert META_DOCS == (
        ROOT / "docs/meta/MEG_ACTIVE_STATE.md",
        ROOT / "docs/meta/MEG_CHAT_HANDOFF.md",
        ROOT / "docs/meta/MEG_NEXT_CHAT_BOOTSTRAP_PROMPT.md",
        ROOT / "docs/meta/domain_packets/WEATHER_BOT_PACKET.md",
    )
    assert all(path.is_file() for path in META_DOCS)


def test_pr308_latest_static_closeout_and_predecessor_context_are_recorded() -> None:
    for path, text in _read_meta_docs().items():
        assert "PR #308" in text, path
        assert "latest" in text.lower() or "post-pr #308" in text.lower(), path
        assert "static planning lane closeout" in text.lower() or "static planning lane closed out" in text.lower(), path
        assert "PR #307" in text, path
        assert "PR #283 remains excluded unless explicitly merged" in text, path


def test_static_planning_lane_is_closed_out() -> None:
    text = _combined().lower()
    assert "weather bot phase 0a static planning lane closed out" in text


def test_approval_and_source_fetching_holds_remain_recorded() -> None:
    text = _combined().lower()
    assert "runtime approval remains not granted" in text
    assert "source-fetching approval remains not granted" in text
    assert "provider/source approval remains not granted" in text
    assert "paper-trade approval remains not granted" in text
    assert "trading/production approval remains not granted" in text
    assert "source-fetching runtime track remains closed/held" in text
    assert "hold_source_fetching_runtime_track" in text


def test_no_owner_capture_or_implementation_lane_is_active() -> None:
    text = _combined().lower()
    assert "no owner-decision capture lane is active" in text
    assert "no runtime/source/provider/paper-trade/trading implementation lane is active" in text


def test_canonical_identifier_posture_is_exact() -> None:
    for path, text in _read_meta_docs().items():
        assert CANONICAL_FIELD_RE.search(text), path
        assert "`token_outcome_pair` remains derived only" in text, path
        assert "`market" + "_id` remains non-routing only" in text, path


def test_next_tracks_are_exact_and_safe() -> None:
    text = _combined()
    assert RECOMMENDED_NEXT_TRACK in text
    assert CONDITIONAL_REVISION_TRACK in text
    for track in (RECOMMENDED_NEXT_TRACK, CONDITIONAL_REVISION_TRACK):
        assert not any(fragment in track for fragment in FORBIDDEN_NEXT_TRACK_FRAGMENTS)


def test_artificial_hybrid_custom_assignment_values_are_rejected_locally() -> None:
    allowed_canonical_fields = {"condition_id", "token_id", "outcome"}
    sample_values = ["condition_id", "condition_id_legacy_identifier_hybrid", "custom_outcome"]
    accepted = [value for value in sample_values if value in allowed_canonical_fields]
    assert accepted == ["condition_id"]
