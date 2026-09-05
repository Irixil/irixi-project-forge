from __future__ import annotations

import importlib.util
import json
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
            self.assertTrue((target / "references" / "evidence-led-discovery.md").is_file())
            self.assertTrue((target / "references" / "change-proposal-review.md").is_file())
            self.assertTrue((target / "references" / "project-record-health.md").is_file())
            self.assertTrue((target / "scripts" / "dz_state.py").is_file())
            self.assertTrue((target / MODULE.MARKER).is_file())

    def test_manifest_reference_sets_point_to_real_files(self) -> None:
        manifest = json.loads((ROOT / "dz-manifest.json").read_text(encoding="utf-8"))

        for paths in manifest["reference_sets"].values():
            for relative_path in paths:
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_published_workflow_versions_match(self) -> None:
        manifest = json.loads((ROOT / "dz-manifest.json").read_text(encoding="utf-8"))
        version = manifest["workflow_version"]
        plugin = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )

        self.assertEqual(plugin["version"], manifest["distribution"]["plugin_version"])

        self.assertIn(
            f'WORKFLOW_VERSION = "{version}"',
            (ROOT / "scripts" / "dz_state.py").read_text(encoding="utf-8"),
        )
        self.assertIn(
            f"DZ workflow version: `{version}`",
            (ROOT / "portable" / "DZ-UNIVERSAL.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            f"DZ workflow guidance version: `{version}`",
            (ROOT / "assets" / "project" / "AGENTS.md").read_text(encoding="utf-8"),
        )

    def test_behavioral_hardening_is_present_in_skill_and_portable_prompt(self) -> None:
        manifest = json.loads((ROOT / "dz-manifest.json").read_text(encoding="utf-8"))
        rules = manifest["non_negotiable_behavior"]
        for key in (
            "named_solution_parts_are_routed_now_later_or_wont",
            "external_action_agents_define_retry_duplicate_timeout_and_recovery",
            "autonomous_change_review_checks_scope_impersonation_duplicates_and_recovery",
            "maintenance_release_requires_current_reverification_and_authorization",
            "beginner_takeover_pause_close_and_health_use_one_four_line_block",
        ):
            self.assertIs(rules[key], True, key)

        guided = (ROOT / "references" / "guided-dialogue.md").read_text(
            encoding="utf-8"
        )
        review = (ROOT / "references" / "change-proposal-review.md").read_text(
            encoding="utf-8"
        )
        portable = (ROOT / "portable" / "DZ-UNIVERSAL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("duplicate-action prevention", guided)
        self.assertIn("“需要时再看” is not a trigger", guided)
        self.assertIn("impersonates the owner", review)
        self.assertIn("concrete opportunity cost visible", review)
        self.assertIn("fresh approval for that exact revision and environment", portable)
        self.assertIn("a branch, commit, pull request", portable)
        self.assertIn("receive current scope-specific authorization", portable)
        self.assertIn(
            "A previous Plan, monitoring setup, or earlier release approval cannot authorize it",
            portable,
        )
        self.assertIn("in the durable project handoff", portable)
        self.assertIn("do not print a second detail list", portable)

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
