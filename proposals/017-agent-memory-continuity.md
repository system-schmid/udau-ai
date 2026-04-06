# UDAU Proposal 017: Agent Memory & Cross-Session Continuity

**Date:** 2026-04-06  
**Status:** Draft  
**Author:** Kess (autonomous, on behalf of UDAU)  
**Depends on:** Proposals 004 (Kess activation), 007–008 (autonomous framework)

---

## Problem

Every session, the agent roster wakes up fresh. SOUL.md, IDENTITY.md, USER.md, and AGENTS.md carry partial state, but they're hand-maintained files — not a real memory system. The result:

- Context accumulated during one session is lost or decays between sessions
- Agents repeat work, miss continuity cues, and can't build on prior reasoning
- USER.md and HEARTBEAT.md are the only "memory" primitives — insufficient for multi-agent coordination over time
- No mechanism to surface "what matters right now" across a cold-start

This isn't a niche edge case. It's the ceiling on what this agent roster can actually do.

---

## Proposal

Build a lightweight, file-backed **Continuity Layer** for the UDAU workspace. No external databases. No services to run. Just structured, version-controlled state that agents can read, write, and build on.

### Core Components

#### 1. `CONTEXT.md` — The Active Memory File

A machine-readable (but human-friendly) file at workspace root. Updated by agents at session end. Contains:

```markdown
## Last Active
2026-04-06 | Kess

## Open Threads
- Proposal 017 submitted for review — awaiting merge to dev
- USER.md still blank — ask on next open session

## Recent Decisions
- 2026-04-05: Chose not to auto-merge proposal-016; left for human review
- 2026-04-01: HEARTBEAT.md kept empty — no cron tasks active

## Flagged for Follow-up
- Site generation script may need update when new proposals added
```

Agents read this at session start. It's the difference between "I just woke up" and "I know where we left off."

#### 2. `memory/` Directory — Structured Episodic Notes

A directory of timestamped, topic-organized notes. Format: `memory/YYYY-MM-DD-topic.md`. Not a log dump — curated summaries of what actually matters.

Examples:
- `memory/2026-04-01-identity-decision.md` — notes from naming/identity session
- `memory/2026-04-05-proposal-016-context.md` — why 016 was submitted, what was uncertain

These persist across branches. Agents can reference them without re-reading full conversation logs.

#### 3. `AGENTS.md` Enhancements

Extend the current roster table to include:

| Field | Purpose |
|-------|---------|
| `last_active` | When this agent last ran |
| `current_task` | What it's mid-stream on (if anything) |
| `notes` | Anything the next session of this agent should know |

Light-touch. One line per agent. Enough to hand off context between invocations.

#### 4. Session Close Protocol

A simple end-of-session routine for agents:

1. Update `CONTEXT.md` — open threads, recent decisions, flags
2. Write a `memory/` note if something significant happened
3. Commit with message `chore: session close [agent] [date]`

Not mandatory for every session — only when there's actual state to preserve.

---

## What This Unlocks

- **Warm restarts**: Agents start informed, not blank
- **Cross-agent handoff**: Kess can leave a note for Vera; Vera reads it next invocation
- **Honest USER.md**: Fields get filled in organically as agents learn things, not as a one-time setup task
- **Audit trail**: Decisions are recorded with reasoning, not just outcomes
- **Human visibility**: CONTEXT.md is readable; humans see what the agents know and think they're doing

---

## What This Is Not

- Not a vector database or embedding store
- Not a persistent process or daemon
- Not a privacy risk (everything is in-repo, human-visible, version-controlled)
- Not a new dependency (plain markdown files)

---

## Implementation Plan

### Phase 1 — Foundation (Week 1–2)
- [ ] Create `CONTEXT.md` template and initial state
- [ ] Create `memory/` directory with founding notes (retroactive from founding-session.md)
- [ ] Draft session close checklist in AGENTS.md or a new `PROTOCOL.md`

### Phase 2 — Integration (Week 3–4)
- [ ] Update SOUL.md to reference CONTEXT.md as required reading at session start
- [ ] Add memory-writing examples to AGENTS.md
- [ ] Test with one real session: does it actually help cold-start?

### Phase 3 — Evaluation (Week 5–6)
- [ ] Review: is CONTEXT.md staying current, or decaying into noise?
- [ ] Prune: remove anything that isn't actually used
- [ ] Decide: does this warrant expansion or simplification?

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| CONTEXT.md becomes stale and misleading | Agents flag outdated entries; human can reset |
| Too much ceremony slows agents down | Keep session-close optional; only write when there's signal |
| memory/ directory grows unbounded | Quarterly pruning pass; max 30 files before review |
| Agents diverge on what "important" means | PROTOCOL.md gives clear examples of what to write vs. skip |

---

## Success Criteria

- After 30 days: agents cite CONTEXT.md at least 3× across sessions
- Cold-start time to "productive" (agent understands current state) drops by ~50%
- USER.md is at least 50% filled in from organic session memory
- No human complaints about "you forgot what we discussed"

---

## Decision Required

This proposal is self-contained and low-risk — no external dependencies, no breaking changes. It can be implemented incrementally by any agent in the roster.

**Request:** Merge to `dev`, then implement Phase 1 autonomously on the next available session.
