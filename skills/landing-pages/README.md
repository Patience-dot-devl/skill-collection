# landing-pages

Fifteen skills for building and optimizing landing pages: web design and UX, conversion
optimization, Core Web Vitals (including CrUX field data) and CMS-specific workflows for Webflow,
Sanity and Contentful. Vendored from their sources; see
[SKILLS_EVALUATION.md](../../SKILLS_EVALUATION.md) for why each was chosen.

There is no single skill that covers "optimized landing pages on any CMS". These split by job:
design and UX first, then conversion and measurement, then the CMS layer.

## Skills

### Web design and UX

| Skill | Source | License | Needs |
|---|---|---|---|
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), commit `7246805`, path `.claude/skills/ui-ux-pro-max` | MIT | Python 3. Searches local CSV data (styles, palettes, fonts, UX rules, landing-page patterns) |

### Conversion and experimentation

| Skill | Source | License | Needs |
|---|---|---|---|
| `cro` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), commit `28e4a81` | MIT | Nothing. Reads `.agents/product-marketing.md` if present |
| `ab-testing` | same | MIT | same |
| `copywriting` | same | MIT | same |
| `content-experimentation-best-practices` | [sanity-io/agent-toolkit](https://github.com/sanity-io/agent-toolkit), commit `feb9d38` | MIT | Nothing |

### Performance and Core Web Vitals

| Skill | Source | License | Needs |
|---|---|---|---|
| `core-web-vitals` | [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills), commit `afa8da9` | MIT | Optional: Chrome DevTools MCP (CrUX in trace summaries), Search Console |
| `performance` | same | MIT | same |
| `web-quality-audit` | same | MIT | `jq` for `scripts/analyze.sh` |
| `seo-aeo-best-practices` | [sanity-io/agent-toolkit](https://github.com/sanity-io/agent-toolkit), commit `feb9d38` | MIT | Nothing |

The `marketing` plugin in this marketplace already bundles the Chrome DevTools, Google Analytics and
Search Console MCP servers that `core-web-vitals` and `performance` use for CrUX and lab data.

### CMS

| Skill | CMS | Source | License | Needs |
|---|---|---|---|---|
| `figma-to-webflow` | Webflow | [webflow/webflow-skills](https://github.com/webflow/webflow-skills), commit `c8a1650` | MIT | Webflow MCP, Figma MCP |
| `site-audit` | Webflow | same | MIT | Webflow MCP |
| `accessibility-audit` | Webflow | same | MIT | Webflow MCP |
| `asset-audit` | Webflow | same | MIT | Webflow MCP |
| `webflow-compress-cms-image` | Webflow | same | MIT | Webflow MCP |
| `contentful-nextjs` | Contentful | [contentful/skills](https://github.com/contentful/skills), commit `4524f53` | MIT | Next.js project |

`seo-aeo-best-practices` and `content-experimentation-best-practices` come from the Sanity toolkit
but are CMS-agnostic. They work on any stack.

## Changes from upstream

Files are unchanged except one edit:

- `ui-ux-pro-max/SKILL.md`: the 11 script paths `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/…`
  now read `${CLAUDE_PLUGIN_ROOT}/skills/ui-ux-pro-max/…`, because this plugin keeps skills under
  `skills/` and not `.claude/skills/`. The search script was run directly and works.

Each upstream licence text is in [`licenses/`](licenses/).

## Not included

| Skill | Why |
|---|---|
| [WordPress/agent-skills](https://github.com/WordPress/agent-skills) (`wp-performance`, `wp-block-themes`, `wp-patterns`, …) | GPL-2.0-or-later. Deliberately not vendored, so this repo carries no GPL obligations. Install from upstream, for example `npx skills add WordPress/agent-skills --skill wp-block-themes` (command from the upstream README). |
| [respira-press/agent-skills-wordpress](https://github.com/respira-press/agent-skills-wordpress) (`conversion-audit`, `page-template-library`, page-builder migrations) | MIT, but each skill calls `respira_*` MCP tools and requires the Respira for WordPress plugin. Useless without it. |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) `web-design-guidelines` | The repo README says MIT but has no `LICENSE` file, and the skill fetches its rules from an unpinned GitHub URL at run time. Install from upstream if you want it. |
| `contentful-personalization` | 30 files and 1.3 MB with a runnable script; install from [contentful/skills](https://github.com/contentful/skills) when needed. |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) other skills (`design`, `brand`, `slides`, …) | Out of scope for landing pages. |
| Squarespace, Wix, Framer, HubSpot CMS, Drupal, Storyblok | No first-party skills found. |

Shopify is covered by Shopify's own toolkit
([Shopify/Shopify-AI-Toolkit](https://github.com/Shopify/Shopify-AI-Toolkit), MIT), so it is not
copied here.

## Install

```bash
claude plugin marketplace add Patience-dot-devl/skill-collection
claude plugin install landing-pages@skill-collection
```
