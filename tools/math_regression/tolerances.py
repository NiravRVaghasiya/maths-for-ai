"""Justified numerical tolerances for the mathematical regression tests.

Every tolerance in this framework is defined here, with the reasoning that
justifies its magnitude. The point is that a tolerance is a *claim about the
dominant error source*, not a knob you turn until the test passes. If a test
needs a looser tolerance than the one its error model predicts, that is a signal
worth investigating, not something to paper over with a bigger number.

There are three error regimes in this suite, and one tolerance family for each.

--------------------------------------------------------------------------------
1. EXACT ALGEBRA (round-off only)
--------------------------------------------------------------------------------
Operations like ``A @ A_inv == I`` or ``det(AB) == det(A)det(B)`` are
mathematically exact; the only error is IEEE-754 double-precision round-off.
Machine epsilon for float64 is eps ~= 2.22e-16. A single operation loses ~eps of
relative precision; a chain of O(n) dependent operations (a length-n dot product,
an n-term factorization) accumulates round-off that grows roughly like
``n * eps`` in the benign case and can be amplified by a problem's condition
number ``kappa``. For the well-conditioned, modest-size (n <= ~50) matrices used
here, ``n * kappa * eps`` stays comfortably below ~1e-9, so:

    ATOL_EXACT = 1e-9,  RTOL_EXACT = 1e-9

is a safe ceiling that is still ~6 orders of magnitude tighter than a
finite-difference tolerance -- i.e. it would still catch a genuinely wrong
result. Deliberately ill-conditioned tests set their own looser bound and say
why.

--------------------------------------------------------------------------------
2. FINITE-DIFFERENCE APPROXIMATION (truncation + round-off tradeoff)
--------------------------------------------------------------------------------
A central difference (f(x+h) - f(x-h)) / (2h) has truncation error O(h^2); a
one-sided (forward) difference has error O(h). But shrinking h also amplifies
round-off, which grows like eps/h. The total error of a central difference is
minimized near

    h* ~= (eps)^(1/3) ~= 6e-6,   giving a best-case accuracy ~ (eps)^(2/3) ~= 4e-11.

In practice we use h = 1e-5 (close to h*) and allow headroom for the O(h^2)
constant (third derivative of the test function) and for composing several
approximations (e.g. a Hessian is a finite difference *of* a finite difference):

    ATOL_FD = 1e-6,  RTOL_FD = 1e-5   (gradients / Jacobians, single FD layer)
    ATOL_FD2 = 1e-3, RTOL_FD2 = 1e-3  (Hessians: FD-of-FD, two layers of O(h^2))

The error-*order* tests (forward ~ O(h), central ~ O(h^2)) don't use these
closeness bounds at all -- they assert the observed convergence *slope* on a
log-log h-sweep, which is a stronger, constant-free statement.

--------------------------------------------------------------------------------
3. MONTE-CARLO ESTIMATION (sampling error)
--------------------------------------------------------------------------------
An empirical mean of N i.i.d. samples has standard error sigma/sqrt(N). To test
"empirical mean ~= analytic mean" we need a band of several standard errors so a
correct test essentially never flakes, while still being tight enough to catch a
wrong formula. We fix N and seed the RNG, then size the tolerance from the
distribution's own standard error:

    MC_SAMPLES = 200_000
    mc_atol(sigma) = MC_SIGMA_BANDS * sigma / sqrt(MC_SAMPLES)

with MC_SIGMA_BANDS = 6. Six standard errors makes a false failure astronomically
unlikely (P ~ 2e-9 for a Gaussian) yet, for the sample sizes here, is far smaller
than the gap a genuinely wrong mean/variance formula would produce. Because the
RNG is seeded, results are deterministic and reproducible across runs.
"""

from __future__ import annotations

import numpy as np

# --- 1. Exact algebra (float64 round-off) ---------------------------------
EPS64: float = float(np.finfo(np.float64).eps)  # ~2.220446e-16
ATOL_EXACT: float = 1e-9
RTOL_EXACT: float = 1e-9

# --- 2. Finite differences -------------------------------------------------
# Step size near the theoretical optimum h* ~= eps^(1/3) for a central diff.
FD_STEP: float = 1e-5
# Best step for a Hessian (FD of FD) is larger: eps^(1/4) ~= 1.2e-4.
FD_STEP_HESSIAN: float = 1e-4

ATOL_FD: float = 1e-6
RTOL_FD: float = 1e-5
ATOL_FD2: float = 1e-3  # Hessian: two composed O(h^2) approximations
RTOL_FD2: float = 1e-3

# --- 3. Monte-Carlo --------------------------------------------------------
MC_SAMPLES: int = 200_000
MC_SIGMA_BANDS: float = 6.0


def mc_atol(sigma: float, n: int = MC_SAMPLES, bands: float = MC_SIGMA_BANDS) -> float:
    """Monte-Carlo absolute tolerance = ``bands`` standard errors of the mean.

    The standard error of an N-sample empirical mean is ``sigma / sqrt(N)``.
    Using several standard errors (default 6) makes a spurious failure of a
    *correct* estimator vanishingly unlikely while staying far tighter than the
    discrepancy a *wrong* closed form would introduce.
    """
    return bands * float(sigma) / np.sqrt(n)


def mc_atol_variance(sigma: float, n: int = MC_SAMPLES, bands: float = MC_SIGMA_BANDS) -> float:
    """Monte-Carlo tolerance for a *variance* estimate.

    For roughly-normal data the sample variance s^2 has standard error
    ``sigma^2 * sqrt(2 / (N - 1))``. We approximate with sqrt(2/N) and again
    allow ``bands`` standard errors.
    """
    return bands * (float(sigma) ** 2) * np.sqrt(2.0 / n)
