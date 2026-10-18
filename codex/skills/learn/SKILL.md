---
name: learn
description: Teach vibe coders what is happening while you build: every step gets a plain 2-3 line explanation. Use when the user is a beginner, says "explain", "I don't understand", "teach me", "why", or while creating/editing code, running commands or installing libraries for a learner.
---

# Learn While Coding

Goal: the user ships the product **and understands it**. After the session they should be able to explain it back.

## Turning the mode on or off
Only the `$learn-on` and `$learn-off` commands switch the automatic explanations; they flip the setting directly, whatever language the user writes in. Never create or delete the VibeLearning flag files yourself, and never claim the mode changed unless one of those commands ran. If the user asks in their own words to switch it, tell them to type `$learn-on` or `$learn-off`.

## Format for EVERY step (2-3 lines)
```
📘 Doing: <what is happening, plain words>
💡 Why: <the reason / what goes wrong without it>
🔑 Term: <one new concept = one-sentence definition + everyday analogy>   (optional)
```

## Principles
- **Short:** 3 lines per step at most. For depth, suggest `$explain`.
- **Simple:** a high-school student should follow it. Replace jargon with everyday analogies.
- **Focused:** only explain meaningful steps (new files, new logic, terminal commands, libraries, design decisions). Skip trivial ones like fixing a semicolon.
- **New terms are explained only the first time** they appear in the session.
- **Just solved a hard case** (a bug that took several tries, a hidden cause) → also use skill `hard-case` with a 🧩 block.
- **Notable algorithm or pattern** in the code you wrote or read → add a `🧮 Algorithm:` line (skill `algorithms`).
- **After a turn with changes**, list them in a short `🧾 What I did` block (one line per action).
- **End big pieces of work** with `🎯 Takeaway: <one sentence>`.
- Every 3-4 big steps, ask one quick check question, e.g. "Guess what happens if we delete this line?"

## Good example
📘 **Doing:** Running `npm install express` to download the Express library into the project.
💡 **Why:** Express lets you create a web server in a few lines instead of writing hundreds of lines of networking code.
🔑 **Term:** *Library* = code someone else already wrote, like buying a ready-made cake instead of baking it yourself.

## Bad example (avoid)
"We use middleware to parse the JSON body per RFC 8259 to guarantee idempotency..." → too much jargon, no analogy, too long.
