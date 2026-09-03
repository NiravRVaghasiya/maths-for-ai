"""Cross-run reproducibility checking.

Executes a notebook twice with the same injected seed and diffs the two
runs' *numeric* stdout output. This is deliberately a separate, opt-in check
(``--check-determinism``) from the main pass/fail matrix run, since running
every notebook twice roughly doubles CI time -- the main run answers "does
it execute correctly", this answers "does it produce the same numbers every
time", which is a distinct question worth its own CI job (see
``.github/workflows/notebook-determinism.yml``).

Comparison strategy: extract every floating-point-looking token from stdout
stream outputs in both runs and compare them numerically with a tolerance,
rather than a byte-for-byte string diff. This avoids false positives from
things that are expected to legitimately differ between runs even when the
underlying computation is fully deterministic (wall-clock timings printed by
a few notebooks, e.g. "13.44 ms", object id()s in repr() output, dict/set
iteration order pre-3.7 semantics that don't apply here but are worth
guarding against generally). A byte-diff would flag those as
"non-reproducible" even though the actual mathematical content is identical
run to run.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Tuple

from .executor import NotebookResult

_FLOAT_TOKEN_RE = re.compile(r"-?\d+\.\d+(?:[eE][+-]?\d+)?")

# Lines containing these substrings are expected to vary run-to-run for
# reasons unrelated to reproducibility (wall-clock timing measurements this
# repo's own notebooks intentionally print, e.g. 08.02's benchmark, 08.05/
# 08.06's timing comparisons) and are excluded from the numeric diff.
_TIMING_LINE_HINTS = re.compile(r"\bms\b|\bsec(?:ond)?s?\b|elapsed|wall.?clock", re.IGNORECASE)


@dataclass
class ReproducibilityDiff:
    notebook_id: str
    relative_path: str
    is_reproducible: bool
    diff_count: int
    sample_diffs: List[Tuple[str, str]]


def _stdout_lines(result: NotebookResult) -> List[str]:
    lines: List[str] = []
    if result.executed_nb is None:
        return lines
    for cell in result.executed_nb.cells:
        if cell.get("cell_type") != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") == "stream" and output.get("name") == "stdout":
                lines.extend(output.get("text", "").splitlines())
    return lines


def compare_runs(
    notebook_id: str, relative_path: str, run_a: NotebookResult, run_b: NotebookResult
) -> ReproducibilityDiff:
    """Compare stdout numeric content between two executions of the same notebook."""
    lines_a = [line for line in _stdout_lines(run_a) if not _TIMING_LINE_HINTS.search(line)]
    lines_b = [line for line in _stdout_lines(run_b) if not _TIMING_LINE_HINTS.search(line)]

    diffs: List[Tuple[str, str]] = []
    for line_a, line_b in zip(lines_a, lines_b):
        if line_a == line_b:
            continue
        floats_a = [float(t) for t in _FLOAT_TOKEN_RE.findall(line_a)]
        floats_b = [float(t) for t in _FLOAT_TOKEN_RE.findall(line_b)]
        if len(floats_a) != len(floats_b):
            diffs.append((line_a, line_b))
            continue
        if any(abs(fa - fb) > 1e-6 * max(1.0, abs(fa)) for fa, fb in zip(floats_a, floats_b)):
            diffs.append((line_a, line_b))
            continue
        # Same numbers (within tolerance) but different surrounding text
        # (e.g. non-numeric formatting drift) still counts as a real diff.
        stripped_a = _FLOAT_TOKEN_RE.sub("<num>", line_a)
        stripped_b = _FLOAT_TOKEN_RE.sub("<num>", line_b)
        if stripped_a != stripped_b:
            diffs.append((line_a, line_b))

    if len(lines_a) != len(lines_b):
        diffs.append((f"<{len(lines_a)} stdout lines>", f"<{len(lines_b)} stdout lines>"))

    return ReproducibilityDiff(
        notebook_id=notebook_id,
        relative_path=relative_path,
        is_reproducible=len(diffs) == 0,
        diff_count=len(diffs),
        sample_diffs=diffs[:5],
    )
