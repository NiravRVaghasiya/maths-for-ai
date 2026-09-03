"""Command-line entry point for the notebook reproducibility audit.

Usage (from the repo root, with the audit venv active):

    python -m notebook_audit --help
    python -m notebook_audit                          # run everything
    python -m notebook_audit --module 08_Advanced_Linear_Algebra
    python -m notebook_audit --notebook 08_Advanced_Linear_Algebra/02_matrix_calculus.ipynb
    python -m notebook_audit --check-determinism      # double-run diff instead of single pass/fail
    python -m notebook_audit --fail-fast

Exit codes: 0 if every notebook passed (and, under --check-determinism,
every notebook was reproducible), 1 otherwise. This is what CI checks.
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import List, Optional

from .classifier import Finding, classify_result
from .discovery import NotebookRef, discover_notebooks, repo_root, representative_notebooks
from .executor import DEFAULT_CELL_TIMEOUT_S, DEFAULT_NOTEBOOK_TIMEOUT_S, execute_notebook
from .reporting import (
    RunRecord,
    build_run_record,
    write_json_report,
    write_junit_report,
    write_markdown_report,
)
from .reproducibility import compare_runs
from .static_checks import scan_notebook_source


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute and audit maths-for-ai notebooks.")
    parser.add_argument(
        "--module",
        action="append",
        dest="modules",
        help="Restrict to one module directory (repeatable). Default: all modules.",
    )
    parser.add_argument(
        "--notebook",
        action="append",
        dest="notebooks",
        help="Restrict to one notebook, given as a path relative to the repo root (repeatable).",
    )
    parser.add_argument(
        "--representative",
        action="store_true",
        help="Run only one representative notebook per module (the first by number). "
        "Used by the fast PR CI tier for broad, cheap coverage; the full suite runs "
        "in the scheduled/nightly tier. Combine with --module to restrict further.",
    )
    parser.add_argument(
        "--seed", type=int, default=0, help="Deterministic seed to inject (default: 0)."
    )
    parser.add_argument(
        "--cell-timeout",
        type=int,
        default=DEFAULT_CELL_TIMEOUT_S,
        help=f"Per-cell timeout in seconds (default: {DEFAULT_CELL_TIMEOUT_S}).",
    )
    parser.add_argument(
        "--notebook-timeout",
        type=int,
        default=DEFAULT_NOTEBOOK_TIMEOUT_S,
        help=f"Whole-notebook wall-clock timeout in seconds (default: {DEFAULT_NOTEBOOK_TIMEOUT_S}).",
    )
    parser.add_argument(
        "--kernel-name",
        default="python3",
        help="Jupyter kernel name to execute under (default: python3). "
        "Use the audit venv's registered kernel name if it differs.",
    )
    parser.add_argument(
        "--fail-fast", action="store_true", help="Stop at the first failing notebook."
    )
    parser.add_argument(
        "--check-determinism",
        action="store_true",
        help="Run every selected notebook TWICE and diff numeric stdout output "
        "instead of doing a single pass/fail run.",
    )
    parser.add_argument(
        "--report-dir",
        default="reports/notebook_audit",
        help="Directory (relative to repo root) to write JSON/Markdown/JUnit reports into.",
    )
    parser.add_argument(
        "--no-inject-seed",
        action="store_true",
        help="Do not inject the determinism seed cell (execute notebooks exactly as authored).",
    )
    return parser.parse_args(argv)


def _select_notebooks(args: argparse.Namespace) -> List[NotebookRef]:
    root = repo_root()
    if args.notebooks:
        if args.representative:
            raise SystemExit("--representative cannot be combined with --notebook.")
        refs = []
        all_refs = {ref.relative_path: ref for ref in discover_notebooks(root=root)}
        for requested in args.notebooks:
            normalized = requested.replace("\\", "/")
            if normalized not in all_refs:
                raise SystemExit(f"Notebook not found in curriculum: {requested}")
            refs.append(all_refs[normalized])
        return refs
    if args.representative:
        return representative_notebooks(modules=args.modules, root=root)
    return discover_notebooks(modules=args.modules, root=root)


def _run_single_pass(refs: List[NotebookRef], args: argparse.Namespace) -> List[RunRecord]:
    records: List[RunRecord] = []
    for i, ref in enumerate(refs, start=1):
        print(f"[{i}/{len(refs)}] Executing {ref.notebook_id} {ref.relative_path} ...", flush=True)
        result = execute_notebook(
            ref,
            seed=args.seed,
            cell_timeout_s=args.cell_timeout,
            notebook_timeout_s=args.notebook_timeout,
            kernel_name=args.kernel_name,
            inject_seed=not args.no_inject_seed,
        )
        findings: List[Finding] = classify_result(result)
        findings.extend(
            scan_notebook_source(
                ref.path, notebook_id=ref.notebook_id, relative_path=ref.relative_path
            )
        )
        record = build_run_record(ref, result, findings)
        records.append(record)

        status_label = "PASS" if record.passed else f"FAIL ({record.status})"
        print(f"    -> {status_label} in {result.duration_s:.1f}s", flush=True)
        if not record.passed:
            for f in record.fail_findings:
                print(f"       [{f.category}] {f.message}", flush=True)
            if args.fail_fast:
                print("--fail-fast set, stopping.", flush=True)
                break
    return records


def _run_determinism_pass(refs: List[NotebookRef], args: argparse.Namespace) -> List[RunRecord]:
    records: List[RunRecord] = []
    for i, ref in enumerate(refs, start=1):
        print(
            f"[{i}/{len(refs)}] Determinism check for {ref.notebook_id} {ref.relative_path} ...",
            flush=True,
        )
        result_a = execute_notebook(
            ref,
            seed=args.seed,
            cell_timeout_s=args.cell_timeout,
            notebook_timeout_s=args.notebook_timeout,
            kernel_name=args.kernel_name,
            inject_seed=not args.no_inject_seed,
        )
        result_b = execute_notebook(
            ref,
            seed=args.seed,
            cell_timeout_s=args.cell_timeout,
            notebook_timeout_s=args.notebook_timeout,
            kernel_name=args.kernel_name,
            inject_seed=not args.no_inject_seed,
        )

        findings: List[Finding] = classify_result(result_a)
        base_status = result_a.status

        if result_a.status == "pass" and result_b.status == "pass":
            diff = compare_runs(ref.notebook_id, ref.relative_path, result_a, result_b)
            if not diff.is_reproducible:
                base_status = "fail"
                findings.append(
                    Finding(
                        category="reproducibility",
                        severity="fail",
                        message=f"Notebook produced different numeric output across two runs "
                        f"with the same seed ({diff.diff_count} differing line(s)).",
                        detail="\n".join(f"RUN1: {a}\nRUN2: {b}" for a, b in diff.sample_diffs),
                    )
                )

        record = RunRecord(
            notebook_id=ref.notebook_id,
            module=ref.module,
            relative_path=ref.relative_path,
            status=base_status,
            duration_s=result_a.duration_s + result_b.duration_s,
            findings=findings,
        )
        records.append(record)
        print(
            f"    -> {'REPRODUCIBLE' if record.passed else 'NOT REPRODUCIBLE / FAILED'}", flush=True
        )
        if args.fail_fast and not record.passed:
            break
    return records


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)
    refs = _select_notebooks(args)
    if not refs:
        print("No notebooks matched the given selection.", file=sys.stderr)
        return 1

    start = time.monotonic()
    if args.check_determinism:
        records = _run_determinism_pass(refs, args)
    else:
        records = _run_single_pass(refs, args)
    total_time = time.monotonic() - start

    root = repo_root()
    report_dir = root / args.report_dir
    write_json_report(records, report_dir / "report.json")
    write_markdown_report(records, report_dir / "report.md")
    write_junit_report(records, report_dir / "junit.xml")

    n_passed = sum(1 for r in records if r.passed)
    print()
    print(f"{'=' * 60}")
    print(f"{n_passed}/{len(records)} notebooks passed in {total_time:.1f}s")
    print(f"Reports written to {report_dir}")
    print(f"{'=' * 60}")

    return 0 if n_passed == len(records) else 1


if __name__ == "__main__":
    sys.exit(main())
