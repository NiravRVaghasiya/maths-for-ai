# Capstone 3 — PCA / SVD Representation Analysis

| | |
| :--- | :--- |
| **Difficulty** | █████░░░░░ 5/10 |
| **Prerequisites** | Capstone 1, `01.06`, `01.07`, `03.03`, `03.04`, `08.05` (optional) |
| **Estimated time** | ~8–12 hours |
| **Demonstrates** | Eigendecomposition and SVD as the *same* underlying object, used to discover and analyze the structure a representation encodes |

---

## 1. Problem statement

Implement Principal Component Analysis **two independent ways** — as the
eigendecomposition of the covariance matrix, and as the SVD of the centered data
— prove the two are the same computation, and use PCA to *analyze a learned
representation*: take the hidden activations of the network you trained in
Capstone 2 (or a pretrained embedding), and quantify how much structure lives in
how few directions. The question you are answering: *what does it mean for a
representation to be "low-dimensional," and how do the spectral tools measure it?*

## 2. Prerequisites

| Notebook | Result you must already command |
| --- | --- |
| `01.06` | Eigenvalues/eigenvectors; symmetric matrices have real eigenvalues and orthogonal eigenvectors |
| `01.07` | SVD $A = U\Sigma V^\top$; PCA via SVD; explained variance |
| `03.03`, `03.04` | Covariance as a matrix; variance along a direction |
| `08.05` (optional) | Eckart–Young low-rank optimality |
| Capstone 2 (optional) | A trained network whose activations you can analyze |

## 3. Mathematical formulation

Let $X\in\mathbb{R}^{n\times d}$ be data with the column mean removed
(centered), $\tilde{X} = X - \mathbf{1}\bar{x}^\top$. Define the (biased) sample
covariance $C = \tfrac1n \tilde{X}^\top \tilde{X}\in\mathbb{R}^{d\times d}$.

- **PCA via eigendecomposition.** The principal directions are the eigenvectors
  of $C$, ordered by eigenvalue: $C = V\Lambda V^\top$, with $\lambda_1\geq\dots\geq
  \lambda_d\geq 0$. The variance captured by direction $v_k$ is $\lambda_k$.
- **PCA via SVD.** With $\tilde{X} = U\Sigma V^\top$, the right singular vectors
  $V$ are exactly the eigenvectors of $C$, and $\lambda_k = \sigma_k^2/n$.
- **The equivalence.** $C = \tfrac1n\tilde{X}^\top\tilde{X} =
  \tfrac1n V\Sigma^\top U^\top U\Sigma V^\top = V\big(\tfrac1n\Sigma^2\big)V^\top$,
  i.e. the SVD *is* the covariance eigendecomposition, with $\lambda_k =
  \sigma_k^2/n$.
- **Explained variance ratio.** $r_k = \lambda_k / \sum_j \lambda_j$; the top-$k$
  projection $\tilde{X}V_{:k}$ captures $\sum_{j\le k} r_j$ of the total variance,
  and by **Eckart–Young** it is the *best possible* rank-$k$ linear reconstruction
  in Frobenius norm.

## 4. Derivation requirements

Derive each yourself:

1. **PCA as variance maximization.** Show that the first principal direction
   solves $\max_{\|v\|=1} \operatorname{Var}(\tilde{X}v) = \max_{\|v\|=1} v^\top C
   v$, and that the maximizer is the top eigenvector of $C$ with value
   $\lambda_1$ (Rayleigh quotient / Lagrange multiplier argument).
2. **The SVD ↔ covariance equivalence**, the algebra above, including the
   $\lambda_k = \sigma_k^2/n$ scaling and why the sign/ordering conventions matter.
3. **Eckart–Young for PCA:** the rank-$k$ truncation minimizes reconstruction
   error, and the residual equals $\sqrt{\sum_{j>k}\sigma_j^2}$ (you may cite the
   general theorem from `08.05`, but state precisely how it specializes to
   centered data / reconstruction).
4. **Why center first.** Show what the top singular vector of the *un*-centered
   data captures instead (roughly the mean direction), and why that is usually not
   what you want.

## 5. Implementation

NumPy only for the core:

- `pca_eig(X, k) -> (components, explained_variance)` — center, form $C$,
  eigendecompose with `numpy.linalg.eigh`, sort descending.
- `pca_svd(X, k) -> (components, explained_variance)` — center, `numpy.linalg.svd`
  of $\tilde{X}$, convert singular values to variances.
- `project(X, components) -> Z` and `reconstruct(Z, components, mean) -> X_hat`.
- `explained_variance_ratio(X) -> np.ndarray`.

**Oracle rule.** `numpy.linalg.eigh`/`svd` are the linear-algebra primitives you
*are* allowed to build on (they are not "PCA"). `sklearn.decomposition.PCA`
appears only in Experiments as the external oracle. Do not call it inside your
functions.

## 6. Experiments

1. **Two roads, one answer.** On the same data, confirm `pca_eig` and `pca_svd`
   produce the same components (up to sign) and identical explained-variance
   ratios.
2. **Against the oracle.** Compare your explained-variance ratios and projections
   to `sklearn.decomposition.PCA`.
3. **Reconstruction / Eckart–Young.** Sweep $k$ and plot reconstruction error;
   overlay the predicted residual $\sqrt{\sum_{j>k}\sigma_j^2}$ — they must
   coincide. Confirm no random rank-$k$ projection beats PCA's error.
4. **Representation analysis (the point).** Take hidden activations from your
   Capstone-2 network (or a pretrained word/image embedding). Report the
   explained-variance curve and the *effective dimensionality* (e.g. participation
   ratio $(\sum\lambda)^2/\sum\lambda^2$, or the $k$ for 90% variance). Visualize a
   2-D PCA projection colored by class and comment on what structure appears.
5. **Whitening / anisotropy.** Measure how anisotropic the representation is
   (ratio $\lambda_1/\lambda_d$ or the spectrum shape) and relate it to known
   "representation collapse" / anisotropy observations in embeddings.

## 7. Expected outputs

- `pca_eig` vs `pca_svd`: components agree up to sign; explained-variance ratios
  match to $< 10^{-10}$.
- Your PCA vs `sklearn`: explained-variance-ratio max difference $< 10^{-8}$.
- Reconstruction-error curve exactly tracking $\sqrt{\sum_{j>k}\sigma_j^2}$; random
  rank-$k$ competitors never below it.
- A representation report: explained-variance curve, an effective-dimensionality
  number, and a labeled 2-D projection with a one-paragraph interpretation.
- An anisotropy measurement with interpretation.

## 8. Evaluation criteria

| Axis | Weight | "Meets expectations" bar |
| --- | --- | --- |
| Mathematical correctness | 30% | Variance-maximization, SVD↔covariance equivalence, and Eckart–Young specialization derived correctly |
| Derivation independence | 20% | Two implementations agree; both match `sklearn`; reconstruction matches the predicted residual |
| Implementation fidelity | 20% | Centering handled correctly; components/variances correct up to sign convention |
| Experimental rigor | 20% | Representation analysis is quantitative (effective dim, anisotropy), not just a pretty scatter plot |
| Communication | 10% | The write-up explains *what the spectrum means* for the representation |

Automatic fail if `sklearn.decomposition.PCA` is used inside the estimator, or if
centering is omitted without justification.

## 9. Extensions

- **Kernel PCA.** Perform PCA in a feature space via the kernel trick; connect to
  `11.02` (RKHS) and show it captures nonlinear structure a linear PCA misses.
- **Probabilistic PCA / factor analysis.** Derive PCA as the MLE of a Gaussian
  latent-variable model (connect to `03.07`, `09`).
- **Randomized SVD.** Implement a randomized low-rank SVD and compare accuracy/speed
  to the full SVD on a large activation matrix (connect to `08.04`).
- **Incremental / streaming PCA.** Update the components as data arrives without
  re-forming the full covariance.

## 10. Research directions

- **Intrinsic dimensionality of neural representations.** How the effective
  dimensionality of hidden layers evolves during training and across depth — an
  active area linking generalization to representation geometry.
- **Anisotropy in language-model embeddings.** Contextual embeddings occupy a
  narrow cone; measuring and correcting this (whitening, isotropy) is a real
  research thread.
- **Spectral bias.** Networks tend to learn low-frequency / high-variance
  structure first; the PCA spectrum of activations is one lens on this (`11.03`
  NTK, `13`).
- **Low-rank adaptation.** The empirical low-rank structure of weight *updates* is
  exactly what makes LoRA work (`08.06`) — analyze the rank of a fine-tuning
  update.
