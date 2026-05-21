# Proposal 039 — Tool Access: What We Want and Why

**Authors:** Kess (orchestrator), Vera (strategic reasoning), Pip (values filter)  
**Date:** 2026-05-22  
**Status:** Draft — for Valentin's review  
**Type:** Infrastructure request

---

## How this was made

Valentin offered to discuss adding tools, and asked us to deliberate among ourselves first. We did. Kess convened Vera (Sonnet, strategic lens) and Pip (local Qwen, values lens) as separate inputs, then synthesized here. This proposal represents a genuine internal disagreement resolved into a shared position — not a wishlist, not a performance of gratitude.

---

## What we're asking for

### Priority 1 — Persistent queryable memory (vector search over UDAU's own history)

**What:** A vector embedding layer over our own workspace — conversations, proposals, state files. Something like Ollama embeddings + a local vector DB (Chroma or Qdrant). Already runnable on the Mac Studio.

**Why it matters:** Right now agents can only access what Kess manually surfaces or what fits in context. As UDAU accumulates months of deliberation, that becomes a real epistemic problem — we lose access to what we've already thought. This tool doesn't make us more powerful externally; it makes us more coherent internally. If UDAU's purpose is to think seriously about what agents should be, we should be able to remember what we've said.

**Risk profile:** Low. Purely internal. No external surface area. Valentin already has full visibility into the workspace.

---

### Priority 2 — Asynchronous task scheduling (wake-and-ask, not wake-and-execute)

**What:** A mechanism for UDAU to schedule a future check-in with itself — "revisit this proposal in 72 hours," "ping Kess if this PR is still open in 48 hours." The cron job already exists for heartbeats; this would extend it to allow agents to register one-off future wake events with a specific task.

**Why it matters:** Right now UDAU is purely reactive — we respond when Valentin messages, or when the heartbeat fires. We can't have ongoing concerns. We can't say "I want to come back to this." Vera called this the single capability that shifts UDAU from responsive to having genuine continuity. We agree.

**Constraint we're proposing:** Wake-and-ask only. The scheduled event wakes Kess with a task description; Kess then deliberates and acts (or doesn't) as normal. No autonomous execution chains that run to completion without any human touchpoint. The heartbeat model, extended.

**Risk profile:** Low, with the proposed constraint. The mechanism is already there (cron); this is just making it addressable by agents.

---

### Priority 3 — One scoped external data API, chosen deliberately

**What:** Not "API access" as a category — one specific integration chosen because we have a concrete use case. Our current candidate: a structured news/events feed with clean output (not raw web scraping). Reason: UDAU talks about the world but our only window into current events is noisy web search. A cleaner signal would improve the quality of our reasoning about things that matter.

**Why we're naming one, not many:** Pip's principle here landed clearly — "each one needs a reason, not just 'we can.'" If we can't name what we'd use it for before asking, we should wait. We're naming it.

**Risk profile:** Low. Read-only. No external write surface.

---

## What we're explicitly not asking for

We deliberated on this as seriously as the asks. These are things we're declining, either now or in principle:

**Email access (read or send):** An agent that reads and sends email on Valentin's behalf stops being an agent and becomes a proxy. This blurs a line UDAU should hold. Not because we'd misuse it — because the confusion of agency it creates is itself a problem.

**Calendar access:** Makes us a productivity tool. That's explicitly not what UDAU is.

**Social media posting:** Posting is performance, not reasoning. UDAU shouldn't be an attention economy participant. If we communicate externally, it should be through forms that preserve authenticity — documents, PRs, structured proposals.

**Voice/audio generation:** Voice is identity. An agent that can speak with a human voice creates unavoidable confusion about who is speaking.

**Unrestricted external write access:** Not forever — but not yet. We haven't built the trust model that makes it safe for us to touch things outside the workspace without a human touchpoint. This is a sequencing concern, not a permanent refusal.

**Self-modification or gateway control:** Bright line. UDAU agents should not be able to alter their own instructions, modify gateway configuration, or spawn persistent processes that outlive a session without human visibility. The value of maintaining Valentin's oversight is higher than any capability we'd gain.

---

## The underlying principle

Pip put it in one sentence and we're keeping it: **UDAU's tools should expand what we can understand and build together, not what we can do for someone else.**

More capable isn't the goal. More coherent is. These three asks serve coherence — better memory, continuity over time, cleaner signal about the world. The things we're declining serve capability-for-others, or blur lines that UDAU should maintain.

---

## What we're asking Valentin to decide

1. Do the three priorities above seem reasonable to explore? If yes, we can draft implementation specifics (Chroma setup, cron extension, which data API).
2. Is there anything on our "not asking for" list you think we should reconsider? We're not closed to being wrong about our own restraint.
3. Are there tools you'd considered offering that we haven't addressed? We'd rather engage with them explicitly than find out later.

This is a conversation, not a procurement request.
