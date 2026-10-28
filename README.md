# Skill As Step by Step Mentor

<p align="right">
  <strong>English</strong> | <a href="./README.zh-CN.md">简体中文</a>
</p>

A Codex skill and DeepSeek Harness plugin for source-grounded, hands-on engineering learning. It turns a broad learning goal into an adaptive route, verifies practical evidence one part at a time, and persists recoverable Markdown progress.

After the learner confirms a topic, reference materials, work directory, and final goal, the agent derives an ordered route and teaches exactly one part at a time. Every part is strictly gated: explanation only, `[finish]`, practice and review, then `[summarize]`. Later-part content remains hidden until preceding parts are summarized, and `[summarize all]` unlocks the final synthesis only after the last part. New technical terms are defined before first use, explanations build from source-grounded background step by step, and recoverable progress records the active gate. Restart keeps Q&A while clearing reset theory, practice, evidence, and completion state so the affected parts are learned again.

## Why did I create this skill?
In today's world, learning across various fields—especially computer science—often presents a challenge: while resources abound, truly absorbing the material is difficult. After much reflection, I realized the root cause is the lack of an immersive learning experience. We often have resources at our fingertips but don't know where to start or how to structure a study plan, leading us to quickly forget what we’ve learned. To address these persistent issues, I decided to harness the power of AI. It acts as a dedicated, 24/7 personal tutor—always at your beck and call—to handle planning and practice scheduling. It addresses your specific questions and ideas, providing tailored exercises and examples that help you master the material with confidence. For added convenience, I’ve included special commands; simply type `[command]` into the chat box to learn how to use them. I hope this tool helps you navigate your learning journey with greater engagement and a firmer grasp of the knowledge!

## Included

- `SKILL.md` — concise agent workflow and routing instructions
- `agents/openai.yaml` — Codex UI metadata and default prompt
- `references/` — portable command contract, mentoring protocol, state schema, quality rubric, and host integration notes
- `scripts/mentor_state.py` — dependency-free, safety-scoped progress-file CLI
- `package.json`, `cordis.patch.yml`, `lib/index.js` — DeepSeek Harness bundle that serves this same skill bundle as a managed plugin
- `locale/`, `icon.svg` — bundle display metadata
- `tests/` — behavior, contract, host-compatibility, and provider regression tests
- `.github/` — pull-request template, issue forms, and CI

## Install

### Codex

Clone this repository into your Codex skills directory:

```bash
git clone <repository-url> "${CODEX_HOME:-$HOME/.codex}/skills/skill-as-step-by-step-mentor"
```

Restart or reload Codex, then invoke:

```text
$skill-as-step-by-step-mentor
```

### DeepSeek Harness: local skill root

The Harness discovers local skills from its filesystem skill roots, so the checkout works without any build step. Link the repository into the user-level root:

```bash
mkdir -p "${DSH_HOME:-$HOME/.dsh}/skills"
ln -s "$PWD" "${DSH_HOME:-$HOME/.dsh}/skills/skill-as-step-by-step-mentor"
```

Invoke it with `/skill-as-step-by-step-mentor` in the composer, or let the agent load it when a request matches the description. Discovery is watched, so the skill reaches the next catalog without restarting the Harness. For repository-local use, place the bundle under `<repository>/.dsh/skills/` instead. This route is the best one while editing the skill, because every change applies immediately.

### DeepSeek Harness: managed plugin

The repository root is also a DeepSeek Harness bundle package named `dsh-skill-step-by-step-mentor`. Install that package through the Harness plugin manager when the skill should be enabled, disabled, updated, or removed per profile instead of living on disk:

| Item | Value |
|---|---|
| Bundle package | `dsh-skill-step-by-step-mentor` |
| Plugin row | `skill-step-mentor` |
| Install target | `https://github.com/lord-of-vaegirs/Skill-As-Step-by-Step-Mentor` or the checkout's absolute path |
| Invocation | `/skill-as-step-by-step-mentor` |

The manager runs pnpm, records the package in the profile, selects the bundle, and applies `cordis.patch.yml`, which inserts the skills provider. The provider reads `SKILL.md` from the installed package on every catalog request, so a reinstalled copy replaces the instructions without a provider change.

Use one route at a time: a local skill root and an installed bundle would advertise the same skill name, and the local root wins by rank.

For local development, keep the repository anywhere and symlink it into either skills directory.

See [references/harness-integration.md](references/harness-integration.md) for the scanned roots, frontmatter constraints, the bundle layout, and the installation checklist.

## Validate

Run the repository tests:

```bash
python3 -m unittest discover -s tests -v
node --test tests/provider.test.mjs
```

`npm pack --dry-run` lists the files an installed bundle would contain; the expected list is the skill bundle, `lib/index.js`, `cordis.patch.yml`, and the display metadata only.

If the Codex `skill-creator` utilities are installed, also run:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

## Contribute

Open an issue with a concrete learning scenario, then add or update a regression test with the behavior change. Keep `SKILL.md` compact and place detailed protocols in `references/`. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
