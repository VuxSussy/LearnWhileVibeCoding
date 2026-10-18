#!/usr/bin/env python3
"""Generate the Codex build of the plugin (the codex/ folder) from the Claude Code sources.

The Claude Code version is the source of truth: edit skills/, commands/ or hooks/, then run
    python3 scripts/build-codex.py
Never edit codex/ by hand; it is overwritten on every build.
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "codex"
COMMANDS = sorted(p.stem for p in (ROOT / "commands").glob("*.md"))


def to_codex_text(text):
    """Rewrite the parts that only make sense in Claude Code into Codex terms."""
    text = text.replace("~/.claude", "~/.codex").replace("$HOME/.claude", "$HOME/.codex")
    # /explain, /hard-case... -> $explain, $hard-case (Codex invokes skills with $)
    names = "|".join(sorted(map(re.escape, COMMANDS), key=len, reverse=True))
    text = re.sub(rf"(?<![\w/.~-])/({names})(?![\w-])", r"$\1", text)
    text = re.sub(r"\$(learn|adhd|practice)-on\|off", r"$\1-on / $\1-off", text)
    return text


def split_frontmatter(text):
    """Split '---\\nkey: value\\n---\\nbody' into (dict, body)."""
    _, head, body = text.split("---\n", 2)
    meta = {}
    for line in head.splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body


def convert_command(name, text):
    """Turn a Claude Code slash command into a Codex skill."""
    meta, body = split_frontmatter(text)
    description = (
        f"{meta['description']}. Use when the user types ${name}"
        + (f" (optionally followed by: {meta['argument-hint']})" if "argument-hint" in meta else "")
        + "."
    )

    # Claude Code runs a !`command` line before reading the prompt; Codex has no such feature,
    # so turn it into an instruction telling Codex to run the command itself.
    body = re.sub(r"^!`(.+)`$", r"First, run this shell command: `\1`", body, flags=re.MULTILINE)
    # Claude Code replaces $ARGUMENTS with what the user typed after the command; in a Codex skill
    # that text only exists in the user's message, so point straight at it.
    body = body.replace("$ARGUMENTS", "(whatever the user wrote after invoking the skill, if anything)")

    body = to_codex_text(body)
    return f"---\nname: {name}\ndescription: {description}\n---\n{body}"


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "skills").mkdir(parents=True)

    # 1. Shared skills: Codex reads this exact SKILL.md format.
    for skill in (ROOT / "skills").iterdir():
        dest = OUT / "skills" / skill.name
        dest.mkdir()
        (dest / "SKILL.md").write_text(to_codex_text((skill / "SKILL.md").read_text()))

    # 2. Slash commands -> skills (Codex plugins have no commands/ folder).
    for cmd in (ROOT / "commands").glob("*.md"):
        dest = OUT / "skills" / cmd.stem
        dest.mkdir()
        (dest / "SKILL.md").write_text(convert_command(cmd.stem, cmd.read_text()))

    # 3. Hooks: same SessionStart / UserPromptSubmit / PostToolUse events; toggles live in ~/.codex.
    shutil.copytree(ROOT / "hooks", OUT / "hooks")
    for f in (OUT / "hooks").iterdir():
        f.write_text(to_codex_text(f.read_text()))
    hooks = json.loads((OUT / "hooks" / "hooks.json").read_text().replace("CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT"))
    (OUT / "hooks" / "hooks.json").write_text(json.dumps(hooks, ensure_ascii=False, indent=2) + "\n")
    for f in [*(OUT / "hooks").glob("*.sh"), *(OUT / "hooks").glob("*.py")]:
        f.chmod(0o755)

    # 4. Manifest: Codex reads plugin.json at the plugin root.
    claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        **{k: claude[k] for k in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")},
        "extensions": {"com.openai": {"interface": {
            "displayName": "VibeLearning",
            "shortDescription": "Learn while you vibe code",
            "developerName": claude["author"]["name"],
            "category": "Education",
            "defaultPrompt": "$explain",
        }}},
    }
    (OUT / "plugin.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    shutil.copy(ROOT / "LICENSE", OUT / "LICENSE")
    print(f"Built {OUT.relative_to(ROOT)}/ with {len(list((OUT / 'skills').iterdir()))} skills")


if __name__ == "__main__":
    build()
