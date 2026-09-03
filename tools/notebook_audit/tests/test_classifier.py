"""Tests for notebook_audit.classifier, run against REAL kernel executions.

Every expected category below was verified against the actual exception
text a real, currently-installed dependency version produces (see the probe
scripts referenced in the audit's working notes) before being encoded as an
assertion here -- none of these are guessed from documentation or memory of
what an error "usually" looks like.
"""

from __future__ import annotations

from notebook_audit.classifier import (
    CAT_DEPRECATED_API,
    CAT_EXECUTION_ORDER,
    CAT_IMPORT_ERROR,
    CAT_NUMERICAL_ERROR,
    CAT_PLOTTING_ERROR,
    CAT_SHAPE_ERROR,
    CAT_TIMEOUT,
    CAT_UNDEFINED_VARIABLE,
    classify_result,
)
from notebook_audit.discovery import NotebookRef
from notebook_audit.executor import execute_notebook

from .conftest import fixture_path


def _ref(name: str) -> NotebookRef:
    path = fixture_path(name)
    return NotebookRef(notebook_id="99.00", module="_fixtures", path=path, relative_path=name)


def _fail_categories(result) -> set:
    return {f.category for f in classify_result(result) if f.severity == "fail"}


def test_clean_notebook_has_no_fail_findings(kernel_name):
    result = execute_notebook(_ref("pass_clean.ipynb"), kernel_name=kernel_name)
    assert _fail_categories(result) == set()


def test_import_error_classified(kernel_name):
    result = execute_notebook(_ref("fail_import_error.ipynb"), kernel_name=kernel_name)
    assert CAT_IMPORT_ERROR in _fail_categories(result)


def test_genuinely_undefined_variable_classified(kernel_name):
    result = execute_notebook(_ref("fail_undefined_variable.ipynb"), kernel_name=kernel_name)
    assert CAT_UNDEFINED_VARIABLE in _fail_categories(result)


def test_variable_defined_in_later_cell_classified_as_execution_order(kernel_name):
    result = execute_notebook(_ref("fail_execution_order.ipynb"), kernel_name=kernel_name)
    categories = _fail_categories(result)
    assert CAT_EXECUTION_ORDER in categories
    assert CAT_UNDEFINED_VARIABLE not in categories


def test_shape_mismatch_classified(kernel_name):
    result = execute_notebook(_ref("fail_shape_error.ipynb"), kernel_name=kernel_name)
    assert CAT_SHAPE_ERROR in _fail_categories(result)


def test_singular_matrix_classified_as_numerical_error(kernel_name):
    result = execute_notebook(_ref("fail_numerical_error.ipynb"), kernel_name=kernel_name)
    assert CAT_NUMERICAL_ERROR in _fail_categories(result)


def test_invalid_plot_color_classified_as_plotting_error(kernel_name):
    result = execute_notebook(_ref("fail_plotting_error.ipynb"), kernel_name=kernel_name)
    assert CAT_PLOTTING_ERROR in _fail_categories(result)


def test_timeout_classified(kernel_name):
    result = execute_notebook(
        _ref("fail_timeout.ipynb"), kernel_name=kernel_name, cell_timeout_s=3, inject_seed=False
    )
    assert CAT_TIMEOUT in _fail_categories(result)


def test_deprecation_warning_classified_as_warn_not_fail(kernel_name):
    result = execute_notebook(_ref("warn_deprecated_api.ipynb"), kernel_name=kernel_name)
    findings = classify_result(result)
    warn_categories = {f.category for f in findings if f.severity == "warn"}
    fail_categories = {f.category for f in findings if f.severity == "fail"}
    assert CAT_DEPRECATED_API in warn_categories
    assert fail_categories == set()  # a warning alone must never fail the notebook
