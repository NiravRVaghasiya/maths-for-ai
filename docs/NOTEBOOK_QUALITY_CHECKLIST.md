# ✅ Notebook Quality Checklist

This is the **single source of truth** for what "done" means for a notebook in
this curriculum. The pull-request template and the
[reviewer checklist](REVIEWER_CHECKLIST.md) both point here, so authors and
reviewers are held to exactly the same bar.

It has two parts:

- **[Part A — The eight mathematical checks](#part-a--the-eight-mathematical-checks)** —
  required for any contribution that adds or changes mathematical content
  (theory, a derivation, an implementation, or an exercise). These are the heart
  of the review.
- **[Part B — Structural, executable, and style checks](#part-b--structural-executable-and-style-checks)** —
  required for any notebook change, mathematical or not.

A change that only touches tooling/CI/docs (no notebook content) is exempt from
both parts; see the [reviewer checklist](REVIEWER_CHECKLIST.md) for those PR
types.

---

## Part A — The eight mathematical checks

Every mathematical contribution must satisfy all eight. Each has a one-line
*claim* (what must be true) and a *how-to-check* (how a reviewer confirms it).

### 1. Notation

- [ ] **Every symbol is defined before or at its first use**, and no symbol is
      silently reused with two different meanings within the notebook.
- [ ] Notation is **consistent with the rest of the curriculum** (e.g. column
      vectors, $W$ for weight matrices, $\odot$ for elementwise product) unless a
      deviation is called out and justified.
- [ ] LaTeX renders correctly (`$...$` inline, `$$...$$` block) in Jupyter/Colab.

*How to check:* read the Theory section as if you knew nothing; if you hit a
symbol you can't resolve, it fails.

### 2. Assumptions

- [ ] **Every hypothesis a result depends on is stated** (independence, full
      rank, positive-definiteness, differentiability, i.i.d., a distributional
      assumption, a domain restriction).
- [ ] The notebook does not apply a result **outside the regime where it holds**
      without saying so.

*How to check:* for each headline result, ask "under what conditions is this
true?" and confirm those conditions appear in the text.

### 3. Derivations

- [ ] **Each derivation step follows from the previous one**, with no unexplained
      leaps; a reader with the stated prerequisites can reproduce it.
- [ ] Proofs (where the notebook is PROOF-BASED per
      [`RIGOR_FRAMEWORK.md`](RIGOR_FRAMEWORK.md)) are complete: no missing case,
      no circular step, quantifiers correct.
- [ ] Non-elementary results are **cited** rather than asserted (see check 6).

*How to check:* work through the derivation line by line; a step you have to
"take on faith" is a gap.

### 4. Dimensions

- [ ] **Every matrix/vector/tensor shape is consistent** through the math and the
      code; matmuls conform, broadcasts are intentional, index ranges are correct.
- [ ] Where an object has a shape/sign/normalization invariant (a Jacobian is
      (outputs × inputs); a covariance is symmetric PSD; a probability vector sums
      to 1), the notebook **states and, in code, checks it** — per the
      [Exercise Framework](EXERCISE_FRAMEWORK.md#dimensional-reasoning-and-numerical-sanity-checks).

*How to check:* annotate each equation and array with its shape; a mismatch or an
unchecked invariant fails.

### 5. Numerical implementation

- [ ] **The code computes what the mathematics says** — same formula, same
      convention, same sign.
- [ ] It is verified against an **independent oracle** — a finite-difference
      check, a trusted library (`numpy.linalg`, `scipy`, `torch.autograd`,
      `sklearn`), or a closed form — **not** merely "runs without error," and
      **not** by comparing the implementation to a copy of itself. This mirrors
      [`MATH_REGRESSION.md`](MATH_REGRESSION.md)'s triangulation principle.
- [ ] Numerically fragile operations use a stable formulation (log-sum-exp,
      subtract-the-max softmax, solve instead of explicit inverse) or say why they
      don't need to.

*How to check:* find the line that verifies the implementation against something
external. If there isn't one, it fails.

### 6. References

- [ ] Non-elementary claims cite an **authoritative source** (textbook + section,
      or paper + equation/theorem number) in *Further Reading* or inline.
- [ ] Citations are **accurate** — the source actually says what it's cited for,
      including author(s), year, and venue.
- [ ] The citation is of the **right kind for its role** (see the four source
      types below). In particular, a *named theorem* is attributed to a theorem
      source, an *empirical number or fitted constant* is cited at its point of
      use to the original research it comes from, and a *library/API behavior* is
      backed by official documentation.

**Four kinds of source — use the one that fits the claim's role:**

| Source type | Cite it for | Example |
|---|---|---|
| **Further reading** | Going deeper on the topic generally; the standard textbook treatment. | *Strang, Introduction to Linear Algebra, Ch. 7.* |
| **Theorem source** | A named result the notebook states or uses. Attribute the theorem itself (name + originator/year, or a textbook that proves it), distinct from "further reading." | *Eckart & Young (1936); see Horn & Johnson, Matrix Analysis, Thm 7.4.9.* |
| **Original research** | A specific empirical claim, benchmark number, fitted constant, or a technique's introduction. Cite the paper the number/method actually comes from, **at the point of use**. | *the Chinchilla constants are from Hoffmann et al. (2022), Table 3.* |
| **Implementation / official documentation** | The behavior, default, or API of a library the code relies on. | *torch.nn.functional.scaled_dot_product_attention, PyTorch docs.* |

`Further Reading` at the end of a notebook is for the *further-reading* and often
*original-research* kinds. A **named theorem's source** belongs inline where the
theorem is stated (e.g. "the **spectral theorem** (see Strang, Ch. 6)") or, if
substantial, as its own labelled Further Reading entry — not silently folded into
generic further reading. An **unusually strong or precise empirical claim** must
carry an original-research citation at its point of use, or be softened to what
the evidence supports (see [Part B → strong claims](#strong-and-precise-claims)).

*How to check:* spot-check one non-trivial claim against its citation, and
confirm each named theorem and each specific number is attributed to the right
kind of source.

### 7. AI connection

- [ ] The **"Why This Matters for AI"** section makes a **specific, working-code**
      connection to a real ML/LLM system or technique — not a vague gesture at
      "this is used in deep learning."
- [ ] The connection is **mathematically honest**: the notebook's math genuinely
      underlies the cited application.

*How to check:* can you name the exact technique/architecture/paper the section
connects to, and does its code demonstrate the link? If not, it fails.

### 8. Exercises

- [ ] **All six levels present, in order**: COMPUTE, UNDERSTAND, DERIVE,
      IMPLEMENT, APPLY, CHALLENGE (see
      [`EXERCISE_FRAMEWORK.md`](EXERCISE_FRAMEWORK.md)).
- [ ] Each is **calibrated to the notebook's difficulty** and includes the
      required solution depth (full solution for COMPUTE/UNDERSTAND, outline for
      DERIVE, self-check for IMPLEMENT/APPLY, rubric for CHALLENGE), inside a
      collapsed `<details>` block.
- [ ] Exercises **don't duplicate** each other or an earlier notebook's take on a
      recurring idea.
- [ ] **Every numeric answer in a solution/self-check was verified against a live
      computation** before being written down.

*How to check:* confirm six level headings, six `<details>` blocks, and run any
numeric solution.

---

## Part B — Structural, executable, and style checks

Required for every notebook change.

### Structure

- [ ] Follows the six-section template (Learning Objective → Theory → Visual
      Intuition → Implementation from Scratch → Why This Matters for AI →
      Exercises); see [`CONTRIBUTING.md`](../CONTRIBUTING.md).
- [ ] Header table present and correct: Difficulty, Prerequisites (backward-only,
      by code), Time, Colab GPU.
- [ ] `LEARNING_PATH.md` updated if a notebook is added/renamed/re-scoped (rows,
      track tables, dependency graph, rigor classification).

### Strong and precise claims

- [ ] **Superlatives and absolutes** ("the best", "the tightest known", "always",
      "never", "state-of-the-art", "the most effective") are either (a) backed by
      a citation, (b) mathematically justified in-context (e.g. "a gradient field
      *always* has zero curl" — true by definition), or (c) softened to what the
      evidence supports ("often outperforms", "among the tightest", "in these
      experiments").
- [ ] **Specific empirical numbers, benchmark results, and fitted constants**
      carry an original-research citation **at their point of use** (not only in
      Further Reading), or are hedged as illustrative.
- [ ] **Historical-primacy claims** ("the first to…") are cited or removed.

*How to check:* search the notebook for superlatives and bare numbers; each
should be sourced, provably true in context, or softened. A correct-but-unhedged
absolute is fine when it is *mathematically* absolute; an *empirical* absolute
almost never is.

### Executable

- [ ] **Runs top-to-bottom in a fresh kernel** with no errors and no leftover
      error output.
- [ ] Uses **only dependencies in `requirements.txt`** (bounded ranges; no new
      dependency without discussion — see [`docs/CI.md`](CI.md)).
- [ ] Passes structural validation (`python tools/ci/validate_notebooks.py`).
- [ ] Passes the audit harness locally where feasible
      (`python -m notebook_audit --notebook <path>`; see
      [`NOTEBOOK_AUDIT.md`](NOTEBOOK_AUDIT.md)).
- [ ] Deterministic where it matters (seeded RNG); no reliance on out-of-order
      cell execution.

### Visualization & style

- [ ] Every plot has a **title and axis labels** (and a legend when >1 series).
- [ ] Prefers geometric/visual intuition before formulas where possible.
- [ ] Code comments explain the **why**, not the what.
- [ ] Output cells cleared of stray large outputs / absolute local paths.

---

## How to run the checks locally

```bash
# structural validity of every notebook
python tools/ci/validate_notebooks.py

# execute one notebook in a fresh kernel and classify any failure
PYTHONPATH=tools python -m notebook_audit --notebook <path> --kernel-name python3

# the mathematical regression suite (independent identity checks)
PYTHONPATH=tools pytest tools/math_regression/tests/ -q
```

See [`docs/CI.md`](CI.md) for how these map to the CI tiers, and
[`REVIEWER_CHECKLIST.md`](REVIEWER_CHECKLIST.md) for what a reviewer verifies per
PR type.
