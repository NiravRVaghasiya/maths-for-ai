"""Shared fixtures/helpers for the mathematical regression tests."""

from __future__ import annotations

import numpy as np
import pytest

# A fixed pool of seeds so every randomized test is reproducible AND exercises
# more than one random instance (a bug that only shows on some matrices, not
# others, is much more likely to be caught by several seeds than by one).
SEEDS = [0, 1, 7, 42, 123]


@pytest.fixture(params=SEEDS)
def rng(request) -> np.random.Generator:
    """A seeded NumPy Generator, parametrized over several seeds."""
    return np.random.default_rng(request.param)


def random_spd(rng: np.random.Generator, n: int, cond_cap: float = 1e3) -> np.ndarray:
    """A random symmetric positive-definite matrix with a bounded condition number.

    Built as ``Q diag(d) Q^T`` with eigenvalues d drawn in [1, cond_cap]. Bounding
    the condition number keeps round-off predictable so the EXACT-algebra
    tolerances remain justified (an unbounded random SPD can be arbitrarily
    ill-conditioned and would need a looser, less meaningful bound).
    """
    q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    d = rng.uniform(1.0, cond_cap, size=n)
    return (q * d) @ q.T


def random_well_conditioned(rng: np.random.Generator, n: int) -> np.ndarray:
    """A random square matrix nudged to be well away from singular.

    Adds n*I to a standard-normal matrix so it is diagonally dominant and
    comfortably invertible -- appropriate for identities like A @ A^{-1} = I
    where we want round-off, not near-singularity, to be the only error.
    """
    a = rng.standard_normal((n, n))
    return a + n * np.eye(n)
