#!/usr/bin/env python3
"""Keep a Codex turn open while a valid DZ ledger is still active."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def emit(value: dict[str, Any]) -> int:
    print(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
    return 0


def find_project(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".dz").is_dir():
            return candidate
    return None


def block(reason: str) -> int:
    return emit({"decision": "block", "reason": reason})


def invalid_reason(detail: str) -> str:
    return (
        f"DZ 账本没通过检查（{detail}）。先用 DZ 状态工具检查，能从 "
        "`.dz/journal.jsonl` 恢复就恢复。如果用户要暂停、取消或诚实收尾，"
        "不要继续开发：恢复后记录 paused 或 finished 和真实的未验证结果。"
        "如果确实无法恢复，下次只如实说明账本损坏、已做内容、未验证内容和恢复办法，"
        "不得宣称 verified。"
    )


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return emit({"systemMessage": "DZ Stop hook 没收到可用的 JSON；本次未执行账本拦截。"})
    if not isinstance(event, dict) or event.get("hook_event_name") != "Stop":
        return emit({})

    cwd = event.get("cwd")
    if not isinstance(cwd, str) or not Path(cwd).is_dir():
        return emit({"systemMessage": "DZ Stop hook 没收到可用的项目路径；本次未执行账本拦截。"})
    project = find_project(Path(cwd))
    if project is None:
        return emit({})

    if not (project / ".dz" / "state.json").is_file():
        detail = "`.dz/state.json` 不存在"
        if event.get("stop_hook_active") is True:
            return emit({"systemMessage": invalid_reason(detail)})
        return block(invalid_reason(detail))

    state_tool = Path(__file__).with_name("dz_state.py")
    if not state_tool.is_file():
        detail = "找不到权威 DZ 状态工具"
        if event.get("stop_hook_active") is True:
            return emit({"systemMessage": invalid_reason(detail)})
        return block(invalid_reason(detail))

    try:
        result = subprocess.run(
            [sys.executable, str(state_tool), "can-stop", str(project)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        detail = f"检查工具无法完成：{type(exc).__name__}"
        if event.get("stop_hook_active") is True:
            return emit({"systemMessage": invalid_reason(detail)})
        return block(invalid_reason(detail))

    if result.returncode == 0:
        return emit({})
    if result.returncode == 2:
        reason = (
            "DZ 账本还是 active。先做 `.dz/state.json` 里的下一个安全动作，"
            "或按用户的真实选择记录为等待、阻塞、暂停、取消或收尾，再结束。"
            "用户说暂停或取消时应立即记录并停止；不要为了放行就把未验证内容说成 verified。"
        )
        if event.get("stop_hook_active") is True:
            return emit(
                {
                    "systemMessage": reason
                    + " Stop hook 已继续过一次，本次为避免死循环放行；账本仍是 active，"
                    "下次进入项目必须先恢复这项未完工作或如实收尾。"
                }
            )
        return block(reason)

    detail = f"权威状态检查失败，退出码 {result.returncode}"
    if event.get("stop_hook_active") is True:
        return emit({"systemMessage": invalid_reason(detail)})
    return block(invalid_reason(detail))


if __name__ == "__main__":
    raise SystemExit(main())
