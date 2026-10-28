# Contributing

Contributions are welcome, especially real learning scenarios, command-edge cases, safety improvements, and evidence-based mentoring patterns.

1. Open an issue that describes the learner request, observed behavior, and desired behavior.
2. Fork the repository and create a focused branch.
3. Keep triggering information in the `SKILL.md` description and core procedure in its body.
4. Put detailed or conditional knowledge in a directly linked file under `references/`.
5. Add or update tests for command contracts, deterministic scripts, and host compatibility.
6. Run `python3 -m unittest discover -s tests -v` and, when available, the Codex `quick_validate.py` utility.
7. Open a pull request using the template.

Keep the skill installable in both Codex and DeepSeek Harness: the frontmatter stays `name` plus a single-line `description` within 500 characters, the name repeats the bundle directory name, and `references/` and `scripts/` paths resolve against the reported skill base directory. See `references/harness-integration.md`.

Do not add credentials, learner secrets, generated progress files, or copyrighted source material. Preserve history and deletion-confirmation guarantees when changing state behavior.
