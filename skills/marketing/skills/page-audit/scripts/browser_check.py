#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright==1.63.0"]
# ///
"""Open one URL in a headless browser and run the accessibility checks that source
code cannot settle.

Runs only when called: uv installs Playwright into a cached, throwaway environment
on first use, and nothing stays running afterwards.

Checks:
  axe       axe-core WCAG 2.x A/AA rules on the rendered page (contrast, names,
            target size, ...), with the page's Content Security Policy bypassed
            so the script can always be injected
  keyboard  presses Tab repeatedly and records where focus lands, whether the
            focused element is visible and has a focus style, skip link, traps
  reflow    re-renders at 320 px wide and reports horizontal overflow

Writes report.json plus screenshots to the output directory and prints a summary.

Usage:
  uv run scripts/browser_check.py https://example.com/page --out ./audit
  uv run scripts/browser_check.py --install-browser        # one-time Chromium download
"""

import argparse
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

AXE_VERSION = "4.14.0"
AXE_URL = f"https://cdn.jsdelivr.net/npm/axe-core@{AXE_VERSION}/axe.min.js"
AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
CACHE_DIR = Path.home() / ".cache" / "page-audit"

FOCUS_PROBE = """() => {
  const el = document.activeElement;
  if (!el || el === document.body || el === document.documentElement) return null;
  const r = el.getBoundingClientRect();
  const cs = getComputedStyle(el);
  const img = el.querySelector && el.querySelector('img[alt], svg[aria-label]');
  const name = (el.getAttribute('aria-label') || el.innerText || el.value || el.getAttribute('alt')
    || (img && (img.getAttribute('alt') || img.getAttribute('aria-label'))) || el.getAttribute('title') || '')
    .trim().replace(/\\s+/g, ' ').slice(0, 80);
  if (!el.dataset.paFocus) el.dataset.paFocus = String(++window.__paFocusCount || (window.__paFocusCount = 1));
  return {
    id: el.dataset.paFocus,
    tag: el.tagName.toLowerCase(),
    role: el.getAttribute('role') || '',
    name,
    href: el.getAttribute('href') || '',
    rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
    visible: r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.opacity !== '0',
    in_viewport: r.bottom > 0 && r.right > 0 && r.top < innerHeight && r.left < innerWidth,
    outline: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0
      ? `${cs.outlineWidth} ${cs.outlineStyle} ${cs.outlineColor}` : '',
    box_shadow: cs.boxShadow !== 'none' ? cs.boxShadow : '',
    path: (() => { const p = []; let n = el; while (n && n.nodeType === 1 && p.length < 4) {
      p.unshift(n.tagName.toLowerCase() + (n.id ? '#' + n.id : '')); n = n.parentElement; } return p.join(' > '); })(),
  };
}"""

UNFOCUSED_STYLE = """(path) => {
  // Blur and re-read styles so a focus style can be told apart from the default look.
  const el = document.activeElement; if (!el) return null;
  el.blur();
  const cs = getComputedStyle(el);
  const out = {outline: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0
      ? `${cs.outlineWidth} ${cs.outlineStyle} ${cs.outlineColor}` : '',
    box_shadow: cs.boxShadow !== 'none' ? cs.boxShadow : '',
    background: cs.backgroundColor, color: cs.color, text_decoration: cs.textDecorationLine};
  el.focus();
  const f = getComputedStyle(el);
  out.focused_background = f.backgroundColor; out.focused_color = f.color;
  out.focused_text_decoration = f.textDecorationLine;
  return out;
}"""

OVERFLOW_PROBE = """() => {
  const vw = document.documentElement.clientWidth;
  const wide = [];
  for (const el of document.body.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > vw + 1 && getComputedStyle(el).position !== 'fixed') {
      wide.push({el: el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
        (el.classList.length ? '.' + [...el.classList].slice(0, 2).join('.') : ''), right: Math.round(r.right)});
    }
    if (wide.length >= 8) break;
  }
  return {viewport: vw, scroll_width: document.documentElement.scrollWidth, overflowing: wide};
}"""


def axe_source():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = CACHE_DIR / f"axe-{AXE_VERSION}.min.js"
    if not cached.exists():
        with urllib.request.urlopen(AXE_URL, timeout=30) as response:
            cached.write_bytes(response.read())
    return cached.read_text(encoding="utf-8")


def goto(page, url):
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception:
        # Pages with long-polling or analytics beacons never go idle; "load" is enough.
        page.goto(url, wait_until="load", timeout=45000)
    page.wait_for_timeout(800)


def run_axe(page, source):
    page.add_script_tag(content=source)
    result = page.evaluate(
        """(tags) => axe.run(document, {runOnly: tags}).then(r => ({
          violations: r.violations.map(v => ({id: v.id, impact: v.impact, help: v.help,
            help_url: v.helpUrl, wcag: v.tags.filter(t => /^wcag\\d/.test(t)), count: v.nodes.length,
            nodes: v.nodes.slice(0, 5).map(n => ({target: n.target.join(' '),
              html: n.html.slice(0, 200), summary: n.failureSummary}))})),
          incomplete: r.incomplete.map(v => ({id: v.id, help: v.help, count: v.nodes.length})),
          passes: r.passes.length}))""",
        AXE_TAGS,
    )
    return result


def settle_scroll(page):
    # Smooth scrolling moves the focused element for a while after Tab; wait until it stops.
    previous = None
    for _ in range(15):
        page.wait_for_timeout(100)
        current = page.evaluate("() => [scrollX, scrollY]")
        if current == previous:
            return
        previous = current


def walk_keyboard(page, presses, out):
    stops = []
    screenshot = None
    for index in range(1, presses + 1):
        page.keyboard.press("Tab")
        settle_scroll(page)
        info = page.evaluate(FOCUS_PROBE)
        if info is None:
            stops.append({"press": index, "focus": "body"})
            continue
        info["press"] = index
        if not info["outline"] and not info["box_shadow"]:
            # No outline or shadow: check whether colour or underline changes on focus.
            styles = page.evaluate(UNFOCUSED_STYLE, info["path"]) or {}
            info["focus_changes"] = [
                key for key in ("background", "color", "text_decoration")
                if styles.get(key) != styles.get("focused_" + key)
            ]
        if screenshot is None and info["visible"] and info["in_viewport"] and info["tag"] in ("a", "button"):
            screenshot = out / "focus.png"
            page.screenshot(path=str(screenshot))
        stops.append(info)

    focused = [stop for stop in stops if "tag" in stop]
    ids = [stop["id"] for stop in focused]
    first = focused[0] if focused else None
    skip_words = ("skip", "inhoud", "content", "hoofdinhoud", "main")
    findings = {
        "skip_link_first": bool(first and first["href"].startswith("#")
                                and any(word in first["name"].lower() for word in skip_words)),
        "never_left_body": not focused,
        "possible_trap": any(ids[i] == ids[i + 1] == ids[i + 2] for i in range(len(ids) - 2)),
        "focus_left_page_at": next((stop["press"] for stop in stops if stop.get("focus") == "body"), None),
        "invisible_focus_stops": [s["press"] for s in focused if not s["visible"]],
        "offscreen_focus_stops": [s["press"] for s in focused if s["visible"] and not s["in_viewport"]],
        "no_focus_style": [s["press"] for s in focused
                           if not s["outline"] and not s["box_shadow"] and not s.get("focus_changes")],
    }
    return {"stops": stops, "findings": findings, "screenshot": str(screenshot) if screenshot else None}


def check(url, out, presses):
    from playwright.sync_api import sync_playwright

    out.mkdir(parents=True, exist_ok=True)
    source = axe_source()
    report = {"url": url, "axe_version": AXE_VERSION}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1366, "height": 900}, bypass_csp=True, locale="nl-NL")
        page = context.new_page()
        goto(page, url)
        report["final_url"] = page.url
        report["title"] = page.title()
        page.screenshot(path=str(out / "desktop.png"))
        report["axe"] = run_axe(page, source)
        report["keyboard"] = walk_keyboard(page, presses, out)

        page.set_viewport_size({"width": 320, "height": 800})
        page.wait_for_timeout(600)
        reflow = page.evaluate(OVERFLOW_PROBE)
        reflow["overflow_px"] = max(0, reflow["scroll_width"] - reflow["viewport"])
        reflow["horizontal_scroll"] = reflow["overflow_px"] > 0
        page.screenshot(path=str(out / "mobile-320.png"))
        report["reflow"] = reflow
        browser.close()

    report["screenshots"] = [str(out / name) for name in ("desktop.png", "mobile-320.png")]
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def summarise(report, out):
    axe = report["axe"]
    keyboard = report["keyboard"]["findings"]
    return {
        "url": report["final_url"],
        "axe_violations": [f'{v["id"]} ({v["impact"]}, {v["count"]}x)' for v in axe["violations"]],
        "axe_incomplete": [f'{v["id"]} ({v["count"]}x)' for v in axe["incomplete"]],
        "axe_passed_rules": axe["passes"],
        "keyboard": keyboard,
        "reflow_overflow_px": report["reflow"]["overflow_px"],
        "files": {"report": str(out / "report.json"), "screenshots": report["screenshots"],
                  "focus_screenshot": report["keyboard"]["screenshot"]},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url", nargs="?", help="page URL")
    parser.add_argument("--out", help="output directory (default: a new temp directory)")
    parser.add_argument("--tabs", type=int, default=20, help="number of Tab presses (default 20)")
    parser.add_argument("--install-browser", action="store_true", help="download Chromium for Playwright and exit")
    args = parser.parse_args()

    if args.install_browser:
        return subprocess.call([sys.executable, "-m", "playwright", "install", "chromium"])
    if not args.url or not args.url.startswith(("http://", "https://")):
        parser.error("a URL starting with http:// or https:// is required")

    out = Path(args.out) if args.out else Path(tempfile.mkdtemp(prefix="page-audit-browser-"))
    try:
        report = check(args.url, out, args.tabs)
    except Exception as error:
        message = str(error)
        hint = None
        if "Executable doesn't exist" in message or "playwright install" in message:
            hint = "Chromium is not installed. Run: uv run scripts/browser_check.py --install-browser"
        print(json.dumps({"error": message.splitlines()[0][:300], "hint": hint}, indent=2))
        return 2
    print(json.dumps(summarise(report, out), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
