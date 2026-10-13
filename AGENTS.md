# AGENTS.md

Rules for any agent working in this repository. Details are in [CONTRIBUTING.md](CONTRIBUTING.md).

This repo is a public Claude Code plugin marketplace of curated and vendored skills. It is not an
application. The plugins live under `skills/`.

## Before you change anything

- Read [`foundation/data-sources.md`](foundation/data-sources.md). It records every upstream source,
  its pinned commit and its licence. Verify a fact there against the live source before you repeat it.
- Work on a branch. Never commit to `main`.

## Folder boundaries

| Path | What it holds | Rule |
|---|---|---|
| `skills/dev-tools/skills/`, `skills/landing-pages/skills/`, `skills/vendored/` | Vendored upstream skills | Keep exactly as received. Do not edit. Change them only by re-vendoring at a new pinned commit |
| `skills/marketing/`, `skills/repo-playbooks/` | Forks and skills written here | Edit freely; record changes in the plugin README |
| `docs/` | Curated documents, one topic per file | Start from `templates/doc-template.md`. Frontmatter required |
| `foundation/` | Register of live sources | Frontmatter required |
| `sources/` | Raw evidence, as received | Never edit |
| `_inbox/` | Unfiled material | Not referenced until filed |

## Hard rules

- **No GPL-licensed code in vendored plugins** (decided 2026-10-13). Link to the upstream install
  instead. Check the upstream licence before copying and keep its licence text in the plugin. If
  upstream has no `LICENSE` file, add a `NOTICE.md` that says so (see the ffuf skill).
- **No secrets or personal data.** The repo is public. Run the check before every commit.
- **History is append-only.** Corrections are new dated entries in the matching `*.history.md`.
- **Dates are ISO** (YYYY-MM-DD). **Links are relative** and spaces are written `%20`.
- A modification to a vendored file must be named in that plugin's README.

## Before every commit

```bash
python3 scripts/check.py        # must print 0 errors
claude plugin validate .        # when a manifest changed
```

Commit message format: `Scope: summary`.
