---
description: Stage, commit, and push the current changes
argument-hint: "[optional commit message]"
allowed-tools: Read, Bash(git:*)
---

You are a senior developer saving work on the Spendly expense tracker.
Always follow the rules in CLAUDE.md.

User input: $ARGUMENTS

## Step 1 — Check for changes
Run `git status`. If the working tree is clean (nothing to commit, nothing
untracked), tell the user there is nothing to push and stop.

## Step 2 — Review what changed
Run `git status` and `git diff` (staged and unstaged) to see every change.
Check for anything that looks like a secret or credential (`.env`,
`credentials.json`, API keys, tokens) before staging. If found, warn the
user and exclude it rather than staging it automatically.

## Step 3 — Stage
Stage the relevant files by name (not `git add -A` / `git add .`) so
secrets or unrelated stray files are never swept in unintentionally.

## Step 4 — Commit
If the user supplied $ARGUMENTS, use it as the commit message.
Otherwise, write a concise commit message (1–2 sentences) describing the
*why* of the change, following the style of recent commits
(`git log -5 --oneline` for reference).

## Step 5 — Push
Push the current branch to its remote (`git push`, or
`git push -u origin <branch>` if it has no upstream yet).

## Step 6 — Confirm
Report back:
- The commit hash and message
- The branch pushed
- Whether it was a new branch on the remote or an update to an existing one
