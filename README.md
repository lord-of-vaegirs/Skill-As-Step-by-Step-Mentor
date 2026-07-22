# Skill As Step by Step Mentor

<p align="right">
  <strong>English</strong> | <a href="./README.zh-CN.md">简体中文</a>
</p>

A Codex skill-agent project for source-grounded, hands-on engineering learning. It turns a broad learning goal into an adaptive route, verifies practical evidence one checkpoint at a time, and persists recoverable Markdown progress.

By default, every learning part explains the relevant knowledge before presenting answers or practice. If no final goal is supplied, Codex proposes an observable goal with success evidence and asks the learner to approve or revise it before the route begins.

## Why did I create this skill?
In today's world, learning across various fields—especially computer science—often presents a challenge: while resources abound, truly absorbing the material is difficult. After much reflection, I realized the root cause is the lack of an immersive learning experience. We often have resources at our fingertips but don't know where to start or how to structure a study plan, leading us to quickly forget what we’ve learned. To address these persistent issues, I decided to harness the power of AI. It acts as a dedicated, 24/7 personal tutor—always at your beck and call—to handle planning and practice scheduling. It addresses your specific questions and ideas, providing tailored exercises and examples that help you master the material with confidence. For added convenience, I’ve included special commands; simply type `[command]` into the chat box to learn how to use them. I hope this tool helps you navigate your learning journey with greater engagement and a firmer grasp of the knowledge!

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
