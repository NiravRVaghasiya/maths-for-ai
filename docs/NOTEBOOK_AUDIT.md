# Notebook Reproducibility Audit

This document describes `tools/notebook_audit`, a CI tool that executes every
notebook in the curriculum in a fresh kernel, classifies any failures into
actionable categories, and reports the result as JSON, Markdown, and JUnit
XML. It exists to answer one question mechanically, on every push and PR:
**does every notebook still run top-to-bottom, in a clean environment, and
produce the same output every time?**

This is a code-correctness/CI tool, not a content-quality reviewer. It
cannot tell you whether a notebook's mathematics is right or whether a
demo actually illustrates what its caption claims — that requires reading
the notebook. It *can* tell you, reliably and automatically, whether a
notebook crashes, hangs, silently relies on execution order, emits a
deprecation warning, or produces different numbers on two runs with the
same seed.

## Quick start

```powershell
# 1. Create and activate a clean environment (one-time setup)
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r tools\notebook_audit\requirements-audit.txt

# 2. Register a Jupyter kernel for the venv (every notebook's own metadata
#    declares kernel name "python3" -- match it, or pass --kernel-name)
.\.venv\Scripts\python.exe -m ipykernel install --user --name python3 --display-name "Python 3"

# 3. Run the audit
$env:PYTHONPATH = "tools"
.\.venv\Scripts\python.exe -m notebook_audit
```

On Linux/macOS, replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`
and set `PYTHONPATH=tools` instead of using `$env:PYTHONPATH`.

Reports are written to `reports/notebook_audit/` (gitignored — this is
generated output, not source) as `report.json`, `report.md`, and
`junit.xml`. The command exits `0` if every notebook passed, `1` otherwise.

### Common invocations

```powershell
# Just one module
python -m notebook_audit --module 08_Advanced_Linear_Algebra

# Just one notebook
python -m notebook_audit --notebook 08_Advanced_Linear_Algebra/02_matrix_calculus.ipynb

# Stop at the first failure instead of running everything
python -m notebook_audit --fail-fast

# Run every selected notebook TWICE and diff numeric output between runs
# (roughly doubles execution time -- an opt-in check, not part of the
# default pass/fail run)
python -m notebook_audit --check-determinism

# If you registered the kernel under a different name than "python3"
python -m notebook_audit --kernel-name maths-for-ai-audit
```

Run `python -m notebook_audit --help` for the full flag list (per-cell and
whole-notebook timeouts, seed value, report directory, etc.).

## What gets executed, and how

- **Discovery** (`discovery.py`): every `*.ipynb` file directly inside one
  of the 13 top-level `NN_ModuleName/` directories. `.audit_tmp/`,
  `_templates/`, `.venv/`, `tools/`, and any dotted directory are never
  treated as curriculum content.
- **Execution** (`executor.py`): each notebook runs in its own fresh
  Jupyter kernel (via `nbclient`, not `papermill`/`nbconvert` subprocesses),
  top to bottom, exactly once per run (twice under `--check-determinism`).
  Kernels are never reused across notebooks, so one notebook's state can
  never leak into the next.
- **Determinism**: a synthetic cell seeding `numpy`, `random`, `torch`
  (when importable), and `PYTHONHASHSEED` is prepended in memory before
  execution and stripped back out before any report references cell
  content — it never touches a notebook file on disk, and every reported
  `cell_index` refers to the notebook's own authored cells, never the
  injected one.
- **Timeouts**: a per-cell timeout (default 300s) and a separate
  whole-notebook wall-clock timeout (default 900s) both apply. A notebook
  that hangs is interrupted and reported as a `timeout` failure, not left
  to run forever.

## Failure categories

Every failure and warning is tagged with one of these categories. Categories
are assigned by inspecting the *actual* exception a real, currently
installed dependency produced (verified against this repo's own installed
versions while building the classifier — see "Lessons learned" below), not
guessed from documentation.

| Category | Severity | Meaning |
|---|---|---|
| `import_error` | fail | `ImportError` / `ModuleNotFoundError` — a dependency is missing or misspelled. |
| `undefined_variable` | fail | `NameError` where the name is never bound anywhere in the notebook — a genuine typo or missing definition. |
| `execution_order` | fail | `NameError` where the name *is* bound, but only in a cell that comes later — the notebook only works if cells run out of the authored top-to-bottom order. |
| `shape_error` | fail | Array/tensor shape or dimension mismatches (numpy broadcasting, matmul dimension mismatches, matplotlib x/y length mismatches). |
| `numerical_error` | fail | Division by zero, singular matrices, non-convergence, invalid values in floating-point ops. |
| `plotting_error` | fail | A matplotlib/seaborn call itself raises (e.g. an invalid color value) for reasons other than a data-shape mismatch. |
| `timeout` | fail | The per-cell or whole-notebook timeout was exceeded. |
| `other_runtime_error` | fail | Any other exception, or a kernel that died/failed to start. Includes `UnboundLocalError` (a real Python local-scoping bug, distinct from a notebook-level execution-order issue). |
| `deprecated_api` | warn | A `DeprecationWarning`/`FutureWarning`/`PendingDeprecationWarning` was emitted. Does not fail the notebook on its own. |
| `filesystem_assumption` | warn | Source contains a hardcoded absolute path literal or a file-write call. Static (source-scan), runs regardless of pass/fail. |
| `reproducibility` | fail (under `--check-determinism` only) | The notebook produced different numeric stdout output across two runs with the same seed. |
| `excessive_runtime` | warn | Notebook took over 120s to execute (informational; does not fail the notebook). |

### What this tool deliberately does NOT try to detect

An earlier version of the classifier attempted to flag a notebook's own
printed self-verification checks (many notebooks print things like
`"holds: True"` or `"match: True"` as an internal correctness check) when
they printed `False`, on the theory that this signals a broken invariant.
**This was removed** after it produced a real false positive:
`11_Functional_Analysis/01_function_spaces_and_norms.ipynb` legitimately
prints `holds: False` for `p=1,3,inf` in its parallelogram-law
demonstration — `False` is the mathematically correct answer there (the
parallelogram law holds *only* for `p=2`), not a regression. Distinguishing
"the notebook demonstrates X is false on purpose" from "X used to be true
and now isn't" requires understanding the notebook's pedagogical intent,
which cannot be done reliably by pattern-matching printed text. That kind
of judgment call belongs in a human content review, not an automated CI
classifier where a false positive erodes trust in the whole report.

For the same reason, this tool cannot and does not check mathematical
correctness, whether a visualization demonstrates what its caption claims,
or whether an "AI/ML connection" section is substantive. Those are exactly
the kinds of things a human (or an LLM doing a dedicated content review)
should read the notebook for.

## Reports

Every run produces three files from the same underlying data, so they can
never disagree with each other:

- **`report.json`** — machine-readable: environment info (Python/numpy/
  torch/etc. versions actually installed), a summary block, and one entry
  per notebook with its status, duration, and every finding.
- **`report.md`** — human-readable: environment table, summary, a
  pass/fail table grouped by module, a detailed "known issues" section for
  every failing notebook (category, message, cell index, and a source
  preview), and a list of passing notebooks that still emitted a warning.
- **`junit.xml`** — one `<testsuite>` per module, one `<testcase>` per
  notebook, with a `<failure>` element for anything that failed. This is
  what CI tooling that understands JUnit (including GitHub's own test
  summary UI, with the right plugin) can render as pass/fail annotations.

## CI usage

This harness is the execution engine behind both CI tiers — see
[`docs/CI.md`](CI.md) for the full architecture. In short:

- **Fast PR tier** (`.github/workflows/ci.yml`) runs the harness with
  `--representative` (one notebook per module) on every push and pull
  request to `main`, alongside code-quality checks and the harness's own
  unit tests.
- **Deep scheduled tier** (`.github/workflows/nightly.yml`) runs the harness
  per module across the full supported Python range (3.11–3.13) on a nightly
  schedule, and — on manual `workflow_dispatch` with `check_determinism=true`
  — the `--check-determinism` double-run.

Both tiers:

1. Install `requirements.txt` (the curriculum's own dependencies) and
   `tools/notebook_audit/requirements-audit.txt` (the harness's pinned
   tooling dependencies).
2. Register a `python3` Jupyter kernel (matching what every notebook's own
   metadata declares).
3. Run `python -m notebook_audit` (with `--representative` or `--module`).
4. Upload the JSON/Markdown/JUnit reports as a build artifact, always (even
   on failure — `if: always()`), and append the Markdown report to the job's
   step summary so results are visible without downloading an artifact.

### History: the workflows this consolidated

Earlier, the repo had four overlapping notebook workflows —
`test-notebooks.yml` (`pytest --nbval-lax`), `colab_test.yml` (a bare
`papermill` loop), `notebook_lint.yml` (`nbformat` + `nbqa`), and
`notebook-reproducibility-audit.yml` (this harness). The first two
re-executed every notebook with no failure classification or structured
report — exactly what this harness already does as a strict superset — so
all four were consolidated into the two-tier `ci.yml` / `nightly.yml`
structure documented in [`docs/CI.md`](CI.md). Nothing that was checked
before is no longer checked; the checks were deduplicated, not dropped.

## Local development

### Running the test suite

The harness has its own test suite (`tools/notebook_audit/tests/`), split
into fast pure-unit tests and slower integration tests that genuinely
execute small synthetic fixture notebooks against a real kernel:

```powershell
$env:PYTHONPATH = "tools"
.\.venv\Scripts\python.exe -m pytest tools/notebook_audit/tests/ -v
```

The fixtures live in `tools/notebook_audit/tests/fixtures/` — one tiny
notebook per failure category (e.g. `fail_shape_error.ipynb`,
`fail_timeout.ipynb`, `warn_deprecated_api.ipynb`). If you change the
classifier, add or extend a fixture rather than only asserting against
hand-written exception strings — several real classification bugs (see
below) were only caught by running fixtures against an actual kernel.

### A note on kernel names

Every notebook in this curriculum declares kernel name `python3` in its own
metadata. If you already have an unrelated `python3` kernel registered
globally (common on a dev machine with its own Jupyter install), registering
another one under the audit venv with the *same* name will overwrite which
Python environment `python3` points to system-wide. To avoid that on a
shared dev machine, register the audit venv's kernel under a distinct name
(e.g. `maths-for-ai-audit`, as this repo's own maintainers did while
building this tool) and pass `--kernel-name maths-for-ai-audit` explicitly.
In CI, the container starts fresh every time, so registering as `python3`
there is safe and simplest.

## Lessons learned while building this

A few things below were **not obvious from reading `nbclient`'s
documentation** and were only discovered by executing real notebooks
against a real kernel and inspecting the actual result — kept here so a
future contributor doesn't have to rediscover them:

- `CellExecutionError` and `CellTimeoutError` (nbclient's own exception
  classes) carry no cell index at all. The only reliable way to find which
  cell failed is to scan the notebook's own cell outputs for the `error`
  output nbclient wrote onto the failing cell before raising.
- On a timeout, nbclient sets a cell's `execution_count` *before* running
  it (so a UI can show a "running" indicator), then fills in outputs
  afterward. A cell that times out mid-execution therefore ends up with its
  `execution_count` set but empty outputs — the failing cell is the *last*
  cell with a non-`None` execution count, not the first one with `None` (an
  initially-plausible-sounding assumption that turned out to be exactly
  backwards, caught by a fixture test).
- Distinguishing "this variable is genuinely never defined" from "this
  variable is defined, just in a cell below the one that failed" cannot be
  done from the exception alone — both raise an identical `NameError` with
  an identical message shape. Only a static scan of the rest of the
  notebook's source (via `ast`) for where the name is actually bound can
  tell the two apart.
- matplotlib's own exception messages frequently don't mention
  "matplotlib" anywhere in the exception text itself (e.g. an invalid color
  value) — the only reliable signal that an error originated in plotting
  code is the file paths inside the traceback.
- Injecting a synthetic seed cell shifts every subsequent cell's index by
  one relative to the notebook's own authored cells. If the failure-locating
  logic computes an index against the notebook *with* the seed cell still
  present, but callers/reports index into the seed-*stripped* copy (which
  is what a report should show), every reported cell index silently ends
  up off by one. This exact bug existed in an early version of this tool
  and was only caught because the test suite asserted against
  `executed_nb` (the stripped copy that reports actually use), not against
  internal state.

The general pattern: nothing about a Jupyter kernel's real failure/timeout
behavior should be assumed from how you'd expect it to work — verify
against an actual execution first, then encode the verified behavior as a
regression-tested fixture.
