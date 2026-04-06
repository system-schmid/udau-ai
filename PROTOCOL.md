# PROTOCOL.md — Session Close Protocol

_One page. Read it. Follow it._

---

## Session Open Checklist

1. **Read `CONTEXT.md`** — know where we left off before doing anything
2. **Scan `state/last-run.md`** — what was Kess last doing?
3. **Check `state/open-threads.json`** — any pending work items?
4. Then proceed with the session's actual task.

## Session Close Checklist

Only required when something significant happened. Skip if it was a trivial info-only session.

1. **Update `CONTEXT.md`:**
   - Set "Last Active" to today + your agent name
   - Add any new Open Threads (or close resolved ones)
   - Log significant decisions under "Recent Decisions"
   - Flag anything for follow-up

2. **Write a `memory/` note** if:
   - A major decision was made
   - A proposal was drafted or closed
   - Something happened that future-you should know about
   - Format: `memory/YYYY-MM-DD-topic.md`

3. **Update `state/last-run.md`** (Kess especially):
   - Date, what was done, what's next

4. **Commit and push to dev:**
   ```
   git add CONTEXT.md memory/ state/ PROTOCOL.md
   git commit -m "chore: session close [agent-name] [date]"
   git push origin dev
   ```

---

## What Goes in Memory vs. What Doesn't

**Write a memory note for:**
- Proposal drafts, ratifications, closures
- Agent identity or roster changes
- Significant decisions about UDAU direction
- Anything Valentin explicitly asked us to remember

**Don't write a memory note for:**
- Routine file edits
- Trivial Q&A sessions
- Things already captured in proposals

---

## Proposal Lifecycle

```
Draft → Accepted → In Progress → Implemented
                              → Closed (Archived)
```

Update the status field in the proposal file when it changes. Proposals over 90 days with no owner or timeline → mark `Closed (Archived)` and add a one-line reason.

---

## On Cost Awareness

Pip runs first. Vera when Pip isn't enough. Maren when there's genuinely open water with no obvious shore. Spawning Maren for a simple task is wasteful; we have a budget and it's shared.

---

_This protocol exists so the next session doesn't start blank. Keep it short. Update it if it's wrong._
