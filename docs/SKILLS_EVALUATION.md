---
title: Evaluation of vendored skills against the current workflow
status: live
updated: 2026-10-18
depends_on:
  - ../foundation/data-sources.md
  - ../sources/skill-baselines-2026-10-18/README.md
---

# Evaluation: vendored skills vs. our current workflow

This repo's environment (Claude Code inside Conductor) already ships a set of built-in skills:
`deep-research`, `conductor`, `dataviz`, `update-config`, `keybindings-help`, `verify`, `code-review`,
`simplify`, `fewer-permission-prompts`, `loop`, `schedule`, `claude-api`, `run`, `init`, `review`,
`security-review` — plus native Plan mode and multi-agent orchestration (Agent/Workflow tools).
Anything vendored here is only worth adopting if it fills a real gap rather than duplicating one of
those.

Of the ~30 skills in the source post, four passed verification (real repo, actively maintained,
concrete SKILL.md) *and* fill a gap in that built-in set well enough to vendor into
[`skills/vendored/`](../skills/vendored/). Everything else is documented in [`README.md`](../README.md) as a link-only
reference — either it overlaps with what we already have, is a full application rather than a
drop-in skill, or its quality/maintenance couldn't be confirmed.

## Vendored (`skills/vendored/`, and the `dev-tools` plugin)

`pypict`, `ffuf` and `webapp-testing` moved to `skills/dev-tools/skills/` so they can be installed
as the `dev-tools` plugin; their files are unchanged. Superpowers stays here as a reference copy.

### `superpowers/` — 15 skills from obra/superpowers (MIT, commit `bb92a77`, v7.0.0)

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
| `diagnosing-superpowers` | **No** | New in v7.0.0. Builds bug reports for the Superpowers maintainers from session transcripts. Useful only if you run the full Superpowers framework; not a general workflow skill. Kept for reference only. |
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

## Landing-pages plugin (`skills/landing-pages/`)

Fifteen skills from six upstream repos, chosen to cover design, conversion, measurement and the CMS
layer for landing pages. No single upstream skill spans CMSs, so the plugin groups by job.

| Group | Skills | Gap it fills |
|---|---|---|
| Design and UX | `ui-ux-pro-max` | Nothing built-in gives searchable style, palette, font, UX-rule and landing-page-pattern data. Overlaps partly with the installed `frontend-design`, which sets aesthetic direction but has no lookup data. |
| Conversion | `cro`, `ab-testing`, `copywriting`, `content-experimentation-best-practices` | `marketing:page-audit` and `seo-audit` cover SEO, GEO and WCAG; none cover CRO, test design or sample size. |
| Performance and CrUX | `core-web-vitals`, `performance`, `web-quality-audit`, `seo-aeo-best-practices` | `page-audit` reads one page's source; these add field-data (CrUX p75) triage and lab-vs-field reasoning. They reuse the Chrome DevTools and Search Console MCP servers already in the `marketing` plugin. |
| CMS | Webflow (5), `contentful-nextjs` | Webflow's official skills drive its MCP server. Contentful's covers Next.js preview and Draft Mode. |

Held back or excluded (details in the plugin README): WordPress/agent-skills (GPL-2.0-or-later,
deliberately not vendored; install from upstream), Respira WordPress skills (require the Respira plugin and MCP server),
Vercel `web-design-guidelines` (no upstream LICENSE file; fetches unpinned rules at run time),
`contentful-personalization` (large, ships a script).

One edit to vendored files: `ui-ux-pro-max/SKILL.md` script paths changed from
`${CLAUDE_PLUGIN_ROOT}/.claude/skills/…` to `${CLAUDE_PLUGIN_ROOT}/skills/…` to match this plugin's
layout. The `${CLAUDE_PLUGIN_ROOT}` substitution itself was not exercised inside a live Claude Code
session; the search script was run directly.

## Baseline test: marketing skills against no skill (2026-10-18)

Five `marketing` skills were run with and without the skill on the same requests and graded blind.
Method, prompts, all 30 outputs and the grades are in
[`sources/skill-baselines-2026-10-18/`](../sources/skill-baselines-2026-10-18/README.md).

| Skill | Opus 5.5 (2 pairs) | Haiku 5.5 (1 pair) |
|---|---|---|
| `draft-content` | with skill ×2, small | with skill, small |
| `campaign-plan` | tie; with skill, small | without, small |
| `competitive-brief` | with skill ×2, small | **without, large** |
| `email-sequence` | without ×2, small | with skill, small |
| `brand-review` | with skill; without (both small) | with skill, small |
| **Total** | **6 with, 3 without, 1 tie** | **3 with, 2 without** |

What the results show:

- **The differences are small.** 14 of 15 verdicts were "small" or a tie. No skill made the core
  deliverable clearly better.
- **Wins came from extras, not from the core work.** The skill versions added SEO notes, pre-publish
  fact-check lists and battlecards. The plans, sequences and copy were of similar quality.
- **The skill makes output about 70% longer** on both models, and graders tend to reward length.
- **`brand-review` found nothing extra.** With and without the skill, Opus caught all 11 planted
  violations in each draft. The skill versions flagged more non-issues (3 against 0 across the Opus
  pairs).
- **The one large difference went against the skill.** On Haiku, `competitive-brief` with the skill
  stated wrong competitor prices as fact. The template asks for more claims than a small model can
  check.

Conclusion: for writing tasks that the model already handles, a long section-by-section template adds
length, not quality. What earns its place in a skill is the short, non-obvious rule: verify each
competitor price against its live page, check the funnel and budget arithmetic, check weekdays against
dates. This matches the "add only what Claude does not already know" rule in
[CONTRIBUTING.md](../CONTRIBUTING.md#writing-skills).

Limits: 15 pairs, one sample each, one LLM grader. The skill body was read directly, so triggering was
not tested. `performance-report`, `seo-audit` and the landing-pages skills were not tested.

## Triage: keep, slim, drop (2026-10-18)

A recommendation, not yet carried out. Vendored skills can only be kept or dropped; slimming applies
to skills that are forked or written here.

| Verdict | Skills | Why |
|---|---|---|
| Drop | `skills/vendored/superpowers/` (15) | Not in the marketplace. The official `superpowers` plugin is installed and newer; the copy here only goes stale |
| Drop | `marketing:brand-review` | No extra catches in the baseline test and more false positives. The value is in the user's own brand guide, not in the template |
| Drop | `marketing:email-sequence` | Lost 2 of 3 pairs to no skill |
| Drop | `marketing:content-creation` | Background twin of `draft-content`; the same job under a second trigger |
| Slim | `marketing:campaign-plan` | Keep the checks the graders caught missing: funnel and budget sums, weekdays against dates, target met or gap stated |
| Slim | `marketing:competitive-brief` | Keep the battlecard and the rule to verify every competitor price against its live page and mark the rest unverified |
| Slim | `marketing:draft-content` | Keep the SEO notes and the pre-publish fact-check list; drop the per-channel templates |
| Keep | `dev-tools` (3), `landing-pages:ui-ux-pro-max`, `landing-pages:web-quality-audit` | Ship scripts, data or a CLI workflow the model cannot do alone |
| Keep | Webflow (5), `contentful-nextjs` | Drive a specific MCP server or API |
| Keep | `marketing:page-audit`, `repo-playbooks` (4) | Scripts and repo conventions; both already have evals |
| Test next | `cro`, `copywriting`, `ab-testing`, `core-web-vitals`, `performance`, `seo-aeo-best-practices`, `content-experimentation-best-practices`, `marketing:performance-report`, `marketing:seo-audit` | Mostly general knowledge; run the same baseline before keeping |

## Important caveat: vendoring ≠ installed

This section applies to what remains in `skills/vendored/` (Superpowers). The `marketing`,
`repo-playbooks` and `dev-tools` plugins are installable through the marketplace manifest.

Copying these `SKILL.md` files into `skills/vendored/` makes them reviewable and diffable in this
repo, but Claude Code doesn't discover skills from an arbitrary repo path — it looks in
`~/.claude/skills/` (personal, global) or a project's own `.claude/skills/` directory (or a
plugin/marketplace). None of that has been touched. To actually put one of these to work, the
concrete next step is copying (or symlinking) the specific skill directory into `~/.claude/skills/`
or a target project's `.claude/skills/` — that's a global-config change, so it's worth deciding
per-skill rather than doing it wholesale.
