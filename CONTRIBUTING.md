# Contributing to Math for AI/ML/LLMs

Thanks for considering a contribution! Contributions of all sizes are welcome — fixing a typo
in a theory section, adding an exercise, improving a plot, or proposing and writing an entirely
new notebook.

## Ways to Contribute

All 89 notebooks have complete content, so the highest-impact contributions now are:

- **Improve existing content.** Clarify an explanation, fix a mathematical error, improve a
  visualization, or make an implementation more readable.
- **Add exercises.** More warm-up/practice/challenge exercises are always useful.
- **Report or fix issues.** Broken Colab links, code that errors out, outdated library APIs.
- **Propose a new topic.** Open an issue using the `topic-request` label (see
  [`.github/ISSUE_TEMPLATE/new_topic_request.md`](.github/ISSUE_TEMPLATE/new_topic_request.md)).
- **Translate.** See the Translation Guidelines below.

## How to Add a New Notebook

1. **Start from the template.** Every notebook follows the structure in
   [`_templates/notebook_template.ipynb`](_templates/notebook_template.ipynb). Copy it rather
   than building a notebook's structure from scratch.
2. **Fill in every section:**
   - **Header table** — difficulty (1–10, shown as a block bar), prerequisites (reference
     prior notebooks by their module.number code, e.g. `01.06`), estimated time in minutes,
     and whether a Colab GPU is needed.
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
   - **🏋️ Exercises** — exactly three: a warm-up, a practice problem, and a challenge that
     connects back to an ML/LLM system.
3. **Cross-reference other notebooks** where relevant: "Recall from `01.06` that
   eigenvalues..." Link to the actual notebook file using a relative path.
4. **Run the whole notebook top to bottom** before opening a PR, and clear any leftover
   error output.

## Review Criteria

Pull requests are reviewed against four criteria:

1. **Theory accuracy** — the mathematics must be correct and precisely stated. Cite a source
   in Further Reading if the result is non-elementary.
2. **Runnable code** — every code cell must execute without errors, top to bottom, in a fresh
   kernel, using only the dependencies in `requirements.txt`.
3. **AI/ML/LLM connection** — the "Why This Matters for AI" section must contain a genuine,
   specific connection with working code, not a vague gesture at "this is used in deep
   learning."
4. **Exercises included** — all three difficulty levels must be present and reasonable.

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
3. Run the notebook(s) you touched top to bottom in a fresh kernel.
4. Open a pull request describing what changed and, for new content, which review criteria
   it satisfies.

If you're not sure whether an idea fits, open an issue first and we can discuss it there.
