# DZ 工作流修缮验证 / Workflow refinement validation

日期 / Date: 2026-09-10. Workflow: `2026-09-10.3`. Plugin: `1.0.9`. State schema: `1.1` (additive requirement index and carry links; use the current tool).

## 这次做了什么

没有重做六阶段流程，也没有去改另一个业务项目。本轮补齐“需求有没有漏、改方向怎么保留成果、什么时候需要问、几个入口如何同步”，并同步中英文 README 和下载使用说明。

- 已确认需求仍是唯一标准。AI 在同一份文档里标记每个完整必做结果，工具读取并核对，不再只看登记过的任务是否全绿。
- 改方案后可批量保留或逐项调整旧任务，未处理的旧任务仍可见。历史和有效代码不删除，旧证明不算新版本通过，做了一半的事也不会自动升为“已实现”。
- 原来已授权的监测可以在指定本地记录中沉淀脱敏发现；这不授予改代码、付款或发布权限。
- 第一句只讨论眼下的问题；有关自动操作的完整限制仍需在接受相关决定或实际行动前说清。用户已经说“先别做”时不再次索要暂停确认。
- 通用提示词由主 Skill 自动生成，项目 AGENTS 只保留接续入口。自动发布检查会发现两者不同步。
- Fast Track 的逐次预览和真实执行授权收窄到批量修改、删除、迁移或覆盖原有资料，不要求每次普通保存和已授权的开发编辑重新审批。

## 自动验证

最终执行 `python3 -B -m unittest discover -s tests -q`：**79 tests, 59.499s, OK**。

| 套件 / Suite | 数量 / Count | 范围 / Scope |
|---|---:|---|
| State | 51 | Decisions, continuity, corruption detection, evidence, issues, action scope, pause/close and legacy migration |
| Coverage and carry | 9 | Omitted Must, optional/cancelled work, malformed/duplicate/example markers, index drift, current-proof requirements, changed promises, atomic failure, unfinished work, issue links and legacy plain specifications |
| Codex Stop hook | 10 | Bounded closeout and honest continuation/stop handling |
| Installer | 6 | Single discoverable entry, backup, package integrity, versions and reference routes |
| Lifecycle | 1 | Actual disposable local program through six stages, including failure, restore and follow-up; no real production or human acceptance |
| Generated entry | 2 | Core changes fail the check until regeneration; distributed prompt and reference links match |

另外通过 Skill 格式检查、Python/JSON 语法检查、生成入口一致性和 Git 差异格式检查。这些检查不把 Markdown 中出现一句话当成 AI 已经执行了该规则。

首轮全量测试发现并处理了四处失败：旧任务的“进行中”误占用新方案执行位置；旧格式迁移测试需要走真实的说明升级步骤；两项旧包装测试仍依赖已经更改的提示词字面句子。后两项改为验证实际安装文件和入口一致性，不冒充行为验收。随后重跑全量得到上面的结果。

## 独立模拟对话

另一次独立上下文读取本版 Skill 和所需参考，只模拟三段对话，没有创建真实产品或伪造接受记录：

1. 模糊的个人记账想法：先给可理解的起步建议，再问最重要的使用情境，没有提前写代码。
2. “不知道，你给我建议，但先别做”：提供手动分类的建议和未来可用的低成本检查方法，不把建议当成已同意，不实施。
3. 已确认手动录入、本机保存后，用户纠正“不想连银行”：把原约定和当前指令对上，保留兼容的手动录入及分类合计，不增加银行连接，不声称执行过检查。

该模拟指出“不知道”分支可能重复询问暂停，以及 Fast Track 对普通保存的限制过宽；本轮据此作了上述窄修正。修正后的这两项对话行为尚未另跑新模拟，更没有拿真实新手体验来代替。自动测试不能证明所有平台或模型都能持续遵守。

## 明确保留的边界

- 用户将在新项目中验证使用体验，目前 **未测试**；不强迫项目负责人亲自做产品上线验收。
- 本轮未逐个平台运行 WorkBuddy、Kimi、智谱、DeepSeek 等；文件接入规则统一不等于所有平台原生兼容。
- 本地账本不是防篡改认证。它不能发现用户意图从未被写进可见需求的语义遗漏，不能独立证明批准和测试是真实的。
- 旧项目升级不悄改已接受的需求。不带必做标记的旧文档需展示并接受完整后继版本，才能获得完整需求覆盖结论；暂停和部分收尾始终可用。
- 早前 `.1` / `.2` 的结果保留在 [Astra 报告](astra-audit-2026-09-10.md) 和 [接续报告](continuity-validation-2026-09-10.md)。不把早前会话自动算作本版所有新增行为的通过证明。

## English summary

This refinement preserves the six-stage workflow and three handbook routes. It adds exact accepted-Must coverage, linked work carry-forward without inherited passes, visible unresolved prior work, scoped monitoring records, progressive beginner dialogue and a generated universal entry point. Existing files and approval history are preserved.

The final automated run passed **79 tests in 59.499 seconds**, split as shown above. An independent read-only dialogue simulation covered a vague personal expense app, uncertainty with an explicit request not to build, and a correction against already accepted manual/local-only behavior. It did not execute an app or impersonate human approval. Two wording frictions were narrowed afterward; those post-adjustment dialogue cases have not been independently rerun.

Real beginner/new-project use and other hosts remain **not tested**. The owner's planned future feedback is not a passed test. Ledger consistency and packaging checks cannot establish semantic completeness, genuine external approval, universal model compliance or production readiness.
