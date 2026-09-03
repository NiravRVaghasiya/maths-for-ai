"""Regression tests for probability & statistics identities (module 03).

Covered: distribution mean/variance closed forms (Bernoulli, Binomial, Poisson,
Exponential, Beta, Normal) verified three ways -- analytic formula vs scipy.stats
vs seeded Monte-Carlo; Bayes' theorem (posterior normalization) and Beta-Bernoulli
conjugacy; Gaussian MLE closed form vs numerical argmax of the log-likelihood;
Fisher information / Cramer-Rao Var(MLE) ~ sigma^2/n via Monte-Carlo; linearity of
expectation; and the law of total probability.

Anti-tautology note: the analytic mean/variance formulas are hand-written; scipy
computes them from its own internals; Monte-Carlo estimates them from samples.
Three independent routes to the same number. Monte-Carlo tolerances come from the
distribution's own standard error (tolerances.mc_atol), not a hand-tuned constant.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats

from ..oracles import seeded_rng
from ..tolerances import ATOL_EXACT, MC_SAMPLES, mc_atol, mc_atol_variance


# --------------------------------------------------------------------------
# Distribution mean & variance: analytic vs scipy vs Monte-Carlo
# --------------------------------------------------------------------------
# Each entry: (name, scipy frozen dist, analytic mean, analytic var, sampler).
def _distributions():
    rng = seeded_rng(0)
    p = 0.3
    yield (
        "bernoulli",
        stats.bernoulli(p),
        p,
        p * (1 - p),
        lambda n: (rng.random(n) < p).astype(float),
    )
    n_bin, p_bin = 10, 0.4
    yield (
        "binomial",
        stats.binom(n_bin, p_bin),
        n_bin * p_bin,
        n_bin * p_bin * (1 - p_bin),
        lambda n: rng.binomial(n_bin, p_bin, size=n).astype(float),
    )
    lam = 4.0
    yield (
        "poisson",
        stats.poisson(lam),
        lam,
        lam,
        lambda n: rng.poisson(lam, size=n).astype(float),
    )
    rate = 1.5  # scipy's expon uses scale = 1/rate
    yield (
        "exponential",
        stats.expon(scale=1 / rate),
        1 / rate,
        1 / rate**2,
        lambda n: rng.exponential(1 / rate, size=n),
    )
    a, b = 2.0, 5.0
    yield (
        "beta",
        stats.beta(a, b),
        a / (a + b),
        a * b / ((a + b) ** 2 * (a + b + 1)),
        lambda n: rng.beta(a, b, size=n),
    )
    mu, sigma = 1.0, 2.0
    yield ("normal", stats.norm(mu, sigma), mu, sigma**2, lambda n: rng.normal(mu, sigma, size=n))


DISTS = list(_distributions())


@pytest.mark.parametrize("name,dist,mean,var,sampler", DISTS, ids=[d[0] for d in DISTS])
def test_distribution_mean_matches_scipy_and_monte_carlo(name, dist, mean, var, sampler):
    # 1) analytic formula vs scipy's own computation (exact).
    assert np.isclose(mean, dist.mean(), atol=ATOL_EXACT, rtol=1e-10)
    # 2) analytic formula vs Monte-Carlo estimate (sampling tolerance).
    samples = sampler(MC_SAMPLES)
    assert np.isclose(mean, samples.mean(), atol=mc_atol(np.sqrt(var)))


@pytest.mark.parametrize("name,dist,mean,var,sampler", DISTS, ids=[d[0] for d in DISTS])
def test_distribution_variance_matches_scipy_and_monte_carlo(name, dist, mean, var, sampler):
    assert np.isclose(var, dist.var(), atol=ATOL_EXACT, rtol=1e-10)
    samples = sampler(MC_SAMPLES)
    assert np.isclose(var, samples.var(), atol=mc_atol_variance(np.sqrt(var)))


def test_binomial_to_poisson_limit():
    """Binomial(n, lambda/n) -> Poisson(lambda) pointwise as n grows.

    A classic distributional identity, checked by pmf convergence at fixed k.
    """
    lam = 3.0
    ks = np.arange(0, 8)
    poisson_pmf = stats.poisson(lam).pmf(ks)
    prev_err = np.inf
    for n in (50, 200, 1000, 5000):
        binom_pmf = stats.binom(n, lam / n).pmf(ks)
        err = np.max(np.abs(binom_pmf - poisson_pmf))
        assert err <= prev_err + 1e-12  # monotone (non-increasing) convergence
        prev_err = err
    assert prev_err < 1e-3  # converged closely by n = 5000


# --------------------------------------------------------------------------
# Bayes' theorem & conjugacy
# --------------------------------------------------------------------------
def test_bayes_posterior_normalizes_and_matches_definition():
    """Posterior(H|E) = P(E|H)P(H) / sum_H P(E|H)P(H); posteriors sum to 1."""
    priors = np.array([0.2, 0.5, 0.3])
    likelihoods = np.array([0.9, 0.4, 0.1])  # P(E | H_i)
    joint = priors * likelihoods
    evidence = joint.sum()  # law of total probability
    posterior = joint / evidence
    assert np.isclose(posterior.sum(), 1.0, atol=ATOL_EXACT)
    # Independent check of one entry against the scalar Bayes formula.
    expected_h0 = (likelihoods[0] * priors[0]) / evidence
    assert np.isclose(posterior[0], expected_h0, atol=ATOL_EXACT)


def test_beta_bernoulli_conjugacy():
    """Beta(a,b) prior + k successes in n trials => Beta(a+k, b+n-k) posterior.

    Verified by comparing the analytic posterior mean to a grid-computed
    normalized (prior x likelihood) posterior mean -- an independent numeric
    integration, not the conjugate shortcut.
    """
    a, b = 2.0, 3.0
    n, k = 20, 7
    post_a, post_b = a + k, b + (n - k)
    analytic_mean = post_a / (post_a + post_b)

    theta = np.linspace(1e-6, 1 - 1e-6, 200_001)
    prior = stats.beta(a, b).pdf(theta)
    likelihood = theta**k * (1 - theta) ** (n - k)
    unnorm = prior * likelihood
    post = unnorm / np.trapezoid(unnorm, theta)
    numeric_mean = np.trapezoid(theta * post, theta)
    assert np.isclose(analytic_mean, numeric_mean, atol=1e-4)


# --------------------------------------------------------------------------
# Maximum likelihood estimation
# --------------------------------------------------------------------------
def test_gaussian_mle_closed_form_matches_numerical_argmax():
    """MLE(mu, sigma^2) = (sample mean, mean squared deviation).

    Closed form vs an independent grid/scipy maximization of the log-likelihood.
    """
    rng = seeded_rng(1)
    data = rng.normal(2.0, 1.5, size=5000)
    mu_hat = data.mean()
    var_hat = data.var()  # biased /n estimator, which is the MLE

    # Independent check: the closed form must be a stationary point of the
    # log-likelihood, i.e. the score (d/dmu, d/dsigma^2) vanishes there.
    def neg_loglik(params):
        mu, log_var = params
        var = np.exp(log_var)
        return 0.5 * (np.log(2 * np.pi * var) + ((data - mu) ** 2 / var)).sum()

    from scipy.optimize import minimize

    res = minimize(
        neg_loglik,
        x0=[0.0, 0.0],
        method="Nelder-Mead",
        options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 10000},
    )
    mu_opt, var_opt = res.x[0], np.exp(res.x[1])
    assert np.isclose(mu_hat, mu_opt, atol=1e-3)
    assert np.isclose(var_hat, var_opt, rtol=2e-3)


def test_cramer_rao_variance_of_gaussian_mean_mle():
    """Var(mu_hat) ~ sigma^2 / n = 1 / (n * Fisher info), verified by Monte-Carlo.

    Fisher information for the mean of a Normal with known sigma is I(mu) = 1/sigma^2,
    so the Cramer-Rao bound (achieved by the sample-mean MLE) is sigma^2/n.
    """
    rng = seeded_rng(2)
    sigma, n, trials = 2.0, 100, 20_000
    estimates = rng.normal(0.0, sigma, size=(trials, n)).mean(axis=1)
    empirical_var = estimates.var()
    crb = sigma**2 / n
    # empirical_var is itself an estimate; its own standard error is
    # crb * sqrt(2/trials). Allow 6 of those.
    tol = 6 * crb * np.sqrt(2 / trials)
    assert np.isclose(empirical_var, crb, atol=tol)


# --------------------------------------------------------------------------
# Expectation identities
# --------------------------------------------------------------------------
def test_linearity_of_expectation_holds_even_under_dependence():
    """E[aX + bY] = a E[X] + b E[Y] regardless of correlation between X and Y."""
    rng = seeded_rng(3)
    # Correlated X, Y via a shared latent, so this isn't trivially independent.
    z = rng.normal(size=MC_SAMPLES)
    x = 2 * z + rng.normal(size=MC_SAMPLES)
    y = -z + 0.5 * rng.normal(size=MC_SAMPLES)
    a, b = 1.5, -2.0
    lhs = (a * x + b * y).mean()
    rhs = a * x.mean() + b * y.mean()
    # Both sides are the SAME samples rearranged, so this is exact up to round-off.
    assert np.isclose(lhs, rhs, atol=1e-9)


def test_variance_identity_matches_moment_definition():
    """Var(X) = E[X^2] - E[X]^2, checked on samples and against the closed form."""
    rng = seeded_rng(4)
    lam = 4.0
    x = rng.poisson(lam, size=MC_SAMPLES).astype(float)
    var_via_identity = (x**2).mean() - x.mean() ** 2
    assert np.isclose(var_via_identity, x.var(), atol=1e-9)  # algebraic identity, exact
    # And both track the analytic Poisson variance (= lam) within sampling error.
    assert np.isclose(x.var(), lam, atol=mc_atol_variance(np.sqrt(lam)))
