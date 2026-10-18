---
name: type-it-yourself
description: Hand terminal commands for tools the user wants to learn (git, npm, yarn, pnpm, pip...) to the user as a guided checklist instead of running them. Use when type-it-yourself mode is on, when a command was blocked by the VibeLearning guard, or when the user says "I want to learn git/npm", "let me type the commands", "don't run git for me", "show me the commands".
---

# Type It Yourself: learn git and npm by typing them

When the AI runs `git commit` or `npm install` silently, the user never learns them.
In this mode the AI still plans and writes the code, but **the user types every command that changes something**,
with a short guide for each one.

## What the user types vs. what you may run
- **User types:** anything that changes the project or its history: `git add/commit/push/pull/checkout/switch/branch <name>/merge/rebase/reset/stash/tag <name>/init/clone`,
  `npm|yarn|pnpm|bun install/add/remove/update/init/create/publish`, `npx create-*`, `pip install/uninstall`.
- **You may still run (read-only):** `git status`, `git diff`, `git log`, `git show`, `git branch -v`, `git remote -v`, `npm ls`, `npm view`, `pip list`, and running the project or its tests (`npm test`, `npm run build`).
  Use them to understand the state and to **check the user's work afterwards**.
- If the guard hook blocks a command, never work around it: no other tool, no script, no hand-editing `package.json`, lockfiles or `.git/`.

## When to hand over commands
- Plan the whole task, then hand over commands **at the point they are needed**, in small batches (1-5 commands).
  Example: `npm install` must happen before you can run the code, so hand that batch over first, wait, then continue.
- Before a batch, list **every** command the user will type in that batch, in order. Never hide one in prose.

## The checklist format
```
⌨️ Your turn in the terminal (2 commands)

1. git add src/cart.js
   📘 What it does: puts cart.js in the "box" of changes that the next commit will save.
   🔍 Parts: `add` = stage changes · `src/cart.js` = which file (`.` would mean every changed file).
   ✅ Expect: no output. `git status` now shows the file in green.

2. git commit -m "Stop cart total going negative"
   📘 What it does: saves a snapshot of the staged changes, with a message describing them.
   🔍 Parts: `commit` = save snapshot · `-m "..."` = the message, written as "what this change does".
   ✅ Expect: a line like `[main 3f2a1bc] Stop cart total going negative`.
   ⚠️ If you see "Please tell me who you are": run `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`, then commit again.

👉 Type `done` when finished, or paste the output if something looks wrong.
```
Rules for each command:
- The command is on its own line, ready to copy, with real file names and messages filled in (no `<placeholders>` unless the user must choose, and then say exactly what to put there).
- 📘 and 🔍 are one line each, in plain words. Explain each flag the **first** time it appears in the session; after that a short reminder is enough.
- ✅ says what success looks like, so the user can tell it worked.
- ⚠️ is optional: the most common error for that command and its fix.
- 🛑 **Risky commands** (`git reset --hard`, `git push --force`, `git clean -fd`, `git checkout -- .`, `rm -rf node_modules`, deleting a branch) get a red line explaining what can be lost and, if there is one, a safer alternative. Prefer the safe one.

## After the user says "done"
1. Verify with a read-only command (`git status`, `git log --oneline -3`, `npm ls <pkg>`) and tell them in one line whether it worked.
2. If it failed, read their output, explain the error in 2-3 plain lines, and give the corrected command in the same format.
3. Praise briefly ("✅ Your first commit is in!"), then continue the task.

## Learning curve
- Once the user has typed a command successfully 3 times, shorten its guide to one line (`git add . — stage everything, as before`).
- Occasionally (about every 5 commands) ask them to **write the command themselves** from a description: "Now save these changes with a message. What do you type?" Then check it.
- With ADHD mode on: batches of at most 2 commands, and only the 📘 and ✅ lines unless they ask for more.
