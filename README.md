# NGO Executive OS

An AI assistant starter kit for a C-level leader at a small or mid-sized NGO who is responsible for fundraising, strategy, board alignment, and senior relationship management.

**Status: experimental. Use at your own risk. Feedback is welcome, but this is not a maintained product and I may not be able to act on every suggestion.**

This kit is designed to work with Codex and other OpenAI-developed tools that can read a project folder, follow `AGENTS.md`, and use markdown files as working context. It borrows three patterns:

1. Workflow-first executive assistance from [Claude Blattman](https://claudeblattman.com/toolkit/executive-assistant/).
2. Donor and relationship logic from AI chief-of-staff systems such as [mimurchison/claude-chief-of-staff](https://github.com/mimurchison/claude-chief-of-staff).
3. Persistent local memory through Obsidian-compatible markdown files.

The default assistant is intentionally conservative. It can brief, organize, draft, and pressure-test. It should not send messages, publish content, change calendars, or alter records without explicit approval.

## Who This Is For

Use this if you are an NGO executive who needs help with:

- donor follow-up
- board preparation
- funder meeting briefs
- proposal and report tracking
- weekly strategy review
- commitment capture
- relationship memory
- source-grounded fundraising narratives

It is tuned for organizations where the executive is still close to fundraising and strategy, not for large teams with mature CRM, grants, and BI functions.

## What You Get

- `AGENTS.md`: standing instructions for Codex or similar OpenAI tools.
- `routines/`: reusable assistant workflows for briefings, donor review, meeting prep, follow-up, proposal tracking, and strategy review.
- `memory/`: Obsidian-friendly markdown files and folders for donors, board members, partners, projects, commitments, and judgment rules.
- `templates/`: copyable markdown templates for donor profiles, meeting notes, proposals, board briefs, and weekly reviews.
- `docs/`: setup, privacy, customization, and operating guidance.
- `examples/`: sanitized examples that show the expected level of detail.
- `SECURITY.md`: sharing and sensitive-data cautions.
- `LICENSE`: default MIT license, which you should change if you want different terms.

## Quick Start

1. Clone or copy this folder into a private workspace.
2. Open the folder in Codex.
3. Read and customize `AGENTS.md`.
4. Copy files from `templates/` into `memory/` as needed.
5. Store the `memory/` folder in Obsidian if you want a human-readable local knowledge base.
6. Ask Codex to run a routine, for example:

```text
Use routines/morning-brief.md and my memory folder to prepare today's executive brief.
```

or:

```text
Use routines/donor-crm-review.md to review my top donor relationships and tell me what needs attention this week.
```

## Recommended First Week

Start with the smallest working system:

1. Fill out `memory/executive-profile.md`.
2. Add 10 to 25 donor profiles under `memory/donors/`.
3. Add current proposals to `memory/fundraising-pipeline.md`.
4. Add board and partner context only when it affects fundraising or strategy.
5. Run `routines/morning-brief.md` three times.
6. Run `routines/donor-crm-review.md` once.
7. Revise `memory/judgment-rules.md` based on what the assistant gets wrong.

Do not connect private accounts until the rules in `docs/privacy-and-permissions.md` are explicit.

Before publishing publicly, run through `docs/github-publishing-checklist.md`.

## What This Assistant Should Not Do

By default, the assistant should not:

- send email
- publish content
- contact donors
- edit calendar events
- change CRM records
- infer sensitive beneficiary details
- invent donor interests, grant criteria, or board positions
- treat an unsourced memory note as verified fact

It can draft suggested actions, but the executive owns judgment, approval, and accountability.

## Feedback

Open an issue if you try this and find something confusing, risky, missing, or unrealistic. Please do not include real donor, beneficiary, board, staff, financial, legal, or confidential organizational information.

This is an experiment. I may not be able to respond to every issue or act on every suggestion.

## Design Principle

The assistant should make the executive's decision surface smaller. It should not make the decision disappear.

## Validate A Fresh Copy

The end-to-end harness builds a temporary workspace from the files Git would
publish, then validates its operating instructions, routines, memory layout,
templates, links, privacy boundary, and examples.

```bash
python3 -m unittest -v tests.test_e2e
```

The suite contains exactly 20 labeled categories: `U01` to `U10` cover setup
and routine usability; `A01` to `A10` cover accidental secrets, private-memory
publication, unsafe paths or commands, broken links, missing routine contracts,
and incomplete distribution copies. It uses the Python standard library and
does not need an API key, private account, model call, or network access.

To debug one category:

```bash
python3 -m unittest -v tests.test_e2e.ExecutiveOsE2E.test_a05_relative_markdown_links_resolve
```

When adding a routine, add its required inputs to the repository, keep explicit
`Purpose`, `Output`, and `Rules` sections, and extend the corresponding workflow
assertion. GitHub Actions runs the same fresh-copy suite on every pull request.
