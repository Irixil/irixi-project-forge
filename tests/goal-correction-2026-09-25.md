# DZ 目标变更同步修复 / Goal correction synchronization

日期：2026-09-25。工作流：`2026-09-25.1`；插件包：`1.0.10`。本次修复在隔离副本中实施，保留来源仓库既有、尚未提交的 9 月 20 日修改。未改任何真实业务项目。

## 实际发现

不是“完全没有保存目标的能力”，而是明确决定如何进入记录、如何继续执行，没有接好：

1. 本机 `2026-09-20.1` 要求新指令只有“仍在当前最终目标里”才能优先，还把明确改目标一律先降为提议。这会让“防 AI 擅改目标”变成“旧文件限制用户改目标”。
2. 正常接受后继目标时，目标索引和当前文件路径会更新，但旧 `next_action` 保持不变。新增测试在未修复代码中实际得到：`obsolete automatic sending` 仍存在于下一步。不能只凭目标字段变了，就说整条执行链已同步。
3. 同步仍依赖 AI 调用工具，原说明缺少明确决定当轮落盘、同步下游并读回核对的统一做法。新对话看不到从未保存的决定时，工具不能凭空恢复它。
4. 独立试用发现工作表混列历史与当前任务，承接后也不能改标题。即使总览正确，读取工作表仍可能被旧任务误导。

这证明了工作流本身存在缺陷；用户所指的具体返工项目和那次执行记录未提供，本报告不冒充对该项目完成了故障追踪或数据修复。

## 最小修复

- 主 Skill 统一明确决定与讨论提议的区别。用户写清的变更本身就是对该差异的确认，专业评估不等于否决用户的普通产品取舍。仍未确定的重要选择才继续问。
- 在现有 `set-decision` 上增加 `--user-change`，复用原后继版本机制，在单次状态操作中记录确切变更。要求旧决定确实接受过、新路径、完整后继文件摘要、决定人和真实来源引用。下游原先接受过、因本次变更而过期的记录可用同一路径同步；从未确认的新内容不能借此跳过讨论。
- 普通接受和直接变更两条路径都会清掉旧执行指令，换成当前决定的核对步骤。暂停不会自动恢复；已有外部动作授权不能挪给新目标。
- 同一轮同步受影响的目标、要求、方案、任务和下一步，再读回核对。旧文件留作历史；未落盘时明确报告失败，不沿用户否定的旧路线继续。
- 工作表增加当前/历史标记；`carry-work --title` 可以在承接一个任务时同步名称。调整任务不再复制旧备注中的执行要求，原文留在历史。旧记录无需为了从待办消失而假装取消或删除。
- 同步主入口、生成的通用版、接续模板、相关细则及中英文 README / 使用说明；不增加第二套目标库或新依赖。

## 自动验证

新增 `tests/test_goal_change.py` 覆盖真实命令与生成文件，不以“提示词里有这句话”当通过：

- 原接受路径消除旧下一步；明确新目标一次写入并在重新读取时生效；原决定/实现/证据保持。
- 讨论中的后继草稿不抢占目标；摘要不匹配不改状态或日志；同路径覆盖和缺少决定来源被拒绝。
- 只改方案或范围时不擅自替换最终目标；覆盖索引及时更新。
- 暂停不会自动恢复；活动中的外部授权不能被新决定复用。
- 完整同步下游、承接任务、更新标题，历史与当前任务在工作表上明确区别。

最终执行 `python3 -B -m unittest discover -s tests -q`：**94 tests, 106.448s, OK**。其中 10 项目标变更专项测试全部通过，包含调整任务不复制旧备注的回归断言。另通过 Skill 格式检查、Python / JSON 语法检查、通用版生成一致性、安装副本测试和差异格式检查。

## 独立执行试验

一名没有本次诊断历史的独立执行者读取本版 Skill，在隔离的合成记账项目处理原样模拟请求：已有手动记账与本地保存，原计划按月合计；现在明确改成按天查看各类花费，其他不变，仅同步记录、不写功能。

实际产物：三份 v2 决定、链接到每日分类要求的新任务、已更新下一步和交接。未重复要求批准。回读 19 条有效日志、0 条无效；无漏记的当前要求、无待承接旧任务；原三份决定及占位实现的 SHA-256 保持。项目如实暂停，未登记任何功能 Passed 证据。

该试验指出下游需要多步登记、历史任务混列和标题无法更新，本轮据此补了上述窄修复。随后同一执行者作聚焦复测：模拟用户再次明确从每日改为每周分类合计。三份 v3 决定通过同一直接入口更新，任务名称同步为“实现每周各类别支出合计”；历史每日任务保持原状态但明确标为非当前待办。回读 25 条有效日志、0 条无效，当前要求无漏项、无未处理的旧任务；原始及 v2 决定与占位实现字节不变。未知的周起止口径进入后续实现前的待确认事项，没有阻挡本轮已明确部分的同步，没有编造该口径已被批准。

第二轮还发现调整任务会复制旧备注中的执行语句；执行者当轮修正了备注，随后工具改为 `revise` 不复制旧备注，历史原文照留，并增加对应回归断言。该最后的自动备注行为由程序测试验证，未再让模拟用户重走第三轮对话。

本机安装副本也运行了 10 项目标变更专项测试；安装保留旧版备份。GitHub 未在本轮推送。

## 限制

这不是所有平台永久遵守规则的保证。账本不能读取未提供的聊天，也不能独立证明模型提交的批准或测试是真的；需要 Agent 实际加载新 Skill、具备相应记录权限并执行同步。宿主自己的目标/计划只有存在受支持且获准的更新入口时才可同步，否则必须标明陈旧，不假装成功。更新安装包不自动重写每一个旧业务项目，也不授权发布或破坏性操作。

## English summary

The previous local rules could demote an explicit user correction to a proposal and give stale saved goals excessive authority. A reproduced implementation defect also retained the old next action after a successor was accepted. This fix records a precise user-authored delta without duplicate approval, reuses the existing successor mechanism, clears stale execution instructions, reconciles downstream records and requires read-back. Historical work is explicitly labelled, and carried tasks can be renamed. Files, evidence and compatible implementation remain intact; exploratory suggestions stay unaccepted, pauses stay paused, and outside-action authority is not inherited.

A bounded independent execution changed a synthetic monthly-expense project to daily-category totals without reapproval or product coding. This is evidence of that tested interaction, not real-product acceptance or universal host compatibility. Unseen conversations and inaccessible host-side goals remain outside the ledger's capabilities.
