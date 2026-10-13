---
title: Data sources
status: live
updated: 2026-10-13
depends_on: []
---

# Data sources

The live sources of truth for this repository. A fact about an upstream skill (its commit, its
licence, whether it still exists) is read from the source named here, not from an earlier copy in
another document. "Last checked" is the date the commit and licence were read from GitHub.

## Upstream skill sources

| What | Where | Owner | Pinned in repo | How to read it | Licence | Last checked | Status |
|---|---|---|---|---|---|---|---|
| Superpowers (13 skills) | [obra/superpowers](https://github.com/obra/superpowers) | obra | `d884ae0` | `gh api repos/obra/superpowers/commits/d884ae0` | MIT | 2026-10-13 | live |
| pypict skill | [omkamal/pypict-claude-skill](https://github.com/omkamal/pypict-claude-skill) | omkamal | `fbda212` | `gh api repos/omkamal/pypict-claude-skill/commits/fbda212` | MIT (`LICENSE` in the skill; GitHub reports none) | 2026-10-13 | live |
| ffuf skill | [jthack/ffuf_claude_skill](https://github.com/jthack/ffuf_claude_skill) | jthack | `50fd4af` | `gh api repos/jthack/ffuf_claude_skill/commits/50fd4af` | README says MIT; no `LICENSE` file upstream | 2026-10-13 | live, licence unconfirmed |
| webapp-testing | [anthropics/skills](https://github.com/anthropics/skills) | Anthropic | `9d2f1ae` | `gh api repos/anthropics/skills/commits/9d2f1ae` | Apache-2.0 (`LICENSE.txt` in the skill) | 2026-10-13 | live |
| marketing plugin (fork) | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Anthropic | `02ffa99` | `gh api repos/anthropics/knowledge-work-plugins/commits/02ffa99` | Apache-2.0 | 2026-10-13 | live |
| Webflow skills (5) | [webflow/webflow-skills](https://github.com/webflow/webflow-skills) | Webflow | `c8a1650` | `gh api repos/webflow/webflow-skills/commits/c8a1650` | MIT | 2026-10-13 | live |
| Sanity skills (2) | [sanity-io/agent-toolkit](https://github.com/sanity-io/agent-toolkit) | Sanity | `feb9d38` | `gh api repos/sanity-io/agent-toolkit/commits/feb9d38` | MIT | 2026-10-13 | live |
| Contentful skill (1) | [contentful/skills](https://github.com/contentful/skills) | Contentful | `4524f53` | `gh api repos/contentful/skills/commits/4524f53` | MIT | 2026-10-13 | live |
| Web quality skills (3) | [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) | Addy Osmani | `afa8da9` | `gh api repos/addyosmani/web-quality-skills/commits/afa8da9` | MIT | 2026-10-13 | live |
| Marketing skills (3) | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Corey Haines | `28e4a81` | `gh api repos/coreyhaines31/marketingskills/commits/28e4a81` | MIT | 2026-10-13 | live |
| ui-ux-pro-max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Next Level Builder | `7246805` | `gh api repos/nextlevelbuilder/ui-ux-pro-max-skill/commits/7246805` | MIT | 2026-10-13 | live |

## Not vendored on purpose

| What | Where | Reason | Last checked |
|---|---|---|---|
| WordPress agent skills | [WordPress/agent-skills](https://github.com/WordPress/agent-skills) | GPL-2.0-or-later; users install from upstream | 2026-10-13 |
| Respira WordPress skills | [respira-press/agent-skills-wordpress](https://github.com/respira-press/agent-skills-wordpress) | Each skill needs the Respira plugin and MCP server | 2026-10-13 |
| Vercel `web-design-guidelines` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | No upstream `LICENSE` file; fetches unpinned rules at run time | 2026-10-13 |

## Other sources

| What | Where | Owner | How to read it | Last checked | Status |
|---|---|---|---|---|---|
| gocrawl (recommended SEO MCP server) | [Patience-dot-devl/gocrawl](https://github.com/Patience-dot-devl/gocrawl) | Patience-dot-devl | `gh api repos/Patience-dot-devl/gocrawl` and its `README.md`; installed with `go install ...@latest`, so it is not pinned here | 2026-10-13 | live, v0.6.0, MIT |
| Plugin and marketplace schema | `claude plugin validate .` and `claude plugin validate skills/<plugin>` | Anthropic (Claude Code CLI) | Run the command; it prints pass or the failing field | 2026-10-13 | live |
| Star counts and "actively maintained" claims in `README.md` | GitHub repository pages | each upstream | Open the repo; figures change daily | TBD | to confirm |
