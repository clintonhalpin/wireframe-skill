#!/usr/bin/env python3
"""
End-to-end HTML conversion test harness.

Mode A — Validate a single HTML file:
    python3 scripts/test_html_conversion.py examples/hotel-booking.html

Mode B — Validate all examples:
    python3 scripts/test_html_conversion.py --all

Exit code 0 if all files pass (>= 90), 1 otherwise.
"""

import glob
import os
import sys

# Ensure scripts/ is on the path
sys.path.insert(0, os.path.dirname(__file__))

from validate_html import validate_file


EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")
PASS_THRESHOLD = 90


def validate_and_report(filepath, verbose=True):
    """Validate a single HTML file and print results. Returns the report."""
    basename = os.path.basename(filepath)
    report = validate_file(filepath)

    status = "PASS" if report["pass"] else "FAIL"
    score = report["score"]

    if verbose:
        print(f"  {basename}: {score}/100 {status}")

        if not report["pass"]:
            # Show failing checks
            for name, check in report["checks"].items():
                if check["deduction"] > 0:
                    print(f"    {name} (-{check['deduction']}pt):")
                    for issue in check["issues"]:
                        print(f"      - {issue}")

    return report


def mode_single(filepath):
    """Mode A: validate a single HTML file."""
    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        return False

    print(f"Validating: {filepath}")
    report = validate_and_report(filepath)
    print(f"\nScore: {report['score']}/100 {'PASS' if report['pass'] else 'FAIL'}")
    return report["pass"]


def mode_all():
    """Mode B: validate all examples/*.html files."""
    html_files = sorted(glob.glob(os.path.join(EXAMPLES_DIR, "*.html")))

    if not html_files:
        print("No HTML files found in examples/", file=sys.stderr)
        return False

    print(f"Validating {len(html_files)} HTML files in examples/\n")

    all_pass = True
    results = []

    for filepath in html_files:
        report = validate_and_report(filepath)
        results.append((os.path.basename(filepath), report))
        if not report["pass"]:
            all_pass = False

    # Summary
    print(f"\n{'─' * 50}")
    print(f"Results: {sum(1 for _, r in results if r['pass'])}/{len(results)} passed")

    min_score = min(r["score"] for _, r in results) if results else 0
    avg_score = sum(r["score"] for _, r in results) / len(results) if results else 0

    print(f"Min score: {min_score}/100")
    print(f"Avg score: {avg_score:.0f}/100")
    print(f"Threshold: {PASS_THRESHOLD}/100")
    print(f"\n{'PASS' if all_pass else 'FAIL'}")

    return all_pass


def main():
    if len(sys.argv) < 2:
        print("Usage:", file=sys.stderr)
        print("  python3 test_html_conversion.py <file.html>", file=sys.stderr)
        print("  python3 test_html_conversion.py --all", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--all":
        success = mode_all()
    else:
        success = mode_single(sys.argv[1])

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
