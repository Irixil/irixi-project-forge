from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install_local_skill.py"
SPEC = importlib.util.spec_from_file_location("install_local_skill", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InstallLocalSkillTests(unittest.TestCase):
    def test_install_contains_one_discoverable_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / ".agents" / "skills" / "dz"
            installed, backup = MODULE.install(ROOT, target)

            self.assertEqual(installed, target)
            self.assertIsNone(backup)
            self.assertEqual(list(target.rglob("SKILL.md")), [target / "SKILL.md"])
            self.assertFalse((target / "skills").exists())
            self.assertTrue((target / "references" / "takeover-resume.md").is_file())
            self.assertTrue((target / "scripts" / "dz_state.py").is_file())
            self.assertTrue((target / MODULE.MARKER).is_file())

    def test_replace_existing_repository_symlink_removes_duplicate_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / ".agents" / "skills" / "dz"
            target.parent.mkdir(parents=True)
            target.symlink_to(ROOT, target_is_directory=True)

            installed, backup = MODULE.install(ROOT, target, replace=True)

            self.assertEqual(installed, target)
            self.assertIsNotNone(backup)
            assert backup is not None
            self.assertTrue(backup.is_symlink())
            self.assertEqual(backup.resolve(), ROOT)
            self.assertFalse(target.is_symlink())
            self.assertEqual(list(target.rglob("SKILL.md")), [target / "SKILL.md"])

    def test_replace_refuses_unmanaged_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / ".agents" / "skills" / "dz"
            target.mkdir(parents=True)
            (target / "user-file.txt").write_text("keep", encoding="utf-8")

            with self.assertRaises(MODULE.InstallError):
                MODULE.install(ROOT, target, replace=True)

            self.assertEqual((target / "user-file.txt").read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
