# Accessibility modes

Modes 5 and 17.

## Contents

- What can and cannot be judged from source
- Browser pass
- Mode 5: WCAG check
- Mode 17: images, alt texts and multimodal findability

## What can and cannot be judged from source

The extractor reads served HTML. That settles some WCAG questions reliably and
leaves others open. Being exact about this is the main quality bar for this mode:
an accessibility report that marks contrast or keyboard access as "goed" without
having tested it gives the owner false assurance about real barriers.

Reliable from source:

- Page title (2.4.2) and page language (3.1.1): `head.title`, `head.html_lang`
- Heading hierarchy (1.3.1, 2.4.6): `headings`, `heading_level_jumps`
- Images without an alt attribute (1.1.1): `images` where `alt` is null
- Links and buttons without an accessible name (2.4.4, 4.1.2): `links` where
  `accessible_name` is empty, `forms.buttons` where `name` is empty
- Form controls without a label (1.3.1, 3.3.2, 4.1.2): `forms.controls` where
  `labelled` is false
- Missing `autocomplete` on personal-data fields (1.3.5)
- Iframes without a title (4.1.2): `iframes`
- Landmarks (1.3.1): `content.element_counts` for main, nav, header, footer
- Zoom blocked in the viewport meta (1.4.4): `user-scalable=no` or `maximum-scale=1`

Needs judgement, possible from source:

- Whether an alt text describes the image well
- Whether link text makes sense out of context
- Readability and plain language (3.1.5 is AAA, but worth reporting)

Not reliable without a rendered page or interaction:

- Colour contrast (1.4.3, 1.4.11)
- Keyboard access and focus order (2.1.1, 2.4.3), visible focus (2.4.7), focus
  not obscured (2.4.11)
- Target size (2.5.8), reflow at 320px (1.4.10), text spacing (1.4.12)
- Error messages and status messages (3.3.1, 4.1.3)
- Anything a script adds after load, such as menus, modals and cookie banners

Run the browser pass below for this last group. If neither route can run, list
these as "niet te beoordelen" and name the tool that would settle each one (axe DevTools, WAVE, a keyboard walkthrough, a screen reader).

A page that passes every source check is not thereby WCAG-conformant, and an
automated check never is a conformance claim. Say that in the report.

## Browser pass

There are two routes. Use ~~browser (Chrome DevTools) when it is connected; it
is the better tool for most audits. Use the bundled script when no browser is
connected, or when the user wants a repeatable result to compare over time.
Either way, automated checks catch roughly a third to a half of WCAG issues;
screen-reader behaviour and the meaning of content stay "niet te beoordelen".

### With ~~browser (Chrome DevTools)

1. `list_pages` for the `pageId`, then `navigate_page` to the URL.
2. `lighthouse_audit` with `mode: navigation`, once with `device: desktop` and,
   for mobile issues, once with `device: mobile`. Its accessibility category runs
   a subset of the axe-core rules; read the failed audits from the report it
   writes. For the full axe rule set, run the script below as well. Its SEO category
   doubles as a check on mode 2.
3. Keyboard: `press_key` Tab about 15 times, with `take_snapshot` every few
   presses to see where focus is. Check skip link, order, nothing invisible, no
   trap. On a focused link, `get_css_styles` shows whether a focus style exists,
   and `take_screenshot` shows whether it is visible enough.
4. Reflow: `resize_page` to 320 by 800 and `take_screenshot`; content should fit
   without horizontal scrolling.
5. A cookie banner or overlay in the first screenshot is a finding of its own:
   check whether it can be closed by keyboard.

### Without a browser: the bundled script

The script starts a headless Chromium only while it runs and leaves nothing
running. It needs `uv`; the first run installs Playwright into uv's cache.

```bash
uv run scripts/browser_check.py "<URL>" --out <working-dir>/browser
```

If it reports that Chromium is missing, run
`uv run scripts/browser_check.py --install-browser` once (about 100 MB) and retry.

It prints a summary and writes `report.json` and screenshots:

- **axe**: axe-core WCAG 2.x A/AA results on the rendered page, with the page's
  Content Security Policy bypassed so axe always loads. `axe_violations` are
  failures (contrast, accessible names, target size and so on); `axe_incomplete`
  are items axe could not decide, which stay "twijfel" until checked by hand.
  `report.json` holds the failing elements per rule.
- **keyboard**: 20 Tab presses. `skip_link_first`, `possible_trap` (focus stuck
  on one element), `invisible_focus_stops` and `offscreen_focus_stops` (focus on
  something the user cannot see), `no_focus_style` (no outline, shadow, colour or
  underline change on focus) and `focus_left_page_at` (where focus ran out of
  page elements; fine at the end of the page, a problem if early).
  `focus.png` shows one focused link or button; look at it to judge whether the
  focus indicator is clear enough.
- **reflow**: the page at 320 px wide. `reflow_overflow_px` above a few pixels
  means horizontal scrolling (1.4.10); `mobile-320.png` shows the result.

Look at `desktop.png` as well: a cookie banner or overlay covering the content is
a finding of its own.

## Mode 5: WCAG check

Accessibility analysis against WCAG 2.2 levels A and AA.

Assess at least:

- Page title and structure
- Heading hierarchy
- Link texts
- Alt texts
- Forms and labels, where present
- Contrast signals, where derivable
- Keyboard logic, where visible
- Error and status messages, where visible
- Language settings
- Readability and comprehensibility

Output a table with:

1. WCAG component or success criterion, with its number
2. Status: goed / twijfel / fout / niet te beoordelen (pass / doubt / fail / not assessable when answering in English)
3. Finding, with the element it concerns
4. Risk for the user: who is affected and how
5. Concrete solution, as corrected markup where that helps

Then give a priority list split into quick wins, medium changes and larger
technical issues. End with an explicit list of what could not be judged reliably
without live interaction or tooling.

## Mode 17: images, alt texts and multimodal findability

Makes visual content better for accessibility and search.

Go through `images`. For each image that matters, look at:

- Presence and quality of the alt text
- Informational value of the image
- Supporting role for understanding and conversion
- Opportunities for captions, file names or surrounding context
- Risk of decorative or meaningless visuals

Three alt states mean different things. No alt attribute is a failure: a screen
reader falls back to the file name. An empty `alt=""` is correct for a decorative
image and wrong for one that carries information. A filled alt is only good if it
says what the image contributes; file names, "afbeelding van" and keyword lists
do not.

To judge an alt text you need to know what the image shows. Use the file name,
the caption and the surrounding text in `page.html`, and view the image itself if
a tool allows it (`take_screenshot` of the element with ~~browser, the script's
screenshots, or opening the image URL). If neither is possible, say the suggested alt is based on
context and needs a visual check.

Output a table with: component, finding, risk, improvement suggestion. Then write
example alt texts and short caption suggestions for the images that need them,
keyed to the image file name so the user can find each one.

Do not suggest alt text for images that are correctly marked decorative, and do
not stuff keywords into alt texts; describe the image for someone who cannot see
it, and the search value follows.
