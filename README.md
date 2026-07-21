# Skill As Step by Step Mentor

A Codex skill-agent project for source-grounded, hands-on engineering learning. It turns a broad learning goal into an adaptive route, verifies practical evidence one checkpoint at a time, and persists recoverable Markdown progress.

## Included

- `SKILL.md` — concise agent workflow and routing instructions
- `agents/openai.yaml` — Codex UI metadata and default prompt
- `references/` — portable command contract, mentoring protocol, state schema, and quality rubric
- `scripts/mentor_state.py` — dependency-free, safety-scoped progress-file CLI
- `tests/` — behavior and contract regression tests
- `.github/` — pull-request template, issue forms, and CI

## Install

Clone this repository into your Codex skills directory:

```bash
git clone <repository-url> "${CODEX_HOME:-$HOME/.codex}/skills/skill-as-step-by-step-mentor"
```

Restart or reload Codex, then invoke:

```text
$skill-as-step-by-step-mentor
```

For local development, keep the repository anywhere and symlink it into the skills directory.

## Validate

Run the repository tests:

```bash
python3 -m unittest discover -s tests -v
```

If the Codex `skill-creator` utilities are installed, also run:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

## Contribute

Open an issue with a concrete learning scenario, then add or update a regression test with the behavior change. Keep `SKILL.md` compact and place detailed protocols in `references/`. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
