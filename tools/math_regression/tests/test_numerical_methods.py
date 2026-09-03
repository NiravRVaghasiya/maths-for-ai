"""Regression tests for numerical-methods identities (module 06).

Covered: finite-difference error ORDER (forward ~ O(h), central ~ O(h^2)) via a
log-log slope; numerically-stable softmax / log-sum-exp equal to their naive
definition when the naive form doesn't overflow, agree with scipy.special, and
survive inputs that overflow the naive form; conjugate gradient solving an SPD
system in <= n steps and matching np.linalg.solve; IEEE-754 float32
decompose/reconstruct round-trip; and a natural-cubic-spline interpolation with
C^2 continuity at the interior knots.

Anti-tautology note: the error-order tests assert a convergence *slope*, a
constant-free property of the scheme itself. The stability tests compare against
an independent oracle (scipy.special) and against the mathematically-invariant
fact that softmax/logsumexp are shift-equivariant.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy.special import logsumexp as scipy_logsumexp
from scipy.special import softmax as scipy_softmax

from ..oracles import log_log_slope, seeded_rng
from ..tolerances import ATOL_EXACT, RTOL_EXACT


# --------------------------------------------------------------------------
# Finite-difference error order
# --------------------------------------------------------------------------
def test_forward_difference_is_first_order():
    """Forward difference (f(x+h)-f(x))/h has truncation error ~ O(h): slope ~ 1."""
    f, fp = np.sin, np.cos
    x = 0.7
    hs = np.array([1e-1, 1e-2, 1e-3, 1e-4])
    errs = np.array([abs((f(x + h) - f(x)) / h - fp(x)) for h in hs])
    assert log_log_slope(hs, errs) == pytest.approx(1.0, abs=0.1)


def test_central_difference_is_second_order():
    """Central difference has truncation error ~ O(h^2): slope ~ 2.

    Steps are kept well above the round-off floor (~1e-6) so truncation, not
    round-off, dominates and the O(h^2) regime is what we actually observe.
    """
    f, fp = np.sin, np.cos
    x = 0.7
    hs = np.array([1e-1, 1e-2, 1e-3, 1e-4])
    errs = np.array([abs((f(x + h) - f(x - h)) / (2 * h) - fp(x)) for h in hs])
    assert log_log_slope(hs, errs) == pytest.approx(2.0, abs=0.1)


# --------------------------------------------------------------------------
# Numerically-stable softmax / logsumexp
# --------------------------------------------------------------------------
def _stable_softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


def _stable_logsumexp(z):
    m = z.max()
    return m + np.log(np.sum(np.exp(z - m)))


def test_stable_softmax_matches_naive_when_naive_is_safe(rng):
    """The max-subtraction is algebraically a no-op: softmax is shift-invariant."""
    z = rng.standard_normal(6)
    naive = np.exp(z) / np.exp(z).sum()
    assert np.allclose(_stable_softmax(z), naive, atol=ATOL_EXACT, rtol=RTOL_EXACT)
    assert np.allclose(_stable_softmax(z), scipy_softmax(z), atol=ATOL_EXACT, rtol=RTOL_EXACT)
    assert np.isclose(_stable_softmax(z).sum(), 1.0, atol=ATOL_EXACT)


def test_stable_softmax_survives_overflow_inputs():
    """Inputs that overflow exp() naively still produce a valid softmax.

    The naive exp(1000) is +inf (=> nan probabilities); the stable form is finite
    and normalized. This is the whole point of the identity.
    """
    z = np.array([1000.0, 1001.0, 1002.0])
    with np.errstate(over="ignore"):  # the overflow is the point we're demonstrating
        naive = np.exp(z)
    assert not np.isfinite(naive).all()  # confirm the naive path really overflows
    s = _stable_softmax(z)
    assert np.all(np.isfinite(s))
    assert np.isclose(s.sum(), 1.0, atol=ATOL_EXACT)
    assert np.allclose(s, scipy_softmax(z), atol=ATOL_EXACT, rtol=RTOL_EXACT)


def test_stable_logsumexp_matches_scipy_and_is_shift_equivariant(rng):
    z = rng.standard_normal(8)
    assert np.isclose(_stable_logsumexp(z), scipy_logsumexp(z), atol=ATOL_EXACT, rtol=RTOL_EXACT)
    # logsumexp(z + c) = logsumexp(z) + c  -- an exact identity.
    c = 5.0
    assert np.isclose(
        _stable_logsumexp(z + c), _stable_logsumexp(z) + c, atol=1e-9, rtol=RTOL_EXACT
    )


# --------------------------------------------------------------------------
# Conjugate gradient
# --------------------------------------------------------------------------
def _conjugate_gradient(a, b, max_iter=None):
    """Textbook CG for SPD A. Returns (x, iters)."""
    n = b.size
    max_iter = max_iter or n
    x = np.zeros(n)
    r = b - a @ x
    p = r.copy()
    rs_old = r @ r
    iters = 0
    for _ in range(max_iter):
        iters += 1
        ap = a @ p
        alpha = rs_old / (p @ ap)
        x = x + alpha * p
        r = r - alpha * ap
        rs_new = r @ r
        if np.sqrt(rs_new) < 1e-12:
            break
        p = r + (rs_new / rs_old) * p
        rs_old = rs_new
    return x, iters


@pytest.mark.parametrize("n", [3, 6, 10])
def test_conjugate_gradient_solves_spd_within_n_steps(n):
    """CG on an SPD system converges to A^{-1}b in at most n iterations.

    The solution is checked against the independent np.linalg.solve, and the
    iteration count against CG's finite-termination guarantee.
    """
    rng = seeded_rng(n)
    q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    a = (q * rng.uniform(1.0, 20.0, n)) @ q.T  # SPD, bounded condition number
    b = rng.standard_normal(n)

    x_cg, iters = _conjugate_gradient(a, b)
    x_true = np.linalg.solve(a, b)
    assert np.allclose(x_cg, x_true, atol=1e-6, rtol=1e-6)
    assert iters <= n


# --------------------------------------------------------------------------
# IEEE-754 float32 decomposition
# --------------------------------------------------------------------------
@pytest.mark.parametrize("value", [1.0, 0.15625, -2.5, 3.14159, 1e-3, 12345.0])
def test_ieee754_float32_reconstruction(value):
    """value = (-1)^sign * (1 + mantissa/2^23) * 2^(exp-127) for normal float32.

    Decompose a float32 into its IEEE-754 fields and reconstruct from the
    formula, independent of the original value.
    """
    import struct

    bits = struct.unpack(">I", struct.pack(">f", np.float32(value)))[0]
    sign = (bits >> 31) & 0x1
    exponent = (bits >> 23) & 0xFF
    mantissa = bits & 0x7FFFFF

    reconstructed = ((-1) ** sign) * (1 + mantissa / 2**23) * 2.0 ** (exponent - 127)
    assert np.isclose(reconstructed, np.float32(value), rtol=1e-6, atol=1e-9)


# --------------------------------------------------------------------------
# Natural cubic spline
# --------------------------------------------------------------------------
def test_cubic_spline_interpolates_and_is_c2_continuous():
    """A natural cubic spline passes through its knots and is C^2 at interior knots.

    Uses scipy's CubicSpline as the (trusted) spline builder, then verifies the
    mathematical DEFINING properties -- interpolation, and continuity of the
    first and second derivatives across each interior knot -- rather than
    re-deriving the tridiagonal solve.
    """
    from scipy.interpolate import CubicSpline

    rng = seeded_rng(0)
    x = np.sort(rng.uniform(0, 10, 8))
    x = np.unique(x)
    y = np.sin(x) + 0.3 * x
    cs = CubicSpline(x, y, bc_type="natural")

    # Interpolation: spline hits every knot exactly.
    assert np.allclose(cs(x), y, atol=1e-10)

    # C^2 continuity: 1st and 2nd derivatives match from both sides at interior knots.
    eps = 1e-6
    for xi in x[1:-1]:
        assert np.isclose(cs(xi - eps, 1), cs(xi + eps, 1), atol=1e-4)  # C^1
        assert np.isclose(cs(xi - eps, 2), cs(xi + eps, 2), atol=1e-3)  # C^2

    # Natural boundary condition: second derivative is zero at the endpoints.
    assert np.isclose(cs(x[0], 2), 0.0, atol=1e-8)
    assert np.isclose(cs(x[-1], 2), 0.0, atol=1e-8)
