"""Tests for notebook_audit.executor against real kernel executions.

These tests genuinely execute notebooks (they are integration tests, not
pure unit tests) because the whole point of this harness is correctly
interpreting real nbclient/Jupyter kernel behavior -- several of the facts
asserted below (e.g. where nbclient puts a timed-out cell's execution_count)
were discovered empirically while building this module and are pinned here
specifically so a future nbclient upgrade that changes that behavior gets
caught immediately instead of silently producing wrong classifications.
"""

from __future__ import annotations

from notebook_audit.discovery import NotebookRef
from notebook_audit.executor import execute_notebook

from .conftest import fixture_path


def _ref(name: str, notebook_id: str = "99.00") -> NotebookRef:
    path = fixture_path(name)
    return NotebookRef(notebook_id=notebook_id, module="_fixtures", path=path, relative_path=name)


def test_clean_notebook_passes(kernel_name):
    result = execute_notebook(_ref("pass_clean.ipynb"), kernel_name=kernel_name)
    assert result.status == "pass"
    assert result.failure is None
    assert result.duration_s > 0


def test_import_error_fails_with_cell_index_and_stops_execution(kernel_name):
    # inject_seed=False: cell_index below is asserted against the fixture's
    # OWN cell numbering, which would otherwise shift by +1 once a seed cell
    # is prepended (cell_index always refers to what actually ran, which is
    # correct executor behavior -- it's the injected-seed offset that must
    # be controlled for in a test asserting an exact index).
    result = execute_notebook(
        _ref("fail_import_error.ipynb"), kernel_name=kernel_name, inject_seed=False
    )
    assert result.status == "fail"
    assert result.failure is not None
    assert result.failure.ename == "ModuleNotFoundError"
    assert result.failure.cell_index == 1  # the import cell, 0-indexed (cell 0 just prints)

    # The cell after the failure must never have run.
    third_cell = result.executed_nb.cells[2]
    assert third_cell.get("execution_count") is None


def test_undefined_variable_fails(kernel_name):
    result = execute_notebook(
        _ref("fail_undefined_variable.ipynb"), kernel_name=kernel_name, inject_seed=False
    )
    assert result.status == "fail"
    assert result.failure.ename == "NameError"
    assert result.failure.cell_index == 0


def test_timeout_detects_last_started_cell_not_first_unstarted_cell(kernel_name):
    result = execute_notebook(
        _ref("fail_timeout.ipynb"), kernel_name=kernel_name, cell_timeout_s=3, inject_seed=False
    )
    assert result.status == "timeout"
    assert result.failure is not None
    # cell 0 (print) completes; cell 1 (time.sleep(30)) is the one that times
    # out -- confirmed empirically that nbclient sets execution_count on a
    # cell BEFORE running it, so the timed-out cell has a non-None
    # execution_count despite never finishing. The failing cell must be
    # cell index 1, not "the first cell with execution_count is None"
    # (there isn't one here, since there are only 2 cells total).
    assert result.failure.cell_index == 1


def test_deprecation_warning_is_captured_but_does_not_fail(kernel_name):
    result = execute_notebook(_ref("warn_deprecated_api.ipynb"), kernel_name=kernel_name)
    assert result.status == "pass"
    assert any("DeprecationWarning" in line for line in result.stderr_warnings)


def test_seed_injection_is_stripped_from_executed_copy(kernel_name):
    result = execute_notebook(_ref("pass_clean.ipynb"), kernel_name=kernel_name, inject_seed=True)
    assert result.status == "pass"
    sources = [str(c.get("source", "")) for c in result.executed_nb.cells]
    assert not any("notebook-audit: injected" in s for s in sources)
    # First real cell should be the fixture's own first cell, not the seed cell.
    assert "import numpy as np" in sources[0]


def test_no_seed_injection_when_disabled(kernel_name):
    result = execute_notebook(_ref("pass_clean.ipynb"), kernel_name=kernel_name, inject_seed=False)
    assert result.status == "pass"
    assert len(result.executed_nb.cells) == 2  # exactly the fixture's own 2 cells
