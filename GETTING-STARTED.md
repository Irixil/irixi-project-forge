# Download and Load DZ in Any Agent

Use SKILL.md’s single confirmation rule: existing explicit acceptance of the same visible position, scope and route counts; ask only about unsettled choices. For a simple utility, one acceptance may cover the three distinct visible product decisions.


[中文](#中文) · [English](#english)

## 中文

### 先记住一件事

把 DZ 下载到电脑，不代表 Agent 已经看见它。你还需要完成下面四种加载方式中的一种：安装 Skill、给 Agent 文件读取权限、把通用版放进平台的指令栏，或者在普通聊天里手动提供通用版。

### 新项目直接这样用

当前个人版沿着“接住目标、组织执行、跟踪变化、交付验证、下次继续”推进。它会告诉你现在可用什么、缺什么、下一步怎么做、哪些需要你决定；六阶段技术检查按项目需要使用，简单任务不要求多 Agent 或整套表格。

在允许使用 DZ 的新项目文件夹中选中 `$dz`；如果菜单没有它但 Agent 能读本地文件，就发送：

```text
先完整读取 <已安装的 DZ 文件夹>/SKILL.md，按 DZ 做这个项目：<用途和希望得到的结果>。完成标准是：<怎样算可用>。已有材料在：<路径>。先用最小可行方式推进，缺少关键决定才问我。
```

接着旧项目可说：“按最新确认目标接着做，先对照当前文件，告诉我已确认成果、缺口和下一步。”只是讨论用“先讨论，别改目标”；已决定用“目标改成 X，其他不变”。已有项目明确暂停 DZ 或另有工作流时保留其规则，不因全局技能更新而自动启用。

改目标时保留仍有效的事实与兼容成果，旧目标专属结论退出当前路线。反复修不好时按入口中的时间/成本/重试限额停下受阻部分并汇报，不无限重复。模拟检查、真实模型试用和真正主流程的结果分别说明；没测过仍是未验证。

这些行为有些是技能文字约束。脚本负责记录一致性、目标/需求关联、证据有效性和接续诊断；它不会自动计时、监控所有 Agent 或强制模型听话。换模型/平台要带走目标、状态、成果和验收资料，并确认实际工具能力，不能保证零成本切换。

### 第一步：下载完整文件夹

选择一种方式：

- [下载 ZIP](https://github.com/Irixil/irixi-project-forge/archive/refs/heads/main.zip)，解压后保留全部文件；
- 或运行：

```bash
git clone https://github.com/Irixil/irixi-project-forge.git dz
```

不要只下载 `SKILL.md`。完整流程还会按当前步骤读取 `references/`、`assets/`、`schemas/` 和 `scripts/` 中的相关文件。

### 第二步：根据你的 Agent 选择一种加载方式

#### A. 平台支持 Agent Skills 或 Skill 文件夹

在普通 Agent 平台的 Skill 管理页面中，导入整个 `dz` 文件夹；平台识别的入口文件是仓库根目录的 `SKILL.md`。Codex 本地安装请在下载目录运行 `python3 scripts/install_local_skill.py`，它会生成只有一个入口的独立 Skill，避免仓库里的插件入口被重复发现。

加载以后，使用该平台实际支持的 Skill 选择器或明确调用语法。它可能显示成 `DZ — Irixi Project Forge`、`dz`、`@dz` 或 `$dz`。如果平台使用 `@` 菜单，就从菜单里选中；只有平台明确把 `$dz` 或其他文字定义为调用语法时，直接输入才会生效。随手打出 `@dz` 不一定会加载 Skill。

DZ 允许 Codex 根据“开始或继续做应用、Agent、产品”的请求自动选择它，但第一次使用或排查问题时，仍建议从菜单明确选中一次。仓库更新后，要先在仓库目录运行 `python3 scripts/install_local_skill.py --replace` 更新安装副本，再重启 Codex；只重启不会复制新文件。

不要同时安装同一版本的“本地 Skill”和“插件版”，否则菜单中仍可能出现两个 DZ。旧说明曾让用户把整个仓库软链接到 Codex 的 Skill 目录，这也会同时暴露根入口和插件内层入口；在仓库目录运行 `python3 scripts/install_local_skill.py --replace` 可以改成单入口安装。旧链接会移到 `~/.agents/skill-backups/`，原仓库不会被删除。

想让第二天的新任务接管昨天的项目，请从具体项目文件夹打开 Agent，而不是只打开它的上一级大文件夹。DZ 建立项目账本时会把一段接续说明合并进项目的 `AGENTS.md`。每次重新接管时，它会先运行只读 `resume-report`，读完每条有效日志、还没解决的问题和后来对问题做过的处理，并在 Git 可用时比较上次保存的文件状态和现在的内容。旧项目说明过期时，它会先把刷新 `install-guidance` 列入建议，等用户确认接管后再执行。其他平台只有在支持长期项目指令并持续开放同一批项目文件时，才能做到同样的接续。

DZ 会把开发和试用中真正影响结果的问题写进项目账本，并自己判断该去修代码、补充原先说法、修改动手办法、留到以后还是重新讨论。小白不用选择技术分类。只是修回原先已经说定的行为时可以直接小修；你明确说清的改法直接更新记录，不重复批准。只有仍没决定的使用方式、内容保存或外传、权限、费用和范围才继续讨论。问题重开后要重新检查；没有实际跑过能重现原问题的检查时，只能说“已经改了，但还没证明真的解决”。

#### B. Agent 能读取本地文件或项目文件夹，但没有 Skill 安装功能

把 `dz` 文件夹放在 Agent 能读取的位置，然后把下面这段话发给它。将尖括号里的内容换成真实路径和你的事情：

```text
请启动 DZ。

先完整读取“<DZ 文件夹的绝对路径>/SKILL.md”。把它当作本次工作的工作方式，并按照其中“Load references only when routed”的规则，只读取当前步骤需要的参考文件，不要一次加载整个 references 文件夹。

开始前先根据你现在真实拥有的工具，说明你能否读取和修改我的项目、运行命令、打开网页和发布；不能确认的能力按没有处理。如果“<我的项目文件夹>”里已经有 .dz/state.json，先把以前的记录、后来新增的操作和项目现在的内容对一遍。汇报现在做到哪、准备怎样继续，等我确认或更正后再行动；不要重新开始，也不要退回旧位置。

我的事情是：<写下你的想法，或者说“整理这个做到一半的项目并继续”>。
```

Agent 必须能实际读取这个路径。一个只能聊天、看不到你电脑文件的网页 AI，不能靠这段话读取本地文件。

#### C. 平台支持系统提示词、项目指令或 API

打开 [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md)，把全文放进平台的系统提示词、项目指令、自定义 Agent 指令或 API 的高优先级指令中。然后发送：

```text
DZ启动：<写下你的想法或当前做到哪里>。
```

平台的接入程序需要自己保存对话、开放真实工具并控制权限。DZ 文件本身不能给 Agent 增加它原来没有的文件、命令、联网或发布能力。

#### D. 平台只有普通聊天、单文件上传或知识库

如果能上传文件，上传 [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md)，然后发送：

```text
请把我上传的 DZ-UNIVERSAL.md 作为本次工作的工作方式。
DZ启动：<写下你的想法或当前做到哪里>。
```

如果只能发送文字，直接打开 `DZ-UNIVERSAL.md`，把全文粘贴进对话，再发送启动句。有些平台只把上传文件或知识库当作参考资料，不会把它当作固定工作规则；遇到这种情况也使用粘贴全文的方法。这种普通聊天方式依赖当前对话，不能保证平台在新对话里继续记得 DZ。

这种方式可以完成脑暴、三项关键决定的确认、专业建议和交接。只有当平台真的提供项目文件、命令、浏览器或发布工具时，它才能直接开发、测试或上线。

### 第三步：确认它真的加载成功

先发送这句检查话：

```text
先不要开始项目。请证明 DZ 已经加载：说出你实际读取的入口文件和 DZ 工作流版本；如果你读取的是完整文件夹，再说出一个你确实能打开的 references 文件名。读不到就直接说读不到，不要猜。
```

完整文件夹应报告入口 `SKILL.md`、从 `dz-manifest.json` 读到的 `workflow_version`，以及一个真实可读的参考文件。通用版应报告入口 `portable/DZ-UNIVERSAL.md` 和写在文件开头的版本。这个回答比只观察语气更可靠，但仍是 Agent 的自我报告；做正式接入的平台应固定一个 Git 提交编号，并由加载程序自己检查下载内容。

接着，第一次项目回复应该能看出三件事：

1. 它知道自己是在使用 DZ，而不是只回答一个普通问题；
2. 它会按当前 Agent 的真实工具说明能做到哪一步，不会假装运行过测试；
3. 新想法会先问一个最重要的问题；做到一半的项目会先把旧记录和后来新增的操作与当前内容对齐，汇报准备怎样继续，等用户确认后再行动。

如果它说“DZ 不在可用 Skill 清单”，但它确实可以读取文件，就使用上面的 B 方式给出完整路径。这样是手动加载，仍然可以运行 DZ；原生 Skill 菜单只是更方便的入口。

### 更新后继续旧项目

当前版本为 `2026-10-03.1`。先更新完整文件夹和平台实际加载的安装副本，再在具体项目里调用 DZ。它核对最新明确决定和现有记录；旧文件不能压过你后来明确修改的目标。可以说：“按我们最新确认的目标，把本地目标、需求、待办和下一步同步好，保留兼容成果；只有缺少关键决定才问我。”AI 必须真的保存并读回核对；读不到最近的决定就问，不准猜。尚在讨论的建议不会自动变成决定。旧文件、证据保留为历史，不清空；没有逐项标记的旧要求先整理给你看，不偷偷接受新内容。你仍可随时暂停或如实收尾。

文件变化、授权过期或生成清单不一致时，DZ 先解释实际差异，再按已允许的范围修复记录，不会因为能读出旧记录就继续旧操作。单纯查看情况不会让其他已验证工作全部重来。旧项目升级不会自动启动已经结束的开发。

### 给平台开发者

先读取公开的 [`dz-manifest.json`](https://raw.githubusercontent.com/Irixil/irixi-project-forge/main/dz-manifest.json)。支持 Agent Skills 时加载其中的 `agent_skill`；不支持时加载 `universal_prompt`。详细的能力判断、按需参考文件、状态保存和权限边界见 [`adapters/README.md`](adapters/README.md)。

## English

### Remember one thing first

Downloading DZ does not automatically make it visible to an agent. You must use one of four loading methods: install the Skill, grant the agent file access, place the universal edition in the host's instruction field, or manually provide the universal edition in ordinary chat.

### Step 1: Download the complete folder

Choose one:

- [Download the ZIP](https://github.com/Irixil/irixi-project-forge/archive/refs/heads/main.zip) and keep every extracted file;
- or run:

```bash
git clone https://github.com/Irixil/irixi-project-forge.git dz
```

Do not download only `SKILL.md`. The full workflow progressively loads relevant files from `references/`, `assets/`, `schemas/`, and `scripts/`.

### Step 2: Choose one loading method

#### A. The host supports Agent Skills or Skill folders

For an ordinary Agent host, import the complete `dz` folder through its Skill manager; the Agent Skills entry point is the root `SKILL.md`. For a local Codex installation, run `python3 scripts/install_local_skill.py` from the downloaded repository. It creates a standalone package with one entry and prevents the nested plugin entry from being discovered a second time.

Invoke it through the host's actual Skill selector or documented invocation syntax. It may appear as `DZ — Irixi Project Forge`, `dz`, `@dz`, or `$dz`. If the host uses an `@` menu, select it there. Direct typing works only when the host explicitly defines that text as invocation syntax; merely typing `@dz` may not attach the Skill.

DZ allows Codex to select it automatically when a request clearly starts or resumes an application, agent, or product. Explicit selection is still the clearest first-use and troubleshooting path. After updating the repository, first run `python3 scripts/install_local_skill.py --replace` from that repository to refresh the installed copy, then restart Codex; restarting alone does not copy new files.

Do not install the same version as both a local Skill and a plugin. That can still show two DZ entries. Older instructions also symlinked the whole repository into Codex's Skill directory, which exposed both the root entry and the nested plugin entry. Run `python3 scripts/install_local_skill.py --replace` from the repository to convert that old symlink into a single-entry installation. The old link moves to `~/.agents/skill-backups/`, and the source repository is not deleted.

To take over the project in a new task tomorrow, open the agent from the exact project folder rather than only its parent container. When DZ initializes its ledger, it merges a continuity section into the project's `AGENTS.md`. On every takeover, it reads `PROJECT.md` and runs the read-only `resume-report`. The tool mechanically validates every journal record, checks that the generated view is current, and compares the saved Git checkpoint with the present worktree while returning a compact summary by default. Relevant accepted requirements and implementation files are still read before acting; full history is opened only for a conflict, unexplained change, damage, stale view, or material uncertainty. Continuous aligned work does not repeat takeover after each question. Another host can provide the same continuity only when it supports persistent project instructions and keeps the same project files available.

DZ records material problems and chooses their existing home: code repair, product wording, technical approach, later work or product purpose. The beginner never selects technical categories. An in-contract defect may be repaired directly. A precise user-decided change updates the records without duplicate approval; only unsettled behavior, information handling, access, cost or scope needs further discussion. Reopened problems require a new check. Without a check that exercises the former failure, DZ says the change is implemented but not yet proven.

#### B. The agent can read local or project files but cannot install Skills

Place the `dz` folder somewhere the agent can read, then send the following. Replace the placeholders with real paths and your request:

```text
Start DZ.

First read “<absolute path to the DZ folder>/SKILL.md” completely. Use it as the working method for this task. Follow its “Load references only when routed” rules and read only the references needed for the current step; do not load the whole references folder at once.

Before starting, use only the tools you can truly access to say whether you can read and modify my project, run commands, browse the web, and publish. Treat anything uncertain as unavailable. If “<my project folder>” already contains .dz/state.json, reconcile prior records and later work with the current project. Report the present and how you propose to continue, then wait for my correction or confirmation before acting. Do not restart or return to the old stopping point.

My request is: <describe the idea, or say “organize and continue this unfinished project”>.
```

The agent must actually have access to that path. A chat-only website that cannot see local files cannot read the folder from this message alone.

#### C. The host supports system instructions, project instructions, or an API

Open [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md) and place its full contents in the host's system prompt, project instructions, custom-agent instructions, or another high-priority API instruction. Then send:

```text
DZ启动: <describe the idea or current project state>.
```

The integration must still preserve the conversation, expose real tools, and enforce permissions. The DZ file cannot grant file, command, network, or release capabilities that the agent did not already have.

#### D. The host only provides ordinary chat, one-file uploads, or a knowledge base

If file upload is available, upload [`portable/DZ-UNIVERSAL.md`](portable/DZ-UNIVERSAL.md), then send:

```text
Use the uploaded DZ-UNIVERSAL.md as the working method for this task.
DZ启动: <describe the idea or current project state>.
```

If the host accepts text only, open `DZ-UNIVERSAL.md`, paste its full contents into the chat, and then send the start message. Some hosts treat uploads and knowledge-base files only as reference material, not persistent working instructions; use the same paste method in that case. This ordinary-chat method is conversation-scoped and does not guarantee that a new chat will remember DZ.

This mode can brainstorm, make the three product decisions explicitly accepted, challenge blind spots, and produce a handoff. It can directly build, test, or release only when the host truly provides project files, commands, a browser, or deployment tools.

### Step 3: Confirm that loading worked

Send this check first:

```text
Do not start the project yet. Prove that DZ is loaded: state the entry file you actually read and the DZ workflow version. If you read the full folder, also name one references file you can truly open. If you cannot read them, say so instead of guessing.
```

The full bundle should report `SKILL.md`, the `workflow_version` read from `dz-manifest.json`, and one genuinely readable reference file. The universal edition should report `portable/DZ-UNIVERSAL.md` and the version written at its top. This is stronger than judging tone alone, but it is still an agent self-report. A production integration should pin an explicit Git commit SHA and verify the fetched content itself.

The first project reply should then demonstrate three things:

1. The agent knows it is running DZ instead of merely answering a generic question.
2. It states what the current host can really do and does not claim tests it never ran.
3. It asks one high-value question for a new idea; for an unfinished project, it reconciles saved records and later work with the current contents, reports the proposed execution, and waits for the user's correction or confirmation before acting.

If it says that DZ is absent from the available Skill list but can read files, use method B with the exact path. That is a valid manual load; a native Skill selector is simply the more convenient entry point.

### Continue an older project after updating

The current version is `2026-10-03.1`. Update the bundle and the copy actually loaded by your host, then invoke DZ inside the specific project. Ask it to synchronize the goal, requirements, work and next action with your latest explicit decision while preserving compatible work. It must save and read back the result, not let stale files overrule that decision. If the decision is inaccessible, it must ask rather than guess. Unaccepted ideas remain proposals; old files and evidence remain history, not current proof. Legacy missing labels are reconciled visibly, never by accepting invented content. You may still pause or close honestly.

Changed files, expired permission and stale generated lists produce diagnosis rather than permission to continue old actions. Repair only within the agreed scope. Read-only inspection preserves unrelated valid proof, and upgrading a closed project does not restart development.

### For host developers

Fetch the public [`dz-manifest.json`](https://raw.githubusercontent.com/Irixil/irixi-project-forge/main/dz-manifest.json) first. Load `agent_skill` when Agent Skills are supported; otherwise load `universal_prompt`. See [`adapters/README.md`](adapters/README.md) for capability routing, on-demand references, durable state, and authorization boundaries.
