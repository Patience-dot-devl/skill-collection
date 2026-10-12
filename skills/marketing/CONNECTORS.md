# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~marketing automation` might mean HubSpot, Marketo, or any other marketing platform with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (design, SEO, email marketing, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

This fork's `.mcp.json` includes four free servers: gocrawl, Chrome DevTools, Google Analytics and Search Console. Chrome DevTools only launches Chrome on its first call. When no browser is connected, `page-audit` falls back to a bundled Playwright script that runs only during the audit. For other categories, connect a server yourself; the skills fall back to working without one. Setup steps are in the README under MCP Integrations.

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | — | Slack, Microsoft Teams |
| Design | `~~design` | — | Canva, Figma, Adobe Creative Cloud |
| Marketing automation | `~~marketing automation` | — | HubSpot, Marketo, Pardot, Mailchimp |
| Product analytics | `~~product analytics` | Google Analytics | Amplitude, Mixpanel |
| Knowledge base | `~~knowledge base` | — | Notion, Confluence, Guru |
| SEO | `~~SEO` | Search Console | Ahrefs, Similarweb, Semrush, Moz |
| Site crawler | `~~site crawler` | gocrawl | Screaming Frog, Sitebulb |
| Browser | `~~browser` | Chrome DevTools | Claude in Chrome, Playwright |
| Email marketing | `~~email marketing` | — | Klaviyo, Mailchimp, Brevo, Customer.io |
| Marketing analytics | `~~marketing analytics` | Google Analytics | Supermetrics, Mailchimp, Semrush |
