"""Shared pytest fixtures for the notebook_audit test suite."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

import pytest

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

# Kernel used to execute fixture notebooks. Must match a kernel actually
# registered on the machine running these tests -- see
# docs/NOTEBOOK_AUDIT.md for the `ipykernel install` command that registers
# it.
#
# Resolution order:
#   1. $NOTEBOOK_AUDIT_TEST_KERNEL, if set (CI sets this to "python3", the
#      kernel name it registers and that every notebook declares).
#   2. "maths-for-ai-audit" -- the distinct name this repo's maintainers use
#      locally to avoid clobbering an unrelated global "python3" kernel (see
#      docs/NOTEBOOK_AUDIT.md, "A note on kernel names").
TEST_KERNEL_NAME = os.environ.get("NOTEBOOK_AUDIT_TEST_KERNEL", "maths-for-ai-audit")


def fixture_path(name: str) -> Path:
    path = FIXTURES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing test fixture: {path}")
    return path


@pytest.fixture(scope="session")
def kernel_name() -> str:
    return TEST_KERNEL_NAME
