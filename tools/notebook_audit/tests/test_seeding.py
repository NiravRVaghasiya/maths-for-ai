"""Unit tests for notebook_audit.seeding (no kernel execution needed)."""

from __future__ import annotations

import nbformat

from notebook_audit.seeding import SEED_CELL_MARKER, inject_seed_cell, strip_injected_cells


def _make_nb(sources: list) -> nbformat.NotebookNode:
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_code_cell(source=s) for s in sources]
    return nb


def test_inject_prepends_exactly_one_cell():
    nb = _make_nb(["print(1)", "print(2)"])
    inject_seed_cell(nb, seed=42)
    assert len(nb.cells) == 3
    assert nb.cells[0]["source"].startswith(SEED_CELL_MARKER)
    assert "42" in nb.cells[0]["source"]


def test_original_cells_are_unmodified_after_injection():
    nb = _make_nb(["print(1)", "print(2)"])
    inject_seed_cell(nb, seed=0)
    assert nb.cells[1]["source"] == "print(1)"
    assert nb.cells[2]["source"] == "print(2)"


def test_strip_removes_only_the_injected_cell():
    nb = _make_nb(["print(1)", "print(2)"])
    inject_seed_cell(nb, seed=0)
    stripped = strip_injected_cells(nb)
    assert len(stripped.cells) == 2
    assert stripped.cells[0]["source"] == "print(1)"
    assert stripped.cells[1]["source"] == "print(2)"


def test_strip_is_a_noop_on_a_notebook_with_no_injected_cell():
    nb = _make_nb(["print(1)"])
    stripped = strip_injected_cells(nb)
    assert len(stripped.cells) == 1
    assert stripped.cells[0]["source"] == "print(1)"
