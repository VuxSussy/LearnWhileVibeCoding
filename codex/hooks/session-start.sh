#!/bin/sh
# Inject the teaching rules (plus the ADHD / practice rules when enabled) at the start of every session.
DIR="$(dirname "$0")"
FLAG="$HOME/.codex/vibe-learning"
# Make sure the activity log exists so $activity always has something to read.
mkdir -p "$FLAG/activity" && touch "$FLAG/activity/latest.jsonl"
[ -f "$FLAG.off" ] || cat "$DIR/teaching-rules.md"
[ -f "$FLAG.adhd" ] && cat "$DIR/adhd-rules.md"
[ -f "$FLAG.practice" ] && cat "$DIR/practice-rules.md"
exit 0
