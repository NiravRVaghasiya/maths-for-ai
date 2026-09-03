# 🎓 Capstone System

The capstone system is where you *prove* you understand the mathematics of this
curriculum by building AI systems that could not work if you didn't. Each
capstone is a **project specification**, not a tutorial: it tells you what to
derive, build, and measure, and how your work will be judged — but it does not
hand you the answer. Deriving the mathematics and defending your results is the
assessment.

This is complementary to the module-12 *teaching notebooks*
(`12_Capstone_Projects/01_…`–`05_…`), which walk you through worked syntheses
with full solutions. The specs here are the graded, do-it-yourself counterpart:
same spirit, no answer key. See [Relationship to the teaching
notebooks](#relationship-to-the-teaching-notebooks).

## The difficulty ladder

Six capstones, each strictly harder than the last, and each depending on the
mathematical machinery you built in the previous one. Do them in order — later
capstones assume you can already do everything the earlier ones demand.

| # | Capstone | Difficulty | Core mathematical demonstration | Spec |
|---|---|---|---|---|
| 1 | Linear Regression from Scratch | ██░░░░░░░░ 2/10 | Optimization of a convex quadratic: normal equations *and* gradient descent, shown to reach the same optimum | [`01_linear_regression.md`](01_linear_regression.md) |
| 2 | Neural Network + Manual Backpropagation | ████░░░░░░ 4/10 | The multivariate chain rule made mechanical: hand-derived per-layer gradients, verified by gradient checking | [`02_neural_network_backprop.md`](02_neural_network_backprop.md) |
| 3 | PCA / SVD Representation Analysis | █████░░░░░ 5/10 | Eigendecomposition and SVD as the *same* object, used to analyze what a representation encodes | [`03_pca_svd_representation.md`](03_pca_svd_representation.md) |
| 4 | Transformer Attention Implementation | ███████░░░ 7/10 | Attention derived, not copied: the √dₖ variance argument, softmax as a differentiable soft-argmax, multi-head factorization | [`04_transformer_attention.md`](04_transformer_attention.md) |
| 5 | Research-Paper Mathematical Reproduction | ████████░░ 8/10 | Decoding a paper's notation and reproducing one of its quantitative claims from its equations | [`05_paper_reproduction.md`](05_paper_reproduction.md) |
| 6 | Experimental Research Hypothesis | ██████████ 10/10 | Formulating a falsifiable hypothesis, designing controlled experiments, and defending (or retracting) a conclusion with statistical rigor | [`06_research_hypothesis.md`](06_research_hypothesis.md) |

The ramp is deliberate:

- **1 → 2**: from a *single* convex objective with a closed form to a *composed*
  non-convex one with no closed form — the chain rule becomes load-bearing.
- **2 → 3**: from *supervised* gradient learning to *unsupervised* structure
  discovery — spectral methods instead of gradient descent.
- **3 → 4**: from static linear representations to *content-dependent* ones —
  attention is a data-dependent linear combination, which is why it needed
  everything from 1–3.
- **4 → 5**: from building a *known* result to reconstructing someone else's from
  their paper — reading mathematics you didn't write.
- **5 → 6**: from reproducing a claim to *making and testing your own* — the jump
  from student to researcher.

## The shared specification structure

Every capstone spec has the same ten sections, in this order. When you write up
your submission, mirror them.

1. **Problem statement** — what you are building and the one-sentence question it
   answers.
2. **Prerequisites** — the curriculum notebooks whose mathematics you must
   already command, with the specific result each supplies.
3. **Mathematical formulation** — the precise objects, objective, and identities,
   stated in notation. This is *what is true*; the derivation is *why*.
4. **Derivation requirements** — the results you must derive yourself (not cite).
   These are the graded mathematical core.
5. **Implementation** — what to build, the required interfaces, and the rule that
   you may use a trusted library only as an *oracle to check against*, never as
   the thing under test.
6. **Experiments** — the controlled comparisons that turn your implementation
   into evidence.
7. **Expected outputs** — concrete artifacts (numbers, plots, tables) a reviewer
   can check, with target values where they are knowable in advance.
8. **Evaluation criteria** — the rubric (below), instantiated for this capstone.
9. **Extensions** — optional harder variants for going beyond the bar.
10. **Research directions** — open questions the capstone opens onto, connecting
    it to real research.

## The evaluation rubric

Each capstone is scored on five axes. The weighting shifts along the ladder:
early capstones weight correctness of derivation and implementation; later ones
weight experimental design and the honesty of the analysis. The bar for "meets
expectations" is stated concretely in each spec's Evaluation section.

| Axis | What it measures |
|---|---|
| **Mathematical correctness** | Are the derivations right, complete, and in consistent notation? Do the stated identities actually hold? |
| **Derivation independence** | Did you *derive* the required results rather than restate them, and does your implementation follow from your own derivation rather than from a library's behavior? |
| **Implementation fidelity** | Does the code compute what the mathematics says, verified against an independent oracle (finite differences, a trusted library, a closed form) — not merely "runs without error"? |
| **Experimental rigor** | Are comparisons controlled (one variable at a time), seeded/reproducible, and reported with appropriate uncertainty? Are negative results reported honestly? |
| **Communication** | Can a reader who knows the math follow your write-up from problem to conclusion, with claims tied to specific evidence? |

### Two rules that apply to every capstone

- **Derive, don't cite, the graded core.** Each spec names the results you must
  produce yourself. You may cite anything *outside* that core (e.g. use a
  known matrix identity in passing), but the derivation requirements are the
  point of the exercise.
- **Never test an implementation against a copy of itself.** A trusted library
  (`numpy.linalg`, `scipy`, `torch.autograd`, `sklearn`) is an **oracle** you
  check your from-scratch code against, in the spirit of
  [`docs/MATH_REGRESSION.md`](../../docs/MATH_REGRESSION.md). Your gradient is
  correct because it matches a finite-difference gradient *and* autograd — three
  independently-derived answers agreeing — not because it equals itself.

## Prerequisites and where each capstone sits

The capstones draw on the same 13 modules as the rest of the curriculum. Roughly:

| Capstone | Leans hardest on |
|---|---|
| 1. Linear regression | `01` Linear Algebra, `02` Calculus (gradients), `04` Optimization (gradient descent, convexity) |
| 2. NN + backprop | Capstone 1, `02` (chain rule, Jacobians), `04` (optimizers), `05` (cross-entropy) |
| 3. PCA / SVD | `01` (eigenvalues, SVD, `07`/`08` advanced LA), `03` (covariance) |
| 4. Attention | Capstones 1–3, `01.10`, `03` (variance), softmax |
| 5. Paper reproduction | Capstones 1–4, plus whatever the chosen paper needs |
| 6. Research hypothesis | All of the above, plus `03`/`09` (statistics, hypothesis testing) |

## Relationship to the teaching notebooks

The five existing module-12 notebooks (`12.01`–`12.05`) remain the *taught*
capstones with full worked solutions and are still referenced by the six
learning tracks in [`LEARNING_PATH.md`](../../LEARNING_PATH.md). This spec-based
system reframes and extends them into an assessable, six-rung ladder:

| This system | Closest teaching notebook(s) | What the spec adds |
|---|---|---|
| 1. Linear regression | (foundational; drawn from `04.02`) | A graded entry-level rung the notebooks didn't have |
| 2. NN + backprop | `12.02` Derive Backprop | A full MLP + training task and a gradient-checking bar |
| 3. PCA / SVD | (drawn from `01.07`) | A representation-analysis capstone the notebooks didn't have |
| 4. Attention | `12.01` Build Attention, `12.04` GPT analysis | An unassisted spec version |
| 5. Paper reproduction | `12.05` Read a Paper | Moves from *reading* to *reproducing a claim* |
| 6. Research hypothesis | (new) | An open-ended research rung above everything else |

Nothing here removes or renumbers the existing notebooks; the specs are additive.
