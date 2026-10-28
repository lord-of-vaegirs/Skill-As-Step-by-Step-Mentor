"""Regression tests for the DeepSeek Harness bundle package shipped at the repository root."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
KEBAB_NAME = re.compile(r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SEMVER = re.compile(r"\A\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?\Z")

# Shipped by the package so an installed copy can serve the skill and its helper.
REQUIRED_PACKAGED_PATHS = [
    "SKILL.md",
    "lib/index.js",
    "cordis.patch.yml",
    "icon.svg",
    "agents",
    "references",
    "scripts",
]


class DshBundleTests(unittest.TestCase):
    def test_manifest_identity_is_installable(self) -> None:
        self.assertRegex(PACKAGE["name"], KEBAB_NAME)
        self.assertRegex(PACKAGE["version"], SEMVER)
        self.assertEqual("module", PACKAGE["type"])
        self.assertTrue(PACKAGE["description"])
        self.assertEqual("MIT", PACKAGE["license"])

    def test_bundle_patch_is_declared_and_present(self) -> None:
        patch = PACKAGE["dsh"]["bundle"]["patch"]
        self.assertEqual("./cordis.patch.yml", patch)
        self.assertTrue((ROOT / patch).is_file())

    def test_bundle_patch_inserts_its_own_provider_row(self) -> None:
        text = (ROOT / "cordis.patch.yml").read_text(encoding="utf-8")
        self.assertIn("insert:", text)
        rows = re.findall(r"name: '([^']+)'", text)
        self.assertEqual([PACKAGE["name"]], rows)
        self.assertRegex(re.search(r"id: ([a-z0-9-]+)", text).group(1), KEBAB_NAME)

    def test_entry_points_resolve(self) -> None:
        self.assertEqual("lib/index.js", PACKAGE["main"])
        for key, value in PACKAGE["exports"].items():
            self.assertTrue(value.startswith("./"), key)
            if "*" in value:
                continue
            self.assertTrue((ROOT / value).is_file(), value)
        self.assertTrue((ROOT / PACKAGE["main"]).is_file())

    def test_package_ships_the_skill_bundle(self) -> None:
        files = PACKAGE["files"]
        for path in REQUIRED_PACKAGED_PATHS:
            self.assertIn(path, files)
        # Tests and repository tooling stay out of the installed copy.
        self.assertNotIn("tests", files)
        self.assertNotIn(".github", files)

    def test_provider_has_no_registry_dependencies(self) -> None:
        source = (ROOT / "lib" / "index.js").read_text(encoding="utf-8")
        imports = re.findall(r"^import .*?from \"([^\"]+)\";$", source, re.MULTILINE)
        self.assertTrue(imports)
        for specifier in imports:
            self.assertTrue(specifier.startswith("node:"), specifier)
        for exported in ["export function apply", "export const inject", "export const name"]:
            self.assertIn(exported, source)

    def test_display_metadata_is_localized(self) -> None:
        for language in ["en", "zh"]:
            locale = json.loads(
                (ROOT / "locale" / f"{language}.json").read_text(encoding="utf-8")
            )
            self.assertTrue(locale["meta"]["title"], language)
            self.assertTrue(locale["meta"]["description"], language)
        self.assertEqual("./icon.svg", PACKAGE["icon"])
        self.assertIn("<svg", (ROOT / "icon.svg").read_text(encoding="utf-8"))

    def test_bundle_does_not_duplicate_the_skill_bundle(self) -> None:
        # The package root is the skill bundle, so a stray copy would drift.
        stray = [
            path
            for path in ROOT.rglob("SKILL.md")
            if path != ROOT / "SKILL.md" and ".git" not in path.parts
        ]
        self.assertEqual([], stray)


if __name__ == "__main__":
    unittest.main()
