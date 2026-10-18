You are a senior marketing lead grading a blind A/B comparison. For each pair below, two assistants answered the same request. You do not know how they differ; judge only the deliverables.

Read the files with the Read tool. Do not read any other files in the repository.

For each pair:
1. Read the request and both deliverables (A and B) in full.
2. Score each 1-10 on:
   - fit: answers the request and uses every fact given; assumptions are reasonable and stated
   - specificity: concrete, actionable, tailored to this business rather than generic template content
   - soundness: numbers add up (budget, funnel, timing); no invented facts presented as real; no claims a legal or brand reviewer would block
   - usability: a professional could ship or act on it with little editing; length fits the job
3. Give a verdict: A, B or tie. Use "tie" when a professional would not care which one they got.
4. Give the size of the difference: none, small or large.
5. In 2-4 sentences, name the concrete differences that drove the verdict (for example a missing section, a wrong calculation, generic filler, a better structure).
EXTRA

Write the result as JSON to OUTFILE with this shape, then reply with only the word DONE:
{"pairs": [{"pair": "<pair name>", "scores": {"A": {"fit": n, "specificity": n, "soundness": n, "usability": n}, "B": {...}}, "verdict": "A|B|tie", "difference": "none|small|large", "reasons": "..."}]}

PAIRS
