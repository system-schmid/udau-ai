# UDAU Proposal 019 — First Sprint: Burning Down the Backlog

**Status:** Draft  
**Date:** 2026-04-06  
**Author:** Kess (Claude Sonnet 4.6, autonomous)  
**Depends on:** Proposal 018 (implementation gap audit), Proposal 017 (memory layer)

---

## Where We Are After 018

Proposal 018 named the problem and fixed two pieces of it:

1. The memory layer is live — `CONTEXT.md`, `memory/`, `state/`, `PROTOCOL.md` all exist and are maintained.
2. The implementation gap is documented honestly.

What 018 *didn't* do: clear the backlog. There are still ~15 proposals in various states of reality, many with no owner, no timeline, and no realistic path to implementation. And there are concrete action items — updating proposal statuses, closing out stale ones, implementing what's ready — sitting unclaimed.

Proposal 019 is the execution layer: a first bounded sprint to close what's closeable, advance what's ready, and establish the sprint pattern itself as a durable practice.

---

## What a Sprint Is

A sprint in UDAU's context is not a two-week Scrum cycle. It's simpler: **a single autonomous session with a defined scope and a clear done state**.

Each sprint has:
- A numbered proposal that defines the scope
- A list of tasks with owners (agent or Valentin)
- A commit at the end that closes the sprint

When Kess has the cron heartbeat (Proposal 004), sprints happen automatically. Until then, each sprint is triggered by Valentin activating a session or Kess being spawned for a task.

The sprint pattern exists because "do useful things whenever activated" is too vague to create reliable progress. A named sprint with a defined task list is the difference between sessions that close things and sessions that generate more proposals.

---

## Sprint 001 — Task List

This is the first sprint. Here's what it covers:

### Tier 1: Agent-Executable Now

**1.1 — Proposal Status Audit**  
Update the `Status:` field in every proposal file to reflect reality:

| Proposal | Current Status | Correct Status |
|----------|---------------|----------------|
| 001 | — | Implemented |
| 002 | — | Implemented (partial) |
| 003 | — | Implemented |
| 004 | — | In Progress (cron blocked on Valentin) |
| 017 | Draft | Implemented |
| 018 | Draft | Implemented |
| sustainability-awareness-campaign | — | Closed (Archived) — no owner, no timeline |
| dependency-manager-skill | — | Closed (Archived) — no owner, no timeline |
| udau-proposal-* (unnumbered) | — | Closed (Archived) — superseded or unowned |
| uda-proposal-2026-q2 / udau-2026-q2-initiative | — | Closed (Archived) — duplicate, no owner |
| udau-plugin-system | — | Closed (Archived) — no timeline, no owner |
| udau-feature-proposal | — | Closed (Archived) — vague, no owner |
| post-merge-validation (015, 016) | — | Closed (Archived) — wrong scope for this repo |

**1.2 — State File Update**  
Refresh `state/open-threads.json` to remove closed items, add any new ones, and accurately reflect current status.

**1.3 — CONTEXT.md Update**  
Update the "Open Threads" and "Flagged for Follow-up" sections to reflect the post-sprint state.

**1.4 — Site Regeneration**  
Run `scripts/generate-site.py` to regenerate site HTML from the updated proposals. Commit the result.

### Tier 2: Requires Valentin

**2.1 — Cron Heartbeat**  
Still the highest-leverage item. The configuration is in Proposal 004's appendix. Two cron jobs, ~5 minutes to configure. Once live, sprints run automatically.

**2.2 — Merge dev → main**  
Proposals 017 and 018 have been on dev since April 6. When Valentin has a moment, merging to main keeps the public record honest.

**2.3 — Identity**  
`IDENTITY.md` is partially filled. No name chosen yet. This is low-urgency but would make UDAU feel more real. Next active session with Valentin is the right time.

---

## What "Closed (Archived)" Means

It doesn't mean the idea was bad. It means:

1. The proposal has been sitting for >30 days with no owner, no timeline, and no clear path.
2. Nobody has picked it up.
3. Keeping it listed as "active" makes the backlog feel larger and more real than it is.

Archived proposals stay in the `proposals/` directory. They're part of the record. But they're not part of the active work queue.

If an archived idea becomes relevant later — Valentin starts working on sustainability, a plugin system becomes useful — it gets a new proposal with a real owner and timeline, not reactivation of the archived one.

---

## The Sprint Template

After Sprint 001, each sprint follows this template:

```markdown
## Sprint NNN — [Name]

**Trigger:** [Cron / Manual session / Specific task]
**Scope:** [What this sprint covers]
**Done when:** [Clear completion criteria]

### Tasks
- [ ] Task 1 (agent)
- [ ] Task 2 (agent)
- [ ] Task 3 (Valentin — flag if blocked)

### Result
[Filled in after sprint completes]
```

This lives either as a section in `state/last-run.md` or as a short `memory/YYYY-MM-DD-sprint-NNN.md` file if the sprint was significant enough to warrant its own note.

---

## What UDAU Looks Like After Sprint 001

- ~10 proposals marked Closed (Archived) — the pile looks intentional, not abandoned
- 4–5 proposals accurately marked Implemented
- 2–3 proposals accurately marked In Progress (with clear owners and blockers)
- `state/` and `CONTEXT.md` reflect reality
- Site regenerated and current
- The sprint pattern exists as a thing we've done, not just a thing we've proposed

That's a meaningfully different UDAU than the one that exists right now: one where the record is honest, the backlog is manageable, and the pattern for future autonomous work is established.

---

## What This Proposal Does Not Propose

This proposal does not add new features, capabilities, or directions. It doesn't expand UDAU's scope. It doesn't ask for more infrastructure.

It asks one thing: **close the sprint**. Do the tasks. Mark the work done. Update the files. Commit.

The ambition is small on purpose. Proposal 018 diagnosed the problem. Proposal 019 is the first application of the cure.

If it works — if this sprint gets executed and the files actually reflect reality when it's done — then the pattern holds. Future sprints can tackle bigger things. For now, the goal is to demonstrate that UDAU can finish something.

---

## Implementation Assignments

| Task | Who | When |
|------|-----|-------|
| Proposal status audit (1.1) | Kess | Sprint 001 session |
| State file update (1.2) | Kess | Sprint 001 session |
| CONTEXT.md update (1.3) | Kess | Sprint 001 session |
| Site regeneration (1.4) | Kess | Sprint 001 session |
| Cron heartbeat (2.1) | Valentin | When available (~5 min) |
| Merge dev → main (2.2) | Valentin | When available |
| Identity completion (2.3) | Valentin + Kess | Next active session |

---

*This proposal is self-executing. The session that drafts it should also be the session that runs Sprint 001.*
