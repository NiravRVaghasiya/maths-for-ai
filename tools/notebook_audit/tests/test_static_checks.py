"""Unit tests for notebook_audit.static_checks (no kernel execution needed)."""

from __future__ import annotations

from notebook_audit.classifier import CAT_FILESYSTEM_ASSUMPTION
from notebook_audit.static_checks import scan_notebook_source

from .conftest import fixture_path


def test_hardcoded_windows_path_is_flagged():
    findings = scan_notebook_source(
        fixture_path("warn_filesystem_assumption.ipynb"),
        notebook_id="99.00",
        relative_path="warn_filesystem_assumption.ipynb",
    )
    assert any(f.category == CAT_FILESYSTEM_ASSUMPTION for f in findings)
    assert all(f.severity == "warn" for f in findings)  # never a hard fail on its own


def test_clean_notebook_has_no_filesystem_findings():
    findings = scan_notebook_source(
        fixture_path("pass_clean.ipynb"),
        notebook_id="99.00",
        relative_path="pass_clean.ipynb",
    )
    assert findings == []


def test_colab_markdown_link_and_prose_path_are_not_false_positives():
    """A Colab badge URL and a plain-prose absolute path mentioned in a
    markdown cell must never be mistaken for a filesystem write -- markdown
    cells are intentionally excluded from the scan, only code cells are
    inspected."""
    findings = scan_notebook_source(
        fixture_path("pass_with_colab_markdown_link.ipynb"),
        notebook_id="99.00",
        relative_path="pass_with_colab_markdown_link.ipynb",
    )
    assert findings == []
