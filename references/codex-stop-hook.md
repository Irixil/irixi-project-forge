# Codex Stop hook

DZ 的项目账本是持久记录，Codex Stop hook 只是一道本机收尾检查。它不会把未完成的东西自动做完，也不是安全边界。

接口格式以 [OpenAI Codex Hooks 官方说明](https://learn.chatgpt.com/docs/hooks) 为准。

## 它做什么

- 从 Codex Stop 事件的 `cwd` 开始向上查找最近的 `.dz/`。
- 没有 `.dz/` 时直接放行，不影响普通项目。有 `.dz/` 但缺少 `state.json` 按损坏账本处理。
- 通过同版本 `scripts/dz_state.py can-stop` 完成结构、证据文件、决策摘要和跨记录规则的语义检查，不维护第二套校验逻辑。
- 有效账本为 `active` 时第一次输出顶层 `decision: "block"` 和 `reason`，向 Codex 请求再做一个安全动作。是否真的继续仍受 hook 信任、平台策略、其他 Stop hook 和宿主行为影响，DZ 不能保证。若同一 Stop 已经请求过一次仍是 `active`，第二次带警告放行，保留未完状态，避免工具故障把用户困在死循环里。
- `waiting_user`、`waiting_authorization`、`blocked`、`paused` 和 `finished` 时输出空 JSON 对象并放行。
- 账本损坏时第一次请求恢复、暂停、取消或诚实收尾。若同一轮已经请求续跑但仍无法恢复，第二次放行并警告不得宣称已验证。

因此，用户任何时候都可以暂停、取消或提前收尾。只要把选择和真实产品结果写入账本，hook 就会放行；它不要求把未通过的检查改成通过。

## 接入

DZ Codex 插件默认读取 `hooks/hooks.json`，命令通过 Codex 提供的 `${PLUGIN_ROOT}` 调用同一插件内的 hook 脚本。不要在 `.codex-plugin/plugin.json` 中重复声明。用户需在 `/hooks` 中查看并信任未受管 hook。

单独 Skill 安装的手动可选模板位于 `assets/codex-hooks/hooks.json.example`。它不具有可直接执行的路径，必须先改成用户已检查的绝对 Skill 路径。已有 `.codex/hooks.json` 时只人工合并 `Stop` 组，绝不覆盖。

## English summary

The hook finds the nearest DZ ledger, delegates consistency validation to the same-version `dz_state.py can-stop`, and requests one continuation attempt for an active or damaged run. It cannot guarantee continuation: trust policy, host behavior, or another matching Stop hook can take precedence. On a second Stop this hook does not repeat its request; it warns and leaves the ledger honestly unfinished, so this hook cannot loop by itself. Waiting, blocked, paused, finished, and non-DZ runs stop normally. Plugin installs use `${PLUGIN_ROOT}` and require explicit review in `/hooks`; the inert project template must be edited to a reviewed absolute Skill path and never overwrites existing hook configuration.
