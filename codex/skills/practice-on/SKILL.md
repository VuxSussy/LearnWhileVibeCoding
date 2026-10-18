---
name: practice-on
description: Turn on practice mode — Claude leaves 3-10 important lines of each new feature for you to write. Use when the user types $practice-on.
---
First, run this shell command: `mkdir -p ~/.codex && touch ~/.codex/vibe-learning.practice`

Practice mode is now ON (remembered for future sessions). From now on apply skill `learn-by-doing`: for each new feature, leave at most one meaningful spot for the user to write.
Tell the user in one line: it's on, they can say "just do it" any time to skip, and `$practice-off` turns it off.
