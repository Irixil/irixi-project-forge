import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "dz_state.py"


class DzStateTests(unittest.TestCase):
    DEFAULT_ACCEPTANCE = "The observable result matches the accepted description"
    FUTURE_EXPIRY = "2099-01-01T00:00:00+00:00"

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name) / "demo"
        self.cli("init", str(self.project), "--name", "Demo")
        for decision in ("intent", "spec", "plan"):
            self.write_project_file(
                f"docs/sdlc/{decision}.md", f"# {decision}\n\nVisible draft for testing.\n"
            )

    def tearDown(self):
        self.temp.cleanup()

    def cli(self, *args, expected=0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected, result.stderr or result.stdout)
        return result

    def state(self):
        return json.loads((self.project / ".dz" / "state.json").read_text(encoding="utf-8"))

    def expire_authorized_lease(self, risk_id):
        state = self.state()
        risk = next(item for item in state["risks"] if item["id"] == risk_id)
        risk["expires_at"] = "2000-01-01T00:00:00+00:00"
        (self.project / ".dz" / "state.json").write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        with (self.project / ".dz" / "journal.jsonl").open(
            "a", encoding="utf-8"
        ) as handle:
            handle.write(
                json.dumps(
                    {"at": "lease elapsed", "event": "lease_elapsed", "state": state},
                    ensure_ascii=False,
                )
                + "\n"
            )

    def write_project_file(self, relative_path, content):
        path = self.project / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return relative_path

    def test_init_installs_refreshable_project_guidance_without_overwriting_other_rules(self):
        agents = self.project / "AGENTS.md"
        initial = agents.read_text(encoding="utf-8")
        self.assertIn("DZ-PROJECT-CONTINUITY:START", initial)
        self.assertIn("$HOME/.agents/skills/dz/SKILL.md", initial)

        agents.write_text("# Team rule\n\nKeep this.\n\n" + initial, encoding="utf-8")
        self.cli("install-guidance", str(self.project))
        self.cli("install-guidance", str(self.project))
        refreshed = agents.read_text(encoding="utf-8")
        self.assertIn("# Team rule\n\nKeep this.", refreshed)
        self.assertEqual(refreshed.count("DZ-PROJECT-CONTINUITY:START"), 1)
        self.assertEqual(refreshed.count("DZ-PROJECT-CONTINUITY:END"), 1)
        self.assertIn("saved `next_action` is an old proposal", refreshed)
        self.assertIn(
            "Do not make new project changes until the user confirms", refreshed
        )
        self.assertIn("resume-report", refreshed)
        self.assertIn("2026-09-05.3", refreshed)

    def test_resume_report_reads_all_journal_records_and_reports_uncertainty_without_git(self):
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_user",
            "--waiting-for",
            "the user's correction",
        )
        report = json.loads(self.cli("resume-report", str(self.project)).stdout)

        self.assertEqual(report["journal_records_reviewed"], len(report["journal_history"]))
        self.assertGreaterEqual(report["journal_records_reviewed"], 3)
        self.assertEqual(report["journal_history"][-1]["event"], "set_run:waiting_user")
        self.assertIsNone(report["workspace"]["changed_since_saved_record"])
        self.assertTrue(report["workspace"]["uncertainty"])
        self.assertTrue(
            report["takeover_rules"]["user_confirmation_required_before_new_mutation"]
        )

    def test_resume_report_detects_a_git_file_changed_after_the_saved_checkpoint(self):
        subprocess.run(["git", "init"], cwd=self.project, capture_output=True, check=True)
        subprocess.run(
            ["git", "config", "user.email", "dz-tests@example.invalid"],
            cwd=self.project,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "DZ tests"],
            cwd=self.project,
            capture_output=True,
            check=True,
        )
        self.write_project_file("app.txt", "saved version\n")
        subprocess.run(["git", "add", "."], cwd=self.project, capture_output=True, check=True)
        subprocess.run(
            ["git", "commit", "-m", "saved checkpoint"],
            cwd=self.project,
            capture_output=True,
            check=True,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_user",
            "--waiting-for",
            "the user's correction",
        )

        self.write_project_file("app.txt", "changed after save\n")
        report = json.loads(self.cli("resume-report", str(self.project)).stdout)

        self.assertTrue(report["workspace"]["changed_since_saved_record"])
        self.assertIn("app.txt", report["workspace"]["changed_paths"])
        self.assertIsNone(report["workspace"]["uncertainty"])

    def test_install_guidance_refreshes_an_old_workflow_version(self):
        state_path = self.project / ".dz" / "state.json"
        journal_path = self.project / ".dz" / "journal.jsonl"
        state = self.state()
        state["workflow_version"] = "2026-09-02.1"
        state.pop("issues")
        state_path.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        records = journal_path.read_text(encoding="utf-8").splitlines()
        latest = json.loads(records[-1])
        latest["state"]["workflow_version"] = "2026-09-02.1"
        latest["state"].pop("issues")
        records[-1] = json.dumps(latest, ensure_ascii=False, separators=(",", ":"))
        journal_path.write_text("\n".join(records) + "\n", encoding="utf-8")

        stale = self.cli("check", str(self.project), expected=1)
        self.assertIn("install-guidance", stale.stderr)
        self.cli("install-guidance", str(self.project))
        self.assertEqual(self.state()["workflow_version"], "2026-09-05.3")
        self.assertEqual(self.state()["issues"], [])
        self.cli("check", str(self.project))

    def evidence_proof(self, evidence_id, revision="rev-1", environment="test"):
        self.ensure_target(revision, environment)
        artifact = self.write_project_file(
            f"docs/sdlc/evidence/{evidence_id}.txt",
            f"Recorded output for {evidence_id}\n",
        )
        return (
            "--artifact",
            artifact,
            "--revision",
            revision,
            "--environment",
            environment,
        )

    def add_work(
        self, item_id="W1", title="Build the flow", optional=False, phase="build"
    ):
        self.accept_chain()
        args = [
            "add-work",
            str(self.project),
            "--id",
            item_id,
            "--title",
            title,
            "--phase",
            phase,
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
        ]
        if optional:
            args.append("--optional")
        self.cli(*args)

    def accept_chain(self):
        for decision in ("intent", "spec", "plan"):
            status = self.state()["decisions"][decision]["status"]
            if status == "accepted":
                continue
            if status != "draft":
                self.cli("set-decision", str(self.project), decision, "--status", "draft")
            self.cli(
                "set-decision",
                str(self.project),
                decision,
                "--status",
                "accepted",
                "--by",
                "project owner",
                "--reference",
                f"test acceptance for {decision}",
            )

    def ensure_target(self, revision="rev-1", environment="test"):
        self.accept_chain()
        current = self.state()["target"]
        if (
            current.get("revision") == revision
            and current.get("environment") == environment
        ):
            return
        proof = self.write_project_file(
            "docs/sdlc/evidence/current-target.txt",
            f"Observed target: {revision} in {environment}\n",
        )
        self.cli(
            "set-target",
            str(self.project),
            "--revision",
            revision,
            "--environment",
            environment,
            "--source",
            "test fixture target observation",
            "--artifact",
            proof,
        )

    def verify_default_work(self, evidence_id="E1", revision="rev-1"):
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            evidence_id,
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "The accepted behavior works",
            "--source",
            "python -m unittest recorded fixture",
            *self.evidence_proof(evidence_id, revision=revision),
            "--result",
            "passed",
        )
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified")

    def test_active_run_cannot_stop_until_it_waits_or_pauses(self):
        self.cli("can-stop", str(self.project), expected=2)
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "paused",
            "--resume-when",
            "User returns",
        )
        self.cli("can-stop", str(self.project))

    def test_user_can_close_with_unverified_work(self):
        self.add_work()
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.assertEqual(self.state()["run"]["product_verdict"], "implemented_unverified")
        self.cli(
            "close",
            str(self.project),
            "--verdict",
            "implemented_unverified",
            "--reason",
            "User chose to stop before testing",
        )
        self.assertEqual(self.state()["run"]["status"], "finished")
        self.assertEqual(self.state()["run"]["product_verdict"], "implemented_unverified")
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "in_progress",
            expected=1,
        )
        self.cli(
            "add-work",
            str(self.project),
            "--id",
            "W2",
            "--title",
            "Must not appear after closure",
            "--phase",
            "build",
            "--acceptance",
            "It remains absent",
            expected=1,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--next-action",
            "Resume the unfinished work",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")

    def test_verified_verdict_requires_passed_evidence(self):
        self.add_work()
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "verified",
            expected=1,
        )
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E1",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "The core path works",
            "--source",
            "python -m unittest",
            *self.evidence_proof("E1"),
            "--result",
            "passed",
        )
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "verified",
        )
        self.assertEqual(self.state()["run"]["product_verdict"], "verified")
        self.cli(
            "close",
            str(self.project),
            "--verdict",
            "verified",
            "--reason",
            "All required work has passed evidence",
        )

    def test_accepted_high_risk_does_not_block_work(self):
        self.ensure_target()
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R1",
            "--title",
            "Public release without rollback rehearsal",
            "--level",
            "critical",
            "--action-kind",
            "public_release",
            "--consequence",
            "Recovery may take longer",
            "--safer-option",
            "Rehearse rollback first",
            "--scope",
            "release v1 to staging",
            "--expires-at",
            self.FUTURE_EXPIRY,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_authorization",
            "--waiting-for",
            "Whether to accept R1 and continue",
            "--pending-risk",
            "R1",
        )
        self.cli(
            "decide-risk",
            str(self.project),
            "R1",
            "--decision",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "conversation turn 12",
            "--next-action",
            "release v1 to staging",
        )
        self.assertEqual(self.state()["risks"][0]["decision"], "accepted")
        self.assertEqual(self.state()["run"]["status"], "active")
        self.assertIsNone(self.state()["run"]["pending_risk_id"])
        self.cli("can-stop", str(self.project), expected=2)
        self.cli(
            "decide-risk",
            str(self.project),
            "R1",
            "--decision",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "duplicate decision",
            "--next-action",
            "Do not run",
            expected=1,
        )

    def test_recover_uses_last_valid_journal_snapshot(self):
        self.add_work(title="Keep this")
        state_path = self.project / ".dz" / "state.json"
        state_path.write_text("{broken", encoding="utf-8")
        self.cli("recover", str(self.project))
        self.assertEqual(self.state()["work_items"][0]["id"], "W1")

    def test_recover_preserves_but_supersedes_changed_decision_artifact(self):
        self.cli("set-decision", str(self.project), "intent", "--status", "draft")
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "visible acceptance",
        )
        self.accept_chain()
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--stage",
            "design",
            "--next-action",
            "Prepare the design work",
        )
        self.write_project_file(
            "docs/sdlc/intent.md", "# Changed after the recorded acceptance\n"
        )
        (self.project / ".dz" / "state.json").write_text("{broken", encoding="utf-8")
        self.cli("recover", str(self.project))
        decision = self.state()["decisions"]["intent"]
        self.assertEqual(decision["status"], "superseded")
        self.assertEqual(decision["accepted_by"], "project owner")
        self.assertEqual(self.state()["run"]["stage"], "discovery")
        self.cli("check", str(self.project))

    def test_generated_views_come_from_state(self):
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "accepted",
            expected=1,
        )
        self.cli("set-decision", str(self.project), "intent", "--status", "draft")
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "test acceptance for intent",
        )
        self.add_work(title="Visible task")
        self.assertEqual(self.state()["decisions"]["intent"]["status"], "accepted")
        self.assertIn("Visible task", (self.project / "docs" / "sdlc" / "work-items.md").read_text())
        self.assertTrue((self.project / "PROJECT.md").is_file())

    def test_issue_is_routed_and_returned_by_resume_report(self):
        routes = {
            "implementation_gap": "work_item",
            "specification_gap": "spec",
            "plan_gap": "plan",
            "new_idea": "backlog",
            "intent_conflict": "intent",
            "production_feedback": "feedback",
        }
        for index, (kind, route) in enumerate(routes.items(), start=1):
            self.cli(
                "add-issue",
                str(self.project),
                "--id",
                f"I{index}",
                "--title",
                "Refresh behavior was never agreed"
                if kind == "specification_gap"
                else kind,
                "--kind",
                kind,
                "--source",
                "tester reproduced the missing state",
                "--expected",
                "the user knows what should happen",
                "--actual",
                "the current records or product disagree",
                "--impact",
                "users may not get the expected result",
            )
            issue = self.state()["issues"][-1]
            self.assertEqual(issue["route"], route)
            self.assertEqual(issue["status"], "open")
        issue_view = (self.project / "docs" / "sdlc" / "issues.md").read_text()
        self.assertIn("Refresh behavior was never agreed", issue_view)

        report = json.loads(self.cli("resume-report", str(self.project)).stdout)
        self.assertEqual(
            {item["id"] for item in report["unresolved_issues"]},
            {f"I{index}" for index in range(1, 7)},
        )
        self.assertTrue(
            any("I1" in entry.get("issue_changes", {}) for entry in report["journal_history"])
        )
        self.assertTrue(
            report["takeover_rules"]["review_unresolved_issues_and_later_issue_changes"]
        )

    def test_issue_cannot_be_called_verified_without_proof_and_prevention(self):
        self.add_work()
        self.cli(
            "add-issue",
            str(self.project),
            "--id",
            "I1",
            "--title",
            "Accepted button action fails",
            "--kind",
            "implementation_gap",
            "--source",
            "manual test",
            "--expected",
            "the accepted action succeeds",
            "--actual",
            "the action returns an error",
            "--impact",
            "the user cannot finish the flow",
            "--work-item",
            "W1",
        )
        self.cli("update-issue", str(self.project), "I1", "--status", "triaged")
        self.cli("update-issue", str(self.project), "I1", "--status", "in_progress")
        self.cli(
            "update-issue",
            str(self.project),
            "I1",
            "--status",
            "implemented_unverified",
            "--resolution",
            "Handled the failing response",
        )
        failed = self.cli(
            "update-issue",
            str(self.project),
            "I1",
            "--status",
            "verified",
            expected=1,
        )
        self.assertIn("regression protection", failed.stderr)
        self.assertEqual(self.state()["issues"][0]["status"], "implemented_unverified")

        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E1",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "regression test",
            "--claim",
            "The failure stays fixed",
            "--source",
            "python -m unittest issue_regression",
            *self.evidence_proof("E1"),
            "--result",
            "passed",
        )
        self.cli(
            "update-issue",
            str(self.project),
            "I1",
            "--status",
            "verified",
            "--evidence",
            "E1",
            "--prevention",
            "A repeatable regression test now covers the failure",
        )
        issue = self.state()["issues"][0]
        self.assertEqual(issue["status"], "verified")
        self.assertEqual(issue["evidence_ids"], ["E1"])

    def test_verified_close_cannot_hide_a_known_implementation_gap(self):
        self.add_work()
        self.verify_default_work()
        self.cli(
            "add-issue",
            str(self.project),
            "--id",
            "I1",
            "--title",
            "Known accepted path is broken",
            "--kind",
            "implementation_gap",
            "--source",
            "user report with reproduction",
            "--expected",
            "the accepted path succeeds",
            "--actual",
            "the accepted path fails",
            "--impact",
            "the user cannot finish",
            "--work-item",
            "W1",
        )
        result = self.cli(
            "close",
            str(self.project),
            "--verdict",
            "verified",
            "--reason",
            "Attempted verified close",
            expected=1,
        )
        self.assertIn("cannot hide unresolved material issues", result.stderr)
        self.assertEqual(self.state()["run"]["product_verdict"], "partially_verified")
        self.cli(
            "close",
            str(self.project),
            "--verdict",
            "partially_verified",
            "--reason",
            "User chose to stop with the issue still open",
        )
        self.assertEqual(self.state()["run"]["status"], "finished")

    def test_acceptance_is_required_and_optional_work_cannot_verify_product(self):
        self.cli(
            "add-work",
            str(self.project),
            "--id",
            "W0",
            "--title",
            "No acceptance",
            expected=2,
        )
        self.add_work(optional=True)
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E1",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "Optional result works",
            "--source",
            "python -m unittest optional_path",
            *self.evidence_proof("E1"),
            "--result",
            "passed",
        )
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified")
        self.accept_chain()
        self.cli(
            "close",
            str(self.project),
            "--verdict",
            "verified",
            "--reason",
            "Optional work alone is not the product",
            expected=1,
        )

    def test_failed_evidence_downgrades_until_a_pass_resolves_it(self):
        self.accept_chain()
        self.add_work()
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E1",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "Core path initially works",
            "--source",
            "python -m unittest core_path",
            *self.evidence_proof("E1"),
            "--result",
            "passed",
        )
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E2",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "regression",
            "--claim",
            "A later regression fails",
            "--source",
            "python -m unittest regression_path",
            *self.evidence_proof("E2"),
            "--result",
            "failed",
        )
        self.assertEqual(self.state()["work_items"][0]["status"], "implemented_unverified")
        self.cli("update-work", str(self.project), "W1", "--status", "verified", expected=1)
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E3",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "regression",
            "--claim",
            "The regression passes after the fix",
            "--source",
            "python -m unittest regression_path",
            *self.evidence_proof("E3"),
            "--result",
            "passed",
            "--resolves",
            "E2",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified")

    def test_decisions_require_order_and_upstream_change_supersedes_downstream(self):
        self.cli("set-decision", str(self.project), "spec", "--status", "draft", expected=1)
        self.cli("set-decision", str(self.project), "plan", "--status", "draft", expected=1)
        self.accept_chain()
        self.cli("set-decision", str(self.project), "intent", "--status", "superseded")
        decisions = self.state()["decisions"]
        self.assertEqual(decisions["intent"]["status"], "superseded")
        self.assertEqual(decisions["spec"]["status"], "superseded")
        self.assertEqual(decisions["plan"]["status"], "superseded")
        self.cli("set-decision", str(self.project), "intent", "--status", "draft")
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "replacement intent acceptance",
        )
        self.assertEqual(self.state()["decisions"]["spec"]["status"], "superseded")

    def test_recover_skips_an_incomplete_utf8_tail(self):
        self.add_work(title="Survive journal damage")
        journal = self.project / ".dz" / "journal.jsonl"
        with journal.open("ab") as handle:
            handle.write(b"\xe4")
        (self.project / ".dz" / "state.json").write_text("{broken", encoding="utf-8")
        self.cli("recover", str(self.project))
        self.assertEqual(self.state()["work_items"][0]["title"], "Survive journal damage")

    def test_check_rejects_missing_fields_and_blocked_requires_kind(self):
        state = self.state()
        del state["run"]["stage"]
        (self.project / ".dz" / "state.json").write_text(json.dumps(state), encoding="utf-8")
        self.cli("check", str(self.project), expected=1)
        self.cli("recover", str(self.project))
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "blocked",
            "--blocker",
            "Missing account",
            "--resume-when",
            "Account is available",
            expected=1,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "blocked",
            "--blocker",
            "Missing account",
            "--blocker-kind",
            "missing_authority",
            "--resume-when",
            "Account is available",
        )

    def test_every_acceptance_criterion_needs_passed_evidence(self):
        first = "The upload succeeds"
        second = "A failed upload can be retried"
        self.accept_chain()
        self.cli(
            "add-work",
            str(self.project),
            "--id",
            "W1",
            "--title",
            "Upload a file",
            "--phase",
            "build",
            "--acceptance",
            first,
            "--acceptance",
            second,
        )
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E1",
            "--work-item",
            "W1",
            "--acceptance",
            first,
            "--kind",
            "test",
            "--claim",
            "Upload succeeds",
            "--source",
            "python -m unittest upload_success",
            *self.evidence_proof("E1"),
            "--result",
            "passed",
        )
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified", expected=1)
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E2",
            "--work-item",
            "W1",
            "--acceptance",
            second,
            "--kind",
            "test",
            "--claim",
            "Retry succeeds after an upload failure",
            "--source",
            "python -m unittest upload_retry",
            *self.evidence_proof("E2"),
            "--result",
            "passed",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified")

    def test_evidence_resolves_only_the_same_acceptance_criterion(self):
        first = "Lint passes"
        second = "The browser flow passes"
        self.accept_chain()
        self.cli(
            "add-work",
            str(self.project),
            "--id",
            "W1",
            "--title",
            "Check the page",
            "--phase",
            "test",
            "--acceptance",
            first,
            "--acceptance",
            second,
        )
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E1",
            "--work-item",
            "W1",
            "--acceptance",
            second,
            "--kind",
            "browser",
            "--claim",
            "The browser flow fails",
            "--source",
            "playwright test core-flow",
            *self.evidence_proof("E1"),
            "--result",
            "failed",
        )
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E2",
            "--work-item",
            "W1",
            "--acceptance",
            first,
            "--kind",
            "lint",
            "--claim",
            "Lint passes",
            "--source",
            "npm run lint",
            *self.evidence_proof("E2"),
            "--result",
            "passed",
            "--resolves",
            "E1",
            expected=1,
        )

    def test_old_target_cannot_resolve_a_new_target_failure(self):
        self.add_work()
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E1",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "Old revision passes",
            "--source",
            "test command",
            *self.evidence_proof("E1", revision="rev-old"),
            "--result",
            "passed",
        )
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E2",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "New revision fails",
            "--source",
            "test command",
            *self.evidence_proof("E2", revision="rev-new"),
            "--result",
            "failed",
        )
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E3",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "Old revision is rerun",
            "--source",
            "test command",
            *self.evidence_proof("E3", revision="rev-old"),
            "--result",
            "passed",
            "--resolves",
            "E2",
            expected=1,
        )
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E4",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "New revision passes after correction",
            "--source",
            "test command",
            *self.evidence_proof("E4", revision="rev-new"),
            "--result",
            "passed",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified")

    def test_accepted_decision_path_cannot_change_in_place(self):
        self.write_project_file("docs/sdlc/intent-v1.md", "# Intent v1\n")
        self.write_project_file("docs/sdlc/intent-v2.md", "# Intent v2\n")
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "draft",
            "--path",
            "docs/sdlc/intent-v1.md",
        )
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "accepted intent v1",
        )
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "accepted",
            "--path",
            "docs/sdlc/intent-v2.md",
            expected=1,
        )
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "superseded",
            "--path",
            "docs/sdlc/intent-v2.md",
            expected=1,
        )
        self.cli("set-decision", str(self.project), "intent", "--status", "superseded")
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "draft",
            "--path",
            "docs/sdlc/intent-v2.md",
        )

    def test_pending_risk_authorization_cannot_be_bypassed(self):
        self.ensure_target()
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R1",
            "--title",
            "Risk R1",
            "--level",
            "critical",
            "--action-kind",
            "public_release",
            "--consequence",
            "A public action may fail",
            "--safer-option",
            "Run one more rehearsal",
            "--scope",
            "release R1",
            "--expires-at",
            self.FUTURE_EXPIRY,
        )
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R2",
            "--title",
            "Risk R2",
            "--level",
            "critical",
            "--action-kind",
            "public_release",
            "--consequence",
            "A public action may fail",
            "--safer-option",
            "Run one more rehearsal",
            "--scope",
            "release R2",
            "--expires-at",
            self.FUTURE_EXPIRY,
            expected=1,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_authorization",
            "--waiting-for",
            "Whether to accept R1",
            "--pending-risk",
            "R1",
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--next-action",
            "Bypass R1",
            expected=1,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_authorization",
            "--waiting-for",
            "Switch to R2",
            "--pending-risk",
            "R2",
            expected=1,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "paused",
            "--resume-when",
            "Owner returns",
        )
        self.assertTrue(self.state()["risks"][0]["authorization_pending"])
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--next-action",
            "Bypass after pause",
            expected=1,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_authorization",
            "--waiting-for",
            "Whether to accept R1",
            "--pending-risk",
            "R1",
        )
        self.cli(
            "decide-risk",
            str(self.project),
            "R1",
            "--decision",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "informed decision",
            "--next-action",
            "release R1",
        )
        self.assertEqual(self.state()["run"]["status"], "active")

    def test_action_kind_controls_authorization_even_when_severity_is_low(self):
        scope = "send one staging notification"
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R1",
            "--title",
            "External notification",
            "--level",
            "low",
            "--action-kind",
            "external_write",
            "--consequence",
            "Another system receives a message",
            "--safer-option",
            "Preview the message first",
            "--scope",
            scope,
            "--expires-at",
            self.FUTURE_EXPIRY,
        )
        self.assertEqual(self.state()["run"]["status"], "waiting_authorization")

        tampered = self.state()
        tampered["risks"][0]["authorization_pending"] = False
        tampered["risks"][0]["action_status"] = "not_applicable"
        tampered["run"].update(
            {
                "status": "active",
                "next_action": scope,
                "waiting_for": None,
                "pending_risk_id": None,
            }
        )
        (self.project / ".dz" / "state.json").write_text(
            json.dumps(tampered), encoding="utf-8"
        )
        with (self.project / ".dz" / "journal.jsonl").open(
            "a", encoding="utf-8"
        ) as handle:
            handle.write(
                json.dumps({"at": "tampered", "event": "tampered", "state": tampered})
                + "\n"
            )
        result = self.cli("check", str(self.project), expected=1)
        self.assertIn("actionable risk", result.stderr)
        self.cli("recover", str(self.project))

        self.cli(
            "decide-risk",
            str(self.project),
            "R1",
            "--decision",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "approved exact notification",
            "--next-action",
            scope,
        )
        self.cli(
            "complete-risk-action",
            str(self.project),
            "R1",
            "--outcome",
            "completed",
            "--reference",
            "notification receipt",
            "--next-action",
            "review the receipt",
        )
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R2",
            "--title",
            "Informational observation",
            "--level",
            "critical",
            "--action-kind",
            "informational",
            "--consequence",
            "A known limitation remains visible",
            "--safer-option",
            "Track it in maintenance",
            "--scope",
            "record the limitation only",
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_authorization",
            "--waiting-for",
            "Authorize an informational note",
            "--pending-risk",
            "R2",
            expected=1,
        )

    def test_ids_are_canonical_and_cannot_hide_required_work(self):
        self.add_work()
        result = self.cli(
            "add-work",
            str(self.project),
            "--id",
            " W2 ",
            "--title",
            "Hidden work",
            "--phase",
            "build",
            "--acceptance",
            "Must be proved",
            expected=1,
        )
        self.assertIn("whitespace", result.stderr)

        state = self.state()
        hidden = dict(state["work_items"][0])
        hidden.update(
            {
                "id": " W1 ",
                "title": "Unproven hidden required work",
                "status": "verified",
                "acceptance": ["This criterion has no evidence"],
                "evidence_ids": [],
            }
        )
        state["work_items"].insert(0, hidden)
        (self.project / ".dz" / "state.json").write_text(
            json.dumps(state), encoding="utf-8"
        )
        result = self.cli("check", str(self.project), expected=1)
        self.assertIn("whitespace", result.stderr)
        self.cli("recover", str(self.project))

    def test_deleted_evidence_is_restored_from_append_only_journal(self):
        self.add_work()
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        for evidence_id, result in (("E1", "passed"), ("E2", "failed")):
            self.cli(
                "add-evidence",
                str(self.project),
                "--id",
                evidence_id,
                "--work-item",
                "W1",
                "--acceptance",
                self.DEFAULT_ACCEPTANCE,
                "--kind",
                "test",
                "--claim",
                f"Evidence {evidence_id}",
                "--source",
                "test command",
                *self.evidence_proof(evidence_id),
                "--result",
                result,
            )
            if evidence_id == "E1":
                self.cli(
                    "update-work",
                    str(self.project),
                    "W1",
                    "--status",
                    "implemented_unverified",
                )
                self.cli(
                    "update-work", str(self.project), "W1", "--status", "verified"
                )
        state = self.state()
        state["evidence"] = [item for item in state["evidence"] if item["id"] != "E2"]
        state["work_items"][0]["evidence_ids"].remove("E2")
        (self.project / ".dz" / "state.json").write_text(
            json.dumps(state), encoding="utf-8"
        )
        result = self.cli("check", str(self.project), expected=1)
        self.assertIn("latest journal snapshot", result.stderr)
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
            expected=1,
        )
        self.cli("recover", str(self.project))
        restored = self.state()
        self.assertEqual([item["id"] for item in restored["evidence"]], ["E1", "E2"])
        self.assertEqual(
            restored["work_items"][0]["status"], "implemented_unverified"
        )

    def test_pending_authorization_survives_close_and_resume(self):
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R1",
            "--title",
            "Release risk",
            "--level",
            "high",
            "--action-kind",
            "public_release",
            "--consequence",
            "The release may fail",
            "--safer-option",
            "Rehearse first",
            "--scope",
            "release revision one",
            "--expires-at",
            self.FUTURE_EXPIRY,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_authorization",
            "--waiting-for",
            "Whether to continue",
            "--pending-risk",
            "R1",
        )
        self.cli(
            "close",
            str(self.project),
            "--verdict",
            "cancelled",
            "--reason",
            "User stopped this run",
        )
        self.assertTrue(self.state()["risks"][0]["authorization_pending"])
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--next-action",
            "Resume release",
            expected=1,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_authorization",
            "--waiting-for",
            "Decide R1 before resuming",
            "--pending-risk",
            "R1",
        )

    def test_decision_artifact_and_acceptance_record_are_locked(self):
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "draft",
            "--path",
            "docs/sdlc/missing.md",
            expected=1,
        )
        self.cli("set-decision", str(self.project), "intent", "--status", "draft")
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "accepted",
            expected=1,
        )
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "visible draft accepted",
        )
        self.write_project_file("docs/sdlc/intent.md", "# Changed without acceptance\n")
        self.cli("check", str(self.project), expected=1)
        self.cli("set-decision", str(self.project), "intent", "--status", "superseded")
        self.cli("set-decision", str(self.project), "intent", "--status", "draft")
        self.cli(
            "set-decision",
            str(self.project),
            "intent",
            "--status",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "replacement draft accepted",
        )
        self.cli("check", str(self.project))

    def test_passed_evidence_requires_intact_artifact_and_revision(self):
        self.add_work()
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E0",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "Unsupported claim",
            "--source",
            "plausible words only",
            "--result",
            "passed",
            expected=2,
        )
        empty = self.write_project_file("docs/sdlc/evidence/empty.txt", "")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E0",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "Empty proof",
            "--source",
            "test command",
            "--artifact",
            empty,
            "--revision",
            "rev-1",
            "--environment",
            "test",
            "--result",
            "passed",
            expected=1,
        )
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E1",
            "--work-item",
            "W1",
            "--acceptance",
            self.DEFAULT_ACCEPTANCE,
            "--kind",
            "test",
            "--claim",
            "Real proof",
            "--source",
            "test command",
            *self.evidence_proof("E1"),
            "--result",
            "passed",
        )
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified")
        self.write_project_file(
            "docs/sdlc/evidence/E1.txt", "Changed after it was recorded\n"
        )
        self.cli("check", str(self.project), expected=1)
        self.cli(
            "close",
            str(self.project),
            "--verdict",
            "cancelled",
            "--reason",
            "User may still stop",
        )
        self.assertEqual(
            self.state()["work_items"][0]["status"], "implemented_unverified"
        )

    def test_verified_criteria_must_share_one_revision(self):
        first = "First behavior passes"
        second = "Second behavior passes"
        self.accept_chain()
        self.cli(
            "add-work",
            str(self.project),
            "--id",
            "W1",
            "--title",
            "Two behaviors",
            "--phase",
            "test",
            "--acceptance",
            first,
            "--acceptance",
            second,
        )
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        for evidence_id, criterion, revision in (
            ("E1", first, "rev-1"),
            ("E2", second, "rev-2"),
        ):
            self.cli(
                "add-evidence",
                str(self.project),
                "--id",
                evidence_id,
                "--work-item",
                "W1",
                "--acceptance",
                criterion,
                "--kind",
                "test",
                "--claim",
                f"{criterion} on {revision}",
                "--source",
                "test command",
                *self.evidence_proof(evidence_id, revision=revision),
                "--result",
                "passed",
            )
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified", expected=1)
        self.cli(
            "add-evidence",
            str(self.project),
            "--id",
            "E3",
            "--work-item",
            "W1",
            "--acceptance",
            first,
            "--kind",
            "test",
            "--claim",
            "First behavior also passes on rev-2",
            "--source",
            "test command",
            *self.evidence_proof("E3", revision="rev-2"),
            "--result",
            "passed",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified")

    def test_run_state_fields_are_mutually_consistent(self):
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--next-action",
            "Keep working",
            "--waiting-for",
            "User reply",
            expected=1,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "waiting_user",
            "--waiting-for",
            "User reply",
            "--blocker",
            "Not actually blocked",
            expected=1,
        )

    def test_recover_skips_a_structurally_malformed_journal_record(self):
        self.add_work()
        malformed = self.state()
        malformed["work_items"][0]["id"] = []
        journal = self.project / ".dz" / "journal.jsonl"
        with journal.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"at": "bad", "event": "bad", "state": malformed}) + "\n")
        (self.project / ".dz" / "state.json").write_text("{broken", encoding="utf-8")
        self.cli("recover", str(self.project))
        self.assertEqual(self.state()["work_items"][0]["id"], "W1")

    def test_recover_downgrades_a_finished_verdict_when_proof_changes(self):
        self.add_work()
        self.verify_default_work()
        self.cli(
            "close",
            str(self.project),
            "--verdict",
            "verified",
            "--reason",
            "All recorded criteria passed",
        )
        self.write_project_file("docs/sdlc/evidence/E1.txt", "Changed later\n")
        (self.project / ".dz" / "state.json").write_text("{broken", encoding="utf-8")
        self.cli("recover", str(self.project))
        recovered = self.state()
        self.assertEqual(recovered["run"]["status"], "finished")
        self.assertEqual(
            recovered["run"]["product_verdict"], "implemented_unverified"
        )
        self.cli("check", str(self.project))

    def test_delivery_stage_cannot_skip_decisions_or_exit_evidence(self):
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--stage",
            "deploy",
            "--next-action",
            "Ship now",
            expected=1,
        )
        self.accept_chain()
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--stage",
            "design",
            "--next-action",
            "Complete the design work",
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--stage",
            "build",
            "--next-action",
            "Build",
            expected=1,
        )
        self.add_work(phase="design")
        self.verify_default_work()
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--stage",
            "build",
            "--next-action",
            "Build the first slice",
        )

    def test_changed_decision_contract_does_not_reuse_old_verified_work(self):
        self.add_work()
        self.verify_default_work()
        old_contract = self.state()["work_items"][0]["contract_sha256"]
        self.cli("set-decision", str(self.project), "intent", "--status", "superseded")
        self.assertIsNone(self.state()["target"]["id"])
        self.write_project_file("docs/sdlc/intent.md", "# Expanded intent v2\n")
        self.accept_chain()
        state = self.state()
        current_contract = hashlib.sha256(
            "\0".join(
                state["decisions"][name]["artifact_sha256"]
                for name in ("intent", "spec", "plan")
            ).encode("ascii")
        ).hexdigest()
        self.assertEqual(state["work_items"][0]["status"], "implemented_unverified")
        self.assertNotEqual(old_contract, current_contract)
        self.assertNotEqual(state["target"].get("contract_sha256"), current_contract)
        self.assertEqual(state["run"]["product_verdict"], "not_assessed")

    def test_resetting_same_revision_creates_a_fresh_target_epoch(self):
        self.add_work()
        self.verify_default_work()
        first_target = self.state()["target"]["id"]
        self.cli("update-work", str(self.project), "W1", "--status", "in_progress")
        self.assertIsNone(self.state()["target"]["id"])
        self.cli(
            "update-work",
            str(self.project),
            "W1",
            "--status",
            "implemented_unverified",
        )
        self.cli("update-work", str(self.project), "W1", "--status", "verified", expected=1)
        proof = self.write_project_file(
            "docs/sdlc/evidence/current-target.txt",
            "A fresh deployment of rev-1 in test\n",
        )
        self.cli(
            "set-target",
            str(self.project),
            "--revision",
            "rev-1",
            "--environment",
            "test",
            "--source",
            "fresh deployment observation",
            "--artifact",
            proof,
        )
        state = self.state()
        self.assertNotEqual(first_target, state["target"]["id"])
        self.assertEqual(state["work_items"][0]["status"], "implemented_unverified")
        self.cli("update-work", str(self.project), "W1", "--status", "verified", expected=1)

    def test_declined_risk_cannot_be_resumed_as_the_same_action(self):
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R1",
            "--title",
            "Destructive production action",
            "--level",
            "critical",
            "--action-kind",
            "delete",
            "--consequence",
            "Production data would be removed",
            "--safer-option",
            "Export and review a deletion list",
            "--scope",
            "delete production database",
            "--expires-at",
            self.FUTURE_EXPIRY,
        )
        self.cli(
            "decide-risk",
            str(self.project),
            "R1",
            "--decision",
            "declined",
            "--by",
            "project owner",
            "--reference",
            "explicit no",
        )
        self.assertEqual(self.state()["run"]["status"], "waiting_user")
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--next-action",
            "delete production database",
            expected=1,
        )

    def test_authorized_risk_scope_is_leased_until_outcome(self):
        self.ensure_target()
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R1",
            "--title",
            "Staging release",
            "--level",
            "high",
            "--action-kind",
            "public_release",
            "--consequence",
            "A bad revision may be visible",
            "--safer-option",
            "Run a staging smoke test",
            "--scope",
            "release rev-1 to staging",
            "--expires-at",
            self.FUTURE_EXPIRY,
        )
        self.cli(
            "decide-risk",
            str(self.project),
            "R1",
            "--decision",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "accepted exact staging action",
            "--next-action",
            "release rev-1 to staging",
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "active",
            "--next-action",
            "release rev-99 to production",
            expected=1,
        )
        self.cli(
            "set-target",
            str(self.project),
            "--revision",
            "rev-99",
            "--environment",
            "production",
            "--source",
            "different deployment observation",
            "--artifact",
            "docs/sdlc/evidence/current-target.txt",
            expected=1,
        )
        self.cli(
            "set-decision",
            str(self.project),
            "plan",
            "--status",
            "superseded",
            expected=1,
        )
        self.cli(
            "close",
            str(self.project),
            "--verdict",
            "cancelled",
            "--reason",
            "User closed DZ while the outside action outcome was still unknown",
        )
        self.cli(
            "complete-risk-action",
            str(self.project),
            "R1",
            "--outcome",
            "completed",
            "--reference",
            "deployment record 1",
        )
        state = self.state()
        self.assertIsNone(state["run"]["authorized_risk_id"])
        self.assertEqual(state["run"]["status"], "finished")
        self.assertEqual(state["run"]["product_verdict"], "cancelled")

    def test_expired_active_lease_blocks_checks_and_execution_results(self):
        scope = "send one staging notification"
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R1",
            "--title",
            "External notification",
            "--level",
            "high",
            "--action-kind",
            "external_write",
            "--consequence",
            "Another system receives a message",
            "--safer-option",
            "Preview the exact message",
            "--scope",
            scope,
            "--expires-at",
            self.FUTURE_EXPIRY,
        )
        self.cli(
            "decide-risk",
            str(self.project),
            "R1",
            "--decision",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "approved exact notification",
            "--next-action",
            scope,
        )
        self.expire_authorized_lease("R1")

        check = self.cli("check", str(self.project), expected=1)
        self.assertIn("expired", check.stderr)
        can_stop = self.cli("can-stop", str(self.project), expected=2)
        self.assertIn("expired", can_stop.stdout)
        for outcome in ("completed", "failed"):
            result = self.cli(
                "complete-risk-action",
                str(self.project),
                "R1",
                "--outcome",
                outcome,
                "--reference",
                f"untrusted {outcome} claim",
                "--next-action",
                "continue without fresh authorization",
                expected=1,
            )
            self.assertIn("expired", result.stderr)

        unchanged = self.state()
        self.assertEqual(unchanged["run"]["status"], "active")
        self.assertEqual(unchanged["run"]["authorized_risk_id"], "R1")
        self.assertEqual(unchanged["risks"][0]["action_status"], "authorized")
        self.assertIsNone(unchanged["risks"][0]["action_reference"])

        self.cli(
            "complete-risk-action",
            str(self.project),
            "R1",
            "--outcome",
            "cancelled",
            "--reference",
            "expired before execution",
            "--next-action",
            "request a fresh exact authorization",
        )
        released = self.state()
        self.assertIsNone(released["run"]["authorized_risk_id"])
        self.assertEqual(released["risks"][0]["action_status"], "cancelled")
        self.assertEqual(
            released["risks"][0]["expires_at"], "2000-01-01T00:00:00+00:00"
        )
        self.cli("check", str(self.project))

        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R2",
            "--title",
            "Fresh external notification",
            "--level",
            "high",
            "--action-kind",
            "external_write",
            "--consequence",
            "Another system receives the new message",
            "--safer-option",
            "Preview the new exact message",
            "--scope",
            "send the newly reviewed staging notification",
            "--expires-at",
            self.FUTURE_EXPIRY,
        )
        fresh = self.state()
        self.assertEqual(fresh["run"]["status"], "waiting_authorization")
        self.assertEqual(fresh["run"]["pending_risk_id"], "R2")

    def test_expired_lease_preserves_paused_and_finished_history(self):
        scope = "send one staging notification"
        self.cli(
            "add-risk",
            str(self.project),
            "--id",
            "R1",
            "--title",
            "External notification",
            "--level",
            "high",
            "--action-kind",
            "external_write",
            "--consequence",
            "Another system receives a message",
            "--safer-option",
            "Preview the exact message",
            "--scope",
            scope,
            "--expires-at",
            self.FUTURE_EXPIRY,
        )
        self.cli(
            "decide-risk",
            str(self.project),
            "R1",
            "--decision",
            "accepted",
            "--by",
            "project owner",
            "--reference",
            "approved exact notification",
            "--next-action",
            scope,
        )
        self.cli(
            "set-run",
            str(self.project),
            "--status",
            "paused",
            "--resume-when",
            "the user reviews the stale authorization",
        )
        self.expire_authorized_lease("R1")

        self.cli("check", str(self.project))
        self.cli("can-stop", str(self.project))
        self.cli(
            "complete-risk-action",
            str(self.project),
            "R1",
            "--outcome",
            "completed",
            "--reference",
            "late completion claim",
            expected=1,
        )
        paused = self.state()
        self.assertEqual(paused["run"]["status"], "paused")
        self.assertEqual(paused["run"]["authorized_risk_id"], "R1")

        self.cli(
            "close",
            str(self.project),
            "--verdict",
            "cancelled",
            "--reason",
            "User ended the run with the expired action unexecuted",
        )
        self.cli("check", str(self.project))
        self.cli("can-stop", str(self.project))
        self.cli(
            "complete-risk-action",
            str(self.project),
            "R1",
            "--outcome",
            "cancelled",
            "--reference",
            "confirmed not executed",
        )
        finished = self.state()
        self.assertEqual(finished["run"]["status"], "finished")
        self.assertEqual(finished["run"]["product_verdict"], "cancelled")
        self.assertIsNone(finished["run"]["authorized_risk_id"])
        self.assertEqual(finished["risks"][0]["action_status"], "cancelled")
        self.assertEqual(
            finished["risks"][0]["expires_at"], "2000-01-01T00:00:00+00:00"
        )
        self.cli("check", str(self.project))

    def test_legacy_v1_migration_preserves_history_but_removes_old_verification(self):
        self.add_work()
        legacy = self.state()
        legacy["schema_version"] = "1.0"
        legacy["run"].pop("authorized_risk_id")
        legacy.pop("target")
        for item in legacy["work_items"]:
            item.pop("contract_sha256")
            item.pop("phase")
        legacy["run"]["status"] = "active"
        legacy["run"]["next_action"] = "perform the old unscoped production action"
        legacy["risks"] = [
            {
                "id": "R-legacy",
                "title": "Old production risk",
                "level": "critical",
                "consequence": "The production action may be destructive",
                "safer_option": "Request a fresh scoped decision",
                "recovery": "unknown",
                "scope": "old broad production action",
                "authorization_pending": False,
                "decision": "accepted",
                "decision_by": "legacy owner",
                "decision_reference": "legacy conversation",
                "decided_at": "2026-01-01T00:00:00+00:00",
            }
        ]
        journal = self.project / ".dz" / "journal.jsonl"
        with journal.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"at": "legacy", "event": "legacy", "state": legacy}) + "\n")
            malformed = json.loads(json.dumps(legacy))
            malformed["decisions"]["intent"] = []
            handle.write(
                json.dumps(
                    {"at": "malformed", "event": "malformed", "state": malformed}
                )
                + "\n"
            )
        (self.project / ".dz" / "state.json").write_text(
            json.dumps(malformed), encoding="utf-8"
        )
        self.cli("migrate", str(self.project))
        migrated = self.state()
        self.assertEqual(migrated["schema_version"], "1.1")
        self.assertEqual(migrated["work_items"][0]["contract_sha256"], "0" * 64)
        self.assertEqual(migrated["run"]["status"], "waiting_user")
        self.assertIsNone(migrated["run"]["next_action"])
        self.assertEqual(migrated["risks"][0]["action_kind"], "informational")
        self.assertEqual(migrated["risks"][0]["action_status"], "not_applicable")
        self.assertTrue((self.project / ".dz" / "migrations").is_dir())
        self.cli("check", str(self.project))


if __name__ == "__main__":
    unittest.main()
