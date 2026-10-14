# Contributing

The conventions for this repository. [AGENTS.md](AGENTS.md) is the short version for agents.

## Layout

| Path | Contents |
|---|---|
| `skills/` | Plugins. Each plugin has `.claude-plugin/plugin.json`, a `README.md` and a `skills/` folder |
| `.claude-plugin/marketplace.json` | The marketplace manifest that lists every plugin |
| `docs/` | Curated documents, one topic per file |
| `foundation/data-sources.md` | Register of upstream sources, pinned commits and licences |
| `templates/` | `doc-template.md` and `history-template.md` |
| `sources/`, `_inbox/` | Raw evidence and unfiled material. The check skips both |
| `scripts/check.py` | The pre-commit check |

## Vendoring a skill

1. Read the upstream licence. Do not vendor GPL-licensed material. Link to upstream instead.
2. Copy the skill folder unchanged at a specific commit. Record the commit and licence in the plugin
   README and in [`foundation/data-sources.md`](foundation/data-sources.md).
3. Copy the upstream `LICENSE` into the plugin (`licenses/` for `landing-pages`, beside the skill
   elsewhere). If upstream has no licence file, add a `NOTICE.md` that states what upstream says.
4. If a vendored file must change (for example a script path), make the smallest edit and list it
   under "Changes from upstream" in the plugin README.
5. Add the folder to `VENDORED_PATHS` in `scripts/check.py` and to `.claude-plugin/marketplace.json`
   if it is a new plugin.
6. Add a section to [`docs/SKILLS_EVALUATION.md`](docs/SKILLS_EVALUATION.md) saying what gap it fills
   and what was left out.

## Writing skills

Applies to skills written or forked here. Vendored skills stay as received. These rules follow
Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
and the [Claude Code skills reference](https://code.claude.com/docs/en/skills), as read on
2026-10-14. Neither page has guidance specific to Claude 5.5; recheck both when they change.

- **Frontmatter is valid YAML.** `name` equals the folder name: 1-64 characters, lowercase letters,
  digits and hyphens, no `anthropic` or `claude`. `description` is quoted or a `>-` block when it
  contains `: ` or quotes. The check enforces this.
- **The description says what and when**, in the third person, under 1024 characters (the limit
  outside Claude Code). In Claude Code the description plus `when_to_use` is cut at 1536 characters
  in the skill listing, so put the main use case and trigger phrases first. The description is the
  only part always in context; keep the workflow out of it.
- **The body is a lean overview**, under 500 lines. Add only what Claude does not already know.
  Detail goes in `references/` files linked directly from `SKILL.md`, one level deep. A reference
  file over 100 lines starts with a contents list. Do not `@`-import them and do not run shell at
  load time (`` !`cmd` ``): a failing command aborts the invocation.
- **Match instruction strictness to fragility.** Give judgment calls goals and a default; give
  fragile or destructive sequences an exact command. Offer one default, with an escape hatch, not a
  menu of tools.
- **Run bundled scripts through their interpreter** (`python3 scripts/x.py`), never by bare path:
  some packagers strip executable bits. Scripts handle their own errors and explain every constant.
- **Name MCP tools with their server** (`gocrawl:crawl`) so the tool is found when several servers
  are connected.
- **No dates or "before/after" logic in a skill body.** Put superseded behaviour in an "old
  patterns" section.
- **Side-effect skills are user-only.** Add `disable-model-invocation: true` to anything that
  writes outside the working directory, publishes, deploys or changes a live system. The flag also
  removes the skill from subagent preloading and scheduled tasks, so do not set it on a skill that
  is meant to trigger on ordinary requests or run unattended. A read-only fetch is not a side
  effect.
- Pure background knowledge that is not a command can use `user-invocable: false`.
- **Claude Code only.** `disable-model-invocation`, `argument-hint` and `user-invocable` are
  accepted in Claude Code. Uploading the skill to claude.ai or the Skills API rejects them, so
  strip them if a skill from here is packaged for upload.
- **Test before you ship.** Write at least three realistic requests with the behaviour you expect,
  run them without the skill and with it, and try the skill on more than one model size. No skill
  in this repository has these evaluations yet.

## Documents

- Documents in `docs/` and `foundation/` start with frontmatter: `title`, `status` (`draft`, `live`
  or `superseded`), `updated` (YYYY-MM-DD) and `depends_on` (a list of relative paths; may be empty).
- Folder `README.md` files need no frontmatter.
- Start a new document from [`templates/doc-template.md`](templates/doc-template.md).
- Set `updated` to today on every file you change.

## History

Each document that changes over time has a `<name>.history.md` file, started from
[`templates/history-template.md`](templates/history-template.md). It is append-only. Add new entries
at the bottom with the date. To correct an entry, add a new dated entry that names the one it
corrects. Never edit or delete an old entry.

## Dates and links

- Dates are ISO (YYYY-MM-DD) in frontmatter and in file names.
- Links are relative Markdown links. Write spaces as `%20`. Do not link to this repository by its
  GitHub URL.

## Filing from the inbox

Move the item out of `_inbox/` into `skills/`, `sources/` or `docs/`. Register any live source in
`foundation/data-sources.md`. Delete the inbox copy.

## Before you commit

```bash
git add -A
python3 scripts/check.py      # 0 errors
claude plugin validate .      # when a manifest changed
```

The check covers links, frontmatter, date formats and secrets. Vendored paths skip all but the
secrets check. Work on a branch and open a pull request. Do not commit to `main`.

## Commit messages

`Scope: summary`, for example `landing-pages: add ui-ux-pro-max` or `docs: record GPL decision`.
Use the imperative and keep the summary under about 70 characters.
