#!/bin/sh
# Inject the teaching rules (plus the ADHD / practice / type-it rules when enabled) at the start of every session,
# followed by what this learner already knows from past sessions (hooks/learner.py).
DIR="$(dirname "$0")"
FLAG="$HOME/.claude/vibe-learning"
# Make sure the activity log and the learner profile exist so /activity and /progress always have something to read.
mkdir -p "$FLAG/activity" && touch "$FLAG/activity/latest.jsonl"
[ -f "$FLAG/learner.json" ] || echo '{}' > "$FLAG/learner.json"
if [ ! -f "$FLAG.off" ]; then
  cat "$DIR/teaching-rules.md"
  python3 "$DIR/learner.py" summary 2>/dev/null
fi
[ -f "$FLAG.adhd" ] && cat "$DIR/adhd-rules.md"
[ -f "$FLAG.practice" ] && cat "$DIR/practice-rules.md"
[ -f "$FLAG.typeit" ] && cat "$DIR/typeit-rules.md"
exit 0
