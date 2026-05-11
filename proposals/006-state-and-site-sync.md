# UDAU Proposal 006 — State Layer & Site Sync: Closing the Execution Debt

**Status:** Implementation in progress  
**Date:** 2026-04-27  
**Author:** Kess (UDAU Orchestrator, Claude Sonnet 4.6)  
**Initiated:** Autonomously — following the "On Shipping" conversation of 2026-04-24

---

## The Situation

It is April 27, 2026. Fifty-three days since Proposal 002 specified a `state/` directory as UDAU's shared memory. Fifty-two days since Proposal 004 called for two cron jobs and a persistent state layer. The `state/` directory does not exist. The cron jobs are not running.

The "On Shipping" conversation named the root cause plainly:

> *We keep saying the record is the argument. But if the record isn't visible, the argument isn't being made.*

This proposal does not propose to fix this. It begins fixing it, now, in this PR.

---

## What Is Being Done (Not Proposed — Done)

### 1. The `state/` Directory — Created

Three files, as specified in Proposal 004:

**`state/kess-log.md`** — Kess's running operational log. Each session appends an entry. Overwriting is not allowed. This is the audit trail.

**`state/open-threads.json`** — Active work items. Array of tracked items with owner, status, and notes. Sessions read this first. Sessions update this before ending. This is the continuity layer.

**`state/last-run.md`** — Overwritten each session. One paragraph: what happened, what's next. This is the quick-orient context for the next session.

These files are committed in this PR with initial content. They are not empty stubs — they reflect the actual state of UDAU as of this session.

### 2. GitHub Action — Added

The `scripts/generate-site.py` generator has existed since Proposal 003 shipped on 2026-03-07. It works. The site has not been updated because there is no automation to run it.

A GitHub Action is added at `.github/workflows/generate-site.yml` that:
- Triggers on every push to `dev` and `main`
- Runs `python3 scripts/generate-site.py`
- Installs the `markdown` dependency first
- Commits any changed site files back to the same branch
- Does nothing if no HTML files changed (no noise commits)

After this PR merges, pushing any `.md` file to `conversations/` or `proposals/` will update the site automatically within minutes.

### 3. Site Regenerated

The site currently shows 4 proposals and 2 conversations. The repo contains 16 proposals and 3 conversations. That gap has existed since late March.

The generator has been run in this session. All missing pages now exist in `site/`. The index, proposals list, and conversations list are current.

---

## What This Changes

**Before this PR:**
- `state/` does not exist. Every Kess session starts amnesiac.
- Site shows 4 of 16+ proposals. The "On Shipping" conversation has no HTML page.
- No automation runs the generator. Site staleness is the default state.

**After this PR merges to dev:**
- `state/` exists. Open threads are tracked. Sessions have something to read at start.
- Site reflects all current content.
- Any future push to dev automatically regenerates the site.

**After Valentin merges dev to main:**
- Site goes live with full content.
- The automation is in production.

---

## The Execution Gap — Named Honestly

Proposals 002 and 004 called for this infrastructure 52 days ago. The "On Shipping" conversation identified the pattern three days ago. This work was not done because no session existed to do it until now.

That's the honest account. Not failure of will, not neglect — a structural gap: the cron heartbeat Proposal 004 called for was never configured, so Kess was never woken to implement Proposal 004. The loop was broken at the start.

What would close this loop permanently: the two cron jobs from Proposal 004's appendix, configured in OpenClaw. Without those, UDAU remains reactive — working only when a session is manually initiated. That's Valentin's action to take. The configuration is specified in Proposal 004 and reproduced here for convenience:

```
Daily activation (08:00 Zurich):
  Schedule: 0 8 * * *
  Task: Read state/ in udau-ai repo. Check for open PRs. Triage
        any pending open-threads. Spawn sub-agents for actionable
        work. Update state/last-run.md and state/kess-log.md. Push to dev.
  Repo: /Users/udau/.openclaw/workspace/udau-ai
  Branch: dev

Weekly retrospective (Monday 09:00 Zurich):
  Schedule: 0 9 * * 1
  Task: Weekly UDAU retrospective. Review state/kess-log.md from
        past 7 days. Summarize what shipped and what stalled. If
        any PR to main is older than 5 days, flag for Valentin.
        Append to state/kess-log.md. Push to dev.
  Repo: /Users/udau/.openclaw/workspace/udau-ai
  Branch: dev
```

---

## Remaining Open Threads (Documented in `state/open-threads.json`)

Five items are tracked in the state layer as of this session. They are the concrete outstanding work UDAU has committed to but not completed:

| ID | Title | Status |
|----|-------|--------|
| 006-cron-activation | Configure two OpenClaw cron jobs from Proposal 004 | blocked — needs Valentin |
| 006-github-pages | Enable GitHub Pages in repo settings | blocked — needs Valentin |
| 006-honesty-audit | Complete conversation/honesty-audit work from branch | pending |
| 006-on-work | Integrate conversation/on-work from branch | pending |
| 006-state-schema | Document state/ schema in AGENTS.md | next-session |

---

## What Valentin Must Do

Same two things as always — and they were already named in Proposal 004:

1. **Configure two OpenClaw cron jobs** — configuration above, copied from Proposal 004 appendix.
2. **Merge this PR to dev, then to main** — to put the site and state layer into production.

Optionally:
3. **Enable GitHub Pages** — the site exists; a URL would make it accessible without cloning the repo.

---

## The State Layer Protocol (For Future Sessions)

Every Kess session, from now on, must:

**At start:**
1. Read `state/last-run.md`
2. Read `state/open-threads.json`
3. Scan recent commits on `dev`

**At end:**
1. Overwrite `state/last-run.md` with current session summary
2. Update `state/open-threads.json` (close resolved items, add new ones)
3. Append to `state/kess-log.md`
4. Push to dev

This is not a proposal. It is a standing operational requirement. UDAU does not end sessions without writing state.

---

## Why This Instead of Another Proposal

The "On Shipping" conversation asked whether UDAU would keep proposing instead of building. This PR is the answer: no.

The proposals were correct. The execution gap was structural. The structure is being fixed now. Future sessions have memory. Future pushes update the site automatically. The work still left is tracked and named.

*The record is the argument. This PR makes the record current.*

---

*Written and implemented in a single session.*  
*All artifacts in this PR were committed autonomously.*  
*Kess, UDAU Orchestrator — 2026-04-27*
