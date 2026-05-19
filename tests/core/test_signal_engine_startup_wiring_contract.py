"""Phase 0A-05E preflight: startup wiring contract for future main integration.

These checks are intentionally static and non-invasive. The forward-looking
assertion is xfail(strict=True) until production wiring is implemented.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest


MAIN_PATH = Path(__file__).resolve().parents[2] / "meg" / "main.py"


def _main_ast() -> ast.AST:
    return ast.parse(MAIN_PATH.read_text(encoding="utf-8"))


def test_current_main_does_not_yet_import_signal_engine_runner() -> None:
    tree = _main_ast()
    imports = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "meg.signal_engine"
    ]

    assert all(
        all(alias.name != "runner" or alias.asname != "signal_engine_runner" for alias in node.names)
        for node in imports
    )


@pytest.mark.xfail(strict=True, reason="Phase 0A-05E is preflight only; startup wiring lands in a future ticket.")
def test_future_main_wires_signal_engine_runner_task() -> None:
    source = MAIN_PATH.read_text(encoding="utf-8")

    assert "from meg.signal_engine import runner as signal_engine_runner" in source
    assert "name=\"signal_engine_runner\"" in source


def test_existing_main_task_names_are_still_present() -> None:
    source = MAIN_PATH.read_text(encoding="utf-8")

    for task_name in (
        'name="polygon_feed"',
        'name="pre_filter_pipeline"',
        'name="signal_aggregator"',
        'name="position_monitor"',
        'name="telegram_bot"',
    ):
        assert task_name in source
