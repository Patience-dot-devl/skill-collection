# Harbour Coffee docs

Rules for anyone, human or agent, working in this repo.

- Registered live sources of truth are listed in `foundation/data-sources.md`. Verify figures there, not in other documents.
- History is append-only. Corrections are new dated entries in the matching `*.history.md`.
- Dates are YYYY-MM-DD. Links are relative.
- No customer names, emails or phone numbers in `docs/` or `foundation/`.
- Run `python3 scripts/check.py` before every commit. Zero errors.
- Never commit to `main`. Commit format: `Scope: summary`.

Details are in [CONTRIBUTING.md](CONTRIBUTING.md).
