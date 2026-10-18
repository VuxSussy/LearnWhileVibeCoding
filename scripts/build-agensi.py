#!/usr/bin/env python3
"""Package VibeLearning as a single standalone skill for agensi.io.

Agensi accepts one skill per zip: one folder with SKILL.md at its root, text files only.
Hooks and mode-switch commands can't ship there, so the core teaching rules become SKILL.md
and every other skill becomes a reference file it points to.
    python3 scripts/build-agensi.py   ->   dist/vibe-learning.zip
"""
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = DIST / "vibe-learning"
REFERENCES = ["hard-case", "functions", "algorithms", "practice", "type-it", "i-have-adhd"]


def strip_frontmatter(text):
    return text.split("---\n", 2)[2].lstrip("\n")


def standalone(text):
    """Remove the parts that only work inside the full plugin (hooks, flag files, -on/-off commands)."""
    text = re.sub(r"## Turning the mode on or off\n.*?\n\n", "", text, flags=re.S)
    text = re.sub(r"`/(learn|practice|type-it|adhd)-(on|off)`", "asking for it", text)
    text = text.replace("skill `", "reference `")
    text = text.replace('# VibeLearning: "learn while you build" mode is ON', "# VibeLearning: learn while you build")
    text = re.sub(r"(?m)^- If the guard hook blocks a command.*\n", "", text)
    text = text.replace(" The full log is available via `/activity`.", "").replace("suggest `/hard-case`", "offer the deep dive below").replace("from `/algorithms`", "from `references/algorithms.md`")
    text = re.sub(r"For more depth the user can type [^.]*\.", "For more depth, use the guides in `references/`.", text)
    return text


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "references").mkdir(parents=True)
    version = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"]

    core = (ROOT / "hooks" / "teaching-rules.md").read_text()
    core = core.split("\nLearning commands:")[0]  # the command list belongs to the plugin
    (OUT / "SKILL.md").write_text(f"""---
name: vibe-learning
description: Learn while you vibe code. Explains every step in 2-3 plain lines, breaks down hard bugs the AI just solved, tours the functions in a file, names the algorithms in the code, lets the user write key lines or type git/npm commands themselves, and has an ADHD-friendly style. Use when the user is a beginner, says "explain", "I don't understand", "teach me", "why did that fix it", "what's in this file", "what algorithm is this", "I want to learn git", or "I have ADHD".
---

{standalone(core).strip()}

## Deeper guides
Read the matching file before doing one of these:

- `hard-case.md`: right after solving a tricky bug, or when the user asks why a fix worked.
- `functions.md`: when the user asks what's in a file or how a function works.
- `algorithms.md`: when the user asks what algorithm/pattern the code uses or whether it is fast enough.
- `practice.md`: when the user wants to write part of the code themselves.
- `type-it.md`: when the user wants to learn git/npm/pip by typing the commands themselves.
- `i-have-adhd.md`: when the user has ADHD, can't focus, or feels overwhelmed by text.
""")
    for name in REFERENCES:
        body = strip_frontmatter((ROOT / "skills" / name / "SKILL.md").read_text())
        (OUT / "references" / f"{name}.md").write_text(standalone(body))
    (OUT / "README.md").write_text(f"""# VibeLearning (skill) v{version}

Learn while you vibe code: plain 2-3 line explanations for every step, hard-bug breakdowns,
function tours, algorithm spotting, practice tasks, type-it-yourself terminal checklists, and an ADHD-friendly style.

## Install

Unzip so the `vibe-learning/` folder lands in your tool's skills folder:

| Tool | Folder |
|---|---|
| Claude Code | `~/.claude/skills/vibe-learning/` (or `.claude/skills/` in a project) |
| OpenAI Codex | `~/.agents/skills/vibe-learning/` (or `.agents/skills/` in a repo) |
| Other Agent Skills tools | their skills folder; the format is the open SKILL.md standard |

Start a new session. The skill kicks in on its own when it fits; in Codex you can also call it with `$vibe-learning`.

This is the standalone skill. The full Claude Code / Codex plugin adds automatic hooks
(rules at session start, an activity log, a guard that stops the AI from running git for you)
and on/off commands: https://github.com/VuxSussy/VibeLearning

License: MIT
""")

    zip_path = DIST / "vibe-learning.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(OUT.rglob("*")):
            if path.is_file() and path.name != ".DS_Store":
                z.write(path, path.relative_to(DIST))
    print(f"Built {zip_path.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
