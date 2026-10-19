---
title: Skills evaluation history
status: live
updated: 2026-10-18
depends_on:
  - SKILLS_EVALUATION.md
---

# Skills evaluation history

Append-only. Add new entries at the bottom. To correct an earlier entry, add a new dated entry that
names the one it corrects; never edit or delete old entries.

## 2026-10-13

- Added the "Landing-pages plugin" section: 15 skills from six upstream repos.
  Source: [`foundation/data-sources.md`](../foundation/data-sources.md).
- Recorded that WordPress/agent-skills (GPL-2.0-or-later) is deliberately not vendored.
- Moved the document from the repository root to `docs/` and added frontmatter, to follow the
  repo-playbooks layout. Content is unchanged by the move.

## 2026-10-14

- Re-vendored upstream skills that had moved past their pins; all other upstreams were already at
  their pinned head. Source: [`foundation/data-sources.md`](../foundation/data-sources.md).
  - Superpowers: `d884ae0` to `bb92a77` (v7.0.0). Rebuilt `brainstorming`, `executing-plans`,
    `subagent-driven-development`, `finishing-a-development-branch` and `writing-plans`; added
    `diagnosing-superpowers`. The copy now has 15 skills. The "13 skills" count in the 2026-10-13
    sections is superseded.
  - `ab-testing`: `28e4a81` to `c7d7dfb`. Duration checklist now accounts for exposure and allocation.
    `cro` and `copywriting` have no upstream changes in that range; their pin moved to `c7d7dfb`.
  - `contentful-nextjs`: `4524f53` to `9100f17`. Version bump only.
  - `webapp-testing`: 17 upstream commits, none touching the skill; pin stays `9d2f1ae`.
- The skill-by-skill verdicts for Superpowers were written against `d884ae0` and have not been
  re-read against v7.0.0 line by line. Re-check `writing-plans` and `executing-plans` before relying on them.

## 2026-10-18

- Added "Baseline test: marketing skills against no skill". Five `marketing` skills, 15 blind pairs
  on Opus 5.5 and Haiku 5.5: 9 wins with the skill, 5 without, 1 tie; 14 of 15 differences small.
  Source: [`sources/skill-baselines-2026-10-18/`](../sources/skill-baselines-2026-10-18/README.md).
- Added "Triage: keep, slim, drop" as a recommendation. Nothing was removed or rewritten yet.
