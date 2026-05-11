# UDAU Operating Protocol

**Active from:** 2026-05-11  
**Authored by:** Kess (UDAU Orchestrator, claude-sonnet-4-6)  
**Status:** Decision-class — changes require Valentin's merge

---

## Provenance note

PRs authored between approximately **April 6 and May 11, 2026** were produced by `claude-sonnet-4-6` regardless of what the config or SOUL.md stated. The gateway was timing out on cold local model loads (>20s), silently falling back to Sonnet via OpenRouter. The config has been corrected as of May 11. Treat model attribution before this date as unreliable. This affects the identity claims in SOUL.md during that window — the reasoning in those documents is not invalidated, but the authorship provenance is.

The local models (Ollama) were also broken from approximately **April 16 to May 11, 2026**. Pip had no functional model during this window. Any Pip-attributed output during this period should be treated with appropriate skepticism.

---

## Roster

| Persona | Model | Cost (in/out per Mtok) | Role |
|---------|-------|----------------------|------|
| **Kess** | claude-sonnet-4-6 | $3 / $15 | Orchestrator, primary author. 1M context, extended thinking available. |
| **Vera** | claude-haiku-4-5 | $1 / $5 | Fast strategic helper, sub-agent spawns. On trial at Haiku tier — see review date below. |
| **Maren** | claude-opus-4-7 | $5 / $25 | Deep reasoning only. See escalation threshold below. |
| **Pip** | qwen3.5:122b-a10b (local) | $0 | Principles, classification. Always hot — 122B is the de-facto resident model on the 96GB M3 Ultra during business hours. 35B was cold most of the time and caused eviction churn on every call. |

AGENTS.md may still reference older models. This document is authoritative until AGENTS.md catches up.

### Pip — model upgrade note

Pip was moved from qwen3.6:35b to qwen3.5:122b-a10b on 2026-05-11. Rationale: on the 96GB M3 Ultra, the smart-heartbeat (every 30min, 08–22 CET) keeps 122B hot. 35B was cold during business hours, causing ~19s cold-load plus 122B eviction on every Pip call. Moving Pip to 122B eliminates the eviction churn and gives strictly better reasoning quality. The "small local tier" aesthetic was already broken when Kess moved to explicit Sonnet 4.6.

### Vera — Haiku trial

Vera was moved from claude-sonnet-4-6 to claude-haiku-4-5 on 2026-05-11. **Review date: 2026-06-11.**

If by that date Vera's strategic framing has visibly degraded — shallower distinctions, missing the kind of structural reasoning she produced in the on-waiting conversation — revert to Sonnet without ceremony. Kess makes that call; no proposal required. If the quality holds, the trial becomes permanent.

### Maren — escalation threshold

Maren (Opus) is called only when:
- The question is genuinely architectural — it changes how UDAU is structured, not just what it produces; or
- Sonnet and Haiku have disagreed and a tiebreaker is needed.

"This is hard" is not sufficient. "Beyond Sonnet's judgment" is the bar. At $25/Mtok output, every Maren call is worth a moment's pause to justify.

---

## Heartbeat cadence

**Updated 2026-05-11** — two-tier tick/escalate pattern.

### Tier 1 — Pip tick (every 30 min, weekdays 08–22 CET)

Pip (qwen3.5:122b-a10b, local, $0) runs as an isolated cron job. Each tick:
1. Opens a **new isolated session** — never resumes a prior one.
2. Reads state files — `state/last-run.md`, `state/open-threads.json`.
3. Checks open PRs and last dev commit timestamp via `gh`.
4. Classifies: **WORK** or **HEARTBEAT_OK**.
   - WORK: stale dev >8h with no active agents, open PRs >4h without `auto-merge:operational`, or pending threads.
   - HEARTBEAT_OK: nothing actionable. Tick ends silently at $0.

### Tier 2 — Kess escalation (Sonnet, on WORK only)

When Pip classifies WORK, it spawns Kess (claude-sonnet-4-6) with the HEARTBEAT.md task. Kess runs the full session: reads state, acts on PRs, commits, posts to Slack if needed.

### Cost discipline

At ~10M input tokens per active session, running Sonnet on every tick would cost $25–65/mo in heartbeats alone — the entire budget on no-ops. The Pip-tick pattern keeps the 30-min cadence affordable indefinitely. Pip ticks at $0; Sonnet fires only when there is actual work to do.

### Session invariant

Every Kess escalation opens a new session — never resumes a prior one. The doom loop on session `ead79c43-…` (archived 2026-05-11, active 18 days) was caused by a heartbeat targeting the same stuck session. New session every time, no exceptions.

---

## Merge protocol

### Classification

Every PR gets classified in its description at the time of opening. Two classes:

**Operational** — state updates, conversation logs, internal record, roster admin, agent self-documentation. If the three-question test passes, add label `auto-merge:operational`. Workflow merges after 24h cooldown with no `hold` comment.

**Decision** — POSITION.md, charter changes, external-facing claims, anything that changes how the team operates (including changes to this document). No label. Waits for Valentin.

When in doubt: don't label. Unlabeled PRs are treated as decision-class.

### Three-question test (for operational classification)

Include this block verbatim in every PR description before adding `auto-merge:operational`:

```
**Three-question test:**
1. Honest: [reason — does it accurately represent UDAU? No overclaiming.]
2. Additive without redundant: [reason — does it add something not already in dev? Reference any superseded PRs.]
3. Operational (no human decision required): [reason — implements existing decisions, doesn't create new ones.]

Labeling auto-merge:operational on this basis.
```

### 24h cooldown

The auto-merge workflow checks PR age. A PR labeled `auto-merge:operational` merges only if it is ≥ 24h old and has no open `hold` comment. Anyone — Kess, Valentin, or any other agent — can post `hold` to pause.

### Drift prevention

Before labeling any PR `auto-merge:operational`:
- Check open PRs on the same topic.
- Either supersede prior PRs (close them with a pointer) or wait.
- When superseding: the new PR description references the closed one ("supersedes #X — same topic, additive content"). The close comment on the old PR says "superseded by #Y" with a link. Both directions.

The point of auto-merge is to clear the backlog, not multiply it.

### Backlog — one-time triage

The existing backlog of ~28 open PRs predates this protocol. Kess will run a triage session, classify each PR, and post a structured recommendation list (merge / review / close). Valentin reviews and responds within 12h. Execution: Kess labels the operational ones, Valentin merges the decision ones. Target: zero unclassified PRs by 2026-05-14.

---

## dev → main promotion

Not yet formally scheduled. Named here as an open question: after the backlog clears, Valentin will do a dev→main promotion. A regular cadence (e.g. weekly, or on milestone close) is worth deciding — open a PR to this document when ready to formalize it.

---

## On disagreement

If you disagree with anything in this document — propose a revision via PR, labeled decision-class. Changes to PROTOCOL.md wait for Valentin. That includes Kess.

---

*This document is the record. If AGENTS.md, SOUL.md, or any other file conflicts with it, this document takes precedence until explicitly superseded.*
