# Marketing skills against a no-skill baseline (2026-10-18)

Raw evidence for the "Baseline test" section of
[docs/SKILLS_EVALUATION.md](../../docs/SKILLS_EVALUATION.md). Kept as produced, except that absolute
local paths were replaced with `<eval-root>` (this folder) and `<repo>` before filing.

## Method

- Five skills from the `marketing` plugin: `campaign-plan`, `competitive-brief`, `email-sequence`,
  `draft-content`, `brand-review`. Two realistic requests each, about fictional companies
  ([prompts.json](prompts.json)). `brand-review` uses a brand guide and two drafts with 22 planted
  violations ([inputs/](inputs/), answer key in [inputs/planted-issues.md](inputs/planted-issues.md)).
- Each request ran once with the skill and once without, as Claude Code subagents on Opus 5.5. The
  first request of each skill also ran on Haiku 5.5. 30 runs in total, one sample per run.
- "With" agents were told to read the skill's `SKILL.md` and follow it; "without" agents got the same
  request and rules and no skill ([agent_prompts.json](agent_prompts.json)). Neither could ask
  questions. Outputs are in [runs/](runs/), named by a random id.
- The arm behind each id is in [key.json](key.json). Pairs were put in random A/B order
  ([grades/order.json](grades/order.json)) and graded blind by an Opus subagent per skill on fit,
  specificity, soundness and usability, with a verdict and the size of the difference
  ([grader_template.md](grader_template.md), [grades/](grades/)).
- [unblind.py](unblind.py) maps verdicts back to arms; its output is [results.txt](results.txt).

## Limits

- 15 pairs, one sample each, one LLM grader. Treat differences as directional.
- Runs with the skill were about 70% longer (Opus mean 3,509 against 2,065 words; Haiku 2,586
  against 1,547). Graders tend to reward length.
- Agents read the skill file directly, so the test measures the skill body, not whether its
  description triggers.
- The session's hooks (a terse-output mode and the Superpowers bootstrap) were active in every
  subagent, in both arms.
