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
            f"# DZ Universal Workflow — {version}",
            (ROOT / "portable" / "DZ-UNIVERSAL.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            f"DZ workflow guidance version: `{version}`",
            (ROOT / "assets" / "project" / "AGENTS.md").read_text(encoding="utf-8"),
        )

    def test_distribution_preserves_declared_controls_and_routes(self) -> None:
        manifest = json.loads((ROOT / "dz-manifest.json").read_text(encoding="utf-8"))
        rules = manifest["non_negotiable_behavior"]
        for key in (
            "one_decision_topic_per_turn",
            "bounded_changes_reopen_only_affected_decisions",
            "reuse_search_runs_only_when_materially_useful",
            "resume_mechanically_validates_every_journal_record",
            "resume_uses_compact_current_summary_by_default",
            "generated_project_view_is_fingerprint_checked",
            "clear_current_user_instruction_counts_as_authorization",
            "ordinary_changes_rerun_affected_and_critical_checks",
            "release_candidate_requires_full_acceptance_set",
            "pre_deploy_ai_preflight_is_default",
            "preflight_separates_end_to_end_and_code_review",
            "safe_preflight_does_not_require_duplicate_permission",
            "ai_preflight_does_not_replace_internal_human_testing",
        ):
            self.assertIs(rules[key], True, key)

        # Packaging integrity is not a behavioral test of an AI. Real dialogue
        # scenarios are evaluated independently, never by matching prose fragments.
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dz"
            MODULE.install(ROOT, target)
            for relative in (
                "SKILL.md", "portable/DZ-UNIVERSAL.md",
                "references/guided-dialogue.md", "references/change-proposal-review.md",
                "references/phase-gates.md", "references/artifacts/review-release.md",
                "references/user-trial.md", "scripts/sync_workflow.py",
            ):
                self.assertEqual((target / relative).read_bytes(), (ROOT / relative).read_bytes(), relative)

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
