#!/usr/bin/env python3
"""Sinh bản plugin cho Codex (thư mục codex/) từ bản Claude Code.

Bản Claude là bản gốc: sửa skills/, commands/, hooks/ rồi chạy lại
    python3 scripts/build-codex.py
Không sửa tay trong codex/ vì sẽ bị ghi đè.
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "codex"
COMMANDS = sorted(p.stem for p in (ROOT / "commands").glob("*.md"))


def to_codex_text(text):
    """Đổi những chỗ chỉ đúng với Claude Code sang cách nói của Codex."""
    text = text.replace("~/.claude", "~/.codex").replace("$HOME/.claude", "$HOME/.codex")
    # /explain, /hard-case... -> $explain, $hard-case (Codex gọi skill bằng $)
    names = "|".join(sorted(map(re.escape, COMMANDS), key=len, reverse=True))
    text = re.sub(rf"(?<![\w/.~-])/({names})(?![\w-])", r"$\1", text)
    text = re.sub(r"\$(learn|adhd|practice)-on\|off", r"$\1-on / $\1-off", text)
    return text


def split_frontmatter(text):
    """Tách '---\\nkey: value\\n---\\nbody' thành (dict, body)."""
    _, head, body = text.split("---\n", 2)
    meta = {}
    for line in head.splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body


def convert_command(name, text):
    """Biến một slash command của Claude thành một skill của Codex."""
    meta, body = split_frontmatter(text)
    description = (
        f"{meta['description']}. Dùng khi người dùng gõ ${name}"
        + (f" (có thể kèm: {meta['argument-hint']})" if "argument-hint" in meta else "")
        + "."
    )

    # Claude tự chạy dòng !`lệnh` trước khi đọc prompt; Codex không có tính năng này,
    # nên đổi thành lời dặn để Codex tự chạy lệnh đó.
    body = re.sub(r"^!`(.+)`$", r"Trước tiên, chạy lệnh shell sau: `\1`", body, flags=re.MULTILINE)
    # Claude thay $ARGUMENTS bằng chữ người dùng gõ kèm lệnh; trong skill của Codex
    # chữ đó chỉ nằm trong tin nhắn của người dùng, nên trỏ thẳng tới nó.
    body = body.replace("$ARGUMENTS", "(phần người dùng viết kèm khi gọi skill, nếu có)")

    body = to_codex_text(body)
    return f"---\nname: {name}\ndescription: {description}\n---\n{body}"


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "skills").mkdir(parents=True)

    # 1. Skill dùng chung: Codex đọc đúng định dạng SKILL.md này.
    for skill in (ROOT / "skills").iterdir():
        dest = OUT / "skills" / skill.name
        dest.mkdir()
        (dest / "SKILL.md").write_text(to_codex_text((skill / "SKILL.md").read_text()))

    # 2. Slash command -> skill (plugin Codex không có thư mục commands/).
    for cmd in (ROOT / "commands").glob("*.md"):
        dest = OUT / "skills" / cmd.stem
        dest.mkdir()
        (dest / "SKILL.md").write_text(convert_command(cmd.stem, cmd.read_text()))

    # 3. Hook: cùng sự kiện SessionStart / UserPromptSubmit, cờ bật/tắt nằm ở ~/.codex.
    shutil.copytree(ROOT / "hooks", OUT / "hooks")
    for f in (OUT / "hooks").iterdir():
        f.write_text(to_codex_text(f.read_text()))
    hooks = json.loads((OUT / "hooks" / "hooks.json").read_text().replace("CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT"))
    (OUT / "hooks" / "hooks.json").write_text(json.dumps(hooks, ensure_ascii=False, indent=2) + "\n")
    for f in (OUT / "hooks").glob("*.sh"):
        f.chmod(0o755)

    # 4. Manifest: Codex đọc plugin.json ở gốc plugin.
    claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        **{k: claude[k] for k in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")},
        "extensions": {"com.openai": {"interface": {
            "displayName": "LearnWhileVibeCoding",
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
