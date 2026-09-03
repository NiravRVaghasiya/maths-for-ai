"""Regression tests for linear-algebra identities (curriculum module 01, 08).

Identities covered: matrix multiplication (definition), inverse (A A^{-1} = I,
solve consistency), determinant (product rule, triangular product), QR
(orthonormal Q, reconstruction), Cholesky (L L^T = A), eigenvalues (A v = lambda
v, trace = sum, det = product, symmetric => real spectrum), and SVD
(reconstruction, orthonormality, singular values = sqrt(eig(A^T A)), Eckart-Young
low-rank optimality).

Anti-tautology note: we never re-run a notebook's "scratch == numpy" check. For
matmul we verify against the *summation definition* (an independent computation),
and elsewhere we assert mathematical *relationships* (e.g. det(AB)=det(A)det(B),
sigma_i = sqrt(eig_i(A^T A))) that hold regardless of which implementation
produced the numbers.
"""

from __future__ import annotations

import numpy as np
import pytest

from ..tolerances import ATOL_EXACT, RTOL_EXACT
from .conftest import random_spd, random_well_conditioned

SIZES = [2, 3, 5, 12]


# --------------------------------------------------------------------------
# Matrix multiplication
# --------------------------------------------------------------------------
@pytest.mark.parametrize("n", SIZES)
def test_matmul_matches_summation_definition(rng, n):
    """(AB)_{ik} = sum_j A_{ij} B_{jk}, computed independently of np.matmul."""
    a = rng.standard_normal((n, n))
    b = rng.standard_normal((n, n))
    prod = a @ b
    # Independent triple-sum definition (einsum expresses the definition, not the
    # BLAS matmul path np.matmul uses).
    definition = np.einsum("ij,jk->ik", a, b)
    assert np.allclose(prod, definition, atol=ATOL_EXACT, rtol=RTOL_EXACT)


def test_matmul_is_associative_and_distributes(rng):
    a = rng.standard_normal((4, 3))
    b = rng.standard_normal((3, 5))
    c = rng.standard_normal((5, 2))
    assert np.allclose((a @ b) @ c, a @ (b @ c), atol=ATOL_EXACT, rtol=RTOL_EXACT)
    d = rng.standard_normal((3, 5))
    assert np.allclose(a @ (b + d), a @ b + a @ d, atol=ATOL_EXACT, rtol=RTOL_EXACT)


# --------------------------------------------------------------------------
# Inverse
# --------------------------------------------------------------------------
@pytest.mark.parametrize("n", SIZES)
def test_inverse_times_matrix_is_identity(rng, n):
    a = random_well_conditioned(rng, n)
    a_inv = np.linalg.inv(a)
    identity = np.eye(n)
    assert np.allclose(a @ a_inv, identity, atol=ATOL_EXACT, rtol=RTOL_EXACT)
    assert np.allclose(a_inv @ a, identity, atol=ATOL_EXACT, rtol=RTOL_EXACT)


@pytest.mark.parametrize("n", SIZES)
def test_solve_is_consistent_with_inverse(rng, n):
    """A x = b  =>  x = A^{-1} b, and A x reproduces b.

    Cross-checks two independent library paths (solve vs inv) against the
    defining equation, so agreement is not circular.
    """
    a = random_well_conditioned(rng, n)
    b = rng.standard_normal(n)
    x = np.linalg.solve(a, b)
    assert np.allclose(a @ x, b, atol=ATOL_EXACT, rtol=RTOL_EXACT)
    assert np.allclose(x, np.linalg.inv(a) @ b, atol=ATOL_EXACT, rtol=RTOL_EXACT)


def test_inverse_of_product_reverses_order(rng):
    """(AB)^{-1} = B^{-1} A^{-1}."""
    a = random_well_conditioned(rng, 5)
    b = random_well_conditioned(rng, 5)
    assert np.allclose(
        np.linalg.inv(a @ b),
        np.linalg.inv(b) @ np.linalg.inv(a),
        atol=ATOL_EXACT,
        rtol=RTOL_EXACT,
    )


# --------------------------------------------------------------------------
# Determinant
# --------------------------------------------------------------------------
def test_determinant_product_rule(rng):
    """det(AB) = det(A) det(B)."""
    a = rng.standard_normal((6, 6))
    b = rng.standard_normal((6, 6))
    assert np.isclose(
        np.linalg.det(a @ b),
        np.linalg.det(a) * np.linalg.det(b),
        atol=ATOL_EXACT,
        rtol=1e-7,  # det scales like product of entries; allow a touch more rel. room
    )


def test_determinant_of_triangular_is_product_of_diagonal(rng):
    """For triangular T, det(T) = prod(diag(T)) -- an independent hand identity."""
    t = np.triu(rng.standard_normal((5, 5)))
    assert np.isclose(np.linalg.det(t), np.prod(np.diag(t)), atol=ATOL_EXACT, rtol=1e-7)


def test_determinant_equals_product_of_eigenvalues(rng):
    a = rng.standard_normal((5, 5))
    eigvals = np.linalg.eigvals(a)
    assert np.isclose(np.linalg.det(a), np.prod(eigvals).real, atol=1e-7, rtol=1e-7)


# --------------------------------------------------------------------------
# QR decomposition
# --------------------------------------------------------------------------
@pytest.mark.parametrize("n", SIZES)
def test_qr_reconstructs_and_q_is_orthonormal(rng, n):
    a = rng.standard_normal((n, n))
    q, r = np.linalg.qr(a)
    assert np.allclose(q @ r, a, atol=ATOL_EXACT, rtol=RTOL_EXACT)
    assert np.allclose(q.T @ q, np.eye(n), atol=ATOL_EXACT, rtol=RTOL_EXACT)
    # R is upper-triangular: its strict lower part is exactly zero.
    assert np.allclose(np.tril(r, -1), 0.0, atol=ATOL_EXACT)


# --------------------------------------------------------------------------
# Cholesky decomposition
# --------------------------------------------------------------------------
@pytest.mark.parametrize("n", SIZES)
def test_cholesky_reconstructs_spd(rng, n):
    a = random_spd(rng, n)
    lower = np.linalg.cholesky(a)
    assert np.allclose(lower @ lower.T, a, atol=1e-8, rtol=RTOL_EXACT)
    assert np.allclose(np.triu(lower, 1), 0.0, atol=ATOL_EXACT)


# --------------------------------------------------------------------------
# Eigenvalues / eigenvectors
# --------------------------------------------------------------------------
@pytest.mark.parametrize("n", SIZES)
def test_eigenpairs_satisfy_defining_equation(rng, n):
    """A v = lambda v for every returned eigenpair."""
    a = rng.standard_normal((n, n))
    eigvals, eigvecs = np.linalg.eig(a)
    for i in range(n):
        lhs = a @ eigvecs[:, i]
        rhs = eigvals[i] * eigvecs[:, i]
        assert np.allclose(lhs, rhs, atol=1e-8, rtol=1e-7)


@pytest.mark.parametrize("n", SIZES)
def test_trace_is_sum_and_det_is_product_of_eigenvalues(rng, n):
    a = rng.standard_normal((n, n))
    eigvals = np.linalg.eigvals(a)
    assert np.isclose(np.trace(a), np.sum(eigvals).real, atol=1e-8, rtol=1e-7)
    assert np.isclose(np.linalg.det(a), np.prod(eigvals).real, atol=1e-7, rtol=1e-6)


@pytest.mark.parametrize("n", SIZES)
def test_symmetric_matrix_has_real_spectrum_and_orthonormal_eigenvectors(rng, n):
    a = rng.standard_normal((n, n))
    sym = a + a.T
    eigvals, eigvecs = np.linalg.eigh(sym)
    # eigh returns real eigenvalues by construction; verify they diagonalize sym:
    # sym = Q diag(lambda) Q^T with Q orthonormal.
    assert np.allclose(eigvecs @ np.diag(eigvals) @ eigvecs.T, sym, atol=1e-8, rtol=1e-7)
    assert np.allclose(eigvecs.T @ eigvecs, np.eye(n), atol=ATOL_EXACT, rtol=RTOL_EXACT)


# --------------------------------------------------------------------------
# SVD
# --------------------------------------------------------------------------
@pytest.mark.parametrize("shape", [(4, 4), (6, 3), (3, 6), (10, 7)])
def test_svd_reconstruction_and_orthonormal_factors(rng, shape):
    a = rng.standard_normal(shape)
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    reconstructed = (u * s) @ vt
    assert np.allclose(reconstructed, a, atol=ATOL_EXACT, rtol=RTOL_EXACT)
    k = s.size
    assert np.allclose(u.T @ u, np.eye(k), atol=ATOL_EXACT, rtol=RTOL_EXACT)
    assert np.allclose(vt @ vt.T, np.eye(k), atol=ATOL_EXACT, rtol=RTOL_EXACT)
    # Singular values are non-negative and sorted descending.
    assert np.all(s >= -ATOL_EXACT)
    assert np.all(np.diff(s) <= ATOL_EXACT)


@pytest.mark.parametrize("shape", [(6, 3), (10, 7), (5, 5)])
def test_singular_values_are_sqrt_eigenvalues_of_gram(rng, shape):
    """sigma_i(A) = sqrt(lambda_i(A^T A)) -- the defining SVD/eigen relationship.

    This is an independent derivation of the singular values (via the eigenvalues
    of the Gram matrix), compared to np.linalg.svd. Agreement confirms the
    identity, not that svd equals itself.
    """
    a = rng.standard_normal(shape)
    s_svd = np.linalg.svd(a, compute_uv=False)
    gram_eigs = np.linalg.eigvalsh(a.T @ a)
    s_from_eig = np.sqrt(np.clip(gram_eigs, 0.0, None))[::-1][: s_svd.size]
    assert np.allclose(s_svd, s_from_eig, atol=1e-8, rtol=1e-7)


def test_eckart_young_low_rank_optimality(rng):
    """The rank-k truncated SVD is the best rank-k approximation in Frobenius norm.

    Eckart-Young: for the truncation A_k = sum_{i<k} sigma_i u_i v_i^T, the error
    equals sqrt(sum_{i>=k} sigma_i^2), and no other rank-k matrix does better.
    We verify (a) the exact residual formula and (b) that random rank-k matrices
    never beat it.
    """
    a = rng.standard_normal((12, 8))
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    k = 3
    a_k = (u[:, :k] * s[:k]) @ vt[:k]
    residual = np.linalg.norm(a - a_k, "fro")
    predicted = np.sqrt(np.sum(s[k:] ** 2))
    assert np.isclose(residual, predicted, atol=1e-8, rtol=1e-7)

    # No random rank-k competitor achieves a smaller error (allow a tiny margin).
    for _ in range(20):
        left = rng.standard_normal((12, k))
        right = rng.standard_normal((k, 8))
        competitor_err = np.linalg.norm(a - left @ right, "fro")
        assert competitor_err >= residual - 1e-9
