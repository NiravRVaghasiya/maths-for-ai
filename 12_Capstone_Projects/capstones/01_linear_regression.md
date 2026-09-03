# Capstone 1 — Linear Regression from Scratch

| | |
| :--- | :--- |
| **Difficulty** | ██░░░░░░░░ 2/10 |
| **Prerequisites** | `01.01`–`01.05`, `02.02`–`02.05`, `04.01`–`04.03` |
| **Estimated time** | ~4–6 hours |
| **Demonstrates** | Optimizing a convex quadratic two ways — the closed-form normal equations and iterative gradient descent — and showing they reach the same optimum |

---

## 1. Problem statement

Fit a linear model $\hat{y} = Xw$ to data by minimizing squared error, **two
independent ways** — solving the normal equations in closed form, and running
gradient descent — and demonstrate empirically that both converge to the same
weight vector. The question you are answering: *why does linear regression have a
closed-form solution at all, and what is gradient descent actually approximating
when it doesn't use one?*

## 2. Prerequisites

| Notebook | Result you must already command |
| --- | --- |
| `01.02`–`01.05` | Matrix multiplication, transpose, inverse, and solving $A\mathbf{x}=\mathbf{b}$ |
| `02.02`–`02.05` | Gradient of a scalar function of a vector; the gradient points uphill |
| `04.01`–`04.03` | Gradient descent as an iterative minimizer; what a convex function is and why it has a unique minimum |

If you cannot state the gradient of $f(w)=\tfrac12\|Xw-y\|^2$ without looking it
up after this capstone, revisit `02.05` and `04.02`.

## 3. Mathematical formulation

Given a design matrix $X\in\mathbb{R}^{n\times d}$ (n examples, d features, a
column of ones for the intercept) and targets $y\in\mathbb{R}^{n}$, the
ordinary-least-squares objective is

$$
\mathcal{L}(w) \;=\; \frac{1}{n}\,\|Xw - y\|_2^2
\;=\; \frac{1}{n}\,(Xw-y)^\top(Xw-y),\qquad w\in\mathbb{R}^d .
$$

Two facts you will establish:

- **Gradient.** $\displaystyle \nabla_w\mathcal{L}(w) = \frac{2}{n}\,X^\top(Xw-y).$
- **Normal equations.** Setting the gradient to zero gives
  $X^\top X\,w^\star = X^\top y$, so when $X^\top X$ is invertible,
  $w^\star = (X^\top X)^{-1}X^\top y.$
- **Convexity.** The Hessian is $\nabla^2\mathcal{L} = \tfrac{2}{n}X^\top X$, which
  is positive semidefinite for any $X$; hence $\mathcal{L}$ is convex and any
  stationary point is a global minimum. This is *why* the single stationary point
  the normal equations find is the answer, and why gradient descent cannot get
  stuck anywhere else.

## 4. Derivation requirements

Derive each of these yourself, showing the steps (not just the result):

1. **The gradient** $\nabla_w\mathcal{L}$, starting from the scalar sum
   $\frac1n\sum_i (x_i^\top w - y_i)^2$ and using the chain rule — then re-derive
   it in matrix form and confirm the two agree.
2. **The normal equations**, by setting your gradient to zero. State explicitly
   the condition under which $(X^\top X)^{-1}$ exists (full column rank), and what
   goes wrong otherwise.
3. **The Hessian**, and a one-line argument that $X^\top X \succeq 0$ (hint:
   $v^\top X^\top X v = \|Xv\|^2$). Conclude convexity.
4. **The gradient-descent convergence condition** for a step size $\eta$ on this
   quadratic: show that the error contracts when $0<\eta<2/\lambda_{\max}(\tfrac2n
   X^\top X)$, and identify the optimal fixed step. (Connect to `04.03`.)

## 5. Implementation

Build, from scratch (NumPy only for the core; see the oracle rule):

- `normal_equation(X, y) -> w` — solve $X^\top X w = X^\top y$. Use a linear
  solver, **not** an explicit inverse, and justify why in your write-up.
- `mse(X, y, w) -> float` and `mse_grad(X, y, w) -> np.ndarray` — the objective
  and your derived gradient.
- `gradient_descent(X, y, lr, n_steps, w0=None) -> (w, history)` — iterative
  minimization returning the final weights and the loss trajectory.

**Oracle rule.** You may use `numpy.linalg.solve` inside `normal_equation` (it is
a linear-system solver, not a regression routine). You must **not** call
`sklearn.linear_model.LinearRegression` or `numpy.polyfit` inside your
implementation — those *are* the thing under test. They appear only in the
Experiments section, as an external oracle to check your answer against.

## 6. Experiments

1. **Closed form vs. gradient descent.** On a synthetic dataset with known true
   weights plus noise, run both methods and report $\|w_{\text{GD}} -
   w_{\text{normal}}\|$ as a function of gradient-descent steps. It should decay
   to round-off.
2. **Against the oracle.** Compare `normal_equation` to
   `sklearn.linear_model.LinearRegression` (fit intercept consistently). Report
   the max absolute coefficient difference.
3. **Gradient check.** Compare `mse_grad` to a central finite-difference gradient
   at several random $w$. (This is the derivation-independence check.)
4. **Step-size sweep.** Run gradient descent at several $\eta$ spanning below,
   near, and above your derived stability threshold $2/\lambda_{\max}$. Show
   convergence, fast convergence, and divergence respectively.
5. **Conditioning.** Increase feature correlation (raise $\kappa(X^\top X)$) and
   show gradient descent slows while the normal equation stays accurate until
   $X^\top X$ becomes near-singular.

## 7. Expected outputs

- A table: `normal_equation` vs `sklearn` coefficients — max difference
  $< 10^{-8}$.
- A convergence plot of $\|w_{\text{GD}}-w^\star\|$ vs. step, on a log axis,
  reaching $\sim 10^{-6}$ or below at a well-chosen $\eta$.
- Gradient-check: max relative error between analytic and finite-difference
  gradient $< 10^{-6}$.
- A step-size figure with three regimes visibly distinct (converge / fast /
  diverge), with the empirical divergence onset near your derived
  $2/\lambda_{\max}$.
- A conditioning plot: gradient-descent steps-to-tolerance rising with
  $\kappa(X^\top X)$.

## 8. Evaluation criteria

Weighting for this capstone (correctness-heavy, as an entry rung):

| Axis | Weight | "Meets expectations" bar |
| --- | --- | --- |
| Mathematical correctness | 35% | Gradient, normal equations, Hessian/convexity all derived correctly and in consistent notation |
| Derivation independence | 20% | Gradient check passes; implementation follows the derived gradient, not a library |
| Implementation fidelity | 20% | Both methods match the oracle to $<10^{-8}$; solver used instead of explicit inverse |
| Experimental rigor | 15% | Step-size regimes and conditioning experiments seeded and correctly interpreted |
| Communication | 10% | Write-up follows problem → math → evidence, claims tied to specific plots |

Automatic fail if `sklearn`/`polyfit` is used *inside* the estimator, or if the
step-size threshold is asserted without derivation.

## 9. Extensions

- **Ridge regression.** Add an $\ell_2$ penalty $\lambda\|w\|^2$; re-derive the
  normal equations to $(X^\top X+\lambda I)w=X^\top y$ and explain geometrically
  why this fixes near-singular $X^\top X$.
- **Weighted least squares.** Introduce per-example weights and re-derive.
- **Stochastic gradient descent.** Implement minibatch SGD; compare its noisy
  trajectory to full-batch and relate the noise scale to batch size.
- **Numerical stability.** Solve via the QR or Cholesky factorization of $X$
  instead of the normal equations and explain why that is better conditioned
  (connect to `06.04`, `08`).

## 10. Research directions

- **Implicit regularization of gradient descent.** On over-parameterized problems
  ($d>n$), gradient descent from zero converges to the *minimum-norm* solution.
  Verify this empirically and connect it to why over-parameterized neural nets
  generalize (`13` Statistical Learning Theory).
- **The double-descent risk curve.** As $d/n$ crosses 1, test error can rise then
  fall again — the same linear model, a genuinely surprising phenomenon
  (`13.08`).
- **Conditioning and optimization.** How the spectrum of $X^\top X$ controls
  first-order convergence is the seed of the entire study of preconditioning and
  second-order methods (`04.07`, `06.04`).
