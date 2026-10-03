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

## Limits

These are synthetic program checks and independent rule review. They do not prove that every model follows the instructions, that any real application has passed its user flow, or that a running parallel worker received a changed goal.

Effort measurement, source relevance, conversation interpretation, worker messaging and everyday communication remain agent instructions. The CLI records and validates the state; it does not automatically time execution, count attempts, cancel processes or attest that model-written approvals and test claims are truthful.

No new real-model/API trial, human trial, live parallel-worker test, full cross-platform run, production deployment or long-term reliability trial was performed for this version. Historical reports keep their original versions and dates. Moving goals, state, deliverables and evidence between platforms may require tool, permission and environment reconciliation or fresh checks.

This update does not bulk-migrate existing projects or enable DZ in a project that explicitly paused it. Use the installed Skill or the portable prompt in an authorized project, and supply its purpose, deliverable and observable completion standard. See `GETTING-STARTED.md` for loading and resumption instructions.
