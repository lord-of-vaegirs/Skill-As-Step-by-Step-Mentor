from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mentor_state.py"


class MentorStateTests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, result.stderr)
        return result

    def test_init_list_show_copy_delete(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            created = self.run_cli(
                root,
                "init",
                "--topic",
                "Memory Safety",
                "--goal",
                "Debug an out-of-bounds write",
                "--foundation",
                "Knows C basics",
                "--filename",
                "session.md",
            )
            source = Path(created.stdout.strip())
            self.assertTrue(source.is_file())
            self.assertIn("schema_version: 1", source.read_text(encoding="utf-8"))

            listed = self.run_cli(root, "list")
            self.assertIn("session.md", listed.stdout)

            shown = self.run_cli(root, "show", "session.md")
            self.assertIn("Memory Safety", shown.stdout)

            copied = self.run_cli(root, "copy", "session.md", "copy.md")
            self.assertTrue(Path(copied.stdout.strip()).is_file())

            preview = self.run_cli(root, "delete", "copy.md", expected=2)
            self.assertIn("Would delete", preview.stdout)
            self.assertTrue((root / "copy.md").exists())

            self.run_cli(root, "delete", "copy.md", "--yes")
            self.assertFalse((root / "copy.md").exists())

    def test_rejects_path_escape_and_unrelated_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "notes.md").write_text("ordinary notes", encoding="utf-8")
            listed = self.run_cli(root, "list")
            self.assertNotIn("notes.md", listed.stdout)

            result = self.run_cli(
                root,
                "init",
                "--topic",
                "x",
                "--goal",
                "y",
                "--filename",
                "../escape.md",
                expected=1,
            )
            self.assertIn("escapes root", result.stderr)


if __name__ == "__main__":
    unittest.main()
