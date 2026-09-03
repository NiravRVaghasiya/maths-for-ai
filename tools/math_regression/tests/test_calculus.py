"""Regression tests for calculus identities (curriculum module 02).

Covered: gradients (analytic vs central-difference vs torch.autograd), the
Jacobian chain rule J_{g o f} = J_g(f(x)) @ J_f(x), the Hessian (symmetry,
matches FD-of-gradient, matches torch.autograd), the directional derivative
identity D_u f = grad f . u, a Taylor-remainder order check, and the softmax
Jacobian identity J = diag(s) - s s^T.

Anti-tautology note: the analytic gradients/Hessians below are hand-derived
closed forms for known functions. Comparing them to a finite-difference oracle
(this framework's own, in oracles.py) and to torch.autograd gives three
independently-computed answers; a bug in any one would break the agreement.
"""

from __future__ import annotations

import numpy as np
import pytest

from ..oracles import (
    finite_diff_gradient,
    finite_diff_hessian,
    finite_diff_jacobian,
    log_log_slope,
)
from ..tolerances import ATOL_FD, ATOL_FD2, RTOL_FD, RTOL_FD2

torch = pytest.importorskip("torch")


# --- A known scalar field with a hand-derived gradient and Hessian ---------
def f_scalar(x):
    # f(x, y) = x^3 y^2 + exp(x y)
    return x[0] ** 3 * x[1] ** 2 + np.exp(x[0] * x[1])


def grad_f_analytic(x):
    x0, x1 = x
    e = np.exp(x0 * x1)
    return np.array(
        [
            3 * x0**2 * x1**2 + x1 * e,  # df/dx
            2 * x0**3 * x1 + x0 * e,  # df/dy
        ]
    )


def hess_f_analytic(x):
    x0, x1 = x
    e = np.exp(x0 * x1)
    return np.array(
        [
            [6 * x0 * x1**2 + x1**2 * e, 3 * 2 * x0**2 * x1 + e + x0 * x1 * e],
            [6 * x0**2 * x1 + e + x0 * x1 * e, 2 * x0**3 + x0**2 * e],
        ]
    )


TEST_POINTS = [np.array([0.6, 0.9]), np.array([-0.4, 1.1]), np.array([1.2, -0.7])]


@pytest.mark.parametrize("x", TEST_POINTS)
def test_gradient_analytic_matches_finite_difference(x):
    assert np.allclose(
        grad_f_analytic(x), finite_diff_gradient(f_scalar, x), atol=ATOL_FD, rtol=RTOL_FD
    )


@pytest.mark.parametrize("x", TEST_POINTS)
def test_gradient_analytic_matches_torch_autograd(x):
    xt = torch.tensor(x, requires_grad=True)
    y = xt[0] ** 3 * xt[1] ** 2 + torch.exp(xt[0] * xt[1])
    y.backward()
    assert np.allclose(grad_f_analytic(x), xt.grad.numpy(), atol=1e-10, rtol=1e-9)


@pytest.mark.parametrize("x", TEST_POINTS)
def test_hessian_symmetry_and_matches_finite_difference(x):
    h_analytic = hess_f_analytic(x)
    # Clairaut: mixed partials commute => Hessian is symmetric.
    assert np.allclose(h_analytic, h_analytic.T, atol=1e-12)
    assert np.allclose(h_analytic, finite_diff_hessian(f_scalar, x), atol=ATOL_FD2, rtol=RTOL_FD2)


@pytest.mark.parametrize("x", TEST_POINTS)
def test_hessian_matches_torch_autograd(x):
    def f_t(v):
        return v[0] ** 3 * v[1] ** 2 + torch.exp(v[0] * v[1])

    h_torch = torch.autograd.functional.hessian(f_t, torch.tensor(x)).numpy()
    assert np.allclose(hess_f_analytic(x), h_torch, atol=1e-9, rtol=1e-8)


# --- Jacobian chain rule ---------------------------------------------------
def test_jacobian_chain_rule():
    """J_{g o f}(x) = J_g(f(x)) @ J_f(x).

    Computed two independent ways: the product of the two component Jacobians,
    and a direct finite-difference Jacobian of the composed map. Both use the
    numerical oracle, but the *chain-rule product* is the identity under test.
    """
    f = lambda x: np.array([x[0] ** 2, x[0] * x[1]])  # noqa: E731
    g = lambda y: np.array([np.sin(y[0]), y[1] ** 2])  # noqa: E731
    h = lambda x: g(f(x))  # noqa: E731
    x0 = np.array([1.2, 0.7])

    j_chain = finite_diff_jacobian(g, f(x0)) @ finite_diff_jacobian(f, x0)
    j_direct = finite_diff_jacobian(h, x0)
    assert np.allclose(j_chain, j_direct, atol=ATOL_FD, rtol=RTOL_FD)

    # Also anchor against a fully analytic Jacobian of the composition.
    x, y = x0
    j_f = np.array([[2 * x, 0.0], [y, x]])
    j_g = np.array([[np.cos(f(x0)[0]), 0.0], [0.0, 2 * f(x0)[1]]])
    assert np.allclose(j_g @ j_f, j_direct, atol=ATOL_FD, rtol=RTOL_FD)


# --- Directional derivative ------------------------------------------------
@pytest.mark.parametrize("x", TEST_POINTS)
def test_directional_derivative_equals_grad_dot_unit(x):
    """D_u f = grad f . u for a unit vector u.

    LHS is a 1-D central difference along u; RHS uses the analytic gradient.
    """
    u = np.array([1.0, 2.0])
    u = u / np.linalg.norm(u)
    h = 1e-5
    directional = (f_scalar(x + h * u) - f_scalar(x - h * u)) / (2 * h)
    assert np.isclose(directional, grad_f_analytic(x) @ u, atol=ATOL_FD, rtol=RTOL_FD)


# --- Taylor expansion order ------------------------------------------------
def test_first_order_taylor_remainder_is_second_order():
    """|f(x+h u) - [f(x) + h grad.u]| ~ O(h^2): the remainder slope on log-log ~ 2."""
    x = np.array([0.6, 0.9])
    u = np.array([0.6, -0.8])  # unit
    f0 = f_scalar(x)
    g0 = grad_f_analytic(x) @ u
    hs = np.array([1e-1, 5e-2, 2.5e-2, 1.25e-2, 6.25e-3])
    errs = np.array([abs(f_scalar(x + h * u) - (f0 + h * g0)) for h in hs])
    assert log_log_slope(hs, errs) == pytest.approx(2.0, abs=0.15)


# --- Softmax Jacobian identity ---------------------------------------------
@pytest.mark.parametrize("z", [np.array([1.0, 2.0, 0.5]), np.array([-1.0, 0.3, 2.2, 0.0])])
def test_softmax_jacobian_identity(z):
    """J_softmax = diag(s) - s s^T, verified against a finite-difference Jacobian."""

    def softmax(v):
        e = np.exp(v - v.max())
        return e / e.sum()

    s = softmax(z)
    j_identity = np.diag(s) - np.outer(s, s)
    j_numeric = finite_diff_jacobian(softmax, z)
    assert np.allclose(j_identity, j_numeric, atol=ATOL_FD, rtol=RTOL_FD)
    # Rows of the softmax Jacobian sum to zero (softmax outputs live on the simplex).
    assert np.allclose(j_identity.sum(axis=1), 0.0, atol=1e-12)
