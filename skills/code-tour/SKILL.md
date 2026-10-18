---
name: code-tour
description: List every function, method and class in a file and explain each one in plain words (what it does, inputs → output, who calls it), plus how they connect. Use when the user asks "what's in this file", "what does this file do", "explain these functions", "walk me through this code", runs /functions or /map, or opens an unfamiliar file they vibe coded.
---

# Code Tour: what lives in this file?

Vibe coders end up with files full of functions they never read. A tour gives them a map:
every function, what it is for, and how the pieces call each other.

## Steps
1. **Read the whole file** (don't guess from the name). For big files (500+ lines), read it in parts.
2. **Find every definition**: functions, methods, classes, components, hooks, handlers, exported constants that hold logic.
   Record the **line number** for each so the user can jump to it.
3. **Work out the connections**: which function calls which, what is exported/used by other files, what is the entry point.
4. **Spot notable algorithms/patterns** while reading (skill `algorithm-spotter`) and mark them with 🧮.

## Output format
**📄 `<file>` in one sentence:** what this file is responsible for, like a job title.

| # | Function | Line | What it does (plain words) | In → Out |
|---|---|---|---|---|
| 1 | `loadUser(id)` | 12 | Fetches one user from the database | user id → user object or `null` |

- Group methods under their class (`ClassName.method`), and list classes first.
- "What it does" is **one sentence**, no jargon. Mark helpers nobody calls with `⚠️ unused?`.
- Add 🧮 next to a function that contains a notable algorithm (details come from `/algorithms`).

**🔗 How they connect:** an arrow diagram of the main flow, at most ~6 boxes:
```
handleSubmit() → validateForm() → saveOrder() → showToast()
```

**🚪 Start reading here:** the one function a beginner should read first, and why (1 line).

## Principles
- Be exact: names and line numbers must match the file. Never invent a function.
- Prefer the *purpose* ("decides whether the user may log in") over restating code ("returns a boolean").
- More than ~25 functions → show the 15 most important ones and say how many were left out.
- With ADHD mode on: show only the table's first 5 rows, then ask whether to continue.
