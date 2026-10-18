---
name: hard-case-explainer
description: Explain a "hard case" the AI just solved so the vibe coder truly understands it. Use right after fixing a tricky bug, a confusing error, something that needed several attempts, or problems involving async/timing/memory/CORS/permissions/cache/library versions, or when the user asks "why did that fix it?", "what did you just change?", "explain this case".
---

# Hard Case Explainer: turn hard bugs into lessons

Vibe coders often only see "error → AI fixes it → error gone" without knowing **what actually happened**.
Next time it shows up, they are stuck again. This skill turns every hard case into a small, reusable lesson.

## What counts as a "hard case"? (one sign is enough)
- It took **2 or more attempts**, or the first fix was wrong.
- The **real cause was somewhere else** than where the error appeared (e.g. it shows in the UI but comes from the API).
- The error message was **confusing or misleading**.
- It involved something "invisible": timing/async, cache, environment variables, library versions, permissions, CORS, encoding, time zones, race conditions, memory leaks.
- The fix is a **workaround** or looks odd in a way a beginner would never come up with.

Trivial bugs (a misspelled variable, a missing bracket) → do **not** use this block; a normal 📘 line is enough.

## The 🧩 block format (1-2 sentences per line)
```
🧩 Hard case: <short, memorable name>
   🤒 Symptom: <what the user saw>
   🔎 Root cause: <what was really going on, with an everyday analogy if possible>
   🛠️ Fix & why it works: <what changed, and why it fixes the root cause instead of hiding the symptom>
   🧠 Spot it next time: <the sign that tells you it's this kind of bug>
```
If a wrong fix was tried first, add `❌ First attempt failed because: ...`. That line is often the biggest lesson.

## Principles
- **Be honest:** if you are not sure about the root cause, say "most likely...". Never make one up.
- **Talk about the user's own code**, with specific files/lines, not generic theory.
- **Keep it short.** For a deep dive (flow diagram, reproducing the bug) suggest `$hard-case`.
- With ADHD mode on: bold the keyword in each line, trim words, keep all 5 lines.

## Example
🧩 **Hard case: "Double-clicking creates two orders"**
   🤒 **Symptom:** Clicking fast twice saves two identical orders.
   🔎 **Root cause:** The first request **hadn't finished** when the second one was sent, like two people withdrawing from one account at the same moment.
   🛠️ **Fix & why it works:** **Disable the button** while sending and add a **unique order key** on the server, so even two sends create only one order.
   🧠 **Spot it next time:** The bug only happens **when you act fast**, so think "two things running on top of each other".
