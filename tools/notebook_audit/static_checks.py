"""Static (pre-execution) source scans.

Some failure categories the audit must detect are risks even when the
notebook happens to execute successfully on the audit machine -- a
hardcoded absolute path might exist on the auditor's laptop and nowhere
else. These checks scan notebook *source* (not execution output) and are
run regardless of the notebook's pass/fail execution status.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

import nbformat

from .classifier import CAT_FILESYSTEM_ASSUMPTION, SEVERITY_WARN, Finding

# Absolute-path patterns for the three OS families a learner might run this
# on: Windows drive-letter paths, POSIX home dirs, and POSIX /tmp writes.
_ABS_PATH_PATTERNS = [
    re.compile(r"[\"']([A-Za-z]:\\\\?[^\"']*)[\"']"),  # "C:\Users\..." or "C:\\Users\\..."
    re.compile(r"[\"'](/home/[^\"']*)[\"']"),
    re.compile(r"[\"'](/Users/[^\"']*)[\"']"),
    re.compile(r"[\"'](/tmp/[^\"']*)[\"']"),
]

_FILE_WRITE_CALL_RE = re.compile(
    r"\bopen\([^)]*[\"'][rwa]\+?b?[\"']|\.to_csv\(|\.savefig\(|\.save\(|os\.makedirs\(|os\.mkdir\("
)

# os.getcwd() / relative "./" assumptions that only work if the working
# directory happens to be the notebook's own folder are common but usually
# benign in this repo (papermill/jupyter both default cwd to the notebook's
# location) -- still worth surfacing as an informational warning per the
# audit's "filesystem assumptions" requirement, distinct from a hard failure.
_CWD_ASSUMPTION_RE = re.compile(r"os\.getcwd\(\)|Path\(\.\)|Path\(\"\.\"\)|Path\('\.'\)")


@dataclass
class StaticFinding:
    notebook_id: str
    relative_path: str
    finding: Finding


def scan_notebook_source(nb_path: Path, *, notebook_id: str, relative_path: str) -> List[Finding]:
    """Scan one notebook's source text (all cells) for filesystem assumptions.

    Only code cells are scanned. Markdown cells routinely contain
    Colab-badge URLs and GitHub blob links that look like paths but are not
    filesystem operations, so they are intentionally excluded to avoid noise.
    """
    nb = nbformat.read(str(nb_path), as_version=4)
    findings: List[Finding] = []

    for index, cell in enumerate(nb.cells):
        if cell.get("cell_type") != "code":
            continue
        source = str(cell.get("source", ""))

        for pattern in _ABS_PATH_PATTERNS:
            for match in pattern.finditer(source):
                findings.append(
                    Finding(
                        category=CAT_FILESYSTEM_ASSUMPTION,
                        severity=SEVERITY_WARN,
                        message=f"Hardcoded absolute path literal found: {match.group(1)!r}",
                        cell_index=index,
                    )
                )

        if _FILE_WRITE_CALL_RE.search(source):
            findings.append(
                Finding(
                    category=CAT_FILESYSTEM_ASSUMPTION,
                    severity=SEVERITY_WARN,
                    message="Cell writes to the filesystem (open/to_csv/savefig/save/mkdir); "
                    "confirm the target path is relative/temporary and safe under CI.",
                    cell_index=index,
                )
            )

    return findings
