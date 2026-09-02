import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "scripts" / "dz_codex_stop_hook.py"
STATE = ROOT / "scripts" / "dz_state.py"


class CodexStopHookTests(unittest.TestCase):
    def state(self, project: Path, *args: str) -> None:
        subprocess.run(
            [sys.executable, str(STATE), *args, str(project)],
            capture_output=True,
            text=True,
            check=True,
        )

    def init(self, project: Path) -> None:
        self.state(project, "init", "--name", "Hook test")

    def hook(self, cwd: Path, *, already_continued: bool = False) -> dict:
        event = {
            "session_id": "test-session",
            "turn_id": "test-turn",
            "cwd": str(cwd),
            "hook_event_name": "Stop",
            "stop_hook_active": already_continued,
            "last_assistant_message": "done",
        }
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(event),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_non_dz_project_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.hook(Path(directory)), {})

    def test_incomplete_dz_directory_is_treated_as_a_damaged_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / ".dz").mkdir()
            output = self.hook(project)
            self.assertEqual(output["decision"], "block")
            self.assertIn("`.dz/state.json` 不存在", output["reason"])

    def test_active_project_is_blocked_from_a_subdirectory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self.init(project)
            child = project / "src" / "feature"
            child.mkdir(parents=True)
            output = self.hook(child)
            self.assertEqual(output["decision"], "block")
            self.assertIn("active", output["reason"])
            self.assertIn("暂停或取消", output["reason"])
            self.assertIn("resume-report", output["reason"])
            self.assertIn("不要照着", output["reason"])
            self.assertNotIn("先做 `.dz/state.json` 里的下一个安全动作", output["reason"])
            second = self.hook(child, already_continued=True)
            self.assertNotIn("decision", second)
            self.assertIn("避免死循环", second["systemMessage"])
            self.assertIn("仍是 active", second["systemMessage"])
            self.assertIn("verified", second["systemMessage"])

    def test_expired_active_action_is_invalid_but_paused_history_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self.init(project)
            subprocess.run(
                [
                    sys.executable,
                    str(STATE),
                    "add-risk",
                    str(project),
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
                    "send one staging notification",
                    "--expires-at",
                    "2099-01-01T00:00:00+00:00",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(STATE),
                    "decide-risk",
                    str(project),
                    "R1",
                    "--decision",
                    "accepted",
                    "--by",
                    "project owner",
                    "--reference",
                    "approved exact notification",
                    "--next-action",
                    "send one staging notification",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            state_path = project / ".dz" / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["risks"][0]["expires_at"] = "2000-01-01T00:00:00+00:00"
            state_path.write_text(
                json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with (project / ".dz" / "journal.jsonl").open(
                "a", encoding="utf-8"
            ) as handle:
                handle.write(
                    json.dumps(
                        {
                            "at": "lease elapsed",
                            "event": "lease_elapsed",
                            "state": state,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )

            blocked = self.hook(project)
            self.assertEqual(blocked["decision"], "block")
            self.assertIn("active", blocked["reason"])
            self.assertNotIn("账本没通过检查", blocked["reason"])

            self.state(
                project,
                "set-run",
                "--status",
                "paused",
                "--resume-when",
                "the user reviews the expired authorization",
            )
            self.assertEqual(self.hook(project), {})

    def test_waiting_states_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "waiting-user"
            self.init(project)
            self.state(project, "set-run", "--status", "waiting_user", "--waiting-for", "one answer")
            self.assertEqual(self.hook(project), {})

            authorization = Path(directory) / "waiting-authorization"
            self.init(authorization)
            self.state(
                authorization,
                "add-risk",
                "--id",
                "R1",
                "--title",
                "public release",
                "--level",
                "critical",
                "--action-kind",
                "public_release",
                "--consequence",
                "data may be exposed",
                "--safer-option",
                "private preview",
                "--scope",
                "one demo",
                "--expires-at",
                "2099-01-01T00:00:00+00:00",
            )
            self.state(
                authorization,
                "set-run",
                "--status",
                "waiting_authorization",
                "--waiting-for",
                "R1 decision",
                "--pending-risk",
                "R1",
            )
            self.assertEqual(self.hook(authorization), {})

    def test_blocked_paused_and_finished_states_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            blocked = root / "blocked"
            self.init(blocked)
            self.state(
                blocked,
                "set-run",
                "--status",
                "blocked",
                "--blocker",
                "missing test device",
                "--blocker-kind",
                "missing_capability",
                "--resume-when",
                "device is available",
            )
            self.assertEqual(self.hook(blocked), {})

            paused = root / "paused"
            self.init(paused)
            self.state(paused, "set-run", "--status", "paused", "--resume-when", "user continues")
            self.assertEqual(self.hook(paused), {})

            finished = root / "finished"
            self.init(finished)
            self.state(finished, "close", "--verdict", "cancelled", "--reason", "user cancelled")
            self.assertEqual(self.hook(finished), {})

    def test_damaged_ledger_blocks_once_with_escape_choices(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self.init(project)
            (project / ".dz" / "state.json").write_text("{broken", encoding="utf-8")
            output = self.hook(project)
            self.assertEqual(output["decision"], "block")
            self.assertIn("恢复", output["reason"])
            self.assertIn("暂停、取消或诚实收尾", output["reason"])
            self.assertIn("不得宣称 verified", output["reason"])

    def test_damaged_ledger_second_stop_allows_honest_ending(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self.init(project)
            (project / ".dz" / "state.json").write_text("{}", encoding="utf-8")
            output = self.hook(project, already_continued=True)
            self.assertNotIn("decision", output)
            self.assertIn("不得宣称 verified", output["systemMessage"])

    def test_plugin_hook_uses_plugin_root_and_stop_contract(self) -> None:
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        handler = config["hooks"]["Stop"][0]["hooks"][0]
        self.assertEqual(handler["type"], "command")
        self.assertEqual(
            handler["command"],
            'python3 "${PLUGIN_ROOT}/scripts/dz_codex_stop_hook.py"',
        )
        self.assertNotIn("matcher", config["hooks"]["Stop"][0])
        manifest = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("hooks", manifest)

    def test_project_template_is_inert_until_path_is_reviewed(self) -> None:
        template_path = ROOT / "assets" / "codex-hooks" / "hooks.json.example"
        self.assertEqual(template_path.name, "hooks.json.example")
        template = json.loads(template_path.read_text(encoding="utf-8"))
        command = template["hooks"]["Stop"][0]["hooks"][0]["command"]
        self.assertIn("/absolute/path/to/dz/", command)
        self.assertFalse((ROOT / ".codex" / "hooks.json").exists())


if __name__ == "__main__":
    unittest.main()
