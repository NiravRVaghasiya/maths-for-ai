---
name: 🐛 Notebook bug
about: A cell errors out, hangs, produces wrong output, or won't run top-to-bottom
title: "[Bug] <notebook code> — <short description>"
labels: ["bug", "needs-triage"]
assignees: ""
---

<!--
This is for CODE that doesn't run correctly. If the code runs fine but the
MATHEMATICS is wrong, use the "Mathematical error" template instead.
-->

## Where

- **Notebook:** <!-- e.g. 01_Linear_Algebra/07_SVD_and_PCA.ipynb (code 01.07) -->
- **Failing cell:** <!-- quote the first few lines of the cell, or its position in the notebook -->

## What happens

- [ ] Cell raises an exception
- [ ] Notebook won't run top-to-bottom (works only if cells are run out of order)
- [ ] Cell hangs / never finishes
- [ ] Produces wrong or nonsensical output (no exception)
- [ ] Plot is broken or missing
- [ ] Deprecation / future warning

## Expected vs. actual

**Expected:** <!-- what the cell should produce -->

**Actual:** <!-- what it actually produces -->

## Full traceback / output

<!-- Paste the COMPLETE error output, not just the last line. -->

```text

```

## Environment

<!-- The reproducibility work pins Python 3.11-3.13 with bounded dependency ranges; a
version mismatch is a common cause. See docs/CI.md and requirements.txt. -->

- **How you ran it:** <!-- local venv / conda / Google Colab / other -->
- **Python version:** <!-- python --version -->
- **Key package versions:** <!-- output of: pip show numpy scipy torch matplotlib | findstr "Name Version"
                                 (or `pip freeze | grep -Ei 'numpy|scipy|torch|matplotlib|sympy'`) -->
- **OS:** <!-- Windows / macOS / Linux -->

## Reproducibility

- [ ] Reproduces on a **fresh kernel** (Restart & Run All)
- [ ] Reproduces on a clean install of `requirements.txt`
- [ ] Reproduces in Google Colab
- [ ] Happens only sometimes (please describe when)

<!-- If you can, run the notebook through the audit harness and paste the classified failure:
     PYTHONPATH=tools python -m notebook_audit --notebook <path> --kernel-name python3
     See docs/NOTEBOOK_AUDIT.md. The failure category (import_error, shape_error,
     numerical_error, timeout, ...) is very helpful for triage. -->

## Suggested fix (optional)

<!-- If you already know the fix, describe it — or just open a PR and link it here. -->
