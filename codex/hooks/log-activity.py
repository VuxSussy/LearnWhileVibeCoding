#!/usr/bin/env python3
"""PostToolUse hook: append one line per tool call to the activity log.

`$activity` reads the log back so the learner can see exactly what the AI did,
even after the conversation has been compacted. The hook never prints to stdout,
so it adds no tokens to the conversation.
"""
import json
import os
import sys
import time

LOG_DIR = os.path.expanduser("~/.codex/vibe-learning/activity")
LATEST = os.path.join(LOG_DIR, "latest.jsonl")
SESSION_MARK = os.path.join(LOG_DIR, "latest.session")
# Bookkeeping tools that say nothing about the code itself.
SKIP = {"TodoWrite", "TodoRead", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "ToolSearch", "update_plan"}


def target_of(tool_input):
    """Pick the most useful 'what was touched' value from a tool's input."""
    for key in ("file_path", "notebook_path", "path", "url", "pattern", "query"):
        if tool_input.get(key):
            return str(tool_input[key])
    return ""


def detail_of(tool_input):
    """A short human-readable detail: the shell command or the tool's own description."""
    for key in ("command", "cmd", "description", "prompt"):
        value = tool_input.get(key)
        if value:
            text = " ".join(value) if isinstance(value, list) else str(value)
            return text if len(text) <= 200 else text[:197] + "..."
    return ""


def main():
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    if not tool or tool in SKIP or tool.startswith("mcp__ccd_"):
        return
    tool_input = event.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {"command": str(tool_input)}
    session = event.get("session_id", "unknown")

    entry = {
        "time": time.strftime("%H:%M:%S"),
        "tool": tool,
        "target": target_of(tool_input),
        "detail": detail_of(tool_input),
    }
    os.makedirs(LOG_DIR, exist_ok=True)

    # latest.jsonl always holds the most recently active session only.
    # shortcut: two sessions running at once will keep resetting each other's latest.jsonl;
    # the per-session files below stay complete.
    previous = open(SESSION_MARK).read().strip() if os.path.exists(SESSION_MARK) else ""
    mode = "a" if previous == session else "w"
    if mode == "w":
        with open(SESSION_MARK, "w") as mark:
            mark.write(session)
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    with open(LATEST, mode) as latest:
        latest.write(line)
    with open(os.path.join(LOG_DIR, f"{session}.jsonl"), "a") as per_session:
        per_session.write(line)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Logging must never break the user's session.
