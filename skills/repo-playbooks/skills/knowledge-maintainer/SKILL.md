---
name: knowledge-maintainer
description: Maintain a living-documentation or knowledge repository with strict rules - figures verified against registered live sources, append-only history with dated corrections, frontmatter kept current (updated, status, depends_on), relative links that resolve, and a pre-commit check. Use when the user says "maintain-docs", asks to update, correct or extend documentation, record a decision, refresh figures, file something from an inbox, or tidy a knowledge base, docs folder or wiki stored in git.
---

# Knowledge maintainer

Keep documentation true over time. A living doc is only trustworthy if every
figure can be traced to a source and every change can be traced in history.

## 1. Read the repo's rules

Read `AGENTS.md`, `CLAUDE.md` or `CONTRIBUTING.md`, and the data-source register
(usually `foundation/data-sources.md`). The register says where each kind of
figure lives and how fresh it must be.

## 2. Gather before you write

- Open the target documents. Read their frontmatter and follow `depends_on`, so
  you know what else a change affects.
- **Verify figures against the live source** named in the register, not against
  an earlier snapshot in another document. If the live source is out of reach,
  say so and mark the figure as unverified rather than repeating an old number.
- Raw material (exports, screenshots, emails) goes into the inbox or `sources/`
  first and is referenced from there. Do not cite a file that is not filed.

## 3. Make the change

- **Append, don't overwrite.** Earlier claims, receipts, logs and `*.history.md`
  files are history. To change or correct something, update the current text and
  add a dated entry (YYYY-MM-DD) to the matching history file or section that
  says what changed, why, and from which source. Never delete the old entry.
- **Frontmatter.** Set `updated:` to today on every file you modify. Keep
  `status` honest (`draft`, `live`, `superseded`). Add to `depends_on` when a
  document now relies on another.
- **Links.** Relative Markdown links only; encode spaces as `%20`.
- If a change makes a dependent document wrong, update it too or list it as a
  follow-up.

## 4. Verify and hand over

Run the repo's check (usually `python3 scripts/check.py`) and fix everything it
reports; the bar is 0 errors. Confirm no history entry was edited or removed:
`git diff` on history files should show only added lines.

If the repo's rules say not to commit to `main`, make the change on a branch.

End with: files changed, the history entries added, the check result, and a
commit message in the repo's format.
