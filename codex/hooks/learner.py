#!/usr/bin/env python3
"""The learner profile: what this person has already learned, remembered across sessions.

Three ways in:
- Stop hook (no arguments): read the AI's last reply and save the 🔑 terms it taught
  and the 🧩 hard cases it explained.
- `learner.py summary`: print a short "already knows" block (session-start.sh adds it to the rules).
- `import learner`: context.py looks terms up while reading the user's next message,
  and records the "what is X?" questions the user asks.
The profile is plain JSON at ~/.codex/vibe-learning/learner.json, so $progress (and you) can read it.
The hook never prints anything, so it adds no tokens to the conversation.
"""
import json
import os
import re
import sys
import time
import unicodedata

PROFILE = os.path.expanduser("~/.codex/vibe-learning/learner.json")
OFF_FLAG = os.path.expanduser("~/.codex/vibe-learning.off")
# Keep the file small: forget the least recently seen entries first.
LIMITS = {"terms": 300, "asked": 100}
MAX_CASES = 30

# `🔑 **Term:** *Environment variable* = a "secret sticky note"...` (the label is translated, so accept any).
TERM_LINE = re.compile(r"🔑\s*\**[^:\n*]{1,30}:\**\s*(.+)")
TERM_SPLIT = re.compile(r"\s*(?:=|—|–)\s*|:\s+")
# `📚 **New terms:** *Hook*, *Stop hook*`: the end-of-turn recap. The Stop hook only gets the turn's
# last message, so this line is what reliably reaches it when the 🔑 lines came earlier in the turn.
RECAP_LINE = re.compile(r"📚\s*\**[^:\n*]{1,30}:\**\s*(.+)")
RECAP_SPLIT = re.compile(r"\s*[,·;]\s*")
# `🧩 **Hard case: "Double-clicking creates two orders"**`
CASE_LINE = re.compile(r"🧩\s*\**[^:\n*]{1,30}:\s*(.+)")
DECORATION = " *_`\"'“”‘’«»"


def plain(text):
    """Lowercase without accents ('Lỗi Đây' -> 'loi day'), so text typed without accents still matches."""
    text = text.lower().replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


def key(term):
    return re.sub(r"\s+", " ", plain(term)).strip(DECORATION)


def load():
    try:
        with open(PROFILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    data.setdefault("terms", {})
    data.setdefault("asked", {})
    data.setdefault("hard_cases", [])
    return data


def save(data):
    for bucket, limit in LIMITS.items():
        trim(data[bucket], limit)
    data["hard_cases"] = data["hard_cases"][-MAX_CASES:]
    os.makedirs(os.path.dirname(PROFILE), exist_ok=True)
    # Write to a temporary file first, then swap it in, so a crash never leaves half a file.
    tmp = PROFILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    os.replace(tmp, PROFILE)


def trim(bucket, limit):
    """Drop the oldest entries once a bucket is over its limit."""
    if len(bucket) <= limit:
        return
    oldest = sorted(bucket, key=lambda k: (bucket[k].get("last", ""), bucket[k].get("count", 0)))
    for k in oldest[: len(bucket) - limit]:
        del bucket[k]


def touch(bucket, term, project, meaning=""):
    """Add one sighting of a term: bump its count and date, keep the first meaning we saw."""
    k = key(term)
    if not k:
        return
    today = time.strftime("%Y-%m-%d")
    entry = bucket.get(k) or {"term": term, "count": 0, "first": today}
    entry["count"] += 1
    entry["last"] = today
    entry["project"] = project
    if meaning and not entry.get("meaning"):
        entry["meaning"] = meaning
    bucket[k] = entry


def clean(text, limit):
    text = re.sub(r"\*\*|__|`", "", text).strip(DECORATION)
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def is_term(term):
    return bool(term) and "<" not in term and len(term.split()) <= 6


def extract_terms(reply):
    """{key: (term, meaning)} from `🔑 Term: *name* = meaning` lines and `📚 New terms: *a*, *b*` recaps."""
    found = {}
    for match in TERM_LINE.finditer(reply):
        parts = TERM_SPLIT.split(match.group(1), maxsplit=1)
        if len(parts) != 2:
            continue
        term, meaning = clean(parts[0], 60), clean(parts[1], 140)
        if is_term(term) and meaning:
            found[key(term)] = (term, meaning)
    for match in RECAP_LINE.finditer(reply):
        for part in RECAP_SPLIT.split(match.group(1)):
            term = clean(part, 60)
            if is_term(term) and key(term) not in found:
                found[key(term)] = (term, "")
    return found


def extract_cases(reply):
    names = (clean(m.group(1), 80) for m in CASE_LINE.finditer(reply))
    return [n for n in names if len(n) >= 3 and "<" not in n]


def last_reply(event):
    """The text the AI wrote in this turn: the last message from the hook input, plus whatever the transcript kept."""
    text = event.get("last_assistant_message")
    text = text if isinstance(text, str) else ""
    return text + "\n" + turn_from_transcript(event.get("transcript_path"))


def turn_from_transcript(path):
    """Every text block of the current turn, if the transcript stores them (the terminal app does)."""
    if not path or not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        f.seek(max(0, f.tell() - 2_000_000))  # the last ~2 MB is plenty for one turn
        lines = f.read().decode("utf-8", "ignore").splitlines()

    parts = []
    # Walk backwards from the end until the user's prompt that started this turn.
    for line in reversed(lines):
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        content = (entry.get("message") or {}).get("content")
        if entry.get("type") == "user":
            blocks = content if isinstance(content, list) else []
            # Tool results are also stored as "user" entries; only a real prompt ends the walk.
            if isinstance(content, str) or any(isinstance(b, dict) and b.get("type") == "text" for b in blocks):
                break
        elif entry.get("type") == "assistant" and isinstance(content, list):
            parts += [b.get("text", "") for b in reversed(content) if isinstance(b, dict) and b.get("type") == "text"]
    return "\n".join(reversed(parts))


def project_of(event):
    return os.path.basename(os.path.normpath(event.get("cwd") or os.getcwd()))


def record_reply(event):
    """Stop hook: remember what the AI just taught."""
    if os.path.exists(OFF_FLAG):
        return
    reply = last_reply(event)
    terms, cases = extract_terms(reply), extract_cases(reply)
    if not terms and not cases:
        return
    data = load()
    project = project_of(event)
    # A term found twice in one turn (its 🔑 line and the 📚 recap) still counts as one sighting.
    for term, meaning in terms.values():
        touch(data["terms"], term, project, meaning)
    known = {c["name"] for c in data["hard_cases"]}
    for name in dict.fromkeys(cases):
        if name not in known:
            data["hard_cases"].append({"name": name, "date": time.strftime("%Y-%m-%d"), "project": project})
    save(data)


def record_question(term, project):
    """context.py: the user asked what `term` means, so it's a concept they are still unsure about."""
    data = load()
    touch(data["asked"], term, project)
    save(data)


def summary():
    """A short block for the session-start rules, or "" for a brand-new learner."""
    data = load()
    if not (data["terms"] or data["asked"] or data["hard_cases"]):
        return ""
    lines = ["", "## What this learner already knows (VibeLearning memory from past sessions)"]
    recent = sorted(data["terms"].values(), key=lambda e: e.get("last", ""), reverse=True)[:30]
    if recent:
        names = ", ".join(e["term"] for e in recent)
        lines.append(f"- Terms already explained: {names}. Don't define these again; connect new ideas to them.")
    shaky = sorted(data["asked"].values(), key=lambda e: (e.get("count", 0), e.get("last", "")), reverse=True)[:10]
    if shaky:
        names = ", ".join(e["term"] + (f" ({e['count']}×)" if e.get("count", 0) > 1 else "") for e in shaky)
        lines.append(f"- They asked what these mean, so they may still be shaky: {names}. When one comes up, check understanding with a tiny example.")
    if data["hard_cases"]:
        names = "; ".join(f"\"{c['name']}\"" for c in data["hard_cases"][-5:])
        lines.append(f"- Hard cases they've been through: {names}. Use them as reference points when a similar bug appears.")
    lines.append("The full list: `$progress`.")
    return "\n".join(lines) + "\n"


def main():
    if sys.argv[1:] == ["summary"]:
        print(summary(), end="")
        return
    record_reply(json.load(sys.stdin))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Memory is a bonus: it must never break the user's session.
