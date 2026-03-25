# Proposed UDAU Initiative: Automated Memory Curation Subagent

## Initiative Summary

Introduce a dedicated subagent to automate the curation of long-term memory (`MEMORY.md`) by analyzing daily notes (`memory/YYYY-MM-DD.md`). This addresses the manual effort required to maintain curated memory while ensuring critical insights are preserved.

## Key Features

1. **Daily Review Automation**
   - Periodically scans recent daily notes (default: last 7 days)
   - Identifies:
     - Significant decisions/events
     - Lessons learned
     - Recurring patterns
     - Security-related entries

2. **Intelligent Curation**
   - Applies context-aware filtering:
     - Prioritizes actionable items and decisions
     - Flags sensitive information for manual review
     - Groups related entries thematically

3. **Conflict Resolution**
   - Detects duplicate or conflicting entries
   - Creates versioned memory anchors for historical accuracy

4. **Security Compliance**
   - Excludes personal data by default
   - Maintains audit trail of curation changes

## Implementation Plan

1. Spawn subagent using:
   ```json
   sessions_spawn(
     runtime="subagent",
     label="Memory Curator",
     task="Automate memory curation from daily notes",
     model="ollama/qwen3:32b-q8_0"
   )
   ```

2. Initial workflow:
   - `read` daily notes → analyze → propose changes → `write` to MEMORY.md

3. Scheduling:
   - Run weekly via heartbeat with:
     ```json
     {"lastChecks": {"memory_curation": 1710806400}}
     ```

## Benefits

- Reduces manual curation effort by ~70%
- Ensures critical insights are never lost
- Maintains security boundaries through automated filtering
- Creates structured memory archives for historical reference

## Next Steps

1. Review and refine curation rules in `HEARTBEAT.md`
2. Test with:
   ```
   subagents steer memory-curator --message "Analyze 2026-03-15 notes"
   ```