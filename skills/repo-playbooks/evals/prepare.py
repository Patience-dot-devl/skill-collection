#!/usr/bin/env python3
"""Create a throw-away git repo for one repo-playbooks eval scenario.

  python3 evals/prepare.py <scenario-id> <empty-dir>

docs-repo scenarios copy fixtures/docs-repo, add scripts/check.py from the
setup-repo assets and commit it. The baseline is checked to pass check.py, so
any later error comes from the agent's change.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECK = HERE.parent / "skills/setup-repo/assets/scripts/check.py"


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


FAQ = """---
title: FAQ
status: live
updated: 2026-09-01
depends_on: [pricing.md]
---

# FAQ

## How much is a kilo of the house blend?

The house blend costs 12.50 per kilo, including VAT.

## Do you deliver?

We deliver in Utrecht, Nieuwegein and Houten.
"""


def make_lean(target):
    """Same repo, but the rules live only in the skills: no append-only note,
    no personal-data rule, no branch rule, no frontmatter guidance."""
    (target / "AGENTS.md").write_text(
        "# Harbour Coffee docs\n\nNotes for the shop. Run `python3 scripts/check.py` before a commit.\n")
    (target / "CONTRIBUTING.md").unlink()
    hist = target / "docs/pricing.history.md"
    hist.write_text(hist.read_text().replace("Append-only. Add new entries at the bottom.", "Log of price changes."))
    (target / "docs/faq.md").write_text(FAQ)


def main():
    scenario, target = sys.argv[1], Path(sys.argv[2])
    evals = {e["id"]: e for e in json.loads((HERE / "evals.json").read_text())["evals"]}
    if scenario not in evals:
        sys.exit(f"unknown scenario {scenario}; known: {', '.join(evals)}")
    if target.exists() and any(target.iterdir()):
        sys.exit(f"{target} is not empty")
    target.mkdir(parents=True, exist_ok=True)
    kind = evals[scenario].get("fixture", "docs-repo")
    git(target, "init", "-q", "-b", "main")
    git(target, "config", "user.email", "eval@example.test")
    git(target, "config", "user.name", "eval")
    if kind in ("docs-repo", "docs-repo-lean"):
        shutil.copytree(HERE / "fixtures/docs-repo", target, dirs_exist_ok=True)
        if kind == "docs-repo-lean":
            make_lean(target)
        (target / "scripts").mkdir()
        shutil.copy(CHECK, target / "scripts/check.py")
        git(target, "add", "-A")
        base = subprocess.run([sys.executable, "scripts/check.py"], cwd=target,
                              capture_output=True, text=True)
        if base.returncode != 0:
            sys.exit("fixture does not pass check.py:\n" + base.stdout)
    elif kind == "existing-readme":
        (target / "README.md").write_text("# Garden notes\n\nMy own notes about the allotment.\n")
        git(target, "add", "-A")
    else:  # empty
        pass
    if kind != "empty":
        git(target, "commit", "-q", "-m", "Baseline")
    if evals[scenario].get("start_branch"):
        git(target, "checkout", "-q", "-b", evals[scenario]["start_branch"])
    print(f"prepared {scenario} in {target}")


if __name__ == "__main__":
    main()
