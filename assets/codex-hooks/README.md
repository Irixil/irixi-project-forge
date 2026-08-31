# DZ Codex Stop hook / DZ Codex 收尾检查

## 中文

安装 DZ 插件时，不需要复制这个模板。插件自带 `hooks/hooks.json`，会从同一个插件目录调用权威状态工具，不会改动项目已有的 `.codex/hooks.json`。

只有单独安装 Skill、并且明确想在某个项目强制检查时，才使用 `hooks.json.example`：

1. 先确认项目中不存在 `.codex/hooks.json`。如果已存在，不要复制或覆盖，只把下面的 `Stop` 组人工合并进现有 `hooks` 对象。
2. 把本文件夹的 `hooks.json.example` 另存为项目的 `.codex/hooks.json`。
3. 把两个示例绝对路径改成已安装 DZ Skill 的真实路径。不要复制 `dz_state.py`；hook 和状态工具必须来自同一个 DZ 版本。
4. 在 Codex 中打开 `/hooks`，核对命令和路径后手动信任。

已有 `hooks.json` 时只合并这一段，不要再创建第二个 `hooks` 键：

```json
"Stop": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "python3 \"/absolute/path/to/dz/scripts/dz_codex_stop_hook.py\"",
        "timeout": 30
      }
    ]
  }
]
```

hook 只在项目或它的上级目录找到 `.dz/` 时工作；有 `.dz/` 但缺少 `state.json` 也算损坏账本。`active` 第一次会向 Codex 请求再继续一次，但 hook 信任、平台策略、其他 Stop hook 或宿主行为仍可能拒绝；`waiting_user`、`waiting_authorization`、`blocked`、`paused` 和 `finished` 会放行。若同一 Stop 已经请求一次后仍是 `active` 或账本仍损坏，第二次会带警告放行并保留真实未完状态，避免工具故障把用户困在死循环里。

## English

The DZ plugin already bundles `hooks/hooks.json`; do not copy this template for a plugin install. The bundled hook calls the authoritative state tool from the same plugin version and does not modify a project's existing `.codex/hooks.json`.

Use `hooks.json.example` only for an explicitly chosen project-level hook with a standalone Skill install:

1. Confirm that `.codex/hooks.json` does not exist. If it does, do not copy or overwrite it; manually merge only the `Stop` group shown above into its existing `hooks` object.
2. Save `hooks.json.example` as `<project>/.codex/hooks.json`.
3. Replace both example absolute paths with the installed DZ Skill root. Do not copy `dz_state.py`; the hook and state tool must stay on the same DZ version.
4. Open `/hooks` in Codex, inspect the command and path, then trust it explicitly.

The hook is inactive when no `.dz/` directory exists. A `.dz/` directory without `state.json` is a damaged ledger. It requests one continuation attempt for an active or damaged run; Codex may still decline it because of trust, policy, or another Stop hook. Waiting, blocked, paused, and finished runs may stop. On a second Stop this hook only warns and keeps the ledger honestly unfinished, so it does not repeat its own request forever.
