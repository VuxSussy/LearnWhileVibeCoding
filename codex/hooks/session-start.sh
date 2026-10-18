#!/bin/sh
# Bơm luật dạy học (và luật ADHD / practice nếu đã bật) vào đầu mỗi session.
DIR="$(dirname "$0")"
FLAG="$HOME/.codex/vibe-learning"
[ -f "$FLAG.off" ] || cat "$DIR/teaching-rules.md"
[ -f "$FLAG.adhd" ] && cat "$DIR/adhd-rules.md"
[ -f "$FLAG.practice" ] && cat "$DIR/practice-rules.md"
exit 0
