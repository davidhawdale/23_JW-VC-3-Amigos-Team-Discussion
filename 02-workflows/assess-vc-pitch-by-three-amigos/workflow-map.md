# Assess VC Pitch by Three Amigos: Workflow Map

```mermaid
flowchart TD
    A[Input: 03-inputs/vc-pitch.md] --> P0
    B[Input: 00-brief/strategic-research-brief.md] --> P0
    C[Input: 10-resources/templates/three-amigos-output-template.md] --> P3

    P0[Phase 0: prepare.py] -->|PASS manifest| TC[TeamCreate: ux-researcher, engineer, product-manager]
    P0 -->|FAIL| R0[Stop: fix missing inputs]

    TC --> D1[SendMessage → ux-researcher: mode=independent]
    TC --> D2[SendMessage → engineer: mode=independent]
    TC --> D3[SendMessage → product-manager: mode=independent]

    D1 --> F11[phase1-independent/ux-review.md]
    D2 --> F12[phase1-independent/engineering-review.md]
    D3 --> F13[phase1-independent/pm-review.md]

    F11 & F12 & F13 --> RD1[SendMessage × 3: ROUND 1 — initial reactions]
    RD1 --> RD2[SendMessage × 3: ROUND 2 — cross-reactions]
    RD2 --> RD3[SendMessage × 3: ROUND 3 — final positions]
    RD3 --> TR[discussion-transcript.md]

    TR --> CON[SendMessage × 3: CONSOLIDATE — write phase2 files]
    CON --> F21[phase2-discussion/ux-response.md]
    CON --> F22[phase2-discussion/engineering-response.md]
    CON --> F23[phase2-discussion/pm-response.md]

    A --> P3[Phase 3: three-amigos-synthesizer]
    B --> P3
    C --> P3
    F11 & F12 & F13 --> P3
    F21 & F22 & F23 --> P3
    TR --> P3

    P3 --> O[Output: 05-outputs/assess-vc-pitch-by-three-amigos.md]

    O --> V[Phase 4: verify.py]
    V -->|PASS| TD[TeamDelete]
    TD --> DONE[Phase 5: report completion]
    V -->|FAIL too long| RETRY1[Re-run synthesizer with stricter length]
    V -->|FAIL missing sections| RETRY2[Re-run synthesizer with template emphasis]
    RETRY1 & RETRY2 --> P3
```

## Automated Validations and Tests

### Phase 0 (`prepare.py`)

- Checks `03-inputs/vc-pitch.md` exists.
- Checks `00-brief/strategic-research-brief.md` exists.
- Creates:
  - `04-process/three-amigos-reviews/phase1-independent/`
  - `04-process/three-amigos-reviews/phase2-discussion/`
- Emits `FAIL` with issues list if required inputs are missing.

### Phase 4 (`verify.py`) on final output

- Output file exists.
- Word count is between `500` and `2500`.
- Required sections exist:
  - `## Executive Summary`
  - `## Desirability Assessment`
  - `## Feasibility Assessment`
  - `## Viability Assessment`
  - `## Cross-Cutting Tensions`
  - `## Consensus Recommendations`
- Consensus recommendations count is `<= 5`.
- Emits JSON report with:
  - `status`
  - `word_count`
  - `max_words`
  - `page_estimate`
  - `issues`

## Orchestrator Gate Checks

- All 3 Phase 1 files exist in `phase1_folder`.
- Discussion transcript exists with Rounds 1, 2, and 3.
- All 3 Phase 2 files exist in `phase2_folder`.
- Re-run only failed reviewer agents in Phase 1.
- Re-run only failed SendMessage calls in Phase 2 rounds.
