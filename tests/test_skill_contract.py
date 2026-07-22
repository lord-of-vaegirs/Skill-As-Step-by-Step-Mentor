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
            "[help]", "[command]", "[start]", "[finish]",
            "[summarize]", "[summarize all]", "[restart]", "[restart all]",
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

    def test_first_part_response_contains_explanation_only(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        state_text = (
            ROOT / "references" / "learning-state-machine.md"
        ).read_text(encoding="utf-8")

        self.assertIn("provide only that part's explanation", skill_text)
        self.assertIn("require `[finish]` before practice", skill_text)
        self.assertIn("Do not combine a part's first explanation", state_text)
        self.assertIn("Do not include exercises", state_text)

    def test_missing_goal_gets_a_user_reviewed_proposal(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        protocol_text = (
            ROOT / "references" / "mentoring-protocol.md"
        ).read_text(encoding="utf-8")
        command_text = (
            ROOT / "references" / "commands.md"
        ).read_text(encoding="utf-8")

        self.assertIn("draft an observable provisional goal", skill_text)
        self.assertIn("approve or revise it", skill_text)
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

        self.assertIn("source-grounded background", skill_text)
        self.assertIn("learner-provided material", protocol_text)
        for step in [
            "**Context**", "**Prerequisites**", "**Vocabulary**",
            "**Structure**", "**Operation**", "**Example**", "**Boundary**",
        ]:
            self.assertIn(step, protocol_text)
        self.assertIn("why the next concept is needed", protocol_text)

    def test_parts_and_phases_are_hard_gated(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        state_text = (
            ROOT / "references" / "learning-state-machine.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Treat the state machine as a hard constraint", skill_text)
        self.assertIn("Never reveal a future part's teaching content", skill_text)
        for phase in [
            "`part_explanation`", "`part_practice`", "`part_review`",
            "`part_summary_ready`", "`final_summary_ready`", "`completed`",
        ]:
            self.assertIn(phase, state_text)
        self.assertIn("Require the exact command or submitted evidence", state_text)

    def test_summary_transitions_follow_user_commands(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        state_text = (
            ROOT / "references" / "learning-state-machine.md"
        ).read_text(encoding="utf-8")

        self.assertIn("prompt the learner to send `[summarize]`", skill_text)
        self.assertIn("prompt `[summarize all]` and wait", skill_text)
        self.assertIn("Error-free result → `part_summary_ready`", state_text)
        self.assertIn("`[summarize all]` → `completed`", state_text)
        self.assertIn("answering ordinary learning requests", skill_text)

    def test_restart_preserves_qa_but_clears_learning_state(self) -> None:
        command_text = (
            ROOT / "references" / "commands.md"
        ).read_text(encoding="utf-8")
        state_text = (
            ROOT / "references" / "learning-state-machine.md"
        ).read_text(encoding="utf-8")
        progress_text = (
            ROOT / "references" / "progress-format.md"
        ).read_text(encoding="utf-8")

        self.assertIn("preserve a Q&A archive", state_text)
        self.assertIn("remove memories of theory learned", state_text)
        self.assertIn("affected history events", state_text)
        self.assertIn("Do not delete the learner's source files", state_text)
        self.assertIn("preserve Q&A archives but clear theory", command_text)
        self.assertIn("## Q&A archive", progress_text)


if __name__ == "__main__":
    unittest.main()
