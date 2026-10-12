# GEO and AI-search modes

Modes 6, 7, 10, 11 and 13. GEO (Generative Engine Optimization) is about whether
answer engines and LLMs can find, understand, trust and quote a page.

Two things hold for all of these modes. First, whether a page is actually cited by
ChatGPT, Perplexity or AI Overviews cannot be observed from the page; these modes
assess how usable the page is as a source, which is the part the owner controls.
Second, quote passages from `page.txt` word for word when judging them. A passage
is citable or it is not, and the user needs to see which one you mean.

## Contents

- Mode 6: GEO overall score
- Mode 7: citability and answer readiness
- Mode 10: entities, semantic coverage and topical gaps
- Mode 11: featured snippets, AI Overviews and zero-click
- Mode 13: E-E-A-T, trust and credibility

## Mode 6: GEO overall score

Assess how usable the content is for AI search, LLM answers and answer engines.

| Component | What to look for |
|---|---|
| Direct answer power | Is the main question answered early, in a sentence that stands on its own |
| Clarity of definitions and summaries | Explicit definitions, a summary or key takeaways |
| Question-and-answer structure | `question_headings`, FAQ blocks, headings that mirror real questions |
| Citability | Self-contained sentences with a named subject, not "this" or "it" |
| Entities and context | Named people, organisations, products, places, with enough context to disambiguate |
| Evidence and source value | Figures, dates, sources, own data, cases |
| Freshness signals | Visible dates, `content.time_elements`, `dateModified` in JSON-LD, `fetch.last_modified` |
| Scannability for machines and people | Heading hierarchy, lists, tables, short paragraphs |
| Structured data | `structured_data` |
| Unique angle | Something this page says that the average page on the topic does not |

Also check `robots_txt.allowed` for the AI crawlers. A page that blocks GPTBot,
ClaudeBot or PerplexityBot limits its own AI-search visibility whatever the
content quality, so report it up front.

Output a table with a 1-10 score, explanation and improvement per component.
Close with:

1. The GEO overall score
2. Why that score follows from the findings
3. The 10 strongest opportunities for visibility in AI search

## Mode 7: citability and answer readiness

Checks whether the page can be quoted or summarised quickly.

Look at:

- Does the main answer come early enough on the page
- Are definitions, conclusions and key sentences explicit enough
- Does the page contain concrete facts, examples and scope
- Are claims supported
- Are there passages that can be quoted literally or nearly literally

A good test for a passage: lifted out of the page and shown alone, does it still
make sense and say something specific? Sentences that lean on the previous
paragraph, open with a pronoun, or hedge without committing fail that test.

Give:

1. A score for answer readiness
2. A list of passages that are already strong, quoted
3. A list of weak or woolly passages, quoted
4. 10 concrete rewrite suggestions, each as before and after

## Mode 10: entities, semantic coverage and topical gaps

Checks whether the page is broad and sharp enough on its topic.

Extract the main entities, subtopics and semantic signals from `page.txt` and the
headings. Then assess:

1. Which core entities are present
2. Which relevant entities or subtopics are missing
3. Where the semantic coverage is thin
4. Whether the page is probably too narrow, too broad or about right

"Missing" is a judgement against what a thorough treatment of the topic would
cover. Say what that judgement is based on: your knowledge of the topic, or, if a
search tool is available, what the top-ranking pages cover.

Output a table with: entity or topic, present / missing / weak, why relevant,
suggested addition. Close with a top 10 of topical gaps.

## Mode 11: featured snippets, AI Overviews and zero-click

Finds SERP opportunities in the existing page.

Look for content that fits an extractable format:

- Definitions
- Step-by-step plans
- Lists
- Comparisons
- Short answers to explicit questions
- Tables or summaries

Use `content.element_counts` (ol, ul, table, details) and `question_headings` to
see what is already structured, and `page.txt` for content that holds the right
information in the wrong shape, such as a process described in a paragraph that
should be a numbered list.

Give:

1. A list of current snippet opportunities
2. Which format fits best for each: paragraph / list / table / FAQ
3. Which rewrite is needed
4. 5 example blocks, written out, ready to place on the page

## Mode 13: E-E-A-T, trust and credibility

Strengthens trust signals for SEO and AI search.

| Component | What to look for |
|---|---|
| Author signals | Byline, author page link, `head.other_meta.author`, `author` in JSON-LD, credentials |
| Evidence, cases, data, examples | First-hand experience, own figures, named clients or cases |
| Transparency | Who is behind the site, contact details, about page, legal pages in footer links |
| Freshness | Published and updated dates, visible and in markup |
| Source references | External links to primary sources (`links` with `kind: external`) |
| Business or editorial credibility | Reviews, certifications, memberships, editorial policy |

Give a 1-10 score, explanation and improvement suggestion per component. Close
with the 8 most important changes to strengthen trust and evidence.

Only what is on this page (and what its links point to) is visible. Reputation
elsewhere, such as reviews on third-party sites or mentions in the press, is out
of view; say so if it matters for the conclusion.
