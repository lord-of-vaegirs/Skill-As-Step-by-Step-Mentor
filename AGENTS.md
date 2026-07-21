# Skill As Step by Step Mentor development context

## Project goal

Maintain a GitHub-ready Codex Skill Agent for source-grounded, hands-on engineering learning. Keep it as a real collaborative project with agent metadata, reusable references, deterministic scripts, tests, and CI rather than reducing it to a standalone `SKILL.md`.

## Origin and current state

- Created on 2026-07-21 from the original v2.1 command-addition specification.
- Preserve the source contract for `[help]` and `[command]` and the portable session commands documented in `references/commands.md`.
- The repository is initialized on branch `main`; the initial files are intentionally uncommitted so the user can own the first commit.
- The project uses the MIT license.

## Architecture

- `SKILL.md`: concise trigger description and core mentoring workflow.
- `agents/openai.yaml`: Codex UI metadata.
- `references/`: command contract, mentoring protocol, progress schema, and learning-quality rubric.
- `scripts/mentor_state.py`: dependency-free progress-file operations with path containment, atomic writes, validation, and explicit delete confirmation.
- `tests/`: CLI and skill-contract regression tests.
- `.github/`: CI, issue form, and pull-request template.

## Non-negotiable behavior

- Treat ordinary usage questions like `[help]` and command-syntax questions like `[command]`.
- Preserve progress history across restart and goto operations.
- Never mark learning complete without proportional evidence.
- Never claim command output, tests, source content, saves, or deletions that were not verified.
- Resolve file operations inside the authorized learning root and require explicit confirmation immediately before deletion.
- Keep `SKILL.md` compact; move detailed conditional guidance into directly linked files under `references/`.

## Validation

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/mentor_state.py
```

Also run Codex skill-creator's `quick_validate.py` when available. After the formal rename, official validation passed, all six repository tests passed, and the earlier independent forward tests still cover `[help]` plus a complete C/C++ fuzz-driver learning intake.

## Collaboration workflow

For behavior changes, start from a concrete learner request or failure mode, update the smallest relevant instruction or resource, add a regression test, and run all validation. Do not commit generated learner progress, credentials, copyrighted learning materials, or local cache files.
