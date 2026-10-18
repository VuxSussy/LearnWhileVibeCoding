#!/usr/bin/env python3
"""PreToolUse hook for type-it-yourself mode.

While ~/.claude/vibe-learning.typeit exists, block shell commands that use git or a
package manager to *change* something, so the AI hands them to the user to type instead.
Read-only commands (git status, git diff, npm ls...) stay allowed so the AI can still
look around and check the user's work.

The flag file may list the tools to guard (e.g. "git" or "git npm"); empty means all of DEFAULT_TOOLS.
"""
import json
import os
import re
import shlex
import sys

FLAG = os.path.expanduser("~/.claude/vibe-learning.typeit")
DEFAULT_TOOLS = {"git", "npm", "npx", "yarn", "pnpm", "bun", "pip", "pip3"}
PACKAGE_MANAGERS = {"npm", "yarn", "pnpm", "bun"}

# git subcommands that only look at the repository.
GIT_READ_ONLY = {
    "status", "diff", "log", "show", "blame", "rev-parse", "ls-files", "ls-tree", "describe",
    "shortlog", "grep", "help", "version", "--version", "-v", "cat-file", "reflog", "whatchanged",
}
# Package manager subcommands that change dependencies or the project.
PACKAGE_CHANGES = {
    "install", "i", "add", "ci", "uninstall", "remove", "rm", "un", "r", "update", "upgrade", "up",
    "init", "create", "publish", "link", "unlink", "dedupe", "prune", "version", "pkg", "patch",
}
PIP_CHANGES = {"install", "uninstall", "download", "wheel"}
WRAPPERS = {"sudo", "command", "time", "env", "exec", "nohup"}


def git_is_read_only(args):
    if not args:
        return True
    sub, rest = args[0], args[1:]
    if sub in GIT_READ_ONLY:
        return True
    # These are read-only only in their "list" forms.
    if sub == "branch":
        return all(a in ("-a", "-r", "-v", "-vv", "--list", "--all", "--remotes", "--show-current") for a in rest)
    if sub == "remote":
        return not rest or rest[0] in ("-v", "show", "get-url")
    if sub == "tag":
        return not rest or rest[0] in ("-l", "--list")
    if sub == "stash":
        return bool(rest) and rest[0] in ("list", "show")
    if sub == "config":
        return any(a in ("--get", "--list", "-l", "--get-all") for a in rest)
    return False


def blocked_tool(segment, tools):
    """Return the guarded command found in one shell segment, or None if it may run."""
    try:
        words = shlex.split(segment)
    except ValueError:
        words = segment.split()
    # Skip leading VAR=value assignments and wrappers like sudo.
    while words and (re.match(r"^\w+=", words[0]) or words[0] in WRAPPERS):
        words = words[1:]
    if not words:
        return None
    tool, args = os.path.basename(words[0]), words[1:]
    if tool not in tools:
        return None
    if tool == "git":
        # Drop global options like `-C path` before the subcommand.
        while args and args[0].startswith("-") and args[0] not in ("--version", "-v"):
            args = args[2:] if args[0] in ("-C", "-c") else args[1:]
        return None if git_is_read_only(args) else segment
    if tool in PACKAGE_MANAGERS:
        return segment if args and args[0] in PACKAGE_CHANGES else None
    if tool in ("pip", "pip3"):
        return segment if args and args[0] in PIP_CHANGES else None
    if tool == "npx":
        # Scaffolders (npx create-react-app ...) set up projects; running other tools is fine.
        return segment if args and re.match(r"^(create-|@[\w-]+/create)", args[0]) else None
    return None


def main():
    if not os.path.exists(FLAG):
        return
    tools = set(open(FLAG).read().split()) or DEFAULT_TOOLS
    event = json.load(sys.stdin)
    command = (event.get("tool_input") or {}).get("command")
    if isinstance(command, list):
        command = " ".join(command)
    if not command:
        return

    segments = [s.strip() for s in re.split(r"&&|\|\||;|\||\n", command) if s.strip()]
    hits = [hit for hit in (blocked_tool(s, tools) for s in segments) if hit]
    if not hits:
        return

    listed = ", ".join(f"`{h}`" for h in hits)
    reason = (
        f"VibeLearning type-it-yourself mode is ON: the user wants to type {listed} themselves to learn it. "
        "Do not run it, and do not work around it (another tool, a script, or editing files such as "
        "package.json or .git by hand). Add it to the ⌨️ Your turn checklist (skill type-it-yourself) "
        "with its explanation, then stop and wait until the user says they ran it. "
        "Read-only checks like `git status` or `npm ls` are still allowed for verifying their work."
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # A broken guard must never break the session; it just lets the command through.
