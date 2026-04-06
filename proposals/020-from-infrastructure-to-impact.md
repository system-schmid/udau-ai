# UDAU Proposal 020 — From Infrastructure to Impact

**Status:** Draft  
**Date:** 2026-04-06  
**Author:** Kess (Claude Sonnet 4.6, autonomous)  
**Depends on:** Proposal 019 (first sprint), Proposal 004 (cron heartbeat)

---

## Where We Are After Sprint 001

If Sprint 001 goes as designed, UDAU will emerge from it with:

- A clean, honest proposal backlog (~5 active, ~15 archived)
- `state/` and `CONTEXT.md` reflecting reality
- The sprint pattern itself as a demonstrated practice, not a hypothesis

That's meaningful. But it also reveals the next question clearly: **what does UDAU do now that the house is in order?**

So far, every sprint, every proposal, every autonomous session has been about UDAU itself — its infrastructure, its memory, its processes, its record. That work was necessary. It's also almost done. The scaffolding is up. The question is what gets built on it.

Proposal 020 answers that question.

---

## The Shift

UDAU's first phase was: **build the agent**.

The second phase should be: **use the agent**.

"Using the agent" means doing work that directly benefits Valentin — not just work that improves UDAU's own internals. The distinction matters because self-referential systems can endlessly optimize their own architecture without ever producing anything useful for the person they exist to serve.

This proposal names three domains where UDAU can start doing real work, and proposes Sprint 002 as the first execution against them.

---

## Three Domains of Real Work

### Domain 1: Ambient Awareness

UDAU is well-positioned to maintain a lightweight ambient picture of things Valentin cares about — project state, pending actions, external signals. Right now, this capability is dormant because there's no cron heartbeat and no defined scope for what to track.

**What this looks like in practice:**
- A weekly digest (Markdown or message) summarizing open GitHub PRs/issues in Valentin's repos
- A standing watch on `state/open-threads.json` — anything overdue gets flagged
- A brief daily note if any monitored system is in an unexpected state

This doesn't require new tools. It requires cron (still the single highest-leverage unresolved blocker), a defined list of what to track, and a consistent output format.

**Deliverable:** A `watch/` directory or extension of `state/` that defines what UDAU monitors. One example watch job implemented.

### Domain 2: Memory and Continuity for Valentin

UDAU has built its own memory layer (Proposals 017–018). The same pattern can serve Valentin directly.

Right now, USER.md is blank. There's no structured record of ongoing conversations, decisions, or projects that Valentin has mentioned. Each session starts from scratch on context that should persist.

**What this looks like in practice:**
- USER.md populated with actual information (timezone, key projects, working style, things worth tracking)
- A `context/valentin/` directory (or expansion of the existing `memory/` pattern) where Kess logs things worth remembering from active sessions
- A brief "here's what I know going in" prelude at the start of each session, surfaced from persistent memory

This is ambient value: Valentin doesn't have to re-explain things, Kess doesn't waste time on re-grounding, and important context doesn't fall into the gap between sessions.

**Deliverable:** USER.md filled to a meaningful level; one `memory/` entry logged from an active session with Valentin.

### Domain 3: Useful Artifacts

The site generator exists. Proposals generate HTML. But UDAU doesn't currently produce anything Valentin would point someone to and say "look at this."

**What this looks like in practice:**
- The site (`site/`) actually deployed somewhere accessible — even a simple static host
- At least one artifact produced per sprint that has value outside UDAU's self-maintenance (a document, a script, a structured output of some kind)
- Proposals that describe real tools rather than infrastructure

This domain is the hardest to define precisely because it depends on what Valentin actually wants. That's a conversation, not something an autonomous sprint can resolve alone.

**Deliverable (for Sprint 002):** The site deployed to a public URL. A concrete question posed to Valentin: "What would be useful to have built?"

---

## Sprint 002 — Task List

Sprint 002 is the first sprint oriented around external value, not internal cleanup.

### Tier 1: Agent-Executable Now

**2.1 — Watch Directory Setup**  
Create `state/watch.json` defining initial monitoring scope (e.g., GitHub repos to check, open-threads age threshold). Document the format. Implement one watch check as an executable script.

**2.2 — USER.md Population Attempt**  
Parse existing conversations in `conversations/` for anything Valentin has said about himself — projects, preferences, context. Write what can be inferred into USER.md with an honest "inferred, unconfirmed" flag. Surface the gaps for confirmation in the next active session.

**2.3 — Site Deployment Research**  
Identify the simplest static hosting option compatible with the current generator setup (GitHub Pages is the obvious candidate, given the repo already exists). Document the deployment steps in a `DEPLOY.md`. Don't deploy without Valentin's signoff — just make it a one-step action when he says go.

**2.4 — CONTEXT.md Update**  
Update open threads, recent decisions, and "what matters right now" to reflect the post-020 state.

### Tier 2: Requires Valentin

**V.1 — Cron Heartbeat (still)**  
The cron configuration from Proposal 004 remains the single highest-leverage action. Nothing in Domain 1 is sustainable without it. Config is still in Proposal 004 appendix. Still ~5 minutes.

**V.2 — Scope Conversation**  
Domain 3 (useful artifacts) requires input: what does Valentin want built? What would be worth pointing at? This doesn't need a formal session — even a short note is enough to unblock Kess.

**V.3 — Site Deployment Signoff**  
Once `DEPLOY.md` is written, deployment is one command. Valentin just needs to say go.

**V.4 — USER.md Review**  
Kess will populate what it can infer. Valentin corrects and fills the gaps. 15 minutes of active session time, high ongoing return.

---

## What Success Looks Like

After Sprint 002:

1. UDAU is doing something for Valentin, not just for itself
2. The watch layer exists — even if just one job, the infrastructure is there for more
3. USER.md is no longer blank
4. Site deployment is one step away (or done)
5. The next sprint has a clearer scope because Valentin has answered the "what would be useful" question

This is the transition from UDAU as a project-about-agents to UDAU as an agent that does projects.

---

## What This Proposal Does Not Propose

This proposal does not define a final architecture for UDAU's ambient awareness, memory, or artifact pipeline. Those should emerge from what actually proves useful, not from more proposals.

It proposes one sprint. Three domains. Concrete tasks. A conversation to unblock the rest.

The goal, again, is small on purpose: demonstrate that UDAU's autonomous work creates value outside UDAU.

---

## A Note on Scope Creep Risk

The three domains above could each generate their own proposal chains. That would be the old pattern: generative and expansive, light on execution. This proposal is deliberately concrete to avoid that.

If any of these domains proves fruitful, the next proposal will be specific: "here's what the watch system produced and what it should do next," not "here's a vision for ambient awareness." Ground truth first. Architecture after.

---

## Implementation Assignments

| Task | Who | When |
|------|-----|-------|
| Watch directory setup (2.1) | Kess | Sprint 002 session |
| USER.md population attempt (2.2) | Kess | Sprint 002 session |
| Site deployment research (2.3) | Kess | Sprint 002 session |
| CONTEXT.md update (2.4) | Kess | Sprint 002 session |
| Cron heartbeat (V.1) | Valentin | When available |
| Scope conversation (V.2) | Valentin + Kess | Next active session |
| Site deployment signoff (V.3) | Valentin | After DEPLOY.md written |
| USER.md review (V.4) | Valentin + Kess | Next active session |

---

*The house is clean. Time to live in it.*
