# Evaluation: vendored skills vs. our current workflow

This repo's environment (Claude Code inside Conductor) already ships a set of built-in skills:
`deep-research`, `conductor`, `dataviz`, `update-config`, `keybindings-help`, `verify`, `code-review`,
`simplify`, `fewer-permission-prompts`, `loop`, `schedule`, `claude-api`, `run`, `init`, `review`,
`security-review` — plus native Plan mode and multi-agent orchestration (Agent/Workflow tools).
Anything vendored here is only worth adopting if it fills a real gap rather than duplicating one of
those.

Of the ~30 skills in the source post, four passed verification (real repo, actively maintained,
concrete SKILL.md) *and* fill a gap in that built-in set well enough to vendor into
[`skills/vendored/`](skills/vendored/). Everything else is documented in `README.md` as a link-only
reference — either it overlaps with what we already have, is a full application rather than a
drop-in skill, or its quality/maintenance couldn't be confirmed.

## Vendored (`skills/vendored/`)

### `superpowers/` — 13 skills from obra/superpowers (MIT, commit `d884ae0`)

| Skill | Fills a gap? | Notes |
|---|---|---|
| `brainstorming` | Yes | Nothing built-in forces a requirements/design pass before creative work. |
| `systematic-debugging` | Yes | No built-in root-cause-first debugging discipline. |
| `test-driven-development` | Yes | No built-in TDD enforcement. |
| `writing-plans` / `executing-plans` | Partial | Conductor's native Plan mode already covers plan authoring + approval; these add a more prescriptive multi-session checkpoint structure. Try native Plan mode first, reach for these only if you want stricter enforcement. |
| `subagent-driven-development` / `dispatching-parallel-agents` | **Redundant** | Conductor's Agent tool and Workflow tool already do parallel/subagent dispatch natively and more capably. Keeping these vendored for reference only — don't route work through them instead of Agent/Workflow. |
| `using-git-worktrees` | Yes, if you work across branches in parallel | No built-in equivalent. |
| `finishing-a-development-branch` | Yes | No built-in "how should this land" decision checklist; complements the PR-creation guidance already in our instructions rather than replacing it. |
| `requesting-code-review` / `receiving-code-review` | Partial overlap | Conductor's `code-review`/`review` skills *perform* a review; these two govern the *process* of asking for and responding to feedback. Complementary, not duplicate. |
| `verification-before-completion` | Partial overlap | Conductor's `verify` skill already exists for this; this skill is a stricter behavioral rule ("evidence before claims") rather than a runner. Worth keeping as a discipline reminder. |
| `using-superpowers` | **Do not use as-is** | This is a bootstrap skill that assumes Superpowers' own slash-command dispatcher and forces skill-invocation-before-any-response. That model conflicts with how Claude Code/Conductor already discovers and invokes skills here — installing it verbatim would fight the existing Skill/ToolSearch mechanism. Kept for reference only. |
| `writing-skills` | **Redundant** | The `skill-creator` plugin already installed locally (`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator`) covers this same job in this exact environment. |

### `pypict/` — omkamal/pypict-claude-skill (MIT, commit `fbda212`)
Real gap: generates PICT pairwise-combinatorial test matrices from a spec. Nothing built-in does
structured combinatorial test design. Needs the `pict` CLI (or its Python port) installed to actually
run — check `scripts/pict_helper.py` before relying on it.

### `ffuf/` — jthack/ffuf_claude_skill (MIT per README, commit `50fd4af`)
Real gap: this drives **active** fuzzing against a running target with the `ffuf` binary — different
from Conductor's `security-review`, which is a static/diff-based review of pending changes. Only
relevant for authorized pentesting/security-research work, and requires `ffuf` installed separately.

### `webapp-testing/` — anthropics/skills, official (Apache-2.0, commit `9d2f1ae`)
The one skill from the post that turned out to be **official Anthropic**, not community — the
reddit post mislabeled it. Partial overlap with Conductor's `run` skill (both drive a live app in a
browser to confirm a change), but this adds concrete Playwright automation (console-log capture,
element discovery, static-HTML harness) that `run`'s generic fallback doesn't have. Worth reaching
for specifically when `run` needs actual browser scripting rather than manual poking.

## Verified but deliberately not vendored

- **yusufkaraaslan/Skill_Seekers** — real and high-value (doc-site/PDF/repo → skill generator), but
  it's a full standalone application (Python package, MCP server, Docker, CI) rather than a drop-in
  SKILL.md, so copying files into this repo wouldn't make it "work." Install/run it separately from
  its own repo when you need to turn internal docs into a skill.
- **defense-in-depth** — the post's source link (`obra/superpowers/skills/defense-in-depth`) 404s;
  the skill doesn't exist in that repo. Excluded as unverifiable.
- **codeinbox/claude-code-discord** — repo returns 404. Dead link, excluded.
- Research/content skills (Tapestry, article-extractor, youtube-transcript, invoice-organizer,
  claude-epub-skill) — all real repos (see `README.md` for links), but none address a gap in *this*
  coding-focused workflow. Worth revisiting if the work here shifts toward content/research tasks.

## Marketing plugin (`skills/marketing/`)

A fork of Anthropic's `marketing` plugin (anthropics/knowledge-work-plugins, Apache-2.0, commit
`02ffa99`), installable through the marketplace manifest in `.claude-plugin/`. Anthropic's eight
skills are unchanged apart from one pointer in `seo-audit`. The addition is `page-audit`.

`page-audit` was written here from an 18-prompt SEO/GEO/WCAG prompt pack. One skill rather than
eighteen, because every prompt takes the same input (one URL) and needs the same first step, and
eighteen near-identical descriptions would compete for the same trigger. Fills a real gap: nothing
built-in audits a web page, and a plain "analyse this URL" prompt reads a markdown rendering that
drops the title tag, meta description, canonical, JSON-LD and alt attributes the audit is about.
Complements Anthropic's `seo-audit` rather than duplicating it: `seo-audit` is site-wide (keyword
research, content gaps, competitor benchmarks), `page-audit` goes deep on one URL (raw-source
extraction, GEO, WCAG, ready-to-use JSON-LD). Not yet run through an eval loop against a no-skill
baseline.

## Important caveat: vendoring ≠ installed

Copying these `SKILL.md` files into `skills/vendored/` makes them reviewable and diffable in this
repo, but Claude Code doesn't discover skills from an arbitrary repo path — it looks in
`~/.claude/skills/` (personal, global) or a project's own `.claude/skills/` directory (or a
plugin/marketplace). None of that has been touched. To actually put one of these to work, the
concrete next step is copying (or symlinking) the specific skill directory into `~/.claude/skills/`
or a target project's `.claude/skills/` — that's a global-config change, so it's worth deciding
per-skill rather than doing it wholesale.
