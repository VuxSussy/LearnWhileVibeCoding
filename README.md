# 🎓 VibeLearning

A **Claude Code** (and **OpenAI Codex**) plugin that lets vibe coders **learn while they build**, so you don't end up with an app that works but that you don't understand.

- Every meaningful step comes with a **2–3 line, plain-language explanation**.
- Every **hard bug Claude solves** is turned into a short, reusable lesson.
- You can **write the important lines yourself**, with hints, and **practice explaining your project** for interviews and project defenses.
- It **shows what it did**: a `🧾 What I did` list after each piece of work, and a full plain-language timeline with `/activity`.
- It **tours your files**: `/functions` lists every function in a file and explains each one, and `/map` explains the whole project.
- It **names the algorithms**: `/algorithms` points out the algorithms, data structures and design patterns in your code, with speed explained in plain words.
- An **ADHD-friendly mode** for people who struggle with focus or long walls of text.

> Explanations come in whatever language you write to Claude, labels included.

## ✨ What it looks like

**Every step: 📘 Doing / 💡 Why / 🔑 Term**

> 📘 **Doing:** Creating a `.env` file to store the API key instead of hard-coding it.
> 💡 **Why:** If the key lives in your code and you push to GitHub, strangers can grab it and use it.
> 🔑 **Term:** *Environment variable* = a "secret sticky note" your program reads when it starts.

**After a hard bug: a 🧩 Hard case block**

> 🧩 **Hard case: "Double-clicking creates two orders"**
> 🤒 **Symptom:** Clicking fast twice saves two identical orders.
> 🔎 **Root cause:** The second request is sent **before the first one finishes**, like two people withdrawing from one account at once.
> 🛠️ **Fix & why it works:** **Disable the button** while sending and add a **unique order key** on the server, so duplicates are rejected at the source.
> 🧠 **Spot it next time:** The bug only happens **when you act fast**, so think "two things running on top of each other".

**After a piece of work: 🧾 What I did**

> 🧾 **What I did**
> - ✏️ edited `src/cart.js` — stop the total from going negative
> - ➕ created `src/cart.test.js` — checks for empty and full carts
> - ▶️ ran `npm test` — all 6 checks passed

**`/functions src/cart.js`: a tour of the file**

> **📄 `src/cart.js` in one sentence:** keeps track of what's in the shopping cart and how much it costs.
>
> | # | Function | Line | What it does | In → Out |
> |---|---|---|---|---|
> | 1 | `addItem(cart, item)` | 8 | Puts an item in the cart, or bumps its quantity | cart + item → new cart |
> | 2 | `total(cart)` 🧮 | 21 | Adds up price × quantity for every item | cart → number |
>
> **🔗 How they connect:** `addItem() → total() → formatPrice()`

**`/algorithms`: name the technique**

> 🧮 **Hash map lookup** — `src/cart.js:10` in `addItem()`
> 💡 **Idea:** Items are stored by their id, like lockers with numbers, so finding one doesn't mean checking them all.
> ⏱️ **Speed:** O(1): the same time whether the cart has 3 items or 3,000.

## 📦 Installation

Inside Claude Code:

```
/plugin marketplace add VuxSussy/VibeLearning
/plugin install vibe-learning@vibe-learning-marketplace
```

Or from a terminal:

```bash
claude plugin marketplace add VuxSussy/VibeLearning
```

```bash
claude plugin install vibe-learning@vibe-learning-marketplace
```

Start a new session and learning mode turns on automatically. To update later, run `claude plugin update vibe-learning`.

## 🧰 What's inside

### Skills (Claude uses them automatically when they fit)

| Skill | What it does |
|---|---|
| `learn-while-coding` | The core teaching rules: 📘/💡/🔑 blocks, everyday analogies, no unexplained jargon. |
| `hard-case-explainer` | After a tricky bug (it took several tries, the cause was hidden, or the error was misleading), explains the symptom, root cause, why the fix works, and how to spot it next time. |
| `learn-by-doing` | Leaves 3–10 meaningful lines for **you** to write, marked with a `TODO`, plus step-by-step hints and feedback. |
| `i-have-adhd` | Smaller chunks, a 🗺️ progress bar, short sentences with **bold keywords**, one next action at a time. |
| `code-tour` | Lists every function, method and class in a file with line numbers, explains each in one plain sentence, and shows how they call each other. |
| `algorithm-spotter` | Names the algorithms, data structures and design patterns in the code, with Big-O speed translated into everyday words. |

### Commands

| Command | What it does |
|---|---|
| `/explain [thing]` | Explains a file, snippet, command or concept piece by piece. |
| `/why [decision]` | Why this approach? Shows the alternatives and when to switch. |
| `/functions <file> [function]` | A tour of a file: every function with its line number, what it does, inputs → output, and how they connect. Add a function name for a step-by-step deep dive. |
| `/algorithms [file \| function]` | Points out the algorithms, data structures and design patterns, with speed in plain words and any real performance problems. |
| `/map [folder]` | A plain-language map of the project: what each folder and key file is for, how a request flows through it, and where to start reading. |
| `/activity [last N \| files \| commands]` | Everything the AI did this session (files read and changed, commands run) as a plain-language timeline. |
| `/hard-case [case] [save]` | Deep dive into the hard bug that was just solved: flow before and after the fix, failed attempts, how to reproduce it yourself, and similar risks elsewhere in the project. |
| `/quiz [topic]` | A 3-question quiz based on **your** code. Answers come after you reply. |
| `/practice [spot]` | Gives you one small coding task right now, with hints. |
| `/interview [practice]` | Generates talking points for explaining your project, or runs a mock interview one question at a time. |
| `/recap [save]` | A study summary of the session (what you built, concepts, algorithms, hard cases, terms). Add `save` to append it to `LEARNING_NOTES.md`. |
| `/glossary [term]` | A table of the terms you have met, each with a one-line meaning and an everyday example. |
| `/where` | "Where was I?" Shows the goal, progress and the single next step. Useful after a break. |
| `/learn-on` · `/learn-off` | Turns automatic explanations on or off. |
| `/practice-on` · `/practice-off` | Turns on a mode where Claude leaves one small piece of each new feature for you to write. |
| `/adhd-on` · `/adhd-off` | Turns ADHD-friendly mode on or off. |

> Toggles are remembered across sessions. If another plugin uses the same command name, use the prefixed form, for example `/vibe-learning:explain`.

### Hooks

| Hook | What it does |
|---|---|
| `SessionStart` | Loads the teaching rules, plus the ADHD and practice rules if you turned them on, at the start of every session. |
| `UserPromptSubmit` | Adds a one-line reminder on each turn so Claude keeps explaining, and keeps writing 🧮, 🧩 and 🧾 blocks, even in long sessions. |
| `PostToolUse` | Writes one line per tool call (time, tool, file or command) to `~/.claude/vibe-learning/activity/`, which `/activity` reads. It prints nothing, so it costs no tokens. Needs `python3`. |

## 🤖 Using it with OpenAI Codex

The same plugin ships a Codex build in [`codex/`](codex/), published through [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json).

```bash
codex plugin marketplace add VuxSussy/VibeLearning
```

Then:

1. Run `codex`, open `/plugins` and install **vibe-learning**.
2. Run `/hooks` and **trust** the plugin's three hooks. Codex skips plugin hooks until you review them, and without them the automatic explanations won't turn on.
3. Start a new session.

Differences from the Claude Code version:

| Claude Code | Codex |
|---|---|
| `/explain`, `/functions`, `/algorithms`… | `$explain`, `$functions`, `$algorithms`… (Codex plugins have no slash commands, so every command is packaged as a skill) |
| Toggles and the activity log stored in `~/.claude/` | Toggles and the activity log stored in `~/.codex/`. Codex may ask permission before writing there. |
| Hooks run automatically | Hooks must be trusted once via `/hooks` |

**No hooks?** Copy [`codex/hooks/teaching-rules.md`](codex/hooks/teaching-rules.md) into `~/.codex/AGENTS.md`, which Codex reads at the start of every session.

> Maintainers: `codex/` is generated. Edit the Claude Code sources (`skills/`, `commands/`, `hooks/`), then run `python3 scripts/build-codex.py`.

## 🧠 ADHD-friendly mode (`/adhd-on`)

For people who **find it hard to stay focused** or **get overwhelmed by long text**. Each step is still explained in 2–3 lines, but:

| Technique | How it helps |
|---|---|
| 🗺️ Progress bar `✅ → 👉 → ⬜` | You always know which step you're on and how many are left. |
| Sentences of 15 words or fewer, **bold keywords** | Skim and still catch the main idea. |
| `👉 Your turn:` with one action only | No freezing in front of too many choices. |
| `🅿️ Later:` | Side ideas are parked so you don't lose the thread. |
| ✅ Small wins, ☕ break nudges | Keeps you motivated and avoids burnout. |
| `/where` shows a 📍 "you are here" block | Get back on track after a distraction without rereading the whole chat. |

You don't have to run a command. Just say *"I have ADHD"* or *"this is too much text"* and Claude switches to this style.

## 🗺️ Suggested learning loop

1. Ask for what you want as usual, and read the 📘💡🔑 blocks as Claude works.
2. When Claude fixes something tricky, read the 🧩 block. Use `/hard-case` if you want the full story.
3. Something unclear? Use `/explain` or `/why`. Opened a file you don't recognize? Use `/functions` and `/algorithms`.
4. Lost track of what the AI changed? Use `/activity`.
5. Finished a feature? Use `/practice` or `/quiz` to check that it sticks.
6. At the end of the day, run `/recap save` to keep your notes, and `/interview` before a demo or project defense.

## 📁 Structure

```
VibeLearning/
├── .claude-plugin/
│   ├── plugin.json          # plugin metadata
│   └── marketplace.json     # makes it installable via /plugin
├── hooks/
│   ├── hooks.json           # registers the hooks
│   ├── session-start.sh     # injects the rules at session start
│   ├── reminder.sh          # per-turn reminder
│   ├── log-activity.py      # records each tool call for /activity
│   ├── teaching-rules.md    # core teaching rules
│   ├── adhd-rules.md        # extra rules when /adhd-on
│   └── practice-rules.md    # extra rules when /practice-on
├── skills/
│   ├── learn-while-coding/SKILL.md
│   ├── hard-case-explainer/SKILL.md
│   ├── learn-by-doing/SKILL.md
│   ├── i-have-adhd/SKILL.md
│   ├── code-tour/SKILL.md
│   └── algorithm-spotter/SKILL.md
├── commands/                # slash commands
├── codex/                   # generated Codex build (plugin.json, skills/, hooks/)
├── .agents/plugins/marketplace.json   # Codex marketplace
├── scripts/build-codex.py   # regenerates codex/ from the Claude sources
└── LICENSE
```

To change the tone or format of the explanations, edit `hooks/teaching-rules.md` and the `SKILL.md` files.

## 🙏 Inspiration & credits

This plugin's ideas were inspired by the following projects. All text in this repository was written from scratch, and no code or prompts were copied.

- **Anthropic's `explanatory-output-style` plugin** ([anthropics/claude-code](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style)): codebase-specific "insight" notes written alongside the code. Here they became the shorter 🔍 Insight line and the 📘/💡/🔑 blocks.
- **Anthropic's `learning-output-style` plugin** ([anthropics/claude-code](https://github.com/anthropics/claude-code/tree/main/plugins/learning-output-style)): asking the user to write small, meaningful pieces of code at decision points. Here this became `learn-by-doing`, adapted for beginners with step-by-step hints, a "just do it for me" escape, and an ADHD-sized variant.
- **[lyqqqq66666/vibe-coding-learning](https://github.com/lyqqqq66666/vibe-coding-learning)** (MIT): turning AI-written code into study notes and interview talking points. Here this became `/recap save`, the hard-case notes and `/interview`.

## 📄 License

[MIT](LICENSE) © 2026 VuxSussy
