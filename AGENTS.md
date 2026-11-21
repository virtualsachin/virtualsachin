# AGENTS.md — `virtualsachin/virtualsachin`

## Repository Role

This repository hosts the public GitHub profile `README.md` for `https://github.com/virtualsachin`.
It serves as the public GitHub entrypoint into Sachin Kumar Sharma's Executive Capability Portfolio, Architectural Research Hub, and Open Engineering Lab.

## Brand Consistency Invariants

Content in `README.md` is kept in sync with `https://virtualsach.in` via `skills/brand-ops`:

- **Canonical Titles:** Keep Sachin's exact executive titles intact:
  - `Agentic Infrastructure Architect`
  - `Director — Cloud & Infrastructure Architecture`
  - `Principal Agentic AI Architect`
- **Core Positioning:** Preserve the core signature line (`Complexity is the Enemy. Always.`), the 20-year first-principles timeline, and the Executive Capability Portfolio / Open Engineering Lab posture (no job-hunting signals or commercial consulting solicitation).
- **Canonical Links & Badges:** Every link and badge URL in `README.md` must use `https://` or `mailto:sachin@virtualsach.in` (no `http://` or broken relative links), and must include `https://virtualsach.in`, `https://virtualsach.in/llms.txt`, and `https://virtualsach.in/blog/`.
- **Public Exposure Hygiene:** `README.md` and repository files must never contain secrets, API/PAT tokens, private keys, RFC 1918 / CGNAT internal IPs, or internal infrastructure hostnames.

## Verification

Run the repository verification gate before committing or opening a pull request:

```bash
./bin/verify
```

`./bin/verify` supports `--fast`, `--no-precommit`, and `--changed` (exiting `64` on unknown flags), and executes:

1. `python3 -m unittest discover -s tests -v` (`tests/test_profile_readme.py`)
2. `gitleaks dir "$ROOT" --no-banner` (when `gitleaks` is installed)
