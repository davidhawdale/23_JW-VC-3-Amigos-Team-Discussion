# Three Amigos Discussion Transcript

**Participants:** UX Researcher (Desirability), Engineer (Feasibility), Product Manager (Viability)
**Date:** 2026-03-16
**Format:** 3-round live discussion following independent reviews

---

## Round 1 — Initial Reactions

### UX Researcher

**Agreements:**
- Engineer's point on proactive orchestration being "the hardest AI product problem" directly validates my concern about the intrusion/helpfulness balance. Users want this, but getting it wrong kills desirability.
- PM's emphasis on migration friction is critical. Users are tired of re-briefing AI, but they're also anchored to ChatGPT. The desirability advantage only matters if switching cost is low enough.

**Tensions:**
- Engineer flags "trust architecture creates user-facing complexity for non-technical users." This is the core tension. Users WANT granular permissions (6 participants explicitly cited this), but only if it doesn't feel like work. We can't solve desirability by making setup a second job.
- PM says "no GTM strategy" but the research shows users would switch for proactive assistance with trust controls. The desirability signal is strong. The gap is translating that into acquisition mechanics, not whether the product is wanted.

**Question for Both:**
- To Engineer: Can the trust architecture be tiered? Power users get granular controls; cautious users get smart defaults with one-click overrides? Does that break the technical model?
- To PM: Is there evidence in the research about what would actually trigger a switch? The participants said they WOULD switch, but did they describe what event or frustration would make them act?

---

### Engineer

**Agreements:**
- UX is right that trust architecture reflects real demand. The technical primitives exist (OAuth, scoped tokens), so this is implementable.
- PM's GTM and moat concerns are valid from a technical lens too. Memory persistence and proactive orchestration are not proprietary algorithms. If this ships, incumbents can replicate the feature set in 6-9 months. The only durable moat is execution quality and user lock-in through stored context.

**Tensions:**
- UX says "proactive orchestration is positioned correctly" but understates the inference complexity. "Surfaced before they ask" sounds user-friendly, but technically it means predicting intent from incomplete signals without creating notification fatigue. That is an unsolved product-engineering problem, not a positioning choice.
- PM worries about unit economics. I agree and want to quantify it: persistent memory requires vector database reads on every query. Proactive orchestration means background inference runs even when users are idle. At 100k users with daily engagement, that is millions of model calls per month. Can this be profitable at consumer price points?

**Question for the panel:**
- UX: You flagged "verification behavior" as missing from the pitch. I see that as a technical feasibility signal too. If users do not trust outputs enough to use them without verification, does that break the proactive orchestration value prop? Are we building a system people will ignore because they have to double-check everything anyway?

---

### Product Manager

**Agreements:**
- UX Expert is right that persistent memory is the core unmet need. From a business lens, this validates the differentiation hypothesis. If users are frustrated enough to cite this 7 times across 53 interviews, there is real switching motivation.
- Engineer's point about proactive orchestration requiring "inference from incomplete data" is the product risk that will make or break viability. If we cannot solve the intrusion problem the UX Expert flags, users will not adopt, and the business fails.

**Tensions:**
- UX Expert says "positioning is grounded in research evidence showing real willingness to switch" — but willingness to switch in an interview is not the same as actual switching behavior in a winner-take-all market. Stated preference is not revealed preference.
- Engineer correctly identifies that trust architecture creates "user-facing complexity for non-technical users." This is a viability concern, not just a UX concern. If setup friction is high, CAC goes up, conversion goes down, and unit economics collapse.

**Critical question for both:**
- What is the minimum viable differentiation that justifies user migration cost? What is the smallest bundle of features that creates enough switching value to overcome ChatGPT inertia, while staying technically feasible and economically viable?

---

## Round 2 — Cross-Reactions

### UX Researcher

**To Engineer on verification behavior:**
No — it reframes the value prop. Users verify outputs for HIGH-STAKES decisions (financial, medical, legal). But proactive orchestration targets LOW-STAKES tasks: reminders, prep work, household admin. Participants 0010, 0016, 0028, 0037, 0040, 0044, 0050 wanted these surfaced automatically. Verification is about trust in accuracy; proactive help is about reducing cognitive load. Different problem spaces.

**To PM on stated vs. revealed preference:**
Fair pushback. Interview willingness isn't conversion. But the research shows BEHAVIORAL evidence of the pain: 7 participants described actively re-briefing AI every session. That's not hypothetical—that's friction they're experiencing today. The switching trigger is whether persistent memory ACTUALLY eliminates that re-briefing. If it does, revealed preference follows.

**On minimum viable differentiation:**
The smallest bundle is: persistent memory + read-only integrations (calendar, email) + proactive reminders. No execution, no banking, no health. Just "remembers you" + "surfaces what's next." That's enough to eliminate re-briefing and prove the orchestration value without the trust/liability/cost explosion of write access.

**Challenge to Engineer:**
You said "notification fatigue" is unsolved. True—but users already HAVE notification fatigue from their existing tools. The bar isn't "perfect inference." The bar is "better than my phone's current notification chaos." Can background inference beat that low bar with simple heuristics (deadlines, calendar proximity, user-set priorities)?

**Challenge to PM:**
You asked about CAC and conversion. But what if persistent memory creates RETENTION value that changes the economics? If users invest context over time, switching cost to LEAVE increases. That's defensibility through data moats, not feature moats.

---

### Engineer

**On tiered trust architecture (UX question):**
Yes, this is technically feasible and actually reduces implementation risk. Smart defaults (read-only calendar, email) with progressive disclosure of granular controls is a standard onboarding pattern. The technical model stays the same; the UX layer just hides complexity until users need it. This also solves PM's setup friction concern.

**On minimum viable differentiation (PM question):**
From a feasibility lens, the smallest technically credible bundle is: persistent memory (session continuity, preference recall) + read-only integrations (calendar, email context) + transparent evidence trails. Skip proactive orchestration in V1. Memory and context are hard but solvable. Proactive inference is a research problem that will burn runway.

**Challenging PM on "stated vs revealed preference":**
Agree that interview statements are not purchase decisions, but PM is understating the technical advantage of first-mover context lock-in. Once users have 6 months of memory stored in our system, migration cost to a competitor is high even if they ship equivalent features. The stored context becomes the moat, not the algorithm.

**Building on UX verification concern:**
V1 should optimize for verifiable transparency (show sources, explain reasoning, surface confidence levels). V2 adds execution with approval gates. V3 introduces proactive suggestions only after trust is earned through reliability. Trying to ship proactive orchestration before solving verification trust is technically and behaviorally backwards.

---

### Product Manager

**To UX on GTM vs. desirability signal:**
You're right that strong desirability signal exists, but that is necessary, not sufficient. The gap is proving that desirability survives contact with reality. Without a GTM strategy, we cannot test whether stated desire converts to actual switching behavior. VCs will not fund "users told us they would switch."

**To Engineer on moat fragility:**
Agreed that memory and orchestration are replicable in 6-9 months. That timeline is the entire viability case. If we cannot achieve product-market fit, acquire 100k+ users, and create meaningful switching costs (via stored context and integrations) before incumbents ship equivalent features, there is no business.

**To UX on trigger events for switching:**
The research does not provide evidence of trigger events. Users described frustration with re-briefing AI, but frustration tolerance is high when the alternative requires migration effort. We need to know: what is the breaking point that turns stated preference into behavior change?

**To Engineer on unit economics at scale:**
Your cost concern (millions of model calls at 100k users) is the viability blocker. Either we need a premium pricing tier that justifies the compute cost, or we need architectural trade-offs that reduce inference load.

**Challenge to both:**
If trust architecture requires setup friction (Engineer) and users will not switch without a trigger event (UX), how do we cold-start this product? First-time users have no stored context, so memory provides zero value. They must invest setup effort for trust controls before experiencing any benefit. What is the wedge that gets people through that valley?

---

## Round 3 — Final Positions

### UX Researcher

**View Shift:**
Engineer is right that we should ship verification transparency BEFORE proactive orchestration. I flagged verification behavior as missing from the pitch, but I had the sequencing backwards. Persistent memory + verifiable transparency is the wedge that solves PM's cold-start problem. Users get immediate value (no re-briefing + trustable answers) without needing invested context.

**Top Recommendations:**

1. **Reframe the pitch around verification as a core differentiator.** The research shows users actively distrust outputs they cannot verify (5 participants). Position the product as "the AI assistant that shows its work." Persistent memory + transparent evidence trails + source citation is the MVP that differentiates from ChatGPT on day one. This solves desirability (users want this), feasibility (Engineer confirmed it's solvable), and viability (provides immediate value without cold-start friction).

2. **Acknowledge proactive orchestration as a V2 capability, not launch promise.** The pitch currently positions proactive help as core to the value prop, but Engineer is correct that inference from incomplete data is unsolved. Users WANT this (7 participants cited it), but shipping it poorly kills trust faster than not shipping it at all. The pitch should frame proactive orchestration as the long-term vision, with V1 focused on memory + verification that users can rely on today.

**Confidence level:** High. The panel converged on tiered architecture, verification-first sequencing, and data moats through stored context.

---

### Engineer

**View Shift:**
- UX's point about "better than notification chaos" is correct and lowers the feasibility bar for V1. Simple heuristics (calendar proximity, user-set priorities, deadline tracking) are deterministic and cheap to run. Proactive orchestration can be decomposed into dumb-but-useful triggers first, then layered with smarter inference later.
- PM's cold-start challenge is the strongest argument against memory-first positioning. Stored context creates a technical moat, but it provides zero value on day one. This changes the MVP recommendation.

**Top Recommendations:**
1. **Lead with read-only integrations + simple proactive triggers, not memory persistence.** V1 value prop: "Sees your calendar and inbox, surfaces what's next based on deadlines and meetings." Users get immediate utility without setup effort. Memory accrues as a side effect, creating lock-in over time. This solves PM's cold-start wedge and stays within feasible engineering scope.

2. **Deprioritize granular permission architecture in V1.** Ship OAuth-based read-only access with binary on/off switches (connect calendar: yes/no). Defer complex permission scoping until post-PMF. Reduces implementation risk, cuts setup friction, and still addresses core user trust concern. Build the complicated trust layer only after proving users want the product at all.

---

### Product Manager

**View Shifts:**
- Engineer and UX have convinced me that stored context creates a legitimate data moat IF we can get users to invest enough context before incumbents ship competing features. The 6-9 month window is tight, but if we achieve meaningful lock-in through accumulated memory, switching costs favor us even after feature parity. This changes the moat analysis from "fragile" to "viable but execution-dependent."
- UX's point that proactive orchestration targets LOW-STAKES tasks while verification applies to HIGH-STAKES decisions is correct. This supports the phased rollout: V1 solves memory and verifiable transparency; V2 adds low-stakes proactive help; V3 tackles execution with approval gates.

**Top Recommendations:**
1. **V1 scope: Persistent memory + read-only integrations + transparent evidence trails.** The wedge is "finally, an AI that remembers you" with calendar/email context to prove immediate value on day one. GTM story becomes: "Stop re-briefing your AI every day."

2. **Business model: Premium tier from day one.** If unit economics require $20-50/month to cover memory storage and continuous integration syncing, position this as a professional productivity tool, not a consumer chatbot replacement. Target users who already pay for productivity SaaS (Notion, Superhuman, etc.). Free tier provides basic chat; paid tier unlocks memory persistence and integrations.

**Remaining viability risk:**
- GTM strategy is still undefined. Engineer and UX have de-risked the product scope, but "how do we acquire the first 10,000 paying users in 6 months" remains unanswered. Without distribution, even the best product fails.
