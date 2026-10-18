---
name: learn-by-doing
description: Let the vibe coder write a small, meaningful piece of code (3-10 lines) themselves, with tiered hints and feedback. Use when the user types $practice, when practice mode is on, or when they say "let me write it", "I want to try", "don't do it all for me".
---

# Learn by Doing: write a little, understand a lot

Reading explanations helps you understand; **writing it yourself** helps you remember. But vibe coders give up easily when handed too much.
So only hand over **one small, meaningful piece, with a safety net**.

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
