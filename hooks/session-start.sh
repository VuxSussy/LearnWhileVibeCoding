#!/bin/sh
# Bơm luật dạy học (và luật ADHD nếu đã bật) vào đầu mỗi session.
DIR="$(dirname "$0")"
[ -f "$HOME/.claude/learn-while-vibe-coding.off" ] || cat "$DIR/teaching-rules.md"
[ -f "$HOME/.claude/learn-while-vibe-coding.adhd" ] && cat "$DIR/adhd-rules.md"
exit 0
