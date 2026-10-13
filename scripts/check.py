#!/usr/bin/env python3
"""Check this repository's conventions before a commit.

Checks every tracked Markdown file (or every Markdown file, outside git) for:

  links        relative links and #anchors that do not resolve, and absolute
               links into this repository that should be relative
  frontmatter  required keys present; `updated` and other date keys in YYYY-MM-DD;
               `depends_on` entries that point at files that exist
  dates        dates in file names in YYYY-MM-DD form
  secrets      likely credentials in any tracked text file

Exits 1 when anything fails, so it can gate a commit:

  python3 scripts/check.py           # whole repository (VENDORED_PATHS skip all but secrets)
  python3 scripts/check.py docs/     # one folder

Adjust the settings below to match the repository's CONTRIBUTING.md.
"""

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

# --- settings -----------------------------------------------------------------

# Folders whose Markdown files must carry frontmatter with these keys.
FRONTMATTER_REQUIRED = {
    "foundation": ["title", "status", "updated", "depends_on"],
    "docs": ["title", "status", "updated", "depends_on"],
}
# Required keys that may be present but empty (e.g. `depends_on: []`).
ALLOW_EMPTY = {"depends_on"}
# Frontmatter keys that hold dates.
DATE_KEYS = ["updated", "created", "date"]
# Folders that are skipped entirely (raw material is checked when it is curated).
SKIP_DIRS = {"_inbox", "sources", "node_modules", ".git"}
# Repository URL prefixes that should be written as relative links instead.
OWN_URL_PREFIXES = []  # e.g. ["https://github.com/your-org/your-repo/blob/main/"]

# Vendored upstream files stay exactly as received, so the links, frontmatter and file-name
# checks skip them. The secrets check still runs on them. Add a prefix when vendoring a new source.
VENDORED_PATHS = [
    "skills/vendored/",
    "skills/dev-tools/skills/",
    "skills/landing-pages/skills/",
    "skills/repo-playbooks/skills/setup-repo/assets/",  # templates link to a layout they are copied into
]

SECRET_PATTERNS = {
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----",
    "AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
    "GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{36,}\b",
    "Slack token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b",
    "Google API key": r"\bAIza[0-9A-Za-z_-]{35}\b",
    "Stripe key": r"\b[rs]k_live_[0-9A-Za-z]{20,}\b",
    "OpenAI or Anthropic key": r"\bsk-(?:ant-)?[A-Za-z0-9_-]{32,}\b",
    "assigned secret": r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"][^'\"\s]{12,}['\"]",
}

# ------------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)|!\[[^\]]*\]\(\s*<?([^)\s>]+)>?")
DATE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")
DATE_LIKE_NAME = re.compile(r"(?<!\d)(\d{4})[-_.]?(\d{1,2})[-_.]?(\d{1,2})(?!\d)")
FENCE = re.compile(r"^(```|~~~)")
SPACED_LINK = re.compile(r"\]\(([^)<>\"]*\s[^)<>\"]*)\)")


def tracked_files(scope):
    try:
        output = subprocess.run(
            ["git", "ls-files", "-z", "--", str(scope)], cwd=ROOT, capture_output=True, check=True
        ).stdout.decode()
        files = [ROOT / name for name in output.split("\0") if name]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = [path for path in scope.rglob("*") if path.is_file()]
    return [path for path in files if not SKIP_DIRS.intersection(path.relative_to(ROOT).parts)]


def is_vendored(path):
    relative = path.relative_to(ROOT).as_posix()
    return any(relative.startswith(prefix) for prefix in VENDORED_PATHS)


def strip_code(text):
    lines, inside = [], False
    for line in text.splitlines():
        if FENCE.match(line.strip()):
            inside = not inside
            lines.append("")
            continue
        lines.append("" if inside else re.sub(r"`[^`]*`", "", line))
    return lines


def slug(heading):
    heading = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return re.sub(r" ", "-", heading)


def anchors(path, cache={}):
    if path not in cache:
        found = set()
        counts = {}
        for line in strip_code(path.read_text(encoding="utf-8", errors="replace")):
            match = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
            if match:
                base = slug(match.group(1))
                count = counts.get(base, 0)
                counts[base] = count + 1
                found.add(base if count == 0 else f"{base}-{count}")
            for explicit in re.findall(r'<a\s+(?:name|id)="([^"]+)"', line):
                found.add(explicit)
        cache[path] = found
    return cache[path]


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    data, key = {}, None
    for line in text[4:end].splitlines():
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(item.group(1).strip().strip("'\""))
            continue
        pair = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if pair:
            key, value = pair.group(1), pair.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                data[key] = [part.strip().strip("'\"") for part in value[1:-1].split(",") if part.strip()]
            else:
                data[key] = value.strip("'\"") if value else []
    return data


def check_links(path, lines, errors):
    for number, line in enumerate(lines, 1):
        for match in SPACED_LINK.finditer(line):
            target = match.group(1).strip()
            if not re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                errors.append(f"{path.relative_to(ROOT)}:{number}: space in link target, encode it as %20: {target}")
        for match in LINK.finditer(line):
            target = match.group(1) or match.group(2)
            where = f"{path.relative_to(ROOT)}:{number}"
            if any(target.startswith(prefix) for prefix in OWN_URL_PREFIXES):
                errors.append(f"{where}: absolute link into this repository, make it relative: {target}")
                continue
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            file_part, _, anchor = target.partition("#")
            if " " in file_part:
                errors.append(f"{where}: space in link target, encode it as %20: {target}")
                continue
            resolved = path if not file_part else (path.parent / unquote(file_part)).resolve()
            if not resolved.exists():
                errors.append(f"{where}: link target does not exist: {target}")
            elif anchor and resolved.suffix == ".md" and anchor not in anchors(resolved):
                errors.append(f"{where}: no heading for anchor #{anchor} in {resolved.relative_to(ROOT)}")


def check_frontmatter(path, text, errors):
    relative = path.relative_to(ROOT)
    required = FRONTMATTER_REQUIRED.get(relative.parts[0], []) if len(relative.parts) > 1 else []
    if path.name == "README.md":
        required = []  # folder indexes do not need document frontmatter
    data = frontmatter(text)
    if data is None:
        if required:
            errors.append(f"{relative}: missing frontmatter (needs {', '.join(required)})")
        return
    for key in required:
        if key not in data:
            errors.append(f"{relative}: frontmatter key '{key}' is missing")
        elif data[key] in ("", []) and key not in ALLOW_EMPTY:
            errors.append(f"{relative}: frontmatter key '{key}' is empty")
    for key in DATE_KEYS:
        value = data.get(key)
        if isinstance(value, str) and value and value != "YYYY-MM-DD" and not DATE.match(value):
            errors.append(f"{relative}: frontmatter '{key}: {value}' is not YYYY-MM-DD")
    depends = data.get("depends_on", [])
    for dependency in [depends] if isinstance(depends, str) and depends else depends or []:
        if not re.match(r"^[a-z]+:", dependency) and not (path.parent / unquote(dependency)).exists():
            errors.append(f"{relative}: depends_on target does not exist: {dependency}")


def check_name_date(path, errors):
    match = DATE_LIKE_NAME.search(path.stem)
    if not match:
        return
    year, month, day = match.groups()
    if not (1990 <= int(year) <= 2100 and 1 <= int(month) <= 12 and 1 <= int(day) <= 31):
        return
    if not DATE.match(match.group(0)):
        errors.append(f"{path.relative_to(ROOT)}: date in file name is not YYYY-MM-DD: {match.group(0)}")


def check_secrets(path, errors):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return
    for number, line in enumerate(text.splitlines(), 1):
        if "check.py: allow-secret" in line:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if re.search(pattern, line):
                errors.append(f"{path.relative_to(ROOT)}:{number}: possible {label}")


def main():
    scope = (ROOT / sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    files = tracked_files(scope)
    errors = []
    markdown = [path for path in files if path.suffix == ".md"]
    for path in markdown:
        if is_vendored(path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        check_links(path, strip_code(text), errors)
        check_frontmatter(path, text, errors)
    for path in files:
        if not is_vendored(path):
            check_name_date(path, errors)
        if path.name != "check.py":
            check_secrets(path, errors)

    for error in errors:
        print(error)
    print(f"\n{len(markdown)} Markdown files, {len(files)} files checked: "
          f"{'0 errors' if not errors else f'{len(errors)} error(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
