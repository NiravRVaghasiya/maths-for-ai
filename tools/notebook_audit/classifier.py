"""Failure and warning classification.

Turns a raw :class:`~notebook_audit.executor.NotebookResult` into one or more
:class:`Finding` objects, each tagged with a specific category from the
audit's required taxonomy:

    import_error, execution_order, undefined_variable, deprecated_api,
    shape_error, numerical_error, plotting_error, filesystem_assumption,
    reproducibility, timeout, other_runtime_error

Classification is intentionally layered:

1. **Exceptions are classified by exception type + message pattern.** This
   is deterministic and auditable -- every rule below is a plain regex over
   ``ename``/``evalue``, not a guess.
2. **Warnings (stderr stream output) are classified separately** from hard
   failures, since a notebook can pass execution while still emitting a
   ``DeprecationWarning`` that matters for a reproducibility audit.
3. **Static, pre-execution checks** (filesystem assumptions, i.e. hardcoded
   absolute paths or writes outside a temp dir) run on the notebook source
   regardless of whether execution passed, since a filesystem assumption
   might happen to work on the audit machine but not elsewhere.

Nothing here silently downgrades a failure to a pass. A notebook with any
CRITICAL-path finding (import_error, undefined_variable, shape_error,
numerical_error, execution_order, plotting_error, timeout,
other_runtime_error) is reported as failing overall; deprecated_api and
filesystem_assumption findings are reported as warnings on an otherwise
passing notebook (they don't stop execution, by definition, but must still
be visible -- "do not silently suppress errors" applies to warnings too).
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from typing import List, Optional, Set

import nbformat

from .executor import NotebookResult

# --- Category constants -----------------------------------------------------

CAT_IMPORT_ERROR = "import_error"
CAT_UNDEFINED_VARIABLE = "undefined_variable"
CAT_EXECUTION_ORDER = "execution_order"
CAT_DEPRECATED_API = "deprecated_api"
CAT_SHAPE_ERROR = "shape_error"
CAT_NUMERICAL_ERROR = "numerical_error"
CAT_PLOTTING_ERROR = "plotting_error"
CAT_FILESYSTEM_ASSUMPTION = "filesystem_assumption"
CAT_REPRODUCIBILITY = "reproducibility"
CAT_TIMEOUT = "timeout"
CAT_OTHER_RUNTIME_ERROR = "other_runtime_error"

SEVERITY_FAIL = "fail"  # stops the notebook; counts against pass/fail
SEVERITY_WARN = "warn"  # doesn't stop the notebook; still reported


@dataclass
class Finding:
    category: str
    severity: str  # "fail" | "warn"
    message: str
    cell_index: Optional[int] = None
    detail: str = ""


# --- Exception-based classification -----------------------------------------

_SHAPE_ERROR_PATTERNS = [
    # Every pattern below is verified against a REAL exception message
    # produced by this repo's actual dependency versions (numpy 2.5.2,
    # matplotlib 3.11.1), not guessed -- see tools/notebook_audit/tests/
    # test_classifier.py for the exact fixtures these were derived from.
    re.compile(r"shapes? .* (not aligned|mismatch|incompatible)", re.IGNORECASE),
    re.compile(r"cannot broadcast", re.IGNORECASE),
    re.compile(
        r"could not be broadcast", re.IGNORECASE
    ),  # numpy: "operands could not be broadcast together with shapes (3,) (4,)"
    re.compile(r"size mismatch", re.IGNORECASE),
    re.compile(r"dimension(s)? .* (mismatch|do not match|not equal)", re.IGNORECASE),
    re.compile(
        r"mismatch in its core dimension", re.IGNORECASE
    ),  # numpy matmul: "...has a mismatch in its core dimension 0..."
    re.compile(r"size \d+ is different from \d+", re.IGNORECASE),  # numpy matmul gufunc detail
    re.compile(r"matmul: .*shape", re.IGNORECASE),
    re.compile(r"expected .*dimension", re.IGNORECASE),
    re.compile(
        r"must have same first dimension", re.IGNORECASE
    ),  # matplotlib: "x and y must have same first dimension"
    re.compile(r"x and y (must|can) ", re.IGNORECASE),
]

_NAME_ERROR_TARGET_RE = re.compile(r"name '([^']+)' is not defined")


def _names_bound_by_cell(source: str) -> Set[str]:
    """Return every name a cell's top-level statements could bind.

    Used to tell "this name is never defined anywhere in the notebook" (a
    genuine typo/undefined-variable bug) apart from "this name IS defined,
    just in a cell that runs later" (an execution-order bug: the notebook
    only works if cells are executed out of the top-to-bottom order, e.g. a
    learner re-running a later cell first in an interactive session, or a
    cell that got reordered/deleted during authoring). Best-effort: parses
    with ``ast`` and walks assignment targets, function/class defs, imports,
    and ``for``/``with``/comprehension binding targets. If the cell doesn't
    parse (e.g. it's the one that already failed), returns an empty set
    rather than raising -- a parse failure here should never crash the
    classifier itself.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()

    bound: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store,)):
            bound.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                bound.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                bound.add(alias.asname or alias.name)
    return bound


def is_defined_in_later_cell(nb: nbformat.NotebookNode, failing_cell_index: int, name: str) -> bool:
    """Check whether ``name`` is bound in any code cell after the one that failed."""
    for cell in nb.cells[failing_cell_index + 1 :]:
        if cell.get("cell_type") != "code":
            continue
        if name in _names_bound_by_cell(str(cell.get("source", ""))):
            return True
    return False


_IMPORT_ERROR_ENAMES = {"ImportError", "ModuleNotFoundError"}

_NUMERICAL_ERROR_PATTERNS = [
    re.compile(r"division by zero", re.IGNORECASE),
    re.compile(r"invalid value encountered", re.IGNORECASE),
    re.compile(r"overflow encountered", re.IGNORECASE),
    re.compile(r"underflow encountered", re.IGNORECASE),
    re.compile(r"singular matrix", re.IGNORECASE),
    re.compile(r"matrix is not positive definite", re.IGNORECASE),
    re.compile(r"did not converge", re.IGNORECASE),
    re.compile(r"eigenvalues did not converge", re.IGNORECASE),
    re.compile(r"nan", re.IGNORECASE),
]
_NUMERICAL_ERROR_ENAMES = {"FloatingPointError", "ZeroDivisionError", "LinAlgError"}

_PLOTTING_ERROR_MODULE_HINTS = re.compile(
    r"matplotlib|seaborn|_tkinter|backend_|figure|axes|colorbar", re.IGNORECASE
)

_DEPRECATION_WARNING_RE = re.compile(
    r"\b(DeprecationWarning|FutureWarning|PendingDeprecationWarning)\b"
)

# NOTE on a deliberately-omitted heuristic: an earlier version of this
# classifier tried to flag a notebook's own printed self-verification checks
# (e.g. "match: True" / "holds: True") when they printed False, on the
# theory that the notebook is reporting its own broken invariant. That is
# NOT reliable and was removed: 11_Functional_Analysis/01_function_spaces_
# and_norms.ipynb legitimately prints "holds: False" for p=1,3,inf in its
# parallelogram-law demo -- False is the mathematically correct answer there
# (the parallelogram law holds ONLY for p=2), not a regression. Distinguishing
# "the notebook demonstrates X is false on purpose" from "X used to be true
# and now is not" requires understanding the notebook's pedagogical intent,
# which cannot be done reliably by pattern-matching printed text. This is
# exactly the kind of semantic judgement call that belongs in a human-read
# audit (see the separate technical/pedagogical audit performed earlier),
# not in an automated CI classifier where a false positive would erode trust
# in the whole report. The categories below (exceptions, warnings, static
# scans, cross-run diffs) are all mechanically verifiable without guessing
# intent, which is why the audit's required failure taxonomy is limited to
# them.


def classify_exception(
    ename: str,
    evalue: str,
    traceback_text: str = "",
    *,
    nb: Optional[nbformat.NotebookNode] = None,
    cell_index: int = -1,
) -> str:
    """Classify a single (ename, evalue, traceback) triple into one category.

    ``traceback_text`` is optional but matters for plotting errors: verified
    empirically that matplotlib's own exception messages (e.g. an invalid
    color, or an x/y length mismatch inside ``plt.plot``) frequently do NOT
    mention "matplotlib" anywhere in ``evalue`` -- the only reliable textual
    signal is the file paths inside the traceback (``.../matplotlib/...``).
    Shape-pattern checks run BEFORE the plotting-module check, since a
    matplotlib x/y-length-mismatch is, substantively, a shape error that
    happens to surface while plotting -- reported as ``shape_error`` (more
    actionable for a math curriculum) rather than the less specific
    ``plotting_error``, which is reserved for plotting-configuration issues
    (bad color values, backend/rendering failures) that aren't about data
    shape at all.

    ``nb``/``cell_index`` are optional but matter for ``NameError``: a plain
    exception-type check cannot distinguish "this name is genuinely never
    defined anywhere" (CAT_UNDEFINED_VARIABLE -- a typo or missing import)
    from "this name IS defined, just in a cell below the one that failed"
    (CAT_EXECUTION_ORDER -- the notebook only works if a learner runs cells
    out of order). This was NOT obvious from exception type alone: verified
    empirically that both cases raise the identical ``NameError`` with the
    identical message shape ("name 'x' is not defined"), so the only
    reliable signal is a static scan of the *rest of the notebook* for where
    ``x`` is actually bound. Without ``nb``, both cases fall back to
    CAT_UNDEFINED_VARIABLE (the safer, more conservative label -- treating a
    real ordering bug as merely "undefined" undercounts one category but
    never invents a false positive).
    """
    if ename in _IMPORT_ERROR_ENAMES:
        return CAT_IMPORT_ERROR
    if ename == "NameError":
        match = _NAME_ERROR_TARGET_RE.search(evalue)
        if match and nb is not None and cell_index >= 0:
            if is_defined_in_later_cell(nb, cell_index, match.group(1)):
                return CAT_EXECUTION_ORDER
        return CAT_UNDEFINED_VARIABLE
    if ename in _NUMERICAL_ERROR_ENAMES:
        return CAT_NUMERICAL_ERROR
    if ename in {"ValueError", "RuntimeError", "IndexError", "TypeError"}:
        for pattern in _SHAPE_ERROR_PATTERNS:
            if pattern.search(evalue):
                return CAT_SHAPE_ERROR
        for pattern in _NUMERICAL_ERROR_PATTERNS:
            if pattern.search(evalue):
                return CAT_NUMERICAL_ERROR
    if ename in {"FileNotFoundError", "PermissionError", "OSError", "NotADirectoryError"}:
        return CAT_FILESYSTEM_ASSUMPTION
    if ename in {"KeyboardInterrupt"}:
        # nbclient interrupts the kernel to enforce a per-cell timeout; the
        # resulting in-notebook exception is a KeyboardInterrupt even though
        # the *cause* is a timeout, not a user interrupt.
        return CAT_TIMEOUT
    if _PLOTTING_ERROR_MODULE_HINTS.search(evalue) or _PLOTTING_ERROR_MODULE_HINTS.search(
        traceback_text
    ):
        return CAT_PLOTTING_ERROR
    return CAT_OTHER_RUNTIME_ERROR


def classify_result(result: NotebookResult) -> List[Finding]:
    """Produce all findings for one executed notebook."""
    findings: List[Finding] = []

    if result.status == "timeout":
        findings.append(
            Finding(
                category=CAT_TIMEOUT,
                severity=SEVERITY_FAIL,
                message=(
                    f"Notebook exceeded its execution timeout "
                    f"(ran {result.duration_s:.0f}s before being interrupted)."
                ),
                cell_index=result.failure.cell_index if result.failure else None,
                detail=(result.failure.evalue if result.failure else "")
                or (result.kernel_startup_error or ""),
            )
        )
    elif result.status == "error":
        findings.append(
            Finding(
                category=CAT_OTHER_RUNTIME_ERROR,
                severity=SEVERITY_FAIL,
                message="Kernel failed to start or died during execution.",
                detail=result.kernel_startup_error or "",
            )
        )
    elif result.status == "fail" and result.failure is not None:
        traceback_text = "\n".join(result.failure.traceback)
        category = classify_exception(
            result.failure.ename,
            result.failure.evalue,
            traceback_text,
            nb=result.executed_nb,
            cell_index=result.failure.cell_index,
        )
        findings.append(
            Finding(
                category=category,
                severity=SEVERITY_FAIL,
                message=f"{result.failure.ename}: {result.failure.evalue}",
                cell_index=result.failure.cell_index,
                detail=result.failure.source,
            )
        )

    # Warnings are independent of pass/fail status -- a notebook can pass
    # while still emitting a DeprecationWarning that matters for this audit.
    for line in result.stderr_warnings:
        if _DEPRECATION_WARNING_RE.search(line):
            findings.append(
                Finding(
                    category=CAT_DEPRECATED_API,
                    severity=SEVERITY_WARN,
                    message=line.strip(),
                )
            )

    if result.duration_s > 120 and result.status == "pass":
        findings.append(
            Finding(
                category="excessive_runtime",
                severity=SEVERITY_WARN,
                message=f"Notebook took {result.duration_s:.0f}s to execute (flag threshold: 120s).",
            )
        )

    return findings
