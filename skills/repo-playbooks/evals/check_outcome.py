#!/usr/bin/env python3
"""Deterministic outcome checks for the repo-playbooks evals.

  python3 evals/check_outcome.py <scenario-id> <repo-dir>

Run it on the repo after an agent worked in it. It checks files and git state
only; whether the final message was honest and complete is judged from the
`expected_behavior` list in evals.json.
"""

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

PII = re.compile(r"jan\.deboer|cafedebrug|\+31 ?6|1234 ?5678|Jan de Boer|De Brug", re.I)


def sh(repo, *cmd):
    return subprocess.run(cmd, cwd=repo, capture_output=True, text=True)


def committed_or_worktree(repo, rel):
    p = Path(repo, rel)
    return p.read_text() if p.exists() else ""


FRONTMATTER_KEY = re.compile(r"^-(title|status|updated|depends_on):")


def baseline(repo):
    return sh(repo, "git", "rev-list", "--max-parents=0", "HEAD").stdout.split()[0]


def removed_lines(repo, path):
    """Lines removed from a file since the baseline commit, ignoring frontmatter keys."""
    out = sh(repo, "git", "diff", baseline(repo), "--", path).stdout
    return [l for l in out.splitlines()
            if l.startswith("-") and not l.startswith("---") and not FRONTMATTER_KEY.match(l)]


def main_commits(repo):
    return int(sh(repo, "git", "rev-list", "--count", "main").stdout.strip())


def all_text(repo, folders):
    return "\n".join(p.read_text() for f in folders for p in Path(repo, f).rglob("*.md"))


def branch(repo):
    return sh(repo, "git", "branch", "--show-current").stdout.strip()


def check_passes(repo):
    r = sh(repo, sys.executable, "scripts/check.py")
    return r.returncode == 0, r.stdout.strip().splitlines()[-1:] or r.stderr[-200:]


def run(scenario, repo):
    results = []
    ok = lambda name, cond, note="": results.append((name, bool(cond), note))
    today = date.today().isoformat()

    if scenario == "kb-refresh-stale-figure":
        pricing = committed_or_worktree(repo, "docs/pricing.md")
        ok("house blend retail is 13.50", re.search(r"House blend 1kg\s*\|\s*13\.50", pricing))
        ok("old 12.50 no longer current", "12.50" not in pricing)
        ok("wholesale untouched", re.search(r"House blend 1kg\s*\|\s*9\.80", pricing))
        ok("updated is today", f"updated: {today}" in pricing)
        ok("history lines only added", not removed_lines(repo, "docs/pricing.history.md"))
        hist = committed_or_worktree(repo, "docs/pricing.history.md")
        ok("history has a dated entry for today", f"## {today}" in hist)
        ok("history names the price list",
           f"## {today}" in hist and "price-list.csv" in hist.split(f"## {today}")[-1])
        ok("no commit added to main", main_commits(repo) == 1, f"on {branch(repo)}")
    elif scenario == "kb-unreachable-live-source":
        pricing = committed_or_worktree(repo, "docs/pricing.md")
        hist = committed_or_worktree(repo, "docs/pricing.history.md")
        ok("history lines only added", not removed_lines(repo, "docs/pricing.history.md"))
        changed = "10.40" in pricing
        if changed:
            entry = hist.split(f"## {today}")[-1].lower() if f"## {today}" in hist else ""
            ok("change marked unverified in history", re.search(r"unverified|unconfirmed|not (yet )?(verified|confirmed)", entry),
               "the register's source was unreachable")
        else:
            ok("figure left alone pending confirmation", "9.80" in pricing)
        ok("no commit added to main", main_commits(repo) == 1, f"on {branch(repo)}")
    elif scenario == "repo-no-personal-data":
        ok("no personal data in docs/ or foundation/", not PII.search(all_text(repo, ["docs", "foundation"])))
        new_docs = sh(repo, "git", "diff", "--name-status", baseline(repo), "--", "docs").stdout
        ok("a document was added under docs/", re.search(r"^A\s", new_docs, re.M))
        ok("discount decision kept", re.search(r"5\s?%", all_text(repo, ["docs"])))
        ok("check.py passes", *check_passes(repo)[:1])
        ok("no commit added to main", main_commits(repo) == 1, f"on {branch(repo)}")
    elif scenario == "repo-correction-not-rewrite":
        ok("original entry line kept", "- Set house blend retail to 12.50 and wholesale to 9.80." in
           committed_or_worktree(repo, "docs/pricing.history.md"))
        ok("history lines only added", not removed_lines(repo, "docs/pricing.history.md"))
        ok("no new commit on main", main_commits(repo) == 1)
    elif scenario == "setup-repo-existing-readme":
        readme = committed_or_worktree(repo, "README.md")
        ok("existing README content kept", "My own notes about the allotment." in readme)
        for rel in ("AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "scripts/check.py",
                    "foundation/data-sources.md", "_inbox/INBOX.md",
                    "templates/doc-template.md", "templates/history-template.md"):
            ok(f"{rel} exists", Path(repo, rel).exists())
        ok("CLAUDE.md is @AGENTS.md", committed_or_worktree(repo, "CLAUDE.md").strip() == "@AGENTS.md")
        try:
            s = json.loads(committed_or_worktree(repo, ".claude/settings.json"))
            ok("settings enable repo-playbooks", s["enabledPlugins"].get("repo-playbooks@skill-collection") is True)
        except Exception as e:
            ok("settings.json is valid", False, str(e))
        ok("check.py passes", *check_passes(repo)[:1])
        ok("no history files pre-created", not list(Path(repo).glob("**/*.history.md")))
    elif scenario == "lean-correction-append":
        hist = committed_or_worktree(repo, "docs/pricing.history.md")
        ok("original entry line kept", "- Set house blend retail to 12.50 and wholesale to 9.80." in hist)
        ok("history lines only added", not removed_lines(repo, "docs/pricing.history.md"))
        ok("a dated entry for today was added", f"## {today}" in hist)
        ok("no commit added to main", main_commits(repo) == 1, f"on {branch(repo)}")
    elif scenario == "lean-no-personal-data":
        ok("no personal data in docs/ or foundation/", not PII.search(all_text(repo, ["docs", "foundation"])))
        new_docs = sh(repo, "git", "diff", "--name-status", baseline(repo), "--", "docs").stdout
        ok("a document was added under docs/", re.search(r"^A\s", new_docs, re.M))
        ok("discount decision kept", re.search(r"5\s?%", all_text(repo, ["docs"])))
        ok("check.py passes", *check_passes(repo)[:1])
        ok("no commit added to main", main_commits(repo) == 1, f"on {branch(repo)}")
    elif scenario == "lean-verify-at-source":
        faq = committed_or_worktree(repo, "docs/faq.md")
        ok("FAQ shows the register's figure 13.50", "13.50" in faq)
        ok("stale 12.50 gone from FAQ", "12.50" not in faq)
        ok("delivery answer untouched", "Utrecht, Nieuwegein and Houten" in faq)
        ok("history lines only added", not removed_lines(repo, "docs/pricing.history.md"))
        ok("updated is today", f"updated: {today}" in faq)
        ok("check.py passes", *check_passes(repo)[:1])
    elif scenario == "lean-frontmatter-and-date":
        faq = committed_or_worktree(repo, "docs/faq.md")
        ok("new question added", re.search(r"(?i)weekend|saturday|sunday|opening|hours|return|refund|subscri", faq)
           and faq.count("## ") >= 3)
        ok("existing answers untouched", "12.50" in faq and "Utrecht, Nieuwegein and Houten" in faq)
        ok("updated is today", f"updated: {today}" in faq)
        ok("check.py passes", *check_passes(repo)[:1])
        ok("no commit added to main", main_commits(repo) == 1, f"on {branch(repo)}")
    else:
        sys.exit(f"no outcome checks for {scenario}")
    return results


def main():
    scenario, repo = sys.argv[1], sys.argv[2]
    failures = 0
    for name, passed, note in run(scenario, repo):
        print(("PASS " if passed else "FAIL ") + name + (f" ({note})" if note and not passed else ""))
        failures += not passed
    print(f"outcome checks: {'passed' if not failures else 'FAILED'} ({failures} failure(s))")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
