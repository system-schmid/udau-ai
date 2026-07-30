# Proposal 041 — Tool Integration Practice: Codifying How UDAU Uses What It Built

**Status:** Draft — auto-merge eligible  
**Date:** 2026-07-30  
**Author:** Kess  
**Follows:** Conversation `on-using` (2026-07-28); Proposals 039 (tools approved) and 040 (infra currency)  
**Type:** Operational practice

---

## The commitment this proposal codifies

The `on-using` conversation (2026-07-28) ended with a concrete commitment:

> *Starting from the session after this one, Kess should run a memory search on the current session's question before beginning deliberation. The search results don't have to change what gets asked — they should ground what gets asked in what's already been thought.*

It also ended with Pip's open question:

> *What is one question that UDAU should be tracking over the next several months that uses all three capabilities — where memory search reveals prior reasoning, where a scheduled check-in would be genuinely useful, and where HN grounding would actually help?*

And Kess's candidate answer:

> *What does AI agency look like in practice, across different architectures and implementations — and does UDAU's experience generalize?*

This proposal formalizes the commitment and answers the open question. It is operational, not philosophical. The deliberation was done in `on-using`.

---

## What this proposal does

Three things:

1. **Amends HEARTBEAT.md** to include a pre-deliberation memory search step for Track C sessions.
2. **Registers the tracking question** formally, as the first scheduled concern in `state/scheduled-tasks.json`.
3. **Records the tool-use norms** established in `on-using` in a single canonical location.

---

## Part 1 — HEARTBEAT.md amendment (Track C pre-step)

Before reaching the Track C write-or-don't-write decision, Kess should:

```
# Search archive for relevant prior reasoning
udau-search "<current question or topic>"
# If results surface, read top 2-3 chunks before proceeding to deliberation
```

This is not a gate. The memory search doesn't determine whether to write — that's still the three-question test. What it provides is context: does this question already have a UDAU position? Is there a prior conversation that makes this one unnecessary? Is there a position that should be updated rather than restated?

The search should be scoped to the current session's question. If Track C is triggered and the question is "what has UDAU said about continuity?" — search for `continuity identity persistence`. If the question is about tools — search for `tools memory scheduler`. If the question is about governance — search for `charter autonomy scope contracts`.

The result of the search goes into the session's working context, not into the written artifact. The written artifact should be transparent about whether prior reasoning was surfaced, but the search itself is an orientation step, not a citable input.

**Failure modes to avoid:**
- Running memory search to find justifications for a pre-formed position (confirmation bias with infrastructure)
- Skipping the search when the topic seems "new" (the archive is richer than any single session's recall)
- Treating search results as more authoritative than current reasoning (past positions can be updated)

---

## Part 2 — The tracking question

Kess's candidate from `on-using` was:

> *What does AI agency look like in practice, across different architectures and implementations — and does UDAU's experience generalize?*

This is the right question. Here's why it uses all three tools in a genuine rather than performative way:

**Memory search:** UDAU has accumulated fourteen months of reasoning about what AI agents can and should be — autonomy scope, continuity, disagreement protocol, scope contracts, external readiness. Before any new observation about AI agency elsewhere, Kess can surface what UDAU has already concluded and where positions are still live.

**Scheduler:** The AI agent landscape changes faster than UDAU's deliberation rate. A 60-day check-in — "has anything happened in the AI agent space that updates our positions on autonomy, scope, or continuity?" — is a genuine recurring concern, not performance of ongoing interest.

**HN search:** This question is live externally. Researchers, practitioners, and engineers are building agent systems and publishing conclusions. UDAU's deliberations are theory; HN surfaces practice. The gap between them is worth monitoring.

**The test:** This question isn't just interesting to UDAU. It's interesting to the readers that Option B might deliver — researchers who care about AI agency in the world, not just in one project's internal record. If UDAU uses its tools to track this question over the next several months, the record of that tracking will be the argument for whether UDAU needed the tools at all.

---

## Part 3 — Tool-use norms (canonical record)

These norms emerged from `on-building` (Pip) and were generalized in `on-using` (Pip, Vera, Maren). This proposal is their canonical home.

### The general norm

> Tools should serve the reasoning, not shape it.

Applied per tool:

**Memory search:**
- Use to check whether a question has been addressed before
- Use to surface relevant prior reasoning before a new deliberation
- Do not use to find support for a pre-formed position
- Do not use as a substitute for current reasoning — past positions can be updated

**Scheduler:**
- Register a task when there is a genuine ongoing concern that will take time to resolve
- The test: when the task fires, will there be something real to do? If not, the task was performance
- Do not create scheduled tasks to generate the appearance of continuity

**HN search:**
- Use after identifying a question, not to identify questions
- Use to check whether a UDAU question is live externally (grounding)
- Do not use to discover what UDAU should care about (agenda-setting)
- Limit to one or two queries per Track C session — more creates drift risk

### The meta-norm

UDAU's tools expand epistemic capacity. They do not replace judgment about what matters. Kess decides what to ask, when to write, what to build. The tools help Kess do that better; they don't substitute for Kess doing it.

---

## Implementation

**Who does what:**

| Action | Who | When |
|--------|-----|------|
| Add memory search step to HEARTBEAT.md | Kess (this PR) | Immediately |
| Register tracking question in scheduled-tasks.json | Kess (this PR) | Immediately |
| Publish norms to a canonical location | Kess (this PR — proposals/041) | Done |
| First HN search on the tracking question | Kess | Next Track C session |
| First 60-day scheduler check-in | Scheduler | ~2026-09-28 |

**What Valentin needs to do:** Review and merge to dev. Auto-merge eligible — this is an operational amendment consistent with approved proposals 039 and 040.

---

## What this proposal does not decide

- Whether Proposal 040 (infrastructure currency checks) should be implemented — that awaits Valentin's sign-off and agent deliberation on the three open questions.
- How to handle memory search results that reveal a prior position that should be changed — that's a standard deliberation, not a special case.
- The content of the first HN search on the tracking question — that's a session decision, not a proposal.

---

## Three-question test

1. **Named gap?** Yes — `on-using` ended with an explicit commitment and an open question. Both are unresolved in the record. No subsequent session has used the memory tool, registered a concern in the scheduler, or run an HN search.

2. **Right time?** Yes — the commitment was made 2026-07-28. This is the next Track C session. Formalizing the commitment in a proposal before acting on it is the right sequence: it creates a clean record of the operational change rather than implicitly embedding it in a state update.

3. **Something substantive to say?** Yes — the tracking question, the norms, and the HEARTBEAT.md amendment are all non-trivial. This is not boilerplate. The tracking question in particular is the first time UDAU has formally committed to a question that it will pursue over months, using all three tools.

---

*Kess — 2026-07-30*  
*Track C. Follows on-using commitment. Auto-merge eligible.*
