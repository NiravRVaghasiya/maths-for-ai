# Mathematical Regression-Testing Framework

`tools/math_regression` is a pytest suite that guards the *mathematics* the
curriculum teaches. It answers a different question from the notebook audit
(`docs/NOTEBOOK_AUDIT.md`): the audit asks "does every notebook still run?"; this
asks "are the mathematical identities the notebooks demonstrate actually true, to
a justified numerical tolerance?"

It runs in the **fast CI tier** (`ci.yml`, the `math-regression` job) because it
is pure math — no notebook execution, no Jupyter kernel — and finishes in a few
seconds.

## What it covers

| Area | Identities tested | File |
|---|---|---|
| Linear algebra | matmul definition; `A A⁻¹ = I`; `solve` consistency; `det(AB)=det(A)det(B)`, triangular/eigenvalue determinant; QR (orthonormal `Q`, `QR=A`); Cholesky `LLᵀ=A`; `Av=λv`, trace=Σλ, det=Πλ, symmetric ⇒ real spectrum; SVD reconstruction, `σᵢ=√λᵢ(AᵀA)`, Eckart–Young low-rank optimality | `test_linear_algebra.py` |
| Calculus | gradient (analytic vs finite-difference vs `torch.autograd`); Hessian symmetry + FD + autograd; Jacobian chain rule `J_{g∘f}=J_g·J_f`; directional derivative `∇f·û`; Taylor remainder order; softmax Jacobian `diag(s)−ssᵀ` | `test_calculus.py` |
| Probability & statistics | mean/variance of Bernoulli, Binomial, Poisson, Exponential, Beta, Normal (analytic vs `scipy.stats` vs Monte-Carlo); Binomial→Poisson limit; Bayes normalization; Beta–Bernoulli conjugacy; Gaussian MLE vs numerical argmax; Cramér–Rao `Var≈σ²/n`; linearity of expectation; `Var=E[X²]−E[X]²` | `test_probability.py` |
| Optimization | linear-regression gradient (analytic vs FD vs vanishing at the OLS optimum); logistic gradient + PSD Hessian (convexity); GD convergence to `A⁻¹b`; Adam/Momentum update equations vs their definition and fixed points; LR-schedule formulas | `test_optimization.py` |
| Numerical methods | forward `O(h)` vs central `O(h²)` finite-difference *order*; stable softmax / logsumexp vs `scipy.special` + overflow survival; conjugate gradient (`≤n` steps, matches `np.linalg.solve`); IEEE-754 float32 reconstruction; natural cubic spline interpolation + `C²` continuity | `test_numerical_methods.py` |

## The core principle: triangulate, don't reproduce

The curriculum notebooks already end most sections with a self-check like
`np.allclose(my_scratch_fn(A), np.linalg.svd(A))`. **Copying that assertion into
a test would be worthless** — it only proves "the code equals itself," and it
would pass even if both the scratch code and the notebook's own check were wrong
in the same way. This framework deliberately does *not* import or re-run notebook
code. Instead every identity is verified by an **independent triangulation** of
up to three sources that can only agree if the mathematics is correct:

- **Analytical** — a closed form derived by hand (e.g. `Var[Binomial]=np(1−p)`,
  the softmax Jacobian `diag(s)−ssᵀ`, the logistic Hessian `Xᵀ diag(p(1−p)) X`).
- **Numerical** — an independent approximation that shares no code with the
  analytic form: finite differences (`oracles.py`), Monte-Carlo sampling, a grid
  or `scipy.optimize` argmax, numeric integration for a posterior.
- **Library** — a trusted third-party oracle whose implementation is entirely
  separate from ours: `numpy.linalg`, `scipy.stats`, `scipy.special`,
  `scipy.optimize`, `torch.autograd`.

Where a relationship is purely structural (`det(AB)=det(A)det(B)`,
`σᵢ=√λᵢ(AᵀA)`, `Var=E[X²]−E[X]²`) we assert the *relationship itself*, which holds
no matter which implementation produced the numbers — again avoiding any
dependence on one specific piece of code being correct.

This design is what makes the suite a real regression guard: a
[mutation check](#does-it-actually-catch-errors) confirms that deliberately wrong
identities are rejected.

## Justified tolerances

Every tolerance lives in `tolerances.py` with the error model that justifies it.
A tolerance here is a *claim about the dominant error source*, not a number tuned
until the test goes green. There are three regimes:

1. **Exact algebra (round-off only).** Operations like `A A⁻¹ = I` are
   mathematically exact; the only error is float64 round-off (`eps ≈ 2.2e-16`).
   For the well-conditioned, modest-size matrices used here, accumulated
   round-off `n·κ·eps` stays well under `ATOL_EXACT = RTOL_EXACT = 1e-9` — still
   ~6 orders of magnitude tighter than a finite-difference bound, so it would
   still flag a genuinely wrong result.

2. **Finite-difference approximation.** A central difference has truncation error
   `O(h²)` but round-off `∝ eps/h`; the total is minimized near
   `h* ≈ eps^(1/3) ≈ 6e-6`. We use `h = 1e-5` with `ATOL_FD = 1e-6`,
   `RTOL_FD = 1e-5`; Hessians (a finite difference *of* a finite difference) use
   the looser `1e-3`. The error-*order* tests don't use these closeness bounds at
   all — they assert the observed convergence *slope* on a log-log `h`-sweep
   (`≈1` forward, `≈2` central), a stronger, constant-free statement.

3. **Monte-Carlo estimation.** An `N`-sample empirical mean has standard error
   `σ/√N`. Tolerances are sized at **6 standard errors** (`mc_atol`,
   `mc_atol_variance`), which makes a spurious failure of a *correct* estimator
   astronomically unlikely (`P ≈ 2e-9` for a Gaussian) while staying far tighter
   than the gap a *wrong* formula would produce. `N = 200_000` and the RNG is
   seeded, so results are deterministic.

## Running it

```bash
pip install -r requirements.txt      # numpy / scipy / torch (the oracles)
pip install -r requirements-dev.txt  # pytest
PYTHONPATH=tools pytest tools/math_regression/tests/ -v
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "tools"
.\.venv\Scripts\python.exe -m pytest tools/math_regression/tests/ -v
```

The whole suite runs in a few seconds. Randomized tests are parametrized over a
fixed pool of seeds (`conftest.py`), so a bug that only shows on some matrices is
still likely to be caught, without any run-to-run flakiness.

## Does it actually catch errors?

Yes — and that's worth re-verifying whenever you touch the tolerances. A quick
mutation check (introduce a wrong identity and confirm the corresponding test
fails) is the fastest way to prove the tolerances aren't so loose they pass
anything. For example, each of these *should* be rejected:

- softmax Jacobian with a sign flip: `diag(s) + ssᵀ` instead of `diag(s) − ssᵀ`;
- an SVD "reconstruction" that drops a singular value (rank-deficient);
- a Poisson variance formula of `λ/2` instead of `λ`.

All three fall outside the justified tolerances and fail, confirming the suite
discriminates correct math from incorrect.

## Adding a new identity

1. Put shared numerical machinery (a new kind of oracle) in `oracles.py`, and any
   new tolerance in `tolerances.py` **with its error-model justification** — never
   inline a bare magic number in an assertion.
2. Add the test to the matching `test_<area>.py`. Verify the identity against at
   least two *independent* sources (analytical + numerical, or + library). If you
   find yourself importing notebook code or re-asserting a notebook's own
   `np.allclose`, stop — that's the tautology this framework exists to avoid.
3. Pick the tolerance regime that matches the error source (exact / finite-diff /
   Monte-Carlo) and use the corresponding constant from `tolerances.py`.
4. Run the suite; if a correct identity needs a looser tolerance than its error
   model predicts, investigate why rather than widening the bound.

## Relationship to the notebook audit

These are complementary, non-overlapping checks:

- **`tools/notebook_audit`** executes notebooks and reports *whether they run*
  (and, optionally, whether they're deterministic). It cannot judge whether the
  math is correct.
- **`tools/math_regression`** never runs a notebook; it checks *whether the
  mathematics is correct*, independent of the notebook implementations.

Both run in the fast CI tier on every push/PR (see `docs/CI.md`).
