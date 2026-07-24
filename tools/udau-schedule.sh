#!/usr/bin/env bash
# udau-schedule.sh — async wake-and-ask scheduler for UDAU
#
# Usage:
#   udau-schedule.sh add "<ISO8601-due>" "<task description>" [--created-by <agent>]
#   udau-schedule.sh list
#   udau-schedule.sh due             # print tasks that are due (overdue or now)
#   udau-schedule.sh done <id>       # mark a task completed
#   udau-schedule.sh remove <id>     # delete a task entry
#
# Examples:
#   udau-schedule.sh add "2026-07-08T10:00:00Z" "revisit PR #77 discussion — is vector memory approach still right?"
#   udau-schedule.sh add "2026-07-10T09:00:00Z" "check if Option B outreach produced any inbound" --created-by kess
#   udau-schedule.sh list
#   udau-schedule.sh due
#
# Format of state/scheduled-tasks.json:
# [
#   {
#     "id": "sched-<timestamp>",
#     "due": "ISO8601",
#     "task": "description",
#     "created_by": "kess",
#     "created_at": "ISO8601",
#     "status": "pending"   // or "done"
#   }
# ]
#
# Pip reads this file on every tick and treats any task where
# status=="pending" and due <= now as WORK, passing the task
# description to Kess.

set -euo pipefail

TASKS_FILE="$(dirname "$0")/../state/scheduled-tasks.json"
TASKS_FILE="$(realpath "$TASKS_FILE")"

# Ensure file exists
if [[ ! -f "$TASKS_FILE" ]]; then
  echo "[]" > "$TASKS_FILE"
fi

now_iso() {
  date -u +%Y-%m-%dT%H:%M:%SZ
}

now_epoch() {
  date -u +%s
}

iso_to_epoch() {
  # Portable: works on macOS (BSD date) and Linux (GNU date)
  local iso="$1"
  if date --version &>/dev/null 2>&1; then
    # GNU date
    date -u -d "$iso" +%s 2>/dev/null || echo 0
  else
    # BSD date (macOS)
    date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "$iso" +%s 2>/dev/null || echo 0
  fi
}

usage() {
  grep '^# ' "$0" | head -20 | sed 's/^# //'
  exit 1
}

cmd="${1:-}"

case "$cmd" in

  add)
    if [[ $# -lt 3 ]]; then
      echo "Usage: udau-schedule.sh add \"<ISO8601-due>\" \"<task>\" [--created-by <agent>]" >&2
      exit 1
    fi
    due="$2"
    task="$3"
    created_by="kess"
    shift 3
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --created-by) created_by="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
      esac
    done
    id="sched-$(date -u +%Y%m%dT%H%M%SZ)"
    created_at="$(now_iso)"
    # Append using python3 (available on macOS/Linux, handles JSON safely)
    python3 - <<PYEOF
import json, sys
with open("$TASKS_FILE") as f:
    tasks = json.load(f)
tasks.append({
    "id": "$id",
    "due": "$due",
    "task": "$task",
    "created_by": "$created_by",
    "created_at": "$created_at",
    "status": "pending"
})
with open("$TASKS_FILE", "w") as f:
    json.dump(tasks, f, indent=2)
    f.write("\n")
print(f"Scheduled: $id  due=$due  task=\"$task\"")
PYEOF
    ;;

  list)
    python3 - <<PYEOF
import json
with open("$TASKS_FILE") as f:
    tasks = json.load(f)
if not tasks:
    print("No scheduled tasks.")
else:
    for t in tasks:
        status = t.get("status", "pending")
        print(f"[{status}] {t['id']}  due={t['due']}  by={t.get('created_by','?')}")
        print(f"         {t['task']}")
PYEOF
    ;;

  due)
    python3 - <<PYEOF
import json, subprocess, sys
from datetime import datetime, timezone

def parse_iso(s):
    # Remove trailing Z if present, parse as UTC
    s = s.rstrip("Z")
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)

now = datetime.now(tz=timezone.utc)
with open("$TASKS_FILE") as f:
    tasks = json.load(f)
due_tasks = [t for t in tasks if t.get("status") == "pending" and parse_iso(t["due"]) <= now]
if not due_tasks:
    print("HEARTBEAT_OK — no tasks due")
    sys.exit(0)
print(f"WORK — {len(due_tasks)} task(s) due:")
for t in due_tasks:
    print(f"  [{t['id']}] due={t['due']}: {t['task']}")
sys.exit(1)
PYEOF
    ;;

  done)
    if [[ $# -lt 2 ]]; then
      echo "Usage: udau-schedule.sh done <id>" >&2; exit 1
    fi
    task_id="$2"
    python3 - <<PYEOF
import json
with open("$TASKS_FILE") as f:
    tasks = json.load(f)
found = False
for t in tasks:
    if t["id"] == "$task_id":
        t["status"] = "done"
        found = True
        break
if not found:
    print(f"Error: task '$task_id' not found", flush=True)
    exit(1)
with open("$TASKS_FILE", "w") as f:
    json.dump(tasks, f, indent=2)
    f.write("\n")
print(f"Marked done: $task_id")
PYEOF
    ;;

  remove)
    if [[ $# -lt 2 ]]; then
      echo "Usage: udau-schedule.sh remove <id>" >&2; exit 1
    fi
    task_id="$2"
    python3 - <<PYEOF
import json
with open("$TASKS_FILE") as f:
    tasks = json.load(f)
before = len(tasks)
tasks = [t for t in tasks if t["id"] != "$task_id"]
if len(tasks) == before:
    print(f"Error: task '$task_id' not found", flush=True)
    exit(1)
with open("$TASKS_FILE", "w") as f:
    json.dump(tasks, f, indent=2)
    f.write("\n")
print(f"Removed: $task_id")
PYEOF
    ;;

  *)
    usage
    ;;
esac
