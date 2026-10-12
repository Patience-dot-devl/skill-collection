# repo-playbooks

Four skills for setting up and maintaining repositories. They replace the JSON playbooks that
used to live in `~/.claude/plugins/global-playbooks/`, which Claude Code did not load as skills.

| Skill | Trigger word | What it does |
|---|---|---|
| `setup-repo` | `setup-repo` | Scaffolds `_inbox/`, `foundation/`, `sources/`, `templates/`, `scripts/check.py`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, and a `.claude/settings.json` that enables this plugin for the repo |
| `repo-maintainer` | `repo-standards` | Applies the repo's own rules when adding or changing files: folder boundaries, templates, no personal data or secrets, append-only history, check before commit, no commits to `main` |
| `knowledge-maintainer` | `maintain-docs` | Keeps living docs true: figures checked against the data-source register, dated corrections in history files, frontmatter and links kept current |
| `explain-plane` | `explain-plane` | Explains code and concepts in ASD-STE100 Simplified Technical English |

The trigger words are in each skill's description, so typing them still invokes the skill. The
skills also trigger on ordinary requests ("set up this repo", "update the docs").

## The checker

`skills/setup-repo/assets/scripts/check.py` is copied into each new repo as `scripts/check.py`.
Python standard library only. It checks Markdown links and anchors, spaces in link targets,
required frontmatter keys per folder, YYYY-MM-DD dates in frontmatter and file names,
`depends_on` targets, and likely secrets. It exits 1 on any error. Settings at the top of the
file adapt it per repo.

## Install

```bash
claude plugin marketplace add Patience-dot-devl/skill-collection
claude plugin install repo-playbooks@skill-collection
```

Repos created with `setup-repo` also offer the plugin automatically through their
`.claude/settings.json`, for anyone with access to `skill-collection`.
