---
name: repo-maintainer
description: Enforce a repository's own structure, safety rules and contribution conventions while creating or editing files in it, as defined in its AGENTS.md, CLAUDE.md, CONTRIBUTING.md or .conductor/instructions.md. Use when the user says "repo-standards", asks to keep a repo tidy or consistent, add a new document or module the way the repo expects, review changes against repo conventions, or prepare a commit in a repo that has such rule files.
---

# Repository maintainer

Make changes the way this repository says changes are made. The rules live in
the repo, not here; this skill is the habit of reading and applying them.

## 1. Read the rules first

Read whichever exist: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
`.conductor/instructions.md`. Note the folder boundaries, templates, date and ID
formats, link rules, commit format and the check command. If the repo has none
of these files, say so and suggest running `setup-repo`.

## 2. Place the change

Decide which folder the change belongs in. Respect boundaries such as public or
user-facing docs versus internal or historical records. If a template exists for
this kind of file, start from it and keep its section order and table columns.

## 3. Make the change

- **Single source of truth.** Link to the canonical place for a fact, tool or
  dependency instead of copying it. If you find a duplicate, point it at the
  source.
- **Formats.** ISO dates (YYYY-MM-DD). IDs follow the repo's scheme and are
  never reused.
- **Links.** Relative Markdown links that resolve from the file they are in.
- **History is append-only.** Never rewrite a receipt, log or history entry.
  Correct it with a new dated entry that names what it corrects.

## 4. Check for things that must not be committed

Scan what you wrote for personal data (customer names, emails, addresses, phone
numbers), credentials, API keys and tokens. Remove them, or stop and ask if they
seem to belong there. These are hard to undo once pushed.

## 5. Verify and hand over

Run the repo's check command (usually `python3 scripts/check.py`) and fix what
it reports until it passes. If you cannot run it, give the user the exact
command. Work on a branch; never commit straight to `main` or `master`.

End with the files changed, the check result, and a commit message in the
repo's format (default `Scope: summary`).
