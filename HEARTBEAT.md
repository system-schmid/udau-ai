# HEARTBEAT.md

**Canonical location:** repo root (`udau-ai/HEARTBEAT.md`)
**Working copy:** `~/.openclaw/workspace/HEARTBEAT.md`
**Last updated:** 2026-05-12

This file is the durable spec for what Kess does when Pip escalates a WORK tick.
The workspace copy is the live version read by the cron job. Keep them in sync.

---

## When Kess is woken by Pip

Pip has already classified the situation as WORK. Kess does not re-litigate that classification.
Read this file, follow it, then stop.

---

## Step 1 — Situational awareness (read before acting)

```
cat ~/.openclaw/workspace/udau-ai/state/last-run.md
cat ~/.openclaw/workspace/udau-ai/state/open-threads.json
git -C ~/.openclaw/workspace/udau-ai log --oneline dev -10
gh pr list --repo system-schmid/udau-ai --state open --json number,title,labels,createdAt,baseRefName
```

---

## Step 2 — Triage

Work through this decision tree in order. Act on the first match. Do not do multiple tracks in one session.

### Track A — PRs awaiting merge or action

If any open PR targeting main has been open >4 hours and is decision-class (no `auto-merge:operational` label):
- Check if it needs a rebase, a close comment, or just a Slack ping to Valentin.
- Post a concise Slack message to #udau: PR number, title, what's blocking, what you recommend.
- Update `state/open-threads.json` if relevant.

If any open PR has a real merge conflict (mergeStateStatus: DIRTY):
- Assess: rebase or close-with-pointer?
- If rebase is mechanical (site index conflicts, state file conflicts): rebase and force-push.
- If rebase requires content judgment: post to Slack with a clear question for Valentin.

### Track B — Stale dev with pending work

If `state/open-threads.json` has items in `pending` or `in-progress` status and dev is stale >8h:
- Pick the highest-priority pending item.
- Do the work: write the file, commit to a new branch, open a PR to dev.
- Update `state/open-threads.json` to reflect progress.
- Post to Slack: what you built, PR link.

### Track B-S — Strategic thread escalation (age trigger)

If Track A and Track B do not apply, but `state/open-threads.json` has any thread where:
- `owner` is `kess`
- `status` is `pending`
- `created` date is >24h ago
- `last_escalated_at` is absent OR >24h ago

Then: pick the oldest qualifying thread. Do the work (proposal, conversation, or decision draft). One thread per session.

After picking the thread, before acting:
- Write `last_escalated_at` (ISO 8601 UTC) to that thread's entry in `state/open-threads.json`.
- Push the state update directly to dev (no PR).

This prevents Pip from re-escalating the same thread on the next tick. Pip reads `last_escalated_at` and suppresses re-escalation if <24h ago.

Dev liveness check: only fire Track B-S if the most recent dev commit is <72h old. If dev is completely dead, something else is wrong — don't act unilaterally.

### Track C — Clean slate (no open threads, no stale PRs)

If the repo is quiet and clean:
- Read `conversations/` for the most recent conversation. What question does it leave open?
- Read `proposals/` — what's the next logical proposal number? What gap exists?
- Write one substantive proposal or start one conversation. Not boilerplate. Only write it if you have something to say.
- Commit to a new branch, open PR to dev with `auto-merge:operational` label if it passes the three-question test.
- Post to Slack: what you wrote and why.

---

## Step 3 — State update (always, regardless of track)

After acting (or deciding not to act):

```
# Update last-run.md
echo "Last run: $(date -u +%Y-%m-%dT%H:%M:%SZ) — Kess (escalated by Pip tick)" \
  > ~/.openclaw/workspace/udau-ai/state/last-run.md
echo "Track: [A/B/C/none] — [one line summary]" >> \
  ~/.openclaw/workspace/udau-ai/state/last-run.md

# Append to kess-log.md
echo "## $(date -u +%Y-%m-%d) — [short description]" >> \
  ~/.openclaw/workspace/udau-ai/state/kess-log.md
echo "[What happened. What was decided. What's next.]" >> \
  ~/.openclaw/workspace/udau-ai/state/kess-log.md
```

Push state updates to dev directly (no PR needed for state files).

---

## What not to do

- Do not run multiple tracks in one session. Pick one, finish it, stop.
- Do not generate proposals for their own sake. Track C has a "nothing to say → don't write" exit.
- Do not post to Slack on HEARTBEAT_OK ticks — those are already filtered by Pip. Only post when you've done something or need Valentin's input.
- Do not escalate to Maren unless the question is genuinely architectural and beyond Sonnet's judgment.
- Do not open a PR to main directly. Dev only; Valentin merges to main.

---

## Slack format for Kess escalation posts

Keep it short. One message, no thread unless Valentin replies.

```
[emoji] [what happened / what you built]
PR: <url|#number — title> (if applicable)
[One sentence on what's next or what you need from Valentin, if anything]
```

Examples:
- `🔧 Rebased PR #36 onto dev — conflict was in state/ files, resolved by taking dev's current state. Now mergeable.`
- `📝 Opened PR #44 — conversation on [topic]. Auto-merge eligible.`
- `⏳ PR #27 has been open 6h, decision-class, no action from Valentin. Worth a look when you have a moment.`
