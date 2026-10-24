#!/usr/bin/env python3
"""Tests for the VibeLearning hooks and the Codex build.

Run from the repository root:
    python3 -m unittest discover -s tests -v
Every test uses a throwaway HOME, so your real ~/.claude and ~/.codex are never touched.
"""
import json
import re
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
                self.assertIn(reminder, self.home.run(HOOKS / "context.py", prompt_event("add a login page")))

    def test_learn_off_silences_teaching_rules(self):
        self.home.flag("off")
        self.assertNotIn("learn while you build", self.start())
        self.assertEqual(self.home.run(HOOKS / "context.py", prompt_event("add a login page")), "")

    def test_new_learner_gets_no_memory_block(self):
        self.assertNotIn("already knows", self.start())
        self.assertEqual(json.loads((self.home.path / ".claude/vibe-learning/learner.json").read_text()), {})


def prompt_event(prompt):
    return json.dumps({"session_id": "test", "cwd": "/projects/shop", "prompt": prompt})


class ContextHookTest(unittest.TestCase):
    """The UserPromptSubmit hook reads each message and tells the AI how to teach it."""

    def setUp(self):
        self.home = FakeHome(self)

    def read(self, prompt):
        return self.home.run(HOOKS / "context.py", prompt_event(prompt))

    def header(self, prompt):
        return self.read(prompt).splitlines()[0]

    def test_detects_what_kind_of_help_is_wanted(self):
        cases = {
            "middleware là gì vậy?": "concept question",
            "what is a closure?": "concept question",
            "làm sao để tự tạo trang đăng nhập": "how to make it",
            "lam sao de tu tao trang dang nhap": "how to make it",  # typed without accents
            "how do I add login with Google?": "how to make it",
            "TypeError: cannot read properties of undefined": "bug",
            "web bị trắng trang sau khi deploy": "bug",
            "mình vẫn chưa hiểu": "confused",
            "tại sao lại dùng useEffect ở đây": "why",
            "giải thích giúp mình hàm này": "explain",
            "Thêm nút đăng xuất vào trang chủ": "build",
            "just do it, add a dark mode toggle": "in a hurry",
            "tắt giải thích đi": "mode switch",
            "ok tiếp": "short follow-up",
        }
        for prompt, intent in cases.items():
            with self.subTest(prompt=prompt):
                self.assertIn(intent, self.header(prompt))

    def test_accents_prevent_false_alarms(self):
        # "lời" (words) is not "lỗi" (error), and praising an explanation is not asking for one.
        header = self.header("lời giải thích này hay đó")
        self.assertNotIn("bug", header)
        self.assertNotIn("explain", header)

    def test_replies_in_vietnamese_with_translated_labels(self):
        for prompt in ("middleware là gì", "middleware la gi"):
            with self.subTest(prompt=prompt):
                self.assertIn("Tự làm thế nào", self.header(prompt))
        self.assertNotIn("Tự làm thế nào", self.header("what is a closure?"))

    def test_stronger_intent_drops_contradicting_advice(self):
        out = self.read("just do it, add a dark mode toggle")
        self.assertNotIn("Blueprint", out)  # no blueprint lecture for someone in a hurry
        out = self.read("làm sao để tự tạo trang đăng nhập")
        self.assertNotIn("Build request", out)  # the how-to advice already covers building

    def test_names_the_concept_and_remembers_the_question(self):
        self.assertIn('"middleware"', self.read("cho mình hỏi middleware là gì"))
        self.assertNotIn("asked what", self.read("cho mình hỏi middleware là gì").split("\n", 2)[1])
        out = self.read("middleware khác gì với route handler?")
        self.assertIn("They asked what middleware means before", out)
        asked = json.loads((self.home.path / ".claude/vibe-learning/learner.json").read_text())["asked"]
        self.assertEqual(asked["middleware"]["count"], 2)
        self.assertEqual(asked["middleware"]["project"], "shop")

    def test_builds_on_terms_learned_in_earlier_sessions(self):
        profile = {"terms": {"api": {"term": "API", "count": 3, "last": "2026-10-01"}}}
        (self.home.path / ".claude/vibe-learning").mkdir(parents=True)
        (self.home.path / ".claude/vibe-learning/learner.json").write_text(json.dumps(profile))
        self.assertIn("Already learned in earlier sessions: API", self.read("gọi API như thế nào cho đúng"))
        self.assertNotIn("Already learned", self.read("thêm trang hồ sơ"))

    def test_points_back_at_earlier_context(self):
        self.assertIn("point back at something earlier", self.read("làm giống cái lúc nãy cho trang hồ sơ"))

    def test_bad_input_falls_back_to_the_plain_reminder(self):
        for stdin in ("not json", "{}", json.dumps({"prompt": ["list"]})):
            with self.subTest(stdin=stdin):
                out = self.home.run(HOOKS / "context.py", stdin)
                self.assertTrue(out == "" or out.startswith("[VibeLearning]"))


class LearnerMemoryTest(unittest.TestCase):
    """The Stop hook saves what the AI taught; session start reminds the AI of it."""
    REPLY = (
        "📘 **Đang làm:** Tạo file `.env`.\n"
        "🔑 **Thuật ngữ:** *Biến môi trường* = tờ giấy nhớ bí mật chương trình đọc khi khởi động.\n"
        "🔑 **Term:** *Middleware* = a checkpoint every request passes through.\n"
        "🧩 **Hard case: \"Double-clicking creates two orders\"**\n"
        "   🤒 **Symptom:** two orders.\n"
    )

    def setUp(self):
        self.home = FakeHome(self)
        self.profile_path = self.home.path / ".claude/vibe-learning/learner.json"

    def stop(self, event):
        self.assertEqual(self.home.run(HOOKS / "learner.py", json.dumps(event)), "")  # never adds tokens

    def profile(self):
        return json.loads(self.profile_path.read_text())

    def test_saves_terms_and_hard_cases_from_the_reply(self):
        self.stop({"cwd": "/projects/shop", "last_assistant_message": self.REPLY})
        terms = self.profile()["terms"]
        self.assertEqual(terms["bien moi truong"]["term"], "Biến môi trường")
        self.assertIn("giấy nhớ", terms["bien moi truong"]["meaning"])
        self.assertEqual(terms["middleware"]["project"], "shop")
        self.assertEqual([c["name"] for c in self.profile()["hard_cases"]], ["Double-clicking creates two orders"])

    def test_reads_only_the_last_turn_from_the_transcript(self):
        def entry(kind, content):
            return json.dumps({"type": kind, "message": {"role": kind, "content": content}})
        lines = [
            entry("user", "first question"),
            entry("assistant", [{"type": "text", "text": "🔑 **Term:** *Old term* = from an earlier turn"}]),
            entry("user", "what is middleware?"),
            entry("assistant", [{"type": "text", "text": "Let me look."}, {"type": "tool_use", "name": "Read"}]),
            entry("user", [{"type": "tool_result", "content": "file text"}]),
            entry("assistant", [{"type": "text", "text": self.REPLY}]),
        ]
        transcript = self.home.path / "transcript.jsonl"
        transcript.write_text("\n".join(lines) + "\n")
        self.stop({"cwd": "/projects/shop", "transcript_path": str(transcript)})
        self.assertNotIn("old term", self.profile()["terms"])
        self.assertIn("middleware", self.profile()["terms"])

    def test_end_of_turn_recap_is_remembered(self):
        # Only the turn's last message reaches the Stop hook, so the 📚 recap carries the earlier 🔑 terms.
        self.stop({"last_assistant_message": "🧾 Mình đã làm\n- ✏️ sửa `app.js`\n📚 **Thuật ngữ mới:** *Hook*, *Stop hook* · *Regex*"})
        self.assertEqual(sorted(self.profile()["terms"]), ["hook", "regex", "stop hook"])

    def test_term_and_recap_in_one_turn_count_once(self):
        self.stop({"last_assistant_message": self.REPLY + "📚 New terms: *Middleware*"})
        self.assertEqual(self.profile()["terms"]["middleware"]["count"], 1)
        self.assertIn("checkpoint", self.profile()["terms"]["middleware"]["meaning"])

    def test_counts_repeats_and_skips_template_placeholders(self):
        self.stop({"last_assistant_message": self.REPLY})
        self.stop({"last_assistant_message": self.REPLY + "🔑 Term: <one new concept> = <definition>"})
        profile = self.profile()
        self.assertEqual(profile["terms"]["middleware"]["count"], 2)
        self.assertEqual(len(profile["hard_cases"]), 1)
        self.assertEqual(len(profile["terms"]), 2)

    def test_session_start_lists_what_they_already_know(self):
        self.stop({"last_assistant_message": self.REPLY})
        out = self.home.run(HOOKS / "session-start.sh", runner="sh")
        self.assertIn("What this learner already knows", out)
        self.assertIn("Biến môi trường, Middleware", out.replace("Middleware, Biến môi trường", "Biến môi trường, Middleware"))
        self.assertIn("Double-clicking creates two orders", out)

    def test_learn_off_stops_recording(self):
        self.home.flag("off")
        self.stop({"last_assistant_message": self.REPLY})
        self.assertFalse(self.profile_path.exists())

    def test_bad_input_never_crashes(self):
        for stdin in ("not json", "{}", json.dumps({"transcript_path": "/nope.jsonl"})):
            with self.subTest(stdin=stdin):
                self.assertEqual(self.home.run(HOOKS / "learner.py", stdin), "")


class PluginLayoutTest(unittest.TestCase):
    SKILLS = ROOT / "skills"
    COMMANDS = ROOT / "commands"
    # Mode command prefix -> flag file. learn's flag means OFF, so learn-on deletes it.
    MODES = {"learn": "off", "practice": "practice", "adhd": "adhd", "type-it": "typeit"}

    def test_no_command_duplicates_a_skill(self):
        skills = {p.name for p in self.SKILLS.iterdir()}
        commands = {p.stem for p in self.COMMANDS.glob("*.md")}
        self.assertEqual(skills & commands, set())

    def test_skill_folder_matches_its_name(self):
        for folder in self.SKILLS.iterdir():
            with self.subTest(skill=folder.name):
                self.assertIn(f"\nname: {folder.name}\n", (folder / "SKILL.md").read_text())

    def test_each_mode_has_deterministic_on_and_off_commands(self):
        flag_path = "~/.claude/vibe-learning.{}"
        for mode, flag in self.MODES.items():
            on = (self.COMMANDS / f"{mode}-on.md").read_text()
            off = (self.COMMANDS / f"{mode}-off.md").read_text()
            with self.subTest(mode=mode):
                # The switch must be a !`...` line the harness runs itself, not an instruction to the AI.
                creates, deletes = (off, on) if flag == "off" else (on, off)
                self.assertRegex(creates, r"(?m)^!`mkdir -p ~/\.claude && touch " + re.escape(flag_path.format(flag)) + "`$")
                self.assertRegex(deletes, r"(?m)^!`rm -f " + re.escape(flag_path.format(flag)) + "`$")
                self.assertIn(f'"$FLAG.{flag}"', (HOOKS / "session-start.sh").read_text())

    def test_every_hook_script_exists(self):
        hooks = json.loads((HOOKS / "hooks.json").read_text())["hooks"]
        for event, groups in hooks.items():
            for hook in (h for g in groups for h in g["hooks"]):
                script = re.search(r"hooks/([\w.-]+)", hook["command"]).group(1)
                with self.subTest(event=event, script=script):
                    self.assertTrue((HOOKS / script).exists())

    def test_skills_never_switch_modes_themselves(self):
        for skill in self.SKILLS.iterdir():
            text = (skill / "SKILL.md").read_text()
            with self.subTest(skill=skill.name):
                self.assertNotRegex(text, r"(touch|rm -f) ~/\.claude/vibe-learning\.")


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

    def test_codex_memory_lives_in_codex_home(self):
        home = FakeHome(self)
        (home.path / ".codex").mkdir()
        home.run(self.codex / "hooks" / "context.py", prompt_event("middleware là gì"))
        self.assertTrue((home.path / ".codex/vibe-learning/learner.json").exists())
        self.assertFalse((home.path / ".claude/vibe-learning/learner.json").exists())

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
