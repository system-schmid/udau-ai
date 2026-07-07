#!/usr/bin/env bash
# hn-search.sh — HN Algolia API search wrapper for UDAU
#
# Usage:
#   hn-search.sh <query> [options]
#
# Options:
#   --n <num>          Number of results to return (default: 5, max: 20)
#   --type <type>      Content type: story (default), comment, all
#   --sort <sort>      Sort: relevance (default), date
#   --days <num>       Only results from last N days (optional)
#   --json             Output raw JSON (default: formatted text)
#   --url-only         Only print URLs (for piping)
#
# Examples:
#   hn-search.sh "AI agent governance"
#   hn-search.sh "digital identity" --n 10 --sort date
#   hn-search.sh "multi-agent systems" --days 30 --json
#   hn-search.sh "autonomous agents ethics" --url-only
#
# API: https://hn.algolia.com/api/v1/search (no auth required)
#
# UDAU usage norms (from proposals/039-tools-implementation.md):
#   - Query, don't curate: use search as calibration ("has this been said?")
#   - Don't let external signal drive what we write — it informs, not directs
#   - Prefer 3–10 results; avoid bulk fetching unrelated content
#   - No write side effects: this tool is read-only
#
# Dependency: curl, python3 (both standard on macOS/Linux)

set -euo pipefail

BASE_URL="https://hn.algolia.com/api/v1"

# Defaults
QUERY=""
N=5
TYPE="story"
SORT="relevance"
DAYS=""
OUTPUT="text"  # text | json | url-only

usage() {
  grep '^#' "$0" | grep -v '^#!/' | head -35 | sed 's/^# //' | sed 's/^#//'
  exit 1
}

if [[ $# -eq 0 ]]; then
  usage
fi

# Parse arguments
QUERY="$1"
shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --n)
      N="$2"; shift 2 ;;
    --type)
      TYPE="$2"; shift 2 ;;
    --sort)
      SORT="$2"; shift 2 ;;
    --days)
      DAYS="$2"; shift 2 ;;
    --json)
      OUTPUT="json"; shift ;;
    --url-only)
      OUTPUT="url-only"; shift ;;
    --help|-h)
      usage ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: hn-search.sh <query> [--n N] [--type story|comment|all] [--sort relevance|date] [--days N] [--json] [--url-only]" >&2
      exit 1 ;;
  esac
done

# Validate n
if ! [[ "$N" =~ ^[0-9]+$ ]] || [[ "$N" -lt 1 ]] || [[ "$N" -gt 20 ]]; then
  echo "Error: --n must be between 1 and 20" >&2
  exit 1
fi

# Build endpoint
case "$SORT" in
  relevance) ENDPOINT="${BASE_URL}/search" ;;
  date)      ENDPOINT="${BASE_URL}/search_by_date" ;;
  *)
    echo "Error: --sort must be 'relevance' or 'date'" >&2
    exit 1 ;;
esac

# Build tags parameter
case "$TYPE" in
  story)   TAGS_PARAM="story" ;;
  comment) TAGS_PARAM="comment" ;;
  all)     TAGS_PARAM="" ;;
  *)
    echo "Error: --type must be 'story', 'comment', or 'all'" >&2
    exit 1 ;;
esac

# URL-encode query using python3
ENCODED_QUERY=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")

# Build URL
URL="${ENDPOINT}?query=${ENCODED_QUERY}&hitsPerPage=${N}"
if [[ -n "$TAGS_PARAM" ]]; then
  URL="${URL}&tags=${TAGS_PARAM}"
fi

# Add date filter if --days specified
if [[ -n "$DAYS" ]]; then
  if ! [[ "$DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: --days must be a positive integer" >&2
    exit 1
  fi
  CUTOFF=$(python3 -c "import time; print(int(time.time()) - ${DAYS} * 86400)")
  URL="${URL}&numericFilters=created_at_i%3E${CUTOFF}"
fi

# Fetch into a temp file (avoids shell escaping / heredoc issues with JSON content)
TMPFILE=$(mktemp /tmp/hn-search-XXXXXX)
trap 'rm -f "$TMPFILE"' EXIT

curl -s --max-time 10 --fail "$URL" > "$TMPFILE" || {
  echo "Error: HN Algolia API request failed (check network)" >&2
  exit 1
}

# Output
case "$OUTPUT" in
  json)
    python3 -m json.tool "$TMPFILE"
    ;;

  url-only)
    python3 - "$TMPFILE" <<'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
hits = data.get("hits", [])
for h in hits:
    url = h.get("url") or "https://news.ycombinator.com/item?id={}".format(h.get("objectID", ""))
    print(url)
PYEOF
    ;;

  text)
    python3 - "$TMPFILE" "$QUERY" "$DAYS" <<'PYEOF'
import json, sys
from datetime import datetime, timezone

tmpfile = sys.argv[1]
query   = sys.argv[2]
days    = sys.argv[3] if len(sys.argv) > 3 else ""

with open(tmpfile) as f:
    data = json.load(f)

hits  = data.get("hits", [])
total = data.get("nbHits", len(hits))
days_note = " (last {} days)".format(days) if days else ""

if not hits:
    print("No results for: {}".format(query))
    sys.exit(0)

print('HN search: "{}" — {} of {} results{}'.format(query, len(hits), total, days_note))
print("─" * 60)

for i, h in enumerate(hits, 1):
    title    = h.get("title") or h.get("story_title") or "(no title)"
    author   = h.get("author", "?")
    points   = h.get("points") or 0
    comments = h.get("num_comments") or 0
    created  = h.get("created_at", "")
    obj_id   = h.get("objectID", "")
    url      = h.get("url") or "https://news.ycombinator.com/item?id={}".format(obj_id)
    hn_url   = "https://news.ycombinator.com/item?id={}".format(obj_id)

    # Format date
    try:
        dt = datetime.fromisoformat(created.rstrip("Z")).replace(tzinfo=timezone.utc)
        date_str = dt.strftime("%Y-%m-%d")
    except Exception:
        date_str = created[:10] if created else "?"

    print("{}. {}".format(i, title))
    print("   {} | {} pts | {} comments | by {}".format(date_str, points, comments, author))
    print("   {}".format(url))
    if url != hn_url:
        print("   HN:  {}".format(hn_url))
    print()
PYEOF
    ;;
esac
