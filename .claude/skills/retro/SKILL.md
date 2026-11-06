---
name: retro
description: Run a developer-experience retrospective. Read Claude Code chat history since the last improvements doc, propose improvements to how Kyle works with Claude, and after approval apply them and record them in a new dated doc in improvements/. Use when the user says "/retro", "run a retro", or asks to review recent sessions for things to improve.
---

# Retro

A retrospective on how Kyle works with Claude Code. Each round is recorded in `improvements/YYYY-MM-DD.md` in this repo, so the folder is the history of every round. Follow the three steps in order. Don't change anything before Step 3.

## Step 1: Review the history since the last retro

1. **Find the start date.** List `improvements/*.md` and take the latest date from the file names. If the folder is empty, ask Kyle for a start date.
2. **Read the last doc.** Note what was already done and its **Open items**. Don't propose those improvements again. Do check whether each open item is now done.
3. **Extract the history.** Run the bundled script:

   ```bash
   python3 -I .claude/skills/retro/scripts/extract.py <start-date> <scratchpad>/retro
   ```

   - The start date is inclusive, because the last retro's day may have had sessions after its doc was written. Skip anything that the last doc already covers.
   - The script writes two files:
     - `messages.txt`: Kyle's own messages from every project, grouped by session.
     - `stats.json`: counts of sessions, messages, output tokens, tools and models.
   - Read all of `messages.txt`. Ignore this retro session itself.
4. **Look for:**
   - **Repeated corrections or preferences:** something Kyle has said more than once, which belongs in `~/.claude/CLAUDE.md`, a project's `CLAUDE.md`, settings or memory.
   - **Repeated workflows:** setup steps or prompt sequences that would work as a skill, or existing skills that misfired, were skipped or need updating. User-level skills are in `~/.claude/skills/`.
   - **Friction:**
     - permission prompts that could go on an allowlist
     - stuck or failed scheduled runs (check `~/.claude/scheduled-tasks/` and that project's transcripts)
     - slow loops
     - work that was abandoned
   - **Stale context:** instructions in `CLAUDE.md`, `AGENTS.md`, skills or memory that contradict each other or no longer match how Kyle works.
   - **Interesting data** worth tracking over time: session and message counts, the busiest project, top tools and model mix. Compare them with the previous doc.

   Use transcript files in `~/.claude/projects/` when you need detail beyond Kyle's messages. When a finding names a file, setting or skill, check it still exists and still says what you think.

## Step 2: Propose improvements

- **If nothing is worth changing,** say so in a few lines and include any interesting data. The retro is done: don't write a doc.
- **Otherwise,** present the findings:
  - a short **Starting point**: the period covered, the key numbers and what's working well
  - a numbered list of proposed improvements, most valuable first
    - For each one, give the evidence (how often it happened and in which projects) and the exact change (which file or setting, and what it will say).
  - the status of each open item from the last doc
- **Ask Kyle** whether to implement them: all, some (by number) or none. Wait for the answer.
  - **No:** stop. Nothing is changed and no doc is written.
  - **Yes:** go to Step 3 with only the approved items.

## Step 3: Apply and record

1. **Apply the approved improvements.** Edit settings, `CLAUDE.md` files, skills or memory as proposed.
   - Follow Kyle's git rules: commit only when asked, straight to `main`, with no Claude attribution.
   - Verify each change: valid JSON, skill frontmatter, files where they should be.
   - If something can't be applied, keep it as an open item and say why. For example, Claude Code may block the edit, or Kyle may need to do it by hand.
2. **Write `improvements/<today>.md`.** Use today's date. If that file already exists, add a `## Round 2` section to it instead. Follow the format of earlier docs:
   - `# Developer experience improvements: <date>`
   - **Source session:** this retro and the period of history it covered.
   - `## Starting point`: key numbers and friction found.
   - `## Improvements`: one `###` heading per improvement, saying what changed and where.
   - `## Open items`: a checklist. Include the open items from the last doc that are still undone, plus anything left from this round. Mark the ones carried over.
3. **Report:** list what changed and give a link to the new doc.
