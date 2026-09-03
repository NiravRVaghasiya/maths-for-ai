"""Independent numerical oracles shared across the regression tests.

These are the "NUMERICAL" leg of the analytical / numerical / library
triangulation. They are written here from first principles precisely so that a
test comparing an *analytic* closed form against one of these functions is a
real cross-check between two independently-derived quantities -- not a notebook
function checked against a copy of itself.

Nothing in this module imports curriculum/notebook code.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from .tolerances import FD_STEP, FD_STEP_HESSIAN


def seeded_rng(seed: int = 0) -> np.random.Generator:
    """Return a deterministically-seeded NumPy Generator.

    All randomized tests draw from a seeded generator so runs are reproducible
    and CI never sees a spurious failure from an unlucky draw.
    """
    return np.random.default_rng(seed)


def finite_diff_gradient(
    f: Callable[[np.ndarray], float], x: np.ndarray, h: float = FD_STEP
) -> np.ndarray:
    """Central-difference gradient of a scalar function f: R^n -> R.

    Central differences give O(h^2) truncation error, an order better than the
    forward difference, for the same reason a symmetric stencil cancels the
    first-order Taylor term.
    """
    x = np.asarray(x, dtype=float)
    grad = np.zeros_like(x)
    for i in range(x.size):
        step = np.zeros_like(x)
        step[i] = h
        grad[i] = (f(x + step) - f(x - step)) / (2.0 * h)
    return grad


def finite_diff_jacobian(
    f: Callable[[np.ndarray], np.ndarray], x: np.ndarray, h: float = FD_STEP
) -> np.ndarray:
    """Central-difference Jacobian of a vector function f: R^n -> R^m.

    Returns an (m, n) matrix J with J[i, j] = d f_i / d x_j.
    """
    x = np.asarray(x, dtype=float)
    f0 = np.asarray(f(x), dtype=float)
    m, n = f0.size, x.size
    jac = np.zeros((m, n))
    for j in range(n):
        step = np.zeros_like(x)
        step[j] = h
        jac[:, j] = (np.asarray(f(x + step)) - np.asarray(f(x - step))) / (2.0 * h)
    return jac


def finite_diff_hessian(
    f: Callable[[np.ndarray], float], x: np.ndarray, h: float = FD_STEP_HESSIAN
) -> np.ndarray:
    """Central-difference Hessian of a scalar function f: R^n -> R.

    Uses the standard second-order mixed-partial stencil
        H[i,j] = (f(x+e_i+e_j) - f(x+e_i-e_j) - f(x-e_i+e_j) + f(x-e_i-e_j)) / (4 h^2)
    which is a finite difference *of* a finite difference -- hence the larger
    optimal step (h ~ eps^(1/4)) and looser tolerance than a single-layer FD.
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    hess = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            xpp = x.copy()
            xpp[i] += h
            xpp[j] += h
            xpm = x.copy()
            xpm[i] += h
            xpm[j] -= h
            xmp = x.copy()
            xmp[i] -= h
            xmp[j] += h
            xmm = x.copy()
            xmm[i] -= h
            xmm[j] -= h
            hess[i, j] = (f(xpp) - f(xpm) - f(xmp) + f(xmm)) / (4.0 * h * h)
    return hess


def empirical_moment(samples: np.ndarray, order: int = 1, central: bool = False) -> float:
    """Empirical raw or central moment of a 1-D sample array.

    A tiny, self-evidently-correct estimator used as the Monte-Carlo leg for the
    probability identities (mean, variance, higher moments).
    """
    samples = np.asarray(samples, dtype=float)
    if central:
        samples = samples - samples.mean()
    return float(np.mean(samples**order))


def log_log_slope(hs: np.ndarray, errors: np.ndarray) -> float:
    """Least-squares slope of log(error) vs log(h).

    Used to verify the *order* of a finite-difference scheme empirically: a
    forward difference should show slope ~1 (error ~ h), a central difference
    slope ~2 (error ~ h^2). Asserting the slope is a constant-free statement
    about the method, stronger than a single closeness check.
    """
    hs = np.asarray(hs, dtype=float)
    errors = np.asarray(errors, dtype=float)
    logs_h = np.log(hs)
    logs_e = np.log(errors)
    slope, _ = np.polyfit(logs_h, logs_e, 1)
    return float(slope)
