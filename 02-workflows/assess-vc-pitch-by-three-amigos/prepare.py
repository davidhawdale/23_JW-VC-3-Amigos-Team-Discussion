#!/usr/bin/env python3
"""
Prepare manifest for the Three Amigos assessment workflow.

Checks that the VC pitch output exists and creates process folders
for the two review phases.

Usage:
    python 02-workflows/assess-vc-pitch-by-three-amigos/prepare.py

Output (stdout): JSON manifest with paths for all review phases.
"""

import json
import os
import sys


def build_manifest() -> dict:
    """Build the Three Amigos assessment manifest."""
    vc_pitch_file = os.path.join("03-inputs", "vc-pitch.md")
    strategic_brief = os.path.join("00-brief", "strategic-research-brief.md")
    template_file = os.path.join(
        "10-resources", "templates", "three-amigos-output-template.md"
    )
    output_file = os.path.join("05-outputs", "assess-vc-pitch-by-three-amigos.md")

    reviews_folder = os.path.join("04-process", "three-amigos-reviews")
    phase1_folder = os.path.join(reviews_folder, "phase1-independent")
    phase2_folder = os.path.join(reviews_folder, "phase2-discussion")

    issues = []

    if not os.path.isfile(vc_pitch_file):
        issues.append(
            f"VC pitch not found: {vc_pitch_file}. "
            "Place vc-pitch.md in 03-inputs/ before running."
        )

    if not os.path.isfile(strategic_brief):
        issues.append(f"Strategic brief not found: {strategic_brief}.")

    if issues:
        print(json.dumps({"status": "FAIL", "issues": issues}, indent=2))
        sys.exit(1)

    os.makedirs(phase1_folder, exist_ok=True)
    os.makedirs(phase2_folder, exist_ok=True)

    reviewers = [
        {
            "role": "ux",
            "agent_name": "ux-reviewer",
            "phase1_output": os.path.join(phase1_folder, "ux-review.md"),
            "phase2_output": os.path.join(phase2_folder, "ux-response.md"),
        },
        {
            "role": "engineering",
            "agent_name": "engineer-reviewer",
            "phase1_output": os.path.join(phase1_folder, "engineering-review.md"),
            "phase2_output": os.path.join(phase2_folder, "engineering-response.md"),
        },
        {
            "role": "pm",
            "agent_name": "pm-reviewer",
            "phase1_output": os.path.join(phase1_folder, "pm-review.md"),
            "phase2_output": os.path.join(phase2_folder, "pm-response.md"),
        },
    ]

    transcript_file = os.path.join(reviews_folder, "discussion-transcript.md")

    return {
        "status": "PASS",
        "vc_pitch_file": vc_pitch_file,
        "strategic_brief": strategic_brief,
        "template_file": template_file,
        "output_file": output_file,
        "transcript_file": transcript_file,
        "reviews_folder": reviews_folder,
        "phase1_folder": phase1_folder,
        "phase2_folder": phase2_folder,
        "reviewers": reviewers,
        "summary": {
            "total_reviewers": len(reviewers),
            "total_phases": 2,
        },
    }


if __name__ == "__main__":
    manifest = build_manifest()
    print(json.dumps(manifest, indent=2))
