"""Verify that generated loading surfaces cannot silently drift from the core."""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WorkflowSyncTests(unittest.TestCase):
    def test_distributed_prompt_matches_and_its_reference_links_resolve(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/sync_workflow.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        prompt = ROOT / "portable/DZ-UNIVERSAL.md"
        for link in re.findall(r"\]\((\.\./references/[^)]+)\)", prompt.read_text()):
            self.assertTrue((prompt.parent / link).is_file(), link)

    def test_core_change_fails_check_until_regenerated(self):
        with tempfile.TemporaryDirectory(prefix="dz-sync-") as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "portable").mkdir()
            for relative in ("scripts/sync_workflow.py", "SKILL.md", "dz-manifest.json", "portable/DZ-UNIVERSAL.md"):
                shutil.copy2(ROOT / relative, root / relative)
            script = root / "scripts/sync_workflow.py"
            skill = root / "SKILL.md"
            skill.write_text(skill.read_text() + "\nSynthetic changed instruction.\n")
            manifest = json.loads((root / "dz-manifest.json").read_text())
            manifest["workflow_version"] = "synthetic-successor"
            (root / "dz-manifest.json").write_text(json.dumps(manifest))
            self.assertEqual(subprocess.run([sys.executable, str(script), "--check"], capture_output=True).returncode, 1)
            subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
            subprocess.run([sys.executable, str(script), "--check"], check=True, capture_output=True)
            prompt = (root / "portable/DZ-UNIVERSAL.md").read_text()
            self.assertIn("synthetic-successor", prompt)
            self.assertIn("Synthetic changed instruction.", prompt)


if __name__ == "__main__":
    unittest.main()
