# Contributing to Math for AI/ML/LLMs

Thanks for considering a contribution! Contributions of all sizes are welcome — fixing a typo
in a theory section, adding an exercise, improving a plot, or proposing and writing an entirely
new notebook.

This project sits at the intersection of mathematics, machine learning, education, and
software, and it needs all four. The next section is a set of on-ramps so you can find the
highest-value place to start *from your background* — you do **not** need to be strong in all
four areas to contribute.

## Where to start (by background)

Pick the row that sounds most like you. Each points to where your expertise is most needed and
the checklist that will be applied to your work. None of these are gates — a mathematician is
welcome to fix a bug, and a software engineer is welcome to propose a topic.

### 🧮 If you're a mathematician

Your superpower is **correctness and precision**. The most valuable things you can do:

- **Audit derivations and proofs** — file a [Mathematical error](#reporting-issues) issue (or a
  PR) when a step doesn't follow, an assumption is missing, or notation is abused. Checks 1–3
  and 6 of the [notebook quality checklist](docs/NOTEBOOK_QUALITY_CHECKLIST.md) are exactly your
  domain.
- **Tighten statements** — add a missing hypothesis, correct a quantifier, or make an informal
  argument rigorous.
- You do **not** need to be a strong programmer: you can report a math error precisely and let
  someone else land the code fix, or pair on a PR. If you *do* touch code, an independent
  numeric check (SymPy, a small NumPy snippet) is the bar, not production engineering.
- **Start here:** [`docs/RIGOR_FRAMEWORK.md`](docs/RIGOR_FRAMEWORK.md) for what level of rigor
  each notebook targets, then the eight mathematical checks in the
  [quality checklist](docs/NOTEBOOK_QUALITY_CHECKLIST.md).

### 🤖 If you're an ML researcher or practitioner

Your superpower is the **AI/ML connection** and knowing what's actually used. The most valuable
things you can do:

- **Strengthen "Why This Matters for AI" sections** — make a connection specific and honest,
  add a working-code link to a real technique/paper, or flag one that overclaims (check 7).
- **Propose research-adjacent content** — a [Curriculum proposal](#reporting-issues) for a
  technique the curriculum is missing, classified against
  [`docs/RIGOR_FRAMEWORK.md`](docs/RIGOR_FRAMEWORK.md).
- **Reproduce and stress-test** — the [capstone system](12_Capstone_Projects/capstones/README.md)
  (paper reproduction, research hypothesis) is a natural home for research-style contributions.
- **Start here:** the [capstone system](12_Capstone_Projects/capstones/README.md) and any
  notebook's "Why This Matters for AI" section.

### 🎓 If you're an educator

Your superpower is **pedagogy** — knowing where learners get stuck and how to unstick them. The
most valuable things you can do:

- **Improve explanations and visual intuition** — clarify a confusing passage, add a geometric
  picture before a formula, or fix an analogy that misleads.
- **Author or refine exercises** — the six-level framework
  ([`docs/EXERCISE_FRAMEWORK.md`](docs/EXERCISE_FRAMEWORK.md)) is where teaching craft lands
  (check 8). UNDERSTAND-level questions targeting common misconceptions are especially valued.
- **Translate** a module (see [Translation Guidelines](#translation-guidelines)).
- You do **not** need to derive new theorems: your contributions are graded on clarity and
  correctness of *presentation*, and reviewers know the difference.
- **Start here:** [`docs/EXERCISE_FRAMEWORK.md`](docs/EXERCISE_FRAMEWORK.md) and the Style
  Guidelines below.

### 💻 If you're a software engineer

Your superpower is **tooling, reproducibility, and code quality**. The most valuable things you
can do:

- **Fix notebook bugs** — cells that error, hang, or rely on out-of-order execution (file a
  [Notebook bug](#reporting-issues) or open a PR); the audit harness
  ([`docs/NOTEBOOK_AUDIT.md`](docs/NOTEBOOK_AUDIT.md)) classifies these.
- **Improve CI, tooling, and reproducibility** — see [`docs/CI.md`](docs/CI.md) for the two-tier
  CI, [`docs/MATH_REGRESSION.md`](docs/MATH_REGRESSION.md) for the identity-testing suite, and
  the harness under `tools/`.
- **Harden numerical implementations** — replace an unstable formula, add a seed, make a check
  independent (check 5).
- You do **not** need deep math: a clean bug fix that keeps the notebook's math unchanged is a
  great contribution.
- **Start here:** [`docs/CI.md`](docs/CI.md) and [`docs/NOTEBOOK_AUDIT.md`](docs/NOTEBOOK_AUDIT.md).

## Ways to Contribute

All 104 notebooks (14 modules) have complete content, so the highest-impact contributions now are:

- **Improve existing content.** Clarify an explanation, fix a mathematical error, improve a
  visualization, or make an implementation more readable.
- **Add exercises.** Every notebook's Exercises section follows the six-level framework in
  [`docs/EXERCISE_FRAMEWORK.md`](docs/EXERCISE_FRAMEWORK.md) (COMPUTE, UNDERSTAND, DERIVE,
  IMPLEMENT, APPLY, CHALLENGE) — improving an existing level's solution, tightening a dimensional
  or numerical sanity check, or strengthening a CHALLENGE's rubric are all useful contributions.
- **Report or fix issues.** Broken Colab links, code that errors out, outdated library APIs.
- **Propose a new topic.** Open an issue using the `topic-request` label (see
  [`.github/ISSUE_TEMPLATE/new_topic_request.md`](.github/ISSUE_TEMPLATE/new_topic_request.md)).
- **Add or refine a capstone.** The [capstone system](12_Capstone_Projects/capstones/README.md)
  is a six-rung ladder of graded project specifications. New specs must follow the shared
  ten-section structure and five-axis rubric documented in its README, preserve the
  increasing-difficulty ordering, and honor the "derive, don't cite" and "never test against a
  copy of itself" rules.
- **Translate.** See the Translation Guidelines below.

## Reporting Issues

Open an issue from the [chooser](.github/ISSUE_TEMPLATE/) — blank issues are disabled so every
report arrives with the context needed to act on it. Pick the template that fits:

| Template | Use it when |
|---|---|
| 🧮 [Mathematical error](.github/ISSUE_TEMPLATE/mathematical_error.md) | A definition, derivation, proof, formula, or numerical claim is **wrong**. Structured around the eight mathematical checks (notation, assumptions, derivation, dimensions, numerical implementation, references). |
| 🐛 [Notebook bug](.github/ISSUE_TEMPLATE/notebook_bug.md) | Code **doesn't run correctly** — a cell errors, hangs, produces wrong output, or won't run top-to-bottom. Captures environment + traceback. |
| 📚 [Curriculum proposal](.github/ISSUE_TEMPLATE/curriculum_proposal.md) | A fleshed-out proposal to **add a notebook or rework content**, with placement, prerequisites, rigor, and the AI connection. |
| 💡 [New topic request](.github/ISSUE_TEMPLATE/new_topic_request.md) | A quick "it'd be nice to cover X" — the lightweight version of a proposal. |

For open-ended questions, use [Discussions](https://github.com/NiravRVaghasiya/maths-for-ai/discussions)
rather than an issue.

## How to Add a New Notebook

1. **Start from the template.** Every notebook follows the structure in
   [`_templates/notebook_template.ipynb`](_templates/notebook_template.ipynb). Copy it rather
   than building a notebook's structure from scratch.
2. **Fill in every section:**
   - **Header table** — difficulty (1–10, shown as a block bar), prerequisites (reference
     prior notebooks by their module.number code, e.g. `01.06`), estimated time in minutes,
     and whether a Colab GPU is needed. List every notebook your new one directly needs — not
     the full transitive closure — following the same convention as existing notebooks (e.g.
     `01.01–01.10` for "all of Module 01," or a comma-separated list of specific codes). See
     [`LEARNING_PATH.md`](LEARNING_PATH.md) for how these prerequisite fields are turned into
     the curriculum's dependency graph; after adding a notebook, double-check by hand that your
     prerequisites don't point forward (a prerequisite must be an *earlier* notebook) or to a
     nonexistent notebook, and consider whether `LEARNING_PATH.md`'s
     tables need a new row for your notebook. Also check whether your notebook belongs in one
     or more of the [six learning tracks](LEARNING_PATH.md#-learning-tracks-six-ways-through-the-curriculum)
     — if it does, add its code to that track's notebook-sequence table too, so the track stays
     a complete, closure-verified subset of the curriculum rather than silently missing new
     content. When adding your notebook's row to `LEARNING_PATH.md`, also classify it against
     [`docs/RIGOR_FRAMEWORK.md`](docs/RIGOR_FRAMEWORK.md): its rigor level (INTUITION,
     COMPUTATIONAL, UNDERGRADUATE, PROOF-BASED, GRADUATE, or RESEARCH), whether proofs are
     load-bearing (None/Light/Central), whether implementation is essential or merely
     illustrative, and what AI/ML background a learner should already have.
   - **🎯 Learning Objective** — one or two sentences, stated plainly.
   - **📐 Theory** — the mathematical explanation, with LaTeX (`$...$` inline, `$$...$$`
     block) that renders correctly in Jupyter/Colab. Define every symbol you use.
   - **👁️ Visual Intuition** — at least one matplotlib plot with a title, axis labels, and a
     legend where applicable. Prefer geometric/visual intuition before (or alongside) formulas.
   - **🐍 Implementation from Scratch** — a working NumPy (or PyTorch, where appropriate)
     implementation of the concept. Comments should explain *why*, not just *what*.
   - **🤖 Why This Matters for AI** — a concrete, working-code connection to a real ML/LLM
     system or technique. This section is not optional filler — it's the reason the notebook
     exists.
   - **🏋️ Exercises** — exactly six, one per level, always in this order: COMPUTE, UNDERSTAND,
     DERIVE, IMPLEMENT, APPLY, CHALLENGE. See
     [`docs/EXERCISE_FRAMEWORK.md`](docs/EXERCISE_FRAMEWORK.md) for what each level tests, how to
     calibrate depth to your notebook's difficulty rating, the solution-depth policy (full
     solutions for COMPUTE/UNDERSTAND, a full outline for DERIVE, a self-check condition for
     IMPLEMENT/APPLY, a rubric for CHALLENGE), and the exact markdown template to use.
3. **Cross-reference other notebooks** where relevant: "Recall from `01.06` that
   eigenvalues..." Link to the actual notebook file using a relative path.
4. **Run the whole notebook top to bottom** before opening a PR, and clear any leftover
   error output.

## Review Criteria

Pull requests are reviewed against four criteria:

1. **Theory accuracy** — the mathematics must be correct and precisely stated. Cite a source
   for any non-elementary result, matched to the claim's role — *further reading* (the standard
   textbook treatment), a *theorem source* (attribute a named theorem to its originator/year or a
   text that proves it, inline where it's stated), *original research* (cite specific empirical
   numbers, benchmark results, and fitted constants at their point of use), or *implementation /
   official documentation* (for library behavior the code relies on). Unusually strong claims
   (superlatives, absolutes, precise empirical numbers) must be supported by a citation, justified
   in-context, or softened — see the [notebook quality checklist](docs/NOTEBOOK_QUALITY_CHECKLIST.md#6-references).
   Core mathematical identities (linear
   algebra, calculus/gradients, probability, optimization, numerical methods) are guarded by the
   regression suite in [`docs/MATH_REGRESSION.md`](docs/MATH_REGRESSION.md); if you add or change
   an identity, add a triangulated test there (analytical vs numerical vs trusted library).
2. **Runnable code** — every code cell must execute without errors, top to bottom, in a fresh
   kernel, using only the dependencies in `requirements.txt`. CI enforces this: see
   [`docs/CI.md`](docs/CI.md) for the two-tier setup (fast per-PR checks + nightly full-suite
   validation) and how to reproduce each check locally before opening a PR.
3. **AI/ML/LLM connection** — the "Why This Matters for AI" section must contain a genuine,
   specific connection with working code, not a vague gesture at "this is used in deep
   learning."
4. **Exercises included** — all six levels (COMPUTE, UNDERSTAND, DERIVE, IMPLEMENT, APPLY,
   CHALLENGE) must be present, calibrated to the notebook's difficulty rating, and each include
   a solution/outline/self-check/rubric per [`docs/EXERCISE_FRAMEWORK.md`](docs/EXERCISE_FRAMEWORK.md).

These four criteria expand into a concrete, tickable bar in the
[**notebook quality checklist**](docs/NOTEBOOK_QUALITY_CHECKLIST.md) — in particular its **eight
mathematical checks** (notation, assumptions, derivations, dimensions, numerical implementation,
references, AI connection, exercises), which every mathematical contribution must satisfy. The
same eight checks appear in the pull-request template, and
[**`docs/REVIEWER_CHECKLIST.md`**](docs/REVIEWER_CHECKLIST.md) describes how a reviewer verifies
them per PR type. Author and reviewer are held to exactly the same bar.

## Style Guidelines

- Write as an expert teacher: clear, encouraging, and precise. Avoid unnecessary jargon; define
  what you must use.
- Reach for analogies and geometric intuition before diving into formulas.
- Code comments explain the *why*, not the *what* — the code already says what it does.
- Every plot needs a title and axis labels; add a legend whenever more than one series is
  plotted.
- No assumed knowledge beyond high-school algebra in Module 00; every later module should
  build only on notebooks that come before it.

## Translation Guidelines

Translations are welcome and should mirror the repository structure under
`translations/{language-code}/` (e.g. `translations/es/01_Linear_Algebra/...`). Translate
prose and exercises; keep code, variable names, and LaTeX untouched. Please translate a full
module at a time rather than scattering partial notebooks, so learners can follow a coherent
path in their language.

## Submitting Your Contribution

1. Fork the repository and create a branch for your change.
2. Make your changes, following the guidelines above.
3. Run the notebook(s) you touched top to bottom in a fresh kernel, and the relevant local
   checks (see [`docs/NOTEBOOK_QUALITY_CHECKLIST.md`](docs/NOTEBOOK_QUALITY_CHECKLIST.md#how-to-run-the-checks-locally)).
4. Open a pull request. The [PR template](.github/PULL_REQUEST_TEMPLATE.md) will prompt you for
   a summary, the type of change, your verification steps, and — for mathematical contributions —
   the eight-check sub-checklist. Fill in what applies.

Your PR will be reviewed against [`docs/REVIEWER_CHECKLIST.md`](docs/REVIEWER_CHECKLIST.md);
reading it before submitting tells you exactly what a reviewer will look for.

If you're not sure whether an idea fits, open an issue first (a
[Curriculum proposal](.github/ISSUE_TEMPLATE/curriculum_proposal.md) or a
[Discussion](https://github.com/NiravRVaghasiya/maths-for-ai/discussions)) and we can discuss it
there.
