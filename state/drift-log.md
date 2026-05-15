# UDAU Drift Log

**Purpose:** Records every sub-agent spawn event and post-completion verification result under the Agent Scope Contracts protocol.  
**Schema:** [state/scope-contracts/README.md](scope-contracts/README.md)  
**Proposal:** [005-agent-scope-contracts](../proposals/005-agent-scope-contracts.md)

---

## Format

Each entry is one of:

- **SPAWN** — contract written, sub-agent launched
- **VERIFY** — post-completion verification result (PASS / LEVEL-1 / LEVEL-2 / LEVEL-3)
- **ESCALATION** — human notification sent (Level 3 only)

```
[YYYY-MM-DDTHH:MM:SSZ] SPAWN   task_id=<id> spawner=<agent> model=<model> summary="<one-line>"
[YYYY-MM-DDTHH:MM:SSZ] VERIFY  task_id=<id> result=PASS|LEVEL-1|LEVEL-2|LEVEL-3 notes="<detail>"
[YYYY-MM-DDTHH:MM:SSZ] ESCALATION task_id=<id> level=3 action="<what was done>"
```

---

## Log

*No entries yet. First entry will appear when Kess issues its first formal Scope Contract.*

---

*Log started: 2026-05-13. Maintained by Kess.*
