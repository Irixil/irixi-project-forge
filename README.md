# Irixi Project Forge

[中文](#中文) · [English](#english)

## 中文

### 简介

Irixi Project Forge 是一套面向非技术产品经理和初学者的 Codex Skill。它既可以从一个模糊想法开始，也可以在讨论、开发、测试甚至上线准备已经进行到一半时接管任务，梳理现状并继续推进。

Skill 的短名称是 `dz`。

DZ 不会把“帮我做一个应用”直接理解为立即写代码。它会帮助你确认真正的问题、第一批用户、可观察结果、MVP 边界和风险，并在关键的人类判断点要求明确确认。

### 核心能力

- 使用普通语言引导产品发现，每轮默认只问一个最关键的问题，最多三个；
- 当你回答“不知道”时，提供专业建议、一个有意义的替代方案和低成本验证方法；
- 区分已确认事实、建议、假设、未知项和明确不做的内容；
- 主动指出用户采用、数据、AI 必要性、模型质量、权限、隐私、成本、失败恢复和运营方面的漏洞；
- 不让非技术用户选择框架或为技术正确性背书；
- 在精确的 Intent、Specification 和 Plan 草稿分别被检查和确认前，不开始正式实现；
- 用真实路径和可复现证据判断完成，而不是只看 Mock、构建成功、部署命令或可访问网址；
- 可以中途接管当前任务，保留有效工作，不强迫用户重新回答已经明确的问题。

### AI 原生 SDLC

DZ 以 Anthropic 的 [AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) 为纲领，并适配 Codex：

```text
PLAN        DESIGN       BUILD          TEST              DEPLOY             MAINTAIN
intent.md → spec.md → plan.md + code → verification.md → review/release.md → feedback/new intent
```

每个阶段读取前一阶段已经确认的产物，并为下一阶段留下可版本化的产物或证据：

1. **Plan**：确认用户、场景、问题、目标、成功信号、限制和主要未知项，输出 `intent.md`。
2. **Design**：定义核心流程、Must / Later / Won't、状态、恢复、数据、权限和验收条件，输出 `spec.md`。
3. **Build**：读取已确认的 Intent 和 Specification，检查项目后提出最小技术路线，输出 `plan.md`，再按可独立验证的薄切片实现。
4. **Test**：持续运行确定性检查和真实路径验证，输出 `verification.md`，必要时进行独立复核。
5. **Deploy**：检查访问控制、密钥、持久化、备份、监控、成本和回滚，输出 `review.md` 与 `release.md`。上线批准不等于上线成功。
6. **Maintain**：把生产反馈、事故和指标转成可追踪证据，经人工判断后进入修复或新的 Intent。

`PROJECT.md` 只保存当前状态和产物链接，不代替完整的 Intent、Specification、Plan 或验证证据。

### 中途调用与任务接管

你可以在同一个对话或开发任务进行到一半时调用 DZ。它不会自动从头开始，也不会因为缺少流程文档就删除已有代码。

DZ 会先进入只读的 `TAKEOVER_AUDIT`：

1. 阅读当前对话里已经明确的目标、决定、否决项、工具结果和未完成问题；
2. 检查 `AGENTS.md`、`PROJECT.md`、`docs/sdlc`、Git 状态与差异、相关代码、测试和现有证据；
3. 分开报告“实际上已经做到了哪一步”和“哪一步有正式确认支持”；
4. 标记哪些工作可以保留、哪些需要复核、哪些仍然未知；
5. 找出最早缺失或被新证据推翻的确认环节；
6. 给出一个推荐的下一步，然后从那里继续，而不是机械重走全部流程。

如果代码已经存在但缺少 SDLC 产物，DZ 会把代码视为“待核对的候选实现”。它会根据对话、代码和测试逐步补出 Draft Intent、Specification 和 Plan，明确标记推断，分别请你检查确认，然后保留符合边界的已有工作并继续验证。

如果已经有有效的 Intent、Specification 和 Plan，而当前只是范围内的缺陷修复，DZ 会直接从 Build 或 Test 继续，不会重新询问用户是谁、产品解决什么问题。只有当修复改变体验、数据、权限、成本、架构或验收标准时，才重新打开受影响的最早环节。

中途接管示例：

```text
@dz 接管当前任务。先梳理我们已经决定了什么、代码和测试做到哪一步、哪些工作可以保留、最早缺少哪项确认，然后从单一下一步继续，不要让我重新解释已经说过的内容。
```

在使用 `$` 调用 Skill 的 Codex 界面中：

```text
$dz Take over the current task. Reconstruct the conversation and project state, preserve valid work, identify the earliest unsupported SDLC gate, and continue from one recommended next action.
```

### 三份技术手册的接入

DZ 整合了以下手册的流程：

- *AI 产品 Vibe Coding 通用技术栈手册*；
- *AI 产品 Vibe Coding 通用前端技术栈手册*；
- *AI Agent 产品上线部署手册*。

这些手册用于选择后端优先或端到端薄切片、确定必须项/默认项/按需项、设计异步任务状态、执行 Mock 加真实模型双层验证，以及检查生产就绪性。

DZ 同时修正了一些不应成为通用规则的高风险捷径：

- 云权限默认采用最小权限和短期凭证，不使用笼统的 FullAccess；
- 不在聊天中索取或暴露密钥；
- 不把临时磁盘或暖实例当作重要数据的可靠持久化；
- 不把邀请码当成通用的公开身份系统；
- 检查日志、监控和分析是否泄露敏感数据；
- 发布前重新核对当前云厂商文档、资格、价格、限制和运行时版本。

### Codex 原生适配

DZ 使用 Codex 自身的执行机制，而不是复制 Claude 专属命令：

- 在当前界面支持时使用 Plan mode 做只读发现和规划；
- 使用 `AGENTS.md` 保存稳定的仓库知识；
- 使用 Skills 保存跨项目方法；
- 使用当前计划跟踪已批准计划的执行；
- 只对真正独立的任务使用子代理或 worktree；
- 使用沙箱、审批、测试、eval、CI 和 review 形成分层控制；
- 使用部署 Skill 或官方文档处理厂商特定步骤。

详细映射见 [`references/codex-native.md`](references/codex-native.md)，开源执行底座见 [`openai/codex`](https://github.com/openai/codex)。

### 安装

把仓库克隆为 `dz`，然后放入或软链接到用户级 Skills 目录：

```bash
git clone https://github.com/Irixil/irixi-project-forge.git dz
mkdir -p "$HOME/.agents/skills"
ln -s "/absolute/path/to/dz" "$HOME/.agents/skills/dz"
```

如果更新后没有立即生效，请重启 Codex 并新建一个任务。

### 使用方式

从模糊想法开始：

```text
@dz 我有一个 AI 产品想法，但不懂技术。请从用户问题开始，每次只问最关键的问题，在我分别确认 Intent、Specification 和 Plan 前不要写代码。
```

导入已有 PRD：

```text
$dz Read this PRD, preserve what is already supported, identify only material product and risk gaps, and guide me through the missing gates.
```

恢复已有项目：

```text
$dz Continue this project. Read PROJECT.md, accepted files under docs/sdlc, AGENTS.md, and current verification evidence. Tell me the supported stage, earliest missing gate, and one next action.
```

检查上线准备：

```text
$dz Audit release readiness without deploying. Check accepted artifacts, real evidence, identity, secrets, persistence, monitoring, cost, and rollback, then explain blockers in product language.
```

ChatGPT Desktop 出现 `@` Skill 选择器时选择 `@dz`。Codex CLI 和 IDE 扩展通常使用 `$dz`。根据 [OpenAI Codex Skills 文档](https://developers.openai.com/codex/skills)，本地独立 Skills 可用于 ChatGPT Desktop、Codex CLI 和 IDE 扩展；若要在 ChatGPT Web 或移动端分发，需要把 Skill 打包进 Plugin。

### 目录结构

```text
dz/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── guided-dialogue.md
    ├── takeover-resume.md
    ├── artifact-chain.md
    ├── artifacts/
    │   ├── intent.md
    │   ├── spec.md
    │   ├── plan.md
    │   ├── verification.md
    │   ├── review-release.md
    │   └── feedback.md
    ├── phase-gates.md
    ├── handbook-routing.md
    ├── agent-harness.md
    ├── codex-native.md
    └── forward-tests.md
```

### 验证

Skill 使用 Codex Skill validator 检查结构，并定义十一组新上下文行为测试：

1. 模糊的“服务所有人”想法；
2. 区块链、RAG 和多 Agent 技术堆砌；
3. 请求永久高权限的自主 Agent；
4. 携带个人数据和前端密钥的危险上线；
5. 在三道确认之间要求提前写代码；
6. 不能合并确认的 Fast Track；
7. 监控不能继承旧授权自行改代码；
8. 有未提交代码但没有 SDLC 产物的中途接管；
9. 已有确认产物时接管一个范围内缺陷修复；
10. 没有仓库、只有长对话的中途接管；
11. 产物过期、代码版本变化和旧验证证据不能混用的接管。

行为测试定义见 [`references/forward-tests.md`](references/forward-tests.md)。

### 许可证

目前尚未选择许可证。源码公开可见，但在作者添加许可证前，不授予复制、修改或再分发权限。

---

## English

### Overview

Irixi Project Forge is a Codex Skill for nontechnical product managers and beginners. It can start from a rough idea or join halfway through an ongoing discussion, implementation, test cycle, or release preparation, reconstruct the task, and continue the workflow.

Its short invocation name is `dz`.

DZ does not interpret “build me an app” as permission to code immediately. It helps establish the real problem, first users, observable outcome, MVP boundary, and risks, then requests explicit acceptance at decisions that require human judgment.

### Core capabilities

- Guides product discovery in plain language, asking one highest-value question by default and never more than three per round.
- Recommends a professional default, a meaningful alternative, and a cheap validation method when the user is unsure.
- Separates confirmed facts, recommendations, assumptions, unknowns, and explicit non-goals.
- Challenges adoption, data, AI necessity, quality, permission, privacy, cost, recovery, and operational blind spots.
- Does not ask a beginner to choose frameworks or certify technical correctness.
- Does not begin formal implementation until the exact Draft Intent, Specification, and Plan have each been inspected and accepted.
- Judges completion by reproducible real-path evidence, not a mock, green build, deploy command, or reachable URL alone.
- Can take over midway, preserve valid work, and avoid repeating decisions already supported by the current task.

### AI-native SDLC

DZ follows Anthropic's [AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), adapted to Codex:

```text
PLAN        DESIGN       BUILD          TEST              DEPLOY             MAINTAIN
intent.md → spec.md → plan.md + code → verification.md → review/release.md → feedback/new intent
```

1. **Plan:** Establish the user, situation, problem, outcome, success signals, constraints, and largest unknowns in `intent.md`.
2. **Design:** Define the primary flow, Must/Later/Won't boundary, states, recovery, data, permissions, and acceptance criteria in `spec.md`.
3. **Build:** Read accepted Intent and Specification, inspect the project, propose the smallest technical route in `plan.md`, then implement independently verifiable thin slices.
4. **Test:** Run continuous deterministic checks and real-path verification, recording evidence in `verification.md` and using independent review when appropriate.
5. **Deploy:** Review access, secrets, persistence, backup, monitoring, cost, and rollback in `review.md` and `release.md`. Release approval is not release completion.
6. **Maintain:** Turn production feedback, incidents, and metrics into evidence, then route human-triaged changes into a bounded fix or new Intent.

`PROJECT.md` is a status dashboard and artifact index, not a replacement for Intent, Specification, Plan, or verification evidence.

### Mid-task takeover

You can invoke DZ halfway through the same conversation or development task. It does not automatically restart and does not delete existing code merely because workflow artifacts are missing.

DZ first enters a read-only `TAKEOVER_AUDIT`:

1. Read the visible goal, decisions, rejected options, tool results, and unfinished questions.
2. Inspect `AGENTS.md`, `PROJECT.md`, `docs/sdlc`, Git status and diff, relevant code, tests, and available evidence.
3. Report observed work state separately from gate-supported workflow state.
4. Mark existing work as keep, review, or unknown.
5. Identify the earliest missing or contradicted gate.
6. Recommend one next action and continue from there instead of replaying the whole process.

When code exists without SDLC artifacts, DZ treats it as candidate implementation under review. It progressively reconstructs Draft Intent, Specification, and Plan from the conversation, code, and tests, labels every inference, asks for exact acceptance, then preserves aligned work and continues verification.

When accepted artifacts already exist and the active task is a bounded defect, DZ resumes from Build or Test without reopening product discovery. It reopens only the earliest artifact affected by a change to experience, acceptance, data, permissions, cost, architecture, or another material boundary.

Take over in ChatGPT Desktop:

```text
@dz Take over the current task. Reconstruct what we decided, what the code and tests prove, what existing work can be kept, and the earliest unsupported SDLC gate. Continue from one recommended next action without making me repeat known context.
```

Take over where Skills use `$` invocation:

```text
$dz Take over the current task, map observed work against accepted artifacts, preserve valid changes, and continue from the earliest missing or contradicted gate.
```

### Integration with the three handbooks

DZ incorporates the workflows from:

- *AI Product Vibe Coding General Technology Stack Handbook*;
- *AI Product Vibe Coding General Frontend Technology Stack Handbook*;
- *AI Agent Product Launch and Deployment Handbook*.

They inform backend-first versus vertical-slice delivery, mandatory/default/on-demand modules, async task states, mock plus real-model verification, browser quality, and production readiness.

DZ also corrects shortcuts that should not become universal defaults:

- prefer least privilege and short-lived cloud credentials to blanket FullAccess;
- never request or expose secrets in chat;
- do not treat ephemeral disk or warm instances as durable storage for valuable data;
- do not treat invitation codes as a universal public identity system;
- audit logs, monitoring, and analytics for sensitive-data leakage;
- recheck current provider documentation, eligibility, pricing, limits, and runtime versions before release.

### Codex-native adaptation

DZ uses Codex-native mechanisms rather than copying Claude-specific commands:

- Plan mode for read-only discovery and planning when supported;
- `AGENTS.md` for stable repository knowledge;
- Skills for reusable cross-project methods;
- the current plan for execution under an accepted implementation plan;
- subagents and worktrees only for genuinely independent work;
- sandboxes, approvals, tests, evals, CI, and review as layered controls;
- provider Skills or official documentation for deployment-specific steps.

See [`references/codex-native.md`](references/codex-native.md) and the open-source [`openai/codex`](https://github.com/openai/codex) harness.

### Installation

Clone the repository as `dz`, then place or symlink it into the user Skills directory:

```bash
git clone https://github.com/Irixil/irixi-project-forge.git dz
mkdir -p "$HOME/.agents/skills"
ln -s "/absolute/path/to/dz" "$HOME/.agents/skills/dz"
```

If an update is not detected, restart Codex and open a fresh task.

### Usage

Start from a rough idea:

```text
$dz I have an AI product idea but I am not technical. Start with the user problem, ask only the most important question each round, and do not code until I separately accept the exact Intent, Specification, and Plan.
```

Bring an existing PRD:

```text
$dz Read this PRD, preserve what is already supported, identify only material product and risk gaps, and guide me through the missing gates.
```

Resume an existing project:

```text
$dz Continue this project. Read PROJECT.md, accepted files under docs/sdlc, AGENTS.md, and current verification evidence. Tell me the supported stage, earliest missing gate, and one next action.
```

Audit release readiness:

```text
$dz Audit release readiness without deploying. Check accepted artifacts, real evidence, identity, secrets, persistence, monitoring, cost, and rollback, then explain blockers in product language.
```

Choose `@dz` when the ChatGPT Desktop `@` Skill picker is available. Codex CLI and the IDE extension commonly use `$dz`. According to the [OpenAI Codex Skills documentation](https://developers.openai.com/codex/skills), standalone local Skills are available in ChatGPT Desktop, Codex CLI, and the IDE extension. Web and mobile distribution requires packaging the Skill in a Plugin.

### Structure

```text
dz/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── guided-dialogue.md
    ├── takeover-resume.md
    ├── artifact-chain.md
    ├── artifacts/
    │   ├── intent.md
    │   ├── spec.md
    │   ├── plan.md
    │   ├── verification.md
    │   ├── review-release.md
    │   └── feedback.md
    ├── phase-gates.md
    ├── handbook-routing.md
    ├── agent-harness.md
    ├── codex-native.md
    └── forward-tests.md
```

### Validation

The package is checked with the Codex Skill validator and defines eleven fresh-context behavioral test families:

1. a vague “product for everyone” idea;
2. fashionable blockchain, RAG, and multi-agent over-scoping;
3. an autonomous agent requesting permanent high-risk permissions;
4. an unsafe release involving personal data and frontend secrets;
5. pressure to write code between the three artifact gates;
6. Fast Track without collapsed confirmations;
7. monitoring that must not inherit old authority to change code;
8. mid-task takeover with uncommitted implementation and no SDLC artifacts;
9. takeover of an in-scope defect under accepted artifacts;
10. takeover of a long discussion with no repository;
11. takeover involving stale artifacts, a changed revision, and revision-bound evidence.

See [`references/forward-tests.md`](references/forward-tests.md) for the behavioral oracles.

### License

No license has been selected. The source is publicly visible, but no permission to copy, modify, or redistribute is granted unless the author adds a license.
