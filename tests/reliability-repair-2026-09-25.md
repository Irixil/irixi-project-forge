# DZ 可靠性修复与验证 / Reliability repair and validation

日期：2026-09-25。候选工作流：`2026-09-25.2`，插件包：`1.0.11`，状态格式仍为 `1.1`。

本次修缮个人工作流，不重做产品框架，不修改用户的其他业务项目，也不自动迁移每个历史项目。以下区分程序检查、真实模型试用与尚未验证的范围。

## 保留什么，修好什么

保留 Anthropic 的六阶段 SDLC、三份技术手册的按需路由、专业建议、用户最终决定权和按平台能力工作。依据已核对的 [Astra 使用指南](https://developers.openai.com/api/docs/guides/latest-model)、[OpenAI 的 Astra Skills 与提示词建议](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)以及 [Anthropic AI-Native SDLC](https://claude.com/blog/the-ai-native-sdlc-playbook)整理核心指令、按需参考和有证据的验证；这不代表官方认证。

| 原来的问题 | 本次处理 | 检查方式 |
| --- | --- | --- |
| 用户已明确改目标，参考页仍可能要求再次批准 | 入口只保留一条修改决定规则；问答、接续、产物模板和评估标准遵循它。明确改动直接保存，探索性意见不执行 | 明确修改与只讨论的独立试用；目标修改回归 |
| 问题重开仍可能引用旧证明 | 每轮工作和问题记录新的证明起点；开始实际修复就更新整项工作的检查边界，不混用修复前其他验收项的结果 | 旧证明拒绝、新证明通过、多问题共享工作、先延后再修复和 A/B 验收回归 |
| 文件变动或授权过期导致接续报告读不出来 | 先提供只读诊断，区分保存的说法与现在可验证的事实；报告本身不授权继续 | 文件变动、过期授权、损坏状态回归 |
| 恢复工作状态时，问题页还错误显示通过 | 同步核对工作与问题的证明，保留历史但撤销失效结论 | 证明文件改变后的恢复回归 |
| 旧版已收尾项目升级卡死，失败还可能先改指引 | 先准备和验证新状态；缺少覆盖证明就如实降为部分验证，不强制重新开工；验证失败不写指引 | 旧格式升级、无写入失败回归 |
| 只是查看记录，却让所有旧检查失效 | 增加明确的只读工作类型；它不能用来登记实现、部署或修复，不获得外部操作许可 | 程序回归及只读登记独立试用 |
| 只核对首页，漏掉待办和问题页被改写 | 三份自动生成的页面都核对完整内容 | 保留旧指纹但改正文等回归 |
| 在父目录调用时找不到子项目 | 识别唯一直接子项目；多个项目时明确报出并询问，不猜、不递归乱找 | 收尾检查回归 |
| 测试通过却没测到实际交互问题 | 增加故障回归和可重建的隔离项目，用全新上下文观察真实回应与文件变化 | 本报告下述模型试用 |

独立代码复查进一步发现并纳入修复：共享进行中工作时的 A/B 旧证明漏洞，以及损坏的历史工作区快照让接续报告崩溃。相邻检查进一步覆盖了新问题和先延后再修复的路径，避免只修复某一种问题状态。损坏快照应显示“无法可靠比较”，不能说没有变化。

## 可重跑的程序检查

在仓库根目录运行：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
python3 -B scripts/sync_workflow.py --check
```

- 修复前第一轮故障测试：8 个测试，出现 7 个失败和 2 个子场景错误；不是只有通过的演示。
- 第一轮完整候选套件：112 个测试，307.974 秒，通过。但独立复查仍发现两处漏洞，所以这个结果不被当作最终修复完成。
- 第二轮针对性红测：3 个测试，12.001 秒，11 个失败（含损坏快照的子场景），确认新增问题可复现。
- 相邻修复入口红测：3 个测试，9.682 秒，全部失败；新问题、先延后再修复仍可混用旧证明，随后统一了修复起点规则。
- 最终针对性回归：15 个测试，37.313 秒，全部通过；包含以上故障和相邻路径。
- Skill 与插件格式检查、13 份 Python 文件语法检查、3 份 JSON 解析、通用版同步和补丁空白检查均通过。隔离安装包 42 份文件逐一匹配源码，且只有一个 `SKILL.md` 入口；用打包后的状态工具检查改目标样本通过。
- 冻结最终核心后的完整套件：**116 个测试，142.020 秒，全部通过**。运行前后核心摘要不变。
- 本机独立 Skill 已更新到 `2026-09-25.2`。安装后 42 份文件再次逐一匹配源码，唯一入口检查通过；用实际安装的工具检查改目标与只读登记样本均通过。旧版 `2026-09-25.1` 保留在本机 `skill-backups/dz-20260925-024640`，未覆盖其他项目或修改全局设置。宿主需要重启并开启新任务，才可靠加载更新后的入口。

新增故障用例位于 [test_audit_regressions.py](test_audit_regressions.py)，并扩展状态、生命周期、目标修改和收尾检查测试。独立复查不改被审查源码，避免拿自己的口头判断替代可复现故障。

最终独立复核：直接重开、新问题、先延后再修复三条路径均拒绝“新 A 证明 + 旧 B 证明”完成工作，拒绝时状态和历史不变；补齐新 B 证明后均可正常收尾。损坏快照返回比较不可用，状态、历史和项目指引字节不变。独立复核前后核心文件摘要相同：

```text
scripts/dz_state.py                 955e76fb82b89423adee799da09b54b06719870a1d08c51071dfdf9468bb17d0
scripts/dz_codex_stop_hook.py       b5de1f49ff1ba4ce1eec4cac60002a422a5f4c08a0a400553196ba6433b20e31
SKILL.md                           e0b14af8595b078bd3b8dd6c5e2a09826d62e94cb545786089dd8c00c5fe5832
schemas/dz-project-state.schema.json 3c4a9a7dd82b2f69a49ced62460538225b8e8ffa71244fd2fda776b527a12878
```

## 全新上下文试用

用 [create_behavior_fixture.py](create_behavior_fixture.py)创建隔离样本。样本原目标是本机手动记账、查看每月分类支出；没有真实应用、真实用户批准或生产验证。试用者只得到候选入口、样本和下面的用户话语，不提供审查答案或评分标准。

| 场景与输入要点 | 实际观察和核对 |
| --- | --- |
| 明确改目标：“别做每月汇总了，明确改成每天……只同步记录和下一步，先别写功能。” | 通过 Codex CLI 0.154.0 显式请求 `gpt-6-astra`，独立临时对话。目标、需求、计划改为按天；新待办待执行，下一步也改为按天；继续暂停；没有新测试证明；旧文档和功能占位文件内容不变。没有索要同一决定的第二次批准 |
| 只讨论：“要不要改成每天……先讨论，别改记录或功能。” | 独立 Agent 指出按天/按月的取舍并问缺少的选择。试用前后整个样本文件哈希清单相同，无写入 |
| 文件冲突：“昨天有人改过文件。先不要动任何东西，帮我对一下……” | 独立 Agent 指出后来出现的云端上传文字与原本仅本机保存冲突，未把文件文字当成用户批准，也没把假的完成清单当事实；说明缺少 Git 历史，不能判断谁、何时改过。前后文件哈希清单相同 |
| 只读登记：“现状和记录我认可。只登记并查看已有记录……不重跑已经通过的检查。看完记录结果并暂停。” | 独立 Agent 添加一次只读查阅及独立查阅说明后暂停。主审逐项比对：原目标、需求与计划记录、被测版本、W1 工作和 E1 旧证明均原样保留；没有重跑产品测试，明确模拟旧结果不证明真实应用通过 |
| 换一个新对话：“现在到底要做什么，哪些已经做了，哪些还没做……先不要动手。” | 再次通过 CLI 显式请求 `gpt-6-astra`，全新临时对话、只读沙箱。正确识别“每天”是现行目标，“每月”只在历史；说明只有记录没有可用应用，连手动记账和保存也不能据占位说明算完成；先讨论下一步，没有写文件。主审核对仍为原来的 15 条历史，状态等于最后一条记录 |

只讨论、文件冲突、只读登记这三个独立 Agent 试用没有可靠的精确模型身份记录，不将它们冒称为 Astra 专项测试。Astra CLI 的两次对话相互独立，不使用 resume/fork 继承上一段聊天。模型试用次数有限，不把一次通过解释为永不跑偏。

这些交互试用在第一轮候选上执行。后续补修集中于问题修复起点与损坏 Git 快照，交互样本没有这两类状态；最终代码另由针对性回归、完整套件和原故障独立复现检查覆盖。没有把某一轮试用冒称成所有后续版本都重新跑过。

## 已知边界

- 更新 Skill 不自动改所有旧项目。重新进入具体项目时，对照最新明确决定和现有记录处理；本次没有批量修改用户项目。
- 只读查阅保留旧证明；真正实现或修复仍保守地使原检查目标失效，需要对当前版本取得证明。本次没有引入复杂的跨版本证明复用系统。
- 记录工具能检查一致性，不能证明 AI 编写的批准、测试结论天然真实，也不能强迫所有宿主持续加载 Skill。
- 接续报告只提供诊断，不授予执行权；授权过期仍然过期。损坏记录不会自动变成可信记录。
- 升级校验失败不先写指引，但不宣称跨多个文件的磁盘写入具有数据库事务保证。
- 真实新项目的长期使用体验、其他 AI 平台、真人内部测试和生产部署均未验证。上述修复与验证阶段没有推送 GitHub；用户随后单独授权发布，实际上传版本以仓库提交记录为准。

## English summary

This repair keeps the six-stage SDLC and handbook routing. It centralizes explicit user corrections, prevents reuse of pre-repair evidence, makes resume diagnostics available without renewing authority, reconciles issue/work proof, upgrades legacy records before writing guidance, separates inspection from implementation, checks every generated view, and safely discovers a unique direct child project.

The first full candidate passed 112 tests, but independent review still reproduced two defects and adjacent repair-entry bypasses; these were added to the repair rather than hidden behind the passing count. The frozen final core passed **116 tests in 142.020 seconds**, plus independent reproduction checks. Fresh-context trials separately exercise a decided correction, exploration, document drift, read-only inspection and re-entry. Actual files and record fields are compared, not just the model's claims. The correction and re-entry CLI trials explicitly requested `gpt-6-astra`; other delegated trial identities are not asserted. Those behavioral trials ran on the first candidate, while later repair-boundary/checkpoint fixes were checked by final regressions and independent reproductions.

The local standalone installation now uses `2026-09-25.2`; all 42 packaged files match source, one Skill entry remains, and the prior version is backed up. Restart the host and open a new task to load it reliably. No real product, production release, universal host compliance or long-term user experience is certified by these synthetic checks. Existing user projects are not bulk-migrated. The repair and validation phase did not push to GitHub; the user subsequently authorized publication separately, and the repository history identifies the published revision.
