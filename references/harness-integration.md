# Harness integration

## Contents

- [Portable rules](#portable-rules)
- [Codex](#codex)
- [DeepSeek Harness](#deepseek-harness)
- [Host checklist](#host-checklist)

## Portable rules

- Treat `SKILL.md` and `references/` as the only behavioral contract. Host metadata files such as `agents/openai.yaml` describe the skill in one host's UI and must never carry required behavior.
- Resolve `references/…` and `scripts/…` against the skill's base directory, which each host reports when the skill loads. Do not assume the process working directory is the skill directory.
- Keep learner progress inside the learner's work directory. The skill directory is read-only input; writing progress there makes one learner's state leak into every other session.
- Keep the bracketed commands (`[help]`, `[finish]`, `[summarize]`, …) as the only state-transition signal. A host's own invocation gesture loads the skill; it never advances a gate.
- Accept both entry paths: an explicit user invocation of the skill, and a model-side load triggered by a matching request. After either one, follow [../SKILL.md](../SKILL.md) routing and intake rules.

## Codex

- Install as a directory bundle under the Codex skills root: `${CODEX_HOME:-$HOME/.codex}/skills/skill-as-step-by-step-mentor`.
- Invoke with the `$skill-as-step-by-step-mentor` prompt; `agents/openai.yaml` supplies the display name, short description, and default prompt.
- Run `python3 <skill-creator>/scripts/quick_validate.py .` when that utility is available.

## DeepSeek Harness

The Harness discovers local skills through its filesystem skill provider, so no plugin build step is required. A skill is a directory bundle `<root>/<name>/SKILL.md` (or a flat `<root>/<name>.md`) directly under a scanned root.

Scanned roots, highest priority first:

| Priority | Root |
|---|---|
| 1 | `<project root>/.dsh/skills` |
| 2 | `<project root>/.agents/skills` |
| 3 | configured custom skill directories |
| 4 | `$DSH_HOME/skills` (default `~/.dsh/skills`) |
| 5 | `$DSH_AGENTS_HOME/skills` (default `~/.agents/skills`) |

The project root is the nearest ancestor containing `.git`, so a repository-local `.dsh/skills` makes the skill available to every session started in that repository only. A user-level root makes it available to every session.

- Install for the current user by symlinking the repository (or a copy of it) into `$DSH_HOME/skills`:

  ```bash
  mkdir -p "${DSH_HOME:-$HOME/.dsh}/skills"
  ln -s "/absolute/path/to/skill-as-step-by-step-mentor" \
    "${DSH_HOME:-$HOME/.dsh}/skills/skill-as-step-by-step-mentor"
  ```

- Invoke with `/skill-as-step-by-step-mentor` in the composer, or let the model load it through the `skill` tool when the request matches the description.
- Discovery is watched, so a new, renamed, edited, or deleted skill reaches the next catalog without restarting the Harness. Frontmatter edits and `SKILL.md` content reload live; edits under `references/` are read at use time.
- Frontmatter constraints: `name` must be kebab-case and match `^[a-z0-9]+(-[a-z0-9]+)*$`, `description` is required, and the catalog truncates a description longer than 500 characters. Optional keys: `whenToUse`, `metadata`, `disable-model-invocation`, `user-invocable`.
- `user-invocable: false` hides the skill from `/name`; `disable-model-invocation: true` hides it from the model catalog and keeps `/name` as its only entry point. This skill keeps both surfaces enabled.

Distribution option: this repository is also a bundle package, so the same checkout installs as a managed plugin. The bundle layout is:

| File | Role |
|---|---|
| `package.json` | Package identity plus `dsh.bundle.patch`; `files` ships the skill bundle and `lib/index.js` |
| `cordis.patch.yml` | Inserts the `skill-step-mentor` row, whose `name` resolves to the package itself |
| `lib/index.js` | `ctx.skills.registerProvider` with a candidate at the bundled rank; imports only Node built-ins |
| `locale/*.json`, `icon.svg` | Display metadata for the plugin list |

Install it through the Harness plugin manager with the GitHub URL or the checkout's absolute path; the manager runs pnpm, selects the bundle in the profile, and applies the patch. Choose this packaging when the skill must be versioned, enabled, or disabled per profile. Keep one route active at a time: a local skill root outranks the bundled provider and would shadow it.

The provider re-reads `SKILL.md` on every catalog request, so a reinstalled copy changes the advertised description and the loaded body without touching the provider. `npm pack --dry-run` is the check that the installed copy still carries `SKILL.md`, `references/`, and `scripts/`.

## Host checklist

Before reporting the skill as installed:

1. Load it once through the host's own path (`/name` or the `skill` tool) and confirm the returned body is the current `SKILL.md`.
2. Confirm the reported base directory contains `references/`, `scripts/`, and `agents/`.
3. Run `python3 "<skill base>/scripts/mentor_state.py" --help` and confirm it prints the subcommands.
4. Confirm `python3 "<skill base>/scripts/mentor_state.py" --root "<work directory>" list` reports only that work directory.
