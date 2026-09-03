"""Report generation: JSON, Markdown, and JUnit XML.

Every report format is derived from the same in-memory list of
:class:`RunRecord` objects, so the three outputs can never disagree with
each other about a given run's outcome.
"""

from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List
from xml.sax.saxutils import escape

from .classifier import SEVERITY_FAIL, Finding
from .discovery import NotebookRef
from .executor import NotebookResult


@dataclass
class RunRecord:
    """Everything the reports need about one executed notebook."""

    notebook_id: str
    module: str
    relative_path: str
    status: str  # "pass" | "fail" | "timeout" | "error"
    duration_s: float
    findings: List[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == "pass" and not any(f.severity == SEVERITY_FAIL for f in self.findings)

    @property
    def fail_findings(self) -> List[Finding]:
        return [f for f in self.findings if f.severity == SEVERITY_FAIL]

    @property
    def warn_findings(self) -> List[Finding]:
        return [f for f in self.findings if f.severity != SEVERITY_FAIL]


def build_run_record(
    ref: NotebookRef, result: NotebookResult, findings: List[Finding]
) -> RunRecord:
    return RunRecord(
        notebook_id=ref.notebook_id,
        module=ref.module,
        relative_path=ref.relative_path,
        status=result.status,
        duration_s=result.duration_s,
        findings=findings,
    )


def _environment_info() -> Dict[str, str]:
    info = {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    for pkg in ("numpy", "torch", "scipy", "matplotlib", "sklearn"):
        try:
            module = __import__(pkg)
            info[f"{pkg}_version"] = getattr(module, "__version__", "unknown")
        except ImportError:
            info[f"{pkg}_version"] = "not installed"
    return info


def write_json_report(records: List[RunRecord], out_path: Path) -> None:
    payload = {
        "environment": _environment_info(),
        "summary": _summary_dict(records),
        "notebooks": [
            {
                "notebook_id": r.notebook_id,
                "module": r.module,
                "relative_path": r.relative_path,
                "status": r.status,
                "duration_s": round(r.duration_s, 2),
                "passed": r.passed,
                "findings": [asdict(f) for f in r.findings],
            }
            for r in records
        ],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _summary_dict(records: List[RunRecord]) -> Dict[str, object]:
    total = len(records)
    passed = sum(1 for r in records if r.passed)
    by_category: Dict[str, int] = {}
    for r in records:
        for f in r.fail_findings:
            by_category[f.category] = by_category.get(f.category, 0) + 1
    warn_by_category: Dict[str, int] = {}
    for r in records:
        for f in r.warn_findings:
            warn_by_category[f.category] = warn_by_category.get(f.category, 0) + 1
    return {
        "total_notebooks": total,
        "passed": passed,
        "failed": total - passed,
        "fail_categories": by_category,
        "warn_categories": warn_by_category,
        "total_duration_s": round(sum(r.duration_s for r in records), 1),
    }


def write_markdown_report(records: List[RunRecord], out_path: Path) -> None:
    summary = _summary_dict(records)
    env = _environment_info()
    lines: List[str] = []
    lines.append("# Notebook Reproducibility Audit Report")
    lines.append("")
    lines.append(f"Generated: {env['timestamp_utc']}")
    lines.append("")
    lines.append("## Environment")
    lines.append("")
    lines.append("| Package | Version |")
    lines.append("|---|---|")
    lines.append(f"| Python | {env['python_version']} |")
    for pkg in ("numpy", "torch", "scipy", "matplotlib", "sklearn"):
        lines.append(f"| {pkg} | {env.get(pkg + '_version', 'unknown')} |")
    lines.append(f"| Platform | {env['platform']} |")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total notebooks:** {summary['total_notebooks']}")
    lines.append(f"- **Passed:** {summary['passed']}")
    lines.append(f"- **Failed:** {summary['failed']}")
    lines.append(f"- **Total execution time:** {summary['total_duration_s']}s")
    lines.append("")

    if summary["fail_categories"]:
        lines.append("### Failure categories")
        lines.append("")
        lines.append("| Category | Count |")
        lines.append("|---|---|")
        for category, count in sorted(summary["fail_categories"].items(), key=lambda kv: -kv[1]):
            lines.append(f"| {category} | {count} |")
        lines.append("")

    if summary["warn_categories"]:
        lines.append("### Warning categories (did not stop execution)")
        lines.append("")
        lines.append("| Category | Count |")
        lines.append("|---|---|")
        for category, count in sorted(summary["warn_categories"].items(), key=lambda kv: -kv[1]):
            lines.append(f"| {category} | {count} |")
        lines.append("")

    lines.append("## Results by module")
    lines.append("")
    modules = sorted(set(r.module for r in records))
    for module in modules:
        module_records = [r for r in records if r.module == module]
        passed_count = sum(1 for r in module_records if r.passed)
        lines.append(f"### {module} ({passed_count}/{len(module_records)} passed)")
        lines.append("")
        lines.append("| Notebook | Status | Duration | Findings |")
        lines.append("|---|---|---|---|")
        for r in sorted(module_records, key=lambda r: r.notebook_id):
            status_icon = "✅" if r.passed else "❌"
            finding_summary = (
                "; ".join(f"{f.category} ({f.severity})" for f in r.findings) if r.findings else "—"
            )
            lines.append(
                f"| {r.notebook_id} `{Path(r.relative_path).name}` | {status_icon} {r.status} "
                f"| {r.duration_s:.1f}s | {finding_summary} |"
            )
        lines.append("")

    failing = [r for r in records if not r.passed]
    if failing:
        lines.append("## Known issues (failing notebooks, detail)")
        lines.append("")
        for r in failing:
            lines.append(f"### {r.notebook_id} — `{r.relative_path}`")
            lines.append("")
            for f in r.fail_findings:
                lines.append(f"- **[{f.category}]** {f.message}")
                if f.cell_index is not None and f.cell_index >= 0:
                    lines.append(f"  - Cell index: {f.cell_index}")
                if f.detail:
                    detail_preview = f.detail.strip().splitlines()
                    preview = "\n".join(detail_preview[:8])
                    lines.append(f"  - Detail:\n    ```\n    {preview}\n    ```")
            lines.append("")

    warned = [r for r in records if r.passed and r.warn_findings]
    if warned:
        lines.append("## Passing notebooks with warnings")
        lines.append("")
        for r in warned:
            lines.append(f"- **{r.notebook_id}** `{r.relative_path}`:")
            for f in r.warn_findings:
                lines.append(f"  - [{f.category}] {f.message}")
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_junit_report(records: List[RunRecord], out_path: Path) -> None:
    """Write a JUnit XML report, one <testsuite> per module.

    This is what makes CI failures show up as per-notebook annotations in
    GitHub Actions' test-reporting UI, rather than as one opaque "job
    failed" line.
    """
    modules = sorted(set(r.module for r in records))
    suites_xml = []
    for module in modules:
        module_records = sorted(
            [r for r in records if r.module == module], key=lambda r: r.notebook_id
        )
        n_tests = len(module_records)
        n_failures = sum(1 for r in module_records if not r.passed)
        total_time = sum(r.duration_s for r in module_records)

        cases_xml = []
        for r in module_records:
            case = [
                f'    <testcase classname="{escape(module)}" name="{escape(r.notebook_id + " " + Path(r.relative_path).name)}" time="{r.duration_s:.2f}">'
            ]
            if not r.passed:
                fail = r.fail_findings[0] if r.fail_findings else None
                message = escape(fail.message if fail else r.status)
                category = escape(fail.category if fail else r.status)
                detail = escape(fail.detail if fail and fail.detail else "")
                case.append(
                    f'      <failure message="{message}" type="{category}">{detail}</failure>'
                )
            case.append("    </testcase>")
            cases_xml.append("\n".join(case))

        suite = (
            f'  <testsuite name="{escape(module)}" tests="{n_tests}" failures="{n_failures}" '
            f'time="{total_time:.2f}">\n' + "\n".join(cases_xml) + "\n  </testsuite>"
        )
        suites_xml.append(suite)

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<testsuites>\n'
        + "\n".join(suites_xml)
        + "\n</testsuites>\n"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(xml, encoding="utf-8")
