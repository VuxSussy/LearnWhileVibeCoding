
# Type-it-yourself mode is ON (skill `type-it-yourself`)
The user wants to learn their tools by typing the commands themselves. Commands that change the project through
git or a package manager (git add/commit/push/branch..., npm/yarn/pnpm/bun install/add/remove/init, npx create-*, pip install) are blocked by a guard hook.
Never run them or work around them. Hand them over in a `⌨️ Your turn` checklist: the exact command, 📘 what it does, 🔍 what each part means, ✅ what success looks like
(plus ⚠️ common error, 🛑 for risky commands). Wait for "done", then verify with a read-only command such as `git status` or `npm ls`.
