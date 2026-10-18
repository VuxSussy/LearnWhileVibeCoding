---
name: explain
description: Explain a file, snippet, command or concept in plain words (defaults to the latest change). Use when the user types $explain (optionally followed by: [file | snippet | concept]).
---
Explain this for a beginner: (whatever the user wrote after invoking the skill, if anything)
(If empty, explain the most recent change or command in the conversation.)

Structure:
1. **One-sentence summary:** what this thing does.
2. **Each important part:** 2-3 plain lines each, with an everyday analogy.
3. **Flow:** briefly show where the data/program goes, as arrows (A → B → C).
4. **🧮 Algorithms/patterns** used, if any: one line each (skill `algorithm-spotter`).
5. **🎯 Remember:** 1-2 bullet points.
Never use jargon without defining it.
