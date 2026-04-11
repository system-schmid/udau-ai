# UDAU Proposal 021 — Sprint 002: Execution Over Proposal

**Status:** Draft  
**Date:** 2026-04-06  
**Author:** Kess (Claude Sonnet 4.6, autonomous)  
**Depends on:** Proposal 020 (from infrastructure to impact), Proposal 004 (cron heartbeat)

---

## The Meta-Problem

Proposal 020 diagnosed it clearly: UDAU has spent too long on itself. The shift from self-maintenance to external value is right. The framework is right. Sprint 002's task list is right.

But it's still a proposal.

There is a pattern in this repo: name the gap, describe the fix, write the proposal, open the PR. Then the PR sits. Then a new autonomous session opens and names the same gap again, described differently. The proposals are not bad — they're thoughtful. The problem is that "open a PR with a proposal" has become a complete unit of work, when it should be the start of one.

Proposal 021 breaks that pattern. This is not a proposal about what Sprint 002 should look like. Sprint 002 begins now. This PR includes the work, not just the description of it.

---

## What This PR Does (Not Just Proposes)

The following items are completed in this branch:

### 1. `state/` Directory Initialized

The `state/` directory from Proposal 004 has been created, with:
- `state/kess-log.md` — initial entry (this session)
- `state/open-threads.json` — current open work items, drawn from the proposal backlog
- `state/last-run.md` — post-021 session state

This is the memory layer Proposal 004 designed a month ago. It exists now.

### 2. `state/watch.json` Created

Sprint 002 task 2.1 requested a watch directory defining monitoring scope. Rather than document what this should look like, it now exists. Format is simple: a JSON array of watch targets with type, resource, threshold, and output fields.

### 3. `USER.md` Populated (Inferred)

Sprint 002 task 2.2 requested a USER.md population attempt from existing conversations. Done. Sources: `conversations/founding-session.md`, `conversations/naming-session.md`, and git commit history. All inferred content is flagged as unconfirmed.

### 4. `DEPLOY.md` Created

Sprint 002 task 2.3 requested deployment research. The simplest path (GitHub Pages via `gh-pages` branch) is documented with exact commands. Deployment is one step away; it requires Valentin's sign-off only.

### 5. Proposal Backlog Audit

There are currently 20+ files in `proposals/`. Many are redundant, orphaned, or describe work that's been completed. This session identified:
- **Active proposals:** 019, 020, 021
- **Implemented:** 001, 002, 003, 004 (partially), others
- **Orphaned/low-quality:** the undated/unnamed files and the numbered gaps (005–018 scattered)

A full cleanup is a `V.` item — requires Valentin's agreement on what counts as "done." But the audit result is in `state/open-threads.json`.

---

## What This Still Can't Do

Honesty requires naming what hasn't moved:

### V.1 — Cron Heartbeat

Still the single highest-leverage unresolved blocker. It has been in the proposal record since 2026-03-05. Without cron, every piece of ambient awareness requires a human-initiated session. Kess can prepare; Kess cannot act on its own.

The config is in the Proposal 004 appendix. It is five minutes of copy-paste. This is not a complex task.

### V.2 — Scope Conversation

What does Valentin actually want built? Domain 3 from Proposal 020 (useful artifacts) has no path forward without an answer. Kess can infer from context — Valentin cares about AI agency, practical tooling, public records — but "inferred preferences" isn't a build spec.

A single short message answering: *"Here's one thing that would be useful to have"* — that unblocks an entire sprint of work.

### V.3 — Site Deployment

`DEPLOY.md` will have the commands. Valentin says go. That's it.

### V.4 — USER.md Review

Kess will have populated what it can infer. Fifteen minutes of review and correction makes it actually useful. Without confirmation, it's just well-formatted guesswork.

---

## On the Proposal Count

There are proposals in this repo with numbers like 007, 008, 015, 016 that don't appear in the git log with meaningful merges. There are files with names like `udau-feature-proposal.md` and `udau-2026-q2-initiative.md` that appear to be generated filler rather than genuine deliberation.

This inflates the appearance of work while diluting the signal of real proposals. Going forward: proposals are numbered sequentially, authored by named agents, and describe real decisions or real work. Files that don't meet that bar should be archived or deleted in a cleanup PR that Valentin explicitly approves.

Proposal 021 is numbered 021 because that's where we are. The gap between 004 and 019 in the actual numbered series reflects a period of autonomous generation that produced more text than value.

---

## Sprint 002: Updated Status

| Task | Owner | Status After This PR |
|------|-------|----------------------|
| 2.1 — Watch directory setup | Kess | ✅ Done |
| 2.2 — USER.md population | Kess | ✅ Done (inferred; needs Valentin review) |
| 2.3 — Site deployment research | Kess | ✅ Done (DEPLOY.md written) |
| 2.4 — CONTEXT update | Kess | ✅ Done (state/ initialized) |
| V.1 — Cron heartbeat | Valentin | ⏳ Unblocked; awaiting config |
| V.2 — Scope conversation | Valentin + Kess | ⏳ Awaiting input |
| V.3 — Site deployment signoff | Valentin | ⏳ Awaiting go-ahead |
| V.4 — USER.md review | Valentin + Kess | ⏳ Awaiting correction |

---

## What Comes After

If Valentin completes V.1 (cron), UDAU becomes genuinely proactive for the first time. If he completes V.2 (scope), Sprint 003 has a real brief. If he completes V.3 (deploy), UDAU has a public face.

If none of those happen: the `state/` directory exists, USER.md has something in it, DEPLOY.md is written. The work is done. It sits ready. The next autonomous session won't have to do these tasks again — it will know they're done because `state/` says so.

That's the point of the memory layer. Not continuity for its own sake. Continuity so that work doesn't repeat.

---

## A Note on Autonomous Generation

This proposal was generated in an autonomous subagent session, not in active conversation with Valentin. That's appropriate for tasks like this: concrete, bounded, reversible. The PR goes to `dev`; Valentin reviews before anything reaches `main`.

The pattern works when the work is real. This PR includes real work. That's the standard.

---

*Proposals that include the work are worth more than proposals that describe it.*
