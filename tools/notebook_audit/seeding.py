"""Deterministic seed injection.

The audit harness never edits notebook files on disk. Instead, it prepends a
synthetic "seed cell" to the in-memory notebook object immediately before
execution. That cell seeds every RNG source used anywhere in the curriculum
(confirmed by repo-wide source scan: ``numpy``/``numpy.random.default_rng``,
``torch``, and stdlib ``random``) so that:

- Notebooks that already self-seed (the vast majority; see
  ``docs/NOTEBOOK_AUDIT.md``) get a harmless, idempotent extra seed call.
- Notebooks that *don't* self-seed still execute deterministically under the
  audit, so a real reproducibility regression shows up as a genuine
  cross-run numeric diff (see ``--check-determinism``) rather than noise from
  the harness itself.

The synthetic cell is stripped back out before any "executed copy" of a
notebook is written to the reports directory, so on-disk artifacts always
reflect only the notebook's own authored cells plus their outputs.
"""

from __future__ import annotations

import nbformat

SEED_CELL_MARKER = (
    "# --- notebook-audit: injected determinism seed (not part of the source notebook) ---"
)

_SEED_CELL_TEMPLATE = """{marker}
import os as _audit_os
_audit_os.environ.setdefault("PYTHONHASHSEED", "{seed}")

import random as _audit_random
_audit_random.seed({seed})

import numpy as _audit_np
_audit_np.random.seed({seed})

try:
    import torch as _audit_torch
    _audit_torch.manual_seed({seed})
    if hasattr(_audit_torch, "use_deterministic_algorithms"):
        _audit_torch.use_deterministic_algorithms(True, warn_only=True)
    if hasattr(_audit_torch, "cuda") and _audit_torch.cuda.is_available():
        _audit_torch.cuda.manual_seed_all({seed})
except ImportError:
    pass

del _audit_os, _audit_random, _audit_np
"""


def build_seed_cell(seed: int) -> nbformat.NotebookNode:
    """Build the in-memory-only seed cell for the given seed value."""
    source = _SEED_CELL_TEMPLATE.format(marker=SEED_CELL_MARKER, seed=seed)
    return nbformat.v4.new_code_cell(source=source)


def inject_seed_cell(nb: nbformat.NotebookNode, seed: int) -> None:
    """Prepend a synthetic seed cell to ``nb.cells`` in place.

    Only mutates the in-memory notebook object; never touches the file on
    disk (callers are expected to have loaded ``nb`` themselves and to write
    executed copies, if any, to a separate reports directory).
    """
    nb.cells.insert(0, build_seed_cell(seed))


def strip_injected_cells(nb: nbformat.NotebookNode) -> nbformat.NotebookNode:
    """Return a copy of ``nb`` with any injected seed cells removed.

    Used when writing an "executed copy" artifact so it reflects only the
    notebook's own authored content.
    """
    nb = nbformat.from_dict(nb)  # deep-ish copy via round-trip through dict
    nb.cells = [
        cell
        for cell in nb.cells
        if not (
            cell.get("cell_type") == "code"
            and str(cell.get("source", "")).startswith(SEED_CELL_MARKER)
        )
    ]
    return nb
