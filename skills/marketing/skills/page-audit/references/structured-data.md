# Structured data mode

Mode 4: check the existing structured data and write the best-fitting JSON-LD.

## Analyse what is there

`structured_data.json_ld` holds every JSON-LD block, parsed, with the `@type`
values found in it. A block with an `error` key failed to parse; that is a finding
of its own, since search engines discard invalid JSON. `microdata_types` and
`rdfa_types` show markup in the other two syntaxes.

Judge the existing markup on correctness, completeness, relevance and technical
quality. Look at:

- Schema type: does it match what the page is (an article, a product, a service,
  a local business, an FAQ, an event)
- Required and recommended properties for that type
- Consistency with the visible content: every value in the markup should be
  findable on the page
- Duplicate or conflicting markup, which is common when a theme and a plugin both
  emit a block (two `Organization` nodes with different names, two `WebPage` nodes)
- Opportunities for richer markup

Output a table with: current structured data, what is right, what is missing or
wrong, advice.

## Write the JSON-LD

Then write the best-fitting structured data for the page as valid JSON-LD.

Only include properties that are logical and defensible from the page. This is
the rule that matters most here. Markup that claims a rating, review count, price,
author, date or opening hours that the page does not show is a violation of
Google's structured data guidelines and can lead to a manual action, so it does
harm beyond being useless. Where a recommended property has no value on the page,
leave it out of the code and list it afterwards as something for the owner to
supply.

Practical points:

- Use `https://schema.org` as `@context`.
- Prefer one `@graph` with nodes linked through `@id` over several loose blocks.
  If the page already has a graph (Yoast and Rank Math emit one), extend it and
  reuse its `@id` values instead of adding a parallel block.
- Use absolute URLs and ISO 8601 dates.
- Pick the most specific type that is true (`Dentist` over `LocalBusiness`).
- Know which types still earn a rich result. Google restricted FAQ rich results
  to well-known government and health sites and retired HowTo rich results in
  2023. `FAQPage` markup can still help machines read a page, so it may be worth
  adding, as long as the user is not promised an FAQ snippet in Google. Eligibility
  changes over time; if the advice hinges on it, check Google's current search
  gallery documentation.

After the code, explain briefly why this schema type and these properties were
chosen.

## Validate before handing over

Check that the JSON parses, since one trailing comma makes the whole block
worthless:

```bash
python3 -m json.tool < block.json
```

Then tell the user to confirm with Google's Rich Results Test (eligibility for
rich results) and the Schema Markup Validator at validator.schema.org (vocabulary
correctness). Parsing proves the syntax; those tools prove the rest.
