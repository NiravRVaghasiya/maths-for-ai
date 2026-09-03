"""Unit tests for notebook_audit.reproducibility (no kernel execution needed).

Builds synthetic NotebookResult objects directly rather than executing real
notebooks, since what's under test here is purely the stdout-diffing logic,
not kernel behavior (already covered by test_executor.py).
"""

from __future__ import annotations

import nbformat

from notebook_audit.executor import NotebookResult
from notebook_audit.reproducibility import compare_runs


def _make_result(stdout_lines: list) -> NotebookResult:
    nb = nbformat.v4.new_notebook()
    cell = nbformat.v4.new_code_cell(source="print(...)")
    cell["outputs"] = [
        {"output_type": "stream", "name": "stdout", "text": "\n".join(stdout_lines) + "\n"}
    ]
    nb.cells = [cell]
    return NotebookResult(notebook=None, status="pass", duration_s=1.0, executed_nb=nb)


def test_identical_output_is_reproducible():
    run_a = _make_result(["result: 3.14159"])
    run_b = _make_result(["result: 3.14159"])
    diff = compare_runs("00.00", "x.ipynb", run_a, run_b)
    assert diff.is_reproducible
    assert diff.diff_count == 0


def test_different_numeric_output_is_flagged():
    run_a = _make_result(["result: 3.14159"])
    run_b = _make_result(["result: 2.71828"])
    diff = compare_runs("00.00", "x.ipynb", run_a, run_b)
    assert not diff.is_reproducible
    assert diff.diff_count == 1


def test_tiny_float_noise_within_tolerance_is_not_flagged():
    run_a = _make_result(["value: 1.0000000001"])
    run_b = _make_result(["value: 1.0000000002"])
    diff = compare_runs("00.00", "x.ipynb", run_a, run_b)
    assert diff.is_reproducible


def test_timing_lines_are_excluded_from_comparison():
    run_a = _make_result(["loop: 13.44 ms", "step=4000"])
    run_b = _make_result(["loop: 87.20 ms", "step=4000"])  # timing differs, step doesn't
    diff = compare_runs("00.00", "x.ipynb", run_a, run_b)
    assert diff.is_reproducible  # the only real diff is on an excluded timing line


def test_timing_exclusion_does_not_hide_a_real_diff_on_another_line():
    run_a = _make_result(["loop: 13.44 ms", "step=4000"])
    run_b = _make_result(["loop: 87.20 ms", "step=9999"])  # step ALSO differs
    diff = compare_runs("00.00", "x.ipynb", run_a, run_b)
    assert not diff.is_reproducible


def test_different_line_counts_flagged():
    run_a = _make_result(["a", "b", "c"])
    run_b = _make_result(["a", "b"])
    diff = compare_runs("00.00", "x.ipynb", run_a, run_b)
    assert not diff.is_reproducible
