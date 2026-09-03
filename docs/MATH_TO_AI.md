# 🔗 Math → AI/ML/LLM Connections

Every notebook in this curriculum ends with a **"Why This Matters for AI"** section that ties its
mathematics to a concrete technique in real ML/LLM systems. This document collects those
connections into one map, so you can navigate *from a technique you care about* to the
mathematics behind it — or the reverse.

Notebook codes are `module.notebook` (e.g. `01.07` = Module 01, notebook 07). The connections
below reflect what the notebooks actually build; they are pointers, not a claim that a single
notebook fully implements a production system.

## By mathematical area

### Linear algebra (Modules 01, 08)

| Mathematics | AI/ML/LLM technique | Notebook(s) |
|---|---|---|
| Vectors, dot products, cosine similarity | Word/sentence embeddings, similarity search | `01.01` |
| Matrix multiplication | The core operation of every neural-network layer | `01.02`, `01.09` |
| Eigenvalues / eigenvectors | PCA, spectral methods, covariance structure | `01.06` |
| SVD & low-rank approximation | PCA, model compression, **LoRA / QLoRA** | `01.07`, `08.05`, `08.06` |
| Matrix decompositions (QR, Cholesky) | Numerically stable solves, sampling | `01.08` |
| Softmax + scaled dot-product | **Transformer attention** (`√dₖ` scaling) | `01.10`, `12.01` |
| Inner-product spaces / Gram matrices | Kernel methods | `08.01`, `11.02` |
| Random matrix theory | Weight initialization, spectra of deep nets | `08.04` |

### Calculus (Module 02)

| Mathematics | AI/ML/LLM technique | Notebook(s) |
|---|---|---|
| Derivatives & the chain rule | The mechanics of **backpropagation** | `02.02`, `02.04` |
| Partial derivatives & gradients | Gradient-based training | `02.03`, `02.05` |
| Jacobians & Hessians | Reverse-mode autodiff, curvature/second-order methods | `02.06` |
| The calculus of backprop | Hand-derived layer gradients vs. autograd | `02.10`, `12.02` |

### Probability & statistics (Modules 03, 09, 13)

| Mathematics | AI/ML/LLM technique | Notebook(s) |
|---|---|---|
| Distributions, expectation, variance | Modeling data and uncertainty | `03.02`, `03.03`, `03.06` |
| Bayes' theorem & inference | Bayesian models, posterior updates | `03.05` |
| Maximum likelihood / Fisher information | The estimation principle behind most training | `03.07` |
| Monte-Carlo & sampling | Stochastic estimation, evaluation | `03.09` |
| Concentration inequalities | Why finite samples generalize | `09.04` |
| Stochastic processes & SDEs | **Diffusion models** | `09.02`, `09.06` |
| ERM, VC dimension, Rademacher complexity | Generalization theory, why over-parameterized nets work | `13.01`–`13.09` |

### Optimization (Module 04)

| Mathematics | AI/ML/LLM technique | Notebook(s) |
|---|---|---|
| Gradient descent & variants | The base training loop (batch/mini-batch/SGD) | `04.02` |
| Convexity & convergence rates | Why (and how fast) training converges | `04.03` |
| Momentum, RMSProp, **Adam** | The optimizers that actually train modern nets | `04.04`, `12.03` |
| Learning-rate schedules | Warmup, cosine decay, one-cycle | `04.06` |
| Second-order / natural gradient | Newton, K-FAC, curvature-aware training | `04.07`, `10.03` |

### Information theory (Module 05)

| Mathematics | AI/ML/LLM technique | Notebook(s) |
|---|---|---|
| Entropy | Uncertainty, perplexity | `05.01`, `05.07` |
| KL divergence | VAEs, distillation, RLHF regularization | `05.02` |
| Cross-entropy | **The standard classification/LM training loss** | `05.03` |
| Mutual information | Representation learning, the information bottleneck | `05.04`, `05.05` |

### Numerical methods (Module 06)

| Mathematics | AI/ML/LLM technique | Notebook(s) |
|---|---|---|
| Floating point & numerical stability | `float32`/`bfloat16`, stable softmax/log-sum-exp | `06.01`, `06.02` |
| Numerical differentiation | Gradient checking | `06.03` |
| Mixed precision & quantization | Efficient training and inference | `06.06`, `06.08` |
| Transformer-specific numerics | Attention overflow, pre- vs post-norm | `06.07` |

### Discrete mathematics (Module 07)

| Mathematics | AI/ML/LLM technique | Notebook(s) |
|---|---|---|
| Combinatorics, graphs, trees | Tokenization, beam search, graph neural nets | `07.01`–`07.03` |
| Automata & formal languages | Grammars, constrained decoding | `07.04` |
| Edit distance, BLEU, ranking | NLP evaluation, RLHF preference data | `07.05` |

### Advanced / research foundations (Modules 10, 11)

| Mathematics | AI/ML/LLM technique | Notebook(s) |
|---|---|---|
| Information geometry / Fisher-Rao metric | Natural gradient descent | `10.02`, `10.03` |
| Lie groups & symmetries | Equivariant / geometric deep learning | `10.04` |
| Function spaces & norms | Universal approximation | `11.01` |
| RKHS / kernel methods | Kernel machines, Gaussian processes | `11.02` |
| Neural tangent kernel / infinite width | A theory of training dynamics | `11.03`, `11.04` |

## By technique (reverse lookup)

- **Transformer attention** → linear algebra (`01.10`), softmax Jacobian (`02.10`), attention
  numerics (`06.07`), full derivation (`12.01`).
- **LoRA / QLoRA fine-tuning** → SVD & low-rank structure (`01.07`, `08.05`), the LoRA notebook
  (`08.06`), quantization (`06.08`).
- **Backpropagation** → chain rule & computation graphs (`02.04`), calculus of backprop
  (`02.10`), a from-scratch build (`12.02`).
- **Diffusion models** → stochastic processes (`09.02`), the diffusion-process math (`09.06`).
- **Optimizers (Adam & co.)** → adaptive methods (`04.04`), a from-scratch Adam (`12.03`).
- **Why deep nets generalize** → concentration (`09.04`), statistical learning theory
  (`13.01`–`13.09`), the NTK (`11.03`, `11.04`).

For a full role-oriented route to any of these, see the [learning
tracks](../LEARNING_PATH.md#-learning-tracks-six-ways-through-the-curriculum) and the
goal-oriented [fast-track paths](../LEARNING_PATH.md#-goal-oriented-learning-paths).
