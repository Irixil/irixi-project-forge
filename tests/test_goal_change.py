"""Goal corrections must update actual state, not merely response wording."""
import hashlib
import json
import unittest

import test_dz_state as fixtures


class GoalChangeTests(unittest.TestCase):
    def setUp(self):
        self.h = fixtures.DzStateTests()
        self.h.setUp()
        self.addCleanup(self.h.tearDown)
        self.h.add_work()
        self.h.cli("set-run", str(self.h.project), "--status", "active",
                   "--next-action", "Continue the obsolete automatic sending feature")

    def successor(self, name="intent"):
        h = self.h
        path = f"docs/sdlc/{name}-corrected.md"
        content = ("# User correction\n- [DZ-GOAL] The owner reviews reply drafts; nothing is sent automatically\n"
                   if name == "intent" else
                   "# Corrected plan\nBuild draft review only; do not connect a sending service.\n")
        h.write_project_file(path, content)
        return path, hashlib.sha256(content.encode()).hexdigest()

    def direct_change(self, name="intent", expected=0, digest=None):
        path, actual_digest = self.successor(name)
        return self.h.cli("set-decision", str(self.h.project), name, "--status", "accepted",
                          "--user-change", "--path", path, "--expected-sha256", digest or actual_digest,
                          "--by", "synthetic owner", "--reference", "fixture: explicitly replace sending with draft review",
                          expected=expected)

    def test_existing_acceptance_path_clears_obsolete_next_action(self):
        h = self.h
        path, _ = self.successor()
        h.cli("set-decision", str(h.project), "intent", "--status", "draft", "--path", path)
        h.cli("set-decision", str(h.project), "intent", "--status", "accepted",
              "--by", "synthetic owner", "--reference", "accepted visible change")
        self.assertNotIn("obsolete automatic sending", h.state()["run"]["next_action"] or "")

    def test_explicit_change_updates_goal_views_and_history_in_one_event(self):
        h = self.h
        h.verify_default_work()
        before = h.state()
        old_intent = (h.project / before["decisions"]["intent"]["path"]).read_bytes()
        h.write_project_file("existing-code.txt", "compatible code; keep it\n")
        old_events = (h.project / ".dz/journal.jsonl").read_text().splitlines()
        self.direct_change()
        current = h.state()
        self.assertIn("nothing is sent automatically", current["goal"]["statement"])
        self.assertEqual(len((h.project / ".dz/journal.jsonl").read_text().splitlines()), len(old_events) + 1)
        self.assertEqual(current["decisions"]["spec"]["status"], "superseded")
        self.assertEqual(current["decisions"]["plan"]["status"], "superseded")
        self.assertIsNone(current["target"]["id"])
        self.assertEqual(current["evidence"], before["evidence"])
        self.assertEqual((h.project / before["decisions"]["intent"]["path"]).read_bytes(), old_intent)
        self.assertEqual((h.project / "existing-code.txt").read_text(), "compatible code; keep it\n")
        report = json.loads(h.cli("resume-report", str(h.project)).stdout)
        self.assertEqual(report["current_summary"]["goal"]["statement"], current["goal"]["statement"])
        self.assertNotIn("obsolete automatic sending", json.dumps(report["current_summary"]["run"]))
        self.assertIn(current["goal"]["statement"], (h.project / "PROJECT.md").read_text())
        self.assertNotIn(before["goal"]["statement"], (h.project / "PROJECT.md").read_text())
        h.cli("update-work", str(h.project), "W1", "--status", "in_progress", expected=1)
        h.cli("check", str(h.project))

    def test_brainstorming_draft_does_not_replace_an_accepted_goal(self):
        h = self.h
        before = h.state()
        path, _ = self.successor()
        h.cli("set-decision", str(h.project), "intent", "--status", "draft", "--path", path)
        self.assertEqual(h.state()["goal"], before["goal"])
        self.assertEqual(h.state()["run"]["next_action"], before["run"]["next_action"])

    def test_wrong_digest_changes_neither_snapshot_nor_journal(self):
        h = self.h
        before = (h.project / ".dz/state.json").read_bytes()
        events = (h.project / ".dz/journal.jsonl").read_bytes()
        self.direct_change(expected=1, digest="0" * 64)
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), before)
        self.assertEqual((h.project / ".dz/journal.jsonl").read_bytes(), events)

    def test_method_change_keeps_final_goal_but_replaces_old_next_action(self):
        h = self.h
        before = h.state()
        self.direct_change(name="plan")
        self.assertEqual(h.state()["goal"], before["goal"])
        self.assertEqual(h.state()["decisions"]["spec"], before["decisions"]["spec"])
        self.assertNotIn("obsolete automatic sending", h.state()["run"]["next_action"] or "")

    def test_accepting_change_does_not_resume_a_paused_run(self):
        h = self.h
        h.cli("set-run", str(h.project), "--status", "paused", "--resume-when", "owner returns")
        self.direct_change()
        self.assertEqual(h.state()["run"]["status"], "paused")
        self.assertIsNone(h.state()["run"]["next_action"])
        h.cli("can-stop", str(h.project))

    def test_specification_change_refreshes_coverage_without_replacing_final_goal(self):
        h = self.h
        original_goal = h.state()["goal"]
        text = "# Explicitly changed scope\n- [DZ-MUST:R1] Show a draft without sending it\n"
        path = h.write_project_file("docs/sdlc/spec-corrected.md", text)
        h.cli("set-decision", str(h.project), "spec", "--status", "accepted", "--user-change",
              "--path", path, "--expected-sha256", hashlib.sha256(text.encode()).hexdigest(),
              "--by", "synthetic owner", "--reference", "fixture: draft-only scope")
        state = h.state()
        self.assertEqual(state["goal"], original_goal)
        self.assertEqual(state["requirements"]["items"][0]["acceptance"], "[DZ-MUST:R1] Show a draft without sending it")
        self.assertEqual(state["decisions"]["plan"]["status"], "superseded")
        self.assertNotIn("obsolete automatic sending", state["run"]["next_action"])
        h.cli("check", str(h.project))

    def test_direct_change_does_not_overwrite_history_or_invent_owner_approval(self):
        h = self.h
        old_path = h.state()["decisions"]["intent"]["path"]
        old_digest = h.state()["decisions"]["intent"]["artifact_sha256"]
        before = (h.project / ".dz/state.json").read_bytes()
        h.cli("set-decision", str(h.project), "intent", "--status", "accepted", "--user-change",
              "--path", old_path, "--expected-sha256", old_digest, "--by", "fixture",
              "--reference", "same path prohibited", expected=1)
        path, digest = self.successor()
        h.cli("set-decision", str(h.project), "intent", "--status", "accepted", "--user-change",
              "--path", path, "--expected-sha256", digest, expected=1)
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), before)

    def test_full_user_correction_reconciles_downstream_and_separates_old_work(self):
        h = self.h
        h.cli("update-work", str(h.project), "W1", "--note", "Obsolete instruction: build automatic sending next")
        self.direct_change()
        for name, text in (
            ("spec", "# Corrected specification\n- [DZ-MUST:R1] Owner reviews drafts without sending\n"),
            ("plan", "# Corrected plan\nKeep local entry; implement review only.\n"),
        ):
            path = h.write_project_file(f"docs/sdlc/{name}-corrected.md", text)
            h.cli("set-decision", str(h.project), name, "--status", "accepted", "--user-change",
                  "--path", path, "--expected-sha256", hashlib.sha256(text.encode()).hexdigest(),
                  "--by", "synthetic owner", "--reference", "same explicit correction; unchanged local boundary")
        h.cli("carry-work", str(h.project), "W1", "--disposition", "revise", "--reason", "explicit correction",
              "--title", "Build draft review", "--acceptance", "[DZ-MUST:R1] Owner reviews drafts without sending")
        s = h.state()
        self.assertEqual(s["work_items"][0]["status"], "pending")
        self.assertEqual(s["work_items"][1]["title"], "Build draft review")
        self.assertIn("Obsolete instruction", s["work_items"][0]["note"])
        self.assertNotIn("Obsolete instruction", s["work_items"][1]["note"])
        work_view = (h.project / "docs/sdlc/work-items.md").read_text()
        self.assertIn("| W1 | 历史，非当前待办 |", work_view)
        self.assertIn(f"| {s['work_items'][1]['id']} | 当前 |", work_view)
        report = json.loads(h.cli("resume-report", str(h.project)).stdout)
        self.assertEqual(report["current_summary"]["work_to_reconcile"], [])
        self.assertEqual(report["current_summary"]["work"]["open_items"][0]["title"], "Build draft review")
        h.cli("check", str(h.project))

    def test_direct_change_cannot_reuse_a_live_outside_action_lease(self):
        h = self.h
        h.cli("add-risk", str(h.project), "--id", "R1", "--title", "Synthetic send",
              "--level", "low", "--action-kind", "external_write", "--consequence", "outside effect",
              "--safer-option", "draft", "--scope", "send the old fixture", "--expires-at", h.FUTURE_EXPIRY)
        h.cli("decide-risk", str(h.project), "R1", "--decision", "accepted", "--by", "synthetic owner",
              "--reference", "fixture", "--next-action", "send the old fixture")
        before = (h.project / ".dz/state.json").read_bytes()
        self.direct_change(expected=1)
        self.assertEqual((h.project / ".dz/state.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
