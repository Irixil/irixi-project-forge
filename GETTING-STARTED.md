# Download and Load DZ in Any Agent

[中文](#中文) · [English](#english)

## 中文

### 先记住一件事

把 DZ 下载到电脑，不代表 Agent 已经看见它。你还需要完成下面四种加载方式中的一种：安装 Skill、给 Agent 文件读取权限、把通用版放进平台的指令栏，或者在普通聊天里手动提供通用版。

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

在平台的 Skill 管理页面中，导入整个 `dz` 文件夹，或把平台的 Skill 目录指向这个文件夹。平台识别的入口文件是仓库根目录的 `SKILL.md`。

加载以后，使用该平台实际支持的 Skill 选择器或明确调用语法。它可能显示成 `DZ — Irixi Project Forge`、`dz`、`@dz` 或 `$dz`。如果平台使用 `@` 菜单，就从菜单里选中；只有平台明确把 `$dz` 或其他文字定义为调用语法时，直接输入才会生效。随手打出 `@dz` 不一定会加载 Skill。

DZ 允许 Codex 根据“开始或继续做应用、Agent、产品”的请求自动选择它，但第一次使用或排查问题时，仍建议从菜单明确选中一次。修改 Skill 后没有出现在菜单里，就重启 Codex。

不要同时安装同一版本的“本地 Skill”和“插件版”，否则菜单中可能出现两个 DZ。两个入口最终使用同一套流程，但保留一个更清楚。

想让第二天的新任务自动接着昨天做，请从具体项目文件夹打开 Agent，而不是只打开它的上一级大文件夹。DZ 建立项目账本时会把一段接续说明合并进项目的 `AGENTS.md`；旧项目可以按 [`references/project-state.md`](references/project-state.md) 运行一次 `install-guidance` 补上。其他平台只有在支持长期项目指令并持续开放同一批项目文件时，才能做到同样的自动接续。

#### B. Agent 能读取本地文件或项目文件夹，但没有 Skill 安装功能

把 `dz` 文件夹放在 Agent 能读取的位置，然后把下面这段话发给它。将尖括号里的内容换成真实路径和你的事情：

```text
请启动 DZ。

先完整读取“<DZ 文件夹的绝对路径>/SKILL.md”。把它当作本次工作的工作方式，并按照其中“Load references progressively”的规则，只读取当前步骤需要的参考文件，不要一次加载整个 references 文件夹。

开始前先根据你现在真实拥有的工具，说明你能否读取和修改我的项目、运行命令、打开网页和发布；不能确认的能力按没有处理。如果“<我的项目文件夹>”里已经有 .dz/state.json，先检查并从真实进度继续，不要重新开始。

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

这种方式可以完成脑暴、三次确认、专业建议和交接。只有当平台真的提供项目文件、命令、浏览器或发布工具时，它才能直接开发、测试或上线。

### 第三步：确认它真的加载成功

先发送这句检查话：

```text
先不要开始项目。请证明 DZ 已经加载：说出你实际读取的入口文件和 DZ 工作流版本；如果你读取的是完整文件夹，再说出一个你确实能打开的 references 文件名。读不到就直接说读不到，不要猜。
```

完整文件夹应报告入口 `SKILL.md`、从 `dz-manifest.json` 读到的 `workflow_version`，以及一个真实可读的参考文件。通用版应报告入口 `portable/DZ-UNIVERSAL.md` 和写在文件开头的版本。这个回答比只观察语气更可靠，但仍是 Agent 的自我报告；做正式接入的平台应固定一个 Git 提交编号，并由加载程序自己检查下载内容。

接着，第一次项目回复应该能看出三件事：

1. 它知道自己是在使用 DZ，而不是只回答一个普通问题；
2. 它会按当前 Agent 的真实工具说明能做到哪一步，不会假装运行过测试；
3. 新想法会先问一个最重要的问题，做到一半的项目会先整理现状，不会立刻乱写代码或重新从头问。

如果它说“DZ 不在可用 Skill 清单”，但它确实可以读取文件，就使用上面的 B 方式给出完整路径。这样是手动加载，仍然可以运行 DZ；原生 Skill 菜单只是更方便的入口。

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

Import the complete `dz` folder through the host's Skill manager, or point its Skill directory at this folder. The Agent Skills entry point is the root `SKILL.md`.

Invoke it through the host's actual Skill selector or documented invocation syntax. It may appear as `DZ — Irixi Project Forge`, `dz`, `@dz`, or `$dz`. If the host uses an `@` menu, select it there. Direct typing works only when the host explicitly defines that text as invocation syntax; merely typing `@dz` may not attach the Skill.

DZ allows Codex to select it automatically when a request clearly starts or resumes an application, agent, or product. Explicit selection is still the clearest first-use and troubleshooting path. Restart Codex if an updated Skill does not appear in the selector.

Do not install the same version as both a local Skill and a plugin. That can show two DZ entries. They lead to the same workflow, so keep one installation.

To resume automatically in a new task tomorrow, open the agent from the exact project folder rather than only its parent container. When DZ initializes its ledger, it merges a continuity section into the project's `AGENTS.md`; an older project can run `install-guidance` once as described in [`references/project-state.md`](references/project-state.md). Another host can provide the same behavior only when it supports persistent project instructions and keeps the same project files available.

#### B. The agent can read local or project files but cannot install Skills

Place the `dz` folder somewhere the agent can read, then send the following. Replace the placeholders with real paths and your request:

```text
Start DZ.

First read “<absolute path to the DZ folder>/SKILL.md” completely. Use it as the working method for this task. Follow its “Load references progressively” rules and read only the references needed for the current step; do not load the whole references folder at once.

Before starting, use only the tools you can truly access to say whether you can read and modify my project, run commands, browse the web, and publish. Treat anything uncertain as unavailable. If “<my project folder>” already contains .dz/state.json, check it and continue from the real state instead of restarting.

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

This mode can brainstorm, run the three confirmations, challenge blind spots, and produce a handoff. It can directly build, test, or release only when the host truly provides project files, commands, a browser, or deployment tools.

### Step 3: Confirm that loading worked

Send this check first:

```text
Do not start the project yet. Prove that DZ is loaded: state the entry file you actually read and the DZ workflow version. If you read the full folder, also name one references file you can truly open. If you cannot read them, say so instead of guessing.
```

The full bundle should report `SKILL.md`, the `workflow_version` read from `dz-manifest.json`, and one genuinely readable reference file. The universal edition should report `portable/DZ-UNIVERSAL.md` and the version written at its top. This is stronger than judging tone alone, but it is still an agent self-report. A production integration should pin an explicit Git commit SHA and verify the fetched content itself.

The first project reply should then demonstrate three things:

1. The agent knows it is running DZ instead of merely answering a generic question.
2. It states what the current host can really do and does not claim tests it never ran.
3. It asks one high-value question for a new idea, or audits the current state of an unfinished project instead of coding blindly or restarting discovery.

If it says that DZ is absent from the available Skill list but can read files, use method B with the exact path. That is a valid manual load; a native Skill selector is simply the more convenient entry point.

### For host developers

Fetch the public [`dz-manifest.json`](https://raw.githubusercontent.com/Irixil/irixi-project-forge/main/dz-manifest.json) first. Load `agent_skill` when Agent Skills are supported; otherwise load `universal_prompt`. See [`adapters/README.md`](adapters/README.md) for capability routing, on-demand references, durable state, and authorization boundaries.
