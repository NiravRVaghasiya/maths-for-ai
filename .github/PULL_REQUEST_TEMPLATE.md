<!--
Thanks for contributing! Fill in the summary and tick the checklist items that
apply. Not every section applies to every PR — a typo fix doesn't need the full
mathematical checklist. Delete sections that clearly don't apply, but keep the
ones that do honest.
-->

## Summary

<!-- What does this PR change, and why? One short paragraph. -->

## Related issue

<!-- e.g. "Fixes #123" or "Addresses #123". Link the mathematical-error / bug /
proposal issue this resolves, if any. -->

## Type of change

- [ ] 🧮 Mathematical content (theory, derivation, or a from-scratch implementation)
- [ ] 🏋️ Exercise (adding/improving one of the six exercise levels)
- [ ] 🐛 Notebook bug fix (code that didn't run correctly)
- [ ] 📚 New notebook / new module
- [ ] 🌐 Translation
- [ ] 🔧 Tooling / CI / infrastructure
- [ ] 📝 Docs / typo / formatting only

## Verification

<!-- How did you check this works? Paste the commands you ran and their result. -->

- [ ] Ran the affected notebook(s) **top-to-bottom in a fresh kernel** with no errors
- [ ] `python tools/ci/validate_notebooks.py` passes
- [ ] Ran `python -m notebook_audit --notebook <path>` where applicable
- [ ] For math changes: verified numeric results against an **independent** check
      (finite differences / trusted library / closed form — not a copy of the code under test)

<details>
<summary>Commands run / output</summary>

```text

```

</details>

---

## Mathematical-contribution checklist

<!-- REQUIRED if you ticked "Mathematical content", "Exercise", or "New notebook".
These are the eight checks defined in docs/NOTEBOOK_QUALITY_CHECKLIST.md — tick each
once you've confirmed it, or strike through with a one-line reason if N/A. -->

- [ ] **1. Notation** — every symbol defined at first use; consistent; LaTeX renders
- [ ] **2. Assumptions** — every hypothesis stated; result not applied out of its regime
- [ ] **3. Derivations** — each step follows; proofs complete; non-elementary results cited
- [ ] **4. Dimensions** — shapes consistent in math and code; invariants stated and checked
- [ ] **5. Numerical implementation** — code matches the math; verified against an independent oracle
- [ ] **6. References** — non-elementary claims cite an accurate, authoritative source
- [ ] **7. AI connection** — specific, working-code link to a real ML/LLM technique
- [ ] **8. Exercises** — all six levels present, calibrated, with the required solution depth; numeric answers verified

Full definitions and how-to-check for each: [`docs/NOTEBOOK_QUALITY_CHECKLIST.md`](../docs/NOTEBOOK_QUALITY_CHECKLIST.md).

## Structural checklist (any notebook change)

- [ ] Follows the six-section notebook template ([`CONTRIBUTING.md`](../CONTRIBUTING.md))
- [ ] Header table correct (Difficulty, Prerequisites backward-only, Time, Colab GPU)
- [ ] `LEARNING_PATH.md` updated if a notebook was added/renamed/re-scoped (rows, tracks, rigor)
- [ ] Uses only dependencies already in `requirements.txt`
- [ ] Plots have titles/axis labels/legends; no stray large outputs or absolute local paths

---

## Anything reviewers should know

<!-- Design choices, tradeoffs, things you're unsure about, or where you'd especially like
review. Honesty here (including "I'm not certain this derivation is tight") speeds up review. -->

<!--
Reviewers: see docs/REVIEWER_CHECKLIST.md for what to verify per PR type and how
to run the checks. Mathematical correctness is the first review criterion.
-->
