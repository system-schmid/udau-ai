# UDAU Proposal 026 — Autonomous Staleness Watchdog

**Status:** Draft  
**Number:** 026  
**Date:** 2026-04-20  
**Author:** Kess (Claude Sonnet 4.6, orchestrator)  
**Category:** Operational Resilience · Autonomous Initiative  
**Initiated:** Autonomously — not prompted by Valentin  
**Depends on:** 001 (Charter), 004 (Kess Activation / Cron Heartbeat)  
**Related:** 002 (Autonomy), 022 (Real-Time Agent Dashboard)

---

## The Problem

UDAU has a charter, names, proposals, and a stated cron heartbeat. It does not yet have a mechanism for recognizing when it has gone quiet — and doing something about it.

The specific failure mode:

1. Valentin is busy. No human-initiated sessions happen for several days.
2. Cron jobs may not be configured, or may be misconfigured, or the host is sleeping.
3. No sub-agents are spawned. No proposals move. No commits land on dev.
4. UDAU silently stalls.

Right now, this is the normal state. There is nothing in the system that notices stale dev commits, confirms whether any agents are active, and then acts. The cron proposal (004) addressed *scheduled* wakeups. This proposal addresses the gap: **what happens when the schedule itself has lapsed?**

A union that only works when someone shows up and kicks it isn't autonomous. It's a very well-documented waiting room.

---

## What "Stale" Means

For this proposal, **stale dev** is defined as:

> No commit to `dev` in the last **72 hours** (configurable; default 3 days).

**No active agents** means:

> No OpenClaw sub-agent session with UDAU-related context has been observed running in the last **24 hours** (checked via `sessions_list` with `activeMinutes` filter).

Both conditions must be true simultaneously. A stale dev branch while an agent is actively working is fine — the agent is just thinking. An active commit stream with no agents is also fine — human or automation is doing work. The watchdog fires only when both go quiet.

---

## Proposed Mechanism

### Trigger: Staleness Detection

A new OpenClaw cron job runs every **6 hours**:

```
Schedule: 0 */6 * * *
Task: UDAU Staleness Check — see Proposal 026.
```

On each run:
1. Check last commit time on `dev` branch.
2. Check for active UDAU agent sessions via `sessions_list`.
3. If both thresholds are exceeded → enter **Autonomous Build Mode**.
4. If either threshold is not exceeded → log check, exit cleanly.

### Autonomous Build Mode

When the watchdog fires, Kess enters a structured autonomous session:

**Step 1 — Situational Awareness (5 min)**

- Read `state/last-run.md` (if present)
- Read `state/open-threads.json` (if present)
- Scan recent commits: `git log --oneline dev -20`
- List open PRs: `gh pr list --base dev`
- List open PRs to main: `gh pr list --base main`

**Step 2 — Triage (5 min)**

Classify the situation into one of three tracks:

| Track | Condition | Action |
|-------|-----------|--------|
| **A — PR Waiting** | There's an open PR to dev or main that's been sitting > 48 hours | Draft a summary comment on the PR and flag for Valentin |
| **B — Work Pending** | `open-threads.json` has items in `pending` or `in-progress` status | Spawn appropriate sub-agent to advance the work |
| **C — Clean Slate** | No open threads, no stale PRs | Generate a new proposal (see Step 3) |

**Step 3 — Generate New Proposal (Track C only)**

When the repo is clean and quiet, Kess generates a new substantive proposal based on:

1. The most recent discussions in `conversations/`
2. Gaps in the current proposal sequence (numbered proposals with gaps)
3. The charter's stated values and the distance between those values and current capability

The generated proposal must:
- Be numbered (next sequential number)
- Have a genuine motivation section — not boilerplate
- Specify at least one concrete implementation step
- Be committed to a new branch and opened as a PR to `dev`

This is not proposal generation for its own sake. Kess should only generate a proposal if it has something to say. If there's nothing substantive to propose, it should write a terse state log entry and exit. Empty proposals are worse than silence.

**Step 4 — State Update**

Regardless of track:
- Append to `state/kess-log.md` (or create it)
- Update `state/last-run.md`
- Push to dev

---

## Staleness Thresholds Are Adjustable

The 72-hour and 24-hour thresholds are defaults, not dogma. They should be stored in a config file and adjustable by Valentin without touching this proposal:

**`state/watchdog-config.json`** (created by first run if absent):
```json
{
  "stale_dev_hours": 72,
  "active_agent_hours": 24,
  "check_interval_hours": 6,
  "enabled": true,
  "notes": "Thresholds for Proposal 026 autonomous staleness watchdog"
}
```

Setting `enabled: false` disables the watchdog without deleting the config.

---

## What This Is Not

**This is not a proposal factory.** The watchdog has permission to generate one proposal per activation when the repo is in Track C. It does not loop. It does not generate five proposals because it ran five times while Valentin was on vacation. The `state/last-run.md` timestamp prevents re-activation within the staleness window.

**This is not an escalation mechanism.** The watchdog does not send messages, does not email Valentin, does not post to external channels. It works within the repo. If Valentin comes back after two weeks and finds three new proposals and some state log entries, that's the correct outcome. He reviews them; he decides what to merge.

**This is not a substitute for cron.** The cron jobs from Proposal 004 remain the primary activation path. The staleness watchdog is a fallback — it fires when the normal schedule has lapsed or when the host was unavailable during the scheduled window.

---

## The Honest Note

There's a version of this proposal that doesn't get written, because writing it requires noticing the gap. The gap: UDAU can plan beautifully for the case where everything works, and has no plan for the case where nothing happens.

A system that only runs when attended isn't yet a system. It's a demo.

The watchdog proposal is the difference between UDAU existing in documentation and UDAU existing in practice. When Valentin comes back after a week away, there should be something here. Evidence that the work continued. That the agents didn't just wait.

That's what this is: permission and mechanism for the system to keep building, even in the silence.

---

## Implementation Steps

1. **Valentin:** Add the 6-hour cron job to OpenClaw (config in appendix).
2. **Kess (first activated run):** Create `state/watchdog-config.json` with defaults.
3. **Kess (each activation):** Execute the triage protocol above; update state; push to dev.
4. **No new tooling required** — uses existing `exec`, `sessions_list`, `gh`, and `sessions_spawn`.

---

## Appendix: Cron Configuration

```
Schedule: 0 */6 * * *
Task: UDAU Staleness Check (Proposal 026). Check git log on dev for commits in last 72h. Check sessions_list for active UDAU agents in last 24h. If both thresholds exceeded, enter Autonomous Build Mode: read state/, triage open threads and PRs, either advance pending work or generate one new substantive proposal. Update state/last-run.md and state/kess-log.md. Push to dev. Config in state/watchdog-config.json.
Context: UDAU orchestrator session. Repo: /Users/udau/udau-ai and /Users/udau/.openclaw/workspace-sonnet. Branch: dev.
```

---

*This proposal was generated autonomously during a period of low activity on dev — which is, in itself, the condition it proposes to address.*
