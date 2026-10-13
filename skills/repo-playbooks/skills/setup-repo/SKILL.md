---
name: setup-repo
description: Scaffold a new repository, or standardize an existing one, into a contract-driven knowledge layout with _inbox/, foundation/, sources/, templates/, a scripts/check.py convention checker, AGENTS.md, CLAUDE.md, CONTRIBUTING.md and README.md, plus project settings that enable the repo-playbooks plugin for everyone who works in it. Use when the user says "setup-repo", asks to set up, bootstrap, scaffold or initialise a repo or workspace, or wants an existing repo brought in line with the standard layout.
disable-model-invocation: true
---

# Set up a repository

Build the standard layout so that every repo works the same way for people and
agents: raw material lands in one place, live truth is registered in one place,
documents follow templates, and one script checks the conventions before a
commit. The maintenance skills in this plugin (`repo-maintainer`,
`knowledge-maintainer`) assume this layout.

## 1. Understand the repo

Get the project name and its subject from the request. If the folder already
has content, look at it first: keep existing files, fit them into the layout,
and list anything you moved. Never overwrite an existing `README.md`,
`AGENTS.md`, `CLAUDE.md` or `CONTRIBUTING.md` without showing the user the
difference.

## 2. Create the layout

| Path | Contents |
|---|---|
| `_inbox/INBOX.md` | How to drop uncurated files here, and that nothing in `_inbox/` is referenced until it is filed |
| `foundation/data-sources.md` | Register of live sources of truth: what, where, owner, how to read it, last checked |
| `docs/README.md` | Index of curated documents, one topic per file, each started from the doc template. Folder `README.md` files need no frontmatter |
| `sources/` | Raw exports and evidence, kept as received. Add a `README.md` saying so |
| `templates/` | Copy `assets/templates/doc-template.md` and `assets/templates/history-template.md` |
| `scripts/check.py` | Copy `assets/scripts/check.py` and make it executable |
| `.claude/settings.json` | Plugin settings, see below |

Copy the bundled files rather than writing new ones, so every repo runs the same
checker. Then adjust the settings block at the top of `check.py`:
`FRONTMATTER_REQUIRED` lists the folders whose documents need frontmatter
(`foundation` and `docs` by default); `OWN_URL_PREFIXES` gets the repo's web URL
if it already has a remote, and stays empty otherwise.

Fill the data-source register only with what the user told you or what you can
see. Sources the project will probably need (analytics, a CMS, Search Console)
may be listed as `status: to confirm` with owner `TBD`, so the register never
claims a source that nobody checked. Do not create history files yet; the first
one is made alongside the first document that changes.

`.claude/settings.json` makes Claude Code offer this plugin to everyone who
opens the repo. Merge into an existing file instead of replacing it:

```json
{
  "extraKnownMarketplaces": {
    "skill-collection": {
      "source": { "source": "github", "repo": "Patience-dot-devl/skill-collection" }
    }
  },
  "enabledPlugins": {
    "repo-playbooks@skill-collection": true
  }
}
```

The `skill-collection` repo is private, so this only works for people with
access to it. Mention that if the repo will have other contributors.

## 3. Write the contract files

- **`AGENTS.md`**: the rules an agent must follow here: folder boundaries, the
  data-source register, append-only history, date and link conventions, "run
  `python3 scripts/check.py` before every commit, 0 errors", no commits to
  `main`. Point to `CONTRIBUTING.md` for details instead of repeating them.
- **`CLAUDE.md`**: one line, `@AGENTS.md`, so Claude Code loads the same rules.
- **`CONTRIBUTING.md`**: the conventions in full: ISO dates (YYYY-MM-DD) in
  frontmatter and file names, relative Markdown links with spaces as `%20`,
  required frontmatter (`title`, `status`, `updated`, and `depends_on`, which
  may be an empty list) for `foundation/` and `docs/`, how history
  files work, how to file something from `_inbox/`, commit message format
  (`Scope: summary`).
- **`README.md`**: what the repo is for, an index of the main documents, and a
  short status section.

Write these for this project, with its name and subject; generic boilerplate
gets ignored.

## 4. Verify

Run `python3 scripts/check.py`. Fix whatever it reports in the files you
created until it prints 0 errors. It only sees files git knows about, so run
`git add -A` first in a new repo.

Leave committing to the user. Report the tree you created, any files you moved,
and any register entries marked `to confirm`. Remind them that the check runs
before every commit, and that after the first commit, work happens on branches
rather than on `main`.
