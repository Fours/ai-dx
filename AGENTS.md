# ai-dx

The record of improvements to Kyle's developer experience with Claude Code: settings, `CLAUDE.md` files, skills, memory and scheduled tasks. There is no app or build here, only docs and one skill.

## Layout

- `improvements/YYYY-MM-DD.md`: one doc per round of improvements, named with the date of the round.
  - The newest file is the starting point for the next retro.
  - Docs are append-only history. Don't rewrite past rounds, except to tick off an open item that is now done. Record a second round on the same day as a `## Round 2` section in that day's file.
  - Format, following `2026-11-06.md`:
    - `## Starting point`: key numbers and the friction found
    - `## Improvements`: one `###` per change, saying what changed and where
    - `## Open items`: a checklist. Undone items carry over to the next doc.
- `.claude/skills/retro/`: the `/retro` skill. It's a project skill, so it only loads in sessions started in this folder.
  - `SKILL.md` describes three steps:
    1. Review the chat history since the last doc.
    2. Propose improvements and wait for approval. If nothing is worth changing, it stops there.
    3. Apply the approved changes and write a new doc.
  - `scripts/extract.py <YYYY-MM-DD> <out-dir>` collects data on or after that date from every project's transcripts. Run it with `python3 -I` (standard library only). It writes:
    - `messages.txt`: Kyle's own messages, grouped by session
    - `stats.json`: counts of sessions, messages, output tokens, tools and models
    - It skips subagent turns and harness-injected messages, so prompts from scheduled-task runs don't appear. Check those runs' transcripts directly.

## Where the things being improved live

Most changes made in a retro land outside this repo:

- `~/.claude/settings.json`: global settings. Attribution is already turned off there.
- `~/.claude/CLAUDE.md`: global instructions covering background, git rules and the "set it up like the portfolio" pattern.
- `~/.claude/skills/`: user-level skills: `add-posthog`, `add-s3-deploy`, `mobile-gate`, `next-task`.
- `~/.claude/scheduled-tasks/`: scheduled tasks such as `daily-job-search`. Its project is `~/Documents/Dev/job-search`.
- `~/.claude/projects/<project>/*.jsonl`: chat transcripts, one file per session. Each project's folder name is its path with `/` replaced by `-`. Each project's memory is in its `memory/` folder.
- Project-level `CLAUDE.md` and `AGENTS.md` files in `~/Documents/Dev/*`. Project instructions override the global ones.

Before recommending a change to any of these, read the current file. Earlier docs may be out of date.

## Conventions

- Follow the git rules in `~/.claude/CLAUDE.md`: commit only when asked, straight to `main`, with no Claude attribution. This folder isn't a git repo yet.
- Write docs in plain, specific language. Name the exact file or setting that changed, and give evidence such as counts and which projects were involved.
