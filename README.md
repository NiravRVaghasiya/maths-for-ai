<p align="center">
  <img src="_assets/images/readme_banner.png" alt="Math for AI/ML/LLMs" width="100%">
</p>

# 🧮 Math for AI/ML/LLMs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NiravRVaghasiya/maths-for-ai/blob/main/00_Prerequisites/01_mathematical_notation.ipynb)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Notebooks](https://img.shields.io/badge/notebooks-89-orange.svg)](#-complete-module-list)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/NiravRVaghasiya/maths-for-ai?style=social)](https://github.com/NiravRVaghasiya/maths-for-ai)
[![GitHub forks](https://img.shields.io/github/forks/NiravRVaghasiya/maths-for-ai?style=social)](https://github.com/NiravRVaghasiya/maths-for-ai/fork)
[![Last Commit](https://img.shields.io/github/last-commit/NiravRVaghasiya/maths-for-ai)](https://github.com/NiravRVaghasiya/maths-for-ai)

> Every piece of mathematics you need to understand, build, and research AI/ML/LLM systems —
> from high school algebra to cutting-edge theory. 89 Jupyter notebooks, 13 modules, all
> Google Colab compatible.

Every notebook pairs a mathematical idea with a plot, a from-scratch NumPy/PyTorch
implementation, and a direct connection to how that idea shows up inside real ML/LLM systems —
from word embeddings and attention to LoRA and diffusion models.

---

## 🎯 Who Is This For?

| If you are... | Start here | Time commitment |
|---|---|---|
| ML beginner with high-school algebra | [`00_Prerequisites`](00_Prerequisites/) | ~80 hrs (Core tier) |
| Data scientist wanting to go deeper | [`04_Optimization`](04_Optimization/) | ~45 hrs (Intermediate tier) |
| Researcher / PhD student | [`09_Advanced_Probability`](09_Advanced_Probability/) | ~55 hrs (Advanced tier) |
| Engineer fine-tuning LLMs | Fast Track: LoRA (see below) | ~35 hrs |

## 🏗️ How Each Notebook Works

Every notebook in this repository follows the same six-part structure:

1. **🎯 Learning Objective** — what you'll understand by the end, plus a difficulty rating,
   prerequisites, and estimated time
2. **📐 Theory** — a clear mathematical explanation with properly rendered LaTeX
3. **👁️ Visual Intuition** — a plot or diagram that builds geometric intuition before the code
4. **🐍 Implementation from Scratch** — a pure NumPy/PyTorch implementation of the concept
5. **🤖 Why This Matters for AI** — a direct, working-code connection to real ML/LLM systems
6. **🏋️ Exercises** — three difficulty levels: warm-up, practice, and an ML-connected challenge

<p align="center">
  <img src="_assets/images/notebook_structure.png" alt="Notebook Structure" width="100%">
</p>

## 🗺️ Visual Learning Path

![Math for AI learning path](_assets/images/learning-path.png)

See [`LEARNING_PATH.md`](LEARNING_PATH.md) for the full flowchart, module dependencies, and
fast-track routes.

## 📚 Complete Module List

### 🟢 CORE TIER — essential for any ML practitioner

| # | Module | Notebooks | Est. Hours |
|---|---|---|---|
| 00 | [Prerequisites & Notation](00_Prerequisites/) | 4 | 6 |
| 01 | [Linear Algebra](01_Linear_Algebra/) | 10 | 20 |
| 02 | [Calculus](02_Calculus/) | 10 | 18 |
| 03 | [Probability & Statistics](03_Probability_and_Statistics/) | 11 | 22 |
| 04 | [Optimization](04_Optimization/) | 9 | 16 |

### 🟡 INTERMEDIATE TIER — required for deep learning & NLP

| # | Module | Notebooks | Est. Hours |
|---|---|---|---|
| 05 | [Information Theory](05_Information_Theory/) | 7 | 12 |
| 06 | [Numerical Methods](06_Numerical_Methods/) | 7 | 10 |
| 07 | [Discrete Mathematics](07_Discrete_Mathematics/) | 5 | 8 |
| 08 | [Advanced Linear Algebra](08_Advanced_Linear_Algebra/) | 6 | 14 |

### 🔴 ADVANCED TIER — required for LLM research & paper comprehension

| # | Module | Notebooks | Est. Hours |
|---|---|---|---|
| 09 | [Advanced Probability](09_Advanced_Probability/) | 6 | 16 |
| 10 | [Differential Geometry & Topology](10_Differential_Geometry_and_Topology/) | 5 | 14 |
| 11 | [Functional Analysis](11_Functional_Analysis/) | 4 | 12 |
| 12 | [Capstone Projects](12_Capstone_Projects/) | 5 | 15 |

**Total: 89 notebooks | ~183 hours of content***

> *\*Hours include notebook reading time (~104 hrs) plus exercises, self-study, and
> re-derivation practice. The `~X min` in each notebook header reflects reading time only.*

<p align="center">
  <img src="_assets/images/curriculum_overview.png" alt="Curriculum Overview" width="100%">
</p>

> **Content status:** All 89 notebooks across all 13 modules have complete, publication-quality
> content — theory, visualizations, from-scratch implementations, AI/ML connections, and
> exercises. See [`CONTRIBUTING.md`](CONTRIBUTING.md) if you'd like to improve or extend it.

## 🚀 Quick Start

```bash
git clone https://github.com/NiravRVaghasiya/maths-for-ai.git
cd maths-for-ai
pip install -r requirements.txt
jupyter lab
```

Or click the "Open in Colab" badge at the top of any notebook to run it in the cloud with zero
setup.

## 🏎️ Fast Track Paths

Don't need the full 22-week curriculum? Pick a goal-oriented shortcut:

| Goal | Path | Est. Time |
|---|---|---|
| **Understand transformers** | `00` → `01` → `02` (chain rule) → `03` (softmax) → `04` (Adam) → `12.01` | ~4 weeks |
| **Read ML papers** | `00` → `01` → `02` → `03` → `05` (KL, entropy) → `12.05` | ~6 weeks |
| **Fine-tune LLMs** | `00` → `01` (SVD) → `02` (chain rule) → `04` (Adam) → `08` (LoRA) | ~5 weeks |
| **Full LLM research track** | `00` → `01` → `02` → `03` → `04` → `05` → `06` → `07` → `08` → `09` → `10` → `11` → `12` | ~22 weeks |

<p align="center">
  <img src="_assets/images/fast_tracks.png" alt="Fast Track Paths" width="100%">
</p>

## 🤝 Contributing

Contributions are very welcome — whether that's filling in a skeleton notebook, fixing a typo
in the theory, improving a visualization, or proposing a whole new topic. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the notebook template, review criteria, and workflow.

## 📖 References

- Deisenroth, Faisal & Ong, *Mathematics for Machine Learning* ([free PDF](https://mml-book.github.io/))
- Goodfellow, Bengio & Courville, *Deep Learning* ([free online](https://www.deeplearningbook.org/))
- Bishop, *Pattern Recognition and Machine Learning*
- MacKay, *Information Theory, Inference, and Learning Algorithms* ([free PDF](https://www.inference.org.uk/mackay/itila/))
- Wasserman, *All of Statistics*

## 📄 License

Released under the [MIT License](LICENSE).
