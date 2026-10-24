#!/usr/bin/env python3
"""UserPromptSubmit hook: read the message the user just sent and tell the AI how to teach *this* one.

The old reminder printed the same line whatever you typed. This hook looks at your words (English or
Vietnamese, with or without accents) to guess what kind of help you want: a concept, a how-to, a bug
fix, a new feature... and whether you sound confused or in a hurry. It also checks the learner profile
(learner.py), so terms you already know get built on instead of explained again.
Everything it prints is added to the AI's context for this one turn.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import learner  # noqa: E402  (the learner profile, in the same folder)

FLAG = os.path.expanduser("~/.claude/vibe-learning")

# What the user wants, in priority order: the first match is the main intent.
# Each entry: the phrases that signal it (regexes, written with Vietnamese accents; text typed
# without accents is matched against an accent-free copy) and what the AI should do about it.
INTENTS = [
    ("in a hurry", [
        r"just (do|fix|make) it", r"skip (the )?explanation", r"no explanations?", r"\bhurry\b", r"\basap\b",
        r"làm luôn", r"làm nhanh", r"nhanh lên", r"khỏi giải thích", r"không cần giải thích", r"đừng giải thích", r"\bgấp\b",
    ], "They're in a hurry: do the work first and keep teaching to one short line per step (📘 with the 🛠️ move folded in). "
       "No 🔑 terms, no practice TODO. Still end with 🧾."),
    ("confused", [
        r"(don'?t|do not|didn'?t|still not) (really )?(understand|get it)", r"\bconfus", r"i'?m lost", r"makes no sense", r"\?{3,}",
        r"không hiểu", r"chưa hiểu", r"khó hiểu", r"chả hiểu", r"chẳng hiểu", r"rối quá", r"\blú\b", r"mơ hồ", r"vẫn chưa rõ",
    ], "They're CONFUSED. Say in one line what you think tripped them up, then explain it a different way: a new analogy, "
       "smaller steps, a tiny concrete example from their own code. Don't repeat the old explanation. End with one quick check question."),
    ("bug", [
        r"\berror\b", r"\bbugs?\b", r"\bcrash", r"exception", r"traceback", r"(doesn'?t|does not|isn'?t|not) work", r"\bbroken\b",
        r"\bfail(s|ed|ing)?\b", r"undefined is not", r"cannot read propert", r"\bblank (page|screen)\b", r"nothing (happens|shows)",
        r"\blỗi\b", r"không chạy", r"không hoạt động", r"bị sai", r"\bhỏng\b", r"\bvăng\b", r"đứng hình", r"không được nữa",
        r"trắng (trang|màn hình)", r"màn hình trắng", r"không (hiện|hiển thị|thấy gì)",
    ], "Bug report. Debug out loud so they learn the method: 🔦 what you check first and why, what each check ruled out, then the fix. "
       "If it turned out tricky → 🧩 block with its 🔦 line."),
    ("how to make it", [
        r"how (do|can|would|should) (i|we|you)\b", r"\bhow to\b", r"teach me", r"step by step", r"from scratch", r"(by|for) myself",
        r"làm sao", r"làm thế nào", r"bằng cách nào", r"cách (làm|tạo|viết|xây|dựng|code|cài)", r"hướng dẫn", r"tự (làm|viết|code|tạo)",
        r"từ đầu", r"dạy (tôi|mình|em|tui)",
    ], "They want to learn HOW TO MAKE it, not just get it. Start with 🧱 Blueprint (parts, order, smallest working version first), "
       "build step by step with a 🛠️ line each (what you'd look up, type or check to do it yourself), finish with 🔁 Rebuild it yourself. "
       "Offer `/rebuild together` so they can build it with their own hands."),
    ("concept question", [
        r"what(?:'s| is| are| does)\s", r"meaning of", r"difference between", r"\bvs\.?\s",
        r"là gì", r"là cái gì", r"là sao", r"nghĩa là", r"khác gì", r"khác nhau", r"khái niệm",
    ], "Concept question{term}. Answer it directly first: plain definition → everyday analogy → where it shows up in THIS project "
       "(file:line if it does) → how it's made or used, in 3-6 lines of code. Then one check question."),
    ("why", [
        r"\bwhy\b", r"tại sao", r"vì sao", r"sao lại", r"lý do",
    ], "Why-question: give the real reason, one realistic alternative with its trade-off, and what breaks if it's done wrong. Point at the exact code."),
    ("explain", [
        r"\bexplain", r"walk me through", r"^\s*giải thích", r"giải thích (giúp|cho|lại|thêm|kỹ|đoạn|cái|hàm|file|code)",
        r"đọc (code|giúp)", r"đoạn (code|này)", r"hoạt động (thế nào|ra sao)",
    ], "Explain request: one-sentence summary → the parts in order → flow arrows → 🛠️ how you'd write this yourself (the recipe, not just the result)."),
    ("build", [
        r"\b(build|create|make|add|implement|write|set ?up|develop|refactor|improve)\b",
        r"\btạo\b", r"\bthêm\b", r"\bviết\b", r"xây dựng", r"phát triển", r"cài đặt", r"\bsửa\b", r"nâng cấp", r"cải thiện",
        r"làm (một|cái|cho|trang|app|web|game|tính năng|chức năng)",
    ], "Build request. Before coding: 🧱 Blueprint in 2-4 lines (parts, order, why). Each meaningful step: 📘 Doing / 💡 Why / 🛠️ How yourself. "
       "When the feature works: 🔁 Rebuild it yourself (≤6 steps) so they could make it again without you."),
]

# A stronger intent makes another one's advice redundant or contradictory: drop the weaker advice.
OVERRIDES = {
    "in a hurry": {"build", "how to make it", "explain"},
    "how to make it": {"build"},
    "mode switch": {"explain", "build"},
}

REFERS_BACK = [
    r"\bearlier\b", r"\babove\b", r"that one", r"the (previous|last) (one|step|thing)", r"same (thing|as before)",
    r"lúc nãy", r"hồi nãy", r"ban nãy", r"vừa nãy", r"vừa rồi", r"ở trên", r"bên trên", r"cái (đó|kia)", r"chỗ (đó|kia)", r"như (cũ|trên)",
]
MODE_SWITCH = [
    r"turn (on|off) (the )?(explanations?|learning|adhd|practice|type.?it)", r"stop explaining",
    r"(tắt|bỏ|ngừng|dừng) (chế độ |phần )?(giải thích|học|adhd|luyện tập|practice)",
    r"(bật|mở) (chế độ )?(adhd|giải thích|học|luyện tập|practice|tự gõ|type.?it)",
]
FOLLOW_UPS = {"ok", "oke", "okay", "yes", "y", "yep", "sure", "continue", "go on", "go", "next", "done",
              "tiep", "tiep di", "tiep tuc", "lam tiep", "ok tiep", "duoc", "dc", "uh", "u", "co", "roi", "xong", "xong roi"}
# Words around a "what is X" question that are not part of X.
FILLER = {"cho", "minh", "toi", "em", "anh", "hoi", "vay", "thi", "cai", "nay", "do", "oi", "ban", "the", "a", "an",
          "so", "and", "va", "con", "khi", "ma", "ra", "nghia", "is", "are"}
VIETNAMESE_LETTERS = set("ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ")
VIETNAMESE_WORDS = {"khong", "ko", "duoc", "dc", "toi", "minh", "cai", "nay", "lam", "sao", "gi", "nhe", "nha", "la",
                    "roi", "chua", "voi", "cua", "thi", "giup", "ban", "vay", "nhu", "nao", "tai", "sao", "gium"}
FALLBACK = ("[VibeLearning] Each step: 📘 Doing / 💡 Why / 🛠️ How yourself (2-3 plain lines). Notable algorithm → 🧮. "
            "Hard case just solved → 🧩. End of a work turn → 🧾 What I did.")
VI_LABELS = "📘 Đang làm · 💡 Vì sao · 🛠️ Tự làm thế nào · 🔑 Thuật ngữ · 🧱 Bản thiết kế · 🔁 Tự làm lại · 🔦 Dò lỗi"


def finder(text):
    """Return a search(pattern) that respects accents when the user typed them."""
    lowered = text.lower()
    accent_free = learner.plain(lowered)
    if accent_free != lowered:  # typed with accents: "lời" must not match "lỗi"
        return lambda pattern: re.search(pattern, lowered)
    return lambda pattern: re.search(learner.plain(pattern), accent_free)


def language(text):
    lowered = text.lower()
    if any(c in VIETNAMESE_LETTERS for c in lowered):
        return "vi"
    # Accents like "à" or "ì" also exist in French, so count common Vietnamese words with the accents removed.
    words = set(re.findall(r"[a-z]+", learner.plain(lowered)))
    return "vi" if len(words & VIETNAMESE_WORDS) >= 2 else "other"


def asked_term(text):
    """The X in "X là gì?" / "what is X?", or "" if there isn't a clear one."""
    quoted = re.search(r"[`\"“'](.{2,40}?)[`\"”']", text)
    patterns = [
        r"([\w.+#/-]+(?:\s+[\w.+#/-]+){0,3})\s+(?:là|la)\s+(?:cái\s+|cai\s+)?(?:gì|gi)\b",
        r"what(?:'s| is| are| does)\s+(?:an?\s+|the\s+)?([\w.+#/-]+(?:\s+[\w.+#/-]+){0,3}?)(?:\s+(?:mean|do|for))?\s*(?:[?.!,]|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        if quoted and quoted.group(1) in match.group(0):
            return quoted.group(1).strip()
        # Keep the words right before "là gì", stopping at the first filler word ("cho mình hỏi middleware" -> "middleware").
        words = match.group(1).split()
        keep = []
        for word in reversed(words):
            if learner.plain(word) in FILLER:
                break
            keep.insert(0, word)
        term = " ".join(keep).strip(" ?.,!")
        if term and learner.plain(term) not in FILLER and term.lower() not in ("this", "that", "it", "these"):
            return term
    return ""


def mentioned(entries, accent_free_text, skip=""):
    """Profile entries whose term appears in the message, most-seen first."""
    hits = [e for k, e in entries.items() if k != skip and len(k) >= 2
            and re.search(rf"(?<![\w]){re.escape(k)}(?![\w])", accent_free_text)]
    return sorted(hits, key=lambda e: e.get("count", 0), reverse=True)[:4]


def notes_for(prompt, profile):
    text = prompt[:20000]
    search = finder(text)
    intents = [(name, guide) for name, patterns, guide in INTENTS if any(search(p) for p in patterns)]
    switching = any(search(p) for p in MODE_SWITCH)
    names = {name for name, _ in intents} | ({"mode switch"} if switching else set())
    dropped = set().union(*(OVERRIDES.get(name, set()) for name in names))
    advice = [(name, guide) for name, guide in intents if name not in dropped]
    lang = language(text)
    accent_free = learner.plain(text)
    is_follow_up = not intents and (accent_free.strip(" .!") in FOLLOW_UPS or len(text.split()) <= 3)

    reply_in = f"reply in Vietnamese, labels too ({VI_LABELS})" if lang == "vi" else "reply in the user's language, labels too"
    labels = ", ".join([name for name, _ in advice] + (["mode switch"] if switching else [])) or ("short follow-up" if is_follow_up else "general")
    lines = [f"[VibeLearning] Reading this message → {labels} · {reply_in}"]

    term = asked_term(text) if any(name == "concept question" for name, _ in intents) else ""
    for name, guide in advice[:3]:
        lines.append("→ " + guide.replace("{term}", f" about \"{term}\"" if term else ""))
    if is_follow_up:
        lines.append("→ Short follow-up: carry on from where you left off; don't restart or re-explain earlier steps.")
    if any(search(p) for p in REFERS_BACK):
        lines.append("→ They point back at something earlier: work out what from the conversation and name it in a few words before answering.")
    if switching:
        lines.append("→ They seem to want to switch a mode. Only commands do that: tell them the exact one "
                     "(`/learn-off`, `/learn-on`, `/adhd-on`, `/practice-on`, `/type-it-on`...).")

    term_key = learner.key(term) if term else ""
    known = mentioned(profile["terms"], accent_free, skip=term_key)
    if known:
        lines.append("→ Already learned in earlier sessions: " + ", ".join(e["term"] for e in known)
                     + ". Build on them instead of defining them again.")
    shaky = mentioned(profile["asked"], accent_free)
    if shaky:
        lines.append("→ They asked what " + ", ".join(e["term"] for e in shaky)
                     + " means before, so it's still shaky: check their understanding with a tiny example.")

    if not any(name == "in a hurry" for name, _ in intents):
        lines.append("Format: each meaningful step 📘 Doing / 💡 Why / 🛠️ How yourself (+🔑 new term). Algorithm → 🧮. "
                     "Hard bug solved → 🧩 with 🔦. End of a work turn → 🧾 What I did (+ 📚 New terms); new feature → 🔁 Rebuild it yourself.")
    if os.path.exists(FLAG + ".adhd"):
        lines.append("[ADHD] Short sentences, bold keywords, update the 🗺️ progress bar, one next action, one question.")
    if os.path.exists(FLAG + ".practice"):
        lines.append("[Practice] New feature → consider leaving one meaningful 3-10 line TODO(you) for the user to write.")
    if os.path.exists(FLAG + ".typeit"):
        lines.append("[Type it yourself] Don't run git/npm/pip commands that change things: hand them over as a "
                     "⌨️ Your turn checklist with a guide for each, then wait.")
    return "\n".join(lines), term


def main():
    if os.path.exists(FLAG + ".off"):
        return
    event = json.load(sys.stdin)
    prompt = event.get("prompt") or ""
    if not isinstance(prompt, str) or not prompt.strip():
        return
    profile = learner.load()
    notes, term = notes_for(prompt, profile)
    print(notes)
    if term:
        learner.record_question(term, learner.project_of(event))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Reading the message is a bonus: if it breaks, fall back to the plain reminder, never block the prompt.
        if not os.path.exists(FLAG + ".off"):
            print(FALLBACK)
