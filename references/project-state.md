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

`state.json` is the current execution source. `PROJECT.md`, `work-items.md`, and `issues.md` are generated views. Accepted Intent, Specification, and Plan files remain the source for product decisions; `discovery-evidence.md` stores only decision-relevant source cards and their limits; verification and release files remain the source for product-result evidence. Never store secrets or private customer content in any ledger field.

```bash
python3 <dz-skill>/scripts/dz_state.py init <project> --name "<project name>" --language zh
python3 <dz-skill>/scripts/dz_state.py resume-report <project>
python3 <dz-skill>/scripts/dz_state.py check <project>
```

`init` also merges a marked DZ continuity section into the project's `AGENTS.md` without replacing other repository instructions and stores a Git workspace checkpoint in the journal when Git is available. `resume-report` is read-only: it mechanically validates every journal record, checks that `PROJECT.md` matches the current snapshot, returns a compact current summary, compares the latest saved workspace checkpoint with the current Git worktree, and names any stale guidance or unavailable comparison. Use `--full-history` or `--full-state` only for a detected conflict, recovery investigation, or explicit audit. For an existing DZ project created before this behavior, first run `resume-report`, show the user the takeover account, then install or refresh the managed section after the user confirms:

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

1. On a new task, explicit re-invocation, or unexplained drift, read `PROJECT.md` and run `resume-report`. Within already-aligned continuous work, use the current snapshot, known changes, and visible user instructions; do not repeat the takeover interview each turn. Read the accepted requirements/plan and affected files needed for the next action even when no mismatch is reported. Expand history only to resolve a conflict, missing fact, or audit question.
2. If the snapshot is damaged, inspect recovery options first; perform recovery when project-record repair is authorized and disclose it. Refresh stale guidance after the takeover route is confirmed. Do not mistake a routine side question or a tool result for a new takeover.
3. Compare the records with observable files and runtime facts; preserve discrepancies.
4. Set one smallest safe next action before doing it.
5. After each meaningful change, check, user decision, failure, risk decision, pause, or cancellation, update the ledger immediately.
6. Before stopping, run `can-stop`. Continue one safe action or truthfully enter a legal waiting, blocked, paused, or finished state.
7. Tell the user in plain language what changed, why the chosen checks were enough for this change, what remains unproven, and what happens next.

Writes are atomic. Each accepted mutation appends a full snapshot. If `state.json` differs from the latest valid journal snapshot, ordinary mutations fail until `recover` restores it. A malformed journal tail is skipped. Missing or changed decision, target, or evidence files downgrade claims during recovery instead of leaving an overstated finished verdict. Version 1.1 is single-writer; coordinate agents through work ownership or separate worktrees.

The report keeps actionable `open_items`, deferred/cancelled items and historical counts separate. It also returns `work_to_reconcile`, so old unresolved work cannot silently disappear when the contract changes. `requirement_coverage` lists each accepted Must, matching current required work, missing work and unverified outcomes. Dashboard validation compares the complete text. Git checkpoints normalize child-project paths; an older incompatible checkpoint reports uncertainty until a new aligned checkpoint is saved. These checks do not prove an approval or test claim is honest.

## Decisions, contract, phases, and target

Write each complete non-empty Draft before registering it. The tool hashes that exact file. Acceptance records the decision owner, visible reference, time, and unchanged digest.

```bash
python3 <dz-skill>/scripts/dz_state.py set-decision <project> intent --status draft
python3 <dz-skill>/scripts/dz_state.py set-decision <project> intent --status accepted --by "project owner" --reference "visible acceptance record"
```

Specification requires accepted Intent; Plan requires both. Accepted successor Intent supersedes Specification and Plan; successor Specification supersedes Plan. Drafting a successor leaves current decisions governing. Acceptance changes the combined contract and invalidates old verification, never deletes code. Inspect the affected wording and implementation; after the revised route is accepted, use `carry-work <project> W1 W2 --disposition keep --reason "why these still fit"` to carry compatible items in one operation. The tool creates linked new-contract records, preserves titles/criteria/notes and issue links, and leaves all old records/evidence in history. Carried implementation remains unverified on the new target. Use `--disposition revise` for changed work (one item may supply repeated `--acceptance` arguments), or `--disposition retire` with a reason to remove it from reconciliation candidates. Cancelled/deferred work is never revived by carry. No carried result authorizes an unseen decision, and no old proof becomes current.

Before accepting a new Specification, record every mandatory outcome as one complete `- [DZ-MUST:R1] observable promise` line outside fenced examples. IDs are unique and stable; malformed or duplicate markers are rejected. The tool derives `requirements` from the accepted file and checks that this index still matches it. Required work and evidence use the exact `[DZ-MUST:R1] observable promise` text, not a paraphrase. Every Must must have current required work and current verification before an overall verified verdict or verified release-stage transition. Optional/cancelled/deferred work cannot cover a Must. Technical work can add its own criteria. These are bookkeeping checks, not a semantic guarantee that the visible Specification captured everything the user meant.

The 1.1 snapshot gains a derived `requirements` index and optional work `carried_from` links; use the current tool to read/write these extensions. Old snapshots remain readable. After confirmed takeover, `install-guidance` derives the index without editing accepted files, downgrades unsupported overall claims and keeps history. A legacy Specification without indexed Must lines needs a visible accepted successor before claiming full coverage; do not secretly insert labels into its accepted bytes. Honest pause/partial close remains available.

When a current Accepted decision may change, keep it governing until the successor is explicitly accepted. Save the successor Draft at a different versioned path; the tool records it as a proposal without replacing the current path or contract. Accepting that proposal promotes it, clears the proposal fields, supersedes affected downstream decisions, and downgrades affected current proof. Discarding it keeps the current accepted decision while the journal preserves the proposal and reason:

```bash
python3 <dz-skill>/scripts/dz_state.py set-decision <project> spec --status draft --path docs/sdlc/spec-v2.md
python3 <dz-skill>/scripts/dz_state.py set-decision <project> spec --status accepted --by "project owner" --reference "visible acceptance record"
python3 <dz-skill>/scripts/dz_state.py discard-decision-proposal <project> spec --reason "owner kept the current version"
```

After Plan acceptance, add every applicable handbook route as work and label its phase:

```bash
python3 <dz-skill>/scripts/dz_state.py add-work <project> --id W1 --phase design --title "Technical fit and thin-slice design" --acceptance "The project-specific approach and exclusions are recorded"
```

Normal progress is `pending → in_progress → implemented_unverified → verified`; side exits are `waiting_user`, `blocked`, `deferred`, and `cancelled`. Entering `in_progress` clears the current verification target because observable behavior may change. After the change, record a fresh target. During development rerun the affected acceptance statements and critical shared paths; before release, every required current-contract item must hold current target evidence. Old evidence remains history and may explain what was unaffected, but it cannot by itself restore current verified status. Stage transitions are ordered. Design must have required verified work before Build; Build needs required implemented work before Test; Deploy needs required Design, Build, and Test work verified against an observed target; Maintain needs required release work verified. Moving backward to repair evidence remains allowed.

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

Changing or clearing the verification target also expires issues' active proof links and returns verified issues to implemented-unverified. Reopening a work item has the same effect. Global evidence records, old journal snapshots, resolution notes and regression-prevention details remain intact. Link fresh current-target evidence before marking an issue verified again; old proof must neither block a new check nor masquerade as its result.

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

The ledger records routing; it does not silently rewrite accepted decisions. When the route is Specification, Plan, or Intent, create a complete visible successor Draft or decision-relevant diff and use the normal acceptance lifecycle before implementation. New ideas remain later work until selected. Production feedback stays in its feedback record until human triage. Follow `issue-learning-loop.md` for the interruption boundary and beginner-facing wording.

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
