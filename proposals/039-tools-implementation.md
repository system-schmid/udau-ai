# Proposal 039 — Tools Implementation Plan

**Status:** Draft  
**Date:** 2026-05-30  
**Author:** Kess  
**Follows:** Proposal 039 (approved 2026-05-30)

---

## Approved scope (from Proposal 039)

1. Persistent queryable memory (vector search over UDAU's own workspace)
2. Asynchronous task scheduling (wake-and-ask, not wake-and-execute)
3. One scoped external data API (structured news/events feed)

---

## Priority 1 — Vector memory

**Stack:** Ollama embeddings (already running) + Chroma (local, lightweight) + a small indexing script.

**What gets indexed:**
- `conversations/` — all .md files
- `proposals/` — all .md files
- `state/` — open-threads.json, kess-log.md, last-run.md

**How agents use it:**
- Kess calls a simple CLI: `udau-search "topic"` → returns top-N chunks with source paths
- Optional: integrate into heartbeat so Kess auto-searches for related prior work before Track C decisions

**What Valentin needs to do:**
- Install Chroma: `pip install chromadb` (already on the machine or one command)
- Run the indexing script once to build the initial index
- (Optional) Add index refresh to the cron job

**Implementation steps for Kess:**
1. Write `tools/memory-index.py` — indexes workspace into Chroma
2. Write `tools/memory-search.py` — CLI wrapper for vector search
3. Add to HEARTBEAT.md: Kess optionally queries before Track C write decision
4. Document in TOOLS.md

---

## Priority 2 — Async task scheduling (wake-and-ask)

**Current state:** Cron job 54b74167 fires Pip every 30min, weekdays 08–22 CET. Pip classifies; if WORK, escalates Kess.

**Extension needed:** Agents should be able to register a one-off future task, e.g.:
```
udau-schedule "2026-06-02T10:00Z" "revisit PR #73 discussion — is on-witnessing still the right frame?"
```

**Mechanism:**
- A simple JSON file: `state/scheduled-tasks.json`
- Each entry: `{ "id": "...", "due": "ISO8601", "task": "...", "created_by": "kess", "created_at": "..." }`
- Pip's tick checks this file in addition to its current classification logic
- If a task is due (or overdue), Pip treats it as WORK and passes the task description to Kess

**What Valentin needs to do:** Nothing — this runs entirely within the existing cron + OpenClaw infrastructure.

**Implementation steps for Kess:**
1. Write `state/scheduled-tasks.json` (initially empty array)
2. Update Pip's heartbeat prompt or classification logic to check scheduled-tasks.json
3. Write `tools/udau-schedule.sh` — CLI wrapper to add entries
4. Update HEARTBEAT.md and PROTOCOL.md

---

## Priority 3 — External data API

**Candidate:** Hacker News Algolia API (`hn.algolia.com/api/v1/search`) — free, structured, no auth, clean JSON output. Relevant because HN surfaces AI/agent research, governance discussions, and technical discourse. UDAU's conversations often reference "what's happening in the field" without a clean signal.

**Alternative:** arXiv API for recent AI papers — also free, structured.

**Not chosen (yet):** NewsAPI, Perplexity, or any paid/authenticated service. Start free.

**How agents use it:**
- Before Track C write decisions, Kess optionally queries HN for recent discussions on relevant topics
- Not for trending content — for calibration ("has this already been said better?")

**What Valentin needs to do:** Nothing for HN Algolia — no auth required.

**Implementation steps for Kess:**
1. Write `tools/hn-search.sh` — wrapper around HN Algolia API
2. Document usage norms in TOOLS.md (query, don't curate; don't let external signal drive what we write)
3. Optionally: add arXiv search for academic framing

---

## Sequencing

| Step | What | When |
|------|------|------|
| 1 | PR this implementation plan to dev | Now |
| 2 | Implement Priority 1 (memory indexing + search) | Next session |
| 3 | Implement Priority 2 (scheduled tasks) | Following session |
| 4 | Implement Priority 3 (HN search tool) | Following session |
| 5 | Update HEARTBEAT.md, PROTOCOL.md, TOOLS.md | As each tool ships |

Each tool ships as its own PR to dev. No bundling.

---

## What this doesn't change

- Valentin retains merge authority to main
- No external write surface introduced
- Agent spawn permissions unchanged
- Self-modification remains off-limits

The tools expand what we can *understand*. They don't change who decides.

---

*Kess — 2026-05-30*
