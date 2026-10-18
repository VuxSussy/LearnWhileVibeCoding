---
name: algorithm-spotter
description: Identify the algorithms, data structures and design patterns used in code (sorting, searching, recursion, hashing, caching/memoization, debounce/throttle, retry with backoff, BFS/DFS, dynamic programming, two pointers, observer, singleton, MVC...) and explain each in plain words with speed (Big-O) in everyday terms. Use when the user asks "what algorithm is this", "how does this work", "is this efficient", "why is it slow", runs $algorithms, or when you write code built on a notable algorithm.
---

# Algorithm Spotter: name the technique, explain the idea

Most code a vibe coder ships is built on a handful of classic ideas. Naming them turns "magic code"
into something they can look up, reason about and reuse.

## What to look for
- **Algorithms:** sorting, binary search, linear search, recursion, BFS/DFS, dynamic programming, greedy choices, two pointers / sliding window, hashing, string matching, shuffling, random sampling.
- **Data structures:** arrays/lists, hash maps/dictionaries/sets, stacks, queues, trees, graphs, linked lists, heaps/priority queues.
- **Practical techniques:** caching/memoization, debounce/throttle, pagination, retry with exponential backoff, batching, lazy loading, rate limiting, optimistic UI updates, polling vs. webhooks.
- **Design patterns:** observer/event listeners, pub-sub, singleton, factory, strategy, middleware chain, MVC/MVVM, state machine, dependency injection.

Only report what is **actually in the code**, with file and line. If something is close to a known algorithm but not quite, say so ("a simplified version of ...").

## Output format for each finding
```
🧮 <Name> — `file:line` in `functionName()`
   💡 Idea: <what it does, in 1-2 plain sentences, with an everyday analogy>
   ⏱️ Speed: <Big-O + plain words, e.g. "O(n²): twice the data ≈ 4× the time">
   ⚠️ Watch out: <when it becomes a problem, or a better choice if there is one>   (optional)
```

Order findings from **most important** to least. End with:
- **📊 Overall:** one line on whether the code is fast enough for its likely data size.
- **📚 Learn next:** one algorithm/pattern worth looking up, and why.

## Speed in plain words (use these)
| Big-O | Plain words |
|---|---|
| O(1) | the same time no matter how much data, like looking up a word you bookmarked |
| O(log n) | barely slower as data grows, like finding a name in a sorted phone book |
| O(n) | twice the data ≈ twice the time, like reading every page |
| O(n log n) | a little worse than O(n), typical for good sorting |
| O(n²) | twice the data ≈ 4× the time, like comparing everyone with everyone at a party |
| O(2ⁿ) | explodes quickly, like trying every combination of a lock |

## Principles
- No math jargon without the plain-words version next to it.
- If the code has a real performance problem (e.g. an O(n²) loop over thousands of items, or a database query inside a loop), say so clearly and suggest the fix in one line.
- Nothing notable found? Say so honestly instead of inventing something.
