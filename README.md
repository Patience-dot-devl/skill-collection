# skill-collection

A curated, fact-checked list of community-built Claude Skills and Claude Code hooks worth trying, compiled from a [r/ClaudeAI roundup](https://www.reddit.com/r/ClaudeAI/comments/1ok9v3d/) of 30+ community skills and verified against GitHub (repo existence, activity, star count) as of 2026-07-09.

Official Anthropic skills (docx/pptx/pdf/xlsx) cover common document tasks well but are narrow. These community skills/hooks extend Claude into dev workflows, research, and automation.

## Installable plugins

The repo root has a plugin marketplace manifest with three plugins:

```bash
claude plugin marketplace add Patience-dot-devl/skill-collection
claude plugin install marketing@skill-collection
claude plugin install repo-playbooks@skill-collection
claude plugin install dev-tools@skill-collection
claude plugin install landing-pages@skill-collection
```

| Plugin | Skills |
|---|---|
| [`marketing`](skills/marketing/) | Anthropic's marketing plugin plus `page-audit` (see below) |
| [`repo-playbooks`](skills/repo-playbooks/) | `setup-repo`, `repo-maintainer`, `knowledge-maintainer`, `explain-plane` |
| [`dev-tools`](skills/dev-tools/) | `pict-test-designer`, `ffuf-web-fuzzing`, `webapp-testing` |
| [`landing-pages`](skills/landing-pages/) | `ui-ux-pro-max`, `cro`, `ab-testing`, `copywriting`, `core-web-vitals`, `performance`, `web-quality-audit`, `seo-aeo-best-practices`, `content-experimentation-best-practices`, plus Webflow and Contentful skills |

The repository is public, so no access setup is needed.

## Repository layout

| Path | Contents |
|---|---|
| [`skills/`](skills/) | The plugins listed above |
| [`docs/`](docs/) | Curated documents, starting with the [skills evaluation](docs/SKILLS_EVALUATION.md) |
| [`foundation/data-sources.md`](foundation/data-sources.md) | Upstream sources, pinned commits and licences |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to vendor a skill, document conventions, pre-commit check |

Run `python3 scripts/check.py` before every commit. It checks links, frontmatter, dates and secrets.

## Vendored skills

Four of the skills below were verified, pulled in as actual files, and evaluated against the skills
this environment (Claude Code + Conductor) already ships built-in — see
**[docs/SKILLS_EVALUATION.md](docs/SKILLS_EVALUATION.md)** for the full gap analysis (what's redundant, what's
complementary, what needs adapting). Three of them (`pypict`, `ffuf`, `webapp-testing`) now ship in
the `dev-tools` plugin. Superpowers (13 skills) stays in
**[skills/vendored/](skills/vendored/)** for reference; install it from
`superpowers@claude-plugins-official` instead.

## Marketing plugin

**[skills/marketing/](skills/marketing/)** is a fork of Anthropic's `marketing` plugin from
[anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
(Apache-2.0, upstream commit `02ffa99`). It keeps Anthropic's skills (`seo-audit`, `draft-content`,
`content-creation`, `brand-review`, `campaign-plan`, `competitive-brief`, `email-sequence`,
`performance-report`) and adds **`page-audit`**: a single-URL audit for SEO, GEO / AI search, WCAG,
structured data and content quality. `page-audit` turns an 18-prompt SEO/GEO/WCAG prompt pack into
18 modes across five reference files, behind one extraction script (`scripts/extract_page.py`,
Python standard library only) that reads title, meta, canonical, headings, links, images, JSON-LD,
form labels and robots.txt from the raw source. The plugin connects four free MCP servers
(gocrawl, Chrome DevTools, Google Analytics, Search Console) instead of upstream's paid and unused ones; setup is in
the plugin README, which also lists every change from upstream.

Do not also install `marketing@knowledge-work-plugins`; the two share skill names.

## Recommended MCP tool: gocrawl

**[gocrawl](https://github.com/Patience-dot-devl/gocrawl)** is the SEO tool this collection
recommends. It is a free, open-source (MIT) website crawler written in Go that also runs as an MCP
server (`gocrawl mcp`), so an agent can crawl a whole site and read the results as structured data.
It is the maintainer's own project, so weigh that accordingly.

- **Whole-site coverage.** Twenty-five analyzers run on every page: technical SEO, redirects,
  broken links, `robots.txt` and sitemap coverage, structured data, SEA checks (UTM, tracking
  pixels, landing-page relevance) and AI-search checks (AEO and GEO).
- **Lab-mode Core Web Vitals** with headless rendering, which complements the CrUX field data the
  `landing-pages` skills read.
- **Reports and tracking.** JSON, CSV or self-contained HTML, plus saved crawls and a `compare`
  command that shows which issues are new and which are resolved between two crawls.
- **One binary, no runtime dependencies.** `go install` and put it on your `PATH`.

It pairs with `page-audit`: gocrawl finds the pages and issues across a site, and `page-audit`
goes deep on one URL. The `marketing` plugin already wires it up as an MCP server; setup is in
[`skills/marketing/README.md`](skills/marketing/README.md).

### Try it and tell us what breaks

We would like you to try it on a real site. It is young (v0.6.0, under active development), and the
most useful thing you can do is run it and report what you find:

1. Install it: `go install github.com/Patience-dot-devl/gocrawl/cmd/gocrawl@latest` (Go 1.27 or
   later; Chrome or Chromium only if you want headless rendering).
2. Crawl a site you know well: `gocrawl crawl https://your-site.example --format html --out report.html`.
3. **[Open an issue](https://github.com/Patience-dot-devl/gocrawl/issues/new)** for anything wrong:
   a false positive, a missed problem, a crash, a confusing flag or a missing analyzer. Include the
   command you ran and what you expected.
4. Tell us what is missing, even if nothing is broken: which checks you rely on in other tools, and
   which reports you would hand to a client. Feedback on the MCP tools (`crawl`, `list_analyzers`)
   is especially welcome, since that is the part agents use.

Contributions follow the repository's
[CONTRIBUTING.md](https://github.com/Patience-dot-devl/gocrawl/blob/main/CONTRIBUTING.md).

## Repository playbooks

**[skills/repo-playbooks/](skills/repo-playbooks/)** turns four JSON playbooks (`setup-repo`,
`repo-maintainer`, `knowledge-maintainer`, `explain-plane`) into skills. The JSON versions lived in
`~/.claude/plugins/global-playbooks/` without a plugin manifest, so Claude Code never loaded them.
`setup-repo` ships a tested convention checker (`scripts/check.py`) and templates instead of
having them written from scratch each time.

## Hubs (start here)

- **[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)** — the biggest, most active curated list of Claude Code skills, agents, hooks, and tooling (~49.5k stars, updated same-day).
- **[BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills)** — curated list of Claude Skills across categories (~9.7k stars).
- **[travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)** — another well-maintained Claude Skills list, more workflow-focused (~14k stars).

## The essentials

- **[obra/superpowers](https://github.com/obra/superpowers)** — the flagship skills framework: brainstorming, TDD enforcement, systematic debugging, execution planning, code review, git-worktree workflows, all via slash commands. Confirmed skill directories: `brainstorming`, `test-driven-development`, `systematic-debugging`, `using-git-worktrees`, `finishing-a-development-branch`, `executing-plans`, `writing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `receiving-code-review`, `requesting-code-review`, `verification-before-completion`. Extremely active, by far the most starred skill repo out there — the default recommendation for coding work.
- **[obra/superpowers-lab](https://github.com/obra/superpowers-lab)** — experimental/bleeding-edge companion to Superpowers, for trying new techniques before they land in the stable repo.
- **[yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)** — turns any documentation site, GitHub repo, or PDF into a Claude Skill automatically. Highest-leverage pick if you work with internal/niche frameworks Claude doesn't know about (~14.4k stars, actively maintained).

## Developer workflow

All of the following are inside **obra/superpowers** (see directory list above) or the **BehiSecc/awesome-claude-skills** index — check there rather than searching separately:

- Test-Driven Development, Systematic Debugging, Finishing a Development Branch, Using Git Worktrees — all in `obra/superpowers`.
- Pypict (combinatorial test-case generation), Webapp Testing with Playwright, ffuf security fuzzing, Defense-in-Depth security/quality checks — listed in `BehiSecc/awesome-claude-skills`.

## Research & knowledge

- **Tapestry** — turns a pile of technical PDFs/docs into a navigable, queryable knowledge graph. Listed in both `BehiSecc/awesome-claude-skills` and `travisvn/awesome-claude-skills`.
- YouTube transcript / article extractor-summarizer skills — listed in `BehiSecc/awesome-claude-skills`.
- Content Research Writer (citations + research organization) — listed in `BehiSecc/awesome-claude-skills`.
- EPUB & PDF Analyzer (query/summarize ebooks and papers) — listed in `BehiSecc/awesome-claude-skills`.

## Productivity & automation

- Invoice/File Organizer — smart categorization of receipts/documents. Listed in `BehiSecc/awesome-claude-skills`.
- Web Asset Generator — icons, Open Graph tags, PWA assets. Listed in `BehiSecc/awesome-claude-skills` and `travisvn/awesome-claude-skills`.

## Claude Code hooks

- **[johnlindquist/claude-hooks](https://github.com/johnlindquist/claude-hooks)** — TypeScript hooks framework with typed payloads and autocompletion. Solid foundation if you're comfortable in TS, but repo activity has slowed (last push Aug 2025) — check for maintained forks before depending on it.
- **CCHooks** (Python), **claude-code-hooks-sdk** (PHP/Laravel-style), **Claudio** (native OS sound alerts), **CC Notify** (desktop notifications on task completion), **fcakyon's code-quality hook collection**, **TypeScript quality hooks by bartolli** — all indexed in `hesreallyhim/awesome-claude-code`; search that repo rather than the author names directly since some aren't easily findable standalone.

## Known dead link

- `codeinbox/claude-code-discord` (Discord/Slack activity notifications), mentioned in the original post, returns **404** — repo no longer exists or was renamed. Not included above.

## Practical notes from the source post

- Skills that solve one specific problem well outperform "makes Claude smarter" generic skills.
- Dev-focused skills tend to be highest quality (built by devs solving their own problems).
- Hooks have a real learning curve but pay off for teams enforcing standards.
- Documentation-to-skill generators (Skill Seekers) are a quietly high-leverage category.