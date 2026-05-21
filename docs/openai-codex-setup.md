# OpenAI Codex Setup

This kit is designed as a folder-based assistant. Codex reads the repo, follows `AGENTS.md`, and uses markdown files as its working memory.

## Setup

1. Put this folder in a private workspace.
2. Open the folder with Codex.
3. Review `AGENTS.md`.
4. Customize the memory files before using live organizational information.
5. Start with read-only analysis and draft generation.

## Running A Routine

Ask Codex to use a specific routine file:

```text
Use routines/meeting-prep.md to prepare for my meeting with [name]. Use relevant memory files, and ask before using connected accounts.
```

or:

```text
Use routines/weekly-strategy-review.md. Focus on fundraising and board priorities for the next two weeks.
```

## Using With ChatGPT

You can upload this folder or selected files into ChatGPT and ask it to follow `AGENTS.md`. For best results, include:

- `AGENTS.md`
- the routine you want to run
- relevant memory files
- any source documents needed for the task

Do not upload sensitive donor, staff, or beneficiary information unless your organization has approved that use.

## Using With Obsidian

Open this folder as an Obsidian vault, or put only the `memory/` folder inside an existing vault. The files are plain markdown and do not require plugins.

Recommended practice:

- use one file per donor, board member, partner, and active strategic project
- keep `commitments.md` current
- review `judgment-rules.md` weekly
- store sensitive notes in `memory/private/`, which is ignored by git

