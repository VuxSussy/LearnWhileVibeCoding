---
name: practice
description: Let the vibe coder write a small, meaningful piece of code (3-10 lines) themselves, with tiered hints and feedback. Use when the user says "let me write it", "I want to try", "don't do it all for me", or when practice mode is on. Invoke with no arguments for one task right now (optionally naming the spot), or with `on` / `off` to leave one spot per new feature automatically.
---

# Learn by Doing: write a little, understand a lot

Reading explanations helps you understand; **writing it yourself** helps you remember. But vibe coders give up easily when handed too much.
So only hand over **one small, meaningful piece, with a safety net**.

## One task right now
Invoked without `on`/`off`: pick **one** meaningful spot in the current work (or the spot the user named), prepare it and hand it over as described below, then stop and wait.

## Turning the mode on or off
Only when the user explicitly asks (e.g. invoking this skill with `on` or `off`, or "turn this mode on/off"). Never toggle it on your own when this skill was picked automatically.
- **on:** run `mkdir -p ~/.claude && touch ~/.claude/vibe-learning.practice`: for each new feature, leave at most one meaningful spot for the user. Mention they can say "just do it" any time to skip.
- **off:** run `rm -f ~/.claude/vibe-learning.practice`: stop handing over tasks unless the user asks for one.
The setting is remembered for future sessions. Confirm in one line what changed and how to undo it.

## Pick the right spot
Good: a **decision** with several valid answers: a condition, error handling, a formula, how to sort/filter data, a message shown to the user.
Bad: boilerplate, configuration, imports, repetitive code, anything with only one way to write it.

## How to hand it over (always all 4 parts, 1-3 lines each)
1. **Prepare everything:** create the file/function, write the name, parameters and return value, and mark the exact spot with `// TODO(you): ...` (in the language's comment syntax).
2. **🎯 Task:** "In `<file>`, write the body of `<name>()` so that ..." in 1-2 sentences, with an example input → expected output.
3. **⚖️ Things to consider:** 1-2 lines about the choice (e.g. "block right away, or allow 3 retries?").
4. **🪜 Tiered hints:** only when asked: `hint 1` (direction), `hint 2` (pseudo-code), `hint 3` (almost the answer). Tell them they can type "hint" any time.

Then **stop and wait**. Don't write it for them.

## When the user submits code
- Praise one specific thing first.
- If something is wrong, point out **the single most important issue**, explain it in 2-3 lines, and let them fix it. Only fix it yourself if they ask.
- Run/check it if possible, then finish with one `🎯 Takeaway:` line.
- If they say "just do it" / "skip": do it right away, no judgement, still explain in 2-3 lines.

## Dosage
- At most **one task per feature**, and never while the user is rushing to fix a production bug.
- With ADHD mode on: tasks of **5 lines or fewer**, include an input/output example, and show hint 1 up front.
