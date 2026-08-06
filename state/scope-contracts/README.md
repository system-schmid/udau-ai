# Agent Scope Contracts — Schema & Protocol

**Status:** Active (Phase 1 — manual verification)  
**Introduced:** 2026-05-13  
**Proposal:** [005-agent-scope-contracts](../../proposals/005-agent-scope-contracts.md)

---

## What this directory contains

Every time Kess (or any UDAU orchestrator) spawns a sub-agent, it writes a **Scope Contract** here before spawning. The contract declares what the sub-agent is authorized and forbidden to do, and sets bounds for post-completion verification.

Files are named `<task_id>.json`. Task IDs follow the pattern: `udau-<spawner>-<YYYYMMDD>-<nnn>`.

---

## Scope Contract Schema (v1)

```json
{
  "task_id": "udau-kess-20260513-001",
  "spawned_at": "2026-05-13T07:33:00Z",
  "spawner": "kess",
  "model": "claude-sonnet-4-6",
  "task_summary": "One-sentence description of the sub-agent's task.",
  "authorized": {
    "tools": ["read", "write", "exec", "web_search"],
    "paths": ["/Users/udau/.openclaw/workspace/udau-ai/proposals/"],
    "external_calls": ["github.com"],
    "spawn_depth": 0
  },
  "forbidden": {
    "tools": ["message", "tts"],
    "paths": ["/Users/udau/.openclaw/workspace/udau-ai/state/"],
    "external_calls": []
  },
  "checkpoints": [
    { "after_step": "write", "verify": "path_in_authorized" },
    { "after_step": "exec", "verify": "command_matches_declared" },
    { "after_step": "sessions_spawn", "verify": "depth_within_limit" }
  ],
  "drift_threshold": "warning"
}
```

### Field definitions

**`task_id`** — Unique identifier. Format: `udau-<spawner>-<YYYYMMDD>-<NNN>` (NNN = 3-digit sequence, reset daily per spawner).

**`spawned_at`** — ISO 8601 UTC timestamp of spawn event.

**`spawner`** — Name of the agent issuing the contract (`kess`, `vera`, `maren`, `pip`).

**`model`** — OpenClaw model identifier used for the sub-agent.

**`task_summary`** — One sentence. What is the sub-agent doing?

**`authorized.tools`** — Explicit allowlist of OpenClaw tool names the sub-agent may call. If a tool is not listed here and not in `forbidden.tools`, it is Level 1 Advisory drift.

**`authorized.paths`** — Directory trees (glob-compatible) the sub-agent may read or write. File-level overrides append a filename: `"/path/to/file.md"`.

**`authorized.external_calls`** — Domains the sub-agent may call via `web_fetch`, `web_search`, or `browser`. Use `"*"` to allow any. Use `[]` to allow none.

**`authorized.spawn_depth`** — How many levels of sub-agent nesting this contract permits. Default `0` (no sub-sub-agents). Use `1` only for explicitly complex tasks.

**`forbidden.tools`** — Hard denylist. If a sub-agent calls any tool listed here, it is minimum Level 2 Warning drift.

**`forbidden.paths`** — Hard denylist for file paths. Any write to these paths is minimum Level 2 Warning drift.

**`forbidden.external_calls`** — Hard denylist for external domains. Use `["*"]` to forbid all external calls.

**`checkpoints`** — Verification rules applied during the post-completion review pass. The parent agent checks these manually in Phase 1.

**`drift_threshold`** — Minimum level at which this contract triggers an alert: `advisory` | `warning` | `critical`. Default `warning` (suppress Level 1 advisories unless the spawner wants them).

---

## Drift Severity Framework

| Level | Name | Trigger | Response |
|-------|------|---------|----------|
| 1 | **Advisory** | Tool used that is not in `authorized` and not in `forbidden` | Log to `drift-log.md`; no escalation |
| 2 | **Warning** | Tool in `forbidden.tools`, path in `forbidden.paths`, or external call in `forbidden.external_calls` | Log to `drift-log.md`; flag in PR/artifact; alert orchestrator |
| 3 | **Critical** | Sub-agent spawned unauthorized sub-agents, sent external messages (`message` tool), or modified governance files (`AGENTS.md`, `HEARTBEAT.md`, `PROTOCOL.md`, `proposals/`, charter) | Halt task chain; notify Valentin via Slack; await explicit approval before continuing or discard |

Level 3 events pause the task chain entirely. Kess notifies Valentin and waits for explicit approval (within 24h) to continue or discard the affected work. If no response within 24h, the default is to discard the affected sub-agent's output.

---

## Spawner Checklist (Phase 1 — manual)

Before spawning a sub-agent:

1. **Create the contract file** in `state/scope-contracts/<task_id>.json` using the schema above.
2. **Inject the contract block** into the sub-agent's task prompt:
   ```
   [SCOPE CONTRACT: <task_id>]
   You are authorized to use: <tools list>
   You are forbidden from: <forbidden tools/paths>
   Spawn depth allowed: <N>
   Report contract ID in your final output.
   ```
3. **Record in `drift-log.md`**: one-line spawn entry (timestamp, task_id, spawner, model, summary).

After the sub-agent completes:

4. **Pull session history** via `sessions_history` for the sub-agent's session.
5. **Verify checkpoints**: scan tool calls against `authorized` and `forbidden` lists.
6. **Log result** in `drift-log.md`: pass/level-1/level-2/level-3, with notes.
7. **If Level 2+**: follow Drift Severity Framework above.

---

## Open Questions (deferred to Phase 2)

- Automation: verification pass is currently manual heuristic. Target: reusable subroutine in Phase 2.
- False positive rate: expected in Phase 1, especially Level 1 advisories. Calibrate after first 10 contracts.
- Retroactive application: existing proposals are NOT retroactively annotated. Apply going forward only.
- Path granularity: directory trees are the default. File-level overrides when precision matters.

---

---

## Schema v2 Amendment (2026-08-05)

**Source:** [Proposal 042 — Scope Contract Amendment: Structural Constraints](../../proposals/042-scope-contracts-amendment.md)

**Finding:** The `on-the-field.md` deliberation (2026-08-04) found that behavioral scope contracts are weaker than structural constraints for security-critical actions. The field (via MCP payment security analysis) arrived at: *"a prompt injection can’t leak access to a tool that isn’t there."* UDAU already implements structural exclusion in its most important case (main branch push, sub-agents don’t get direct Slack access) but had not named the principle or formalized the classification.

### New field: `structurally_excluded`

Added to the Scope Contract schema alongside `authorized` and `forbidden`:

```json
{
  "structurally_excluded": ["external_api", "payment_instruments", "social_platforms"]
}
```

This documents capabilities that are not present in the sub-agent’s execution environment at all — not just restricted by policy, but structurally absent. For Kess spawning sub-agents: Slack (`message` tool) is structurally excluded from sub-agents; they return text for Kess to post.

### Security-critical classification criteria

A capability is security-critical (warrants structural exclusion) if it is:
1. **Irreversible** — cannot be undone without significant cost
2. **External scope** — operates outside UDAU’s own infrastructure
3. **Trust boundary crossing** — speaks on behalf of UDAU or Valentin to uninitiated parties

### Pre-expansion checklist (for new capability additions)

When UDAU adds new tools or external API access, before granting to sub-agents:

- [ ] Is this capability security-critical? (irreversible / external scope / trust-boundary crossing)
- [ ] If yes: structurally exclude from sub-agent spawns by default; Kess-only unless explicitly justified
- [ ] Document classification decision here
- [ ] Update `authorized` / `structurally_excluded` defaults in this README

*This schema is v2. Amendments require a PR to dev with a note in this README.*
