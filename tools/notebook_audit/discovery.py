"""Notebook discovery for the reproducibility audit.

Finds every notebook that belongs to the curriculum (top-level ``NN_Name``
module directories) while explicitly excluding scratch/tooling directories.
Module directories are discovered dynamically (any top-level dir matching
``^\\d{2}_``) rather than hardcoded, so the harness keeps working if a new
module is added.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

# Directories that must never be treated as curriculum content, even if they
# happen to match the module-name pattern or contain .ipynb files.
EXCLUDED_DIR_NAMES = {
    ".audit_tmp",
    "_templates",
    ".ipynb_checkpoints",
    ".venv",
    "venv",
    ".git",
    ".github",
    "tools",
    "tests",
    "node_modules",
}

_MODULE_DIR_RE = re.compile(r"^\d{2}_")
_LEADING_DIGITS_RE = re.compile(r"^(\d+)")


def repo_root() -> Path:
    """Return the repository root, derived from this file's location.

    This file lives at ``<root>/tools/notebook_audit/discovery.py``.
    """
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class NotebookRef:
    """A single discovered notebook."""

    notebook_id: str  # e.g. "08.02"
    module: str  # e.g. "08_Advanced_Linear_Algebra"
    path: Path  # absolute path to the .ipynb file
    relative_path: str  # POSIX-style path relative to repo root, for reporting

    @property
    def name(self) -> str:
        return self.path.stem


def discover_modules(root: Optional[Path] = None) -> List[str]:
    """Return sorted module directory names (e.g. ``00_Prerequisites``)."""
    root = root or repo_root()
    modules = []
    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        if entry.name in EXCLUDED_DIR_NAMES:
            continue
        if _MODULE_DIR_RE.match(entry.name):
            modules.append(entry.name)
    return sorted(modules)


def _module_number(module_name: str) -> str:
    match = _LEADING_DIGITS_RE.match(module_name)
    return match.group(1) if match else "??"


def _notebook_number(file_stem: str) -> str:
    match = _LEADING_DIGITS_RE.match(file_stem)
    return match.group(1) if match else "??"


def discover_notebooks(
    modules: Optional[Sequence[str]] = None, root: Optional[Path] = None
) -> List[NotebookRef]:
    """Discover all curriculum notebooks, optionally restricted to a subset
    of module directory names.

    Notebooks are found via a non-recursive glob per module directory, since
    the curriculum keeps all notebooks flat inside their module folder (no
    nested subfolders), which also naturally avoids ``.ipynb_checkpoints``
    (a hidden subfolder, never matched by a non-recursive ``*.ipynb`` glob).
    """
    root = root or repo_root()
    all_modules = discover_modules(root)
    selected = list(modules) if modules else all_modules

    unknown = set(selected) - set(all_modules)
    if unknown:
        raise ValueError(f"Unknown module(s) requested: {sorted(unknown)}")

    refs: List[NotebookRef] = []
    for module in selected:
        module_dir = root / module
        module_num = _module_number(module)
        for nb_path in sorted(module_dir.glob("*.ipynb")):
            if nb_path.name.startswith("."):
                continue
            nb_num = _notebook_number(nb_path.stem)
            notebook_id = f"{module_num}.{nb_num}"
            refs.append(
                NotebookRef(
                    notebook_id=notebook_id,
                    module=module,
                    path=nb_path,
                    relative_path=nb_path.relative_to(root).as_posix(),
                )
            )
    return refs


def representative_notebooks(
    modules: Optional[Sequence[str]] = None, root: Optional[Path] = None
) -> List[NotebookRef]:
    """Return one representative notebook per module (the first, by sort order).

    Used by the fast PR CI tier to get broad, cheap coverage: executing the
    first notebook of every module exercises each module's own setup/imports
    and catches gross breakage (a missing dependency, a module-wide API change)
    without paying to run all ~100 notebooks on every push. The full suite runs
    in the scheduled/nightly tier instead.

    The "first" notebook per module is a deterministic, dependency-light choice:
    notebooks are numbered so that ``NN_01`` is the module's foundational
    notebook, which by construction has the fewest intra-module prerequisites.
    """
    refs = discover_notebooks(modules=modules, root=root)
    first_per_module: dict[str, NotebookRef] = {}
    for ref in refs:  # refs are already sorted by module then notebook number
        if ref.module not in first_per_module:
            first_per_module[ref.module] = ref
    return [first_per_module[m] for m in sorted(first_per_module)]
