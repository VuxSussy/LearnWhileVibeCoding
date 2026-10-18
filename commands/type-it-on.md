---
description: Turn on type-it-yourself mode — the AI lists the git/npm/pip commands with a guide for each, and you type them
argument-hint: [tools to learn, e.g. "git" or "git npm" - default: git, npm, npx, yarn, pnpm, bun, pip]
allowed-tools: Bash(mkdir:*), Bash(touch:*)
---
!`mkdir -p ~/.claude && touch ~/.claude/vibe-learning.typeit`

Type-it-yourself mode is now ON (remembered for future sessions). A guard hook now blocks commands that change the project through the guarded tools; read-only commands still work.

Tools requested: $ARGUMENTS
If specific tools were named (git, npm, npx, yarn, pnpm, bun, pip, pip3), write them space-separated into the flag file, e.g. `printf 'git npm' > ~/.claude/vibe-learning.typeit`, so only those are guarded. If none were named, leave the file empty (all of them are guarded).

From now on apply skill `type-it-yourself`: hand those commands over as a ⌨️ Your turn checklist with a guide for each, wait for "done", then verify.
Tell the user in one or two lines: it's on, which tools are guarded, that they'll get a checklist to type, and `/type-it-off` turns it off.
