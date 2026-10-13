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

Applies to skills written or forked here. Vendored skills stay as received.

- **Frontmatter is valid YAML.** `name` equals the folder name (lowercase letters, digits, hyphens).
  `description` is quoted or a `>-` block when it contains `: ` or quotes. The check enforces this.
- **The description says what and when**, in the third person, under 1024 characters. It is the only
  part that is always in context, so keep it short and put trigger phrases in it, not the workflow.
- **The body is a lean overview**, under 500 lines. Detail goes in `references/` files linked
  directly from `SKILL.md`, one level deep. Do not `@`-import them and do not run shell at load time;
  the body and references then cost nothing until the skill is called.
- **Skills with side effects are user-only.** Add `disable-model-invocation: true` to anything that
  writes files, publishes, deploys or probes a live target. Its description then stays out of
  context until you invoke it by name.
- Pure background knowledge that is not a command can use `user-invocable: false`.

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
