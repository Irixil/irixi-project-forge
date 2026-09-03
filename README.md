# Irixi Project Forge

[中文](#中文) · [English](#english)

## 中文

### 简介

Irixi Project Forge 是一套面向非技术产品经理和初学者的跨平台 AI 产品工作流。能粘贴提示词的平台可以手动运行 DZ 的精简核心；只有平台允许安装 Skill 或让 Agent 读取文件，下载的完整版本才能被直接加载。能否查看项目、开发、测试或上线，再由 Agent 实际拥有的工具决定。DZ 能从一个模糊想法开始，也能在讨论、开发、测试甚至上线准备进行到一半时接手并继续。

工作流的短名称是 `dz`。

DZ 不会把“帮我做一个应用”直接理解为立即写代码。它会先用大白话和你说清三件事：想帮谁解决哪件麻烦、这次先做什么和不做什么、准备先从哪一步动手并怎样亲手试。每说清一件都让你看一眼，对了才往下走。

### 下载后，一分钟让 Agent 开始使用

1. [下载完整 ZIP](https://github.com/Irixil/irixi-project-forge/archive/refs/heads/main.zip) 并解压；不要只保存一份 `SKILL.md`。
2. 能安装 Skill 的平台，导入整个文件夹并选择 `DZ — Irixi Project Forge`。能读项目文件但不能安装 Skill 的 Agent，把下面这句话发给它：

```text
请完整读取“<DZ 文件夹的绝对路径>/SKILL.md”，按照里面的规则启动 DZ，只按当前步骤读取需要的参考文件。先说明你真实能使用哪些工具，再处理我的事情：<写下想法或当前做到哪里>。
```

3. 支持系统提示词、项目指令或 API 的平台，把 [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md) 的全文放进对应指令栏。只能聊天或上传单个文件的平台，上传它并发送 `DZ启动：<你的事情>`；如果平台不会把上传文件当作工作指令，就先把文件全文粘贴进对话。

**下载不等于已经加载。** Agent 必须获得文件夹读取权限、通过 Skill 入口安装，或在平台支持的指令栏或当前对话中收到通用版全文。完整操作说明见 [`GETTING-STARTED.md`](GETTING-STARTED.md)。

### 最后会得到什么

一个想法适合继续开发，并且当前平台真的能读写项目、运行和检查时，你最终会得到四样东西：

1. 一个真正可以使用的应用或 Agent；
2. 三份你能看懂并亲自确认的简短记录：想解决哪件麻烦、这次先做什么、准备怎样动手和试用；
3. 可以复查的测试结果，说明哪些已经能用、哪些还没证明；
4. 上线方法、已知风险，以及出问题时怎样恢复。

如果在前期发现这个想法不值得做，DZ 会直接说明原因和更省钱的替代办法，不会为了交付代码而硬做。

如果当前平台只能聊天，DZ 会完成讨论、三次确认和一份可交给开发型 AI 的接力说明；它不会假装已经做出或试过应用。

简单理解：DZ 负责带路，当前有执行能力的 AI 负责动手；在 Codex 中，动手的就是 Codex。Hubo Agent Harness 是设计参考，不是运行依赖。DZ 已把其中“保存状态、拆开任务、拿证据说话、中断后恢复”的做法变成自己的规则和可运行项目账本；使用 DZ 时不会重新运行教程，也不要求用户阅读它。

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
- 可以中途再次接管当前任务，把所有旧记录和后来新增的操作与项目现状重新对齐，先汇报并讨论接下来的做法，再从用户确认的当前位置继续；
- 每次有效动作后记录做了什么、证据在哪里、还差什么和下一步是什么；在能再次读取同一项目的环境里可以换对话恢复，普通聊天则带上导出的交接记录；
- 把“这次工作能不能停”“用户是否决定收尾”“产品是否真的试过”分开，不用验收把用户困住。

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

### 风险不会变成死胡同

发现隐私、费用、公开发布、数据丢失或恢复困难等风险时，DZ 不会只说“不行”。它会先用大白话告诉你：准备做什么、最坏会怎样、影响谁、风险有多大、更稳妥的做法是什么、出问题能不能恢复。

要花钱、给外部发消息或写数据、删除、搬数据、公开发布、操作生产环境、使用敏感资料，或做其他会产生实际后果的动作时，不管风险被写成低、中还是高，都必须针对这一次具体动作单独确认。如果你确实有权决定并明确接受，DZ 就继续执行，同时把风险和没有试过的部分如实保留下来。账本会发出一张“一次性通行条”，只对应你看到的动作、当前版本、使用位置、金额上限和截止时间；任何一项改变或通行条到期，都要重新确认。动作完成、失败或取消也会用掉它。真正调用外部工具的平台还必须在 AI 不能改写的审批入口里执行同样限制。

你随时可以暂停、取消或先收尾。DZ 会留下交接记录，但不会把“我先不做了”“网址能打开”或“我接受风险”写成“已经全部验证通过”。“DZ 已取消”只表示 DZ 不再发起新动作，不代表外部网站或已经启动的任务一定停下；能取消时只发送一次有时间限制的取消信号，再查一次是否停下，不会借着取消反复操作。只有缺少账号或工具、你无权替别人决定、平台本身不允许、必要条件不存在，或没有使用第三方内容的权利时，动作才会真正卡住。

### 在不同 AI 上怎么用

所有平台都使用同一套 DZ 流程，不按品牌另写一套。能接收文字的平台至少可以手动粘贴通用版；要自动读取下载的完整文件夹，平台还必须支持 Skill 或文件读取。能否读取项目、写代码、运行测试或上线，只看当前平台实际开放的工具。WorkBuddy、Kimi、智谱、DeepSeek、Claude、Gemini、Codex、私有模型和以后出现的新平台都按这条规则处理，但这不代表我们已经逐个平台保证原生兼容。后文的 Codex 只是一个完整接入示例。

| 平台提供的入口 | 统一加载方式 | 实际结果 |
|---|---|---|
| 支持 Skill 或 `SKILL.md` | 安装完整仓库目录 | 使用完整流程，并根据平台明确提供的工具决定能做什么 |
| 支持系统提示词、项目指令或 API | 加载 [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md)，再传入能力说明 | 使用同一流程；接入程序负责保存对话、执行工具和控制权限 |
| 支持文件上传或知识库 | 上传通用提示词，并按需加入相关参考文件 | 使用同一流程；能否动手开发取决于会话工具 |
| 只能普通聊天 | 粘贴通用提示词，用 `DZ启动：` 开始 | 完成脑暴、确认边界和交接；不会假装已经开发或测试 |

通用提示词是一份安全、可单文件使用的精简版。若要让 API 版获得与完整 Skill 相同的技术手册和产物模板，接入程序还应按 `dz-manifest.json` 的 `reference_sets` 提供按需读取，不要把所有资料一次性塞进上下文。

入口取决于 DZ 是怎样装进去的：在支持插件的界面中打开 `@` 菜单，选择“DZ — Irixi Project Forge”（选中后可能显示为 `@dz`）；在 Codex CLI 或 IDE 中，用 `/skills` 选择 `dz`，或直接输入 `$dz`。只有已经加载通用提示词的其他 AI 平台才使用：

```text
DZ启动：我想做……我完全不懂产品和技术。请用短句和具体例子，一次只问我一件事。
```

### 自动适配接口（给平台开发者，普通用户可跳过）

普通用户不需要配置下面这些内容；能粘贴通用提示词就可以使用 DZ。

仓库提供一套公开适配入口：

- [`dz-manifest.json`](dz-manifest.json) 告诉加载器有哪些入口、参考资料和工作流版本标签；
- [`adapters/dz-capabilities.schema.json`](adapters/dz-capabilities.schema.json) 描述当前 AI 真实拥有的能力；
- [`schemas/dz-project-state.schema.json`](schemas/dz-project-state.schema.json) 规定跨对话项目状态的统一格式；
- [`scripts/dz_state.py`](scripts/dz_state.py) 在能运行 Python 的平台创建、检查、恢复和生成项目账本；
- [`scripts/dz_codex_stop_hook.py`](scripts/dz_codex_stop_hook.py) 在账本仍显示“正在做”时向 Codex 请求一次续跑；是否真的继续还受 Hook 信任、策略和其他 Stop hook 影响；
- [`adapters/README.md`](adapters/README.md) 给出加载顺序和能力说明示例；
- [`references/platform-adapters.md`](references/platform-adapters.md) 规定怎样自动选择“只引导、可查看、可开发、可上线”的做法。

公开加载地址：[`dz-manifest.json`](https://raw.githubusercontent.com/Irixil/irixi-project-forge/main/dz-manifest.json)。有联网和系统指令权限的接入程序可以先读取它，再按清单加载对应入口。这个 `main` 地址会随仓库更新；需要每次得到完全相同内容的接入程序，应把网址中的 `main` 换成一次明确的 Git 提交编号。

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

在能够读写项目并运行状态工具的环境里，DZ 用 `.dz/state.json` 保存当前快照，用 `.dz/journal.jsonl` 追加每次重要变化，并由状态工具生成 `PROJECT.md`、`docs/sdlc/work-items.md` 和 `docs/sdlc/issues.md`。用户确认过的“为什么做、做成什么、怎么做”三份原文会合成一枚内容指纹，每项施工都绑在这枚指纹上；只要其中一份改变，旧施工和旧证明就不能悄悄沿用。每次检查前还要保存当前代码、构建或线上版本的真实观察证明，并生成一个新的检查批次；哪怕版本名字没变，重新设置检查对象也要重新跑完本批次的每条约定。旧结果只保留为历史。

开发、试用或上线后发现的重要问题也会单独记下来。DZ 自己判断它应该回到当前修理任务、补充用户会遇到的情况、修改动手方法、放到以后、重新讨论为什么做，还是先作为上线反馈观察；不会让小白选择技术分类，也不会把所有问题都塞进 PRD。只是代码没有做到原先已经说定的事，DZ 可以直接做小修并留下记录；如果会改变用户怎么用、保存或传出什么、谁能看到、花多少钱或这次做多少，必须先把原话、建议改法和影响完整给用户看，等用户同意后再动。

“已经改了”不等于“真的好了”。没有亲手跑过能重现原问题的检查时，DZ 必须写成“已经改了，但还没证明真的解决”；只有当前版本实际通过检查，并留下以后能重复运行的防复发检查，才能写成已经解决。

在 Codex 中，建账命令还会把一段带标记的接续说明合并进项目 `AGENTS.md`，不会覆盖项目原有规则。以后从这个具体项目文件夹新建任务，或者在做到一半时再次调用 DZ，它会先运行只读的 `resume-report`：读完每条有效日志、没有解决的问题和后来对问题做过的处理，并在 Git 可用时把上次保存的文件状态与现在比较。上次写下的“下一步”只是一条旧建议；如果中间已经有人继续修改，DZ 必须保留并说明这些变化，不能退回旧位置。无法可靠判断修改时间时，它会直说，不会猜。它先用大白话汇报现在做到哪、哪些能留下、发现了什么问题、哪里冲突、接下来建议怎样做，并和用户确认后再继续。旧 DZ 项目会先报告说明过期，把 `install-guidance` 列入建议；用户确认接管以后再刷新。

账本格式已升级到 `1.1`。旧的 `1.0` 项目必须先运行迁移；工具会备份旧快照和日志、保留历史，并把无法确定属于哪份决定或哪次检查的内容降为“还没证明”，不会替用户猜。这个本地工具能检查前后记录是否一致、证明文件是否被改动，却不能证明 AI 写下的“用户已同意”或“测试真的执行过”一定真实，因为能改项目的 AI 也可能改账本并调用工具。需要防篡改的批准或验证，必须由 AI 无法控制的平台审批入口和测试执行器签发。其他接入程序要保存同样结构；普通聊天只能导出可复制的交接记录。`PROJECT.md` 不代替完整决定或验证证据。

这些英文名称和文件名只在项目内部使用。和小白沟通时，DZ 默认只说“想帮谁解决哪件麻烦”“这次做什么、不做什么”“先做哪一步、做完怎样试”“让它真的做一遍”和“放到网上给别人用前再检查一次”。

### 中途调用与任务接管

你可以在同一个对话或开发任务进行到一半时再次调用 DZ。能读取项目时，它会把所有可见讨论、以前的决定、项目账本、日志和项目现在的文件对一遍，也会查明上次记录以后又改了什么。它不会把项目退回上次停下的位置，也不会因为缺少流程文档就删除中间做出的东西。它先汇报完整现状和接下来的建议做法，让用户更正、补充并讨论；用户确认后才继续。不能读取以前聊天或项目时，它会直说并只索要最小交接记录。想让新任务自动接续，要从具体项目文件夹打开 Agent；只打开装着多个项目的上一级文件夹时，Agent 可能不知道该接哪一个。

DZ 会先只看不改，用四句短话说明：

1. 上次记录以前已经做出了什么；
2. 上次记录以后又发生了什么，哪些具体东西可以留下；
3. 现在有什么冲突，或哪件事还没人点头、没人亲手试过；
4. 接下来建议按什么顺序做、为什么，并请用户更正或确认后一起决定怎样执行。

如果代码已经存在但缺少说明，DZ 不会删除代码。它会先把“想解决哪件麻烦、这次做什么和不做什么、准备怎样动手和试用”补清楚，再留下对得上的部分继续检查。

如果前面三件事已经说定，而现在只是修一个小问题，DZ 会直接继续，不会让你从头再讲。只有这次修改会改变别人怎样使用、会保存什么内容、谁能查看或修改、要花多少钱，或会换掉主要做法时，才重新问受影响的那一件事。

在支持 `@` 插件菜单的界面里，中途接管示例：

```text
@dz 重新接管现在这个东西。先别改。把以前的记录和现在的内容对一遍，用四句短话告诉我：以前做了什么、后来又改了什么、现在还缺什么、你准备怎样继续。先和我确认再行动。
```

在使用 `$` 调用 Skill 的 Codex 界面中：

```text
$dz 重新接管现在这个东西。别从头问，也别退回旧位置。用短句告诉我以前做了什么、后来又改了什么、哪些还没亲手试过，以及你准备怎样继续。先和我确认再行动。
```

### 三份技术手册的接入

DZ 整合了以下手册的流程：

- *AI 产品 Vibe Coding 通用技术栈手册*；
- *AI 产品 Vibe Coding 通用前端技术栈手册*；
- *AI Agent 产品上线部署手册*。

这三份手册不是可看可不看的参考。第三次确认完成后，DZ 会把适用内容拆成必须入账的施工项：所有项目走通用开发路线；有界面的项目增加代表页面、真实后台、浏览器和中断恢复路线；需要给别人使用时增加账号、隔离、密钥、存储、监控、费用、恢复、上线检查、README 和交接；上线后增加结果、故障、成本和反馈路线。每一项都要留下实际结果，不能只写“参考过手册”。具体框架和云平台仍是可替换的建议，不是强制答案。

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
- 使用 `.dz/state.json`、追加日志和工作账本保存跨对话进度；
- 使用仓库内的状态工具检查暂停、恢复、风险决定和完成证据；
- 插件安装时使用 Stop hook 在结束前检查账本；第一次发现仍在做会请求 Codex 再继续一次，但平台策略仍可能拒绝；第二次仍未收好则带警告放行并保留未完状态，避免死循环；
- 使用当前计划跟踪已批准计划的执行；
- 只对真正独立的任务使用子代理或 worktree；
- 使用沙箱、审批、测试、eval、CI 和 review 形成分层控制；
- 使用部署 Skill 或官方文档处理厂商特定步骤。

仓库本身同时是一个可校验的 Codex 插件包和一个可单独安装的 Skill。插件会自带本机 Stop hook，但它只会请求一次收尾续跑，也不保证请求被 Codex 接受；本 hook 不会重复请求，因此不会由它自己造成死循环。它不是安全边界，持续记忆仍来自项目账本、项目规则和验证证据。详细映射见 [`references/codex-native.md`](references/codex-native.md)，hook 说明见 [`references/codex-stop-hook.md`](references/codex-stop-hook.md)，开源执行底座见 [`openai/codex`](https://github.com/openai/codex)。

### 在 Codex 中安装（示例）

把仓库克隆为 `dz`，然后运行自带安装脚本。脚本只把独立 Skill 需要的内容复制到用户级 Skills 目录，不复制插件内层入口，因此 Codex 菜单里只出现一个 DZ：

```bash
git clone https://github.com/Irixil/irixi-project-forge.git dz
cd dz
python3 scripts/install_local_skill.py
```

以前按照旧说明把整个仓库软链接到 `~/.agents/skills/dz`，导致出现两个入口时，在仓库目录运行：

```bash
python3 scripts/install_local_skill.py --replace
```

这个命令会把旧软链接移到 `~/.agents/skill-backups/`，不会删除它指向的仓库。以后仓库更新后，必须再次运行 `python3 scripts/install_local_skill.py --replace`，把新文件复制到安装位置；只重启 Codex 不会更新那份副本。重新安装后再重启 Codex，并新建一个任务。

本地 Skill 和插件安装二选一，避免两个 `dz` 版本互相遮挡。不要只复制 `skills/dz/` 内层目录，它需要同一仓库根目录中的完整工作流和参考文件。

插件会从同一版本目录自动加载 Stop hook，并要求你在 Codex 的 `/hooks` 中核对后信任。若只装本地 Skill，hook 是可选项：按 [`assets/codex-hooks/README.md`](assets/codex-hooks/README.md) 人工检查并合并模板，绝不覆盖项目已有的 `.codex/hooks.json`。

当前仓库已经是可校验的插件包，但还没有发布成可用 Marketplace 命令一键安装的市场源；因此本节只给出已经验证过的本地 Skill 安装方法。

### 使用方式

从模糊想法开始：

```text
$dz 我想做一个帮小店整理顾客留言的东西。我不懂产品和技术。请用短句和具体例子，一次只问我一件事。先把要做的事说清，再动手。
```

读已有说明：

```text
$dz 读一下这份说明。已经说清的别再问。直接告诉我哪件事还没说清，一次只问一件事。
```

恢复已有项目：

```text
$dz 重新接管这个东西。先别改。读完以前的记录，再和现在的文件对一遍。用四句短话告诉我：以前做了什么、后来改了什么、哪里还说不准、你建议接下来怎样做。先和我讨论，等我确认后再动手。
```

检查上线准备：

```text
$dz 先别放到网上给别人用。请让它真的做一遍，再告诉我：现在能做什么、还有什么没试、出问题怎样恢复。
```

让 DZ 先找可复用的小零件：

```text
$dz 我想加一个文件上传后失败自动重试的能力。先说清我们真正需要的动作，再找找 GitHub 上有没有合适的小零件。不要搬整个项目；请判断哪些值得用、哪些只值得参考、哪些不该用。
```

上面是 Codex 的写法。在支持插件 `@` 菜单的平台里，打开 `@` 菜单并选择“DZ — Irixi Project Forge”；选中后可看到 `@dz`。不同宿主的入口可能不同，但加载后执行的是同一套 DZ 规则。Codex 的 Skill 入口见 [OpenAI 官方 Skills 文档](https://developers.openai.com/codex/skills)。

### 目录结构

```text
dz/
├── .codex-plugin/
│   └── plugin.json
├── SKILL.md
├── GETTING-STARTED.md
├── LICENSE.md
├── dz-manifest.json
├── skills/
│   └── dz/
│       ├── SKILL.md
│       └── agents/openai.yaml
├── scripts/
│   ├── dz_state.py
│   ├── dz_codex_stop_hook.py
│   └── install_local_skill.py
├── hooks/
│   └── hooks.json
├── schemas/
│   └── dz-project-state.schema.json
├── tests/
│   ├── test_dz_state.py
│   ├── test_dz_codex_stop_hook.py
│   └── test_install_local_skill.py
├── assets/
│   ├── project/AGENTS.md
│   └── codex-hooks/
│       ├── README.md
│       └── hooks.json.example
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
    ├── project-state.md
    ├── issue-learning-loop.md
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
    ├── codex-stop-hook.md
    └── forward-tests.md
```

### 验证

Skill 与插件分别通过结构校验；项目账本有四十二组可运行测试，Codex 收尾检查有十组，单入口安装有三组，合计五十五组；另定义二十组新上下文行为测试：

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
14. 中途接手时也必须用四句短话说清以前有什么、后来改了什么、哪里还说不准、准备怎样继续，并等用户确认；
15. 先说清真正需要的小动作，再安全寻找和筛选现成零件；不能把公开、Star 或 Demo 当成使用许可和质量证明，也不能在确认动手办法前下载运行陌生代码；
16. 具体风险讲清并由有权决定的人接受后，继续执行该次动作，同时保留风险和未验证项；
17. 暂停后停止动作，换对话从账本恢复，取消后保留文件且不谎称完成；
18. 用户可以随时收尾，但构建成功、网址可访问或接受风险都不能冒充验证通过；
19. 中途再次调用时，必须把旧记录和后来新增的操作重新对齐，先汇报完整现状和准备怎样执行，用户确认后再继续，不能退回旧位置。
20. 开发中发现的重要问题必须留下记录并由 DZ 自动分流；小修不反复打扰用户，改变原先约定时先给用户看完整改法；只有实际检查通过并留下防复发办法才能说问题解决。

行为测试定义见 [`references/forward-tests.md`](references/forward-tests.md)。

### 许可证

本项目采用 [PolyForm Perimeter License 1.0.1](LICENSE.md)。

你可以下载、使用、修改和分享 DZ，也可以在个人或公司内部使用。但不能把 DZ 换名字、换包装或换平台后，向别人提供一个替代 DZ 的竞争产品或服务；收费和免费都不允许。分发时必须同时保留许可证和其中的 `Required Notice`。如需进行竞争性发行，必须先取得权利人的单独书面授权。

因为这份许可限制竞争性使用，本项目属于“源码公开可用”，不属于 OSI 定义下允许自由竞争和销售的传统开源软件。许可只覆盖本仓库中权利人有权授权的内容；第三方链接、名称和材料仍按各自条款处理。

---

## English

### Overview

Irixi Project Forge is a cross-platform AI product workflow for nontechnical product managers and beginners. A host that accepts pasted instructions can manually run the compact DZ core. Direct loading of the downloaded full edition requires Skill installation or file access. The agent's real tools determine whether it can inspect a project, build, test, or release. DZ can start from a rough idea or join halfway through discussion, implementation, testing, or release preparation and continue from the real state.

Its short name is `dz`.

DZ does not interpret “build me an app” as permission to code immediately. It first settles three things in everyday language: who needs help with which trouble, what to do and leave out this time, and what to make first and personally try afterward. You see and approve each one before the work moves on.

### Start it in any agent in one minute

1. [Download the complete ZIP](https://github.com/Irixil/irixi-project-forge/archive/refs/heads/main.zip) and extract it. Do not save only `SKILL.md`.
2. On a host that installs Skills, import the complete folder and select `DZ — Irixi Project Forge`. For a file-capable agent without Skill installation, send:

```text
Read “<absolute path to the DZ folder>/SKILL.md” completely and start DZ under its rules. Load only the references needed for the current step. First state which tools you can truly use, then handle my request: <describe the idea or current state>.
```

3. On a host with system instructions, project instructions, or an API, place the full contents of [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md) in that instruction field. On a chat-only or one-file-upload host, upload it and send `DZ启动: <your request>`; if the host does not treat uploads as working instructions, paste the file's full contents into the chat first.

**Download is not load.** The agent must receive folder access, a Skill installation, or the full universal edition through a supported instruction field or the current conversation. See [`GETTING-STARTED.md`](GETTING-STARTED.md) for complete platform-neutral instructions.

### What you get

When an idea is worth building and the current host can actually read, write, run, and check the project, a DZ project should leave you with four things:

1. An application or agent that can actually be used.
2. Three short records you can understand and confirm: which trouble to solve, what to do this time, and how to make and try it.
3. Reproducible test results showing what works and what is still unproven.
4. A launch approach, known risks, and a recovery plan.

If early discovery shows that the idea is not worth building, DZ explains why and recommends a cheaper alternative instead of producing code for its own sake.

On a chat-only host, DZ completes the discussion, three confirmations, and a handoff for an execution-capable AI. It never pretends the application was built or tested.

In simple terms: DZ guides the work and the current execution-capable AI does the hands-on work; on Codex, that worker is Codex. Hubo Agent Harness is a design reference, not a runtime dependency. DZ turns its lessons about durable state, small work items, evidence, and interruption recovery into DZ rules and an executable project ledger. It does not rerun the tutorial or require users to read it.

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
- Can re-enter midway, reconcile all prior records and later work with the current project, report and discuss the proposed execution, then continue from the user-confirmed present without discarding valid work or repeating settled decisions.
- Records each meaningful action, its evidence, remaining work, and next action. A fresh task can recover when it can reopen the same project; plain chat must carry the exported handoff.
- Separates whether work may stop, whether the user chose to close, and whether the product is actually verified.

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

### Risk does not become a dead end

When DZ finds privacy, spending, public-release, data-loss, or recovery risk, it does not stop at “no.” It explains the intended action, worst credible consequence, affected people, severity, safer option, and recovery path in ordinary language.

Spending, external messages or writes, deletion, migration, public release, production access, sensitive-data use, and other materially consequential actions require fresh authorization for the exact action regardless of whether the displayed severity is low, medium, or high. If you have authority and knowingly accept it, DZ continues within that scope while preserving the risk and any unverified checks. The ledger issues a one-action lease bound to the reviewed action, accepted decisions, target ID, revision, environment, spending ceiling when applicable, and expiry. Any bound fact change or expiry requires fresh authorization; completion, failure, or cancellation consumes the lease. A real tool-using host must enforce the same action ID, bounds, and expiry through an approval boundary the model cannot rewrite.

You may pause, cancel, or close at any time. DZ leaves an honest handoff, but it never turns “stop here,” a reachable URL, or accepted risk into “fully verified.” “DZ cancelled” means DZ starts no new action; it does not prove that an external job stopped. Where cancellation is available, DZ sends one time-bounded cancellation signal, checks status once, and does not keep acting under cancellation authority. An action is genuinely blocked only when an account or capability is missing, the user lacks authority, the host forbids it, a required external condition does not exist, or third-party rights are unavailable.

### Using DZ on different AI platforms

Every platform uses the same DZ workflow instead of a brand-specific edition. A host that accepts text can at least receive the universal edition manually; automatic loading of the downloaded full folder also requires Skill support or file access. Whether it can read a project, write code, run tests, or release depends only on the tools actually available. WorkBuddy, Kimi, Zhipu, DeepSeek, Claude, Gemini, Codex, private models, and future hosts all follow this rule, but this is not a claim of tested native compatibility with every host. Codex appears later only as one complete integration example.

| What the host accepts | Unified loading form | Result |
|---|---|---|
| Skills or `SKILL.md` | Install the full repository bundle | Keep the full workflow and decide what can be done from tools the host explicitly exposes |
| System prompts, project instructions, or an API | Load [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md), then append a capability card | Keep the same flow; the integration owns history, tool execution, and permissions |
| File upload or a knowledge base | Upload the universal prompt and only the references needed now | Keep the same flow; hands-on delivery depends on the chat's actual tools |
| Plain text chat only | Paste the universal prompt and start with `DZ启动：` | Brainstorm, confirm boundaries, and create a handoff without pretending to have built or tested anything |

The universal prompt is a safe, single-file compact edition. To give an API host the same handbook detail and artifact templates as the full Skill, expose the manifest's `reference_sets` through on-demand retrieval instead of concatenating every resource into every request.

The entry point depends on the host. On a plugin surface, open the `@` menu and select “DZ — Irixi Project Forge” (the selected mention may appear as `@dz`). In Codex CLI or the IDE extension, use `/skills` to select `dz`, or type `$dz`. Only on another AI host that has already loaded the universal prompt, use:

```text
DZ启动：I want to build ... I know nothing about product or software work. Use short sentences and concrete examples, and ask me one thing at a time.
```

### Automatic adapter interface (for host developers; ordinary users can skip this)

Ordinary users do not need to configure any of this. Pasting the universal prompt is enough to use DZ.

The repository exposes a public adapter interface:

- [`dz-manifest.json`](dz-manifest.json) tells a loader which entry point to use;
- [`adapters/dz-capabilities.schema.json`](adapters/dz-capabilities.schema.json) describes what the current host can actually do;
- [`schemas/dz-project-state.schema.json`](schemas/dz-project-state.schema.json) defines the cross-task project-state contract;
- [`scripts/dz_state.py`](scripts/dz_state.py) creates, checks, recovers, and renders the project ledger where Python is available;
- [`scripts/dz_codex_stop_hook.py`](scripts/dz_codex_stop_hook.py) requests one continuation attempt when the ledger still says work is active; trust, policy, and other Stop hooks still determine whether Codex continues;
- [`adapters/README.md`](adapters/README.md) defines the loading sequence and provides an example capability card;
- [`references/platform-adapters.md`](references/platform-adapters.md) defines how DZ selects guide, inspect, build, or release behavior.

Public loader URL: [`dz-manifest.json`](https://raw.githubusercontent.com/Irixil/irixi-project-forge/main/dz-manifest.json). An integration with web access and system-instruction control can fetch it first, then load the selected entry point. This `main` URL is an update channel; integrations that require reproducible content should replace `main` with an explicit Git commit SHA.

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

Where the host can read and write the project and run the state tool, DZ stores the current snapshot in `.dz/state.json`, appends important changes to `.dz/journal.jsonl`, and uses the tool to generate `PROJECT.md`, `docs/sdlc/work-items.md`, and `docs/sdlc/issues.md`. The exact accepted Intent, Specification, and Plan form one combined contract digest to which delivery work is bound; changing any one prevents silent reuse. Before evidence is recorded, DZ saves inspectable proof of the observed code, build, or deployment and creates a fresh target epoch. Resetting the target requires every criterion to run again even when the visible revision and environment text are unchanged. Old results remain history.

Material problems found during implementation, testing, use, or production are recorded separately. DZ chooses whether each one belongs with current repair work, a user-visible product decision, the technical approach, later work, the reason for the product, or production feedback. It never asks a beginner to choose technical categories and never dumps every problem into the PRD. A bounded defect inside already accepted behavior may be repaired without duplicate product approval. If the change affects how people use it, what is kept or sent, who can access it, material cost, or current scope, DZ first shows the old wording, complete proposed wording, and concrete impact, then waits for acceptance.

“Changed” is not “fixed.” Until a check actually exercises the former failure, DZ records the issue as implemented but unproven. It becomes verified only when the current target passes and a repeatable regression check or equivalent prevention is retained.

On Codex, ledger initialization also merges a marked continuity section into the project's `AGENTS.md` without replacing existing rules. A later task opened from that exact project folder, or a mid-task re-invocation, first runs the read-only `resume-report`. It reads every valid journal record, unresolved issue, and later issue change and, when Git is available, compares the latest saved workspace checkpoint with the current worktree. The saved next action is only an old proposal. DZ preserves work done after the save, names any comparison it cannot make reliably, explains the reconciled present, important problems, and proposed execution in plain language, and waits for the user to correct or confirm it before continuing. For an older DZ project, it proposes `install-guidance` and refreshes the managed guidance only after that takeover confirmation.

State schema `1.1` requires an explicit migration from `1.0`. The tool first backs up the legacy snapshot and journal, preserves history, and downgrades records that cannot honestly be tied to the current contract and target instead of guessing. The local ledger checks consistency and artifact integrity; it is not trusted proof of human approval or test execution when the same AI can write its files and invoke its CLI. Tamper-resistant approvals and Passed claims require a host-controlled approval surface and runner outside the model's write authority. Other integrations must persist the equivalent structure; plain chat can only export a copyable handoff. `PROJECT.md` does not replace product decisions or verification evidence.

Those English names and filenames stay inside the project. With a beginner, DZ says “who needs help with which trouble,” “what to do and leave out this time,” “what to make first and how to try it,” “make it do the real job once,” and “check it again before putting it online for other people.”

### Mid-task takeover

You can invoke DZ again halfway through the same conversation or development task. When it can read the project, it reconciles all visible discussion, accepted decisions, the ledger and journal, the current files, and work performed after the latest save. It does not roll the project back to that save or delete later work merely because workflow records are behind. It first reports the complete current position and proposed execution, lets the user correct and discuss it, and continues only after confirmation. If it cannot read prior conversation or project evidence, it says so and requests the smallest handoff record. For automatic pickup in a new task, open the agent from the exact project folder; a parent folder containing several projects may be ambiguous.

DZ first inspects without changing anything, then uses four short lines:

1. What existed before the latest saved record.
2. What changed afterward and which specific parts can stay.
3. What now conflicts, lacks agreement, or has not been personally tried.
4. What DZ recommends doing next, in what order and why, followed by one question that invites correction and discussion before execution.

When code exists without a clear explanation, DZ preserves it as potentially useful work that still needs checking. It writes down which trouble to solve, what to do and leave out this time, and what to make and try first. It asks the user whether those exact sentences are right, then keeps the parts that match.

When those decisions already exist and the task is a bounded defect, DZ resumes from implementation or testing without restarting product discovery. It reopens only the earliest decision affected by a change to experience, data, permissions, cost, architecture, or another material boundary.

Take over on a surface with the `@` plugin menu:

```text
@dz Take over the project as it exists now. Do not change anything yet. Reconcile prior records with later work, then tell me in four short lines what existed, what changed, what remains uncertain, and how you propose to continue. Confirm it with me before acting.
```

Take over where Skills use `$` invocation:

```text
$dz Take over the project as it exists now without restarting or returning to the old stopping point. Use short sentences to explain what existed, what changed later, what nobody has personally tried, and how you propose to continue. Confirm it with me before acting.
```

### Integration with the three handbooks

DZ incorporates the workflows from:

- *AI Product Vibe Coding General Technology Stack Handbook*;
- *AI Product Vibe Coding General Frontend Technology Stack Handbook*;
- *AI Agent Product Launch and Deployment Handbook*.

These handbooks are not optional reading. After the third confirmation, DZ expands every applicable route into required ledger work: the general build route for every project; representative-page, real-backend, browser, interruption, and recovery work for a UI; identity, isolation, secrets, storage, monitoring, cost, recovery, production checks, README, and handoff when other people will use it; and result, incident, cost, and feedback work after release. Every item needs real evidence. Frameworks and cloud providers remain replaceable recommendations rather than mandatory answers.

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
- `.dz/state.json`, an append-only journal, and the work ledger for cross-task progress;
- the repository state tool for pause, recovery, risk decisions, and evidence checks;
- the bundled Stop hook for a final ledger check: it requests one continuation for an active run, subject to host policy, then permits a warned second stop while preserving the unfinished state so the hook cannot loop by itself;
- the current plan for execution under an accepted implementation plan;
- subagents and worktrees only for genuinely independent work;
- sandboxes, approvals, tests, evals, CI, and review as layered controls;
- provider Skills or official documentation for deployment-specific steps.

The repository is both a validated Codex plugin bundle and a standalone Skill. The local Stop hook requests one bounded closeout continuation; Codex may still decline it because of trust, policy, or another Stop hook. This hook does not repeat its own request, is not an infinite runner, and is not a security boundary. Durable supervision still comes from project state, project rules, and verification evidence. See [`references/codex-native.md`](references/codex-native.md), [`references/codex-stop-hook.md`](references/codex-stop-hook.md), and the open-source [`openai/codex`](https://github.com/openai/codex) harness.

### Installation on Codex (example)

Clone the repository as `dz`, then run the bundled installer. It copies only the standalone Skill contents into the user Skills directory and omits the nested plugin entry, so Codex shows one DZ entry:

```bash
git clone https://github.com/Irixil/irixi-project-forge.git dz
cd dz
python3 scripts/install_local_skill.py
```

If the previous instructions symlinked the whole repository to `~/.agents/skills/dz` and produced two entries, run this from the repository:

```bash
python3 scripts/install_local_skill.py --replace
```

This moves the old symlink to `~/.agents/skill-backups/` and does not delete the repository it points to. After a later repository update, run `python3 scripts/install_local_skill.py --replace` again to copy the new files into the installed Skill; restarting Codex alone cannot update that copied package. Then restart Codex and open a fresh task.

Choose either the local Skill or the plugin installation so two `dz` versions do not shadow each other. Do not copy `skills/dz/` by itself; that wrapper needs the canonical workflow and references at the same repository root.

The plugin loads its Stop hook from the same version and asks you to inspect and trust it through Codex `/hooks`. With a standalone local Skill, the hook is optional: follow [`assets/codex-hooks/README.md`](assets/codex-hooks/README.md) to review and merge the inert template without overwriting an existing project `.codex/hooks.json`.

The repository is a valid plugin bundle, but it has not yet been published as a marketplace source with a one-command marketplace install. This section therefore documents only the locally validated Skill installation.

### Usage

Start from a rough idea:

```text
$dz I want to make something that helps a small shop sort customer messages. I know nothing about product or software work. Use short sentences and concrete examples. Ask me one thing at a time, and make sure we understand the job before writing code.
```

Read an existing description:

```text
$dz Read this description. Do not ask again about things it already explains. Tell me the one important thing that is still unclear, then ask one question.
```

Resume an existing project:

```text
$dz Take over this project again without editing yet. Read all saved records and compare them with the current files. In four short lines, tell me what existed, what changed later, what is still uncertain, and how you recommend proceeding. Discuss it with me and wait for my confirmation before acting.
```

Audit release readiness:

```text
$dz Do not put this online for other people yet. Make it do the real job once, then tell me what works now, what nobody has tried, and how to restore it if something goes wrong.
```

Ask DZ to look for reusable parts:

```text
$dz I want file uploads to retry after a failure. First clarify the exact behavior we need, then look for suitable GitHub parts. Do not import a whole project; tell me what is worth using, what is only worth learning from, and what should be rejected.
```

The examples above use Codex. On a plugin surface with an `@` menu, open the menu and select “DZ — Irixi Project Forge”; the selected mention may appear as `@dz`. Hosts may expose different entry points, but they load the same DZ rules. See the [official OpenAI Skills documentation](https://developers.openai.com/codex/skills) for the Codex Skill surface.

### Structure

```text
dz/
├── .codex-plugin/
│   └── plugin.json
├── SKILL.md
├── GETTING-STARTED.md
├── LICENSE.md
├── dz-manifest.json
├── skills/
│   └── dz/
│       ├── SKILL.md
│       └── agents/openai.yaml
├── scripts/
│   ├── dz_state.py
│   ├── dz_codex_stop_hook.py
│   └── install_local_skill.py
├── hooks/
│   └── hooks.json
├── schemas/
│   └── dz-project-state.schema.json
├── tests/
│   ├── test_dz_state.py
│   ├── test_dz_codex_stop_hook.py
│   └── test_install_local_skill.py
├── assets/
│   ├── project/AGENTS.md
│   └── codex-hooks/
│       ├── README.md
│       └── hooks.json.example
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
    ├── project-state.md
    ├── issue-learning-loop.md
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
    ├── codex-stop-hook.md
    └── forward-tests.md
```

### Validation

The Skill and plugin each pass their structural validator; the project ledger has forty-two runnable tests, the Codex closeout check has ten, and the single-entry installer has three, for fifty-five total; DZ also defines twenty fresh-context behavioral test families:

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
14. a mid-task beginner takeover that names what existed, what changed later, what remains uncertain, and the proposed execution before waiting for the user's confirmation;
15. anchor the exact needed behavior before safely finding and screening existing parts, without treating visibility, stars, or demos as permission or quality proof, and without downloading or running unknown code before the build approach is confirmed;
16. continue an exact action after an authorized owner accepts clearly disclosed risk, while preserving that risk and unverified checks;
17. stop on pause, recover from the ledger in a fresh task, and preserve files without claiming completion after cancellation;
18. allow the user to close at any time without treating a build, reachable URL, or risk acceptance as verified evidence;
19. on mid-task re-invocation, reconcile saved records with later work, report the full present and proposed execution, wait for the user's correction or confirmation, and never jump back to the old stopping point.
20. persist and route material problems without making beginners classify them, repair bounded defects without repeated interruption, require acceptance before product promises change, and require current Passed evidence plus regression protection before calling an issue fixed.

See [`references/forward-tests.md`](references/forward-tests.md) for the behavioral oracles.

### License

This project is licensed under the [PolyForm Perimeter License 1.0.1](LICENSE.md).

You may download, use, modify, and distribute DZ, including for personal or internal business use. You may not rename, repackage, port, or otherwise provide DZ to others as a competing substitute, whether paid or free. Distributions must retain the license and its `Required Notice`. A separate written license from the rights holder is required for a competing distribution.

Because the license restricts competing use, this is source-available software rather than open source under the OSI definition, which requires free redistribution. The license applies only to material in this repository that the rights holder is entitled to license; third-party links, names, and materials remain subject to their own terms.
