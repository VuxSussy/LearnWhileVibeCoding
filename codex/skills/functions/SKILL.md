---
name: functions
description: List every function and class in a file and explain each one in plain words, with how they connect. Use when the user types $functions (optionally followed by: <file> [function name]).
---
Use skill `code-tour` on: (whatever the user wrote after invoking the skill, if anything)
(If no file is given, use the file most recently edited or discussed in the conversation and say which one you picked.)

- With only a file: give the full tour (one-sentence summary, the function table with line numbers, how they connect, where to start reading).
- With a file and a function name: explain just that function in depth:
  1. **What it's for** (1 sentence).
  2. **Step by step:** each block of the function in 1-2 plain lines, citing line numbers.
  3. **In → Out:** parameters, return value, and side effects (writes to a file, calls an API, changes state...).
  4. **Who calls it / what it calls.**
  5. **🧮 Algorithm or pattern** inside, if any (skill `algorithm-spotter`).
  6. **⚠️ Edge cases** it does or doesn't handle (empty input, `null`, errors).
