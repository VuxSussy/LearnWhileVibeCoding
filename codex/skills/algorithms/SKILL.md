---
name: algorithms
description: Point out the algorithms, data structures and design patterns in a file or function, with speed explained in plain words. Use when the user types $algorithms (optionally followed by: [file | function | folder]).
---
Use skill `algorithm-spotter` on: (whatever the user wrote after invoking the skill, if anything)
(If empty, use the code written or discussed most recently in this conversation and say what you picked.)

Read the code first, then report each finding in the 🧮 format (idea, speed in plain words, watch out), most important first.
Finish with **📊 Overall** (is it fast enough for its likely data size?) and **📚 Learn next** (one algorithm/pattern worth looking up).
If you find a real performance problem, show a short before/after snippet of the fix, but don't apply it unless the user asks.
