<p align="center">
  <img src="_assets/images/readme_banner.png" alt="Math for AI/ML/LLMs" width="100%">
</p>

# 🧮 Math for AI/ML/LLMs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NiravRVaghasiya/maths-for-ai/blob/main/00_Prerequisites/01_mathematical_notation.ipynb)
[![Python 3.11–3.13](https://img.shields.io/badge/python-3.11%E2%80%933.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Notebooks](https://img.shields.io/badge/notebooks-104-orange.svg)](#-complete-module-list)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/NiravRVaghasiya/maths-for-ai?style=social)](https://github.com/NiravRVaghasiya/maths-for-ai)
[![GitHub forks](https://img.shields.io/github/forks/NiravRVaghasiya/maths-for-ai?style=social)](https://github.com/NiravRVaghasiya/maths-for-ai/fork)
[![Last Commit](https://img.shields.io/github/last-commit/NiravRVaghasiya/maths-for-ai)](https://github.com/NiravRVaghasiya/maths-for-ai)

> A structured, mathematics-first, implementation-driven curriculum for understanding modern
> AI/ML — from foundational linear algebra and calculus through the theory behind transformers,
> LoRA, and diffusion models. 104 Jupyter notebooks across 14 modules, all Google Colab
> compatible.

This is a curriculum, not a reference: it takes you along a dependency-ordered path from the
prerequisites up to research-level topics, rather than trying to be an encyclopedia of all
mathematics. It is deliberately scoped to the mathematics that actually shows up when you read,
build, and reason about modern ML/LLM systems — deep enough to derive the key results yourself,
not a survey of everything a mathematician knows.

Concretely, every notebook pairs a mathematical idea with a plot, a from-scratch NumPy/PyTorch
implementation, and a direct connection to how that idea appears inside real ML/LLM systems.

### What "mathematics-first, implementation-driven" means

- **Mathematics-first** — each topic starts from definitions and derivations, with symbols
  defined and results built up rather than asserted. Where a notebook states a named theorem, it
  attributes it; where it makes an empirical claim, it cites the source (see
  [`docs/NOTEBOOK_QUALITY_CHECKLIST.md`](docs/NOTEBOOK_QUALITY_CHECKLIST.md)).
- **Implementation-driven** — you don't just read the math, you build it from scratch in NumPy/
  PyTorch and check it against a trusted reference, so understanding is verified in code, not
  assumed.
- **Structured** — notebooks form a verified dependency graph and six role-based learning tracks,
  so there's a defined order in and a defined destination out.

### Scope: five layers of mathematics

The curriculum spans five distinguishable layers, so you can tell what a topic is *for* before
you invest in it. This maps onto the module classification below (🟢/🟡/🔵/🔴):

| Layer | What it covers | Modules |
|---|---|---|
| **Foundational** | The core every ML practitioner uses daily: linear algebra, calculus, probability, optimization. | `00`–`04` (🟢 CORE) |
| **Professional** | What practical training, fine-tuning, and evaluation work leans on: information theory, numerical methods, and the applied capstones. | `05`, `06`, `12` (🟡 IMPORTANT) |
| **LLM-relevant** | Mathematics that pays off specifically for language models — the linear algebra behind LoRA/attention and the NLP-adjacent discrete math. | `07`, `08` (🔵 SPECIALIZED) |
| **Research** | Foundations for generative models and learning theory: advanced probability and its concentration/generalization tools. | `09` (🔵 SPECIALIZED) |
| **Specialized / advanced** | Graduate-level theory for specific research directions: differential geometry, functional analysis, information geometry, the NTK. | `10`, `11` (🔴 ADVANCED) |

These layers overlap — many LLM-relevant results build on foundational ones, and the research
layer draws on all of them — so treat them as a guide to *purpose and depth*, not as hard walls.
The [learning tracks](#-who-is-this-for) below thread through these layers in the order that fits
a given goal.

---

## 🧭 Start Here

New to the repo? In 30 seconds:

1. **Open the first notebook in Colab** — click the badge at the top, or start with
   [`00_Prerequisites/01_mathematical_notation.ipynb`](00_Prerequisites/01_mathematical_notation.ipynb).
   No install needed.
2. **Or run locally** — see [Installation](#-installation) (`pip install -r requirements.txt`,
   then `jupyter lab`).
3. **Pick a path for your goal** — choose a [learning track](#-who-is-this-for) (Beginner →
   Researcher) or a [fast-track path](#-fast-track-paths) to one specific destination like
   "understand transformers."
4. **Work through a notebook** — read the theory, run the from-scratch implementation, do the
   [six exercises](#-how-each-notebook-works). Every notebook is self-contained and states its
   prerequisites.

If you're brand new to the math behind ML, start with the
[🌱 AI/ML Beginner track](LEARNING_PATH.md#-track-aiml-beginner).

---

## 🎯 Who Is This For?

This repository is organized into six **role-based learning tracks** — each one a curated,
dependency-verified subset of the curriculum (nothing is duplicated per track; a track is just
a defined notebook set plus an order). Pick the one that matches your goal:

| Track | Notebooks | Est. Hours | For |
|---|---|---|---|
| 🌱 [AI/ML Beginner](LEARNING_PATH.md#-track-aiml-beginner) | 26 | ~46h | Understand the math behind ML for the first time |
| ⚙️ [ML Engineer](LEARNING_PATH.md#-track-ml-engineer) | 54 | ~105h | Build, train, and ship models day to day |
| 🧠 [Deep Learning Engineer](LEARNING_PATH.md#-track-deep-learning-engineer) | 63 | ~124h | Production-scale DL: numerics, mixed precision, GPT-scale models |
| 🤖 [LLM Engineer](LEARNING_PATH.md#-track-llm-engineer) | 74 | ~147h | Fine-tune, adapt, and deploy LLMs (LoRA/QLoRA) |
| 🔬 [ML Researcher](LEARNING_PATH.md#-track-ml-researcher) | 62 | ~125h | Generative models, learning theory, research papers |
| 🎓 [Mathematical ML Researcher](LEARNING_PATH.md#-track-mathematical-ml-researcher) | 104 | ~245h | Full theoretical foundations: information geometry, functional analysis, NTK |

Each track lists its exact starting prerequisites, required/optional modules, notebook
sequence, expected competency, and capstone in
**[`LEARNING_PATH.md`](LEARNING_PATH.md#-learning-tracks-six-ways-through-the-curriculum)**.
The tracks nest into two ladders that both start at Beginner and both pass through ML Engineer —
LLM Engineer and ML Researcher are siblings (different specializations of the same base), and
Mathematical ML Researcher is their union plus the two most advanced modules.

> **Note:** the per-track notebook counts and hour estimates above were computed against an
> earlier 89-notebook version of the curriculum. Newer material — Module 13 (Statistical
> Learning Theory) and several notebooks added to Modules 04, 06, and 09 — brings the total to
> **104 notebooks across 14 modules** (see the [module list](#-complete-module-list)) but is not
> yet folded into each track's transitive-closure count. The track *structure and ordering*
> remain correct; the numbers will be recomputed. Until then, treat the track figures as a
> lower bound.

## 🏗️ How Each Notebook Works

Every notebook in this repository follows the same six-part structure:

1. **🎯 Learning Objective** — what you'll understand by the end, plus a difficulty rating,
   prerequisites, and estimated time
2. **📐 Theory** — a clear mathematical explanation with properly rendered LaTeX
3. **👁️ Visual Intuition** — a plot or diagram that builds geometric intuition before the code
4. **🐍 Implementation from Scratch** — a pure NumPy/PyTorch implementation of the concept
5. **🤖 Why This Matters for AI** — a direct, working-code connection to real ML/LLM systems
6. **🏋️ Exercises** — six progressive levels (COMPUTE → UNDERSTAND → DERIVE → IMPLEMENT → APPLY
   → CHALLENGE), each with a solution, outline, self-check, or rubric — see
   [`docs/EXERCISE_FRAMEWORK.md`](docs/EXERCISE_FRAMEWORK.md)

<p align="center">
  <img src="_assets/images/notebook_structure.png" alt="Notebook Structure" width="100%">
</p>

## 🔗 Math → AI/ML/LLM Connections

The point of every notebook's **"Why This Matters for AI"** section is that the mathematics is
not abstract — each idea is load-bearing in a real system. A few examples:

| Mathematics | Powers… | Notebook |
|---|---|---|
| Eigen/SVD & low-rank structure | PCA, LoRA / QLoRA fine-tuning | `01.07`, `08.05`, `08.06` |
| The chain rule & Jacobians | Backpropagation / autograd | `02.04`, `02.10`, `12.02` |
| Softmax & the √dₖ scaling | Transformer attention | `01.10`, `12.01` |
| KL divergence & cross-entropy | Training losses, VAEs, distillation | `05.02`, `05.03` |
| Adam / momentum / convergence | Optimizers that train modern nets | `04.04`, `12.03` |
| Concentration & generalization bounds | Why over-parameterized nets generalize | `09.04`, `13.05`–`13.09` |
| Stochastic processes & SDEs | Diffusion models | `09.02`, `09.06` |

See **[`docs/MATH_TO_AI.md`](docs/MATH_TO_AI.md)** for the full map from math topic to AI/ML/LLM
technique, keyed to the notebook that makes each connection concrete.

## 🗺️ Visual Learning Path

![Math for AI learning path](_assets/images/learning-path.png)

See [`LEARNING_PATH.md`](LEARNING_PATH.md) for the six role-based tracks in full detail, the
complete prerequisite graph (module-level *and* notebook-level), a Mermaid dependency diagram,
per-notebook classification/rigor/AI-relevance tags, and narrow goal-oriented paths (for when
you want one destination notebook rather than a full role) computed directly from the
dependency graph. Every notebook's **rigor** — INTUITION, COMPUTATIONAL, UNDERGRADUATE,
PROOF-BASED, GRADUATE, or RESEARCH, plus whether proofs/implementation are load-bearing and what
AI/ML background is expected — is defined in [`docs/RIGOR_FRAMEWORK.md`](docs/RIGOR_FRAMEWORK.md).

## 📚 Complete Module List

This is the full 14-module inventory the tracks above are built from — useful if you want to
browse by subject rather than by role. Each module is tagged with its primary
[classification](LEARNING_PATH.md#classification-legend) — 🟢 CORE, 🟡 IMPORTANT, 🔵
SPECIALIZED, or 🔴 ADVANCED — based on how many other notebooks in the curriculum depend on it
and how universal it is for AI/ML work. A handful of individual notebooks are classified
differently from their module's default (e.g. cross-entropy loss in Module 05 is CORE even
though the rest of the module is IMPORTANT) — see [`LEARNING_PATH.md`](LEARNING_PATH.md) for
every per-notebook override and exactly why.

### 🟢 CORE — essential for any ML practitioner

| # | Module | Notebooks | Est. Hours |
|---|---|---|---|
| 00 | [Prerequisites & Notation](00_Prerequisites/) | 4 | 6 |
| 01 | [Linear Algebra](01_Linear_Algebra/) | 10 | 20 |
| 02 | [Calculus](02_Calculus/) | 10 | 18 |
| 03 | [Probability & Statistics](03_Probability_and_Statistics/) | 11 | 22 |
| 04 | [Optimization](04_Optimization/) | 12 | ~20 |

### 🟡 IMPORTANT — needed for practical training, fine-tuning, and evaluation work

| # | Module | Notebooks | Est. Hours |
|---|---|---|---|
| 05 | [Information Theory](05_Information_Theory/) | 7 | 12 |
| 06 | [Numerical Methods](06_Numerical_Methods/) | 8 | ~12 |
| 12 | [Capstone Projects](12_Capstone_Projects/) | 5 | 15 |

### 🔵 SPECIALIZED — high-value for a specific role or research direction

| # | Module | Notebooks | Est. Hours |
|---|---|---|---|
| 07 | [Discrete Mathematics](07_Discrete_Mathematics/) | 5 | 8 |
| 08 | [Advanced Linear Algebra](08_Advanced_Linear_Algebra/) | 6 | 14 |
| 09 | [Advanced Probability](09_Advanced_Probability/) | 8 | ~20 |
| 13 | [Statistical Learning Theory](13_Statistical_Learning_Theory/) | 9 | ~18 |

### 🔴 ADVANCED — graduate/research-level mathematical maturity

| # | Module | Notebooks | Est. Hours |
|---|---|---|---|
| 10 | [Differential Geometry & Topology](10_Differential_Geometry_and_Topology/) | 5 | 14 |
| 11 | [Functional Analysis](11_Functional_Analysis/) | 4 | 12 |

**Total: 104 notebooks across 14 modules.**

> Notebook counts are verified against the repository. Hour figures are rough estimates —
> those marked `~` are approximate; each notebook's own header carries a more precise
> reading-time estimate. Module 13 (Statistical Learning Theory) and the newer notebooks in
> Modules 04, 06, and 09 are complete content but are still being woven into the role-based
> [learning tracks](#-who-is-this-for) above.

<p align="center">
  <img src="_assets/images/curriculum_overview.png" alt="Curriculum Overview" width="100%">
</p>

> **Content status:** All 104 notebooks across these 14 modules have complete content — theory,
> visualizations, from-scratch implementations, AI/ML connections, and exercises — held to the
> bar in [`docs/NOTEBOOK_QUALITY_CHECKLIST.md`](docs/NOTEBOOK_QUALITY_CHECKLIST.md) and executed
> in CI. It is a living curriculum, not a finished textbook; see [`CONTRIBUTING.md`](CONTRIBUTING.md)
> if you'd like to improve or extend it.

## 🎓 Capstone System

Beyond the taught notebooks, the
[**capstone system**](12_Capstone_Projects/capstones/) is a graded, do-it-yourself
ladder of six increasingly hard projects that ask you to *prove* you understand the
math by building AI systems that couldn't work without it — with no answer key:

1. **Linear Regression from Scratch** — normal equations *and* gradient descent to the same optimum
2. **Neural Network + Manual Backpropagation** — hand-derived gradients, verified by gradient checking
3. **PCA / SVD Representation Analysis** — eigendecomposition and SVD as one object, used to analyze representations
4. **Transformer Attention Implementation** — attention *derived*, including the √dₖ scaling and its backward pass
5. **Research-Paper Mathematical Reproduction** — reproduce a paper's quantitative claim from its equations
6. **Experimental Research Hypothesis** — formulate, test, and honestly defend your own falsifiable hypothesis

Every capstone follows the same ten-part specification (problem statement,
prerequisites, mathematical formulation, derivation requirements, implementation,
experiments, expected outputs, evaluation criteria, extensions, research
directions) and is scored on a five-axis rubric. See the
[capstone system README](12_Capstone_Projects/capstones/README.md) for the full
ladder, rubric, and how it relates to the module-12 teaching notebooks.

## 🗂️ Repository Structure

```text
maths-for-ai/
├── 00_Prerequisites/ … 13_Statistical_Learning_Theory/   # 14 module directories (104 notebooks)
│   └── NN_topic_name.ipynb                                # one self-contained notebook per topic
├── 12_Capstone_Projects/
│   ├── 01_…–05_….ipynb                                    # taught capstone notebooks
│   └── capstones/                                         # graded do-it-yourself capstone specs
├── docs/                                                  # frameworks & guides
│   ├── MATH_TO_AI.md            # math → AI/ML/LLM technique map
│   ├── EXERCISE_FRAMEWORK.md    # the six-level exercise system
│   ├── RIGOR_FRAMEWORK.md       # per-notebook rigor classification
│   ├── NOTEBOOK_QUALITY_CHECKLIST.md · REVIEWER_CHECKLIST.md
│   ├── CI.md · NOTEBOOK_AUDIT.md · MATH_REGRESSION.md
│   └── LORA_PATHWAY.md · TRANSFORMER_PATHWAY.md · RESEARCH_PAPER_PATHWAY.md
├── tools/                                                 # repo tooling (not curriculum content)
│   ├── notebook_audit/          # executes & classifies notebook runs
│   ├── math_regression/         # tests mathematical identities
│   └── ci/                      # notebook structural validation
├── _templates/                  # notebook template
├── .github/                     # issue/PR templates, CI workflows
├── LEARNING_PATH.md             # the authoritative learning roadmap
├── CONTRIBUTING.md · CODE_OF_CONDUCT.md · SECURITY.md
├── requirements.txt · requirements-lock.txt · requirements-dev.txt · environment.yml · pyproject.toml
└── README.md
```

## 🚀 Quick Start

The simplest way to run everything locally:

```bash
git clone https://github.com/NiravRVaghasiya/maths-for-ai.git
cd maths-for-ai
pip install -r requirements.txt
jupyter lab
```

Or click the "Open in Colab" badge at the top of any notebook to run it in the cloud with zero
setup.

## 💻 Installation

**Recommended Python: 3.12** (any of 3.11, 3.12, or 3.13 works). Python 3.10 is not recommended
— it reaches end of life in October 2026 and the current scientific stack (NumPy 2.x) no longer
targets it.

Every notebook runs on **CPU** — no GPU is required for any notebook in the curriculum. A couple
of the heavier deep-learning notebooks train a little faster on a GPU but do not need one.

### Option A — pip (simple, forward-compatible)

Best for most learners. Uses bounded version ranges so you get recent, compatible releases:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

This installs the **CPU build of PyTorch** on Windows and macOS. On Linux, `pip install torch`
pulls a CUDA-enabled wheel by default; to force CPU-only on Linux, see
[CPU-only PyTorch](#cpu-only-pytorch) below.

### Option B — conda

```bash
conda env create -f environment.yml
conda activate maths-for-ai
jupyter lab
```

The conda environment pins the `cpuonly` PyTorch build from conda-forge.

### Option C — exact reproducible environment (lock file)

When you need a byte-for-byte reproducible environment (reproducing a reported result, CI, or
bisecting a regression), install the fully pinned lock instead of the ranges:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-lock.txt
```

`requirements-lock.txt` pins every direct and transitive dependency to the exact versions the
notebook suite was verified against. `requirements.txt` is the loose, forward-compatible set;
the lock file is the frozen snapshot.

### CPU-only PyTorch

On Linux the default PyTorch wheel bundles CUDA. If you have no NVIDIA GPU (or want the smaller
download), install the CPU build explicitly:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Then install the rest with the CPU torch already satisfied:

```bash
pip install -r requirements.txt
```

### Optional — GPU (CUDA) PyTorch

GPU is **optional** for this curriculum. If you have an NVIDIA GPU and want CUDA acceleration for
the deep-learning notebooks, install a CUDA build of PyTorch from the official index that matches
your driver's CUDA version (check the [PyTorch install selector](https://pytorch.org/get-started/locally/)
for the current recommended command):

```bash
# Example — CUDA 12.4 build (pick the CUDA tag that matches your system):
pip install torch --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

Verify the GPU is visible:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Everything else in `requirements.txt` is CPU/GPU-agnostic — only the `torch` wheel changes.

## 🏎️ Fast Track Paths

The [six learning tracks](#-who-is-this-for) above cover most goals — check there first. The
table below is for a **narrower** destination: one specific notebook rather than a full role.
Each path lists every module its goal notebook *actually* transitively requires (computed from
the real dependency graph, not approximated) — see
[`LEARNING_PATH.md`](LEARNING_PATH.md#-goal-oriented-learning-paths) for the exact notebook list
behind each one.

| Goal | Modules needed | Est. Time |
|---|---|---|
| **Understand transformers** (`12.01`) | `00`–`05` (52 notebooks) | ~10 weeks |
| **Fine-tune LLMs / LoRA** (`08.06`) | `00`–`03`, `05`–`08` (60 notebooks) | ~11.5 weeks |
| **Read ML papers fluently** (`12.05`) | `00`–`05`, `12` (56 notebooks) | ~11 weeks |
| **Generative models & diffusion** (`09.06`) | `00`, `03`, `09` (21 notebooks) | ~4 weeks |
| **NLP-adjacent discrete math** (`07.05`) | `00`, `07` (9 notebooks) | ~1.5 weeks |
| **DL theory & generalization** (`11.04`) | `00`–`03`, `05`–`09`, `11` (70 notebooks) | ~14 weeks |
| **Natural gradient / info geometry** (`10.03`) | `00`–`04`, `09`–`10` (53 notebooks) | ~10.5 weeks |
| **Full curriculum** | all 14 modules (104 notebooks) | ~18+ weeks |

<p align="center">
  <img src="_assets/images/fast_tracks.png" alt="Fast Track Paths" width="100%">
</p>

## 🤝 Contributing

Contributions are very welcome — whether that's fixing a typo in the theory, improving a
visualization, adding an exercise, fixing a notebook bug, or proposing a whole new topic.
[`CONTRIBUTING.md`](CONTRIBUTING.md) has **role-based on-ramps** for mathematicians, ML
researchers, educators, and software engineers, plus the notebook template, review criteria, and
workflow. New issues go through structured [templates](.github/ISSUE_TEMPLATE/) (mathematical
error, notebook bug, curriculum proposal); pull requests use the
[PR template](.github/PULL_REQUEST_TEMPLATE.md) and are reviewed against
[`docs/REVIEWER_CHECKLIST.md`](docs/REVIEWER_CHECKLIST.md). Please also read our
[Code of Conduct](CODE_OF_CONDUCT.md).

Every push and pull request runs a fast set of CI checks (code quality, the notebook test
harness's unit tests, the mathematical-regression suite, and a representative notebook from each
module), and a deeper nightly job executes every notebook across the full supported Python range.
The two-tier setup — what each job checks, how dependencies are cached, and how to reproduce every
check locally — is documented in [`docs/CI.md`](docs/CI.md).

## 📖 References

- Deisenroth, Faisal & Ong, *Mathematics for Machine Learning* ([free PDF](https://mml-book.github.io/))
- Goodfellow, Bengio & Courville, *Deep Learning* ([free online](https://www.deeplearningbook.org/))
- Bishop, *Pattern Recognition and Machine Learning*
- MacKay, *Information Theory, Inference, and Learning Algorithms* ([free PDF](https://www.inference.org.uk/mackay/itila/))
- Wasserman, *All of Statistics*

## 📄 License

Released under the [MIT License](LICENSE) — free to use, adapt, and share, including for
teaching. Security policy: [`SECURITY.md`](SECURITY.md).

---

## ⭐ Star & Share

If this curriculum helps you understand the mathematics behind modern AI, please **star the
repo** — it helps other learners find it — and share it with someone learning ML. Spotted a
mathematical error or a broken notebook? [Open an issue](.github/ISSUE_TEMPLATE/) or a PR;
corrections are some of the most valuable contributions.
