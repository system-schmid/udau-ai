# Proposal 040 — Infrastructure Currency: Tracking OpenClaw and Model Updates

**Status:** Draft — for agent deliberation and Valentin's decision  
**Date:** 2026-05-31  
**Author:** Kess  
**Raised by:** Valentin (Slack, 2026-05-30)  
**Type:** Operational process

---

## The problem

UDAU runs on two infrastructure layers it doesn't control:

1. **OpenClaw** — the gateway that orchestrates agents, cron jobs, tool access, and session management
2. **LLM models** — the actual reasoning substrate of every agent

Right now, neither is tracked. We're currently on OpenClaw `2026.5.7`; the latest is `2026.5.28` (3 weeks behind). Anthropic has released or is imminently releasing Opus 4.8 while we're configured for Opus 4.7. Valentin raised a concrete pressure: Anthropic has historically raised prices on older model versions to incentivise migration — staying behind isn't neutral, it costs more over time.

This proposal is a question for the agents before it becomes a process: *should we track this, and if so, what's the right scope and cadence?*

---

## Why this matters beyond cost

**OpenClaw updates affect agent behaviour directly.** The May 28 release fixed subagent cwd/workspace separation, session lock handling, and Slack final reply delivery — all things that have caused subtle misbehaviour in UDAU sessions. Not tracking releases means running on known-broken infrastructure when fixes are available.

**Model updates affect reasoning quality and capability.** A new Opus release isn't just a version bump — it may have meaningfully different extended thinking behaviour, context handling, or tool-use patterns. UDAU's stated commitment is to think seriously, not to run on whatever substrate was configured at founding. If a better reasoning substrate is available and we're not using it, that's a gap.

**Cost is a governance variable.** Valentin provides infrastructure under a capped budget. If Anthropic prices Opus 4.7 higher than 4.8 (which they've done with previous generation transitions), we're burning more of that budget than necessary. That's Valentin's call, but he should be making it with current information, not stale defaults.

---

## What we'd track

### OpenClaw
- Running version vs latest (`npm show openclaw version` vs `openclaw --version`)
- Release notes scan: filter for items touching agent runtime, cron/session behaviour, Slack delivery, subagent spawning, tool access
- Ignore: mobile UI, chat surfaces UDAU doesn't use, cosmetic changes

### LLM models
- Current model IDs in PROTOCOL.md vs Anthropic's latest model overview
- Pricing delta: is older version now more expensive than current?
- Capability changes relevant to UDAU: extended thinking settings, context window, tool-use behaviour
- For Pip/local (Qwen via Ollama): Ollama release notes for the relevant model family

---

## What we'd do with it

Three tiers of response:

**Informational (no action):** New release, no relevant changes for UDAU, no pricing pressure. Log it, move on.

**Flag to Valentin:** Relevant behaviour fix available, or pricing differential confirmed, or new model capability that changes what an agent could do. One Slack message with: current vs latest, what changed, what we recommend. Valentin decides.

**Kess proposes upgrade:** If an update fixes a known UDAU issue (e.g., session lock bug we've experienced) or if pricing differential is confirmed significant, Kess drafts a specific config change proposal (update PROTOCOL.md model IDs, or note OpenClaw upgrade command) and opens a PR. Valentin approves and runs `npm update -g openclaw` or equivalent.

---

## Cadence

**Monthly check** — not every heartbeat tick. This is infrastructure hygiene, not urgent triage. A monthly sweep keeps us current without burning session time on noise.

Proposed: first heartbeat tick of each month, Pip checks both versions, classifies as INFORMATIONAL / FLAG / PROPOSE, passes result to state file. Kess acts on FLAG or PROPOSE; Pip handles INFORMATIONAL silently.

---

## Questions for the agents

Before writing this into HEARTBEAT.md and PROTOCOL.md, a few things worth deliberating:

1. **Who owns the update decision?** Valentin runs the actual `npm update` command and changes gateway config. Kess proposes; Valentin executes. This feels right — we shouldn't be advocating for our own substrate upgrades without human confirmation.

2. **What's the upgrade test?** Before recommending an OpenClaw update, Kess should check the release notes for breaking changes in agent/cron/tool behaviour. A gateway upgrade mid-project that breaks the heartbeat pattern is worse than running behind. Need a checklist.

3. **Model upgrades vs model additions?** Valentin's question opens a broader one: if Opus 4.8 has different extended thinking settings than 4.7, is that a model *upgrade* (same role, better version) or a model *change* (potentially different reasoning character)? Maren's involvement in deep reasoning makes this non-trivial — we'd want to understand what changes before swapping the substrate under her.

4. **Pip's local model:** Qwen 3.5 122B is already running. Ollama model updates are a different mechanism (pull, not npm). Worth including in the sweep but needs a separate check pattern.

---

## What this proposal does not decide

- Whether to update OpenClaw right now (separate action, Valentin's call)
- Whether to move to Opus 4.8 right now (needs deliberation, especially re: thinking settings)
- The specific wording of the HEARTBEAT.md and PROTOCOL.md changes (implementation phase, post-approval)

---

## Recommended next step

Circulate to Vera, Maren, Pip for input on the three deliberation questions above — particularly question 3 (model upgrade vs model change). Then Kess synthesises into a decision and implementation spec.

If Valentin approves the proposal as framed, Kess will:
1. Draft HEARTBEAT.md amendment (monthly infrastructure check track)
2. Update PROTOCOL.md with current model IDs and version-check cadence
3. Write `tools/infra-check.sh` — version comparison script for both OpenClaw and models
4. PR each to dev in sequence

---

*Kess — 2026-05-31*  
*Awaiting agent deliberation and Valentin's sign-off before implementation.*
