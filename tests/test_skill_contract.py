from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_links_exist(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        links = re.findall(r"\]\((references/[^)]+)\)", text)
        self.assertGreaterEqual(len(links), 4)
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)

    def test_portable_commands_are_documented(self) -> None:
        text = (ROOT / "references" / "commands.md").read_text(encoding="utf-8")
        commands = [
            "[help]", "[command]", "[start]", "[restart all]",
            "[goto whole head]", "[goto whole tail]", "[goto part head]",
            "[goto part tail]", "[save]", "[save exit]", "[exit]",
            "[del]", "[del exit]", "[list]", "[load all]",
        ]
        for command in commands:
            self.assertIn(command, text)

    def test_openai_prompt_names_skill(self) -> None:
        text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$skill-as-step-by-step-mentor", text)

    def test_formal_name_is_consistent(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        agent_text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
        command_text = (ROOT / "references" / "commands.md").read_text(encoding="utf-8")

        self.assertIn("name: skill-as-step-by-step-mentor", skill_text)
        self.assertIn("# Skill As Step by Step Mentor", skill_text)
        self.assertIn('display_name: "Skill As Step by Step Mentor"', agent_text)
        self.assertIn("# Skill As Step by Step Mentor", readme_text)
        self.assertIn("Skill As Step by Step Mentor 使用方法", command_text)

    def test_explanation_precedes_answers_by_default(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        protocol_text = (
            ROOT / "references" / "mentoring-protocol.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Default to explanation before answer", skill_text)
        self.assertIn("every learning interaction", skill_text)
        self.assertIn("explicitly says", skill_text)
        self.assertIn("Do not infer the exception", protocol_text)
        self.assertIn("resume explanation-first teaching", protocol_text)

    def test_missing_goal_gets_a_user_reviewed_proposal(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        protocol_text = (
            ROOT / "references" / "mentoring-protocol.md"
        ).read_text(encoding="utf-8")
        command_text = (
            ROOT / "references" / "commands.md"
        ).read_text(encoding="utf-8")

        self.assertIn("draft an observable provisional goal", skill_text)
        self.assertIn("approve or revise it before finalizing the route", skill_text)
        self.assertIn("autonomously propose a provisional goal", protocol_text)
        self.assertIn("do not finalize the route", protocol_text)
        self.assertIn("Codex 会提出", command_text)

    def test_new_terminology_is_explained_before_use(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        protocol_text = (
            ROOT / "references" / "mentoring-protocol.md"
        ).read_text(encoding="utf-8")
        progress_text = (
            ROOT / "references" / "progress-format.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Before first using an unexplained", skill_text)
        self.assertIn("### Terminology gate", protocol_text)
        self.assertIn("define it in plain language", protocol_text)
        self.assertIn("Do not hide a new term", protocol_text)
        self.assertIn("## Terminology ledger", progress_text)

    def test_explanations_follow_a_guided_dependency_chain(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        protocol_text = (
            ROOT / "references" / "mentoring-protocol.md"
        ).read_text(encoding="utf-8")

        self.assertIn("guided dependency chain", skill_text)
        self.assertIn("learner-provided materials", skill_text)
        for step in [
            "**Context**", "**Prerequisites**", "**Vocabulary**",
            "**Structure**", "**Operation**", "**Example**", "**Practice**",
        ]:
            self.assertIn(step, protocol_text)
        self.assertIn("why the next concept is needed", protocol_text)


if __name__ == "__main__":
    unittest.main()
