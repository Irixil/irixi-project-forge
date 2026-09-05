# AI-Native SDLC Artifact Lifecycle

Each stage produces a human-readable, machine-actionable artifact. The next stage reads that artifact instead of reconstructing decisions from chat memory. Create only the current artifact; do not generate an empty document suite at kickoff.

```text
PROJECT.md                         # Status dashboard and links
.dz/state.json                     # Current execution snapshot
.dz/journal.jsonl                  # Append-only recovery snapshots
docs/sdlc/intent.md                # Product decision
docs/sdlc/discovery-evidence.md    # Optional evidence cards and research limitations supporting Intent
docs/sdlc/spec.md                  # Product decision
docs/sdlc/plan.md                  # Product and delivery decision
docs/sdlc/work-items.md            # Generated work/evidence ledger
docs/sdlc/issues.md                # Generated material-problem ledger
docs/sdlc/verification.md          # Reproducible evidence
docs/sdlc/review.md                # Independent disposition
docs/sdlc/release.md               # Release authority and production evidence
docs/sdlc/feedback/<record>.md      # Production evidence and triage
AGENTS.md                          # Stable repository knowledge
```

If another system is authoritative, record its link, ID, and accepted version. Keep one source of truth per artifact.

## Lifecycle families

Do not force every artifact into one status vocabulary:

| Artifact | Lifecycle statuses | What changes the status |
|---|---|---|
| `intent.md`, `spec.md`, `plan.md` | Draft → Accepted → Superseded | Explicit acceptance of the exact Draft or decision-relevant diff by the relevant owner |
| `verification.md` | In progress → Passed / Blocked → Superseded | Reproducible checks against frozen criteria |
| `review.md` | In review → Changes required / Passed → Superseded | Independent reviewer disposition |
| `release.md` | Draft → Approved → Deploying → Released / Rolled back → Superseded | Authorized approval, deployment, and post-release evidence |
| feedback record | New → Triaged → Converted / Closed | Human triage |
| issue ledger record | Open → Triaged / Waiting / In progress → Implemented unverified → Verified; or Deferred / Dismissed | Observable problem, selected route, current Passed evidence, and retained regression protection |

Every artifact records its source of truth, preceding artifact or evidence, relevant revision/environment, and decision or evidence record. For Intent, Specification, and Plan, hash the complete visible Draft and record the unchanged digest, deciding owner, visible acceptance reference, and time. A timestamp, Git author, chat summary, or model assertion is not approval or proof.

Execution state uses a separate lifecycle described in [project-state.md](project-state.md). A run can be paused, cancelled, or finished with unverified work without changing any decision artifact or pretending verification passed.

A conversational decision record is valid only when the exact Draft or complete decision-relevant diff was visible and the relevant owner explicitly accepted that version. Determine workflow authority from the highest contiguous accepted artifact chain; a later file cannot bridge an earlier missing or contradicted gate.

User-facing acceptance does not require lifecycle jargon or a magic sentence. Introduce the visible record with everyday wording such as “我把刚才说定的事写成几句话,” “这次先做什么、不做什么,” or “准备先做哪一步，做完怎样亲手试.” Ask what is wrong and let the user reply naturally. “对，就是这个意思” or “没问题” can be explicit acceptance when it unambiguously refers to that exact visible content. “Continue,” silence, enthusiasm, or approval of another action is not acceptance.

For personal product choices, the user is normally the decision owner. For organizational policy, legal, security, privacy, financial, or production risk, record a named authorized owner's role, scope, and approval evidence; wait if authority is unclear. Once the authorized owner knowingly accepts a residual risk they are entitled to decide, retain the risk record and continue inside its exact scope. Risk severity alone is not a blocker. Missing authority, missing technical access, platform prohibition, and unavailable third-party rights remain blockers rather than accepted risk.

## Exact-Draft acceptance protocol

For `intent.md`, `spec.md`, and `plan.md`:

1. Write the artifact with `Status: Draft` only when the stage is decision-mature.
2. Show the exact artifact or a complete decision-relevant diff.
   If plain-language presentation needs multiple messages, number every part, state the total, and do not request or record acceptance until the final part is visible. The acceptance must clearly refer to the complete set.
3. Invite corrections and update the Draft visibly.
4. Ask the relevant owner to accept that exact version in product language.
5. Hash the unchanged Draft, then record the digest, deciding owner, visible acceptance reference, and time before changing that same version to `Accepted`.
6. Version it with the code when a repository exists; do not push externally unless requested.

Never silently overwrite an Accepted artifact. A material change reopens the appropriate gate and produces a visible revision.

## PROJECT.md dashboard

Create this when the project location is known, project-record writes are authorized, and substantive planning or implementation will continue across turns. Do not make a beginner separately ask to “formalize” work they already asked DZ to carry through. Generate it from `.dz/state.json` and keep it short:

```markdown
# {Project name}

> Current stage: DISCOVERY
> Current gate: Intent not yet accepted
> Source of truth: Linked artifacts below

## Product in one sentence
- Current understanding:
- Confidence: confirmed / assumption

## Artifact chain
- Intent: not created | Draft | Accepted — [intent.md](docs/sdlc/intent.md)
- Specification: not created | Draft | Accepted — [spec.md](docs/sdlc/spec.md)
- Plan: not created | Draft | Accepted — [plan.md](docs/sdlc/plan.md)
- Verification: not started | in progress | passed | blocked — [verification.md](docs/sdlc/verification.md)
- Review: not started | in review | changes required | passed — [review.md](docs/sdlc/review.md)
- Release: not prepared | draft | approved | deploying | released | rolled back — [release.md](docs/sdlc/release.md)

## Current decision
- Confirmed:
- Assumptions:
- Blocking concern:
- Next user action:
- Next delivery action:

## Evidence and blockers
- Evidence:
- Unverified:
- Known limitation:
- Blocker and recovery condition:
```

Update the state after every meaningful change, check, user decision, failure, issue route or status change, risk decision, pause, cancellation, or handoff. Regenerate the dashboard, work ledger, and issue ledger from that state; do not edit them into a second source of truth or copy full artifacts into them.

During a mid-task takeover, the plain-language continuity summary comes first. Update `PROJECT.md` only when writing is authorized and routing is clear. If code exists without accepted artifacts, record the implementation as candidate or unverified work; do not falsify past acceptance or discard it automatically.

## Honest stopping and early closure

The user may stop at any time. Record one of these without altering evidence:

- paused — preserve the next action and the condition for resuming;
- cancelled — do not start new product work; for an already-running action, allow only a bounded cancellation signal, one status confirmation, and the minimum state/journal/handoff updates, and do not call it stopped until that check says so;
- implemented but unverified — code or configuration exists, but required real checks did not run;
- partially verified — some required behaviors have passed evidence and every gap remains listed;
- verified — every required work item has passed evidence.

Risk acceptance permits the named action to continue; it never changes a failed or unverified result into Passed.

## Change routing

First assess a user-proposed modification through [change-proposal-review.md](change-proposal-review.md). If it responds to an observed material problem, also classify that problem through [issue-learning-loop.md](issue-learning-loop.md). Preserve the proposal's conversation or journal reference, or the issue ID when one exists, in any successor Draft so later sessions can see why the accepted wording changed. Do not create an issue merely to store an unsupported feature idea.

- Evidence challenges the problem or outcome: revise and re-accept intent.
- Experience, MVP, data, permissions, or acceptance changes: revise and re-accept spec.
- Architecture, provider, material cost, migration, delivery order, adopted third-party part, material dependency, license, or integration-boundary changes: revise and re-accept plan. Also revise Specification when users would see a changed behavior, account, cost, information flow, attribution duty, or acceptance promise.
- A check fails: preserve evidence, return to the responsible slice, then repeat the same check.
- Critical review finding: preserve the failed review and open a scoped risk decision. Recommend resolving and re-verifying, but continue when a named authorized owner knowingly accepts that exact residual risk; never relabel the review or missing evidence as passed. Stop only for a true blocker such as missing authority, capability, required external condition, host permission, or third-party right.
- Release fails: use the recovery or rollback action available and authorized for that exact environment, record what actually happened, and return to verification. If that recovery path was never rehearsed, keep it labeled unverified rather than inventing a verified rollback.
- Production signal: create feedback; human triage decides whether it becomes a bounded defect or new intent.

## AGENTS.md boundary

When coding begins, keep `AGENTS.md` concise and stable: purpose, directory map, start/test/build commands, architecture, conventions, protected areas, security boundaries, and recurring mistakes. Current scope, decisions, and evidence belong in SDLC artifacts. If repository instructions change during a task, read them explicitly or start a fresh task before relying on automatic discovery.
