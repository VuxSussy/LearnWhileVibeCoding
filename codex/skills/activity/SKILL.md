---
name: activity
description: Show everything the AI did in this session — files read and changed, commands run — explained in plain words. Use when the user types $activity (optionally followed by: [last N | files | commands]).
---
Activity log recorded by VibeLearning (one JSON line per tool call: time, tool, target, detail):
First, run this shell command: `tail -n 200 ~/.codex/vibe-learning/activity/latest.jsonl`

Turn this into a plain-language timeline for a beginner. Filter: (whatever the user wrote after invoking the skill, if anything) (e.g. "last 10", "files", "commands"; default: everything).
If the log is empty or missing, rebuild the timeline from the conversation instead and say so in one line.

Format:
1. **🧾 Summary:** one line with counts, e.g. "Read 6 files, changed 3, ran 4 commands."
2. **⏱️ Timeline**, grouped into phases (e.g. "Exploring", "Building", "Testing"), one line per meaningful action:
   `14:02 ✏️ edited src/app.js — added the login check so wrong passwords are rejected`
   Icons: 👀 read/search, ✏️ edit, ➕ create, ▶️ command, 🌐 web, 🧩 other. Merge repeated reads of the same file into one line.
3. **📂 Files changed:** the list of files created/edited, each with one line on why.
4. **🎯 Takeaway:** one line on the most important thing that happened.
Explain commands in plain words (e.g. "`npm test` = run the automatic checks"). Never just echo the raw JSON.
