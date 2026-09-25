# DZ Project State and Continuity

Use this reference after the project directory is known and DZ may save project records. The user does not need to type these commands.

## What the ledger does and does not prove

The ledger prevents accidental forgetting and inconsistent status changes. It hashes accepted decision files and evidence files, keeps an append-only snapshot journal, binds work to one accepted decision contract, and makes target changes invalidate old verification.

It is not a security boundary. The CLI, state file, journal, and Stop hook normally run with the same local authority as the AI. They cannot independently prove that a user really approved something or that a command really ran when the caller can fabricate those inputs. `--by`, `--reference`, and `--source` are audit records, not trust tokens. A product may receive a trusted `verified` attestation only when a host-controlled approval UI and test runner outside the model's write authority issue the decision and execution records. Without that layer, `verified` means only “the local ledger is internally consistent and its files are inspectable.” Sandboxes, native approvals, CI, review, and production policy remain separate controls.

## Files and initialization

```text
.dz/state.json                 # current machine-readable snapshot
.dz/journal.jsonl              # append-only full snapshots
.dz/migrations/*               # backups made by schema migration
PROJECT.md                     # generated plain-language dashboard
docs/sdlc/work-items.md        # generated work view
docs/sdlc/issues.md            # generated material-problem view
docs/sdlc/discovery-evidence.md # optional decision-relevant user and market evidence cards
docs/sdlc/*.md                 # accepted decisions and detailed records
docs/sdlc/evidence/*           # durable test, browser, model, or user-check output
```

`state.json` is the current execution source. `PROJECT.md`, `work-items.md`, and `issues.md` are generated views. Accepted Intent, Specification, and Plan files remain the source for product decisions. The ledger's `goal` object is only a derived index of the exact `DZ-GOAL` line and Intent digest, never a second editable goal. `discovery-evidence.md` stores only decision-relevant source cards and their limits; verification and release files remain the source for product-result evidence. Never store secrets or private customer content in any ledger field.

```bash
python3 <dz-skill>/scripts/dz_state.py init <project> --name "<project name>" --language zh
python3 <dz-skill>/scripts/dz_state.py resume-report <project>
python3 <dz-skill>/scripts/dz_state.py check <project>
```

`init` also merges a marked DZ continuity section into the project's `AGENTS.md` without replacing other repository instructions and stores a Git workspace checkpoint in the journal when Git is available. `resume-report` is read-only: it mechanically checks every journal record, compares all three generated views with the snapshot, returns a compact summary and compares the saved Git checkpoint with the current worktree. Inspect `diagnostics.current_records_valid`, `blocking_errors`, `summary_basis`, generated-view warnings and any unavailable comparison before relying on the summary. A readable but inconsistent snapshot is labelled stored records; a damaged snapshot may fall back to a valid journal baseline, never silently become current truth. If neither is usable, only diagnostic facts are returned. `execution_allowed: false` means this report never grants authority, not that a healthy authorized project can never proceed. `check` and mutations retain their strict rules. Use `--full-history` or `--full-state` for a detected conflict, recovery investigation or explicit audit. For an older project, first show the takeover account, then refresh the managed section after the user confirms:

```bash
python3 <dz-skill>/scripts/dz_state.py install-guidance <project>
```

Use `--language en` for English. Never reinitialize an existing ledger. A project created with state schema 1.0 must be upgraded once with `migrate`; DZ backs up the old state and journal, retains old work and evidence as history, and deliberately removes any old verified claim because 1.0 did not bind it to a complete decision contract or explicit target. A 1.0 risk decision remains history only: migration never turns an old broad approval into a 1.1 action lease, and any material next action needs a fresh exact authorization.

```bash
python3 <dz-skill>/scripts/dz_state.py migrate <project>
```

## Three separate questions

Actual progress is generated from the current-contract work statuses, current verification verdict, and run status. `resume-report` returns it as `current_summary.progress`; `PROJECT.md` renders the same result. Pause, cancellation and unfinished checks remain explicit. No separate editable progress field is stored. `run.stage` remains the separately controlled workflow-gate record, not an activity label: a local repair can be checked and closed without pretending to have completed deployment. Consumers must not describe actual progress from `run.stage` alone. Older projects obtain the corrected report read-only; after takeover confirmation, an ordinary authorized ledger update regenerates the page.

1. **May this turn stop?** An `active` run asks for another safe action. It may stop at `waiting_user`, `waiting_authorization`, `blocked`, `paused`, or `finished`.
2. **Did the user end DZ work?** The user may pause, cancel, or close at any time. That changes the run, never the evidence.
3. **What did the product prove?** Product verification is derived from the current accepted contract, current target epoch, required work, and intact evidence. A request to stop cannot upgrade it.

`finished + cancelled` means DZ stopped taking new product actions. It does not mean an external deployment, model job, payment, message, or deletion stopped. For an already-running action, cancellation permits one bounded cancellation signal, one status check, and the minimum ledger and handoff writes. Record the outside action as cancellation requested, unknown, still running, failed, or confirmed stopped from that real result; the free-text close reason is not proof, and do not keep polling under cancellation authority.

## Fixed turn loop

On every meaningful stateful turn:

1. On a new task, explicit re-invocation, or unexplained drift, read the active final goal in `PROJECT.md` before the saved next action, then run `resume-report`. Within already-aligned continuous work, use the current snapshot, known changes, and visible user instructions; do not repeat the takeover interview each turn. Read the accepted requirements/plan and affected files needed for the next action even when no mismatch is reported. Expand history only to resolve a conflict, missing fact, or audit question.
2. If the snapshot is damaged, inspect recovery options first; perform recovery when project-record repair is authorized and disclose it. Refresh stale guidance after the takeover route is confirmed. Do not mistake a routine side question or a tool result for a new takeover.
3. Compare the records with observable files and runtime facts; preserve discrepancies.
4. Trace `final goal → current Must → work item → next action`, then set the smallest safe next action. If the chain breaks, route the idea as support, an explicit goal replacement, or later work before acting.
5. After each meaningful change, check, user decision, failure, risk decision, pause, or cancellation, update the ledger immediately.
6. Before stopping, run `can-stop`. Continue one safe action or truthfully enter a legal waiting, blocked, paused, or finished state.
7. Tell the user in plain language what changed, why the chosen checks were enough for this change, what remains unproven, and what happens next.

Writes are atomic. Each accepted mutation appends a full snapshot. If `state.json` differs from the latest valid journal snapshot, ordinary mutations fail until `recover` restores it. A malformed journal tail is skipped. Missing or changed decision, target, or evidence files downgrade claims during recovery instead of leaving an overstated finished verdict. Version 1.1 is single-writer; coordinate agents through work ownership or separate worktrees.

The report shows the indexed final goal before execution state and keeps actionable `open_items`, deferred/cancelled items and historical counts separate. It also returns `work_to_reconcile`, so old unresolved work cannot silently disappear when the contract changes. `requirement_coverage` lists each accepted Must, matching current required work, missing work and unverified outcomes. Generated-view validation compares the complete text of PROJECT.md, work-items.md and issues.md; `generated_views.all_current` summarizes those comparisons. A stale generated page is repaired from state, never accepted as a new decision. Git checkpoints normalize child-project paths; an older incompatible checkpoint reports uncertainty until a new aligned checkpoint is saved. These checks do not prove semantic goal alignment, approval, or a test claim is honest.

## Decisions, contract, phases, and target

Write each complete non-empty Draft before registering it. The tool hashes that exact file. Intent acceptance additionally requires exactly one visible `- [DZ-GOAL] observable, solution-independent final result` line outside fenced examples. The tool indexes that exact line for the dashboard and resume report; it never edits an accepted Intent. Acceptance records the decision owner, visible reference, time, and unchanged digest.

```bash
python3 <dz-skill>/scripts/dz_state.py set-decision <project> intent --status draft
python3 <dz-skill>/scripts/dz_state.py set-decision <project> intent --status accepted --by "project owner" --reference "visible acceptance record"
```

Specification requires accepted Intent; Plan requires both. Accepted successor Intent supersedes Specification and Plan; successor Specification supersedes Plan. Drafting a successor leaves current decisions governing. Acceptance changes the combined contract and invalidates old verification, never deletes code. Inspect the affected wording and implementation; after the revised route is accepted, use `carry-work <project> W1 W2 --disposition keep --reason "why these still fit"` to carry compatible items in one operation. The tool creates linked new-contract records, preserves titles/criteria/notes and issue links, and leaves all old records/evidence in history. Carried implementation remains unverified on the new target. Use `--disposition revise` for changed work (one item may supply repeated `--acceptance` arguments), or `--disposition retire` with a reason to remove it from reconciliation candidates. Cancelled/deferred work is never revived by carry. No carried result authorizes an unseen decision, and no old proof becomes current.

Before accepting a new Specification, record every mandatory outcome as one complete `- [DZ-MUST:R1] observable promise` line outside fenced examples. IDs are unique and stable; malformed or duplicate markers are rejected. The tool derives `requirements` from the accepted file and checks that this index still matches it. Required work and evidence use the exact `[DZ-MUST:R1] observable promise` text, not a paraphrase. Every Must must have current required work and current verification before an overall verified verdict or verified release-stage transition. Optional/cancelled/deferred work cannot cover a Must. Technical work can add its own criteria. These are bookkeeping checks, not a semantic guarantee that the visible Specification captured everything the user meant.

The 1.1 snapshot gains derived indexes and optional work metadata; use the current tool to read/write these extensions. Old snapshots remain readable. After confirmed takeover, `install-guidance` builds and validates the full updated state before writing managed guidance: derive current indexes, reconcile unsupported claims, then save. A closed legacy project does not become active. A legacy Specification without indexed Must lines needs a visible accepted successor before claiming full coverage; do not secretly insert labels into its accepted bytes or invent approval. Honest pause/partial close remains available. A failed validation must leave guidance and records untouched; an interrupted write still requires the normal journal recovery check.

For `carry-work --disposition revise`, old notes remain with the predecessor instead of being copied into the new task. Write only current reasons/instructions on the successor. `keep` retains inspected compatible notes; read them for stale execution directions as well as checking criteria.

For an unaccepted proposal, save a Draft at a new path; it does not replace the current goal or contract. Acceptance promotes it, supersedes affected downstream decisions and expires old proof. For a definite user correction, the decision already exists: save its exact delta plus unchanged content without inventing details, then use the atomic path below instead of seeking duplicate approval. Never keep implementing the rejected route during record repair. Both acceptance paths replace the old saved next action with reconciliation, preserve pause/authorization boundaries and regenerate the current views. Discarding a genuine proposal preserves the current decision and proposal history:

```bash
python3 <dz-skill>/scripts/dz_state.py set-decision <project> spec --status draft --path docs/sdlc/spec-v2.md
python3 <dz-skill>/scripts/dz_state.py set-decision <project> spec --status accepted --by "project owner" --reference "visible acceptance record"
python3 <dz-skill>/scripts/dz_state.py discard-decision-proposal <project> spec --reason "owner kept the current version"
```

For an explicit user-decided correction of an already accepted record (or a formerly accepted downstream record superseded by this correction):

```bash
python3 <dz-skill>/scripts/dz_state.py set-decision <project> intent --status accepted --user-change --path docs/sdlc/intent-v2.md --expected-sha256 "<SHA-256 of this exact successor>" --by "project owner" --reference "<actual user instruction or visible accepted delta>"
python3 <dz-skill>/scripts/dz_state.py resume-report <project>
```

Use `spec` or `plan` when only that decision changes. The new path preserves accepted bytes; the digest guards against changed content. The flag is not approval and must never be used for brainstorming, a vague 'continue', unseen inferred choices or an AI recommendation. It reuses the normal successor transition in one journal mutation. Missing metadata, wrong digest or a live authorized outside action fails without changing the snapshot. Handle such a failure explicitly; never report synchronization or resume rejected work. A legacy version first needs its ordinary guidance refresh; do not reinitialize it.

Then reconcile downstream records in the same turn as far as the actual user decision allows. The same flag can record an explicitly settled successor of a previously accepted, now-superseded Specification/Plan; its prerequisites must already be accepted. It cannot accept a never-reviewed initial Draft. Cite the actual delta and retained wording; ask only for materially new choices. Carry/revise/retire old work, using `carry-work --title` for an affected title when carrying one item. The work page explicitly labels older-contract tasks as historical, not current to-dos; do not cancel history merely to hide it. Set the real next action, regenerate any scoped handoff and update an existing host plan/goal when its supported tool and authority permit it. Read back the report: goal, accepted paths, active work and next action must agree. The CLI cannot see unseen conversations, judge semantics, or update another platform's task by itself.

After Plan acceptance, add every applicable handbook route as work and label its phase:

```bash
python3 <dz-skill>/scripts/dz_state.py add-work <project> --id W1 --phase design --title "Technical fit and thin-slice design" --acceptance "The project-specific approach and exclusions are recorded"
```

Implementation progress is `pending → in_progress → implemented_unverified → verified`; side exits are `waiting_user`, `blocked`, `deferred`, and `cancelled`. Beginning a new implementation attempt clears the current verification target because observable behavior may change. After the change, observe a fresh target. During development rerun affected statements and critical shared paths; before release, every required current-contract item needs current-target evidence. Old evidence remains history, not proof for a changed target. Stage transitions remain ordered: Design needs required verified work before Build; Build needs required implemented work before Test; Deploy needs required Design/Build/Test work verified against an observed target; Maintain needs required release work verified. Moving backward to repair evidence remains allowed.

For an inspection that changes no product behavior, create a separate work item with `--mode read_only --reason "what is inspected and why nothing changes"`. The default remains `implementation`; old work without a mode keeps that meaning. Choose the mode when creating the item, not after implementation. Read-only work uses `pending → in_progress → verified`, with new evidence from that inspection, and retains the existing target and unrelated proof. It cannot claim an implementation repair, enter deployment, or create/accept an outside-action lease. An observed target and an active authorized run are needed for this registered verification route; ordinary read-only diagnosis via `resume-report` remains available without them. Do not resume a paused run just to register an inspection unless the user authorized that continuation.

```bash
python3 <dz-skill>/scripts/dz_state.py add-work <project> --id OBS1 --phase maintain --optional --mode read_only --reason "Inspect existing records without product changes" --title "Inspect current records" --acceptance "Current saved records and listed gaps were inspected"
python3 <dz-skill>/scripts/dz_state.py update-work <project> OBS1 --status in_progress
# Perform and record the actual inspection on the unchanged target, then verify OBS1.
```

This mode is a bookkeeping distinction, not an operating-system sandbox. If inspection reveals that implementation is needed, record it separately under the appropriate authority; never label a real change read-only to preserve old proof.

Before recording evidence, explicitly set the observed target. Its proof may be a captured commit, build, or deployment query. Every `set-target` creates a new target epoch, even when revision and environment text are unchanged, because configuration, model, data, or deployment state may have changed.

```bash
python3 <dz-skill>/scripts/dz_state.py update-work <project> W1 --status in_progress
# Perform the bounded work, then observe the result that will actually be checked.
python3 <dz-skill>/scripts/dz_state.py set-target <project> --revision "observed commit or build id" --environment "local test" --source "exact observation command or method" --artifact "docs/sdlc/evidence/current-target.txt"
python3 <dz-skill>/scripts/dz_state.py add-evidence <project> --id E1 --work-item W1 --acceptance "exact acceptance statement from W1" --kind test --claim "..." --source "exact command or method" --artifact "docs/sdlc/evidence/E1.txt" --revision "observed commit or build id" --environment "local test" --result passed
python3 <dz-skill>/scripts/dz_state.py update-work <project> W1 --status implemented_unverified
python3 <dz-skill>/scripts/dz_state.py update-work <project> W1 --status verified
```

Every criterion claimed current for one work item must have intact Passed evidence under the same current contract and target epoch. A Passed record may resolve a Failed or Unverified gap only for the same work item, exact statement, and target epoch. Targeted development checks do not create an overall release verdict; a release candidate needs every required statement on the release target. Old evidence remains history and cannot cover a new deployment or a return to an older revision. Evidence is append-only; never delete, change, or reorder it to obtain a pass.

Changing or clearing the verification target expires active issue proof links and returns verified implementation issues to unverified. Beginning implementation through either a work item or an issue uses the same transition; merely starting a read-only inspection does not. Moving an issue into `in_progress` starts a repair attempt even if its linked work was already running, the issue is new, or it returned through a deferred state. That attempt resets the work and issue proof boundaries; repeating the same status is not a new attempt. To associate an issue without starting a repair, only link its work item. History remains intact. Link fresh current-target evidence before marking the issue verified again; old proof must neither block a new check nor masquerade as its result.

## Material problems and learning

Record a material problem as soon as it is observed. DZ chooses the internal kind from the evidence; never ask a beginner to choose a technical category. The kind automatically selects one durable route: current delivery work, Specification, Plan, backlog, Intent, or production feedback.

```bash
python3 <dz-skill>/scripts/dz_state.py add-issue <project> --id I1 --title "Accepted action fails" --kind implementation_gap --source "manual reproduction" --expected "the accepted action succeeds" --actual "it returns an error" --impact "the user cannot finish" --work-item W1
python3 <dz-skill>/scripts/dz_state.py update-issue <project> I1 --status triaged
python3 <dz-skill>/scripts/dz_state.py update-issue <project> I1 --status in_progress
python3 <dz-skill>/scripts/dz_state.py update-issue <project> I1 --status implemented_unverified --resolution "smallest repair made"
python3 <dz-skill>/scripts/dz_state.py update-issue <project> I1 --status verified --evidence E1 --prevention "repeatable regression check"
```

An implementation issue may move into implementation only when it links to work under the accepted current decision contract. `implemented_unverified` requires a resolution note. `verified` additionally requires linked current Passed evidence and a concrete regression check or equivalent prevention. `deferred` and `dismissed` require a retained reason. A failed update is not persisted, so a premature attempt to call an issue verified cannot rewrite its prior honest state.

The ledger records routing; it does not silently rewrite accepted decisions. When the route is Specification, Plan, or Intent, apply SKILL.md's correction rule: record the user's exact decided delta directly, or show a successor Draft/decision-relevant diff and ask about genuinely unsettled choices. New ideas remain later work until selected. Production feedback stays in its feedback record until human triage. Follow `issue-learning-loop.md` for the interruption boundary and beginner-facing wording.

When records appear duplicated, contradictory, stale, orphaned, or falsely complete, run the focused audit in `project-record-health.md`. Repair generated views from state, preserve historical evidence, and route each material finding through its existing canonical home. Do not create a second permanent status or issue system.

## Risk decisions and exact action leases

Risk severity never causes an automatic refusal. Explain the concrete consequence, safer option, recovery, missing proof, and exact scope. The owner may choose safer handling, informed continuation, pause, or cancellation when they have authority to decide.

Authorization is determined by action type, not severity alone. Spending, external writes or messages, deletion, migration, public release, production access, sensitive-data use, and other material actions require a current decision even if labeled low or medium. An informational risk does not. Adding an actionable risk atomically enters `waiting_authorization`, so a crash cannot leave the action active between “record risk” and “ask permission.”

```bash
python3 <dz-skill>/scripts/dz_state.py add-risk <project> --id R1 --title "..." --level high --action-kind public_release --consequence "..." --safer-option "..." --scope "release rev-1 to staging" --expires-at "<future ISO-8601 time with timezone>"
python3 <dz-skill>/scripts/dz_state.py decide-risk <project> R1 --decision accepted --by "project owner" --reference "visible decision record" --next-action "release rev-1 to staging"
python3 <dz-skill>/scripts/dz_state.py complete-risk-action <project> R1 --outcome completed --reference "deployment record" --next-action "run staging checks"
```

For accepted or mitigated action risk, `--next-action` must exactly equal the reviewed scope. The request snapshots the current accepted contract and target, and records a future ISO-8601 expiry with an explicit timezone; spending also requires `--amount-limit`. Public-release and production actions cannot be accepted without an explicit observed target. The resulting authorization lease stays bound to that scope, contract, target ID, revision, environment, amount limit, and expiry. Before expiry, completion, failure, or cancellation consumes it. Once it expires, DZ must not begin or continue the authorized action under that lease, and only cancellation may release the stale lease. Preserve any later outside result as observed evidence or handoff history rather than presenting it as completion under the expired authorization; create a fresh exact request before any further material step. Changing a product decision, target, or implementation is refused until an authorized lease is consumed or cancelled. A pending request whose context changed must be declined and recreated. Ordinary run updates cannot expand it. A declined action enters `waiting_user` and cannot be resumed with the same recorded scope. Pause or close preserves a still-valid pending decision or unconsumed lease.

This lease makes the ledger consistent; it does not intercept operating-system or external tools. A capable host must enforce the same action ID and scope in a trusted before-action policy and consume the lease from observed results. Risk acceptance never changes Failed or Unverified evidence into Passed, grants missing access, overrides platform policy, or creates third-party rights.

Use `blocked` only for a real missing condition:

```bash
python3 <dz-skill>/scripts/dz_state.py set-run <project> --status blocked --blocker "..." --blocker-kind missing_capability --resume-when "..."
```

Allowed kinds are `missing_capability`, `missing_authority`, `missing_external_condition`, `host_denial`, and `rights_missing`.

## Pause, close, and resume

```bash
python3 <dz-skill>/scripts/dz_state.py set-run <project> --status paused --resume-when "user asks to continue"
python3 <dz-skill>/scripts/dz_state.py close <project> --verdict implemented_unverified --reason "user chose to stop before the real-model check"
python3 <dz-skill>/scripts/dz_state.py set-run <project> --status active --next-action "first unfinished action"
```

- `finished + cancelled`: DZ stopped; external-action state remains separately evidenced.
- `finished + implemented_unverified`: an implementation exists but required checks do not.
- `finished + partially_verified`: only part of the current required behavior passed.
- `finished + verified`: every required current-contract work item passed on the explicit current target.

`finished` is closed to ordinary mutations. Record an outstanding external action outcome if necessary, without reopening or upgrading the finished verdict. To do new project work, explicitly resume the run as `active` first. A move to `waiting_user`, `waiting_authorization`, `blocked`, or `paused` records an honest non-working state and does not permit new product actions.

For a nontechnical user, keep a pause or close reply compact and concrete. Group what exists and was actually tried, what remains unfinished or unproven, whether an outside task was really stopped, and the saved next step or honest closing result. Do not omit a material risk merely to meet a length target. A detailed durable handoff may remain in project files or be linked when it helps or the user asks.

On resume or mid-task re-invocation, trust neither chat nor ledger alone and never treat the recorded next action as a command. Run `resume-report`; the tool validates the full journal but returns a compact current summary and workspace comparison by default. Reconcile that with the relevant visible conversation and current running state. Read relevant current requirements and affected files before acting; expand full history for a mismatch, unexplained change, contradiction, stale view, damage, or material uncertainty. Preserve work performed after the latest saved record. Before new mutations, report the reconciled present, unresolved material problems, and proposed execution in plain language, let the user correct it, and discuss how to proceed. Continue only after that checkpoint is confirmed; it does not retroactively accept product decisions or authorize an external action.

The JSON Schema checks shape. `check` adds cross-record consistency for contract binding, target epoch, evidence, issue routing and proof, stage gates, journal continuity, and risk leases. Neither supplies trusted human or execution attestation by itself. A host lacking a trusted approval and execution channel must disclose that limitation instead of presenting the local ledger as tamper-proof proof.
