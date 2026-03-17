# Three Amigos VC Pitch Assessment

A multi-agent system that stress-tests a VC pitch through a structured panel review using the **DVF framework** (Desirability, Feasibility, Viability). Three specialist AI reviewers independently evaluate the pitch, engage in a live multi-round discussion, then a synthesiser produces a final assessment document.

## How It Works

The system uses a **3-layer architecture** — directives define goals, an orchestrator makes decisions, and execution is split between deterministic Python scripts and specialised sub-agents.

### The Five Phases

| Phase | Description |
| --- | --- |
| **0 — Prepare** | Validates inputs exist, creates output folders, emits a JSON manifest |
| **1 — Independent Reviews** | Three specialists review the pitch blind, in parallel |
| **2 — Live Discussion** | Three rounds of genuine back-and-forth between reviewers via Claude Code Teams |
| **3 — Synthesis** | A synthesiser reads all reviews + discussion transcript, writes the final assessment |
| **4 — Verify** | Checks output constraints (word count, required sections, recommendation limits) |

### The Panel

| Reviewer | Lens | Focus |
| --- | --- | --- |
| **UX Reviewer** | Desirability | Does the pitch reflect what users actually want? |
| **Engineer Reviewer** | Feasibility | Are the technical claims credible? Can it be built? |
| **PM Reviewer** | Viability | Is there a real business with a defensible path to revenue? |

Each reviewer produces an independent review (Phase 1) and a discussion response (Phase 2). The **Three Amigos Synthesiser** then consolidates everything into a structured final assessment.

## Project Structure

```
├── 00-brief/                  # Research scope and context
│   └── strategic-research-brief.md
├── 01-directives/             # What to do and why
│   └── assess-vc-pitch-by-three-amigos.md
├── 02-workflows/              # How to do it
│   ├── assess-vc-pitch-by-three-amigos/
│   │   ├── orchestration.md   # Step-by-step phase instructions
│   │   ├── workflow-map.md    # Mermaid flowchart + validation specs
│   │   ├── prepare.py         # Phase 0 — input validation
│   │   └── verify.py          # Phase 4 — output validation
│   └── shared/                # Shared utilities
├── 03-inputs/                 # The pitch being assessed
│   └── vc-pitch.md
├── 04-process/                # Intermediate artefacts
│   ├── workflow-run-log.jsonl
│   └── three-amigos-reviews/
│       ├── phase1-independent/ # Individual blind reviews
│       ├── phase2-discussion/  # Post-discussion responses
│       └── discussion-transcript.md
├── 05-outputs/                # Final deliverable
│   └── assess-vc-pitch-by-three-amigos.md
├── 10-resources/
│   └── templates/             # Output structure template
└── .claude/
    ├── agents/                # Sub-agent definitions
    │   ├── ux-reviewer/
    │   ├── engineer-reviewer/
    │   ├── pm-reviewer/
    │   └── three-amigos-synthesizer/
    ├── skills/
    │   └── run-workflow/      # /run-workflow skill
    └── watch-agent.sh         # Stream agent output to terminal (requires jq)
```

## Running the Workflow

```
/run-workflow assess-vc-pitch-by-three-amigos
```

This triggers the full five-phase pipeline. The skill reads the directive, executes each phase per the orchestration file, logs the result, and cleans up.

### Watching agents work in real time

When the orchestrator launches background agents, it will post watch commands to paste into your terminal. To see each agent's output live:

**1. Split the VS Code terminal into panes**

Open the VS Code terminal panel and press `Cmd+\` (Mac) or `Ctrl+Shift+5` (Windows/Linux) to split it. Repeat for as many agents as are running — typically 2–3 panes.

**2. Paste the watch command into each pane**

The orchestrator will give you a command per agent, like:

```bash
.claude/watch-agent.sh "Quality Reviewer" /private/tmp/claude-501/.../tasks/abc123.output
```

The script waits for the output file to appear, then streams the agent's thinking and tool calls in plain text as it works.

**3. Watch side by side**

Each pane shows one agent. You'll see their reasoning, which files they're reading, and their conclusions as they happen.

The helper script lives at `.claude/watch-agent.sh`. It requires `jq` (`brew install jq` if not already installed).

### Prerequisites

- **Claude Code** with the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` flag enabled (configured in `.claude/settings.json`)
- Python 3 (standard library only — no external dependencies)
- Input files in place: `03-inputs/vc-pitch.md` and `00-brief/strategic-research-brief.md`

## Output

The final assessment is written to `05-outputs/assess-vc-pitch-by-three-amigos.md`. It follows a structured template:

1. **Executive Summary** — overall verdict
2. **Desirability Assessment** — strengths, concerns, recommendations
3. **Feasibility Assessment** — technical credibility analysis
4. **Viability Assessment** — business model and market analysis
5. **Cross-Cutting Tensions** — genuine disagreements between reviewers (max 3)
6. **Consensus Recommendations** — prioritised actions (max 5)

Constrained to ~2,500 words (~5 pages), bullet-point format.

## Architecture

The 3-layer architecture separates concerns:

- **Layer 1 (Directive):** Defines goals, inputs, and acceptance criteria. Human-readable cover sheets.
- **Layer 2 (Orchestration):** The AI orchestrator reads directives and makes decisions — calling scripts and agents in the right order, handling errors, and self-annealing when things break.
- **Layer 3 (Execution):** Deterministic Python scripts handle validation and verification. Sub-agents handle tasks requiring judgement (reviewing, discussing, synthesising).

This design pushes precision work into deterministic code and uses LLM agents where judgement adds value, avoiding the compounding error problem of chaining probabilistic steps.
