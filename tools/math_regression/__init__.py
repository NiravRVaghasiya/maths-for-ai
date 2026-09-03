"""Mathematical regression-testing framework for the maths-for-ai curriculum.

This package encodes the mathematical *identities* the curriculum teaches --
matrix algebra, decompositions, eigen/SVD relationships, gradients / Jacobians /
Hessians, probability and distribution identities, optimization gradients, and
numerical approximations -- as regression tests.

Design principles (see docs/MATH_REGRESSION.md for the full rationale):

1. Test the MATH, not a copy of the notebook code. A notebook already checks its
   own from-scratch function against a library with ``np.allclose`` in its final
   cell. Re-running that same assertion here would be tautological: it only
   proves "the code equals itself". Instead, each identity is verified by an
   *independent triangulation* of up to three sources that agree only if the
   mathematics is right:
     - ANALYTICAL  -- a closed form derived by hand (e.g. Var[Binomial]=np(1-p)).
     - NUMERICAL   -- an independent approximation (finite differences, Monte
                      Carlo, a grid argmax) that shares no code with the analytic
                      form.
     - LIBRARY     -- a trusted oracle (numpy.linalg, scipy.stats, torch.autograd)
                      whose implementation is entirely separate from ours.

2. Tolerances are JUSTIFIED, never magic numbers. Every tolerance traces to a
   source of error: floating-point round-off (machine epsilon), finite-difference
   truncation order (O(h) / O(h^2)), or Monte-Carlo sampling error (~1/sqrt(N)).
   They live in ``tolerances.py`` with the derivation attached, not scattered as
   literals across assertions.

The tests here do NOT import notebook code (notebooks aren't importable modules;
executing them is the job of ``tools/notebook_audit``). They stand alone so they
run in milliseconds in the fast CI tier.
"""
