"""Execute DZ's six stages with an actual, disposable, stdlib-only program.

Run with ``python3 -m unittest discover -s tests -p test_dz_lifecycle.py -v``.
All decision owners and triage decisions below are explicitly synthetic test
fixtures, never evidence of a real user's approval. No server, fixed port,
network, dependency install, external release, or business project is involved.
The test exercises the CLI, not imported implementation internals. Every Passed
record contains raw results from checks actually executed in this run.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "dz_state.py"
SYNTHETIC_OWNER = "SYNTHETIC TEST FIXTURE ONLY; no real user approval"

APP = '''import json
import sys


def main():
    try:
        request = json.load(sys.stdin)
        text = request.get("text") if isinstance(request, dict) else None
        if not isinstance(text, str):
            raise ValueError("text must be a string")
        tokens = text.split()
    except (ValueError, TypeError):
        print(json.dumps({"error": "invalid_request"}), file=sys.stderr)
        return 2
    print(json.dumps({"tokens": tokens, "count": len(tokens)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

CRITERIA = {
    "design": "The installed stdlib runtime loads and all three accepted decision digests match their complete visible fixtures.",
    "build": "[DZ-MUST:R1] The actual program returns ordered whitespace-separated tokens and their count through stdin/stdout.",
    "test": "[DZ-MUST:R2] Real independent processes handle Unicode and empty text, reject malformed/non-string requests, then recover on valid input.",
    "review": "The current source compiles and its imports and calls stay inside the declared JSON/stdin/stdout boundary.",
    "deploy": "The executable in the isolated release directory matches the approved source and its real core flow survives a rehearsed local restore.",
    "maintain": "Real release-process outcomes and timing produce inspectable metrics and feedback without changing the executable.",
}

INTENT = """# Intent
Status: Draft
Source: synthetic lifecycle-test request; no real user approval.
A single local operator wants to inspect words in short public sample text.
The current workaround is counting whitespace-separated tokens by hand.
Success means entering text and receiving the ordered tokens and exact count.
Need and adoption are fixture assumptions, not market or user-research evidence.
No sensitive input, network, paid service, model, or external action is needed.
The disposable experiment is stopped if exact examples cannot be reproduced.
"""

SPEC = """# Specification
Status: Draft
Predecessor: the exact accepted intent.md fixture.
Must: a local command reads one JSON object with a string text field from stdin
and returns JSON tokens (split on whitespace) and count through stdout, exit 0.
Empty text returns an empty list and count 0. Unicode is preserved in order.
Malformed JSON, missing text, and non-string text return only the controlled
invalid_request JSON error on stderr, no stdout, and exit 2. A later valid
invocation succeeds. No input is retained, so there is no durable business state.
Later: punctuation-aware splitting, if a real owner selects that new promise.
Won't: browser UI, AI/model calls, accounts, payments, network, shared hosting,
file mutation, background jobs, analytics service, or public deployment.
Only disposable sample inputs are used. There is no human quality claim.
"""
SPEC += "\n- " + CRITERIA["build"] + "\n- " + CRITERIA["test"] + "\n"

PLAN = """# Plan
Status: Draft
Predecessors: the exact accepted intent.md and spec.md fixtures.
Use the installed Python interpreter and json/sys standard library modules.
Build one local stdin -> validation -> split -> JSON output slice in app.py.
No package/repository reuse or provider is needed for this trivial operation.
Design checks runtime availability and the complete accepted decision records.
Build runs the actual command. Test checks every Must, invalid input and
recovery, and separately compiles/inspects source imports and calls.
The limited code check is automated; it is not a human security review.
Deploy copies the executable only into this test's TemporaryDirectory release
subdirectory. Observe its digest, run the core flow, inject a broken disposable
copy, restore the saved copy, and rerun the same real flow. Cost is zero.
Maintain captures actual outcomes/latency and punctuation feedback; synthetic
triage may defer a new promise, but cannot authorize a real product change.
General handbook routes: runtime intake, slice, implementation, deterministic
regression, real local-tool flow, and fixture-only walkthrough/handoff apply.
Frontend/model/provider/cloud/identity/persistence/migration/secrets/paid-resource
routes are excluded because the specification has no such interface or data.
No actual internal human acceptance or production readiness is claimed.
Every new target epoch reruns required checks before overall verification.
"""


class DzLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dz-lifecycle-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve() / "project"
        self.project.mkdir()
        self.release = Path(self.temp.name).resolve() / "local-release"
        self.release.mkdir()
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.cli("init", "--name", "Synthetic local lifecycle fixture", "--language", "en")
        self.git("init")
        self.check_number = 0
        self.epochs = []
        self.check_runs = {}

    def run_process(self, argv, *, cwd=None, input_text=None, expected=0):
        start = time.perf_counter_ns()
        with subprocess.Popen(
            [str(value) for value in argv],
            cwd=cwd or self.project,
            env=self.env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        ) as process:
            try:
                stdout, stderr = process.communicate(input_text, timeout=20)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                self.fail(f"Timed out: {argv}")
            record = {
                "argv": [str(value) for value in argv],
                "cwd": str(cwd or self.project),
                "pid": process.pid,
                "stdin": input_text,
                "stdout": stdout,
                "stderr": stderr,
                "returncode": process.returncode,
                "elapsed_ns": time.perf_counter_ns() - start,
            }
        self.assertEqual(record["returncode"], expected, json.dumps(record, ensure_ascii=False, indent=2))
        return record

    def cli(self, command, *args, expected=0):
        return self.run_process(
            [sys.executable, "-I", "-B", SCRIPT, command, self.project, *args],
            expected=expected,
        )

    def git(self, *args):
        return self.run_process(
            ["git", "-c", "core.hooksPath=" + os.devnull, "-c", "commit.gpgsign=false", *args]
        )

    def commit_fixture(self, message):
        self.git("add", ".")
        return self.git(
            "-c", "user.name=DZ synthetic fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "-m", message,
        )

    def write(self, relative, content):
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def write_json(self, relative, data):
        return self.write(relative, json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    def state(self):
        return json.loads((self.project / ".dz/state.json").read_text(encoding="utf-8"))

    @staticmethod
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def ledger_bytes(self):
        return {
            name: (self.project / name).read_bytes()
            for name in (".dz/state.json", ".dz/journal.jsonl", "PROJECT.md")
        }

    def rejected_without_mutation(self, command, *args):
        before = self.ledger_bytes()
        raw = self.cli(command, *args, expected=1)
        self.assertTrue(raw["stderr"].strip())
        self.assertEqual(self.ledger_bytes(), before)
        return raw

    def accept_visible_decisions(self):
        # Each complete document is delivered to a separate synthetic recipient.
        # A receipt binds the exact visible bytes; this cannot attest human consent.
        for index, (name, document) in enumerate((
            ("intent", INTENT), ("spec", SPEC), ("plan", PLAN)
        )):
            path = self.write(f"docs/sdlc/{name}.md", document)
            self.cli("set-decision", name, "--status", "draft")
            self.rejected_without_mutation(
                "set-run", "--status", "active", "--stage", "design", "--next-action", "premature fixture build"
            )
            self.rejected_without_mutation("set-decision", name, "--status", "accepted")
            receipt = self.write_json(f"fixture/visible-{name}.json", {
                "kind": "synthetic_test_approval_not_real_user_authorization",
                "sequence": index + 1,
                "owner": SYNTHETIC_OWNER,
                "path": str(path.relative_to(self.project)),
                "complete_visible_document": path.read_text(encoding="utf-8"),
                "sha256": self.digest(path),
                "decision": "accept this exact complete fixture draft",
            })
            self.cli("set-decision", name, "--status", "accepted", "--by", SYNTHETIC_OWNER,
                     "--reference", str(receipt.relative_to(self.project)))
            state = self.state()
            self.assertEqual(state["decisions"][name]["artifact_sha256"], self.digest(path))
            self.assertEqual(state["decisions"][name]["accepted_by"], SYNTHETIC_OWNER)
            self.assertEqual(state["run"]["stage"], name + "_accepted")
            self.assertEqual(sum(value["status"] == "accepted" for value in state["decisions"].values()), index + 1)
            self.assertFalse((self.project / "app.py").exists())
        self.commit_fixture("three distinct synthetic accepted decisions")

    def enter_stage(self, stage):
        self.cli("set-run", "--status", "active", "--stage", stage,
                 "--next-action", f"execute isolated {stage} fixture work")
        self.assertEqual(self.state()["run"]["stage"], stage)

    def begin_work(self, *ids):
        for work_id in ids:
            self.cli("update-work", work_id, "--status", "in_progress")

    def finish_implementation(self, *ids):
        for work_id in ids:
            self.cli("update-work", work_id, "--status", "implemented_unverified")

    def observe_target(self, program=None):
        path = program or self.project / "docs/sdlc/plan.md"
        raw = self.run_process([sys.executable, "-I", "-B", "-c",
            "import hashlib,json,pathlib,sys; p=pathlib.Path(sys.argv[1]); "
            "print(json.dumps({'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'runtime':sys.version}))",
            path], cwd=path.parent)
        observation = json.loads(raw["stdout"])
        self.assertGreater(observation["bytes"], 0)
        self.assertEqual(observation["sha256"], self.digest(path))
        self.revision = observation["sha256"]
        self.environment = str(path.parent.resolve())
        artifact = self.write_json(f"docs/sdlc/evidence/target-{len(self.epochs) + 1}.json", raw)
        historical_evidence = self.state()["evidence"]
        self.cli("set-target", "--revision", self.revision, "--environment", self.environment,
                 "--source", "independent Python file digest/runtime observation",
                 "--artifact", str(artifact.relative_to(self.project)))
        current = self.state()
        self.assertEqual(current["evidence"], historical_evidence)
        self.assertFalse(any(item["status"] == "verified" for item in current["work_items"]))
        target_id = current["target"]["id"]
        self.assertNotIn(target_id, self.epochs)
        self.epochs.append(target_id)

    def check_design(self):
        raw = self.run_process([sys.executable, "-I", "-B", "-c", """
import hashlib, importlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
receipts = [json.loads((root / ('fixture/visible-' + name + '.json')).read_text())
            for name in ('intent', 'spec', 'plan')]
observations = []
for receipt in receipts:
    data = (root / receipt['path']).read_bytes()
    observations.append({'sha256': hashlib.sha256(data).hexdigest(),
                         'bytes': len(data), 'sequence': receipt['sequence'],
                         'visible_matches': data.decode('utf-8') == receipt['complete_visible_document'],
                         'digest_matches': hashlib.sha256(data).hexdigest() == receipt['sha256']})
print(json.dumps({'version': list(sys.version_info[:3]),
                  'modules': [importlib.import_module(name).__name__ for name in ('json', 'sys')],
                  'decisions': observations}))
""", self.project])
        result = json.loads(raw["stdout"])
        self.assertGreaterEqual(result["version"][:2], [3, 9])
        self.assertEqual(result["modules"], ["json", "sys"])
        self.assertEqual([item["sequence"] for item in result["decisions"]], [1, 2, 3])
        for item in result["decisions"]:
            self.assertTrue(item["visible_matches"] and item["digest_matches"])
            self.assertGreater(item["bytes"], 0)
        return [raw]

    def invoke_app(self, program, text, *, expected=0, error=False):
        raw = self.run_process([sys.executable, "-I", "-B", program], cwd=program.parent,
                               input_text=text, expected=expected)
        if error:
            self.assertEqual(raw["stdout"], "")
            self.assertEqual(json.loads(raw["stderr"]), {"error": "invalid_request"})
        else:
            self.assertEqual(raw["stderr"], "")
        return raw

    def check_build(self, program):
        raw = self.invoke_app(program, json.dumps({"text": "one  two\nthree"}))
        self.assertEqual(json.loads(raw["stdout"]), {"tokens": ["one", "two", "three"], "count": 3})
        return [raw]

    def check_flow(self, program):
        results = []
        for text, expected in (("猫  头鹰\n你好", ["猫", "头鹰", "你好"]), (" \t\n", [])):
            raw = self.invoke_app(program, json.dumps({"text": text}))
            self.assertEqual(json.loads(raw["stdout"]), {"tokens": expected, "count": len(expected)})
            results.append(raw)
        for malformed in ("{broken", '{}', '{"text": 42}', "null"):
            results.append(self.invoke_app(program, malformed, expected=2, error=True))
        recovery = self.invoke_app(program, '{"text":"recovered input"}')
        self.assertEqual(json.loads(recovery["stdout"]), {"tokens": ["recovered", "input"], "count": 2})
        results.append(recovery)
        return results

    def check_review(self, program):
        raw = self.run_process([sys.executable, "-I", "-B", "-c", """
import ast, hashlib, json, pathlib, sys
path = pathlib.Path(sys.argv[1]); source = path.read_text(); tree = ast.parse(source)
compile(tree, str(path), 'exec')
imports = sorted(alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names)
from_imports = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
calls = sorted(set(ast.unparse(node.func) for node in ast.walk(tree) if isinstance(node, ast.Call)))
print(json.dumps({'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'imports': imports,
                  'from_imports': from_imports, 'calls': calls, 'nodes': len(list(ast.walk(tree)))}))
""", program])
        result = json.loads(raw["stdout"])
        self.assertEqual(result["sha256"], self.digest(program))
        self.assertEqual(result["imports"], ["json", "sys"])
        self.assertEqual(result["from_imports"], [])
        self.assertEqual(set(result["calls"]), {
            "ValueError", "isinstance", "json.dumps", "json.load", "len", "main",
            "print", "request.get", "sys.exit", "text.split",
        })
        self.assertGreater(result["nodes"], 0)
        return [raw]

    def check_release(self, program):
        self.assertEqual(program.parent.resolve(), self.release)
        self.assertEqual(self.digest(program), self.digest(self.project / "app.py"))
        # Deliberate fault and restore touch only this test's release copy.
        # Always restore, including when the expected failure is not observed.
        backup = self.release / "app.rollback.py"
        shutil.copy2(program, backup)
        try:
            program.write_text("import sys\nprint('fixture release unavailable', file=sys.stderr)\nsys.exit(7)\n", encoding="utf-8")
            broken = self.run_process([sys.executable, "-I", "-B", program], cwd=self.release, expected=7)
            self.assertTrue(broken["stderr"].strip())
        finally:
            shutil.copy2(backup, program)
        self.assertEqual(self.digest(program), self.digest(self.project / "app.py"))
        restored = self.check_build(program)
        digest_result = self.run_process([sys.executable, "-I", "-B", "-c",
            "import hashlib,json,pathlib,sys; p=pathlib.Path(sys.argv[1]); print(json.dumps({'restored_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}))",
            program], cwd=self.release)
        self.assertEqual(json.loads(digest_result["stdout"])["restored_sha256"], self.revision)
        return [broken, *restored, digest_result]

    def record_pass(self, work_id, raw_results):
        self.check_number += 1
        evidence_id = f"E{self.check_number}"
        self.assertTrue(raw_results)
        for raw in raw_results:
            self.assertTrue((raw["stdout"] + raw["stderr"]).strip())
            self.assertGreater(raw["elapsed_ns"], 0)
            self.assertNotEqual(raw["pid"], os.getpid())
        artifact = self.write_json(f"docs/sdlc/evidence/{evidence_id}.json", {
            "work_item": work_id, "criterion": CRITERIA[work_id],
            "target_id": self.state()["target"]["id"],
            "revision": self.revision, "environment": self.environment,
            "raw_results": raw_results,
            "limits": "Executed synthetic fixture checks; no real human approval or production claim.",
        })
        self.cli("add-evidence", "--id", evidence_id, "--work-item", work_id,
                 "--acceptance", CRITERIA[work_id], "--kind", "local-integration",
                 "--claim", CRITERIA[work_id], "--source", "actual subprocess commands and raw results in artifact",
                 "--artifact", str(artifact.relative_to(self.project)), "--revision", self.revision,
                 "--environment", self.environment, "--result", "passed")
        self.cli("update-work", work_id, "--status", "verified")
        self.check_runs.setdefault(work_id, []).append(self.state()["target"]["id"])
        return evidence_id

    def verify_current(self, ids, program=None):
        checks = {
            "design": self.check_design,
            "build": lambda: self.check_build(program),
            "test": lambda: self.check_flow(program),
            "review": lambda: self.check_review(program),
        }
        for work_id in ids:
            self.record_pass(work_id, checks[work_id]())

    def pause_and_resume_in_fresh_process(self, program):
        self.cli("set-run", "--status", "paused", "--next-action", "old fixture proposal: test saved executable",
                 "--resume-when", "synthetic fixture explicitly realigns the observed workspace")
        self.cli("can-stop")
        before = self.ledger_bytes()
        unchanged = json.loads(self.cli("resume-report")["stdout"])
        self.assertFalse(unchanged["workspace"]["changed_since_saved_record"])
        program.write_text(program.read_text(encoding="utf-8") + "\n# later source edit after paused save\n", encoding="utf-8")
        later = self.write("later-operator-note.txt", "Preserve this post-save fixture note.\n")
        raw = self.cli("resume-report", "--full-history", "--full-state")
        report = json.loads(raw["stdout"])
        self.assertEqual(self.ledger_bytes(), before, "resume-report must be read-only")
        self.assertNotEqual(raw["pid"], os.getpid())
        records = [json.loads(line) for line in (self.project / ".dz/journal.jsonl").read_text().splitlines()]
        self.assertEqual(report["journal_records_reviewed"], len(records))
        self.assertEqual(len(report["journal_history"]), len(records))
        self.assertEqual(report["invalid_journal_records"], 0)
        self.assertEqual(report["current_state"], self.state())
        self.assertEqual(report["current_summary"]["run"]["status"], "paused")
        self.assertEqual(report["current_summary"]["run"]["stage"], "build")
        self.assertTrue(report["generated_views"]["project_dashboard_current"])
        self.assertTrue(report["workspace"]["changed_since_saved_record"])
        self.assertIsNone(report["workspace"]["uncertainty"])
        self.assertTrue({"app.py", later.name}.issubset(set(report["workspace"]["changed_paths"])))
        self.assertTrue(report["takeover_rules"]["saved_next_action_is_advisory"])
        self.assertTrue(report["takeover_rules"]["user_confirmation_required_before_new_mutation"])
        source_after_save = program.read_bytes()
        self.write_json("fixture/resume-confirmation.json", {
            "owner": SYNTHETIC_OWNER, "observed_report": report,
            "decision": "Synthetic fixture only: preserve both later files; reobserve target and test current source.",
        })
        self.cli("set-run", "--status", "active", "--next-action", "fixture realigned: test preserved current executable")
        self.assertEqual(program.read_bytes(), source_after_save)
        self.assertTrue(later.exists())

    def check_maintenance(self, program):
        before = program.read_bytes()
        raw = self.check_build(program)
        raw.append(self.invoke_app(program, '{"text":false}', expected=2, error=True))
        feedback = self.invoke_app(program, '{"text":"hello,world"}')
        self.assertEqual(json.loads(feedback["stdout"]), {"tokens": ["hello,world"], "count": 1})
        raw.append(feedback)
        metrics = {
            "observed_invocations": len(raw),
            "successful_invocations": sum(item["returncode"] == 0 for item in raw),
            "controlled_rejections": sum(item["returncode"] == 2 for item in raw),
            "total_elapsed_ns": sum(item["elapsed_ns"] for item in raw),
            "cost": 0, "scope": "disposable local process observations, not production metrics",
        }
        self.assertEqual(metrics["successful_invocations"], 2)
        self.assertEqual(metrics["controlled_rejections"], 1)
        self.write_json("docs/sdlc/feedback/metrics.json", metrics)
        self.write_json("docs/sdlc/feedback/punctuation.json", {
            "status": "Triaged", "source": feedback,
            "observation": "The real command treats hello,world as one whitespace-separated token.",
            "owner": SYNTHETIC_OWNER,
            "decision": "Synthetic triage: conforms to current spec; defer punctuation splitting until a new spec is chosen.",
        })
        self.cli("add-issue", "--id", "F1", "--title", "Observed punctuation tokenization",
                 "--kind", "production_feedback", "--source", "docs/sdlc/feedback/punctuation.json",
                 "--expected", "Whitespace-separated tokens per accepted spec",
                 "--actual", feedback["stdout"].strip(),
                 "--impact", "Potential later punctuation-aware requirement; no current Must failure")
        self.cli("update-issue", "F1", "--status", "triaged")
        self.cli("update-issue", "F1", "--status", "deferred", "--resolution",
                 "SYNTHETIC fixture triage only: current whitespace behavior is correct; new promise requires a future visible spec decision")
        self.assertEqual(program.read_bytes(), before, "maintenance observation cannot modify the released program")
        issue = self.state()["issues"][0]
        self.assertEqual((issue["route"], issue["status"]), ("feedback", "deferred"))
        return raw

    def test_six_stage_execution_with_real_local_release_and_cross_process_resume(self):
        self.accept_visible_decisions()
        for work_id, acceptance in CRITERIA.items():
            phase = "test" if work_id == "review" else work_id
            self.cli("add-work", "--id", work_id, "--phase", phase,
                     "--title", "Execute " + work_id + " fixture route", "--acceptance", acceptance)

        self.enter_stage("design")
        self.rejected_without_mutation("set-run", "--status", "active", "--stage", "build", "--next-action", "skip design proof")
        self.begin_work("design")
        self.finish_implementation("design")
        self.observe_target()
        self.rejected_without_mutation("update-work", "design", "--status", "verified")
        self.verify_current(["design"])

        self.enter_stage("build")
        self.begin_work("build")
        program = self.write("app.py", APP)
        self.commit_fixture("actual executable for the accepted local slice")
        program.write_text(program.read_text(encoding="utf-8") + "\n# saved local source note\n", encoding="utf-8")
        self.finish_implementation("build")
        self.observe_target(program)
        self.verify_current(["design", "build"], program)
        self.pause_and_resume_in_fresh_process(program)

        self.enter_stage("test")
        self.begin_work("test")
        self.write_json("docs/sdlc/evidence/test-before-final-target.json", self.check_flow(program))
        self.finish_implementation("test")
        self.begin_work("review")
        self.write_json("docs/sdlc/evidence/review-before-final-target.json", self.check_review(program))
        self.finish_implementation("review")
        self.observe_target(program)
        self.rejected_without_mutation("set-run", "--status", "active", "--stage", "deploy", "--next-action", "skip current test evidence")
        self.verify_current(["design", "build", "test", "review"], program)
        self.write("docs/sdlc/verification.md", "Actual subprocess checks cover the frozen Must criteria; raw results are linked by the ledger.\n")
        self.write("docs/sdlc/review.md", "Executed source compile/import/call checks passed. This limited deterministic preflight is separate from flow checks; no human review, browser, model, or public-production claim is made.\n")

        self.enter_stage("deploy")
        self.begin_work("deploy")
        deployed = self.release / "app.py"
        shutil.copy2(program, deployed)
        self.finish_implementation("deploy")
        # The fault/recovery rehearsal finishes before the stable target is observed.
        self.revision = self.digest(program)
        release_results = self.check_release(deployed)
        self.observe_target(deployed)
        self.verify_current(["design", "build", "test", "review"], deployed)
        self.record_pass("deploy", release_results)
        self.write_json("docs/sdlc/release.json", {
            "target": str(deployed), "revision": self.revision,
            "audience": "this synthetic fixture only", "external_release": False,
            "authorization": "parent task permits isolated local test deployment only",
            "rollback_results": release_results,
            "limitations": "No actual human acceptance, credentials, cloud, or production environment tested.",
        })

        self.enter_stage("maintain")
        self.begin_work("maintain")
        maintenance_results = self.check_maintenance(deployed)
        self.finish_implementation("maintain")
        # Starting work creates a new epoch even for this read-only monitoring
        # slice. Repeat the required restore and checks, retaining all old proof.
        release_results = self.check_release(deployed)
        self.observe_target(deployed)
        self.verify_current(["design", "build", "test", "review"], deployed)
        self.record_pass("deploy", release_results)
        self.record_pass("maintain", maintenance_results)
        self.cli("close", "--verdict", "verified", "--reason",
                 "All required synthetic fixture checks executed; no real user acceptance or production claim")
        self.cli("can-stop")
        self.cli("check")

        state = self.state()
        self.assertEqual(state["run"]["stage"], "maintain")
        self.assertEqual(state["run"]["product_verdict"], "verified")
        self.assertEqual(state["run"]["status"], "finished")
        self.assertEqual(len(self.epochs), 5)
        for work_id in CRITERIA:
            self.assertIn(state["target"]["id"], self.check_runs[work_id])
        for evidence in state["evidence"]:
            artifact = self.project / evidence["artifact_path"]
            self.assertEqual(evidence["artifact_sha256"], self.digest(artifact))
            proof = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertTrue(proof["raw_results"])
            self.assertEqual(proof["criterion"], CRITERIA[evidence["work_item_id"]])
        self.assertEqual(len(state["evidence"]), self.check_number)
        self.assertEqual(self.digest(deployed), self.digest(program))
        records = [json.loads(line) for line in (self.project / ".dz/journal.jsonl").read_text().splitlines()]
        stages = {record["state"]["run"]["stage"] for record in records}
        self.assertTrue({"plan_accepted", "design", "build", "test", "deploy", "maintain"}.issubset(stages))
        report = json.loads(self.cli("resume-report")["stdout"])
        self.assertEqual(report["journal_records_reviewed"], len(records))
        self.assertEqual(report["current_summary"]["work"]["by_status"], {"verified": len(CRITERIA)})
        self.assertFalse(report["workspace"]["changed_since_saved_record"])


if __name__ == "__main__":
    unittest.main()
