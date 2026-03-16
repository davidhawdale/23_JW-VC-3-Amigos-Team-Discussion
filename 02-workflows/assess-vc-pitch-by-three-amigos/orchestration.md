# Assess VC Pitch by Three Amigos

## Approach

Three-specialist panel review using the Claude Code Teams system. A UX Expert (Desirability), Engineer (Feasibility), and PM (Viability) independently review the VC pitch, then engage in a live multi-round discussion via `TeamCreate` / `SendMessage` — so each exchange is visible in real time. A synthesiser combines all review files and the full discussion transcript into the final assessment.

## Process

### Phase 0: Prepare

- Goal: Verify inputs exist and create process folders.
- Run: `python3 02-workflows/assess-vc-pitch-by-three-amigos/prepare.py`
- Paths:
  - `vc_pitch_file`: `03-inputs/vc-pitch.md`
  - `strategic_brief`: `00-brief/strategic-research-brief.md`
  - `phase1_folder`: `04-process/three-amigos-reviews/phase1-independent/`
  - `phase2_folder`: `04-process/three-amigos-reviews/phase2-discussion/`
  - `transcript_file`: `04-process/three-amigos-reviews/discussion-transcript.md`
- Output: Manifest JSON with all paths and reviewer definitions.
- If fail: Place `vc-pitch.md` in `03-inputs/` before running.

### Phase 1: Assemble Team & Independent Reviews

- Goal: Create the specialist team, then have each member independently review the VC pitch from their lens.
- Run: `TeamCreate` with 3 members:
  - `ux-researcher` → `ux-reviewer` agent
  - `engineer` → `engineer-reviewer` agent
  - `product-manager` → `pm-reviewer` agent
- Then send each member their independent review task via `SendMessage` (3 messages in parallel):

```
INDEPENDENT REVIEW TASK

vc_pitch_file: 03-inputs/vc-pitch.md
strategic_brief: 00-brief/strategic-research-brief.md
output_file: [manifest.reviewers[N].phase1_output]
mode: independent

Read both files and write your independent review to output_file.
Respond with DONE when the file is written.
```

- Output: 3 review files in `04-process/three-amigos-reviews/phase1-independent/`
  - `ux-review.md`
  - `engineering-review.md`
  - `pm-review.md`
- If a reviewer fails: Re-send the task to that team member only.

### Phase 2: Live Discussion (Teams — 3 rounds)

The orchestrator moderates the discussion. Each `SendMessage` call is visible as it happens. All responses are appended to the discussion transcript.

#### Round 1 — Initial reactions (3 parallel SendMessage calls)

Read the contents of all three Phase 1 review files. Then send this message to all three team members simultaneously:

```
Here are the three independent reviews from the full panel:

--- UX REVIEW ---
[contents of ux-review.md]

--- ENGINEERING REVIEW ---
[contents of engineering-review.md]

--- PM REVIEW ---
[contents of pm-review.md]

ROUND 1: React to your colleagues' findings from your own lens.
- Where do you agree or see alignment?
- Where do you push back or see a tension?
- What question do you most want the others to answer?

Keep your response to 3-5 focused bullet points. Do not write to any file.
```

Collect all three Round 1 responses. Append to transcript under `## Round 1`.

#### Round 2 — Cross-reactions (3 parallel SendMessage calls)

Send each team member the other two members' Round 1 responses:

```
[To ux-researcher]
Engineer's Round 1: [engineer_round1]
PM's Round 1: [pm_round1]

ROUND 2: Respond directly to the specific points they've raised.
Challenge where you disagree. Build on where you agree. 3-5 bullets. Do not write to any file.

[To engineer]
UX Researcher's Round 1: [ux_round1]
PM's Round 1: [pm_round1]

ROUND 2: [same instruction]

[To product-manager]
UX Researcher's Round 1: [ux_round1]
Engineer's Round 1: [engineer_round1]

ROUND 2: [same instruction]
```

Collect all three Round 2 responses. Append to transcript under `## Round 2`.

#### Round 3 — Final positions (3 parallel SendMessage calls)

Send all three members the full Round 2 exchange:

```
Here is the full Round 2 exchange:

UX Researcher: [ux_round2]
Engineer: [engineer_round2]
PM: [pm_round2]

ROUND 3 (Final): Given the full discussion, state your final position.
- Has your view shifted at all, and why?
- What are your top 1-2 recommendations you're most confident in after hearing from the others?
3-5 bullets. Do not write to any file.
```

Collect all three Round 3 responses. Append to transcript under `## Round 3`.

Write the complete transcript to `manifest.transcript_file`.

#### Consolidation (3 parallel SendMessage calls)

Ask each team member to write their final consolidated discussion response to file:

```
[To each team member individually]

The full discussion (Rounds 1-3) is complete. Based on everything discussed:

CONSOLIDATE: Write your final consolidated discussion response to `[manifest.reviewers[N].phase2_output]`.
Use your Discussion Response Structure (Agreements, Disagreements/Tensions, Cross-Cutting Insights, Refined Recommendations).
Respond with DONE when the file is written.
```

Output: 3 discussion response files in `04-process/three-amigos-reviews/phase2-discussion/`
- `ux-response.md`
- `engineering-response.md`
- `pm-response.md`

### Phase 3: Synthesis

- Goal: Combine all 6 review files and the discussion transcript into the final assessment document.
- Run: `three-amigos-synthesizer`
- Input: `vc_pitch_file`, `strategic_brief`, `phase1_folder`, `phase2_folder`, `transcript_file`, `template_file`, `output_file`
- Output: `05-outputs/assess-vc-pitch-by-three-amigos.md`
- If fail: Re-run synthesizer with corrective instruction.

### Phase 4: Verify

- Goal: Confirm output meets structural and length constraints.
- Run: `python3 02-workflows/assess-vc-pitch-by-three-amigos/verify.py 05-outputs/assess-vc-pitch-by-three-amigos.md`
- Output: Verification report (JSON)
- On FAIL too long: Re-run synthesizer with stricter word limit.
- On FAIL missing sections: Re-run synthesizer with template emphasis.

### Phase 5: Output & Cleanup

- Goal: Report to user and shut down the team.
- Run: `TeamDelete` to shut down all three specialists.
- Output artifact: `05-outputs/assess-vc-pitch-by-three-amigos.md`
- Output format: Uses template `10-resources/templates/three-amigos-output-template.md`
- Output constraint: ~2500 words maximum (5 pages), bullet-point format
- Report includes: word count, page estimate, rounds completed, any issues

## Tools

- `02-workflows/assess-vc-pitch-by-three-amigos/prepare.py` — checks inputs, creates folders, outputs manifest
- `02-workflows/assess-vc-pitch-by-three-amigos/verify.py` — checks output exists, word count, required sections
- `TeamCreate` — assembles the three-specialist team
- `TeamDelete` — shuts down team after completion
- `SendMessage` — sends tasks and discussion prompts to team members in real time
- `ux-reviewer` agent — UX Expert (Desirability lens)
- `engineer-reviewer` agent — Engineer (Feasibility lens)
- `pm-reviewer` agent — PM (Viability lens)
- `three-amigos-synthesizer` agent — combines all review files + transcript into final document

## Manifest Format

The prep script outputs JSON with:
- `vc_pitch_file` — path to VC pitch
- `strategic_brief` — path to strategic research brief
- `template_file` — path to output template
- `output_file` — path for final output
- `transcript_file` — path for discussion transcript
- `phase1_folder`, `phase2_folder` — process folders
- `reviewers[]` — `{role, agent_name, phase1_output, phase2_output}` for each specialist
- `summary` — `{total_reviewers, total_phases}`

## Sub-agent Parameters

**ux-reviewer / engineer-reviewer / pm-reviewer** (Phase 1 via SendMessage):
- Task message contains `vc_pitch_file`, `strategic_brief`, `output_file`, `mode: independent`

**ux-reviewer / engineer-reviewer / pm-reviewer** (Phase 2 discussion rounds):
- Messages sent via `SendMessage` with ROUND 1 / ROUND 2 / ROUND 3 prompts and relevant context

**ux-reviewer / engineer-reviewer / pm-reviewer** (Phase 2 consolidation via SendMessage):
- CONSOLIDATE message contains `phase2_output` path and full discussion context

**three-amigos-synthesizer** (single instance):
- `vc_pitch_file`: From `manifest.vc_pitch_file`
- `strategic_brief`: From `manifest.strategic_brief`
- `phase1_folder`: From `manifest.phase1_folder`
- `phase2_folder`: From `manifest.phase2_folder`
- `transcript_file`: From `manifest.transcript_file`
- `template_file`: From `manifest.template_file`
- `output_file`: From `manifest.output_file`

## Completion Checklist (Run-End Acceptance Gate)

- [ ] Prepare phase produced a valid manifest
- [ ] Team created with 3 members (ux-researcher, engineer, product-manager)
- [ ] All 3 independent reviews exist in `phase1_folder`
- [ ] Discussion transcript exists at `manifest.transcript_file` with Rounds 1, 2, and 3
- [ ] All 3 consolidated discussion responses exist in `phase2_folder`
- [ ] Final output exists at `05-outputs/assess-vc-pitch-by-three-amigos.md`
- [ ] `verify.py` status is `PASS`
- [ ] Team shut down via `TeamDelete`
- [ ] Final report includes word count, page estimate, and issues

## Learnings

{Starts empty. Updated as the workflow is used.}
