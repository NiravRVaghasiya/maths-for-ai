---
name: 🧮 Mathematical error
about: Report an incorrect definition, derivation, proof, formula, or numerical claim
title: "[Math] <notebook code> — <short description>"
labels: ["mathematical-error", "needs-triage"]
assignees: ""
---

<!--
Thank you for catching this — mathematical correctness is the repository's first
review criterion. The more of the fields below you can fill in, the faster this
can be verified and fixed. You do NOT need to complete every field; "which
notebook" + "what's wrong" + "why" is already a useful report.
-->

## Where

- **Notebook:** <!-- e.g. 02_Calculus/06_jacobians_and_hessians.ipynb (code 02.06) -->
- **Section:** <!-- Theory / Visual Intuition / Implementation / Why This Matters for AI / Exercises -->
- **Cell or equation:** <!-- quote the exact line, equation, or a screenshot -->

## What is stated (the claim you believe is wrong)

<!-- Quote the current text/equation verbatim. -->

## Why it is incorrect

Please identify which kind of error this is (check any that apply) and explain:

- [ ] **Notation** — a symbol is undefined, reused with two meanings, or inconsistent with the rest of the curriculum
- [ ] **Assumption** — a hypothesis is missing, unstated, or the result is applied outside its valid regime
- [ ] **Derivation / proof** — a step does not follow, a case is missing, or the logic is invalid
- [ ] **Dimensions / shapes** — a shape, index range, units, or broadcasting is wrong
- [ ] **Numerical implementation** — the code does not compute what the math says (wrong sign, off-by-one, unstable formula)
- [ ] **Reference** — a cited source is wrong, misquoted, or contradicts the claim
- [ ] **Other** — describe below

**Explanation:**

<!-- The specific step that fails and why. If it's a derivation, point to the exact line. -->

## The correct version (if you have it)

<!-- The corrected statement/derivation/formula. If you're not sure of the fix, that's fine —
just describe what's wrong and leave this blank. -->

## Supporting reference

<!-- An authoritative source (textbook + page, paper + equation number, or a standard identity)
that supports the correction. This is what lets a reviewer verify without re-deriving from
scratch. -->

## Verification (optional but very helpful)

<!-- A short numerical check, SymPy snippet, or counterexample demonstrating the discrepancy.
The repository's own math-regression suite (docs/MATH_REGRESSION.md) is the model: an
independent computation that disagrees with the stated claim is the strongest possible evidence. -->

```python
# optional: minimal snippet demonstrating the error
```
