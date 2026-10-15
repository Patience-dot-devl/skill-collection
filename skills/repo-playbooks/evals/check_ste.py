#!/usr/bin/env python3
"""Mechanical Simplified Technical English checks for explain-plane output.

  python3 evals/check_ste.py <answer.md>

Checks what a script can: sentence length (25 words, 20 for numbered steps),
contractions, paragraph length (6 sentences) and a list of words the skill
names as replaced. Passive voice and noun clusters need a reader.
"""

import re
import sys

BANNED = ["utilize", "utilise", "initiate", "facilitate", "demonstrate", "leverage", "subsequently"]
CONTRACTION = re.compile(r"\b\w+(?:n't|'re|'ll|'ve|'s|'d)\b")


def prose_lines(text):
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code and not line.startswith("#") and line.strip():
            yield line


def main():
    text = open(sys.argv[1]).read()
    problems = []
    for line in prose_lines(text):
        step = bool(re.match(r"\s*\d+[.)]\s", line))
        body = re.sub(r"^\s*(?:\d+[.)]|[-*])\s+", "", line)
        body = re.sub(r"`[^`]*`", "CODE", body)
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]
        if len(sentences) > 6:
            problems.append(f"paragraph with {len(sentences)} sentences: {body[:50]}...")
        for s in sentences:
            n = len(s.split())
            limit = 20 if step else 25
            if n > limit:
                problems.append(f"{n} words (max {limit}): {s[:70]}...")
    for m in CONTRACTION.finditer(re.sub(r"`[^`]*`|```.*?```", "", text, flags=re.S)):
        if not m.group(0).endswith("'s"):  # possessives are allowed
            problems.append(f"contraction: {m.group(0)}")
    for w in BANNED:
        if re.search(rf"\b{w}", text, re.I):
            problems.append(f"complex word: {w}")
    for p in problems:
        print("FAIL", p)
    print(f"ste checks: {'passed' if not problems else 'FAILED'} ({len(problems)} problem(s))")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
