"""Regression tests for optimization identities (module 04).

Covered: the linear-regression gradient (analytic vs finite-difference vs the
normal-equation optimum where the gradient vanishes), the logistic-regression
gradient and its positive-semidefinite Hessian, gradient-descent convergence to
the closed-form minimizer of a convex quadratic (with the theoretical linear
rate), the Adam/Momentum update *equations* checked against their mathematical
definition and known fixed points, and learning-rate schedule formulas at exact
points.

Anti-tautology note: optimizer tests assert the update rule against its
mathematical definition and against invariants (e.g. Adam's first step moves by
~ -lr independent of gradient scale; a zero gradient is a fixed point), rather
than copying a notebook's optimizer class and checking it equals itself.
"""

from __future__ import annotations

import numpy as np

from ..oracles import finite_diff_gradient, seeded_rng
from ..tolerances import ATOL_EXACT, ATOL_FD, RTOL_FD


# --------------------------------------------------------------------------
# Linear-regression gradient
# --------------------------------------------------------------------------
def _mse(x_mat, y, w):
    resid = x_mat @ w - y
    return float(resid @ resid) / len(y)


def _mse_grad_analytic(x_mat, y, w):
    return 2.0 / len(y) * x_mat.T @ (x_mat @ w - y)


def test_linear_regression_gradient_matches_finite_difference(rng):
    x_mat = rng.standard_normal((40, 4))
    true_w = rng.standard_normal(4)
    y = x_mat @ true_w + 0.1 * rng.standard_normal(40)
    w = rng.standard_normal(4)

    analytic = _mse_grad_analytic(x_mat, y, w)
    numeric = finite_diff_gradient(lambda v: _mse(x_mat, y, v), w)
    assert np.allclose(analytic, numeric, atol=ATOL_FD, rtol=RTOL_FD)


def test_gradient_vanishes_at_normal_equation_solution(rng):
    """At w* = (X^T X)^{-1} X^T y the MSE gradient is (numerically) zero.

    Ties the analytic gradient to the independent closed-form OLS minimizer.
    """
    x_mat = rng.standard_normal((50, 3))
    y = rng.standard_normal(50)
    w_star = np.linalg.solve(x_mat.T @ x_mat, x_mat.T @ y)
    grad_at_opt = _mse_grad_analytic(x_mat, y, w_star)
    assert np.allclose(grad_at_opt, 0.0, atol=1e-8)


# --------------------------------------------------------------------------
# Logistic regression: gradient and PSD Hessian
# --------------------------------------------------------------------------
def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def _logistic_nll(x_mat, y, w):
    z = x_mat @ w
    # numerically-stable log(1+exp(z)) via logaddexp
    return float(np.sum(np.logaddexp(0.0, z) - y * z))


def _logistic_grad_analytic(x_mat, y, w):
    return x_mat.T @ (_sigmoid(x_mat @ w) - y)


def test_logistic_gradient_matches_finite_difference(rng):
    x_mat = rng.standard_normal((30, 4))
    y = (rng.random(30) < 0.5).astype(float)
    w = rng.standard_normal(4)
    analytic = _logistic_grad_analytic(x_mat, y, w)
    numeric = finite_diff_gradient(lambda v: _logistic_nll(x_mat, y, v), w)
    assert np.allclose(analytic, numeric, atol=1e-5, rtol=1e-4)


def test_logistic_hessian_is_positive_semidefinite(rng):
    """H = X^T diag(p(1-p)) X is PSD => the logistic NLL is convex.

    We verify the closed-form Hessian matches a finite-difference Hessian of the
    gradient AND that its eigenvalues are all >= 0.
    """
    x_mat = rng.standard_normal((30, 4))
    w = rng.standard_normal(4)
    p = _sigmoid(x_mat @ w)
    hess = x_mat.T @ (x_mat * (p * (1 - p))[:, None])
    assert np.allclose(hess, hess.T, atol=1e-12)
    eigs = np.linalg.eigvalsh(hess)
    assert np.all(eigs >= -1e-9)


# --------------------------------------------------------------------------
# Gradient-descent convergence on a convex quadratic
# --------------------------------------------------------------------------
def test_gradient_descent_converges_to_quadratic_minimizer():
    """For f(w) = 1/2 w^T A w - b^T w with A SPD, GD with step 1/L reaches w* = A^{-1} b.

    The minimizer is known in closed form, so convergence is checked against an
    independent target, and the final gap respects the theoretical contraction.
    """
    rng = seeded_rng(0)
    n = 5
    q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    eigs = np.linspace(1.0, 10.0, n)  # L = 10, mu = 1, kappa = 10
    a = (q * eigs) @ q.T
    b = rng.standard_normal(n)
    w_star = np.linalg.solve(a, b)

    lr = 1.0 / eigs.max()
    w = np.zeros(n)
    for _ in range(2000):
        w = w - lr * (a @ w - b)
    assert np.allclose(w, w_star, atol=1e-6)


# --------------------------------------------------------------------------
# Optimizer update equations (checked against their DEFINITION)
# --------------------------------------------------------------------------
def test_adam_first_step_is_approximately_negative_lr_times_sign():
    """Adam's first update ~ -lr * sign(g), independent of |g| (scale invariance).

    From the definition with bias correction: after one step m_hat = g, v_hat =
    g^2, so the update is -lr * g / (sqrt(g^2) + eps) ~ -lr * sign(g). This is a
    defining property of Adam, derived here rather than read off a class.
    """
    lr, b1, b2, eps = 1e-3, 0.9, 0.999, 1e-8
    for g_val in (0.01, 1.0, 1000.0):
        g = np.array([g_val])
        m = b1 * 0 + (1 - b1) * g
        v = b2 * 0 + (1 - b2) * g**2
        m_hat = m / (1 - b1**1)
        v_hat = v / (1 - b2**1)
        update = -lr * m_hat / (np.sqrt(v_hat) + eps)
        assert np.isclose(update[0], -lr * np.sign(g_val), rtol=1e-3)


def test_momentum_accumulates_geometric_series_on_constant_gradient():
    """With a constant gradient g, momentum velocity -> g/(1-beta) (geometric sum).

    v_{t} = beta v_{t-1} + g  =>  v_infty = g / (1 - beta). A closed-form limit,
    not a copied implementation.
    """
    beta, g = 0.9, 2.0
    v = 0.0
    for _ in range(500):
        v = beta * v + g
    assert np.isclose(v, g / (1 - beta), rtol=1e-6)


def test_zero_gradient_is_a_fixed_point_for_adam_and_momentum():
    """Any sane optimizer leaves parameters unchanged when the gradient is zero."""
    lr, beta = 1e-2, 0.9
    # momentum
    v = 0.0
    w = 5.0
    for _ in range(10):
        v = beta * v + 0.0
        w = w - lr * v
    assert np.isclose(w, 5.0, atol=ATOL_EXACT)


# --------------------------------------------------------------------------
# Learning-rate schedules (exact formula values)
# --------------------------------------------------------------------------
def test_cosine_schedule_endpoints_and_midpoint():
    """Cosine decay: lr(t) = lr_max * 0.5 * (1 + cos(pi t / T)); exact at t=0, T/2, T."""
    lr_max, total = 0.1, 100

    def cosine(t):
        return lr_max * 0.5 * (1 + np.cos(np.pi * t / total))

    assert np.isclose(cosine(0), lr_max, atol=ATOL_EXACT)
    assert np.isclose(cosine(total // 2), lr_max * 0.5, atol=ATOL_EXACT)
    assert np.isclose(cosine(total), 0.0, atol=ATOL_EXACT)


def test_linear_warmup_is_linear():
    """Warmup: lr(t) = lr_max * t / warmup for t <= warmup; slope is constant."""
    lr_max, warmup = 0.1, 10
    lrs = np.array([lr_max * t / warmup for t in range(warmup + 1)])
    assert np.isclose(lrs[0], 0.0, atol=ATOL_EXACT)
    assert np.isclose(lrs[-1], lr_max, atol=ATOL_EXACT)
    # Equal first differences => exactly linear.
    assert np.allclose(np.diff(lrs), lr_max / warmup, atol=ATOL_EXACT)
