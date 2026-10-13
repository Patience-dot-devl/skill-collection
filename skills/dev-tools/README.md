# dev-tools

Three development skills that fill gaps in Claude Code's built-in set. Vendored unchanged from
their sources; see [SKILLS_EVALUATION.md](../../SKILLS_EVALUATION.md) for why each was chosen.

| Skill | Source | License | Needs |
|---|---|---|---|
| `pict-test-designer` (`skills/pypict/`) | [omkamal/pypict-claude-skill](https://github.com/omkamal/pypict-claude-skill), commit `fbda212` | MIT (`LICENSE`) | `pict` CLI or the `pypict` Python package |
| `ffuf-web-fuzzing` (`skills/ffuf/`) | [jthack/ffuf_claude_skill](https://github.com/jthack/ffuf_claude_skill), commit `50fd4af` | MIT per upstream README; no license file upstream, see [`NOTICE.md`](skills/ffuf/NOTICE.md) | `ffuf` binary. Only for targets you are authorised to test |
| `webapp-testing` (`skills/webapp-testing/`) | [anthropics/skills](https://github.com/anthropics/skills), commit `9d2f1ae` | Apache-2.0 (`LICENSE.txt`) | Python Playwright |

Superpowers is not included: install it from the official marketplace
(`superpowers@claude-plugins-official`), which carries a newer version than the copy in
`skills/vendored/`.

## Install

```bash
claude plugin marketplace add Patience-dot-devl/skill-collection
claude plugin install dev-tools@skill-collection
```
