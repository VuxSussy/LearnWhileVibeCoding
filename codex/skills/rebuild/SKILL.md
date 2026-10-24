---
name: rebuild
description: Teach the user how to build something themselves from an empty file, using the real code in their project - the core idea, a blueprint of the parts and the order to build them, then milestones with the key code, how a developer would figure each one out, and how to check it works. Use when the user says "how do I make this myself", "teach me to build it", "I only know what it does, not how to make it", "from scratch", "làm sao để tự làm", "dạy tôi cách làm ra nó", or after a feature they want to really learn. Invoke with a feature, file or folder; add `together` to build it with your own hands step by step, or `save` to keep the guide.
---

# Rebuild It Yourself: from "I know what it does" to "I can make it"

Reading finished code shows *what* it does. Making something takes a different skill: knowing **where to start, in what order,
what to look up, and how to check each piece**. This skill teaches that path, using the user's own project as the example.

## Pick the target
- Use what the user named (a feature, a file, a folder). Nothing named → the feature built most recently in this conversation; say what you picked.
- **Read the real code first** (the entry point, then every file the feature touches). The guide must match their project, not a generic tutorial.
- Too big for one guide (more than ~6 milestones)? Teach the core slice that everything else hangs on, and list the rest under 🚀 Next.

## The guide (default)
1. **🧠 The core idea** (2-3 lines): what it is in one sentence, and the one trick that makes it work, with an everyday analogy.
2. **🧱 Blueprint:** the parts as an arrow line (`form → check input → send to server → save → show result`), then the build order and why.
   Always start with the **smallest version that runs** (a walking skeleton), then add one piece at a time.
3. **🪜 Milestones** (3-6), each one runnable on its own:
   ```
   Milestone 2/5: Save the order to the database
   🎯 Goal: after clicking "Buy", a new row appears in the orders table.
   ✍️ Write: the key code, ≤15 lines, trimmed from the real project (and `file:line` where it lives now).
   🛠️ How you'd figure this out yourself: the search phrase ("express post json body"), the doc page, what to console.log.
   ✅ Check it works: the exact command or click, and what you should see.
   ⚠️ Common trap: (optional) the mistake beginners make here.
   ```
4. **🧭 The pattern to reuse** (1-2 lines): the general recipe this is one example of, so it carries over to other projects
   (e.g. "every form that saves data = UI → validate → send → store → confirm").
5. **🏋️ Try it yourself** (2 ideas, easy then harder): small variations to build alone to prove it stuck
   (e.g. "add a quantity field", "show an error message when the server is down").

If the project did something unusual or hacky, say so honestly and show the cleaner way in one line.

## Together mode (`together`)
Build it with the user, one milestone at a time, and **they write the code**:
1. Show the 🧠 idea and the 🧱 blueprint, and agree where to build: a new file, a branch, or a `practice/` folder so their working code stays safe.
2. For each milestone give the 🎯 Goal, the ✅ Check and the empty function or file, then stop and wait.
   Hints only when asked, in tiers (`hint 1` direction · `hint 2` pseudo-code · `hint 3` almost the answer), as in skill `practice`.
3. When they submit: run or check it, praise one specific thing, coach the single most important issue, then move to the next milestone.
4. "show me" → show your version of this milestone. "just do it" → finish the rest yourself, still with 📘/💡/🛠️ lines.

## Save (`save`)
Append the guide to `LEARNING_NOTES.md` under `## 🔁 How to build <name>` with today's date (create the file if it's missing).

## Principles
- **Order matters more than code.** The main lesson is *which piece comes first and why*; never walk through files in the order they happen to be in.
- **Every milestone must run on its own.** No step that only works after three more steps.
- The 🛠️ line teaches the search-and-check habit: name real search phrases, docs or debug prints, never just "look it up online".
- With ADHD mode on: at most 3 milestones per guide, and one milestone per reply in `together` mode.
