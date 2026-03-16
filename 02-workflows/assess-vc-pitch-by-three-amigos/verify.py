#!/usr/bin/env python3
"""
Verify the Three Amigos assessment output meets constraints.

Checks that the output file exists, has required sections,
and stays within the 5-page word limit (~2500 words).

Usage:
    python 02-workflows/assess-vc-pitch-by-three-amigos/verify.py <output_file>

Output (stdout): JSON verification report with pass/fail status.

Exit codes:
    0 — all checks passed
    1 — one or more checks failed
"""

import json
import os
import re
import sys
import importlib.util
from pathlib import Path


def _load_bootstrap():
    bootstrap_path = Path(__file__).resolve().parents[1] / "shared" / "bootstrap.py"
    spec = importlib.util.spec_from_file_location("workflow_bootstrap", str(bootstrap_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load bootstrap helper at {bootstrap_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BOOTSTRAP = _load_bootstrap()

MAX_WORDS = 2500
MIN_WORDS = 500


def verify(output_file: str) -> dict:
    """Run all verification checks on the Three Amigos assessment output."""
    issues = []
    verify_helpers = BOOTSTRAP.import_shared(__file__, "verify_helpers")

    if not verify_helpers.file_exists(output_file):
        return {
            "status": "FAIL",
            "issues": [f"Output file does not exist: {output_file}"],
            "word_count": 0,
        }

    content = verify_helpers.read_text(output_file)

    word_count = verify_helpers.word_count(content)

    if word_count < MIN_WORDS:
        issues.append(
            f"Too short: {word_count} words (minimum {MIN_WORDS})"
        )

    if word_count > MAX_WORDS:
        issues.append(
            f"Too long: {word_count} words (maximum {MAX_WORDS}). "
            f"Must fit within 5 pages."
        )

    required_sections = [
        "## Executive Summary",
        "## Desirability Assessment",
        "## Feasibility Assessment",
        "## Viability Assessment",
        "## Cross-Cutting Tensions",
        "## Consensus Recommendations",
    ]
    missing_sections = verify_helpers.missing_headings(content, required_sections)
    if missing_sections:
        issues.append(
            f"Missing sections: {', '.join(missing_sections)}"
        )

    recommendations_match = re.search(
        r"## Consensus Recommendations\s*\n([\s\S]*?)(?:\n## |\Z)", content
    )
    if recommendations_match:
        rec_text = recommendations_match.group(1)
        bullet_count = len(re.findall(r"^\s*(?:\d+\.|[-*])\s", rec_text, re.MULTILINE))
        if bullet_count > 5:
            issues.append(
                f"Too many consensus recommendations: {bullet_count} (maximum 5)"
            )

    page_estimate = round(word_count / 500, 1)

    report = {
        "status": "PASS" if not issues else "FAIL",
        "word_count": word_count,
        "max_words": MAX_WORDS,
        "page_estimate": page_estimate,
        "issues": issues,
    }

    return report


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python 02-workflows/assess-vc-pitch-by-three-amigos/verify.py "
            "<output_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    report = verify(sys.argv[1])
    print(json.dumps(report, indent=2))

    sys.exit(0 if report["status"] == "PASS" else 1)
