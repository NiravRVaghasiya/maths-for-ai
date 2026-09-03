"""Notebook execution engine.

Executes a single notebook in a fresh, isolated kernel using ``nbclient``
directly (not via ``papermill``/``nbconvert`` CLI subprocesses) so that this
module has direct programmatic access to per-cell outputs, timing, and
exceptions with nothing silently swallowed.

Design choices, and why:

- One fresh kernel process per notebook (``NotebookClient`` starts and
  shuts down its own ``KernelManager`` unless one is passed in). This
  matches "execute every notebook from start to finish" in a clean state and
  avoids state leaking between notebooks (a real execution-order-bug risk if
  a shared kernel were reused).
- Errors are never caught-and-discarded: ``CellExecutionError`` is caught
  only to extract structured fields (cell index, ename, evalue, traceback)
  before being re-raised information into the ``NotebookResult``; the
  underlying notebook object still carries the real ``error`` output cell
  for the report/artifact.
- A hard wall-clock timeout applies per notebook (default 900s) *and* nbclient
  applies a per-cell timeout (default 300s) so one runaway cell cannot hang
  the whole matrix run silently.
- Windows' default Proactor asyncio event loop does not support the
  ``add_reader`` calls pyzmq needs; nbclient works around this with an extra
  thread but it is faster and quieter to switch to the Selector policy up
  front on win32 (verified empirically against this environment).
"""

from __future__ import annotations

import asyncio
import sys
import time
import traceback
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError, CellTimeoutError, DeadKernelError

from .discovery import NotebookRef
from .seeding import inject_seed_cell, strip_injected_cells

if sys.platform == "win32":
    # pyzmq's default async transport needs add_reader/add_writer, which the
    # default ProactorEventLoop on Windows does not implement. Without this,
    # nbclient still works (it falls back to a polling thread) but emits a
    # RuntimeWarning per kernel and is measurably slower to tear down.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


DEFAULT_CELL_TIMEOUT_S = 300
DEFAULT_NOTEBOOK_TIMEOUT_S = 900
SLOW_NOTEBOOK_THRESHOLD_S = 120  # flagged as "excessive runtime" in the report


@dataclass
class CellFailure:
    """Structured detail about the cell that stopped execution, if any."""

    cell_index: int
    ename: str
    evalue: str
    traceback: List[str] = field(default_factory=list)
    source: str = ""


@dataclass
class NotebookResult:
    """Outcome of executing a single notebook."""

    notebook: NotebookRef
    status: str  # "pass" | "fail" | "timeout" | "error"
    duration_s: float
    failure: Optional[CellFailure] = None
    stderr_warnings: List[str] = field(default_factory=list)
    kernel_startup_error: Optional[str] = None
    executed_nb: Optional[nbformat.NotebookNode] = None

    @property
    def passed(self) -> bool:
        return self.status == "pass"


def _collect_stderr_warning_lines(nb: nbformat.NotebookNode) -> List[str]:
    """Pull every stderr stream line out of every cell's outputs.

    This is how Python warnings (DeprecationWarning, FutureWarning, etc.)
    surface under nbclient: they are written to the kernel's stderr stream
    and captured as a ``stream`` output with ``name == "stderr"``, not
    raised as exceptions. Confirmed empirically against this repo's nbclient
    version (0.11.0) before relying on it for classification.
    """
    lines: List[str] = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") == "stream" and output.get("name") == "stderr":
                text = output.get("text", "")
                lines.extend(line for line in text.splitlines() if line.strip())
    return lines


def execute_notebook(
    ref: NotebookRef,
    *,
    seed: int = 0,
    cell_timeout_s: int = DEFAULT_CELL_TIMEOUT_S,
    notebook_timeout_s: int = DEFAULT_NOTEBOOK_TIMEOUT_S,
    kernel_name: str = "python3",
    inject_seed: bool = True,
) -> NotebookResult:
    """Execute one notebook top-to-bottom in a fresh kernel.

    Nothing about failures is suppressed: any ``CellExecutionError`` is
    captured with full structured detail (cell index/ename/evalue/traceback)
    and the underlying notebook's own ``error`` output cell is preserved
    unmodified in ``executed_nb`` for reporting.
    """
    nb = nbformat.read(str(ref.path), as_version=4)
    if inject_seed:
        inject_seed_cell(nb, seed)

    client = NotebookClient(
        nb,
        timeout=cell_timeout_s,
        kernel_name=kernel_name,
        resources={"metadata": {"path": str(ref.path.parent)}},
        allow_errors=False,  # never silently continue past a failing cell
        record_timing=True,
    )

    start = time.monotonic()
    status = "pass"
    failure: Optional[CellFailure] = None
    kernel_startup_error: Optional[str] = None

    try:
        _run_with_wall_clock_timeout(client, notebook_timeout_s)
    except CellTimeoutError as exc:
        status = "timeout"
        failure = _failure_from_notebook_scan(nb, fallback_evalue=str(exc))
    except CellExecutionError as exc:
        status = "fail"
        failure = _failure_from_notebook_scan(
            nb, fallback_ename=exc.ename, fallback_evalue=exc.evalue
        )
    except DeadKernelError as exc:
        status = "error"
        kernel_startup_error = f"Kernel died during execution: {exc}"
    except TimeoutError as exc:
        status = "timeout"
        kernel_startup_error = str(exc)
    except Exception as exc:  # kernel failed to even start, etc. -- still reported, never swallowed
        status = "error"
        kernel_startup_error = f"{type(exc).__name__}: {exc}\n" + traceback.format_exc()
    finally:
        duration = time.monotonic() - start

    result_nb = nb if inject_seed is False else strip_injected_cells(nb)

    # INVARIANT: CellFailure.cell_index must always index into
    # result_nb.cells (== NotebookResult.executed_nb.cells), never into the
    # raw `nb` that may still contain the injected seed cell as cells[0].
    # _failure_from_notebook_scan() necessarily computes its index against
    # `nb` (the seed cell has already been injected by that point), so it
    # must be shifted back by 1 whenever a seed cell was injected. This was
    # caught by test_classifier.py's execution-order test actually failing
    # against the real (stripped) executed_nb, not assumed correct from
    # reading the code -- see docs/NOTEBOOK_AUDIT.md's "lessons" section.
    if inject_seed and failure is not None:
        if failure.cell_index == 0:
            # The seed cell itself failed (e.g. torch totally unimportable
            # in this environment) -- not attributable to any authored
            # cell. -1 signals "no authored cell", callers must handle it.
            failure = CellFailure(
                cell_index=-1,
                ename=failure.ename,
                evalue=failure.evalue,
                traceback=failure.traceback,
                source=failure.source,
            )
        elif failure.cell_index > 0:
            failure = CellFailure(
                cell_index=failure.cell_index - 1,
                ename=failure.ename,
                evalue=failure.evalue,
                traceback=failure.traceback,
                source=failure.source,
            )

    return NotebookResult(
        notebook=ref,
        status=status,
        duration_s=duration,
        failure=failure,
        stderr_warnings=_collect_stderr_warning_lines(nb),
        kernel_startup_error=kernel_startup_error,
        executed_nb=result_nb,
    )


def _run_with_wall_clock_timeout(client: NotebookClient, notebook_timeout_s: int) -> None:
    """Run ``client.execute()`` but also enforce a whole-notebook deadline.

    ``nbclient``'s own ``timeout`` kwarg is a *per-cell* timeout; a notebook
    with many cells each just under that limit could otherwise run
    unboundedly long. We additionally bound the *entire* execution using a
    background-thread watchdog that kills the kernel if the deadline passes,
    since ``NotebookClient.execute()`` itself is a blocking call.
    """
    import threading

    exc_holder: Dict[str, BaseException] = {}

    def _target() -> None:
        try:
            client.execute()
        except BaseException as exc:  # re-raised on the calling thread below
            exc_holder["exc"] = exc

    thread = threading.Thread(target=_target, daemon=True)
    thread.start()
    thread.join(timeout=notebook_timeout_s)

    if thread.is_alive():
        # Whole-notebook deadline exceeded. Best-effort kernel teardown so we
        # don't leak a runaway process, then surface a clear timeout error.
        try:
            if client.km is not None:
                client.km.interrupt_kernel()
                time.sleep(1)
                client.km.shutdown_kernel(now=True)
        except Exception:
            pass
        raise TimeoutError(
            f"Notebook exceeded the {notebook_timeout_s}s whole-notebook timeout "
            "(this is the outer wall-clock limit, separate from the per-cell timeout)."
        )

    if "exc" in exc_holder:
        raise exc_holder["exc"]


def _failure_from_notebook_scan(
    nb: nbformat.NotebookNode,
    *,
    fallback_ename: str = "",
    fallback_evalue: str = "",
) -> CellFailure:
    """Locate the failing cell by scanning for an ``error`` output.

    Neither ``CellExecutionError`` nor ``CellTimeoutError`` carry a cell
    index (verified by inspecting nbclient 0.11.0's exception classes
    directly), so the authoritative source of "which cell, and what error"
    is the notebook object itself: nbclient writes a real ``error`` output
    onto the cell that failed before raising. A timeout has no such output
    (the cell that hung produced no error output), so for timeouts we fall
    back to "the first cell with no execution_count", i.e. the first cell
    that never finished.
    """
    for index, cell in enumerate(nb.cells):
        if cell.get("cell_type") != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                return CellFailure(
                    cell_index=index,
                    ename=output.get("ename", fallback_ename) or fallback_ename,
                    evalue=output.get("evalue", fallback_evalue) or fallback_evalue,
                    traceback=list(output.get("traceback", []) or []),
                    source=str(cell.get("source", "")),
                )

    # No error output found (typical for a timeout). nbclient assigns each
    # cell's execution_count *before* running it (so Jupyter can show a
    # "running" state), then fills in outputs afterward -- confirmed
    # empirically: a cell that times out mid-execution ends up with its
    # execution_count set but an empty outputs list, while cells never
    # reached keep execution_count=None. So the failing cell is the LAST one
    # with a non-None execution_count, not the first one with None.
    last_started_index = -1
    for index, cell in enumerate(nb.cells):
        if cell.get("cell_type") == "code" and cell.get("execution_count") is not None:
            last_started_index = index

    if last_started_index >= 0:
        cell = nb.cells[last_started_index]
        return CellFailure(
            cell_index=last_started_index,
            ename=fallback_ename or "TimeoutError",
            evalue=fallback_evalue,
            traceback=[],
            source=str(cell.get("source", "")),
        )

    return CellFailure(cell_index=-1, ename=fallback_ename, evalue=fallback_evalue)
