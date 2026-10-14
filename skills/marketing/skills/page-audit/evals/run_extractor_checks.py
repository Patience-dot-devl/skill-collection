#!/usr/bin/env python3
"""Check the extractor against the 'deterministic' items in evals.json.

Usage: python3 evals/run_extractor_checks.py
Standard library only. Exit code 1 when any check fails. The behaviour items in
evals.json need a reviewer or an LLM judge and are not run here.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXTRACTOR = HERE.parent / "scripts" / "extract_page.py"


def observed(page, summary):
    images = summary["images"]
    return {
        "title": page["head"]["title"],
        "title_chars": len(page["head"]["title"]),
        "meta_description_chars": len(page["head"]["meta_description"]),
        "meta_robots": page["head"]["meta_robots"],
        "html_lang": page["head"]["html_lang"],
        "h1_count": summary["h1"].__len__(),
        "word_count": summary["word_count"],
        "images_alt_missing": images["alt_missing"],
        "images_alt_empty": images["alt_empty"],
        "generic_anchor_text": summary["links"]["generic_anchor_text"],
        "controls_without_label": summary["forms"]["controls_without_label"],
        "likely_client_rendered": summary["likely_client_rendered"],
    }


def main():
    spec = json.loads((HERE / "evals.json").read_text())
    failures = 0
    for case in spec["evals"]:
        expected = case["deterministic"]
        if not expected:
            continue
        with tempfile.TemporaryDirectory() as out:
            name = Path(case["fixture"]).stem
            result = subprocess.run(
                [sys.executable, str(EXTRACTOR), f"https://example.test/{name}",
                 "--html-file", str(HERE / case["fixture"]), "--out", out, "--no-robots"],
                capture_output=True, text=True,
            )
            if result.returncode:
                print(f"FAIL {case['id']}: extractor exited {result.returncode}\n{result.stderr}")
                failures += 1
                continue
            summary = json.loads(result.stdout)
            page = json.loads((Path(out) / "page.json").read_text())
        got = observed(page, summary)
        for key, want in expected.items():
            if key == "title":
                have = got["title"]
            else:
                have = got[key]
            if have != want:
                print(f"FAIL {case['id']}: {key} expected {want!r}, got {have!r}")
                failures += 1
    print("extractor checks:", "FAILED" if failures else "passed", f"({failures} failure(s))")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
