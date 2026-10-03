"""Synthetic ledger tests; these do not prove model compliance or real product quality."""
import json
import shutil
import unittest
import test_dz_state as fixtures


class PersonalWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.h = fixtures.DzStateTests()
        self.h.setUp()
        self.addCleanup(self.h.tearDown)

    def test_effort_stop_is_durable_readable_and_does_not_fake_verification(self):
        h = self.h
        h.add_work()
        h.cli("update-work", str(h.project), "W1", "--status", "in_progress")
        h.cli("update-work", str(h.project), "W1", "--status", "blocked",
              "--blocker", "Two attempts repeated the same error with no new facts",
              "--note", "15-minute/three-attempt slice; two no-progress attempts reached stop condition")
        h.cli("set-run", str(h.project), "--status", "blocked", "--blocker-kind", "effort_limit",
              "--blocker", "The configured no-progress stop condition was reached",
              "--resume-when", "Choose a distinct repair hypothesis or supply a missing diagnostic")
        h.cli("can-stop", str(h.project))
        before = (h.project / ".dz/state.json").read_bytes()
        journal = (h.project / ".dz/journal.jsonl").read_bytes()
        report = json.loads(h.cli("resume-report", str(h.project)).stdout)
        self.assertEqual(report["current_summary"]["run"]["blocker_kind"], "effort_limit")
        self.assertEqual(report["current_summary"]["work"]["open_items"][0]["status"], "blocked")
        self.assertNotEqual(report["current_summary"]["progress"]["verification"], "verified")
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), before)
        self.assertEqual((h.project / ".dz/journal.jsonl").read_bytes(), journal)
        h.cli("set-run", str(h.project), "--status", "active",
              "--next-action", "Inspect a newly supplied diagnostic under the current goal")
        self.assertIsNone(h.state()["run"]["blocker_kind"])
        self.assertNotEqual(h.state()["run"]["product_verdict"], "verified")
        h.cli("check", str(h.project))

    def test_effort_stop_requires_reason_and_resume_condition_without_partial_write(self):
        h = self.h
        before = (h.project / ".dz/state.json").read_bytes()
        journal = (h.project / ".dz/journal.jsonl").read_bytes()
        for extra in (("--blocker", "retry limit"), ("--resume-when", "new hypothesis")):
            h.cli("set-run", str(h.project), "--status", "blocked", "--blocker-kind", "effort_limit",
                  *extra, expected=1)
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), before)
        self.assertEqual((h.project / ".dz/journal.jsonl").read_bytes(), journal)

    def test_local_success_cannot_hide_failed_required_main_flow(self):
        h = self.h
        main = "[DZ-MUST:R2] Complete the input-to-saved-result user flow"
        h.write_project_file("docs/sdlc/spec.md", f"# Required outcomes\n- {h.DEFAULT_ACCEPTANCE}\n- {main}\n")
        h.add_work()
        h.cli("add-work", str(h.project), "--id", "W2", "--title", "Core user flow",
              "--phase", "test", "--acceptance", main)
        h.verify_default_work()
        proof = h.evidence_proof("E2")
        h.cli("add-evidence", str(h.project), "--id", "E2", "--work-item", "W2",
              "--acceptance", main, "--kind", "test", "--claim", "Synthetic main flow failed",
              "--source", "Synthetic deterministic fixture", *proof, "--result", "failed")
        self.assertEqual(h.state()["work_items"][0]["status"], "verified")
        before = (h.project / ".dz/state.json").read_bytes()
        h.cli("close", str(h.project), "--verdict", "verified", "--reason", "Local check passed", expected=1)
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), before)
        report = json.loads(h.cli("resume-report", str(h.project)).stdout)
        self.assertNotEqual(report["current_summary"]["progress"]["verification"], "verified")
        self.assertIn("W2", [w["id"] for w in report["current_summary"]["work"]["open_items"]])

    def test_portable_records_preserve_goal_evidence_and_pause_without_execution(self):
        h = self.h
        h.add_work()
        h.verify_default_work()
        h.cli("set-run", str(h.project), "--status", "paused", "--resume-when", "Owner returns")
        original = h.state()
        moved = h.project.parent / "moved-project"
        shutil.copytree(h.project, moved)
        journal = (moved / ".dz/journal.jsonl").read_bytes()
        report = json.loads(h.cli("resume-report", str(moved)).stdout)
        self.assertEqual(report["current_summary"]["goal"]["statement"], original["goal"]["statement"])
        self.assertEqual(report["current_summary"]["run"]["status"], "paused")
        self.assertEqual(json.loads((moved / ".dz/state.json").read_text()), original)
        self.assertEqual((moved / ".dz/journal.jsonl").read_bytes(), journal)
        self.assertTrue(report["generated_views"]["all_current"])
        self.assertTrue(report["diagnostics"]["record_integrity_ok"])
        self.assertFalse(report["diagnostics"]["execution_allowed"])


if __name__ == "__main__":
    unittest.main()
