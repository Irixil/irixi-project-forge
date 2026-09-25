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
    if (current / ".dz").is_dir():
        return current
    children = sorted(
        candidate
        for candidate in current.iterdir()
        if not candidate.is_symlink()
        and candidate.is_dir()
        and (candidate / ".dz").is_dir()
    )
    if len(children) > 1:
        names = "、".join(candidate.name for candidate in children)
        raise ValueError(
            f"当前目录有多个 DZ 项目（{names}），无法确定本任务对应哪一个。"
            "先说明需要选择项目，不要猜测、读取或修改其中任何账本，也不要盲目继续开发。"
            "用户要求暂停或取消时直接遵从，不要为了通过检查而要求继续。"
        )
    if children:
        return children[0]
    for candidate in (current, *current.parents):
        if (candidate / ".dz").is_dir():
            return candidate
        if (candidate / ".git").exists():
            break
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
    try:
        project = find_project(Path(cwd))
    except (OSError, ValueError) as exc:
        reason = f"DZ 项目路径无法确定：{exc}"
        if event.get("stop_hook_active") is True:
            return emit({"systemMessage": reason + " Stop hook 已请求过一次，本次为避免死循环放行。"})
        return block(reason)
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
            "DZ 账本还是 active。不要照着 `.dz/state.json` 里保存的旧下一步直接做。"
            "先只读运行 DZ 状态工具的 `resume-report`；工具会检查全部历史，先用它给出的当前摘要与项目现状对一遍。"
            "如果用户还没确认当前情况和接下来的做法，先用短句汇报并记录为等待用户；"
            "如果用户已经确认，继续完成当前约定内仍可执行的工作，不要每做一步就重复确认。也可以按用户的真实选择记录为"
            "阻塞、暂停、取消或收尾，再结束。"
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
