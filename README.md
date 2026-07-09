# skill-collection

A curated, fact-checked list of community-built Claude Skills and Claude Code hooks worth trying, compiled from a [r/ClaudeAI roundup](https://www.reddit.com/r/ClaudeAI/comments/1ok9v3d/) of 30+ community skills and verified against GitHub (repo existence, activity, star count) as of 2026-07-09.

Official Anthropic skills (docx/pptx/pdf/xlsx) cover common document tasks well but are narrow. These community skills/hooks extend Claude into dev workflows, research, and automation.

## Vendored skills

Four of the skills below were verified, pulled in as actual files, and evaluated against the skills
this environment (Claude Code + Conductor) already ships built-in — see
**[SKILLS_EVALUATION.md](SKILLS_EVALUATION.md)** for the full gap analysis (what's redundant, what's
complementary, what needs adapting) and **[skills/vendored/](skills/vendored/)** for the files
themselves: `superpowers/` (13 skills), `pypict/`, `ffuf/`, `webapp-testing/`.

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