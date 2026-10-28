# Skill As Step by Step Mentor development context

## Project goal

Maintain a GitHub-ready Skill Agent for source-grounded, hands-on engineering learning that installs unchanged in Codex and in DeepSeek Harness. Keep it as a real collaborative project with agent metadata, reusable references, deterministic scripts, tests, and CI rather than reducing it to a standalone `SKILL.md`.

## Origin and current state

- Created on 2026-07-21 from the original v2.1 command-addition specification.
- Preserve the source contract for `[help]` and `[command]` and the portable session commands documented in `references/commands.md`.
- The repository is initialized on branch `main`; the initial files are intentionally uncommitted so the user can own the first commit.
- The project uses the MIT license.

## Architecture

- `SKILL.md`: concise trigger description and core mentoring workflow.
- `agents/openai.yaml`: Codex UI metadata; never a carrier of required behavior.
- `references/`: command contract, mentoring protocol, progress schema, learning-quality rubric, and host integration notes.
- `references/harness-integration.md`: discovered skill roots, frontmatter constraints, invocation forms, and the installation checklist shared by both hosts.
- `scripts/mentor_state.py`: dependency-free progress-file operations with path containment, atomic writes, validation, and explicit delete confirmation.
- `package.json`, `cordis.patch.yml`, `lib/index.js`: DeepSeek Harness bundle; the repository root is the package, and `lib/index.js` registers one skills provider without registry dependencies.
- `locale/`, `icon.svg`: bundle display metadata for the plugin list.
- `tests/`: CLI, skill-contract, host-compatibility, bundle-manifest, and Node provider regression tests.
- `.github/`: CI, issue form, and pull-request template.

## Non-negotiable behavior

- Treat ordinary usage questions like `[help]` and command-syntax questions like `[command]`.
- Preserve progress history across restart and goto operations.
- Never mark learning complete without proportional evidence.
- Never claim command output, tests, source content, saves, or deletions that were not verified.
- Resolve file operations inside the authorized learning root and require explicit confirmation immediately before deletion.
- Keep `SKILL.md` compact; move detailed conditional guidance into directly linked files under `references/`.
- Resolve `references/` and `scripts/` paths against the skill's reported base directory, never the process working directory.
- Keep the frontmatter to `name` and `description`, keep the name equal to the bundle directory, and keep the single-line description within the 500-character host catalog budget.
- Write progress only inside the learner's work directory, never inside the skill bundle.
- Keep the bundle dependency-free: `lib/index.js` imports `node:` builtins only, because a profile install runs pnpm against the registry.
- Keep one skill bundle: the package root is the skill root, so never commit a second copy of `SKILL.md`.

## Validation

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/mentor_state.py
node --test tests/provider.test.mjs
npm pack --dry-run --json
```

Also run Codex skill-creator's `quick_validate.py` when available. The frontmatter must parse with a strict YAML parser, because DeepSeek Harness drops a skill whose frontmatter is invalid without showing the model a diagnostic.

## Collaboration workflow

For behavior changes, start from a concrete learner request or failure mode, update the smallest relevant instruction or resource, add a regression test, and run all validation. Do not commit generated learner progress, credentials, copyrighted learning materials, or local cache files.
