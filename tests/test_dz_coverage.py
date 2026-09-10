"""Synthetic ledger regressions, not evidence that a real product passed."""
import copy
import hashlib
import importlib.util
import json
import unittest

import test_dz_state as fixtures

module_spec = importlib.util.spec_from_file_location("dz_coverage_state", fixtures.SCRIPT)
state_tool = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(state_tool)


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.h = fixtures.DzStateTests()
        self.h.setUp()
        self.addCleanup(self.h.tearDown)

    def spec(self, text):
        self.h.write_project_file("docs/sdlc/spec.md", text)

    def report(self):
        return json.loads(self.h.cli("resume-report", str(self.h.project)).stdout)

    def test_omitted_must_cannot_be_hidden_by_verified_registered_work(self):
        h = self.h
        self.spec(f"# Must\n- {h.DEFAULT_ACCEPTANCE}\n- [DZ-MUST:R2] Delete the saved item\n")
        h.add_work()
        h.verify_default_work()
        coverage = self.report()["current_summary"]["requirement_coverage"]
        self.assertEqual(coverage["missing_work"], ["R2"])
        self.assertEqual(h.state()["run"]["product_verdict"], "partially_verified")
        self.assertTrue(any("every accepted Must" in error for error in
                            state_tool.stage_transition_errors(h.state(), "test", "deploy")))
        before = (h.project / ".dz/state.json").read_bytes()
        h.cli("close", str(h.project), "--verdict", "verified", "--reason", "synthetic audit", expected=1)
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), before)
        h.cli("close", str(h.project), "--verdict", "partially_verified", "--reason", "owner stops with R2 missing")
        h.cli("can-stop", str(h.project))

    def test_optional_or_cancelled_work_does_not_cover_required_outcome(self):
        h = self.h
        h.add_work(optional=True)
        self.assertEqual(self.report()["current_summary"]["requirement_coverage"]["missing_work"], ["R1"])
        h.add_work(item_id="required")
        h.cli("update-work", str(h.project), "required", "--status", "cancelled")
        self.assertEqual(self.report()["current_summary"]["requirement_coverage"]["missing_work"], ["R1"])

    def test_requirements_ignore_fenced_examples_but_reject_missing_or_duplicate_ids(self):
        h = self.h
        h.cli("set-decision", str(h.project), "intent", "--status", "draft")
        h.cli("set-decision", str(h.project), "intent", "--status", "accepted", "--by", "fixture", "--reference", "fixture")
        for content in ("# No list\n", "```markdown\n- [DZ-MUST:R1] Example only\n```\n",
                        "- [DZ-MUST:R1] One\n- [DZ-MUST:R1] Two\n", "- [DZ-MUST:R1]\n"):
            self.spec(content)
            h.cli("set-decision", str(h.project), "spec", "--status", "draft")
            h.cli("set-decision", str(h.project), "spec", "--status", "accepted", "--by", "fixture", "--reference", "fixture", expected=1)
        self.spec(f"```markdown\n- [DZ-MUST:IGNORE] Example\n```\n- {h.DEFAULT_ACCEPTANCE}\n")
        h.cli("set-decision", str(h.project), "spec", "--status", "draft")
        h.cli("set-decision", str(h.project), "spec", "--status", "accepted", "--by", "fixture", "--reference", "fixture")
        self.assertEqual([r["id"] for r in h.state()["requirements"]["items"]], ["R1"])

    def test_derived_index_cannot_drop_a_promise_without_changing_spec(self):
        h = self.h
        h.add_work()
        state = h.state()
        state["requirements"]["items"] = []
        # Deliberate corruption fixture, not a sanctioned update.
        (h.project / ".dz/state.json").write_text(json.dumps(state))
        result = h.cli("check", str(h.project), expected=1)
        self.assertIn("index differs", result.stderr)

    def change_plan(self):
        h = self.h
        h.write_project_file("docs/sdlc/plan-v2.md", "# New accepted route\nRetain existing behaviour; adjust implementation order.\n")
        h.cli("set-decision", str(h.project), "plan", "--status", "draft", "--path", "docs/sdlc/plan-v2.md")
        h.cli("set-decision", str(h.project), "plan", "--status", "accepted", "--by", "fixture", "--reference", "visible fixture v2")

    def test_carry_keeps_work_and_history_but_never_reuses_old_pass(self):
        h = self.h
        h.add_work()
        h.verify_default_work()
        evidence = copy.deepcopy(h.state()["evidence"])
        h.write_project_file("user-code.txt", "keep this later valid work\n")
        self.change_plan()
        self.assertEqual(self.report()["current_summary"]["work_to_reconcile"][0]["id"], "W1")
        h.cli("carry-work", str(h.project), "W1", "--disposition", "keep", "--reason", "current plan keeps this implementation")
        current = h.state()["work_items"][-1]
        self.assertEqual(current["carried_from"], "W1")
        self.assertEqual(current["title"], h.state()["work_items"][0]["title"])
        self.assertEqual(current["status"], "implemented_unverified")
        self.assertEqual(current["evidence_ids"], [])
        self.assertEqual(h.state()["evidence"], evidence)
        self.assertEqual((h.project / "user-code.txt").read_text(), "keep this later valid work\n")
        self.assertEqual(self.report()["current_summary"]["work_to_reconcile"], [])
        h.cli("update-work", str(h.project), current["id"], "--status", "verified", expected=1)
        h.cli("carry-work", str(h.project), "W1", "--disposition", "keep", "--reason", "duplicate", expected=1)
        h.cli("add-evidence", str(h.project), "--id", "E2", "--work-item", current["id"],
              "--acceptance", h.DEFAULT_ACCEPTANCE, "--kind", "test", "--claim", "synthetic current check",
              "--source", "regression fixture", *h.evidence_proof("E2", revision="rev-2"), "--result", "passed")
        h.cli("update-work", str(h.project), current["id"], "--status", "verified")
        self.assertTrue(self.report()["current_summary"]["requirement_coverage"]["complete"])
        h.cli("check", str(h.project))

    def test_changed_promise_requires_revised_work_and_retirement_stays_visible(self):
        h = self.h
        h.add_work()
        h.add_work(item_id="drop")
        new_promise = "[DZ-MUST:R1] A deliberately changed accepted outcome"
        h.write_project_file("docs/sdlc/spec-v2.md", "# Successor\n- " + new_promise + "\n")
        h.cli("set-decision", str(h.project), "spec", "--status", "draft", "--path", "docs/sdlc/spec-v2.md")
        h.cli("set-decision", str(h.project), "spec", "--status", "accepted", "--by", "fixture", "--reference", "changed promise")
        self.change_plan()
        h.cli("carry-work", str(h.project), "W1", "--disposition", "keep", "--reason", "wrongly unchanged", expected=1)
        h.cli("carry-work", str(h.project), "W1", "--disposition", "revise", "--acceptance", new_promise, "--reason", "accepted changed outcome")
        self.assertEqual(h.state()["work_items"][-1]["status"], "pending")
        h.cli("carry-work", str(h.project), "drop", "--disposition", "retire", "--reason", "not selected in current plan")
        self.assertEqual(self.report()["current_summary"]["work_to_reconcile"], [])
        self.assertEqual(h.state()["work_items"][1]["status"], "cancelled")

    def test_carry_is_atomic_and_does_not_upgrade_unfinished_implementation(self):
        h = self.h
        h.add_work()
        h.cli("update-work", str(h.project), "W1", "--status", "in_progress")
        self.change_plan()
        before = (h.project / ".dz/state.json").read_bytes()
        journal = (h.project / ".dz/journal.jsonl").read_bytes()
        h.cli("carry-work", str(h.project), "W1", "missing", "--disposition", "keep", "--reason", "fixture", expected=1)
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), before)
        self.assertEqual((h.project / ".dz/journal.jsonl").read_bytes(), journal)
        h.cli("carry-work", str(h.project), "W1", "--disposition", "keep", "--reason", "continue unfinished slice")
        self.assertEqual(h.state()["work_items"][-1]["status"], "in_progress")

    def test_carry_relinks_open_issue_without_losing_its_record(self):
        h = self.h
        h.add_work()
        h.cli("add-issue", str(h.project), "--id", "I1", "--title", "Input fails",
              "--kind", "implementation_gap", "--source", "synthetic fixture",
              "--expected", "input accepted", "--actual", "input rejected",
              "--impact", "core path fails", "--work-item", "W1")
        old_issue = h.state()["issues"][0]
        self.change_plan()
        h.cli("carry-work", str(h.project), "W1", "--disposition", "keep", "--reason", "same affected implementation")
        issue = h.state()["issues"][0]
        self.assertEqual(issue["work_item_id"], h.state()["work_items"][-1]["id"])
        self.assertEqual(issue["expected"], old_issue["expected"])
        self.assertEqual(issue["actual"], old_issue["actual"])
        self.assertEqual(issue["status"], "open")
        self.assertEqual(len(h.state()["issues"]), 1)
        h.cli("check", str(h.project))

    def test_legacy_plain_spec_upgrade_is_honest_and_never_rewrites_it(self):
        h = self.h
        h.accept_chain()
        plain = "# Accepted older specification\nAn older plain-language promise.\n"
        self.spec(plain)
        state = h.state()
        state["workflow_version"] = "2026-09-10.2"
        state.pop("requirements")
        state["decisions"]["spec"]["artifact_sha256"] = hashlib.sha256(plain.encode()).hexdigest()
        # Synthetic old-version snapshot plus matching journal; no real approval implied.
        (h.project / ".dz/state.json").write_text(json.dumps(state))
        with (h.project / ".dz/journal.jsonl").open("a") as handle:
            handle.write(json.dumps({"at": "synthetic legacy", "event": "fixture", "state": state}) + "\n")
        self.assertFalse(self.report()["current_summary"]["requirement_coverage"]["indexed"])
        h.cli("install-guidance", str(h.project))
        self.assertEqual((h.project / "docs/sdlc/spec.md").read_text(), plain)
        self.assertEqual(h.state()["requirements"]["items"], [])
        h.cli("set-run", str(h.project), "--status", "paused", "--resume-when", "visible successor review")
        h.cli("can-stop", str(h.project))


if __name__ == "__main__":
    unittest.main()
