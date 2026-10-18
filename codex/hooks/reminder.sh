#!/bin/sh
# One-line nudge on every prompt so explanations don't fade out in long conversations.
FLAG="$HOME/.codex/vibe-learning"
[ -f "$FLAG.off" ] || echo "[VibeLearning] Each step: 📘/💡/🔑 (2-3 plain lines). Notable algorithm → 🧮 line. Hard case just solved → 🧩 block. End of a work turn → 🧾 What I did."
[ -f "$FLAG.adhd" ] && echo "[ADHD] Short sentences, bold keywords, update the 🗺️ progress bar, one next action, one question."
[ -f "$FLAG.practice" ] && echo "[Practice] New feature → consider leaving one meaningful 3-10 line TODO(you) for the user to write."
[ -f "$FLAG.typeit" ] && echo "[Type it yourself] Don't run git/npm/pip commands that change things: hand them over as a ⌨️ Your turn checklist with a guide for each, then wait."
exit 0
