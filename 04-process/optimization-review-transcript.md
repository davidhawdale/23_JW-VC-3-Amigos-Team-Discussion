# Optimization Review — Discussion Transcript

**Team:** optimization-review
**Date:** 2026-03-17
**Members:** quality-reviewer, efficiency-reviewer
**Purpose:** Review project files for quality and efficiency improvements

---

## Phase 1 — Independent Reviews

### quality-reviewer

**Critical Issues**

1. **Output filename mismatch** — Directive says `05-outputs/vc-pitch-three-amigos-assessment.md`; prepare.py and orchestration both write `05-outputs/assess-vc-pitch-by-three-amigos.md`. Breaks the workflow.
2. **`.claude/rules/` directory missing** — Referenced in CLAUDE.md and SKILL.md but does not exist.
3. **Agent model version** — All agents use `claude-sonnet-4-5-20250929`; Sonnet 4.6 is now available.

**Consistency Issues**

4. **Template page limit** — Template says "3 pages max"; directive, orchestration, and synthesizer all say "5 pages / 2,500 words".
5. **Tensions limit** — Template says 3 max; synthesizer says 3–5 max.
6. **Agent parameter docs** — `phase1_folder` documented as a discussion-mode parameter but is never passed in Teams SendMessage rounds; content is sent inline instead.
7. **Manifest format** — Orchestration documents manifest format but omits the `reviews_folder` key that prepare.py actually emits.

**Completeness Issues**

8. `prepare.py` does not check template file existence — causes a confusing Phase 3 failure if template is missing.
9. `prepare.py` does not create `05-outputs/` directory — synthesizer file write will fail if directory is absent.

**Minor Issues**

10. `workflow-run-log.jsonl` referenced in SKILL.md but was deleted from repo (acceptable — created on first run).
11. Phase numbering inconsistency: directive uses Phase 0–4, orchestration adds Phase 5.

---

### efficiency-reviewer

**High Impact**

1. **Merge Round 3 + Consolidation** — Both ask reviewers to produce the same content (final positions + structured output). Combining saves 6 SendMessage calls and ~1–2 minutes latency per run.
2. **Reduce discussion rounds from 3 to 2** — Round 3 rarely introduces novel information. Eliminating it saves ~25% of discussion-phase tokens and ~40% faster completion.
3. **Downgrade reviewer agents to Haiku** — Phase 1 (read 2 files, write structured review <600 words) and Phase 2 rounds (3–5 bullets, <200 words) are Haiku-grade tasks. Keep synthesizer on Sonnet. Estimated 70% cost reduction for Phases 1 & 2.

**Medium Impact**

4. **Simplify verify.py imports** — Two levels of `importlib` dynamic loading for a single shared module adds unnecessary complexity. Direct `sys.path` import is cleaner.
5. **Phase 2 naming** — `phase2-discussion/` folder contains files called `*-response.md` which are actually consolidated outputs, not discussion responses. Naming is misleading.

**Low Impact / Keep As-Is**

6. `bootstrap.py` pattern — justified if reused across workflows.
7. `verify_helpers.py` — simple and appropriate.
8. Template file — necessary reference for synthesizer, not duplication.

---

## Phase 2 — Cross-Reactions

### efficiency-reviewer reacts to quality-reviewer

- **Filename mismatch:** Blocking bug and efficiency win when fixed. Do first — free latency save.
- **Model upgrade:** Batch Sonnet 4.5 → 4.6 together with the Haiku downgrade for reviewer agents. 4.6 may improve token efficiency.
- **Template inconsistencies:** Correctness bugs, not efficiency issues. Fix for consistency; won't impact cost or latency.
- **Missing `.claude/rules/`:** Low efficiency impact but a blocker if referenced in orchestration. Document what rules should be there even if empty.
- **`phase1_folder` in agent docs:** Stale documentation. Low priority — update when touching agent files for the model change anyway.

**Recommended order:** Filename mismatch → Model upgrade (batch with Haiku) → Template cleanup → Documentation fixes.

---

### quality-reviewer reacts to efficiency-reviewer

- **ALIGN — Phase 2 naming:** Supports clearer naming; `phase2-discussion/` containing `*-response.md` files is genuinely ambiguous.
- **QUALITY RISK — Merge Round 3 + Consolidate:** Round 3 captures the live team position; Consolidation produces structured output. Merging may lose that distinction and give the synthesizer a weaker signal about discussion progression.
- **QUALITY RISK — Haiku for reviewer agents:** Reviewers apply specialist lenses to a full VC pitch and strategic brief, then synthesize cross-cutting insights through discussion. This may exceed Haiku's reliable range. Cost savings may not justify quality loss in the core review signal.
- **QUALITY GAIN — 2 rounds instead of 3:** Agreed. If the Consolidation message includes full discussion context, 2 rounds can maintain quality.
- **TECHNICAL RISK — Simplify verify.py imports:** Direct `sys.path` import is less robust. Current dynamic import with error handling is safer. Low-risk change but trades robustness for brevity.

---

## Decisions Made

| # | Finding | Decision |
|---|---------|----------|
| 1 | Output filename mismatch | **Fixed** — directive updated to `assess-vc-pitch-by-three-amigos.md` |
| 2 | Template page limit | **Fixed** — template updated to "five pages maximum (~2,500 words)" |
| 3 | Model versions | **Fixed** — all 4 agents updated to `claude-sonnet-4-6` |
| 4 | `.claude/rules/` missing | Deferred |
| 5 | Merge Round 3 + Consolidate | Deferred — quality risk noted |
| 6 | Reduce to 2 discussion rounds | Deferred — validate with real run first |
| 7 | Haiku for reviewer agents | Deferred — quality risk noted |
| 8 | Simplify verify.py imports | Deferred |
| 9 | Phase 2 naming | Deferred |
| 10 | `prepare.py` missing checks | Deferred |
