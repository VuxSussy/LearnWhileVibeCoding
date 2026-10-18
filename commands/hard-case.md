---
description: Deep dive into a hard case the AI just solved — root cause, why the fix works, and how to spot it next time
argument-hint: [case description - defaults to the latest hard bug] [save]
---
Use skill `hard-case-explainer` to dig into this case (if empty: the hardest case solved in this conversation): $ARGUMENTS

Present in this order, 2-3 plain lines per part:
1. **The full 🧩 block** (symptom, root cause, fix & why it works, spot it next time).
2. **🎬 Flow before and after the fix** as two arrow lines, e.g. `Click → send request → (not done yet) → click again → second request ❌`.
3. **❌ Attempts that didn't work** (if any) and why.
4. **🧪 Reproduce it yourself:** one simple way for the user to make the bug appear again and see it with their own eyes.
5. **🔁 Other places in the project that could have the same bug** (if any, at most 2).
6. **❓ One check question** for the user to answer; wait for the answer before commenting.

If the arguments contain "save": append the 🧩 block to `LEARNING_NOTES.md` under a `## 🧩 Hard cases` heading (create it if missing).
