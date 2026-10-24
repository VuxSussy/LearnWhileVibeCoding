---
name: progress
description: What you've learned so far, across every session — terms, concepts you were unsure about, hard cases — and what to review next. Use when the user types $progress (optionally followed by: [project name - optional]).
---
VibeLearning's learner memory (JSON: `terms` the AI taught with 🔑, `asked` = concepts the user asked "what is X?" about, `hard_cases` = 🧩 cases they went through; each with counts, dates and project):
First, run this shell command: `cat ~/.codex/vibe-learning/learner.json`

Turn it into a short, encouraging progress report for a beginner. Filter to this project if given: (whatever the user wrote after invoking the skill, if anything)

1. **📈 In numbers:** one line, e.g. "42 terms learned in 5 projects, 6 hard cases solved."
2. **✅ Solid:** terms seen in several sessions or projects, grouped by topic (web, data, git, tools...), names only.
3. **🟡 Still shaky:** concepts they asked about (most-asked first), each with a fresh one-line explanation and one tiny example.
4. **🧩 Hard cases you've beaten:** the names, newest first, at most 5.
5. **🎯 Review next:** the 2-3 most useful things to revisit, and the command for each (`$explain <term>`, `$rebuild <feature>`, `$quiz <topic>`).

If the memory is empty, say that it fills up as Claude teaches (every `🔑 Term` and `🧩 Hard case` is saved) and when they ask "what is X?".
The file lives at `~/.codex/vibe-learning/learner.json`; deleting it resets the memory.
