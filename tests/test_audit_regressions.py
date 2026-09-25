"""State-machine regressions from the read-only workflow audit; synthetic projects only."""
import hashlib
import json
import os
import subprocess
import unittest

import test_dz_state as fixtures


class AuditRegressionTests(unittest.TestCase):
    def setUp(self):
        self.h = fixtures.DzStateTests()
        self.h.setUp()
        self.addCleanup(self.h.tearDown)
        self.h.add_work()

    def verified_issue(self):
        h = self.h
        h.cli("add-issue", str(h.project), "--id", "I1", "--title", "Observed regression",
              "--kind", "implementation_gap", "--source", "synthetic reproduction",
              "--expected", "success", "--actual", "failure", "--impact", "flow fails", "--work-item", "W1")
        h.cli("update-issue", str(h.project), "I1", "--status", "triaged")
        h.cli("update-issue", str(h.project), "I1", "--status", "in_progress")
        h.cli("update-issue", str(h.project), "I1", "--status", "implemented_unverified", "--resolution", "first repair")
        h.verify_default_work()
        h.cli("update-issue", str(h.project), "I1", "--status", "verified", "--evidence", "E1", "--prevention", "regression test")

    def test_reopening_issue_reopens_work_and_expires_old_proof(self):
        h = self.h
        self.verified_issue()
        h.cli("update-issue", str(h.project), "I1", "--status", "in_progress")
        state = h.state()
        self.assertIsNone(state["target"]["id"])
        self.assertEqual(state["work_items"][0]["status"], "in_progress")
        self.assertEqual(state["issues"][0]["evidence_ids"], [])
        h.cli("update-issue", str(h.project), "I1", "--status", "implemented_unverified", "--resolution", "second repair")
        h.cli("update-issue", str(h.project), "I1", "--status", "verified", "--evidence", "E1", expected=1)
        h.cli("close", str(h.project), "--verdict", "verified", "--reason", "cannot reuse old proof", expected=1)

    def test_recovery_downgrades_issues_whose_evidence_changed(self):
        h = self.h
        self.verified_issue()
        h.write_project_file(h.state()["evidence"][0]["artifact_path"], "changed proof\n")
        h.cli("recover", str(h.project))
        state = h.state()
        self.assertEqual(state["issues"][0]["status"], "implemented_unverified")
        self.assertEqual(state["issues"][0]["evidence_ids"], [])
        self.assertEqual(state["work_items"][0]["status"], "implemented_unverified")
        h.cli("check", str(h.project))

    def test_linking_an_issue_preserves_target_but_entering_repair_starts_a_new_attempt(self):
        h = self.h
        self.verified_issue()
        h.cli("update-work", str(h.project), "W1", "--status", "in_progress")
        h.cli("add-evidence", str(h.project), "--id", "E2", "--work-item", "W1",
              "--acceptance", h.DEFAULT_ACCEPTANCE, "--kind", "test", "--claim", "current check",
              "--source", "synthetic check", *h.evidence_proof("E2", revision="rev-2"), "--result", "passed")
        h.cli("update-issue", str(h.project), "I1", "--status", "verified", "--evidence", "E2")
        target = h.state()["target"]
        h.cli("add-issue", str(h.project), "--id", "I2", "--title", "Second repair in same work",
              "--kind", "implementation_gap", "--source", "fixture", "--expected", "success",
              "--actual", "failure", "--impact", "flow fails", "--work-item", "W1")
        h.cli("update-issue", str(h.project), "I2", "--status", "triaged")
        self.assertEqual(h.state()["target"], target)
        self.assertEqual(h.state()["issues"][0]["status"], "verified")
        h.cli("update-issue", str(h.project), "I2", "--status", "in_progress")
        self.assertIsNone(h.state()["target"]["id"])
        self.assertEqual(h.state()["work_items"][0]["evidence_floor"], 2)
        self.assertEqual(h.state()["issues"][0]["status"], "implemented_unverified")
        h.cli("update-issue", str(h.project), "I1", "--status", "verified", "--evidence", "E2", expected=1)
        h.cli("add-evidence", str(h.project), "--id", "E3", "--work-item", "W1",
              "--acceptance", h.DEFAULT_ACCEPTANCE, "--kind", "test", "--claim", "new repair check",
              "--source", "synthetic check", *h.evidence_proof("E3", revision="rev-2"), "--result", "passed")
        current_target = h.state()["target"]
        h.cli("update-issue", str(h.project), "I2", "--status", "in_progress")
        self.assertEqual(h.state()["target"], current_target)
        self.assertEqual(h.state()["work_items"][0]["evidence_floor"], 2)
        h.cli("update-issue", str(h.project), "I2", "--status", "implemented_unverified", "--resolution", "new repair")
        h.cli("update-issue", str(h.project), "I2", "--status", "verified", "--evidence", "E3", "--prevention", "regression check")
        h.cli("update-issue", str(h.project), "I1", "--status", "verified", "--evidence", "E3")
        self.assertNotEqual(h.state()["target"]["id"], target["id"])

    def test_reopened_issue_requires_fresh_proof_for_all_work_criteria(self):
        self.assert_repair_requires_fresh_work_proof("reopened")

    def test_new_issue_requires_fresh_proof_for_all_work_criteria(self):
        self.assert_repair_requires_fresh_work_proof("new")

    def test_deferred_issue_resuming_repair_requires_fresh_proof_for_all_work_criteria(self):
        self.assert_repair_requires_fresh_work_proof("deferred")

    def assert_repair_requires_fresh_work_proof(self, route):
        h = fixtures.DzStateTests()
        h.setUp()
        self.addCleanup(h.tearDown)
        h.accept_chain()
        criterion_b = "Second criterion remains correct"
        h.cli("add-work", str(h.project), "--id", "W1", "--title", "Two-criterion implementation",
              "--phase", "build", "--acceptance", h.DEFAULT_ACCEPTANCE, "--acceptance", criterion_b)
        h.cli("add-issue", str(h.project), "--id", "I1", "--title", "Criterion A failure",
              "--kind", "implementation_gap", "--source", "fixture", "--expected", "pass",
              "--actual", "fail", "--impact", "flow fails", "--work-item", "W1")
        h.cli("update-issue", str(h.project), "I1", "--status", "triaged")
        h.cli("update-issue", str(h.project), "I1", "--status", "in_progress")
        h.cli("update-issue", str(h.project), "I1", "--status", "implemented_unverified", "--resolution", "first repair")

        def prove(evidence_id, criterion):
            h.cli("add-evidence", str(h.project), "--id", evidence_id, "--work-item", "W1",
                  "--acceptance", criterion, "--kind", "test", "--claim", criterion,
                  "--source", "synthetic fixture", *h.evidence_proof(evidence_id), "--result", "passed")

        prove("A1", h.DEFAULT_ACCEPTANCE)
        prove("B1", criterion_b)
        if route != "deferred":
            h.cli("update-issue", str(h.project), "I1", "--status", "verified", "--evidence", "A1", "--prevention", "regression check")
        old_evidence = h.state()["evidence"]
        repair_id = "I1"
        if route == "new":
            repair_id = "I2"
            h.cli("add-issue", str(h.project), "--id", repair_id, "--title", "New criterion A failure",
                  "--kind", "implementation_gap", "--source", "fixture", "--expected", "pass",
                  "--actual", "fail", "--impact", "flow fails", "--work-item", "W1")
            h.cli("update-issue", str(h.project), repair_id, "--status", "triaged")
        elif route == "deferred":
            h.cli("update-issue", str(h.project), repair_id, "--status", "deferred", "--resolution", "repair postponed")
            h.cli("update-issue", str(h.project), repair_id, "--status", "triaged")
        h.cli("update-issue", str(h.project), repair_id, "--status", "in_progress")
        h.cli("update-issue", str(h.project), repair_id, "--status", "implemented_unverified", "--resolution", "second repair")
        prove("A2", h.DEFAULT_ACCEPTANCE)
        h.cli("update-issue", str(h.project), repair_id, "--status", "verified", "--evidence", "A2", "--prevention", "regression check")
        if route == "new":
            h.cli("update-issue", str(h.project), "I1", "--status", "verified", "--evidence", "A2")
        h.cli("update-work", str(h.project), "W1", "--status", "implemented_unverified")
        h.cli("update-work", str(h.project), "W1", "--status", "verified", expected=1)
        h.cli("close", str(h.project), "--verdict", "verified", "--reason", "partial recheck cannot finish", expected=1)
        self.assertEqual(h.state()["evidence"][:2], old_evidence)
        prove("B2", criterion_b)
        h.cli("update-work", str(h.project), "W1", "--status", "verified")
        h.cli("close", str(h.project), "--verdict", "verified", "--reason", "all criteria checked after repair")
        h.cli("check", str(h.project))

    def test_malformed_workspace_checkpoints_report_uncertainty_without_altering_journal(self):
        h = self.h
        env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        subprocess.run(["git", "init"], cwd=h.project, env=env, capture_output=True, check=True)
        h.cli("set-run", str(h.project), "--status", "active", "--next-action", "inspect current records")
        journal_path = h.project / ".dz/journal.jsonl"
        original_lines = journal_path.read_text().splitlines()
        original_last = json.loads(original_lines[-1])
        malformed = [
            {"entries": [None]}, {"entries": {}}, {"entries": [{"path": ["bad"]}]},
            {"entries": [{"path": None}]}, {"entries": [{"path": "a", "status": 5, "content": {}}]},
            {"entries": [{"path": "a", "status": "??", "content": None}]},
            {"entries": [{"path": "a", "status": "??", "content": {"kind": []}}]},
            {"entries": [{"path": "a", "status": "??", "content": {"kind": "missing"}, "source": []}]},
            {"entries": [original_last["workspace"]["entries"][0]] * 2},
            {"digest": None}, {"digest": "0" * 64}, {"head": []}, {"branch": {}}, {"project_prefix": []},
        ]
        for changed in malformed:
            with self.subTest(changed=changed):
                record = json.loads(json.dumps(original_last))
                record["workspace"].update(changed)
                h.write_project_file(".dz/journal.jsonl", "\n".join(original_lines[:-1] + [json.dumps(record)]) + "\n")
                before = journal_path.read_bytes()
                report = json.loads(h.cli("resume-report", str(h.project)).stdout)
                self.assertIsNone(report["workspace"]["changed_since_saved_record"])
                self.assertTrue(report["workspace"]["uncertainty"])
                self.assertEqual(report["journal_records_reviewed"], len(original_lines))
                self.assertEqual(report["invalid_journal_records"], 0)
                self.assertEqual(journal_path.read_bytes(), before)
                h.cli("check", str(h.project))

    def add_read_only(self):
        h = self.h
        h.cli("add-work", str(h.project), "--id", "O1", "--title", "Read existing diagnostics",
              "--phase", "maintain", "--optional", "--acceptance", "Existing diagnostics were inspected",
              "--mode", "read_only", "--reason", "Only inspect the unchanged local target")

    def test_read_only_work_retains_proof_but_needs_its_own_fresh_check(self):
        h = self.h
        self.verified_issue()
        before = h.state()
        self.add_read_only()
        h.cli("update-work", str(h.project), "O1", "--status", "in_progress")
        self.assertEqual(h.state()["target"], before["target"])
        self.assertEqual(h.state()["work_items"][0]["status"], "verified")
        self.assertEqual(h.state()["issues"][0], before["issues"][0])
        h.cli("update-work", str(h.project), "O1", "--status", "implemented_unverified", expected=1)
        h.cli("update-work", str(h.project), "O1", "--status", "verified", expected=1)
        h.cli("add-evidence", str(h.project), "--id", "O1-E1", "--work-item", "O1",
              "--acceptance", "Existing diagnostics were inspected", "--kind", "inspection",
              "--claim", "Current diagnostics checked", "--source", "synthetic check",
              *h.evidence_proof("O1-E1"), "--result", "passed")
        h.cli("update-work", str(h.project), "O1", "--status", "verified")
        h.cli("update-work", str(h.project), "O1", "--status", "in_progress")
        h.cli("update-work", str(h.project), "O1", "--status", "verified", expected=1)
        h.cli("check", str(h.project))
        h.write_project_file("docs/sdlc/plan-v2.md", "# Updated plan\nKeep the independent observation task.\n")
        h.cli("set-decision", str(h.project), "plan", "--status", "draft", "--path", "docs/sdlc/plan-v2.md")
        h.cli("set-decision", str(h.project), "plan", "--status", "accepted", "--by", "fixture", "--reference", "explicit plan correction")
        h.cli("carry-work", str(h.project), "O1", "--disposition", "keep", "--reason", "still observe the current target")
        carried = h.state()["work_items"][-1]
        self.assertEqual(carried["mode"], "read_only")
        self.assertEqual(carried["status"], "pending")
        self.assertEqual(carried["evidence_ids"], [])
        h.cli("check", str(h.project))

    def test_read_only_work_cannot_enter_an_authorized_action(self):
        h = self.h
        h.verify_default_work()
        self.add_read_only()
        h.cli("update-work", str(h.project), "O1", "--status", "in_progress")
        h.cli("add-risk", str(h.project), "--id", "R1", "--title", "Outside write",
              "--level", "low", "--action-kind", "external_write", "--consequence", "outside effect",
              "--safer-option", "local inspection", "--scope", "write outside", "--expires-at", h.FUTURE_EXPIRY, expected=1)

    def test_read_only_mode_cannot_claim_implementation_or_release_or_bypass_pause(self):
        h = self.h
        h.verify_default_work()
        for phase in ("build", "deploy"):
            h.cli("add-work", str(h.project), "--id", "not-read-only", "--title", "Disallowed",
                  "--phase", phase, "--acceptance", "new implementation", "--mode", "read_only",
                  "--reason", "claimed inspection", expected=1)
        h.cli("add-work", str(h.project), "--id", "no-reason", "--title", "Disallowed",
              "--phase", "test", "--acceptance", "observation", "--mode", "read_only", expected=1)
        self.add_read_only()
        h.cli("add-issue", str(h.project), "--id", "not-repaired", "--title", "Repair claim",
              "--kind", "implementation_gap", "--source", "fixture", "--expected", "fixed",
              "--actual", "broken", "--impact", "failure", "--work-item", "O1", expected=1)
        h.cli("set-run", str(h.project), "--status", "paused", "--resume-when", "owner returns")
        h.cli("update-work", str(h.project), "O1", "--status", "in_progress", expected=1)
        self.assertEqual(h.state()["run"]["status"], "paused")
        h.cli("close", str(h.project), "--verdict", "cancelled", "--reason", "stop")
        h.cli("update-work", str(h.project), "O1", "--status", "in_progress", expected=1)
        self.assertEqual(h.state()["run"]["status"], "finished")

    def test_resume_report_diagnoses_artifact_drift_without_authorizing_execution(self):
        h = self.h
        h.verify_default_work()
        h.write_project_file("docs/sdlc/intent.md", "Changed accepted intent\n")
        state_bytes = (h.project / ".dz/state.json").read_bytes()
        journal_bytes = (h.project / ".dz/journal.jsonl").read_bytes()
        report = json.loads(h.cli("resume-report", str(h.project)).stdout)
        self.assertTrue(report["diagnostics"]["read_only"])
        self.assertFalse(report["diagnostics"]["execution_allowed"])
        self.assertTrue(any("artifact" in item for item in report["diagnostics"]["blocking_errors"]))
        self.assertFalse(report["diagnostics"]["current_records_valid"])
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), state_bytes)
        self.assertEqual((h.project / ".dz/journal.jsonl").read_bytes(), journal_bytes)
        h.cli("check", str(h.project), expected=1)

    def test_resume_report_checks_every_generated_view(self):
        h = self.h
        for name, key in (("work-items", "work_items_current"), ("issues", "issues_current")):
            with self.subTest(name=name):
                h.write_project_file(f"docs/sdlc/{name}.md", "stale body with a plausible heading\n")
                report = json.loads(h.cli("resume-report", str(h.project)).stdout)
                self.assertFalse(report["generated_views"][key])
                self.assertFalse(report["generated_views"]["all_current"])

    def test_snapshot_drift_report_uses_a_labeled_journal_fallback_without_repairing(self):
        h = self.h
        h.write_project_file(".dz/state.json", '{"schema_version":"1.1","work_items":false}\n')
        before = (h.project / ".dz/state.json").read_bytes()
        report = json.loads(h.cli("resume-report", str(h.project)).stdout)
        self.assertEqual(report["diagnostics"]["summary_basis"], "journal_fallback")
        self.assertFalse(report["diagnostics"]["record_integrity_ok"])
        self.assertFalse(report["diagnostics"]["execution_allowed"])
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), before)
        h.cli("check", str(h.project), expected=1)

    def legacy_snapshot(self, spec):
        h = self.h
        h.verify_default_work()
        h.cli("close", str(h.project), "--verdict", "verified", "--reason", "synthetic older completion")
        state = h.state()
        h.write_project_file("docs/sdlc/spec.md", spec)
        state["decisions"]["spec"]["artifact_sha256"] = hashlib.sha256(spec.encode()).hexdigest()
        contract = hashlib.sha256("\0".join(state["decisions"][name]["artifact_sha256"] for name in ("intent", "spec", "plan")).encode("ascii")).hexdigest()
        state["workflow_version"] = "2026-09-10.2"
        state.pop("requirements")
        state["target"]["contract_sha256"] = contract
        for item in state["work_items"] + state["evidence"]:
            item["contract_sha256"] = contract
        h.write_project_file(".dz/state.json", json.dumps(state))
        journal = (h.project / ".dz/journal.jsonl").read_text()
        h.write_project_file(".dz/journal.jsonl", journal + json.dumps({"at": "synthetic legacy", "event": "legacy fixture", "state": state}) + "\n")

    def test_finished_legacy_plain_spec_can_upgrade_without_claiming_coverage(self):
        h = self.h
        self.legacy_snapshot("# Accepted legacy specification\nObservable promise in ordinary prose.\n")
        h.cli("install-guidance", str(h.project))
        self.assertEqual(h.state()["run"]["status"], "finished")
        self.assertEqual(h.state()["run"]["product_verdict"], "partially_verified")
        self.assertEqual(h.state()["requirements"]["items"], [])
        h.cli("check", str(h.project))

    def test_rejected_guidance_upgrade_changes_no_guidance_or_records(self):
        h = self.h
        self.legacy_snapshot("- [DZ-MUST:R1] One\n- [DZ-MUST:R1] Duplicate\n")
        h.write_project_file("AGENTS.md", "User rules that must survive a rejected upgrade.\n")
        paths = [h.project / name for name in ("AGENTS.md", ".dz/state.json", ".dz/journal.jsonl")]
        before = [path.read_bytes() for path in paths]
        h.cli("install-guidance", str(h.project), expected=1)
        self.assertEqual([path.read_bytes() for path in paths], before)


if __name__ == "__main__":
    unittest.main()
