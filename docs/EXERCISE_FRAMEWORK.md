# 🏋️ Exercise Framework

This document specifies how exercises work across all 89 notebooks: the six-level structure
every notebook's `## 🏋️ Exercises` section follows, how difficulty is calibrated per notebook,
how solutions are presented, and the policy for dimensional reasoning, numerical sanity checks,
and avoiding repetition. It exists so exercises are a **designed, load-bearing part of the
curriculum** — not an appendix bolted onto the end of each notebook.

If you are adding a new notebook or exercise, this document (not just imitation of a nearby
notebook) is the source of truth for structure. See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for
where this fits into the overall notebook template.

---

## Why redesign this

Every notebook previously had exactly three exercises — Warm-up, Practice, Challenge. That
structure conflated two different things under "Warm-up" (recall a fact vs. compute something)
and skipped two skills entirely: no notebook ever asked a *pure conceptual* question with zero
computation, and "Practice" inconsistently meant either "derive this by hand" or "write this
code," depending on the notebook. The three-tier system also gave no consistent place for
dimensional/shape reasoning, no consistent verification mechanism, and no solutions at all —
every exercise was purely self-graded.

The six-level system below fixes all four problems: it names six *distinct* skills explicitly,
gives each one a consistent place across all 89 notebooks, builds in a verification step
(dimensional reasoning or a numerical sanity check) wherever the underlying object has a
shape/sign/normalization to check, and provides a solution or solution outline for every
exercise — full worked solutions where seeing the answer accelerates learning (COMPUTE,
UNDERSTAND, DERIVE), and a self-check condition rather than a full answer where the point is to
build something yourself (IMPLEMENT, APPLY, CHALLENGE).

---

## The six levels

Every notebook's Exercises section has **exactly six exercises, one per level, always in this
order**. The order is deliberate: each level requires the previous one's skill as a
sub-routine — you cannot meaningfully derive a formula you can't compute an instance of, and you
cannot apply a concept to a new scenario if you can't already implement it.

| # | Level | Tests | Typical shape |
|---|---|---|---|
| 1 | 🔢 **COMPUTE** | Can you correctly execute the mechanical procedure on a small, tractable example? | By-hand (or by-SymPy) computation with a specific numeric answer, verified against code. |
| 2 | 💭 **UNDERSTAND** | Do you understand what the object/theorem/algorithm *means*, and when it does and doesn't apply? | Predict-then-verify, compare two candidates, spot the error, explain a "why," identify which hypothesis of a theorem is violated. Little to no computation. |
| 3 | ✏️ **DERIVE** | Can you produce the mathematics yourself, not just recognize or apply it? | A genuine pen-and-paper derivation: prove an identity, derive a special case, complete an induction, take a symbolic derivative/integral, derive a gradient formula. |
| 4 | 🐍 **IMPLEMENT** | Can you translate mathematics into correct, independently-verified code? | Extend or modify the notebook's own code — a new function, an added feature, an alternative implementation — always checked against a library call, a symbolic result, or a provided closed form. |
| 5 | 🤖 **APPLY** | Can you transfer the concept to a genuinely different AI/ML scenario? | A new scenario not already fully worked out in the notebook's own "Why This Matters for AI" section — requires combining the concept with at least one other idea. |
| 6 | 🚀 **CHALLENGE** | Can you reason like a practitioner or researcher facing an open, only partially-specified problem? | Multi-part investigation, a failure mode or limitation to characterize, a connection to a cited paper or a later module, tolerating some ambiguity in what "done" looks like. |

**Every notebook gets all six levels — depth is calibrated, not level count.** A difficulty-1
notebook's DERIVE is a two-line algebraic manipulation; a difficulty-8 notebook's DERIVE is a
multi-step proof chaining several results together. Keeping all six levels present everywhere
means a learner always knows exactly what kind of thinking is being asked for at "exercise 3" in
*any* notebook in the curriculum — the structure itself becomes something you can rely on, not
just the content.

---

## Calibration by difficulty

Every notebook header already states a difficulty rating (`1`–`10`, shown as a block bar). Use
that rating — not module identity — to calibrate depth, since difficulty varies within a module
(e.g. `01.01` is a 2, `01.10` is a 5). The table below gives the calibration actually used:

| Difficulty | Maturity tier | COMPUTE | UNDERSTAND | DERIVE | IMPLEMENT | APPLY | CHALLENGE |
|---|---|---|---|---|---|---|---|
| 1–2 | Foundational | Simple arithmetic / a 3–4 term example | A single, sharply-posed "why," often targeting a common misconception | A short manipulation or one-trick proof (≤ 5 lines) | A small, clearly-scoped code addition | One clear, bounded AI connection | A bounded but genuinely open extension (1 sub-question) |
| 3–5 | Undergraduate | A small but real computation (3×3 matrix, multi-step Bayes update) | Compare/contrast two cases, or identify which theorem hypothesis fails | A real multi-step derivation | A real extension requiring a design choice, checked against a library | Requires combining 2 ideas from the notebook | An investigation with 2–3 sub-parts |
| 6 | Adv. undergrad / beginning grad | Concrete but with more moving parts (e.g. one full Adam step) | An edge-case or subtlety question | A full multi-step proof, often of a named result's special case | Building a nontrivial component (a class, an alternative algorithm), checked against a real library (`torch`, `scipy`) | A realistically involved ML scenario | Genuinely open-ended; may require reading between the lines of a cited paper |
| 7 | Graduate | Careful bookkeeping on an abstract object (a Fisher-metric entry, a measure-theoretic construction) | Distinguishing formally similar but different conditions (a.s. vs. in-probability, etc.) | A graduate-level derivation connecting to a cited theorem | Implementing and validating a nontrivial numerical procedure two independent ways | Connecting abstract theory to a concrete architecture or paper | A mini research investigation without one single "correct" answer |
| 8 | Research | As diff-7, with less hand-holding | As diff-7, often about a regime boundary (phase transition, asymptotic behavior) | Multi-step, may require an inductive/asymptotic argument | Implementing a research-adjacent procedure (e.g. a simplified DDIM sampler) | Direct engagement with a specific paper's claim | An experiment-plus-interpretation question with a genuinely ambiguous "right" answer |

This is guidance, not a rigid formula — the goal is that a learner who found the notebook's own
Theory/Implementation sections appropriately challenging finds the exercises appropriately
challenging too, neither trivial busywork nor a wall.

---

## Dimensional reasoning and numerical sanity checks

Wherever the mathematical object in question *has* a shape, sign, or normalization constraint,
at least one exercise (usually COMPUTE or IMPLEMENT) makes checking it an explicit, named step —
not an afterthought. Concretely:

- **Linear algebra / calculus / tensors:** "predict the shape of `X @ W` before running it,"
  "confirm the Jacobian's shape is (outputs × inputs)," "check the result is symmetric /
  positive-semi-definite as the construction guarantees."
- **Probability / statistics:** "confirm your computed distribution sums/integrates to 1,"
  "check the variance you computed is non-negative," "confirm the two independent computations
  of the same quantity agree to within floating-point tolerance."
- **Numerical methods:** "compare against the closed-form limit as a sanity check," "confirm the
  answer doesn't depend on an arbitrary choice it provably shouldn't (a sign flip, a basis
  choice)."
- **Optimization / information theory:** "confirm the loss is non-negative," "confirm KL
  divergence is exactly 0 only when the two distributions are equal."

Not every exercise has a natural dimensional or sanity check to make (a Venn-diagram set
exercise doesn't), so this is applied *where appropriate*, per the task's own framing — but
wherever the underlying object has a checkable invariant, making that check an explicit,
callable-out step is required, not optional polish.

---

## Solutions: full answers vs. solution outlines

Solutions are provided for **every exercise**, but the *depth* of what's given is different by
design, matching how much a full answer would short-circuit the intended learning:

| Level | What's given | Why |
|---|---|---|
| COMPUTE | Full worked solution | The point is executing a known procedure correctly; seeing a correct worked example is how you catch your own arithmetic mistakes. |
| UNDERSTAND | Full solution (the reasoning, 2–5 sentences) | The point is the *reasoning*, and reasoning is exactly what should be checkable/comparable. |
| DERIVE | Full solution outline (every real step, condensed) | A derivation with zero feedback is exactly where self-study breaks down; the outline lets you check each step without removing the work of filling in algebra. |
| IMPLEMENT | A **self-check condition**, not a solution | The task already includes verification against a library/closed form — that check *is* the answer key. Handing out code would remove the actual exercise. |
| APPLY | A **"what you should observe"** statement | States the qualitative/quantitative result a correct attempt produces, without writing the scenario for you. |
| CHALLENGE | A **rubric-style expectation** ("what a strong answer covers"), sometimes omitted entirely | Genuinely open-ended by design; over-specifying the "right" answer would contradict the level's purpose. |

Every solution/outline/self-check is inside a collapsed `<details><summary>...</summary>` block
directly under its exercise, so the notebook stays scannable and nothing is spoiled by accident
— you choose when to reveal it. This renders correctly as a native collapsible element in
Jupyter, JupyterLab, Google Colab, and GitHub's notebook viewer.

---

## Avoiding repetition

Two kinds of repetition are actively guarded against:

1. **Within a notebook:** the six exercises must each test a genuinely different facet. If
   COMPUTE and IMPLEMENT would be satisfied by literally the same single calculation, one of
   them is testing nothing new — rewrite one to target a different aspect of the concept.
2. **Across notebooks:** several ideas recur across the curriculum by design (attention appears
   in `01.10`, `02.10`, and `12.01`; low-rank approximation appears in `01.07` and again in
   `08.05`–`08.06`; the chain rule appears throughout Module 02 and again in `12.02`). When an
   exercise touches a recurring idea, it targets **that specific notebook's own lens** on the
   idea rather than re-asking the earlier notebook's question. For example, `01.07`'s APPLY
   exercise asks you to *recognize* the SVD-to-LoRA connection via the energy-captured curve;
   `08.06`'s exercises instead manipulate LoRA's actual rank/alpha hyperparameters, because by
   `08.06` the recognition step is assumed and the manipulation is the new content.

When editing or adding an exercise for a concept that also appears elsewhere in the curriculum,
check the other notebook's exercises first (its own `## 🏋️ Exercises` cell) and make sure the
two are testing different things.

---

## Template

```markdown
## 🏋️ Exercises

Six levels, in order: mechanical computation → conceptual understanding → derivation →
implementation → application → open-ended challenge. Solutions/outlines are in the collapsed
`Solution` blocks below each exercise — try before revealing.

### 🔢 COMPUTE
1. [Small, tractable by-hand computation, with a numeric answer to check. Include a
   dimensional/sanity check step where the object has a shape/sign/normalization to verify.]

<details>
<summary>💡 Solution</summary>

[Full worked solution, ending in the same numeric check the exercise asked for.]

</details>

### 💭 UNDERSTAND
2. [A conceptual question — predict-then-verify, compare/contrast, spot the error, or a
   sharply-posed "why" — answerable with little or no computation.]

<details>
<summary>💡 Solution</summary>

[The reasoning, 2-5 sentences.]

</details>

### ✏️ DERIVE
3. [A genuine pen-and-paper derivation or proof.]

<details>
<summary>💡 Solution outline</summary>

[Every real step, condensed but complete.]

</details>

### 🐍 IMPLEMENT
4. [Extend/modify the notebook's own code; state exactly what it should be checked against.]

<details>
<summary>✅ How to know you're right</summary>

[The specific check/assertion/comparison that should hold if the implementation is correct.]

</details>

### 🤖 APPLY
5. [A new, plausible AI/ML scenario not already fully worked out in the notebook, requiring
   genuine transfer of the concept.]

<details>
<summary>✅ What you should observe</summary>

[The qualitative or quantitative result a correct attempt produces.]

</details>

### 🚀 CHALLENGE
6. [Open-ended synthesis, investigation, or extension. May connect to a cited paper or a later
   module. Tolerates ambiguity in what "done" means.]

<details>
<summary>🔍 What a strong answer covers</summary>

[Rubric-style expectations, not a full solution — sometimes omitted for the most open items.]

</details>

---
```

This replaces the notebook's existing `## 🏋️ Exercises` markdown cell wholesale (it is always
the single markdown cell directly before `## 📚 Further Reading`), keeping the same heading and
position in the notebook. **Never edit `.ipynb` files with a plain string-replace tool** — the
raw file is JSON with escaped quotes and newlines, and naive substring matching against readable
text will silently fail to find text that visibly exists. Use a small `nbformat` script: load
the notebook with `nbformat.read(path, as_version=4)`, find the Exercises cell by scanning
`cell['source']` for the `## 🏋️ Exercises` heading, replace `cell['source']` with the new text
wholesale, `nbformat.validate(nb)`, then `nbformat.write(nb, path)`.

Because the Exercises section is always a markdown cell with no executable code, editing it
**cannot** break a notebook's execution — there is nothing to run. `nbformat.validate()` after
every edit catches structural JSON corruption; a full `notebook_audit` kernel-execution pass is
reserved for spot-checks rather than run on every single edit, since it verifies something a
markdown-only change cannot affect.

---

## Retained vs. new content

Every existing Warm-up/Practice/Challenge exercise was reviewed rather than discarded. Where an
existing exercise already fit one of the six levels well, it was kept — often verbatim, always
after label mapping (a "Practice" that was a code extension became IMPLEMENT; a "Practice" that
was a hand derivation became DERIVE; a "Challenge" that was a bounded single-technique
connection became APPLY; a "Challenge" that was already a genuine open investigation stayed
CHALLENGE). UNDERSTAND and, in some notebooks, DERIVE, are the levels most often newly written,
since the old three-tier structure had no dedicated slot for either.

See [Exercise Coverage by Module](#exercise-coverage-by-module) at the end of this document for
the per-module accounting of what was retained vs. newly written.

---

## Exercise Coverage by Module

All 89 notebooks across all 13 modules now follow the six-level structure — verified
structurally (every notebook's Exercises cell contains all six level headings and at least one
`<details>` solution block) and, per module, via a batched `notebook_audit` kernel-execution
pass confirming the redesign introduced no structural breakage. The table below summarizes each
module's scope and what the exercises specifically emphasize, to make the anti-repetition
boundaries between modules (and between notebooks within a module) visible at a glance.

| Module | Notebooks | Exercise emphasis |
|---|---|---|
| `00` Prerequisites | 4 | Notation, sets/logic/proofs, functions, and the NumPy/SymPy toolkit — COMPUTE/UNDERSTAND carry most of the weight at this difficulty tier; DERIVE exercises are short (≤5-line) manipulations. |
| `01` Linear Algebra | 10 | Vectors through SVD/PCA, decompositions, tensors, and transformer linear algebra. APPLY/CHALLENGE exercises anchor recurring curriculum threads (e.g. `01.07`'s SVD-energy-capture APPLY exercise recognizes the LoRA connection without manipulating LoRA hyperparameters directly, deferring that to `08.06`). |
| `02` Calculus | 10 | Limits through backpropagation calculus. DERIVE exercises are genuine symbolic derivations (chain rule, Jacobians, gradients); IMPLEMENT exercises are checked against `torch.autograd` or SymPy, never hand-verified alone. |
| `03` Probability and Statistics | 11 | Fundamentals through Bayesian deep learning. Sanity checks emphasize distribution-defining invariants (sums/integrates to 1, non-negative variance) as an explicit, named COMPUTE/IMPLEMENT step. |
| `04` Optimization | 9 | Landscape through loss-landscape visualization. Exercises deliberately partition natural-gradient/Fisher-information depth away from this module (kept to Newton/BFGS/quasi-Newton mechanics in `04.07`) so `10.02`–`10.03` can own that territory without duplication. |
| `05` Information Theory | 7 | Entropy through information theory in LLMs. Numerical sanity checks emphasize KL/cross-entropy non-negativity and equality-iff-identical-distributions. |
| `06` Numerical Methods | 7 | Floating point through numerical issues in transformers. Exercises chain tightly module-internally (e.g. `06.02`'s log-sum-exp CHALLENGE anticipates `06.06`'s float32/bfloat16 quantization-gap argument); `06.07` stays strictly on softmax/LayerNorm/attention-scaling numerics, leaving the underlying transformer math itself to `01.10`/`02.10`. |
| `07` Discrete Mathematics | 5 | Combinatorics through discrete math in NLP. `07.04` and `07.05` cross-reference each other's DFA/mod-3 constructions without duplicating; `07.04`'s CHALLENGE extends its own DFA into a pushdown-automaton-style unbounded-depth constrained decoder. |
| `08` Advanced Linear Algebra | 6 | Inner product spaces through LoRA. Anti-repetition is load-bearing here: `08.01` stays on Gram matrices/projection theorem (not kernel trick/RKHS, owned by `11.02`); `08.04` owns random-matrix-specific spectral laws (semicircle, Marchenko-Pastur, BBP transition) while `09.04` owns the general concentration-inequality toolkit; `08.05` stays on Eckart-Young/randomized SVD/Nyström (not LoRA rank/alpha, owned by `08.06`). |
| `09` Advanced Probability | 6 | Measure theory through diffusion process math. `09.02` (general stochastic processes) and `09.03` (Markov-chain-specific) split cleanly; `09.06`'s CHALLENGE directly measures the DDIM-vs-DDPM diversity tradeoff via retrained-model sample statistics rather than asserting it. |
| `10` Differential Geometry and Topology | 5 | Manifolds through topological data analysis. The module's clearest internal split: `10.02` owns the geometric/metric-space framing of information geometry (Fisher-Rao metric, statistical manifolds), `10.03` owns natural gradient descent as an optimization algorithm (K-FAC, TRPO) — deliberately the only notebook in the curriculum with this depth, since `04.07` stayed shallow on it by design. |
| `11` Functional Analysis | 4 | Function spaces through infinite-width networks. Kernel/RKHS-specific exercises live here (`11.02`), not in `08.01`. |
| `12` Capstone Projects | 5 | End-to-end builds (attention, backprop, Adam, GPT analysis, paper reading). CHALLENGE exercises are the most open-ended in the curriculum by design, consistent with these notebooks' own synthesis-over-many-modules character. |

**Retained vs. new, in aggregate:** every prior Warm-up/Practice/Challenge exercise was reviewed
before writing the six-level replacement; a substantial fraction of COMPUTE, IMPLEMENT, and
APPLY content is re-labeled prior material (often verbatim) rather than freshly written, per the
mapping described above. UNDERSTAND is the level written from scratch most consistently across
all 89 notebooks, since no prior tier targeted pure conceptual understanding with zero
computation. Every numeric claim appearing in a solution, self-check, or rubric — across all 89
notebooks — was verified against a live Python computation before being written down, catching
several errors in the process (e.g. a variance-direction sign error in an earlier draft, an
imprecise "empirical Fisher equals true Fisher when predictions equal labels" claim corrected to
the accurate expectation-level identity in `10.03`, and an initially-assumed clean monotonic
peak-LR-vs-warmup relationship in `04.06` that turned out to be genuinely noisy at fine
resolution and was reported as such rather than smoothed over).
