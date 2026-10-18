#!/usr/bin/env python3
"""Tests for the VibeLearning hooks and the Codex build.

Run from the repository root:
    python3 -m unittest discover -s tests -v
Every test uses a throwaway HOME, so your real ~/.claude and ~/.codex are never touched.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS = ROOT / "hooks"


class FakeHome:
    """A temporary HOME directory with optional VibeLearning flag files."""

    def __init__(self, test):
        self.dir = tempfile.TemporaryDirectory()
        test.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name)
        (self.path / ".claude").mkdir()

    def flag(self, name, content=""):
        (self.path / ".claude" / f"vibe-learning.{name}").write_text(content)

    def run(self, script, stdin="", runner=sys.executable):
        env = {**os.environ, "HOME": str(self.path)}
        result = subprocess.run([runner, str(script)], input=stdin, capture_output=True, text=True, env=env)
        return result.stdout


def bash_event(command):
    return json.dumps({"session_id": "test", "tool_name": "Bash", "tool_input": {"command": command}})


class TypeItGuardTest(unittest.TestCase):
    BLOCKED = [
        'git add . && git commit -m "fix cart"',
        "cd app && git push origin main",
        "git branch feature-x",
        "git checkout -b login",
        "git reset --hard HEAD~1",
        "git stash",
        "npm install express",
        "npm i -D jest",
        "yarn add react",
        "pnpm remove lodash",
        "npx create-vite my-app",
        "pip install requests",
        "sudo npm install -g typescript",
        "FOO=1 git commit -m x",
    ]
    ALLOWED = [
        "git status",
        "git diff --stat && git log --oneline -5",
        "git -C repo branch -v",
        "git --no-pager log -3",
        "git remote -v",
        "git stash list",
        "git config --get user.name",
        "npm test",
        "npm run build | tail -5",
        "npm ls express",
        "npx tsc --noEmit",
        "pip list",
        "ls -la; echo done",
    ]

    def setUp(self):
        self.home = FakeHome(self)

    def decision(self, command):
        out = self.home.run(HOOKS / "type-it-guard.py", bash_event(command))
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "allow"

    def test_blocks_commands_that_change_things(self):
        self.home.flag("typeit")
        for command in self.BLOCKED:
            with self.subTest(command=command):
                self.assertEqual(self.decision(command), "deny")

    def test_allows_read_only_commands_and_running_the_project(self):
        self.home.flag("typeit")
        for command in self.ALLOWED:
            with self.subTest(command=command):
                self.assertEqual(self.decision(command), "allow")

    def test_does_nothing_when_mode_is_off(self):
        self.assertEqual(self.decision("git push --force"), "allow")

    def test_flag_file_limits_the_guarded_tools(self):
        self.home.flag("typeit", "git")
        self.assertEqual(self.decision("git commit -m x"), "deny")
        self.assertEqual(self.decision("npm install express"), "allow")

    def test_reason_names_the_blocked_commands(self):
        self.home.flag("typeit")
        out = json.loads(self.home.run(HOOKS / "type-it-guard.py", bash_event("git status && git push")))
        # Only the "wants to type ..." part lists commands; the rest of the message mentions git status as an example.
        listed = out["hookSpecificOutput"]["permissionDecisionReason"].split("wants to type ")[1].split(" themselves")[0]
        self.assertEqual(listed, "`git push`")

    def test_bad_input_never_crashes(self):
        self.home.flag("typeit")
        for stdin in ("not json", "{}", json.dumps({"tool_input": {"command": ["git", "push"]}})):
            with self.subTest(stdin=stdin):
                self.home.run(HOOKS / "type-it-guard.py", stdin)  # must not raise


class ActivityLogTest(unittest.TestCase):
    def setUp(self):
        self.home = FakeHome(self)
        self.log_dir = self.home.path / ".claude" / "vibe-learning" / "activity"

    def log(self, session, tool, tool_input):
        event = json.dumps({"session_id": session, "tool_name": tool, "tool_input": tool_input})
        self.assertEqual(self.home.run(HOOKS / "log-activity.py", event), "")  # never adds tokens

    def entries(self, name="latest"):
        return [json.loads(line) for line in (self.log_dir / f"{name}.jsonl").read_text().splitlines()]

    def test_records_edits_and_commands(self):
        self.log("s1", "Edit", {"file_path": "/p/app.js"})
        self.log("s1", "Bash", {"command": "npm test", "description": "Run tests"})
        latest = self.entries()
        self.assertEqual([e["tool"] for e in latest], ["Edit", "Bash"])
        self.assertEqual(latest[0]["target"], "/p/app.js")
        self.assertEqual(latest[1]["detail"], "npm test")

    def test_skips_bookkeeping_tools(self):
        self.log("s1", "TodoWrite", {"todos": []})
        self.log("s1", "Read", {"file_path": "/p/a.py"})
        self.assertEqual([e["tool"] for e in self.entries()], ["Read"])

    def test_new_session_resets_latest_but_keeps_history(self):
        self.log("s1", "Read", {"file_path": "/p/a.py"})
        self.log("s1", "Read", {"file_path": "/p/b.py"})
        self.log("s2", "Read", {"file_path": "/p/c.py"})
        self.assertEqual(len(self.entries()), 1)
        self.assertEqual(len(self.entries("s1")), 2)

    def test_long_commands_are_trimmed(self):
        self.log("s1", "Bash", {"command": "echo " + "x" * 500})
        self.assertLessEqual(len(self.entries()[0]["detail"]), 200)


class SessionHooksTest(unittest.TestCase):
    def setUp(self):
        self.home = FakeHome(self)

    def start(self):
        return self.home.run(HOOKS / "session-start.sh", runner="sh")

    def test_default_session_loads_only_teaching_rules(self):
        out = self.start()
        self.assertIn('"learn while you build" mode is ON', out)
        self.assertNotIn("ADHD-friendly mode is ON", out)
        self.assertTrue((self.home.path / ".claude/vibe-learning/activity/latest.jsonl").exists())

    def test_each_flag_adds_its_rules(self):
        for flag, heading, reminder in [("adhd", "ADHD-friendly mode is ON", "[ADHD]"),
                                        ("practice", "Practice mode is ON", "[Practice]"),
                                        ("typeit", "Type-it-yourself mode is ON", "[Type it yourself]")]:
            with self.subTest(flag=flag):
                self.home.flag(flag)
                self.assertIn(heading, self.start())
                self.assertIn(reminder, self.home.run(HOOKS / "reminder.sh", runner="sh"))

    def test_learn_off_silences_teaching_rules(self):
        self.home.flag("off")
        self.assertNotIn("learn while you build", self.start())
        self.assertEqual(self.home.run(HOOKS / "reminder.sh", runner="sh"), "")


class CodexBuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build-codex.py")], check=True, capture_output=True)
        cls.codex = ROOT / "codex"

    def test_every_command_becomes_a_skill(self):
        for command in (ROOT / "commands").glob("*.md"):
            with self.subTest(command=command.stem):
                self.assertTrue((self.codex / "skills" / command.stem / "SKILL.md").exists())

    def test_no_claude_only_syntax_left(self):
        for path in self.codex.rglob("*"):
            if path.is_file() and path.suffix in (".md", ".sh", ".py", ".json"):
                text = path.read_text()
                with self.subTest(file=str(path.relative_to(ROOT))):
                    for leftover in ("$ARGUMENTS", "~/.claude", "$HOME/.claude", "CLAUDE_PLUGIN_ROOT"):
                        self.assertNotIn(leftover, text)
                    self.assertNotRegex(text, r"(?m)^!`")

    def test_codex_guard_reads_codex_flag(self):
        home = FakeHome(self)
        (home.path / ".codex").mkdir()
        (home.path / ".codex" / "vibe-learning.typeit").write_text("")
        self.assertIn('"deny"', home.run(self.codex / "hooks" / "type-it-guard.py", bash_event("git push")))

    def test_versions_match(self):
        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        codex = json.loads((self.codex / "plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        self.assertEqual(claude["version"], codex["version"])
        self.assertEqual(claude["version"], market["plugins"][0]["version"])


if __name__ == "__main__":
    unittest.main()
