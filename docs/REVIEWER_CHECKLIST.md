# 🔎 Reviewer Checklist

How to review a pull request against this repository. It exists so review is
**consistent** — every PR is held to the same bar regardless of who reviews it —
and so reviewers know exactly what to check for each kind of change without
re-reading every framework doc each time.

The four standing review criteria (from [`CONTRIBUTING.md`](../CONTRIBUTING.md))
are: **theory accuracy, runnable code, a genuine AI/ML connection, and complete
exercises.** This document turns them into a per-PR-type procedure. The detailed
per-item bar lives in the [notebook quality
checklist](NOTEBOOK_QUALITY_CHECKLIST.md); this is the *how you review*, that is
the *what "good" means*.

## First: what kind of PR is this?

Route by the author's "Type of change" (verify they picked the right one):

| PR type | Go to |
|---|---|
| Mathematical content / new notebook / exercise | [Reviewing mathematical content](#reviewing-mathematical-content) |
| Notebook bug fix | [Reviewing a notebook bug fix](#reviewing-a-notebook-bug-fix) |
| Tooling / CI / infrastructure | [Reviewing tooling / infrastructure](#reviewing-tooling--infrastructure) |
| Docs / typo / translation | [Reviewing docs & translations](#reviewing-docs--translations) |

A single PR can be more than one type; apply each relevant section.

---

## Reviewing mathematical content

This is the highest-stakes review. **Correctness is non-negotiable** — an elegant
notebook with a wrong derivation is worse than no notebook.

1. **Run the eight mathematical checks.** Go through
   [Part A of the quality checklist](NOTEBOOK_QUALITY_CHECKLIST.md#part-a--the-eight-mathematical-checks)
   in this order — notation, assumptions, derivations, dimensions,
   `numerical implementation`, references, AI connection, exercises. Each has a
   "how to check." Do not rubber-stamp — actually work through at least one full
   derivation and one numeric verification yourself.
2. **Independently verify one non-trivial numeric claim.** Re-derive or
   re-compute it (a quick SymPy/NumPy snippet, or the math-regression suite).
   Confirm the implementation is checked against something *external*, not
   against itself.
3. **Check the structural/executable items** in
   [Part B](NOTEBOOK_QUALITY_CHECKLIST.md#part-b--structural-executable-and-style-checks):
   fresh-kernel run, only-`requirements.txt` deps, structural validation, plots
   labeled.
4. **If it's a new/renamed notebook**, confirm `LEARNING_PATH.md` is updated:
   dependency edges point backward only, track tables include it if it belongs to
   a track, and it's classified per [`RIGOR_FRAMEWORK.md`](RIGOR_FRAMEWORK.md).
5. **Confirm CI is green** (fast tier) — but note CI checks *execution and style*,
   not *mathematical correctness*; that judgment is yours.

**Decision:** request changes if any of the eight checks fails; a math error is a
blocking issue, not a nit.

## Reviewing a notebook bug fix

1. **Reproduce the original bug** (or trust a clear traceback in the linked
   issue), then confirm the fix actually resolves it.
2. **Fresh-kernel top-to-bottom run** of the whole notebook — a fix that breaks a
   later cell isn't a fix. Use
   `python -m notebook_audit --notebook <path> --kernel-name python3`.
3. **Check the fix doesn't change the mathematics.** A bug fix should make the
   code match the intended math; if it changes the *result*, re-review it as
   mathematical content (the eight checks).
4. **Guard against regressions:** if the bug was a numerical-stability or
   determinism issue, confirm a seed/stable-formulation was added, not just a
   one-off patch.

**Decision:** approve when the notebook runs clean end-to-end and the math is
unchanged (or correctly corrected).

## Reviewing tooling / infrastructure

For CI, the audit harness, the math-regression suite, packaging, or scripts —
notebook content is untouched.

1. **CI passes**, and any new check is actually exercised (not accidentally a
   no-op / `|| true` that can never fail).
2. **Tests updated/added** for changed tooling; the harness's own suite
   (`tools/notebook_audit/tests/`) and the math-regression suite still pass.
3. **No hidden dependency drift** — new deps are pinned/bounded and justified (see
   [`docs/CI.md`](CI.md)); lock file regenerated if the environment changed.
4. **Reproducibility preserved** — changes don't make notebook execution
   non-deterministic or environment-specific.

**Decision:** approve when checks are green, meaningfully test the change, and the
environment story stays coherent.

## Reviewing docs & translations

1. **Links resolve** (relative paths, anchors) and cross-references are accurate.
2. **Consistency** with the frameworks it touches (rigor, exercise, quality
   checklist) — a doc that contradicts a framework should be reconciled, not
   merged.
3. **Translations:** prose/exercises translated, **code/variables/LaTeX left
   untouched**, a full module at a time (see CONTRIBUTING → Translation
   Guidelines). You don't need to be fluent to check structure and that code is
   unchanged.

---

## Review decision rubric

| Verdict | When |
|---|---|
| ✅ **Approve** | All applicable checks pass; math is correct and verified; CI green. Minor style nits can be follow-ups. |
| 💬 **Approve with comments** | Correct and mergeable, but with non-blocking suggestions (clearer wording, an extra sanity check) the author may take or leave. |
| 🔁 **Request changes** | Any mathematical error; a notebook that doesn't run clean; a missing required section or exercise level; an unverified numeric claim; a broken cross-reference. |
| ❓ **Needs discussion** | Scope/placement questions (does this belong here? which module? forward-pointing prerequisite?) — route back to a Curriculum-proposal discussion rather than iterating in the PR. |

## Reviewer conduct

- Review as an expert *and* a mentor: explain *why* something needs to change,
  cite the framework doc, and prefer a concrete suggestion over a vague objection.
- Separate blocking issues (correctness, won't-run, missing required section) from
  preferences. Label nits as nits.
- Be especially welcoming to first-time and cross-discipline contributors — a
  mathematician may not know the audit harness, and a software engineer may not
  know the rigor scheme. Point them to the right doc rather than assuming.
