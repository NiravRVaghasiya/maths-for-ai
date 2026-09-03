#!/usr/bin/env python3
"""Structural validation of every curriculum notebook via nbformat.

Reads each notebook and runs ``nbformat.validate`` on it, catching corrupt or
schema-invalid notebooks (bad JSON, missing required fields, wrong nbformat
version) before anything tries to execute them. This is a cheap, execution-free
gate in the CI "code-quality" job.

Exits 0 if every notebook is structurally valid, 1 otherwise, printing one line
per notebook so a failure points directly at the offending file.

Run locally with:

    python tools/ci/validate_notebooks.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat

# Directories that are not curriculum content and should be skipped. Mirrors
# tools/notebook_audit/discovery.EXCLUDED_DIR_NAMES so the two stay consistent.
EXCLUDED_DIR_PARTS = {
    ".audit_tmp",
    "_templates",
    ".ipynb_checkpoints",
    ".venv",
    "venv",
    ".git",
    ".github",
    "node_modules",
}


def repo_root() -> Path:
    # This file lives at <root>/tools/ci/validate_notebooks.py
    return Path(__file__).resolve().parents[2]


def is_excluded(path: Path, root: Path) -> bool:
    rel_parts = set(path.relative_to(root).parts)
    return bool(rel_parts & EXCLUDED_DIR_PARTS)


def main() -> int:
    root = repo_root()
    failed = False
    checked = 0

    for path in sorted(root.rglob("*.ipynb")):
        if is_excluded(path, root):
            continue
        # Skip the audit harness's own test fixtures: several are intentionally
        # malformed to test the classifier and would fail structural validation
        # by design.
        if "notebook_audit" in path.parts and "fixtures" in path.parts:
            continue
        checked += 1
        rel = path.relative_to(root).as_posix()
        try:
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            print(f"OK   {rel}")
        except Exception as exc:  # noqa: BLE001 - report any validation failure
            print(f"FAIL {rel}: {exc}")
            failed = True

    print(f"\nChecked {checked} notebook(s).")
    if failed:
        print("Notebook structural validation FAILED.", file=sys.stderr)
        return 1
    print("All notebooks are structurally valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
