# SEO modes

Modes 2, 3, 12 and 16. All start from the extractor output described in `SKILL.md`.

## Contents

- Mode 2: SEO quickscan
- Mode 3: search intent, task intent and content fit
- Mode 12: internal link opportunities and anchor texts
- Mode 16: competition and SERP opportunities

## Mode 2: SEO quickscan

A fast diagnosis of content, technique and on-page SEO for one page.

Assess each of these from the evidence:

| Component | Where to look |
|---|---|
| Title tag | `head.title`, `title_length`, `title_count` |
| Meta description | `head.meta_description`, length |
| URL structure | `fetch.final_url`, `fetch.redirects` |
| H1, H2 and heading structure | `headings`, `heading_level_jumps` |
| Search-intent fit | `page.txt` against the query the page evidently targets |
| Internal links on the page | `links` with `kind: internal`, anchor texts |
| Scannability | headings, lists, tables, paragraph length in `page.txt` |
| Depth of content | `content.word_count`, what `page.txt` actually covers |
| Indexation and canonical signals | `head.meta_robots`, `fetch.x_robots_tag`, `head.canonical`, `robots_txt`, `head.hreflang` |
| Structured data | `structured_data` |

If ~~browser is connected, run `performance_start_trace` for Core Web Vitals and
the insights behind them (render-blocking resources, LCP element, layout shifts),
and `lighthouse_audit` for its SEO category. Without it, leave speed to gocrawl's
headless crawl or mark it as not assessed.

Useful checks that are easy to miss: a canonical pointing somewhere other than the
final URL, a `noindex` in either the meta tag or the `X-Robots-Tag` header, more
than one title or H1, a redirect chain longer than one hop, a title that will be
truncated (roughly over 60 characters) or a description outside roughly 120-160
characters. Lengths are guidelines for display, not ranking rules; say so rather
than presenting them as hard limits.

Output a table with: component, score 1-10, what works, what is wrong or weak,
concrete improvement. Close with the 7 most important improvements in order of
impact.

## Mode 3: search intent, task intent and content fit

Checks whether the page matches what the searcher wants.

Work out:

1. The likely primary intent
2. Possible secondary intents
3. What the visitor probably wants to do, know or compare
4. How well the current page serves that
5. Which parts are missing to serve it better

Derive the intent from the title, H1, headings and body, and name the query or
queries you assume the page targets, since the whole assessment depends on that
assumption. If ~~SEO or web search is available, look at what currently ranks for that
query: the result types that dominate (guides, product pages, comparisons, tools)
are the best evidence of what searchers want. Without a search tool, say the
intent is inferred from the page alone.

Put the result in a table with a 1-10 score for intent fit. Then give 5 concrete
changes to structure, headings and content that would tighten the fit.

## Mode 12: internal link opportunities and anchor texts

Helps the page land better in the internal site structure.

One page shows its outgoing links, not its incoming ones. Use `links` for what the
page links to and with which anchors. For the rest of the site, look at the
navigation and footer links in `links`, and fetch the sitemap listed under
`robots_txt.sitemaps` if there is one, so suggestions name pages that exist.
Incoming links cannot be observed from here; recommend page types for them and say
a crawler or Search Console is needed to see the real ones.

Give:

1. Which types of pages should ideally link to this URL
2. Which types of pages this URL should link to
3. 15 anchor-text suggestions
4. Risks of anchors that are too vague or too exact-match

Flag existing anchors that say nothing ("lees meer", "klik hier"); the summary
counts them under `links.generic_anchor_text`. Put the result in a table with
priority high / medium / low. Reason from findability, UX and topical coherence.

## Mode 16: competition and SERP opportunities

Sharpens the view of opportunities and risks in the search results.

This mode is only as good as its evidence. If ~~SEO is connected, pull the ranking
pages and their keyword overlap from it. Otherwise, if web search is available, search
the page's primary query (and one or two close variants), open the top results,
and base the analysis on what is there. If no search tool is available, do the
analysis as an estimate from topic, intent and page type, and label it as an
estimate at the top of the output, because the user will otherwise read guesses
about competitors as observations.

Work out:

1. Which type of competitor dominates
2. Which content formats they use
3. Where this page falls short on content
4. Where the opportunities to win are
5. Which differentiation makes sense

Close with a list of 10 concrete changes that would make the page more
competitive.
