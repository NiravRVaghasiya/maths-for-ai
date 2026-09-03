# 🎓 Rigor Classification

This document defines the curriculum's **rigor classification**: a six-level scale — INTUITION,
COMPUTATIONAL, UNDERGRADUATE, PROOF-BASED, GRADUATE, RESEARCH — assigned to every one of the 89
notebooks, together with three explicit per-notebook flags (whether proofs are required, whether
implementation is required, and what AI/ML background is expected). It exists so a learner can
tell, before opening a notebook, what *kind* of mathematical engagement it demands — not just how
hard it is in the abstract.

This is a distinct axis from the two classifications [`LEARNING_PATH.md`](../LEARNING_PATH.md)
already uses:

- **Classification** (🟢 CORE / 🟡 IMPORTANT / 🔵 SPECIALIZED / 🔴 ADVANCED) answers *"how
  essential is this to AI/ML practice in general?"* — it's about the notebook's role in the
  curriculum, not its difficulty.
- **Rigor** (this document) answers *"what kind and level of mathematical engagement does this
  notebook actually demand?"* — it's about the learner's experience inside the notebook.

A notebook can be any combination: `08.06` (LoRA) is IMPORTANT-classified but only
UNDERGRADUATE-rigor; `09.01` (Measure Theory) is SPECIALIZED-classified but GRADUATE-rigor. The
two axes are intentionally independent.

**This rigor classification replaces the old free-text `Maturity` column** in
`LEARNING_PATH.md`'s per-notebook tables (values were: Foundational, Undergraduate, Adv.
Undergrad, Graduate, Research). See [Correspondence to the old Maturity column](#correspondence-to-the-old-maturity-column)
below for the exact mapping. It does not touch
[`docs/EXERCISE_FRAMEWORK.md`](EXERCISE_FRAMEWORK.md)'s own "Maturity tier" column, which
calibrates *exercise depth* against the numeric Difficulty rating and remains a separate,
working system — the two are related (a RESEARCH-rigor notebook will tend to have
research-tier exercises) but are not merged, since exercise calibration and rigor
classification answer different questions.

---

## The six levels

| # | Level | What it means | Typical numeric Difficulty |
|---|---|---|---|
| 1 | 🌱 **INTUITION** | Pure conceptual or geometric understanding. No symbol-heavy derivation, no formal proof, no algorithm to trace. The point is building a correct mental picture. | 1 |
| 2 | 🔢 **COMPUTATIONAL** | Mechanical procedures executed correctly on concrete examples — by hand or by code. Pattern recognition and correct execution matter more than formal argument. | 1–3 |
| 3 | 🎓 **UNDERGRADUATE** | Standard undergraduate mathematical treatment: definitions, worked multi-step derivations, real but short arguments. Proofs, if present, are procedural rather than the main event. | 3–5 |
| 4 | 📐 **PROOF-BASED** | A genuine mathematical proof — not just a derivation — is the load-bearing content: induction, epsilon-delta arguments, optimality/convergence guarantees, a named theorem's proof. | 4–6 |
| 5 | 🏛️ **GRADUATE** | Graduate-level abstraction: measure theory, functional analysis, general/abstract objects (arbitrary Banach spaces, general kernels, tensor decompositions). Proofs are present, but the bigger leap is generality and abstraction, not proof mechanics alone. | 6–7 |
| 6 | 🔬 **RESEARCH** | Frontier material tied to specific, current research (a named paper, a technique still active in the literature). Exercises tolerate real open-endedness; "done" isn't always sharply defined. | 7–8 |

The "Typical numeric Difficulty" column is guidance, not a formula — rigor is about *what kind*
of thinking is demanded, difficulty is about *how hard* that thinking is, and they correlate
strongly but not perfectly (a PROOF-BASED notebook at difficulty 4 and one at difficulty 6 both
have "prove this" as their central demand; only the second is also harder in absolute terms).

---

## The three per-notebook flags

Every notebook additionally gets three short, explicit flags, since two notebooks at the same
rigor level can still differ sharply on these:

### Proofs Required

| Value | Meaning |
|---|---|
| **None** | No formal proof appears or is asked for. Derivations, if any, are algebraic manipulation, not proof by induction/contradiction/epsilon-delta/etc. |
| **Light** | A short, procedural proof or derivation appears (≤5–10 lines), usually in the DERIVE exercise. Understanding it doesn't require prior proof-writing experience. |
| **Central** | A genuine, non-trivial proof is the notebook's main content or its DERIVE exercise's core task — the kind of argument a real analysis/algebra/statistics course would grade as a proof, not a computation. |

### Implementation Required

| Value | Meaning |
|---|---|
| **Illustrative** | The notebook's code demonstrates or visualizes a concept already fully conveyed by the Theory section; you could understand the notebook's point without running the code yourself. |
| **Essential** | You cannot fully get the notebook's point without engaging with the code — implementing, modifying, or extending it (per the mandatory IMPLEMENT/APPLY exercise levels, see [`EXERCISE_FRAMEWORK.md`](EXERCISE_FRAMEWORK.md)) is where the understanding actually lands. |

In practice, **Essential is the default for nearly every notebook** in this curriculum — every
notebook has a working from-scratch implementation and mandatory code-based exercise levels.
**Illustrative** is reserved for the small number of notebooks whose central content is genuinely
conceptual (e.g. set theory, notation) and where the code cells exist to demonstrate rather than
to carry the main idea.

### Expected AI Knowledge

What AI/ML background (not math background — that's the existing `Prerequisites` field) a
learner should already have *before* starting the notebook, distinct from what the notebook's
own "Why This Matters for AI" section teaches:

| Value | Meaning |
|---|---|
| **None** | No AI/ML background assumed. The notebook is pure mathematics; any AI connection is introduced from scratch in its own "Why This Matters for AI" section. |
| **Basic ML** | Assumes familiarity with the basic vocabulary of training a model — loss functions, gradient descent, train/test splits — without needing to already know *this specific* notebook's technique. |
| **Deep Learning** | Assumes familiarity with neural network training specifically — backpropagation, layers, activation functions, and (once relevant) attention/transformers — since the notebook's connections build on that vocabulary rather than introducing it. |
| **Research-level** | Assumes familiarity with a *specific*, named, currently-active technique or paper (LoRA, diffusion models, RLHF, the NTK) as background, because the notebook engages with that technique's mathematics directly rather than introducing it from zero. |

---

## Calibration guidance (defaults by module position, with overrides)

Like the existing Classification legend, rigor is assigned **per notebook based on actual
content**, not mechanically from difficulty or module alone — but the following patterns hold
broadly and are the default starting point before checking for content-specific overrides:

- Module `00` and early notebooks in modules `01`–`03`, `07`: INTUITION or COMPUTATIONAL, Proofs
  None, Implementation Illustrative-to-Essential, AI Knowledge None.
- Most of modules `01`–`06`, `12`: UNDERGRADUATE, Proofs Light, Implementation Essential, AI
  Knowledge None-to-Basic ML, rising to Deep Learning by the time a module reaches transformer-
  or training-loop-specific content.
- Notebooks whose theory section's central content is a named theorem's proof or a convergence/
  optimality guarantee (regardless of module): PROOF-BASED, Proofs Central, even if the module's
  other notebooks are UNDERGRADUATE.
- Modules `08`–`09` (advanced linear algebra, advanced probability): mostly PROOF-BASED or
  GRADUATE depending on how abstract the specific notebook's objects are (a concrete Eckart-Young
  proof vs. genuine measure theory).
- Modules `10`–`11`: mostly GRADUATE, rising to RESEARCH for notebooks tied to a specific
  contemporary technique or paper (natural gradient/K-FAC, NTK, infinite-width networks,
  diffusion-adjacent topology).

## Correspondence to the old Maturity column

| Old `Maturity` value | Typical new Rigor level(s) |
|---|---|
| Foundational | INTUITION or COMPUTATIONAL (split by whether the notebook is concept-only vs. compute-heavy — this distinction didn't exist in the old scheme) |
| Undergraduate | UNDERGRADUATE, or PROOF-BASED if the notebook's core content is a proof despite otherwise-undergraduate difficulty |
| Adv. Undergrad | PROOF-BASED or GRADUATE, judged by abstraction level, not just difficulty number |
| Graduate | GRADUATE, or RESEARCH if tied to a specific contemporary technique/paper |
| Research | RESEARCH |

The old five-tier scheme conflated "how hard" with "what kind of thinking" — this six-level
scheme separates them by adding PROOF-BASED as its own tier (a proof-centric notebook can appear
at moderate difficulty) and splitting Foundational into INTUITION vs. COMPUTATIONAL (a
notation-reading notebook and a matrix-arithmetic notebook are both "easy" but demand genuinely
different things).

---

## Where this lives

Like `Classification`, `Maturity`, and `AI Relevance`, the rigor classification lives in
[`LEARNING_PATH.md`](../LEARNING_PATH.md)'s per-notebook tables — **not** in the notebook files
themselves (the notebook header table's four fields — Difficulty, Prerequisites, Time, Colab
GPU — are unchanged; see [`CONTRIBUTING.md`](../CONTRIBUTING.md)). This keeps notebook files
untouched by classification-scheme changes and keeps all classification bookkeeping in one
place.

## Rigor Classification by Module

See [`LEARNING_PATH.md`](../LEARNING_PATH.md#-notebook-level-graph-by-module) for the full
per-notebook table (columns: Code, Notebook, Prerequisites, Optional, Dependents, **Rigor**,
**Proofs**, **Implementation**, AI Relevance, **Expected AI Knowledge**) — every one of the 89
notebooks is classified there.
