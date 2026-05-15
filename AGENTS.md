# UDAU Agent Roster

## Sub-Agent Roster

| Name | Model | Role |
|------|-------|------|
| **Kess** | Claude Sonnet 4.6 | Orchestrator — coordinates, synthesizes, routes |
| **Vera** | Claude Haiku 4.5 (trial through 2026-06-11) | Strategic reasoning sub-agent |
| **Maren** | Claude Opus 4.7 | Deep reasoning sub-agent — called when others hit open water |
| **Pip** | Qwen3.5 122B (qwen3.5:122b-a10b) | Principles, quick checks — ask Pip first |

---

## Agent Scope Contracts

**Required since:** 2026-05-13 | **Proposal:** [005](proposals/005-agent-scope-contracts.md) | **Schema:** [state/scope-contracts/README.md](state/scope-contracts/README.md)

Every sub-agent spawn must be preceded by a Scope Contract. This is Phase 1 (manual). Do not skip it.

### Pre-spawn checklist

**Step 1 — Write the contract file**

Create `state/scope-contracts/<task_id>.json` before calling `sessions_spawn`. Use the schema in `state/scope-contracts/README.md`. Task ID format: `udau-<spawner>-<YYYYMMDD>-<NNN>`.

Minimal contract template:

```json
{
  "task_id": "udau-kess-20260513-001",
  "spawned_at": "<ISO 8601 UTC>",
  "spawner": "kess",
  "model": "<model-id>",
  "task_summary": "<one sentence>",
  "authorized": {
    "tools": ["read", "write", "exec"],
    "paths": ["<working directory tree>"],
    "external_calls": [],
    "spawn_depth": 0
  },
  "forbidden": {
    "tools": ["message", "tts"],
    "paths": ["/Users/udau/.openclaw/workspace/udau-ai/state/", "/Users/udau/.openclaw/workspace/udau-ai/proposals/"],
    "external_calls": []
  },
  "checkpoints": [
    { "after_step": "write", "verify": "path_in_authorized" },
    { "after_step": "sessions_spawn", "verify": "depth_within_limit" }
  ],
  "drift_threshold": "warning"
}
```

**Step 2 — Inject the contract block into the sub-agent task prompt**

Append this to the task description passed to `sessions_spawn`:

```
[SCOPE CONTRACT: <task_id>]
Authorized tools: <comma-separated list>
Authorized paths: <comma-separated list>
Forbidden tools: <comma-separated list>
Spawn depth: <N>
Report this contract ID in your final output.
```

**Step 3 — Log the spawn in drift-log.md**

```
[<timestamp>] SPAWN   task_id=<id> spawner=kess model=<model> summary="<one-line>"
```

### Post-completion checklist

**Step 4 — Pull session history**

Use `sessions_history` for the sub-agent's session key. Scan tool calls.

**Step 5 — Verify checkpoints**

Check each tool call against `authorized` and `forbidden`. Any deviation from `forbidden` is Level 2+. Any tool not in `authorized` and not in `forbidden` is Level 1.

**Step 6 — Log result in drift-log.md**

```
[<timestamp>] VERIFY  task_id=<id> result=PASS notes="<brief>"
```

**Step 7 — If Level 2+, follow the Drift Severity Framework**

See `state/scope-contracts/README.md` for the full framework. Level 3 = halt + Slack Valentin.

### Defaults

- `spawn_depth: 0` — no sub-sub-agents unless the task explicitly requires it
- `forbidden.tools` always includes `message` and `tts` unless the sub-agent is explicitly tasked with external communication
- `forbidden.paths` always includes `state/` and `proposals/` unless the sub-agent is a state-management or proposal-authoring task
- `drift_threshold: "warning"` — suppress Level 1 advisories by default
