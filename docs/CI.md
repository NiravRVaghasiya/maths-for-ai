# Continuous Integration Architecture

This repository's CI is built in **two tiers**: a fast tier that runs on every
push and pull request, and a deep tier that runs on a nightly schedule (and on
demand). The split exists so contributors get a quick, reliable signal on every
change without paying — on every push — for the full cost of executing all ~100
notebooks across every supported Python version.

```
                    ┌───────────────────────────────────────────┐
   push / PR  ───▶  │  ci.yml  (FAST TIER, ~single-digit minutes) │
                    │  • code-quality      (lint + format + nbfmt)│
                    │  • unit-tests        (harness test suite)   │
                    │  • math-regression   (identity triangulation)│
                    │  • representative    (1 notebook / module)  │
                    └───────────────────────────────────────────┘

                    ┌───────────────────────────────────────────┐
   nightly    ───▶  │  nightly.yml  (DEEP TIER)                   │
   (cron) +         │  • full-audit   (ALL notebooks × py3.11-13) │
   manual           │  • determinism  (opt-in double-run diff)    │
                    └───────────────────────────────────────────┘
```

Both tiers execute notebooks through the same engine —
[`tools/notebook_audit`](../tools/notebook_audit) — so a failure means the same
thing in both places. See [`docs/NOTEBOOK_AUDIT.md`](NOTEBOOK_AUDIT.md) for how
that engine classifies failures.

## Tier 1 — Fast PR checks (`.github/workflows/ci.yml`)

Triggered on every `push` and `pull_request` to `main`. Single OS
(`ubuntu-latest`), single Python (**3.12**, the recommended version), with
`concurrency: cancel-in-progress` so a newer commit cancels an in-flight run for
the same branch/PR. Four independent jobs run in parallel:

| Job | What it checks | Blocking? |
|---|---|---|
| **code-quality** | `ruff check tools/` and `black --check tools/` (Python tooling sources); `nbformat` structural validation of every notebook; `nbqa ruff`/`nbqa black` on notebooks. | Python-source lint/format and notebook structural validation are **blocking**. Notebook *style* (`nbqa`) is **advisory** (`continue-on-error`) — see rationale below. |
| **unit-tests** | The audit harness's own test suite (`tools/notebook_audit/tests/`), including tests that execute tiny synthetic fixture notebooks against a real kernel. JUnit report uploaded. | Blocking. |
| **math-regression** | The mathematical regression suite (`tools/math_regression/tests/`): verifies the curriculum's mathematical *identities* — matrix/decomposition/eigen/SVD relationships, gradients/Jacobians/Hessians, probability & distribution identities, optimization gradients, numerical approximations — by triangulating analytical vs numerical vs trusted-library results with justified tolerances. Pure math, no notebook execution, runs in seconds. See [`docs/MATH_REGRESSION.md`](MATH_REGRESSION.md). JUnit report uploaded. | Blocking. |
| **representative-notebooks** | Executes **one notebook per module** (the first, via `notebook_audit --representative`) in a fresh kernel. Broad, cheap breakage detection: catches a missing dependency or a module-wide API break. Markdown report appended to the job summary; full report uploaded as an artifact. | Blocking. |

### Why notebook style is advisory but Python-source style is blocking

`tools/` is ordinary Python we own and can keep pristine, so its lint/format is
enforced. The 100+ curriculum notebooks are *authored teaching material* where
auto-formatting can fight intentional layout (aligned matrices, deliberate
step-by-step spacing). Enforcing `black` on them would either produce a huge
noisy reformat or block unrelated PRs over cosmetic notebook diffs. So notebook
style is surfaced (a contributor can see and fix drift) but never fails the
build. Notebook **structure** (valid JSON / nbformat) *is* blocking, because a
structurally broken notebook can't be executed or opened at all.

## Tier 2 — Deep scheduled validation (`.github/workflows/nightly.yml`)

Triggered by `schedule` (daily at 03:17 UTC) and `workflow_dispatch` (manual).
Two jobs:

| Job | What it checks | When |
|---|---|---|
| **full-audit** | Every notebook, one job per **(module × Python version)** cell, across the full supported range **3.11 / 3.12 / 3.13**. `fail-fast: false` so one module's failure doesn't mask others. Per-cell report uploaded; Markdown appended to the run summary. | Every scheduled run and every manual dispatch. |
| **determinism** | Runs every notebook **twice** and diffs numeric stdout between the runs (`--check-determinism`) to catch unseeded randomness. Single Python (3.12). | **Opt-in only** — manual dispatch with `check_determinism=true`. Roughly doubles runtime. |

Manual dispatch accepts two inputs: `check_determinism` (bool) and
`python_versions` (a JSON list, default `["3.11","3.12","3.13"]`) so you can, for
example, re-run just one Python version after a targeted fix.

## Dependency caching

Both workflows use `actions/setup-python`'s built-in `cache: pip`, keyed on the
relevant requirements files via `cache-dependency-path`:

- **code-quality** keys on `requirements-dev.txt` (it only needs the toolchain).
- **unit-tests / representative / nightly** key on `requirements.txt` +
  `tools/notebook_audit/requirements-audit.txt` (and dev reqs where used).

Keying on the requirements files means the cache is reused across runs until a
dependency actually changes, and is invalidated automatically when one does — no
manual cache-busting. The cache stores the pip download/wheel cache, so installs
skip re-downloading unchanged wheels.

## How failures are reported

Every notebook-executing job produces the audit harness's three report formats
(`report.json`, `report.md`, `junit.xml` — see
[`docs/NOTEBOOK_AUDIT.md`](NOTEBOOK_AUDIT.md#reports)). In CI:

- The **Markdown** report is appended to the job's **step summary**, so you can
  see exactly which notebook failed and why (with a failure category and a
  source preview) directly on the run page — no artifact download needed.
- The full report directory (all three formats) is uploaded as a **build
  artifact** with `if: always()`, so it's available even when the job fails.
- The **unit-tests** job uploads a JUnit XML so test failures render in GitHub's
  test UI.

A job's pass/fail is driven by the harness's exit code (`0` = all selected
notebooks passed, `1` = at least one failed), so a red check always corresponds
to a real, categorized failure in the report.

## Reproducing CI locally

The dependencies:

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r tools/notebook_audit/requirements-audit.txt
python -m ipykernel install --user --name python3 --display-name "Python 3"
```

Then, mirroring each fast-tier job:

```bash
# code-quality (blocking parts)
ruff check tools/
black --check tools/
python tools/ci/validate_notebooks.py

# unit-tests
PYTHONPATH=tools NOTEBOOK_AUDIT_TEST_KERNEL=python3 \
  pytest tools/notebook_audit/tests/ -v --timeout=300

# math-regression (pure math, no kernel needed)
PYTHONPATH=tools pytest tools/math_regression/tests/ -v

# representative-notebooks
PYTHONPATH=tools python -m notebook_audit --representative --kernel-name python3
```

To reproduce a nightly full-audit run for a single module:

```bash
PYTHONPATH=tools python -m notebook_audit --module 01_Linear_Algebra --kernel-name python3
```

On Windows PowerShell, set env vars with `$env:PYTHONPATH = "tools"` (etc.) on
their own line, and use `.venv\Scripts\python.exe` — see
[`docs/NOTEBOOK_AUDIT.md`](NOTEBOOK_AUDIT.md#quick-start).

## Adding a new module or notebook

No workflow edit is needed for a new **notebook** — discovery is dynamic
(`tools/notebook_audit/discovery.py` globs each module directory), so the fast
tier picks it up automatically (if it's the first in its module, it also becomes
that module's representative) and the nightly full-audit runs it.

A new **module** directory (`NN_Name/`) is discovered automatically by the fast
tier and the harness. The only manual step is adding the new module to the
**matrix lists** in `nightly.yml` (the `full-audit` and `determinism` jobs
enumerate modules explicitly so each gets its own parallel job). The
`test_discovery.py` tests assert module/notebook counts *structurally* (sum over
modules, directories-on-disk), so they do not need editing when the curriculum
grows.
