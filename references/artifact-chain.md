# AI-Native SDLC Artifact Lifecycle

Each stage produces a human-readable, machine-actionable artifact. The next stage reads that artifact instead of reconstructing decisions from chat memory. Create only the current artifact; do not generate an empty document suite at kickoff.

```text
PROJECT.md                         # Status dashboard and links
docs/sdlc/intent.md                # Product decision
docs/sdlc/spec.md                  # Product decision
docs/sdlc/plan.md                  # Product and delivery decision
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

Every artifact records its source of truth, preceding artifact or evidence, relevant revision/environment, and decision or evidence record. A timestamp, Git author, chat summary, or model assertion is not approval or proof.

A conversational decision record is valid only when the exact Draft or complete decision-relevant diff was visible and the relevant owner explicitly accepted that version. Determine workflow authority from the highest contiguous accepted artifact chain; a later file cannot bridge an earlier missing or contradicted gate.

For personal product choices, the user is normally the decision owner. For organizational policy, legal, security, privacy, financial, or production risk, record a named authorized owner's role, scope, and approval evidence; stop if authority is unclear.

## Exact-Draft acceptance protocol

For `intent.md`, `spec.md`, and `plan.md`:

1. Write the artifact with `Status: Draft` only when the stage is decision-mature.
2. Show the exact artifact or a complete decision-relevant diff.
3. Invite corrections and update the Draft visibly.
4. Ask the relevant owner to accept that exact version in product language.
5. Record the acceptance reference and change the same version to `Accepted`.
6. Version it with the code when a repository exists; do not push externally unless requested.

Never silently overwrite an Accepted artifact. A material change reopens the appropriate gate and produces a visible revision.

## PROJECT.md dashboard

Create this only when the project location is known and the user asks to formalize the work. Keep it short:

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
- Next Codex action:

## Evidence and blockers
- Evidence:
- Unverified:
- Known limitation:
- Blocker and recovery condition:
```

Update the dashboard at transitions, material decisions, pauses, handoffs, or new evidence. Do not copy full artifacts into it.

During a mid-task takeover, the chat-level Task Continuity Map comes first. Update `PROJECT.md` only when writing is authorized and routing is clear. If code exists without accepted artifacts, record the implementation as candidate or unverified work; do not falsify past acceptance or discard it automatically.

## Change routing

- Evidence challenges the problem or outcome: revise and re-accept intent.
- Experience, MVP, data, permissions, or acceptance changes: revise and re-accept spec.
- Architecture, provider, material cost, migration, or delivery order changes: revise and re-accept plan.
- A check fails: preserve evidence, return to the responsible slice, then repeat the same check.
- Critical review finding: resolve and re-verify before release preparation.
- Release fails: use the verified rollback, record evidence, and return to verification.
- Production signal: create feedback; human triage decides whether it becomes a bounded defect or new intent.

## AGENTS.md boundary

When coding begins, keep `AGENTS.md` concise and stable: purpose, directory map, start/test/build commands, architecture, conventions, protected areas, security boundaries, and recurring mistakes. Current scope, decisions, and evidence belong in SDLC artifacts. If repository instructions change during a task, read them explicitly or start a fresh task before relying on automatic discovery.
