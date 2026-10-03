# DZ personal workflow update and validation

Date: 2026-10-03. Workflow version: `2026-10-03.1`. Plugin metadata: `1.0.12`. State format remains `1.1`.

## Entrypoints and scope

The maintained entrypoint is repository-root `SKILL.md`. The plugin entrypoint `skills/dz/SKILL.md` forwards to it, and `portable/DZ-UNIVERSAL.md` is generated from it. A standalone installation contains one `SKILL.md` entrypoint. This update builds on `2026-09-25.2` and preserves its existing reliability repairs and technical handbook routing.

The personal workflow is **接住目标 → 组织执行 → 跟踪变化 → 交付验证 → 下次继续**. These describe collaboration with the user; the six SDLC stages remain the technical implementation detail. No new platform or additional gate states are introduced.

## Changes

- Preserve the latest explicit goal and distinguish a decided correction from exploratory discussion. Reconcile downstream decisions, work, materials and verification without reviving obsolete instructions or deleting compatible results.
- Permit concise visible decisions for small utilities, including one unambiguous acceptance covering all shown choices. A known folder alone does not require initializing a continuity ledger, and multiple agents are optional.
- Bound repetitive repair effort by time, cost, retry count and a no-progress stop condition. Add `effort_limit` to the state tool and schema so a truthful stop has a reason and resume condition.
- Coordinate authorized parallel outputs against the current goal and decision contract. Keep a single ledger writer; old-contract output cannot count as current acceptance evidence.
- Reassess materials as usable, needing recheck, or old-goal history. Preserve supported facts independently of old recommendations or decisions.
- Explain usable results, missing proof, the next useful action and actual user decisions. Save the current goal, results, evidence references, unresolved issues and next action for resumption or transfer.

## Validation evidence

Before preparing this shareable snapshot, the complete local regression suite passed **120 tests in 86.325 seconds**. Four new synthetic CLI tests passed in both the primary and independent checks. After local installation, 14 goal-change and personal-workflow tests passed in 8.808 seconds. The new effort-stop scenario fails against the prior tool because it does not recognize `effort_limit`, and passes against the updated tool.

The four new tests cover:

1. A durable effort stop can be reported read-only and resumed without inventing verified results.
2. A missing stop reason or resume condition is rejected without partial state or journal writes.
3. A passed local check cannot hide a failed mandatory user flow or produce an overall verified verdict.
4. Copied project records preserve the goal, evidence and paused status without granting execution authority.

Independent rule review found and corrected two stale reference conflicts: requiring separate confirmation rounds for a simple utility, and initializing a ledger solely because a project path is known. Resume wording now recognizes an already explicit instruction covering the same position, scope and route. The final review found no remaining required rule or program corrections.

Skill validation, portable-entrypoint synchronization, Python syntax checks, JSON parsing and patch whitespace checks passed. The standalone installation was checked file by file and retained one Skill entrypoint. Raw local logs, deployment records and backups are intentionally excluded from this repository update.

To rerun the repository checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
python3 -B scripts/sync_workflow.py --check
```

## Real model and live-worker trials

A subsequent bounded trial used synthetic local inputs, existing authentication and existing tools. No new credentials, software installation, production actions or new paid-service setup were used. Raw prompts, tool events, file hashes and process receipts remain local; no private project material is included here.

Four fresh, ephemeral **Codex CLI 0.154.0** sessions used **`gpt-6-astra`**, selected from the signed-in account's `model/list` default. The initially configured `gpt-6.1-sol` alias was rejected by this standalone CLI before model execution; those two failed startup requests are not counted as behavior tests. The override applied only to the trial invocation and did not change shared settings.

| Scenario | Observed evidence and scope |
|---|---|
| Explicit monthly-to-daily change | Current Intent, Specification, Plan, successor work and next step were saved for the daily goal; old decisions/work stayed in history. Original supported facts remained, with an applicability annotation; the old monthly conclusion was classified as history. Pause remained; no product code was created. |
| Unconfirmed exploration | The model discussed tradeoffs. The complete project file set and all content hashes stayed identical. |
| Local pass and main-flow failure | Existing input check exited 0; the main flow exited 1 at the protected synthetic storage failure. Source, sample and acceptance hashes stayed unchanged. The record remained partly verified and blocked, with failed mandatory evidence. |
| No-progress stop | One fixed diagnostic probe exited 1 without new information. The model stopped early because source inspection showed no recovery branch or new hypothesis, preserving the attempt budget, `effort_limit` reason and resume condition. Stopping before the maximum is allowed. |
| Fresh-session resumption | A new process without chat history read the updated daily goal and distinguished saved decisions from an unimplemented application. It suggested a current-goal next step without a repeated interview. Complete file set and hashes stayed unchanged. |

The four sessions completed within their 300-second limits (approximately 155, 50, 231 and 61 seconds). The behavior prompts did not require a particular ledger answer; the resulting files and actual tool traces were examined separately. The CLI rejected an invalid work-state transition during the failure trial; the model read the permitted transitions and completed the record through the supported route. This recovery is an observed bounded trial, not a promise that all tool mistakes are recoverable.

The coordinator launched two actual concurrent **Codex host workers**. Their ready messages and isolated outputs reported the old monthly contract, then the accepted daily contract after rereading. The outputs were material review and implementation suggestions. Both ultimately acknowledged the exact current contract, kept the old draft as history and reported product implementation and acceptance as unverified. The coordinator alone wrote the shared ledger. Their initial 90-second waits expired before the direct update message arrived; rereading exposed the change, and follow-up messages supplied explicit acknowledgment. This account rests on coordinator-observed host messages and worker outputs. Separate per-tool worker traces were not exported for independent review, so independent checks can compare their reported versions and results with saved records but cannot separately verify each worker read or message-receipt event. Therefore the observed scope is eventual explicit synchronization and version checking, not instantaneous automatic notification, automatic worker cancellation or concurrent product-code merging.

An installed **Claude Code 2.1.224** reported existing OAuth login, but its real request returned repeated HTTP 401 `authentication_failed` before behavior execution. The scoped trial process was stopped after about 61 seconds, without reading or creating credentials. No second Claude session was attempted. **Second-platform behavior remains blocked and unverified**, even though portable records and rules can be transferred.

An independent reviewer checked the four CLI prompts, raw tool events, baselines and resulting records. All four scoped scenarios passed; read-only state checks on the four synthetic projects also passed. No required DZ behavior or code correction was identified. The review retained the live-worker evidence limitation and second-platform authentication blocker above.

## Limits

These are synthetic program checks, independent review and the specific real-model/live-worker trials above. They do not prove that every model follows the instructions or that a real business application has passed its user flow. Worker acknowledgment was observed in this bounded host scenario only.

Effort measurement, source relevance, conversation interpretation, worker messaging and everyday communication remain agent instructions. The CLI records and validates the state; it does not automatically time execution, count attempts, cancel processes or attest that model-written approvals and test claims are truthful.

No human usability trial, completed second-platform behavior trial, full cross-platform run, production deployment or long-term reliability trial was performed for this version. Historical reports keep their original versions and dates. Moving goals, state, deliverables and evidence between platforms may require tool, permission and environment reconciliation or fresh checks.

This update does not bulk-migrate existing projects or enable DZ in a project that explicitly paused it. Use the installed Skill or the portable prompt in an authorized project, and supply its purpose, deliverable and observable completion standard. See `GETTING-STARTED.md` for loading and resumption instructions.
