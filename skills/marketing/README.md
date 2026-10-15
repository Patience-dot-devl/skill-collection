# Marketing Plugin

> **Fork notice.** This is a copy of the `marketing` plugin from
> [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
> (Apache-2.0, upstream commit `02ffa99`, 2026-10-11), modified in this repository:
>
> - Added the `page-audit` skill (`skills/page-audit/`), built from an 18-prompt SEO, GEO and
>   WCAG prompt pack.
> - `seo-audit`: the on-page step points to `page-audit` for a deeper single-page pass, and the
>   technical step uses `~~site crawler` when connected.
> - `plugin.json`: version suffix and description updated.
> - `.mcp.json`: upstream servers replaced by gocrawl, Chrome DevTools, Google Analytics and Search
>   Console; see MCP Integrations below.
> - `CONNECTORS.md`: the table shows this fork's servers and adds the `~~site crawler` and
>   `~~browser` categories.
>
> All other files are unchanged from upstream. To pull in upstream changes, diff this directory
> against `marketing/` at a newer upstream commit.

A marketing plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Content creation, campaign planning, brand voice management, competitive analysis, and performance reporting.

## Installation

```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install marketing@knowledge-work-plugins
```

## Commands

| Command | Description |
|---|---|
| `/draft-content` | Draft blog posts, social media, email newsletters, landing pages, press releases, and case studies |
| `/campaign-plan` | Generate a full campaign brief with objectives, channels, content calendar, and success metrics |
| `/brand-review` | Review content against your brand voice, style guide, and messaging pillars |
| `/competitive-brief` | Research competitors and generate a positioning and messaging comparison |
| `/performance-report` | Build a marketing performance report with key metrics, trends, and optimization recommendations |
| `/seo-audit` | Run a comprehensive SEO audit — keyword research, on-page analysis, content gaps, technical checks, and competitor comparison |
| `/email-sequence` | Design and draft multi-email sequences for nurture flows, onboarding, drip campaigns, and more |

## Skills

| Skill | Description |
|---|---|
| `content-creation` | Content type templates, writing best practices by channel, SEO fundamentals, headline formulas, and CTA guidance |
| `campaign-planning` | Campaign frameworks, channel selection, content calendar creation, budget allocation, and success metrics |
| `brand-voice` | Brand voice documentation, voice attributes, tone adaptation, style guide enforcement, and terminology management |
| `competitive-analysis` | Competitive research methodology, messaging comparison, content gap analysis, positioning, and battlecard creation |
| `performance-analytics` | Key metrics by channel, reporting templates, trend analysis, attribution modeling, and optimization frameworks |
| `page-audit` | Single-URL audit for SEO, GEO / AI search, WCAG, structured data and content quality: 18 modes behind one raw-source extraction script (added in this fork) |

## Example Workflows

### Drafting a Blog Post

```
> /draft-content
Type: blog post
Topic: How AI is transforming B2B marketing
Audience: Marketing directors at mid-market SaaS companies
Key messages: AI saves time on repetitive tasks, improves personalization, requires human oversight
Tone: Authoritative but approachable
Length: 1200 words
```

Claude will generate a structured blog post draft with an engaging headline, introduction with a hook, organized sections, SEO-optimized subheadings, and a clear call to action.

### Planning a Campaign

```
> /campaign-plan
Goal: Drive 500 signups for our new product launch
Audience: Technical decision-makers at enterprise companies
Timeline: 6 weeks
Budget range: $20,000-$30,000
```

Claude will produce a campaign brief covering objectives, audience segmentation, key messages, channel strategy, a week-by-week content calendar, and KPIs to track.

### Reviewing Content Against Brand Guidelines

```
> /brand-review
[paste your draft content]
```

If your brand style guide is configured in local settings, Claude will check your content against voice, tone, terminology, and messaging pillars. If not configured, Claude will ask about your guidelines or provide a generic review for clarity, consistency, and professionalism.

## Configuration

Configure your brand voice, style guide, and target personas in a local settings file for personalized output. This allows commands like `/draft-content` and `/brand-review` to automatically apply your brand standards without prompting each time.

## MCP Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

This fork pre-configures four free MCP servers. They run locally, so each machine needs the
setup below. A server that is not set up fails to start; the skills keep working without it.

| Server | Category | Gives the skills | Source |
|---|---|---|---|
| **gocrawl** | `~~site crawler` | Technical, on-page, structured data, AEO/GEO checks; Core Web Vitals with headless rendering | [Patience-dot-devl/gocrawl](https://github.com/Patience-dot-devl/gocrawl) |
| **chrome-devtools** | `~~browser` | Headless Chrome with DevTools: Lighthouse (accessibility, SEO, best practices), performance traces with Core Web Vitals and CrUX field data, network, console, screenshots | Google's official [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) (Apache-2.0), pinned to 1.10.1 |
| **google-analytics** | `~~product analytics`, `~~marketing analytics` | GA4 reports: sessions, engagement, conversions, funnels | Google's official [google-analytics-mcp](https://github.com/googleanalytics/google-analytics-mcp) (Apache-2.0) |
| **search-console** | `~~SEO` | Real queries, clicks, CTR, positions, URL inspection, sitemaps | Community [AminForou/mcp-gsc](https://github.com/AminForou/mcp-gsc) (MIT), pinned to 0.4.1. Google has no official one. |

### Setup

The two Google servers run through `uvx`, which comes with [uv](https://docs.astral.sh/uv/).
Credentials are read from environment variables, which Claude Code passes on to the servers. Set
them in your shell profile or under `env` in `~/.claude/settings.json`; nothing secret goes into
this plugin.

**gocrawl**

```bash
go install github.com/Patience-dot-devl/gocrawl/cmd/gocrawl@latest
```

The `gocrawl` binary must be on your `PATH`. Headless rendering also needs Chrome or Chromium.

gocrawl is young. If you try it, please [open an issue](https://github.com/Patience-dot-devl/gocrawl/issues/new)
for anything that is wrong or missing, and say which analyzers you would like to see.

**Chrome DevTools**

Needs Node.js (`npx`) and Google Chrome. Chrome starts on the first browser call, not with the
session, and runs headless with a throwaway profile (`--isolated`), so it never sees your own
logins. Usage statistics to Google are switched off. Performance traces do send the audited URL to
Google's CrUX API to fetch real-user data; add `--performanceCrux=false` to the args to stop that.

**Browser fallback (not a server)**

When no browser server is connected, `page-audit` runs a headless browser through
`skills/page-audit/scripts/browser_check.py` only during a WCAG check. It uses Playwright via `uv` (installed on
first use) and axe-core, downloaded once into `~/.cache/page-audit`. Install Chromium once with
`uv run skills/page-audit/scripts/browser_check.py --install-browser`.

**Google Analytics** (read-only)

1. In a Google Cloud project, enable the Google Analytics Admin API and Data API.
2. Sign in with Application Default Credentials and the read-only scope:
   ```bash
   gcloud auth application-default login \
     --scopes https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform \
     --client-id-file=YOUR_CLIENT_JSON_FILE
   ```
3. Set `GOOGLE_PROJECT_ID` to the project ID. `GOOGLE_APPLICATION_CREDENTIALS` is only needed if
   the credentials file is not in gcloud's default location.

**Search Console**

1. In a Google Cloud project, enable the Search Console API and create an OAuth client of type
   Desktop app. Download its JSON file.
2. Set `GSC_OAUTH_CLIENT_SECRETS_FILE` to the path of that file. The first call opens a browser
   to sign in. For a service account instead, set `GSC_CREDENTIALS_PATH` and `GSC_SKIP_OAUTH=true`,
   and add the service account as a user on the property.

This server asks for the full `webmasters` scope, not read-only, because it can also add sites and
submit sitemaps. `.mcp.json` sets `GSC_ALLOW_DESTRUCTIVE=false`, which blocks its delete tools.
Bump the pinned version deliberately after reading its changelog, since it holds a Google token.

### Not included

Upstream also ships Slack, Canva, Figma, HubSpot, Amplitude, Notion, Ahrefs, Similarweb, Klaviyo,
Supermetrics, Gmail and Google Calendar. They were removed so installing the plugin does not add
servers that go unused; Ahrefs and Similarweb also need paid plans. To add one back, copy its
entry from upstream `marketing/.mcp.json`.

## page-audit evaluations

`skills/page-audit/evals/` holds five scenarios (`evals.json`) and four local HTML fixtures, so
no network is needed. `python3 skills/page-audit/evals/run_extractor_checks.py` runs the
extractor against the deterministic items. The behaviour items are written for a reviewer or an
LLM judge and have not been run against a model yet.
