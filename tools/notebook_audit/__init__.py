"""Reproducibility audit tooling for the maths-for-ai notebook curriculum.

This package executes every notebook in the curriculum in a fresh kernel,
classifies any failures into actionable categories, and produces
machine-readable (JSON, JUnit XML) and human-readable (Markdown) reports.

See tools/notebook_audit/README.md (or docs/NOTEBOOK_AUDIT.md at the repo
root) for usage.
"""

__version__ = "1.0.0"
