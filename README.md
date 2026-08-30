# Irixi Project Forge

[中文](#中文) · [English](#english)

## 中文

### 简介

Irixi Project Forge 是一套面向非技术产品经理和初学者的跨平台 AI 产品工作流。只要一个 AI 能接收文字，它就能运行 DZ 的核心流程；能否查看项目、开发、测试或上线，再由它实际拥有的工具决定。DZ 能从一个模糊想法开始，也能在讨论、开发、测试甚至上线准备进行到一半时接手并继续。

工作流的短名称是 `dz`。

DZ 不会把“帮我做一个应用”直接理解为立即写代码。它会先用大白话和你说清三件事：想帮谁解决哪件麻烦、这次先做什么和不做什么、准备先从哪一步动手并怎样亲手试。每说清一件都让你看一眼，对了才往下走。

### 最后会得到什么

一个想法适合继续开发时，你最终会得到四样东西：

1. 一个真正可以使用的应用或 Agent；
2. 三份你能看懂并亲自确认的简短记录：想解决哪件麻烦、这次先做什么、准备怎样动手和试用；
3. 可以复查的测试结果，说明哪些已经能用、哪些还没证明；
4. 上线方法、已知风险，以及出问题时怎样恢复。

如果在前期发现这个想法不值得做，DZ 会直接说明原因和更省钱的替代办法，不会为了交付代码而硬做。

简单理解：DZ 负责带路，当前有执行能力的 AI 负责动手；在 Codex 中，动手的就是 Codex。Agent Harness 教程只在幕后提供“怎样记住进度、拆开任务、检查结果”的经验。DZ 已经把这些经验写进自己的规则；每次使用时不会重新运行教程，也不要求用户阅读它。

### 核心能力

- 默认先说结论，使用短句和具体例子，不主动展示内部流程名、英文状态或文件名；
- 普通回复要么最多两个短段落，要么最多四条，不混着堆；通常不超过约 180 个中文字，每轮只问一件事；
- 自动判断当前 AI 只能聊天、能查看项目、能开发，还是还能上线，并据此调整做法；
- 当你回答“不知道”时，提供专业建议、一个有意义的替代方案和低成本验证方法；
- 区分已确认事实、建议、假设、未知项和明确不做的内容；
- 主动指出用户采用、数据、AI 必要性、模型质量、权限、隐私、成本、失败恢复和运营方面的漏洞；
- 每次增加一项有实际用途的新能力时，先找有没有合适的现成“小零件”，再判断该直接用、改造、只学做法后自己写，还是不用；
- 不让非技术用户选择框架或为技术正确性背书；
- 在“想解决哪件麻烦”“这次做什么、不做什么”“准备先做哪一步、做完怎样试”分别被你看过并点头前，不开始正式制作；
- 用真实路径和可复现证据判断完成，而不是只看 Mock、构建成功、部署命令或可访问网址；
- 可以中途接管当前任务，保留有效工作，不强迫用户重新回答已经明确的问题。

### 先找现成的小零件

DZ 不会为了一个好用的小部分，把别人的整台“机器”搬进你的产品。它会先说清我们到底需要哪个小动作，再把这个动作拆开去找。例如“上传文件”可以拆成选择文件、判断格式、显示进度、失败重试和保存结果，而不是直接寻找并照搬一套完整的文件管理系统。

这项检查放在原来的流程里，不会多出一套要你学习的步骤：

1. “想解决哪件麻烦”已经写给你看、并由你点头后，DZ 用约 10–20 分钟快速看三到五种现成办法，判断有没有值得继续看的小零件；
2. “这次做什么和不做什么”已经写给你看、并由你点头后，DZ 再认真检查最合适的一到三个。许可证、依赖和能否安全使用由 DZ 判断；你只需决定是否接受它带来的费用、内容外传或使用变化；
3. 最后只给出四种结论之一：使用维护好的软件包或稳定接口、改造许可清楚的小模块、只学它的做法后独立实现、明确不用。

GitHub 搜索只代表找到了候选，不代表已经获准使用，也不代表它安全或适合当前产品。Star 多、Demo 能跑都不能替代许可证、来源、安全、维护和真实接入测试。没有清楚许可证的代码不复制，也不拿来运行；能用官方软件包或稳定接口时，优先不剪取别人项目里的内部文件。采用的小零件会固定到不会悄悄变化的代码记录或实际安装包，隔在我们自己的接口后面，并留下来源、所需声明、自己的测试、负责人和移除办法。GitHub 对无许可证公开仓库的说明见[官方文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。

如果当前 AI 不能联网，DZ 会直说“这次没有实际搜索”，然后给出不含私密内容的搜索词和检查表，不会编造项目、许可证或维护情况。

### DZ 怎么跟你说话

“小白能懂”是硬要求，不是语气装可爱：

- 默认你没学过产品和技术，不让你先学术语再做项目；
- 一次只讲一件事，只说最重要的后果，只问一个能凭生活经验回答的问题；
- 不直接扔出“目标、范围、边界、验证、部署、权限、数据”这类大词，而是说清谁做什么、会看到什么、哪里可能出问题；
- 你说“没听懂”时，它会停下来，换成你这个项目里的一个具体例子，不会拿更多术语解释术语；
- 语气尊重成年人，不哄人、不卖萌、不把简单说成啰嗦。

每次回复前，DZ 会在心里检查：一个第一次接触这件事的人，能不能复述“会发生什么、为什么现在要管、我只要回答什么”。复述不了，就重写。

### 在不同 AI 上怎么用

所有平台都使用同一套 DZ 流程。只要能接收文字，就可以使用；能否读取项目、写代码、运行测试或上线，只看当前平台实际开放的工具，不看品牌。WorkBuddy、Kimi、智谱、DeepSeek、Claude、Gemini、Codex、私有模型和以后出现的新平台都不需要分别开发不同版本。后文的 Codex 只是一个完整接入示例。

| 平台提供的入口 | 统一加载方式 | 实际结果 |
|---|---|---|
| 支持 Skill 或 `SKILL.md` | 安装完整仓库目录 | 使用完整流程，并自动调用该平台真正开放的工具 |
| 支持系统提示词、项目指令或 API | 加载 [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md)，再传入能力说明 | 使用同一流程；接入程序负责保存对话、执行工具和控制权限 |
| 支持文件上传或知识库 | 上传通用提示词，并按需加入相关参考文件 | 使用同一流程；能否动手开发取决于会话工具 |
| 只能普通聊天 | 粘贴通用提示词，用 `DZ启动：` 开始 | 完成脑暴、确认边界和交接；不会假装已经开发或测试 |

通用提示词是一份安全、可单文件使用的精简版。若要让 API 版获得与完整 Skill 相同的技术手册和产物模板，接入程序还应按 `dz-manifest.json` 的 `reference_sets` 提供按需读取，不要把所有资料一次性塞进上下文。

入口取决于 DZ 是怎样装进去的：ChatGPT Desktop 的本地 Skill 和 ChatGPT 网页、桌面、手机里的 Plugin 都输入 `@` 选择 `dz`；Codex CLI 和 IDE 扩展用 `/skills` 选择，或直接输入 `$dz`。只有已经加载了通用提示词的其他 AI 平台才使用：

```text
DZ启动：我想做……我完全不懂产品和技术。请用短句和具体例子，一次只问我一件事。
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

这些英文名称和文件名只在项目内部使用。和小白沟通时，DZ 默认只说“想帮谁解决哪件麻烦”“这次做什么、不做什么”“先做哪一步、做完怎样试”“让它真的做一遍”和“放到网上给别人用前再检查一次”。

### 中途调用与任务接管

你可以在同一个对话或开发任务进行到一半时调用 DZ。它不会自动从头开始，也不会因为缺少流程文档就删除已有代码。

DZ 会先只看不改，用四句短话说明：

1. 别人已经做出了什么；
2. 哪些具体东西可以留下；
3. 哪件事还没人点头，或还没人亲手试过；
4. 现在先做哪一小步，并只问你一个问题。

如果代码已经存在但缺少说明，DZ 不会删除代码。它会先把“想解决哪件麻烦、这次做什么和不做什么、准备怎样动手和试用”补清楚，再留下对得上的部分继续检查。

如果前面三件事已经说定，而现在只是修一个小问题，DZ 会直接继续，不会让你从头再讲。只有这次修改会改变别人怎样使用、会保存什么内容、谁能查看或修改、要花多少钱，或会换掉主要做法时，才重新问受影响的那一件事。

中途接管示例：

```text
@dz 接着做现在这个东西。先别改。用四句短话告诉我：别人做出了什么、哪些能留、还缺什么、现在先干什么。已经说过的别再问。
```

在使用 `$` 调用 Skill 的 Codex 界面中：

```text
$dz 接着做现在这个东西。别从头问。用短句告诉我哪些已经做好、哪些还没亲手试过，以及现在只做哪一小步。
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
@dz 我想做一个帮小店整理顾客留言的东西。我不懂产品和技术。请用短句和具体例子，一次只问我一件事。先把要做的事说清，再动手。
```

读已有说明：

```text
@dz 读一下这份说明。已经说清的别再问。直接告诉我哪件事还没说清，一次只问一件事。
```

恢复已有项目：

```text
@dz 接着做这个东西。不要从头问。用四句短话告诉我：别人做出了什么、哪些能留、还缺什么、现在先干什么。
```

检查上线准备：

```text
@dz 先别放到网上给别人用。请让它真的做一遍，再告诉我：现在能做什么、还有什么没试、出问题怎样恢复。
```

让 DZ 先找可复用的小零件：

```text
@dz 我想加一个文件上传后失败自动重试的能力。先说清我们真正需要的动作，再找找 GitHub 上有没有合适的小零件。不要搬整个项目；请判断哪些值得用、哪些只值得参考、哪些不该用。
```

在 ChatGPT 里输入 `@` 并选择 `dz`；本地独立 Skill 只出现在 ChatGPT Desktop，打包成 Plugin 后也可用于 ChatGPT 网页和手机。Codex CLI 与 IDE 扩展用 `/skills` 选择或输入 `$dz`。以上入口来自 [OpenAI 官方 Skills 文档](https://developers.openai.com/codex/skills)。

### 目录结构

```text
dz/
├── SKILL.md
├── LICENSE.md
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
    ├── reuse-scout.md
    ├── agent-harness.md
    ├── platform-adapters.md
    ├── codex-native.md
    └── forward-tests.md
```

### 验证

Skill 使用 Codex Skill validator 和 JSON 检查验证结构，并定义十五组新上下文行为测试：

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
12. 面向小白时必须简短、具体，只问一个问题；听不懂时必须换成当前事情里的例子；
13. 同一套 DZ 在聊天型、可开发型和可上线型平台上自动选择合适做法；相同能力不因平台品牌不同而改变；
14. 中途接手时也必须用四句短话说清已经做了什么、什么能留、什么没试、下一步做什么；
15. 先说清真正需要的小动作，再安全寻找和筛选现成零件；不能把公开、Star 或 Demo 当成使用许可和质量证明，也不能在确认动手办法前下载运行陌生代码。

行为测试定义见 [`references/forward-tests.md`](references/forward-tests.md)。

### 许可证

本项目采用 [PolyForm Perimeter License 1.0.1](LICENSE.md)。

你可以下载、使用、修改和分享 DZ，也可以在个人或公司内部使用。但不能把 DZ 换名字、换包装或换平台后，向别人提供一个替代 DZ 的竞争产品或服务；收费和免费都不允许。分发时必须同时保留许可证和其中的 `Required Notice`。如需进行竞争性发行，必须先取得权利人的单独书面授权。

因为这份许可限制竞争性使用，本项目属于“源码公开可用”，不属于 OSI 定义下允许自由竞争和销售的传统开源软件。许可只覆盖本仓库中权利人有权授权的内容；第三方链接、名称和材料仍按各自条款处理。

---

## English

### Overview

Irixi Project Forge is a cross-platform AI product workflow for nontechnical product managers and beginners. Any AI that accepts text can run the DZ core; its actual tools determine whether it can inspect a project, build, test, or release. DZ can start from a rough idea or join halfway through discussion, implementation, testing, or release preparation and continue from the real state.

Its short name is `dz`.

DZ does not interpret “build me an app” as permission to code immediately. It first settles three things in everyday language: who needs help with which trouble, what to do and leave out this time, and what to make first and personally try afterward. You see and approve each one before the work moves on.

### What you get

When an idea is worth building, a DZ project should leave you with four things:

1. An application or agent that can actually be used.
2. Three short records you can understand and confirm: which trouble to solve, what to do this time, and how to make and try it.
3. Reproducible test results showing what works and what is still unproven.
4. A launch approach, known risks, and a recovery plan.

If early discovery shows that the idea is not worth building, DZ explains why and recommends a cheaper alternative instead of producing code for its own sake.

In simple terms: DZ guides the work and the current execution-capable AI does the hands-on work; on Codex, that worker is Codex. The Agent Harness tutorial contributes behind-the-scenes lessons about remembering progress, splitting work, and checking results. DZ has already turned those lessons into its own rules; it does not rerun the tutorial or require the user to read it for every project.

### Core capabilities

- Leads with the answer, uses short sentences and concrete examples, and hides internal state names, English lifecycle labels, and filenames by default.
- Uses either at most two short paragraphs or at most four bullets without mixing both, normally stays under about 120 English words, and asks one question per round.
- Detects whether the current AI can only chat, inspect a project, build it, or also release it, then adjusts the workflow automatically.
- Recommends a professional default, a meaningful alternative, and a cheap validation method when the user is unsure.
- Separates confirmed facts, recommendations, assumptions, unknowns, and explicit non-goals.
- Challenges adoption, data, AI necessity, quality, permission, privacy, cost, recovery, and operational blind spots.
- For every meaningful new capability, looks for suitable existing “parts,” then decides whether to use, adapt, independently reimplement, or reject them.
- Does not ask a beginner to choose frameworks or certify technical correctness.
- Does not begin formal implementation until the user has separately confirmed which trouble to solve, what to do and leave out this time, and what to make first and how to try it.
- Judges completion by reproducible real-path evidence, not a mock, green build, deploy command, or reachable URL alone.
- Can take over midway, preserve valid work, and avoid repeating decisions already supported by the current task.

### Find existing parts before building

DZ does not import someone else's whole “machine” because one small part looks useful. It first names the exact behavior we need, then searches for that behavior in smaller pieces. For example, “file upload” may become file selection, format checks, progress, retry, and result storage instead of a search for a complete file-management product to copy.

This check lives inside the existing workflow, so the user does not have to learn another process:

1. Once the exact first decision about the trouble is visible and accepted, DZ spends about 10–20 minutes scanning three to five approaches to see whether a useful part probably exists.
2. Once what is included and left out is visible and accepted, DZ deeply reviews the best one to three. DZ owns the license, dependency, and technical-fit checks; you decide only whether to accept changes in cost, information sharing, or user experience.
3. It records one of four outcomes: use a maintained package or stable API, adapt a small clearly licensed module, learn the behavior and implement it independently, or reject it.

A GitHub result is only a candidate, not permission, safety evidence, or product fit. Stars and a working demo do not replace licensing, provenance, security, maintenance, and real integration tests. Code without a clear license is neither copied nor executed. A supported package or stable interface is preferred to cutting internal files from another project. Any adopted part is pinned to an immutable source record or exact resolved artifact, wrapped behind a product-owned interface, and recorded with provenance, required notices, product-owned tests, an owner, and a removal path. See GitHub's [official repository licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

If the current AI cannot access the public web, DZ says that no live search occurred and exports sanitized search phrases plus the review card. It does not invent repositories, licenses, or maintenance facts.

### How DZ talks to you

“A complete beginner can understand it” is a hard requirement, not a childish tone:

- DZ assumes no product or technical vocabulary and does not make you learn terms before making progress.
- It discusses one decision, one important consequence, and one question at a time.
- Instead of labels such as “scope,” “validation,” “deployment,” “permissions,” or “data boundary,” it says who does what, what they will see, and what could actually go wrong.
- If you say you do not understand, it stops and uses one concrete scene from your project. It does not explain jargon with more jargon.
- It speaks to you as a capable adult: respectful, direct, and brief.

Before every reply, DZ silently checks whether someone new to the subject could repeat back what will happen, why it matters now, and the one answer DZ needs. If not, it rewrites the reply.

### Using DZ on different AI platforms

Every platform uses the same DZ workflow. Any AI that accepts text can use it; whether it can read a project, write code, run tests, or release depends only on the tools actually available, never the brand. WorkBuddy, Kimi, Zhipu, DeepSeek, Claude, Gemini, Codex, private models, and future hosts do not need separate DZ versions. Codex appears later only as one complete integration example.

| What the host accepts | Unified loading form | Result |
|---|---|---|
| Skills or `SKILL.md` | Install the full repository bundle | Keep the full workflow and automatically use only the tools actually exposed by that host |
| System prompts, project instructions, or an API | Load [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md), then append a capability card | Keep the same flow; the integration owns history, tool execution, and permissions |
| File upload or a knowledge base | Upload the universal prompt and only the references needed now | Keep the same flow; hands-on delivery depends on the chat's actual tools |
| Plain text chat only | Paste the universal prompt and start with `DZ启动：` | Brainstorm, confirm boundaries, and create a handoff without pretending to have built or tested anything |

The universal prompt is a safe, single-file compact edition. To give an API host the same handbook detail and artifact templates as the full Skill, expose the manifest's `reference_sets` through on-demand retrieval instead of concatenating every resource into every request.

The entry point depends on how DZ was installed. In ChatGPT, type `@` to select `dz`: this covers a local Skill in ChatGPT Desktop and a packaged Plugin on ChatGPT web, desktop, or mobile. In Codex CLI or the IDE extension, run `/skills` or type `$dz`. Only on another AI host that has already loaded the universal prompt, use:

```text
DZ启动：I want to build ... I know nothing about product or software work. Use short sentences and concrete examples, and ask me one thing at a time.
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

Those English names and filenames stay inside the project. With a beginner, DZ says “who needs help with which trouble,” “what to do and leave out this time,” “what to make first and how to try it,” “make it do the real job once,” and “check it again before putting it online for other people.”

### Mid-task takeover

You can invoke DZ halfway through the same conversation or development task. It does not automatically restart and does not delete existing code merely because workflow artifacts are missing.

DZ first inspects without changing anything, then uses four short lines:

1. What the previous person actually made.
2. Which specific parts can stay.
3. What nobody has agreed or personally tried yet.
4. The one small thing to do now, followed by one question.

When code exists without a clear explanation, DZ preserves it as potentially useful work that still needs checking. It writes down which trouble to solve, what to do and leave out this time, and what to make and try first. It asks the user whether those exact sentences are right, then keeps the parts that match.

When those decisions already exist and the task is a bounded defect, DZ resumes from implementation or testing without restarting product discovery. It reopens only the earliest decision affected by a change to experience, data, permissions, cost, architecture, or another material boundary.

Take over in ChatGPT Desktop:

```text
@dz Continue this work. Do not change anything yet. In four short lines, tell me what was made, what can stay, what is missing, and what one small thing to do now. Do not ask me to repeat known facts.
```

Take over where Skills use `$` invocation:

```text
$dz Continue this work without starting over. Use short sentences to tell me what is already done, what nobody has personally tried, and the one small thing to do now.
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
@dz I want to make something that helps a small shop sort customer messages. I know nothing about product or software work. Use short sentences and concrete examples. Ask me one thing at a time, and make sure we understand the job before writing code.
```

Read an existing description:

```text
@dz Read this description. Do not ask again about things it already explains. Tell me the one important thing that is still unclear, then ask one question.
```

Resume an existing project:

```text
@dz Continue this work without starting over. In four short lines, tell me what was made, what can stay, what is missing, and what one small thing to do now.
```

Audit release readiness:

```text
@dz Do not put this online for other people yet. Make it do the real job once, then tell me what works now, what nobody has tried, and how to restore it if something goes wrong.
```

Ask DZ to look for reusable parts:

```text
@dz I want file uploads to retry after a failure. First clarify the exact behavior we need, then look for suitable GitHub parts. Do not import a whole project; tell me what is worth using, what is only worth learning from, and what should be rejected.
```

In ChatGPT, type `@` and select `dz`: a standalone local Skill appears in ChatGPT Desktop, while a packaged Plugin also works on ChatGPT web and mobile. In Codex CLI or the IDE extension, run `/skills` or type `$dz`. These entry points follow the [official OpenAI Skills documentation](https://developers.openai.com/codex/skills).

### Structure

```text
dz/
├── SKILL.md
├── LICENSE.md
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
    ├── reuse-scout.md
    ├── agent-harness.md
    ├── platform-adapters.md
    ├── codex-native.md
    └── forward-tests.md
```

### Validation

The package is checked with the Codex Skill validator and JSON validation, and defines fifteen fresh-context behavioral test families:

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
12. concise, concrete guidance for a complete beginner, with one question and a same-project example after confusion;
13. automatic capability-aware behavior across chat-only, build-capable, and release-capable hosts, with identical behavior for identical capabilities regardless of brand;
14. a mid-task beginner takeover that names what was made, what can stay, what has not been personally tried, and the one next action in four short lines;
15. anchor the exact needed behavior before safely finding and screening existing parts, without treating visibility, stars, or demos as permission or quality proof, and without downloading or running unknown code before the build approach is confirmed.

See [`references/forward-tests.md`](references/forward-tests.md) for the behavioral oracles.

### License

This project is licensed under the [PolyForm Perimeter License 1.0.1](LICENSE.md).

You may download, use, modify, and distribute DZ, including for personal or internal business use. You may not rename, repackage, port, or otherwise provide DZ to others as a competing substitute, whether paid or free. Distributions must retain the license and its `Required Notice`. A separate written license from the rights holder is required for a competing distribution.

Because the license restricts competing use, this is source-available software rather than open source under the OSI definition, which requires free redistribution. The license applies only to material in this repository that the rights holder is entitled to license; third-party links, names, and materials remain subject to their own terms.
