"""Regression tests for portability across skill hosts (Codex and DeepSeek Harness)."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = re.compile(r"\A---\r?\n(?P<body>[\s\S]*?)\r?\n---(?:\r?\n|\Z)")
KEBAB_NAME = re.compile(r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")
# The DeepSeek Harness catalog truncates longer descriptions.
HOST_DESCRIPTION_LIMIT = 500
BEHAVIOR_REFERENCES = [
    "commands.md",
    "learning-state-machine.md",
    "mentoring-protocol.md",
    "progress-format.md",
    "quality-rubric.md",
]


def frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if match is None:
        raise AssertionError("SKILL.md is missing YAML frontmatter")
    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise AssertionError(f"malformed frontmatter line: {line!r}")
        fields[key.strip()] = value.strip()
    return fields


class HarnessContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.fields = frontmatter(self.skill_text)

    def test_frontmatter_satisfies_host_requirements(self) -> None:
        self.assertEqual({"name", "description"}, set(self.fields))
        self.assertRegex(self.fields["name"], KEBAB_NAME)
        self.assertTrue(self.fields["description"])

    def test_install_docs_use_the_bundle_directory_name(self) -> None:
        # A directory bundle is registered under its directory name, so the
        # documented install path must repeat the frontmatter name exactly.
        name = self.fields["name"]
        for readme in ["README.md", "README.zh-CN.md"]:
            text = (ROOT / readme).read_text(encoding="utf-8")
            self.assertIn(f"skills/{name}", text, readme)
            self.assertIn(f"/{name}`", text, readme)

    def test_description_fits_the_host_catalog_budget(self) -> None:
        description = self.fields["description"]
        self.assertLessEqual(len(description), HOST_DESCRIPTION_LIMIT, len(description))
        self.assertNotIn("\n", description)

    def test_description_announces_the_portable_commands(self) -> None:
        for command in ["[help]", "[command]", "[start]", "[finish]", "[summarize]"]:
            self.assertIn(command, self.fields["description"])

    def test_script_invocations_resolve_against_the_skill_base(self) -> None:
        self.assertNotIn("python3 scripts/", self.skill_text)
        self.assertIn("<skill base>/scripts/mentor_state.py", self.skill_text)
        self.assertIn("--root", self.skill_text)

    def test_behavior_references_avoid_host_specific_wording(self) -> None:
        for name in BEHAVIOR_REFERENCES:
            text = (ROOT / "references" / name).read_text(encoding="utf-8")
            self.assertNotIn("Codex", text, name)

    def test_harness_integration_documents_both_hosts(self) -> None:
        text = (ROOT / "references" / "harness-integration.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Codex", text)
        self.assertIn("## DeepSeek Harness", text)
        self.assertIn("$DSH_HOME/skills", text)
        self.assertIn("<project root>/.dsh/skills", text)
        self.assertIn("/skill-as-step-by-step-mentor", text)

    def test_harness_integration_links_resolve(self) -> None:
        base = ROOT / "references"
        text = (base / "harness-integration.md").read_text(encoding="utf-8")
        links = re.findall(r"\]\((\.\.?/[^)#]+)\)", text)
        self.assertTrue(links)
        for link in links:
            self.assertTrue((base / link).resolve().is_file(), link)

    def test_skill_is_invocable_by_both_host_surfaces(self) -> None:
        # Omitting the invocation keys keeps the model catalog and /name enabled.
        self.assertNotIn("disable-model-invocation", self.fields)
        self.assertNotIn("user-invocable", self.fields)


if __name__ == "__main__":
    unittest.main()
