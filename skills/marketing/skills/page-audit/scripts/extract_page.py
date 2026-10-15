#!/usr/bin/env python3
"""Fetch one URL and extract the on-page signals an SEO / GEO / WCAG audit needs.

Standard library only. Writes three files to the output directory and prints a
compact summary to stdout:

  page.html  raw source exactly as served (grep it for anything not extracted)
  page.txt   visible text in reading order
  page.json  every extracted signal (head tags, headings, links, images,
             structured data, form controls, robots rules)

Usage:
  extract_page.py https://example.com/page
  extract_page.py https://example.com/page --out ./audit
  extract_page.py https://example.com/page --html-file saved.html   # skip the fetch

This reads the served HTML only. It does not run JavaScript, so content that is
injected client-side will be missing; the summary flags pages where that looks
likely.
"""

import argparse
import json
import re
import sys
import tempfile
import urllib.error
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 page-audit-skill"
)

# Crawlers whose robots.txt access matters for search and AI-search visibility.
ROBOT_AGENTS = [
    "*",
    "Googlebot",
    "Bingbot",
    "Google-Extended",
    "GPTBot",
    "OAI-SearchBot",
    "ChatGPT-User",
    "ClaudeBot",
    "PerplexityBot",
]

SKIP_TAGS = {"script", "style", "noscript", "template", "svg"}
BLOCK_TAGS = {
    "p", "div", "section", "article", "main", "header", "footer", "nav", "aside",
    "h1", "h2", "h3", "h4", "h5", "h6", "li", "ul", "ol", "dl", "dt", "dd",
    "table", "tr", "td", "th", "br", "hr", "blockquote", "figure", "figcaption",
    "form", "details", "summary", "pre", "address",
}
COUNTED_TAGS = {
    "main", "nav", "header", "footer", "aside", "article", "section", "table",
    "ul", "ol", "dl", "details", "blockquote", "figure", "figcaption", "video",
    "audio", "form",
}
CONTROL_TYPES_WITHOUT_LABEL = {"hidden", "submit", "button", "reset", "image"}
GENERIC_ANCHORS = {
    "klik hier", "lees meer", "lees verder", "hier", "meer", "meer info",
    "meer informatie", "bekijk", "bekijk meer", "click here", "read more",
    "here", "more", "learn more", "more info", "link",
}


def clean(text):
    return re.sub(r"\s+", " ", text).strip()


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({"status": code, "from": req.full_url, "to": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, timeout=30):
    recorder = RedirectRecorder()
    opener = urllib.request.build_opener(recorder)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "nl,en;q=0.8",
        },
    )
    try:
        response = opener.open(request, timeout=timeout)
    except urllib.error.HTTPError as error:
        response = error
    body = response.read()
    return {
        "status": response.getcode(),
        "final_url": response.geturl(),
        "headers": {key.lower(): value for key, value in response.headers.items()},
        "redirects": recorder.chain,
        "body": body,
    }


def decode(body, content_type):
    match = re.search(r"charset=([\w-]+)", content_type or "", re.I)
    if not match:
        match = re.search(rb"<meta[^>]+charset=[\"']?([\w-]+)", body[:4096], re.I)
    charset = match.group(1) if match else "utf-8"
    if isinstance(charset, bytes):
        charset = charset.decode("ascii", "replace")
    try:
        return body.decode(charset, "replace")
    except LookupError:
        return body.decode("utf-8", "replace")


class PageParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.skip_depth = 0
        self.jsonld_buffer = None
        self.text = []
        self.html_lang = None
        self.title_parts = None
        self.titles = []
        self.meta = {}
        self.canonicals = []
        self.hreflang = []
        self.headings = []
        self.heading = None
        self.links = []
        self.link = None
        self.images = []
        self.jsonld_raw = []
        self.microdata_types = []
        self.rdfa_types = []
        self.controls = []
        self.label = None
        self.label_for = set()
        self.buttons = []
        self.button = None
        self.iframes = []
        self.time_values = []
        self.counts = {}
        self.script_count = 0

    @staticmethod
    def image_source(attrs):
        # Lazy loaders put a placeholder in src and the real file in a data attribute.
        for key in ("data-lazy-src", "data-src", "data-original"):
            if attrs.get(key):
                return attrs[key]
        return attrs.get("src", "")

    def separate(self):
        # Keeps "06 123<br>mail@x" from collapsing into one word in headings and anchors.
        self.text.append("\n")
        for target in (self.heading, self.link, self.button):
            if target is not None:
                target["parts"].append(" ")

    def handle_starttag(self, tag, attrs):
        attrs = {key: (value or "") for key, value in attrs}
        if tag == "script":
            self.script_count += 1
        if tag in SKIP_TAGS:
            if tag == "script" and "ld+json" in attrs.get("type", "").lower() and not self.skip_depth:
                self.jsonld_buffer = []
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in BLOCK_TAGS:
            self.separate()
        if tag in COUNTED_TAGS:
            self.counts[tag] = self.counts.get(tag, 0) + 1
        if "itemscope" in attrs and attrs.get("itemtype"):
            self.microdata_types.append(attrs["itemtype"])
        if attrs.get("typeof"):
            self.rdfa_types.append(attrs["typeof"])

        if tag == "html":
            self.html_lang = attrs.get("lang") or None
        elif tag == "title":
            self.title_parts = []
        elif tag == "meta":
            key = (attrs.get("name") or attrs.get("property") or attrs.get("http-equiv") or "").lower()
            if key:
                self.meta.setdefault(key, []).append(attrs.get("content", ""))
        elif tag == "link":
            rel = attrs.get("rel", "").lower().split()
            href = urljoin(self.base_url, attrs.get("href", ""))
            if "canonical" in rel:
                self.canonicals.append(href)
            elif "alternate" in rel and attrs.get("hreflang"):
                self.hreflang.append({"hreflang": attrs["hreflang"], "href": href})
        elif re.fullmatch(r"h[1-6]", tag):
            self.heading = {"level": int(tag[1]), "parts": []}
        elif tag == "a":
            self.link = {
                "href": attrs.get("href", ""),
                "rel": attrs.get("rel", ""),
                "aria_label": attrs.get("aria-label", ""),
                "title": attrs.get("title", ""),
                "parts": [],
                "image_alts": [],
            }
        elif tag == "img":
            image = {
                "src": urljoin(self.base_url, self.image_source(attrs)),
                "alt": attrs["alt"] if "alt" in attrs else None,
                "width": attrs.get("width", ""),
                "height": attrs.get("height", ""),
                "loading": attrs.get("loading", ""),
                "decorative_role": attrs.get("role") in ("presentation", "none")
                or attrs.get("aria-hidden") == "true",
                "inside_link": self.link is not None,
            }
            self.images.append(image)
            if self.link is not None and image["alt"]:
                self.link["image_alts"].append(image["alt"])
        elif tag in ("input", "select", "textarea"):
            control_type = attrs.get("type", "text").lower() if tag == "input" else tag
            if control_type in ("submit", "button", "reset"):
                self.buttons.append({"name": clean(attrs.get("value") or attrs.get("aria-label", ""))})
            elif control_type not in CONTROL_TYPES_WITHOUT_LABEL:
                self.controls.append({
                    "tag": tag,
                    "type": control_type,
                    "id": attrs.get("id", ""),
                    "name": attrs.get("name", ""),
                    "aria_label": attrs.get("aria-label", ""),
                    "aria_labelledby": attrs.get("aria-labelledby", ""),
                    "title": attrs.get("title", ""),
                    "placeholder": attrs.get("placeholder", ""),
                    "autocomplete": attrs.get("autocomplete", ""),
                    "required": "required" in attrs or attrs.get("aria-required") == "true",
                    "wrapped_in_label": self.label is not None,
                })
        elif tag == "label":
            self.label = True
            if attrs.get("for"):
                self.label_for.add(attrs["for"])
        elif tag == "button":
            self.button = {"aria_label": attrs.get("aria-label", ""), "parts": []}
        elif tag == "iframe":
            self.iframes.append({"src": attrs.get("src", ""), "title": attrs.get("title", "")})
        elif tag == "time":
            self.time_values.append(attrs.get("datetime", ""))

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            if tag == "script" and self.jsonld_buffer is not None:
                self.jsonld_raw.append("".join(self.jsonld_buffer))
                self.jsonld_buffer = None
            return
        if self.skip_depth:
            return
        if tag in BLOCK_TAGS:
            self.separate()
        if tag == "title" and self.title_parts is not None:
            self.titles.append(clean("".join(self.title_parts)))
            self.title_parts = None
        elif re.fullmatch(r"h[1-6]", tag) and self.heading:
            self.headings.append({"level": self.heading["level"], "text": clean("".join(self.heading["parts"]))})
            self.heading = None
        elif tag == "a" and self.link:
            link = self.link
            self.link = None
            text = clean("".join(link["parts"]))
            self.links.append({
                "href": link["href"],
                "text": text,
                "accessible_name": text or clean(link["aria_label"]) or clean(" ".join(link["image_alts"])) or clean(link["title"]),
                "rel": link["rel"],
            })
        elif tag == "label":
            self.label = None
        elif tag == "button" and self.button:
            self.buttons.append({"name": clean("".join(self.button["parts"])) or clean(self.button["aria_label"])})
            self.button = None

    def handle_data(self, data):
        if self.jsonld_buffer is not None:
            self.jsonld_buffer.append(data)
            return
        if self.skip_depth:
            return
        if self.title_parts is not None:
            self.title_parts.append(data)
            return
        self.text.append(data)
        for target in (self.heading, self.link, self.button):
            if target is not None:
                target["parts"].append(data)


def collect_types(node, found):
    if isinstance(node, dict):
        declared = node.get("@type")
        if isinstance(declared, str):
            found.append(declared)
        elif isinstance(declared, list):
            found.extend(str(item) for item in declared)
        for value in node.values():
            collect_types(value, found)
    elif isinstance(node, list):
        for item in node:
            collect_types(item, found)


def parse_jsonld(blocks):
    parsed = []
    for raw in blocks:
        entry = {}
        try:
            entry["data"] = json.loads(raw)
            types = []
            collect_types(entry["data"], types)
            entry["types"] = types
        except json.JSONDecodeError as error:
            entry["error"] = str(error)
            entry["raw"] = raw.strip()[:2000]
        parsed.append(entry)
    return parsed


def classify_links(links, page_url):
    page_host = urlparse(page_url).netloc.lower().removeprefix("www.")
    result = []
    for link in links:
        href = link["href"].strip()
        if not href or href.startswith("#"):
            kind = "fragment"
        elif re.match(r"(javascript|mailto|tel|sms|data):", href, re.I):
            kind = "other"
        else:
            absolute = urljoin(page_url, href)
            host = urlparse(absolute).netloc.lower().removeprefix("www.")
            kind = "internal" if host == page_host else "external"
            href = absolute
        result.append({**link, "href": href, "kind": kind, "nofollow": "nofollow" in link["rel"].lower()})
    return result


def check_robots(page_url):
    origin = "{0.scheme}://{0.netloc}".format(urlparse(page_url))
    robots_url = origin + "/robots.txt"
    try:
        response = fetch(robots_url, timeout=15)
    except Exception as error:  # network errors should not sink the audit
        return {"url": robots_url, "error": str(error)}
    if response["status"] != 200:
        return {"url": robots_url, "status": response["status"], "note": "no usable robots.txt; crawling is allowed by default"}
    text = decode(response["body"], response["headers"].get("content-type"))
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(text.splitlines())
    return {
        "url": robots_url,
        "status": 200,
        "allowed": {agent: parser.can_fetch(agent, page_url) for agent in ROBOT_AGENTS},
        "sitemaps": re.findall(r"(?im)^\s*sitemap:\s*(\S+)", text),
    }


def heading_jumps(headings):
    jumps = []
    previous = 0
    for heading in headings:
        if previous and heading["level"] > previous + 1:
            jumps.append("h{} follows h{}: {!r}".format(heading["level"], previous, heading["text"][:80]))
        previous = heading["level"]
    return jumps


def build(page_url, html, response):
    parser = PageParser(page_url)
    parser.feed(html)
    parser.close()

    text = re.sub(r"[ \t\r\f\v]+", " ", "".join(parser.text))
    text = re.sub(r"\s*\n\s*", "\n", text).strip()
    words = text.split()
    links = classify_links(parser.links, page_url)
    for control in parser.controls:
        control["labelled"] = bool(
            control["wrapped_in_label"]
            or (control["id"] and control["id"] in parser.label_for)
            or control["aria_label"]
            or control["aria_labelledby"]
            or control["title"]
        )

    title = parser.titles[0] if parser.titles else ""
    description = (parser.meta.get("description") or [""])[0]
    headers = response["headers"] if response else {}
    page = {
        "requested_url": page_url,
        "fetch": {
            "status": response["status"] if response else None,
            "final_url": response["final_url"] if response else page_url,
            "redirects": response["redirects"] if response else [],
            "content_type": headers.get("content-type"),
            "x_robots_tag": headers.get("x-robots-tag"),
            "last_modified": headers.get("last-modified"),
        },
        "head": {
            "title": title,
            "title_length": len(title),
            "title_count": len(parser.titles),
            "meta_description": description,
            "meta_description_length": len(description),
            "meta_robots": parser.meta.get("robots", []),
            "canonical": parser.canonicals,
            "html_lang": parser.html_lang,
            "hreflang": parser.hreflang,
            "viewport": parser.meta.get("viewport", []),
            "open_graph": {key: value for key, value in parser.meta.items() if key.startswith("og:")},
            "twitter": {key: value for key, value in parser.meta.items() if key.startswith("twitter:")},
            "other_meta": {
                key: value for key, value in parser.meta.items()
                if key in ("author", "article:published_time", "article:modified_time", "date", "last-modified", "keywords")
            },
        },
        "headings": parser.headings,
        "heading_level_jumps": heading_jumps(parser.headings),
        "question_headings": [heading["text"] for heading in parser.headings if heading["text"].endswith("?")],
        "content": {
            "word_count": len(words),
            "intro": " ".join(words[:120]),
            "element_counts": parser.counts,
            "time_elements": parser.time_values,
            "script_count": parser.script_count,
            # A short page is not a client-rendered one. Flag it only when scripts ship and
            # almost no text is served, or when a thin page carries many scripts.
            "likely_client_rendered": parser.script_count >= 1
            and (len(words) < 30 or (len(words) < 150 and parser.script_count >= 10)),
        },
        "links": links,
        "images": parser.images,
        "structured_data": {
            "json_ld": parse_jsonld(parser.jsonld_raw),
            "microdata_types": parser.microdata_types,
            "rdfa_types": parser.rdfa_types,
        },
        "forms": {"controls": parser.controls, "buttons": parser.buttons},
        "iframes": parser.iframes,
    }
    return page, text


def summarise(page):
    links = page["links"]
    images = page["images"]
    controls = page["forms"]["controls"]
    json_ld = page["structured_data"]["json_ld"]
    return {
        "fetch": page["fetch"],
        "title": "{} ({} chars)".format(page["head"]["title"], page["head"]["title_length"]),
        "meta_description": "{} ({} chars)".format(page["head"]["meta_description"], page["head"]["meta_description_length"]),
        "canonical": page["head"]["canonical"],
        "meta_robots": page["head"]["meta_robots"],
        "html_lang": page["head"]["html_lang"],
        "h1": [heading["text"] for heading in page["headings"] if heading["level"] == 1],
        "heading_count": len(page["headings"]),
        "heading_level_jumps": len(page["heading_level_jumps"]),
        "word_count": page["content"]["word_count"],
        "likely_client_rendered": page["content"]["likely_client_rendered"],
        "links": {
            "internal": sum(link["kind"] == "internal" for link in links),
            "external": sum(link["kind"] == "external" for link in links),
            "without_accessible_name": sum(not link["accessible_name"] for link in links),
            "generic_anchor_text": sum(link["text"].lower() in GENERIC_ANCHORS for link in links),
        },
        "images": {
            "total": len(images),
            "alt_missing": sum(image["alt"] is None for image in images),
            "alt_empty": sum(image["alt"] == "" for image in images),
        },
        "structured_data": {
            "json_ld_types": [kind for block in json_ld for kind in block.get("types", [])],
            "json_ld_parse_errors": sum("error" in block for block in json_ld),
            "microdata_types": page["structured_data"]["microdata_types"],
        },
        "forms": {
            "controls": len(controls),
            "controls_without_label": sum(not control["labelled"] for control in controls),
            "buttons_without_name": sum(not button["name"] for button in page["forms"]["buttons"]),
        },
        "iframes_without_title": sum(not frame["title"] for frame in page["iframes"]),
        "robots_txt": page.get("robots_txt"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url", help="page URL (also used to resolve relative links)")
    parser.add_argument("--out", help="output directory (default: a new temp directory)")
    parser.add_argument("--html-file", help="read HTML from this file instead of fetching the URL")
    parser.add_argument("--no-robots", action="store_true", help="skip the robots.txt check")
    args = parser.parse_args()

    if not re.match(r"https?://", args.url, re.I):
        parser.error("url must start with http:// or https://")

    response = None
    if args.html_file:
        html = Path(args.html_file).read_text(encoding="utf-8", errors="replace")
        page_url = args.url
    else:
        try:
            response = fetch(args.url)
        except Exception as error:
            print(json.dumps({"error": "fetch failed", "detail": str(error), "url": args.url}, indent=2))
            return 2
        content_type = response["headers"].get("content-type", "")
        if content_type and "html" not in content_type.lower():
            print(json.dumps({"error": "not an HTML page", "content_type": content_type, "status": response["status"]}, indent=2))
            return 2
        html = decode(response["body"], content_type)
        page_url = response["final_url"]

    page, text = build(page_url, html, response)
    page["requested_url"] = args.url
    if not args.no_robots:
        page["robots_txt"] = check_robots(page_url)

    out = Path(args.out) if args.out else Path(tempfile.mkdtemp(prefix="page-audit-"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "page.html").write_text(html, encoding="utf-8")
    (out / "page.txt").write_text(text, encoding="utf-8")
    (out / "page.json").write_text(json.dumps(page, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = summarise(page)
    summary["files"] = {name: str(out / name) for name in ("page.json", "page.txt", "page.html")}
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
