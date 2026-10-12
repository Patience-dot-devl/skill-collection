# Content modes

Modes 1, 8, 9, 14 and 15. These produce text the user will publish or hand to a
writer, so write in the language of the page and match its tone and form of
address (in Dutch: je or u, as the page uses).

The counts below (25 questions, 10 title tags and so on) are the defaults from the
source prompt pack. Follow the user's number if they give one.

## Contents

- Mode 1: real search questions and reader questions
- Mode 8: title tag, meta description, H1 and intro
- Mode 9: FAQ based on the page
- Mode 14: information density, scannability and writing style
- Mode 15: content refresh brief

## Mode 1: real search questions and reader questions

Question research based on one page.

From the page, its headings, content, search intent and likely information need,
work out which questions readers or searchers really have. Give 25 concrete
questions in a table:

1. Question
2. Why this question is alive
3. Search intent or need behind it
4. Stage in the customer journey: orientation / comparison / decision
5. Promising for SEO / GEO / FAQ / social / newsletter
6. Already answered on the page: yes / partly / no

Conditions:

- Avoid generic questions that would fit any page on the topic
- Mix basic questions, doubts, buying questions and in-depth questions
- Use plain language, the way people ask
- Base the list on the URL and on what is still missing from the page

Column 6 matters most to the user: it separates questions the page should start
answering from ones it already covers. Check each against `page.txt`.

If ~~SEO or web search is available, check "People also ask" and related searches for
the page's main query and mark which questions come from there. Otherwise the list
is reasoned from the page, which is fine, as long as the output does not present
the questions as measured search demand.

## Mode 8: title tag, meta description, H1 and intro

Quick on-page improvements for click-through and clarity.

Assess the current state of `head.title`, `head.meta_description`, the H1 and the
first paragraph (`content.intro`). Then give:

1. A short diagnosis per component
2. 10 new title tags
3. 10 new meta descriptions
4. 5 better H1 variants
5. 3 new intros

Conditions:

- Write concretely
- Avoid generic SEO language ("de beste", "alles wat je moet weten", "ontdek")
- Take search intent into account
- Make the variants useful for search engine and person alike

Show the character count after each title and meta description, and keep titles
to roughly 60 characters and descriptions to roughly 155 so they display in full.
Make the variants differ in angle (benefit, question, number, audience, outcome),
because ten rewordings of one idea give the user nothing to choose between. Only
promise what the page delivers.

## Mode 9: FAQ based on the page

Pulls FAQ and "People also ask" opportunities from one URL.

Build an FAQ section that helps SEO, GEO and usability. Give:

1. 15 relevant questions
2. A compact answer per question
3. Why this question follows from the page or the searcher
4. Whether the question fits better in the body text, in an FAQ, or in a separate article

Write the answers clearly and factually, without repetition. Each answer should
stand on its own: lead with the answer, name the subject, keep it to two or three
sentences. That is what makes it usable for both a reader and an answer engine.

Answer only from what the page supports. Where a good question cannot be answered
from the page, keep the question and mark the answer as something the owner needs
to supply, since an invented price, term or guarantee would end up published.

Close with advice on the best placement of the FAQ on the page. If the user wants
FAQPage markup, see `structured-data.md`.

## Mode 14: information density, scannability and writing style

Writing analysis for SEO, GEO and ease of use.

Assess `page.txt` on:

- Superfluous introduction
- Woolliness
- Concrete wording
- Rhythm and paragraph structure
- Subheadings
- Use of examples
- Repetition
- Answer speed: how quickly the reader gets what they came for

Output a table with score, diagnosis and concrete improvement per component, and
quote an example from the page for each diagnosis. Then give 10 rewrite guidelines
that make this page stronger for readers and answer engines. Tie each guideline to
this page; "write shorter sentences" is true of every page and helps nobody.

## Mode 15: content refresh brief

Turns analysis into an assignment for a writer or content specialist.

Include:

1. Goal of the page
2. Likely primary search intent
3. What must be kept
4. What should be cut, merged or rewritten
5. Which new sections are missing
6. Which questions must be answered
7. Which SEO, GEO and UX improvements are needed
8. The desired new structure of the page, as a heading outline

Keep it compact, concrete and executable. The reader is a writer who has not seen
the analysis, so name sections by their current heading and say what to do with
each. Mark facts the writer has to obtain from the business (prices, figures,
names), so they are not left to be made up.
