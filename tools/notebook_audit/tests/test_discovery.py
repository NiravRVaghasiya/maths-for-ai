"""Unit tests for notebook_audit.discovery against the REAL repo tree.

These intentionally run against the actual curriculum (not a synthetic
fixture tree) since discovery's whole job is correctly enumerating the real
notebooks and excluding real scratch directories -- a synthetic fixture tree
would not exercise the actual exclusion list.

Deliberately NOT asserting exact hard-coded module/notebook counts: the
curriculum grows (e.g. module 13 was added after this harness was written),
and a hard-coded "== 89" turns every legitimate new-notebook PR red for the
wrong reason. Instead these assert structural invariants that stay true as
the curriculum grows.
"""

from __future__ import annotations

import re

from notebook_audit.discovery import discover_modules, discover_notebooks, repo_root

_MODULE_DIR_RE = re.compile(r"^\d{2}_")


def test_repo_root_contains_requirements_txt():
    assert (repo_root() / "requirements.txt").exists()


def test_discovered_modules_match_the_numbered_directories_on_disk():
    modules = discover_modules()
    # Every discovered module is a NN_ directory, and every NN_ directory on
    # disk (that isn't excluded scratch/tooling) is discovered.
    on_disk = {p.name for p in repo_root().iterdir() if p.is_dir() and _MODULE_DIR_RE.match(p.name)}
    assert set(modules) == on_disk
    # Sanity anchors: the first and a late module are present.
    assert "00_Prerequisites" in modules
    assert "12_Capstone_Projects" in modules


def test_excludes_scratch_and_tooling_directories():
    modules = discover_modules()
    for excluded in (".audit_tmp", "_templates", "tools", ".venv", ".github"):
        assert excluded not in modules


def test_total_notebook_count_equals_sum_over_modules():
    all_refs = discover_notebooks()
    per_module_total = sum(len(discover_notebooks(modules=[m])) for m in discover_modules())
    assert len(all_refs) == per_module_total
    # The curriculum is non-trivial; guard against discovery silently finding
    # nothing (e.g. a broken glob) without pinning an exact, brittle count.
    assert len(all_refs) >= 89


def test_notebook_ids_are_well_formed():
    refs = discover_notebooks(modules=["08_Advanced_Linear_Algebra"])
    ids = {r.notebook_id for r in refs}
    assert "08.02" in ids
    matrix_calculus = next(r for r in refs if r.notebook_id == "08.02")
    assert matrix_calculus.path.name == "02_matrix_calculus.ipynb"


def test_restricting_to_one_module_only_returns_that_modules_notebooks():
    refs = discover_notebooks(modules=["00_Prerequisites"])
    assert len(refs) == 4
    assert all(r.module == "00_Prerequisites" for r in refs)


def test_unknown_module_raises():
    import pytest

    with pytest.raises(ValueError):
        discover_notebooks(modules=["99_Does_Not_Exist"])
