# Irixi Project Forge

[中文](#中文) · [English](#english)

## 中文

### 简介

Irixi Project Forge 是一套面向非技术产品经理和初学者的跨平台 AI 产品工作流。只要一个 AI 能接收文字，它就能运行 DZ 的核心流程；能否查看项目、开发、测试或上线，再由它实际拥有的工具决定。DZ 能从一个模糊想法开始，也能在讨论、开发、测试甚至上线准备进行到一半时接手并继续。

工作流的短名称是 `dz`。

DZ 不会把“帮我做一个应用”直接理解为立即写代码。它会先用大白话帮你确认真正的问题、第一批用户、想达到的结果、第一版做什么和不做什么，再一步一步开发和检查。

### 最后会得到什么

一个想法适合继续开发时，你最终会得到四样东西：

1. 一个真正可以使用的应用或 Agent；
2. 三份你能看懂并亲自确认的简短记录：为什么做、第一版做什么、准备怎么开发；
3. 可以复查的测试结果，说明哪些已经能用、哪些还没证明；
4. 上线方法、已知风险，以及出问题时怎样恢复。

如果在前期发现这个想法不值得做，DZ 会直接说明原因和更省钱的替代办法，不会为了交付代码而硬做。

简单理解：DZ 负责带路，当前有执行能力的 AI 负责动手；在 Codex 中，动手的就是 Codex。Agent Harness 教程只在幕后提供“怎样记住进度、拆开任务、检查结果”的经验。DZ 已经把这些经验写进自己的规则；每次使用时不会重新运行教程，也不要求用户阅读它。

### 核心能力

- 默认先说结论，使用短句和具体例子，不主动展示内部流程名、英文状态或文件名；
- 普通对话保持在几个短段落内，每轮只问一个最关键的问题；
- 自动判断当前 AI 只能聊天、能查看项目、能开发，还是还能上线，并据此调整做法；
- 当你回答“不知道”时，提供专业建议、一个有意义的替代方案和低成本验证方法；
- 区分已确认事实、建议、假设、未知项和明确不做的内容；
- 主动指出用户采用、数据、AI 必要性、模型质量、权限、隐私、成本、失败恢复和运营方面的漏洞；
- 不让非技术用户选择框架或为技术正确性背书；
- 在“为什么做”“第一版做什么”“准备怎么开发”分别被你看过并确认前，不开始正式实现；
- 用真实路径和可复现证据判断完成，而不是只看 Mock、构建成功、部署命令或可访问网址；
- 可以中途接管当前任务，保留有效工作，不强迫用户重新回答已经明确的问题。

### 在不同 AI 上怎么用

所有平台都使用同一套 DZ 流程。只要能接收文字，就可以使用；能否读取项目、写代码、运行测试或上线，只看当前平台实际开放的工具，不看品牌。WorkBuddy、Kimi、智谱、DeepSeek、Claude、Gemini、Codex、私有模型和以后出现的新平台都不需要分别开发不同版本。后文的 Codex 只是一个完整接入示例。

| 平台提供的入口 | 统一加载方式 | 实际结果 |
|---|---|---|
| 支持 Skill 或 `SKILL.md` | 安装完整仓库目录 | 使用完整流程，并自动调用该平台真正开放的工具 |
| 支持系统提示词、项目指令或 API | 加载 [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md)，再传入能力说明 | 使用同一流程；接入程序负责保存对话、执行工具和控制权限 |
| 支持文件上传或知识库 | 上传通用提示词，并按需加入相关参考文件 | 使用同一流程；能否动手开发取决于会话工具 |
| 只能普通聊天 | 粘贴通用提示词，用 `DZ启动：` 开始 | 完成脑暴、确认边界和交接；不会假装已经开发或测试 |

通用提示词是一份安全、可单文件使用的精简版。若要让 API 版获得与完整 Skill 相同的技术手册和产物模板，接入程序还应按 `dz-manifest.json` 的 `reference_sets` 提供按需读取，不要把所有资料一次性塞进上下文。

`@dz`、`$dz` 或 `/dz` 只是部分平台的快捷入口。所有其他平台统一使用：

```text
DZ启动：我想做……请用大白话，每次只问一个问题。
```

### 自动适配接口（给平台开发者，普通用户可跳过）

普通用户不需要配置下面这些内容；能粘贴通用提示词就可以使用 DZ。

仓库提供一套公开适配入口：

- [`dz-manifest.json`](dz-manifest.json) 告诉加载器应该读取哪个版本；
- [`adapters/dz-capabilities.schema.json`](adapters/dz-capabilities.schema.json) 描述当前 AI 真实拥有的能力；
- [`adapters/README.md`](adapters/README.md) 给出加载顺序和能力说明示例；
- [`references/platform-adapters.md`](references/platform-adapters.md) 规定怎样自动选择“只引导、可查看、可开发、可上线”的做法。

公开加载地址：[`dz-manifest.json`](https://raw.githubusercontent.com/Irixil/irixi-project-forge/main/dz-manifest.json)。有联网和系统指令权限的接入程序可以先读取它，再按清单加载对应入口。

加载器能提供能力说明时，DZ 直接选择最合适的做法。没有说明时，DZ 只根据眼前真实可见的工具做安全判断；无法确认的能力一律按“没有”处理。能调用工具不等于获得授权，发布、付费、删除、外部写入和生产操作仍需单独确认。

平台名字只用于显示和排查问题，绝不能参与流程选择。相同能力的 WorkBuddy、Kimi、智谱或任何未知 AI，必须得到相同的 DZ 工作方式。

这不是一个能强行控制所有 AI 网站的魔法接口。目标平台至少要允许读取 Skill、系统提示词、项目指令或上传文件；否则只能手动粘贴通用提示词。

### AI 原生 SDLC

DZ 以 Anthropic 的 [AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) 为纲领。流程本身不绑定模型，当前 AI 只替换执行接头：

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

这些英文名称和文件名是 DZ 在项目内部使用的记录。和初学者沟通时，DZ 默认只说“确认目标”“确认第一版范围”“确认开发方案”“检查是否真的能用”和“准备上线”。

### 中途调用与任务接管

你可以在同一个对话或开发任务进行到一半时调用 DZ。它不会自动从头开始，也不会因为缺少流程文档就删除已有代码。

DZ 会先只看不改，用几句话说明：

1. 当前已经做到哪里；
2. 哪些内容和代码可以继续使用；
3. 还有哪件事没有确认或没有测试证明；
4. 建议接下来只做什么，并只问你一个问题。

如果代码已经存在但缺少项目记录，DZ 不会删除代码。它会把已有代码当成“可能有用、但还要核对的工作”，补清目标、第一版范围和开发方案，再保留符合要求的部分继续检查。

如果目标、第一版范围和开发方案已经确认，而当前只是修复一个范围内的问题，DZ 会直接继续修改或测试，不会让你重新回答产品是给谁用的。只有修复会改变体验、数据、权限、成本或主要技术方案时，才重新确认受影响的部分。

中途接管示例：

```text
@dz 接管当前任务。先梳理我们已经决定了什么、代码和测试做到哪一步、哪些工作可以保留、最早缺少哪项确认，然后从单一下一步继续，不要让我重新解释已经说过的内容。
```

在使用 `$` 调用 Skill 的 Codex 界面中：

```text
$dz Take over the current task. In plain language, tell me where we are, what can be kept, what is still missing, and the one thing we should do next.
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

### 接入示例：Codex

DZ 使用 Codex 自身的执行机制，而不是复制 Claude 专属命令：

- 在当前界面支持时使用 Plan mode 做只读发现和规划；
- 使用 `AGENTS.md` 保存稳定的仓库知识；
- 使用 Skills 保存跨项目方法；
- 使用当前计划跟踪已批准计划的执行；
- 只对真正独立的任务使用子代理或 worktree；
- 使用沙箱、审批、测试、eval、CI 和 review 形成分层控制；
- 使用部署 Skill 或官方文档处理厂商特定步骤。

详细映射见 [`references/codex-native.md`](references/codex-native.md)，开源执行底座见 [`openai/codex`](https://github.com/openai/codex)。

### 在 Codex 中安装（示例）

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
@dz 我有一个 AI 产品想法，但不懂技术。请用简短的大白话带我一步一步做，每次只问一个最重要的问题。先帮我确认目标、第一版范围和开发方案，再开始写代码。
```

导入已有 PRD：

```text
$dz 阅读这份 PRD。保留已经说清楚的内容，用大白话告诉我还缺什么，并且一次只带我解决一件事。
```

恢复已有项目：

```text
$dz 接着做这个项目。不要从头问，用简短的话告诉我已经做到哪里、什么可以保留、还缺什么，以及唯一的下一步。
```

检查上线准备：

```text
$dz 先不要上线。请检查它是否真的能安全使用，再用大白话告诉我哪些已经准备好、哪些必须先解决。
```

ChatGPT Desktop 出现 `@` Skill 选择器时选择 `@dz`。Codex CLI 和 IDE 扩展通常使用 `$dz`。根据 [OpenAI Codex Skills 文档](https://developers.openai.com/codex/skills)，本地独立 Skills 可用于 ChatGPT Desktop、Codex CLI 和 IDE 扩展；若要在 ChatGPT Web 或移动端分发，需要把 Skill 打包进 Plugin。

### 目录结构

```text
dz/
├── SKILL.md
├── dz-manifest.json
├── agents/
│   └── openai.yaml
├── adapters/
│   ├── README.md
│   ├── dz-capabilities.schema.json
│   └── example-capabilities.json
├── portable/
│   └── DZ-UNIVERSAL.md
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
    ├── platform-adapters.md
    ├── codex-native.md
    └── forward-tests.md
```

### 验证

Skill 使用 Codex Skill validator 和 JSON 检查验证结构，并定义十三组新上下文行为测试：

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
11. 产物过期、代码版本变化和旧验证证据不能混用的接管；
12. 面向非技术初学者时必须简短、浅显，只问一个问题，不暴露内部术语；
13. 同一套 DZ 在聊天型、可开发型和可上线型平台上自动选择合适做法；相同能力不因平台品牌不同而改变。

行为测试定义见 [`references/forward-tests.md`](references/forward-tests.md)。

### 许可证

目前尚未选择许可证。源码公开可见，但在作者添加许可证前，不授予复制、修改或再分发权限。

---

## English

### Overview

Irixi Project Forge is a cross-platform AI product workflow for nontechnical product managers and beginners. Any AI that accepts text can run the DZ core; its actual tools determine whether it can inspect a project, build, test, or release. DZ can start from a rough idea or join halfway through discussion, implementation, testing, or release preparation and continue from the real state.

Its short name is `dz`.

DZ does not interpret “build me an app” as permission to code immediately. In plain language, it first helps establish the real problem, first users, desired outcome, and what the first version will and will not do, then builds and checks the product step by step.

### What you get

When an idea is worth building, a DZ project should leave you with four things:

1. An application or agent that can actually be used.
2. Three short records you can understand and confirm: why it should exist, what the first version includes, and how it will be built.
3. Reproducible test results showing what works and what is still unproven.
4. A launch approach, known risks, and a recovery plan.

If early discovery shows that the idea is not worth building, DZ explains why and recommends a cheaper alternative instead of producing code for its own sake.

In simple terms: DZ guides the work and the current execution-capable AI does the hands-on work; on Codex, that worker is Codex. The Agent Harness tutorial contributes behind-the-scenes lessons about remembering progress, splitting work, and checking results. DZ has already turned those lessons into its own rules; it does not rerun the tutorial or require the user to read it for every project.

### Core capabilities

- Leads with the answer, uses short sentences and concrete examples, and hides internal state names, English lifecycle labels, and filenames by default.
- Keeps ordinary replies short and asks one highest-value question per round.
- Detects whether the current AI can only chat, inspect a project, build it, or also release it, then adjusts the workflow automatically.
- Recommends a professional default, a meaningful alternative, and a cheap validation method when the user is unsure.
- Separates confirmed facts, recommendations, assumptions, unknowns, and explicit non-goals.
- Challenges adoption, data, AI necessity, quality, permission, privacy, cost, recovery, and operational blind spots.
- Does not ask a beginner to choose frameworks or certify technical correctness.
- Does not begin formal implementation until the user has separately confirmed why the product should exist, what the first version includes, and how it will be built.
- Judges completion by reproducible real-path evidence, not a mock, green build, deploy command, or reachable URL alone.
- Can take over midway, preserve valid work, and avoid repeating decisions already supported by the current task.

### Using DZ on different AI platforms

Every platform uses the same DZ workflow. Any AI that accepts text can use it; whether it can read a project, write code, run tests, or release depends only on the tools actually available, never the brand. WorkBuddy, Kimi, Zhipu, DeepSeek, Claude, Gemini, Codex, private models, and future hosts do not need separate DZ versions. Codex appears later only as one complete integration example.

| What the host accepts | Unified loading form | Result |
|---|---|---|
| Skills or `SKILL.md` | Install the full repository bundle | Keep the full workflow and automatically use only the tools actually exposed by that host |
| System prompts, project instructions, or an API | Load [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md), then append a capability card | Keep the same flow; the integration owns history, tool execution, and permissions |
| File upload or a knowledge base | Upload the universal prompt and only the references needed now | Keep the same flow; hands-on delivery depends on the chat's actual tools |
| Plain text chat only | Paste the universal prompt and start with `DZ启动：` | Brainstorm, confirm boundaries, and create a handoff without pretending to have built or tested anything |

The universal prompt is a safe, single-file compact edition. To give an API host the same handbook detail and artifact templates as the full Skill, expose the manifest's `reference_sets` through on-demand retrieval instead of concatenating every resource into every request.

`@dz`, `$dz`, and `/dz` are shortcuts on some hosts. Everywhere else, use:

```text
DZ启动：I want to build ... Please use plain language and ask one question at a time.
```

### Automatic adapter interface (for host developers; ordinary users can skip this)

Ordinary users do not need to configure any of this. Pasting the universal prompt is enough to use DZ.

The repository exposes a public adapter interface:

- [`dz-manifest.json`](dz-manifest.json) tells a loader which entry point to use;
- [`adapters/dz-capabilities.schema.json`](adapters/dz-capabilities.schema.json) describes what the current host can actually do;
- [`adapters/README.md`](adapters/README.md) defines the loading sequence and provides an example capability card;
- [`references/platform-adapters.md`](references/platform-adapters.md) defines how DZ selects guide, inspect, build, or release behavior.

Public loader URL: [`dz-manifest.json`](https://raw.githubusercontent.com/Irixil/irixi-project-forge/main/dz-manifest.json). An integration with web access and system-instruction control can fetch it first, then load the selected entry point.

When a loader supplies a validated capability card, DZ selects the best-supported behavior. Without one, DZ relies only on tools and environment facts it can truly see; unknown abilities are treated as unavailable. Tool access is never authorization: publishing, spending, deletion, external writes, and production changes still require separate approval.

The host name is diagnostic only and must never influence routing. WorkBuddy, Kimi, Zhipu, or any unknown AI with the same capabilities must receive the same DZ behavior.

This interface cannot force an arbitrary AI website to load DZ. The host must support a Skill, system instruction, project instruction, or file upload; otherwise the universal prompt must be pasted manually.

### AI-native SDLC

DZ follows Anthropic's [AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook). The workflow is model-neutral; the current AI changes only the execution connector:

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

Those English names and filenames are internal project records. With a beginner, DZ normally says “confirm the goal,” “confirm the first-version boundary,” “confirm the build approach,” “check that it really works,” and “prepare to go live.”

### Mid-task takeover

You can invoke DZ halfway through the same conversation or development task. It does not automatically restart and does not delete existing code merely because workflow artifacts are missing.

DZ first inspects without changing anything, then explains in a few short blocks:

1. Where the task is now.
2. What existing work can be kept.
3. What is still unconfirmed or unproven.
4. The single recommended next action and one question for the user.

When code exists without project records, DZ preserves it as potentially useful work that still needs checking. It reconstructs the goal, first-version boundary, and build approach, asks the user to confirm them in ordinary language, then keeps aligned work and continues testing.

When those decisions already exist and the task is a bounded defect, DZ resumes from implementation or testing without restarting product discovery. It reopens only the earliest decision affected by a change to experience, data, permissions, cost, architecture, or another material boundary.

Take over in ChatGPT Desktop:

```text
@dz Take over the current task. In plain language, tell me where we are, what can be kept, what is still missing, and the one thing we should do next. Do not make me repeat known context.
```

Take over where Skills use `$` invocation:

```text
$dz Take over the current task. Preserve useful work, explain the real situation simply, and continue from one clear next step.
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

### Integration example: Codex

DZ uses Codex-native mechanisms rather than copying Claude-specific commands:

- Plan mode for read-only discovery and planning when supported;
- `AGENTS.md` for stable repository knowledge;
- Skills for reusable cross-project methods;
- the current plan for execution under an accepted implementation plan;
- subagents and worktrees only for genuinely independent work;
- sandboxes, approvals, tests, evals, CI, and review as layered controls;
- provider Skills or official documentation for deployment-specific steps.

See [`references/codex-native.md`](references/codex-native.md) and the open-source [`openai/codex`](https://github.com/openai/codex) harness.

### Installation on Codex (example)

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
$dz I have an AI product idea but I am not technical. Guide me step by step in plain, concise language, ask one important question at a time, and confirm the goal, first-version boundary, and build approach before coding.
```

Bring an existing PRD:

```text
$dz Read this PRD, keep what is already clear, explain only the important gaps in plain language, and guide me through one decision at a time.
```

Resume an existing project:

```text
$dz Continue this project without starting over. Tell me simply where it stands, what can be kept, what is missing, and the one next action.
```

Audit release readiness:

```text
$dz Do not deploy yet. Check whether this is genuinely safe and usable, then explain in plain language what is ready and what must be fixed first.
```

Choose `@dz` when the ChatGPT Desktop `@` Skill picker is available. Codex CLI and the IDE extension commonly use `$dz`. According to the [OpenAI Codex Skills documentation](https://developers.openai.com/codex/skills), standalone local Skills are available in ChatGPT Desktop, Codex CLI, and the IDE extension. Web and mobile distribution requires packaging the Skill in a Plugin.

### Structure

```text
dz/
├── SKILL.md
├── dz-manifest.json
├── agents/
│   └── openai.yaml
├── adapters/
│   ├── README.md
│   ├── dz-capabilities.schema.json
│   └── example-capabilities.json
├── portable/
│   └── DZ-UNIVERSAL.md
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
    ├── platform-adapters.md
    ├── codex-native.md
    └── forward-tests.md
```

### Validation

The package is checked with the Codex Skill validator and JSON validation, and defines thirteen fresh-context behavioral test families:

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
11. takeover involving stale artifacts, a changed revision, and revision-bound evidence;
12. concise plain-language guidance for a nontechnical beginner, with one question and no exposed internal jargon;
13. automatic capability-aware behavior across chat-only, build-capable, and release-capable hosts, with identical behavior for identical capabilities regardless of brand.

See [`references/forward-tests.md`](references/forward-tests.md) for the behavioral oracles.

### License

No license has been selected. The source is publicly visible, but no permission to copy, modify, or redistribute is granted unless the author adds a license.
