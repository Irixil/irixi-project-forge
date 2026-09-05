# Mid-Task Takeover and Resume

Use this reference when DZ is explicitly invoked after meaningful discussion, planning, tool calls, implementation, testing, or release work has already happened, including a second invocation in the same task. The objective is continuity: understand the complete current position, preserve valid work done before or after the latest saved record, repair only missing workflow contracts, agree how to proceed, and continue from the smallest justified next step.

## Core rule

Do not restart merely because DZ was invoked late. Do not return mechanically to the last saved stopping point, because the user or another agent may have changed the project since then. Do not continue blindly merely because code exists.

Enter `TAKEOVER_AUDIT` and maintain two separate assessments:

- **Observed work state:** what discussion, files, code, tests, commands, or deployment evidence show has happened.
- **Gate-supported workflow state:** the latest SDLC state supported by an exact accepted artifact or valid decision record.

These may differ. For example, a repository may contain substantial code while the gate-supported state is still missing Intent, or the ledger may propose an old next action while newer files show that action was already attempted. Report both without pretending the code is worthless or accepted. Treat the ledger's `next_action` as a saved proposal until current evidence confirms it is still next.

## Begin read-only

Pause new implementation mutations until the takeover route is clear. Do not undo, delete, format, rewrite, commit, or discard existing work merely because artifacts are missing.

Inspect only what is available and relevant:

1. The current user's latest request and the full visible conversation: original goal, corrections, explicit decisions, rejected options, promised next action, approvals, tool results, failures, unfinished questions, and work performed since DZ last wrote project state.
2. Repository guidance and state the host can access: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or another active instruction file; `PROJECT.md`; `docs/sdlc`; README; version-control status and diff; branch or isolated workspace; relevant source and tests; run instructions; and current plan.
   When `.dz/state.json` exists, run the current DZ state tool's read-only `resume-report`. It must validate the snapshot, read every valid journal record, show the saved run history, list unresolved issues and later issue changes, and compare the latest saved workspace checkpoint with the current Git worktree when available. Reconcile that report with current files, test artifacts, and relevant running state. If no saved comparison exists, state that the timing of later changes is uncertain instead of guessing. If the snapshot is damaged, recover from `.dz/journal.jsonl` and report the recovery. If project guidance is stale, propose `install-guidance` and wait for the takeover confirmation before running it. The ledger is a saved account of execution, not permission to ignore later work and not proof that a decision was accepted or a test passed.
3. Evidence: exact commands and outputs, test or eval results, screenshots or browser evidence, review findings, release records, and known failures.
4. Operational state when relevant: running task or terminal state, migrations, external side effects, deployment environment, and rollback readiness.

Do not open or reveal secrets. Do not assume another task, hidden conversation, or undocumented approval is available. If required context is not visible, name the gap instead of inventing it.

## Evidence and authority ladder

Apply these rules together:

1. The user's current correction or changed goal overrides older product assumptions, but may reopen a gate.
2. An exact Accepted artifact or valid scope-specific decision record establishes a gate. In conversation, a valid decision record requires that the exact Draft or complete decision-relevant diff was visible and the relevant owner explicitly accepted that version. A filename, heading, old summary, informal plan, or code comment does not.
3. Reproducible tests and observed behavior establish implementation evidence, not product intent or approval.
4. Current code, UI, schemas, prompts, and infrastructure reveal candidate behavior and constraints. They may be retained, but they do not prove that users wanted them.
5. Conversation facts may be carried forward without making the user repeat them. If an exact artifact was never shown and accepted, reconstruct it as Draft rather than silently marking it Accepted.
6. Existing authorization remains valid only for its named action, target, environment, cost, and time. Invoking DZ neither revokes a current scope-specific authorization nor expands it.
7. A recorded accepted risk remains valid only for the same action and scope. Do not ask for the same decision again merely because the session changed; reopen it when the action, target, revision, environment, amount, time, consequence, or decision owner changes.

Classify every important item as `supported`, `inferred`, `contradicted`, or `missing`.

Infer only the highest **contiguous** supported gate chain. A later artifact that looks accepted cannot bridge a missing or contradicted Intent, Specification, or Plan.

## Produce a plain-language continuity summary

The first substantive takeover response should be a compact, user-readable summary, not the new-idea interview scaffold. It must describe the present after reconciling the whole available history with changes made since the latest saved record. Keep the precise internal assessment, but explain it so a complete beginner can repeat it back. Use concrete work and results, not category words:

```text
以前已经做到：[name the visible result, not “progress”].
后来又发生了：[name work or changes after the latest saved record, or say that none were found]. These can stay: [name the useful part].
现在还不能确定：[name the exact conflict, missing agreement, or untried result]. If skipped, [one concrete consequence].
我建议接下来：[name the small actions, order, and reason, plus one meaningful option when it changes the outcome]. Ask whether this account is correct and how the user wants to proceed.
```

Do not list every file, replay the entire conversation, or print labels such as `TAKEOVER_AUDIT`, “gate-supported state,” `Intent`, or `Specification` unless the user asks for technical detail. Avoid “现有进度,” “成果,” “验证,” “真实环境,” and “真人试用.” Say exactly what was made, what changed later, what was tried, by whom, and what happened. For example, replace “两项检查通过” with the two observed results, and replace “还缺真人试用” with “还没请以后要用它的人亲手从头做到尾.” Keep the entire beginner-facing takeover report to exactly one compact block: at most four one-sentence lines or bullets, normally under about 220 Chinese characters or 140 English words, with no second audit list or explanatory paragraph before or after it. Group internal detail instead of leaking it. The fourth line contains the recommended next step, reason, meaningful alternative when needed, and one question that invites correction and discussion. Use up to three questions only during a genuine incident when delay increases harm and they cannot be decided separately.

Compact example:

```text
- 以前：页面能粘贴留言；空着会提醒，旧价格问题也能拆开。
- 后来：没有发现别的已证明改动，这两项可以留着。
- 还缺：店主没从头试完，所以不知道回复是否真能用。
- 建议：先请一位店主试一条打码留言，免得继续改错方向。这样接着做对吗？
```

## Route by takeover shape

### A. Discussion exists, but no repository or formal artifacts

- Extract the user's already stated user, situation, problem, desired outcome, boundaries, evidence, and rejected options.
- Do not ask those questions again.
- Identify the smallest material gap preventing an Intent Draft or later artifact.
- Recommend a default if the user is uncertain, then ask only for that gap.
- When mature, show the exact reconstructed Draft and use the normal acceptance protocol.

### B. Code or uncommitted work exists, but SDLC artifacts are missing

- Preserve the working tree. Report which changes appear aligned, questionable, or unrelated; do not delete them.
- Treat existing implementation as a **candidate implementation under review**, not as an accepted product contract.
- Reconstruct `intent.md`, `spec.md`, and `plan.md` progressively from the conversation, code, tests, and docs. Label every inference.
- Ask only for product decisions that cannot be recovered from evidence. Do not make the user choose frameworks already working adequately.
- Show and obtain acceptance of each exact Draft in order. Until Plan acceptance, do not add new implementation changes; read-only inspection and safe evidence collection may continue.
- After Plan acceptance, compare the retained code against the accepted artifacts. Keep aligned work, repair mismatches, and verify the real flow. Do not rebuild from scratch without a concrete reason.

### C. Accepted artifacts exist and the current task fits them

- Verify artifact versions, current code revision, and whether the active work item stays inside the accepted experience, data, permissions, cost, and architecture boundaries.
- Do not reopen Intent or Specification for a bounded defect that does not change their promises.
- If an existing Accepted Plan or an exact, explicitly accepted decision-relevant Plan addendum covers the work, resume the applicable Build or Test slice without demanding duplicate approval.
- If the fix changes scope, acceptance, permissions, provider, architecture, migration, or material cost, reopen only the earliest affected gate. Preserve later artifacts as historical records but treat them as non-governing until reconciled.

### D. Artifacts exist but are stale, inconsistent, or contradicted

- Identify the earliest artifact contradicted by current evidence or the user's changed goal.
- A decision artifact becomes stale for the current iteration only when a material contradiction affects its user, outcome, scope, acceptance, data, permissions, architecture, cost, or other governing boundary. Age alone is not enough.
- Preserve the historical `Accepted` status and decision record. Treat the artifact as non-governing for the current iteration, create a successor Draft or visible decision-relevant diff, and obtain fresh acceptance. Do not invent a `Pending` lifecycle status.
- Verification, review, and release evidence are bound to the recorded code revision, configuration, environment, and test inputs. A later revision does not erase that evidence, but it cannot govern the new revision until the affected checks are repeated.
- `PROJECT.md` is derivative. If it conflicts with accepted artifacts or observed evidence, report the conflict and update the dashboard only when writing is authorized; never use it to overrule the source artifacts.
- Reconcile downstream artifacts and implementation only after the earliest affected decision is accepted. Keep unaffected historical records intact.

### E. Deployment or external side effects are already in progress

- Establish the exact environment, revision, operator, side effects already completed, and rollback state.
- Do not assume that invoking DZ authorizes stopping, retrying, rolling back, or continuing the external action.
- Contain immediate harm only within a current incident runbook and action-specific authority. Otherwise present the safest next authorization decision.

## Continuation rules

- Route from the reconciled present, not automatically from Discovery, the newest code, the last saved stopping point, or the ledger's old proposed next action. Use the earliest unsupported or contradicted gate only to decide which agreement governs the next change.
- Preserve previously accepted exact artifacts unless current evidence reopens them.
- Preserve valid implementation work whenever it can satisfy the accepted contract safely.
- A missing artifact requires retrospective alignment, not retrospective fiction. Never invent past approval.
- The continuity summary is not formal acceptance of a product artifact, but it is a required resume checkpoint. Before new edits, commands, paid calls, external writes, or release actions, show the summary and proposed execution, let the user correct them, and wait for confirmation. After confirmation, carry out the agreed next step without repeatedly asking about unchanged details.
- Keep just-in-time boundaries for credentials, sensitive data, paid calls, external writes, destructive actions, migrations, and release.
- At handoff or pause, update `PROJECT.md` and the current evidence artifact only when writing is authorized, so a later task can resume without reconstructing everything again.
- When persistent state is available, update `.dz/state.json` after every meaningful change and regenerate `PROJECT.md`, `work-items.md`, and `issues.md`. A user pause, cancellation, or early closure is a legal stopping state and never becomes verified completion.

## Takeover completion standard

Takeover is complete when:

- the current objective and active work item are clear;
- observed work and gate-supported state are separately identified;
- existing changes have a keep/review decision rather than being ignored;
- the earliest missing or reopened gate is named;
- current evidence and authorization boundaries are explicit;
- unresolved, deferred, and recently changed material problems are accounted for and routed;
- the user sees the recommended next actions, their order, why they are recommended, and any meaningful alternative in plain language;
- the user has confirmed or corrected the current-position summary and discussed how to proceed;
- the workflow has resumed from that agreed present position without discarding later work or repeating settled questions.
