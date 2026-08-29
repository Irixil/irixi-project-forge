# Six-Stage AI-Native SDLC Gates

The six stages are a loop, not a waterfall. A stage may return to an earlier artifact when evidence changes the product. What must remain linear is decision authority: an unaccepted artifact cannot trigger the next stage.

```text
PLAN → DESIGN → BUILD → TEST → DEPLOY → MAINTAIN
  ↑                                         │
  └──────────── new accepted intent ────────┘
```

Use natural product language with users. Internal state and gate names exist to prevent skipping, not to make a beginner learn process terminology.

## Entry routing

### New idea

- State: `DISCOVERY`
- First action: guided problem interview
- First artifact: `intent.md`, only after enough conversation to review
- Prohibited: stack selection, formal implementation plan, or product code

### Existing notes or PRD

- Extract confirmed facts, assumptions, conflicts, missing acceptance, and missing risk boundaries.
- Start at the earliest incomplete artifact; do not repeat answers already supported by evidence.
- A document labeled “PRD” may still be only an intent draft.

### Existing codebase

- Inspect read-only first: `PROJECT.md`, SDLC artifacts, `AGENTS.md`, README, Git status, structure, run/test instructions, current data, and evidence.
- Do not read or reveal secrets.
- Report which stage the evidence supports. Code volume does not prove a passed gate.
- Resume from the earliest missing or contradicted artifact.

### Working MVP or deployment request

- Audit the accepted intent, spec, plan, and verification evidence.
- If the core path uses mocks, lacks a real-model or browser check, or has no persistence/identity boundary, return to Test or Design rather than treating it as release-ready.

### Production signal

- Capture evidence before proposing a solution.
- Begin with read-only diagnosis. Execute containment only when an explicit incident runbook and current action-specific authorization cover it.
- Let a human triage whether the signal is noise, a bounded defect, or new intent.

## Stage 1 — PLAN: problem discovery and intent

### Purpose

Capture what is wanted, why, for whom, under which constraints, in the originator's own terms.

### Required work

- identify the primary user and triggering situation;
- understand the current workaround and pain;
- define the desired observable outcome and initial success signals;
- distinguish evidence, assumptions, and unknowns;
- challenge solution-first framing and “everyone” audiences;
- identify the largest value, data, permission, cost, and adoption uncertainties;
- define a validation experiment and kill criterion when evidence is weak.

### User experience

Ask one question at a time by default. Give a recommendation or example. If the user is unsure, turn uncertainty into a reversible assumption and validation step. Explain that no code will be written yet.

### Artifact

`docs/sdlc/intent.md` in Draft, then Accepted status.

### Gate: Intent accepted

Show the exact Draft artifact or a complete decision-relevant diff. The user corrects it or explicitly accepts that exact version, including:

- who experiences the problem;
- in which concrete situation;
- what is wrong with the current approach;
- what outcome should improve;
- how early success will be observed;
- material constraints and the main uncertainty.

Only after acceptance mark that artifact version Accepted and enter Design. Do not pass when the audience is undefined, success equals “the product is built,” or a solution is being treated as evidence of need.

## Stage 2 — DESIGN: product definition and specification

### Prerequisite

Read accepted `intent.md`.

### Purpose

Compress requirements and experience design into a specification the implementation and verification stages can act on.

### Required work

- define the one-sentence product and primary end-to-end flow;
- specify inputs, user-visible process, human confirmation points, outputs, and retained data;
- select one primary terminal and one first-version business loop;
- define Must, Later, and Won't;
- design loading, empty, queued, running, waiting, partial, failure, permission, disconnect, cancel, and recovery behavior as applicable;
- determine application, deterministic workflow, agent, or hybrid;
- define acceptance criteria before implementation;
- run a professional concern review across adoption, data, AI necessity, quality, safety, privacy, permissions, accessibility, cost, and operations;
- route genuine high-uncertainty questions to a bounded experiment.

### User experience

Explain the proposed experience and tradeoffs in product language. The user decides product value, boundary, and ordinary product tradeoffs. A named authorized owner decides organizational policy, legal, security, privacy, financial, or production risk. Do not ask the user to choose frameworks.

### Artifact

`docs/sdlc/spec.md` in Draft, plus a Minimal Agent Card when an agent is included.

### Gate: Specification accepted

Show the exact Draft artifact or a complete decision-relevant diff. The user corrects it or explicitly accepts that exact version, including:

- primary user flow and product result;
- Must / Later / Won't boundary;
- important states and failure recovery;
- acceptance scenarios;
- data, external-action, budget, and permission boundaries;
- unresolved assumptions they are consciously carrying.

Only after acceptance mark that artifact version Accepted and enter technical planning. Blocking concerns must be resolved. Important unresolved concerns need a decision from the named owner authorized for that risk. Deferrable concerns belong in Later, Won't, or the risk register with a revisit trigger.

## Stage 3 — BUILD: technical planning and thin-slice implementation

### Prerequisite

Read accepted `intent.md` and `spec.md`, current repository rules, code, environment, and supplied handbooks.

### Purpose

Make the work inspectable before coding, then build one independently acceptable business slice at a time.

### Planning work

- perform read-only repository and environment intake;
- choose backend-first or end-to-end vertical slice;
- retain reasonable existing architecture;
- apply mandatory baselines, default choices, and requirement-triggered modules;
- specify files/modules, data, state, APIs, prompts, models, tools, permissions, budgets, and stopping conditions;
- define the first real business loop;
- specify fast checks, real acceptance evidence, risks, alternatives not chosen, and rollback;
- make the plan complete enough for an engineer without chat history to implement.

### Artifact before code

`docs/sdlc/plan.md` in Draft.

### Gate: Plan approved

Show the exact Draft artifact or a complete decision-relevant diff. The user explicitly confirms that version's product impact, material cost, new platforms or accounts, deferred capabilities, and phase order. The named authorized owner confirms any organizational or regulated risk boundary. Codex owns technical quality and must not transfer technical sign-off to the user. Only then mark that plan version Accepted and begin implementation.

### Implementation loop

For each approved thin slice:

1. Restate the user-visible result and exclusions.
2. Implement the smallest necessary change.
3. Run fast deterministic checks.
4. Exercise the real flow or interaction needed for that slice.
5. Fix confirmed failures and repeat the same evidence.
6. Update `plan.md` only when implementation materially departs from it.
7. Record evidence in `verification.md`.

The next reversible slice may proceed under the approved plan. Stop for scope changes, new credentials, material cost, sensitive data, external writes, destructive or irreversible actions, incompatible migrations, or release.

## Stage 4 — TEST: continuous feedback and independent verification

### Prerequisite

Read accepted `spec.md`, accepted `plan.md`, the implementation revision, and current evidence.

### Purpose

Determine whether the real product fulfills the accepted promises. The implementation session's self-check is necessary but not always sufficient.

### Evidence layers

- **Deterministic:** unit, schema, state, parser, permission, idempotency, failure-injection, build, lint, type, and integration checks.
- **Real behavior:** real model/tool/network, real browser/backend/device, or safe real integration for every distinct critical contract.
- **Fresh context:** independent verification against intent, spec, and plan for public, agentic, sensitive, costly, larger, or otherwise standard-risk work.

### Mandatory rules

- Freeze acceptance criteria from `spec.md`; changing them reopens Design.
- Protect checks from being weakened merely to pass.
- Label mocks and real systems separately.
- Preserve failures and exact reproduction evidence.
- Verify at least one relevant failure and recovery path, not only the happy path.
- For UI, inspect applicable states, responsive targets, keyboard behavior, console/network, refresh, disconnect, and recovery.
- For agents, verify representative cases, permissions, budgets, stopping conditions, tool misuse, and human takeover.
- For production, verify identity isolation, persistence, backup/restore, observability, cost controls, and rollback.

### Artifacts

`docs/sdlc/verification.md` and, when applicable, `docs/sdlc/review.md` or a linked review record.

### Gate: Reviewed and verifiable

- Every Must criterion has inspectable evidence.
- No unresolved critical finding remains.
- Unverified paths and known limitations are explicit.
- The implementation matches accepted intent, spec, and plan, or accepted revisions exist.

## Stage 5 — DEPLOY: controlled release

### Prerequisite

Read accepted artifacts, passed verification, review results, and the current deployment provider's authoritative documentation.

### Purpose

Prepare all release work while preserving a human production boundary.

### Required work

- name the exact target environment and audience;
- explain the release plan, required accounts, user actions, and cost in plain language;
- use least-privilege, short-lived credentials and secure secret entry;
- verify target-runtime compatibility, identity isolation, durable data and files, migrations, backup and restore, logging and alerts, privacy, cost limits, smoke tests, and rollback;
- prepare provider-specific deployment only after provider selection;
- ensure any paid resource or public exposure receives informed approval;
- give the beginner click-by-click instructions for unavoidable console actions, one screen at a time.

### Artifact

`docs/sdlc/release.md`.

### Gate: Production release approved

A named release owner with authority for that environment explicitly approves it after seeing passed evidence, unresolved risks, cost, and rollback. For a personal project this may be the user. Record the approver role, scope, and approval evidence; stop if authority is unclear. Earlier requests such as “just deploy it” do not count as informed final approval if readiness information was unavailable at the time.

After release, a successful command or reachable URL proves only part of the path. Run the real production core flow, access-isolation check, persistence/recovery check where relevant, and monitoring check before marking Released.

## Stage 6 — MAINTAIN: observe, learn, and restart the loop

### Purpose

Keep the product aligned with user outcomes and turn real failures into durable improvements.

### Start manually

- define a small metric set: success, quality, failure, latency, cost, adoption, and human takeover as relevant;
- collect user feedback and incident evidence;
- triage findings as dismiss, monitor, bounded fix, or new intent;
- add shipped incidents to tests or evals;
- update stable repository instructions only for recurring cross-task lessons;
- introduce deterministic monitoring before model-driven diagnosis;
- automate only low-risk, reversible actions after the manual path and rollback are rehearsed.

### Artifact

`docs/sdlc/feedback/<record>.md`; human-triaged product changes create a new `intent.md` and re-enter Plan.

Monitoring may diagnose read-only and present a feedback or proposed-intent Draft without persisting it. Writing that record, creating code, a branch, commit, PR, external write, or production change must re-enter the applicable gates and receive fresh authorization; monitoring cannot inherit that authority by triggering itself.

## Fast Track boundary

Fast Track is allowed only when all are true:

- the user explicitly requests it;
- the product is a small utility, not a new uncertain product concept;
- local, single-user, low-cost, reversible, no sensitive data, no external writes, no paid actions, and no production release;
- success is objectively verifiable.

It may shorten documents and hold three confirmations close together, but must still confirm intent, specification/boundary, and plan separately. The first real flow and evidence remain mandatory.

If the utility mutates local user files or data, the accepted specification and plan must include a preview or dry run, collision and idempotency behavior, an inspectable change manifest, a tested undo or rollback path, and fresh authorization for the real apply step. Test on disposable copies before originals.

## Reopening rules

- Evidence contradicts the problem or value: reopen Intent.
- A request changes experience, scope, data, permissions, or acceptance: reopen Specification.
- A new architecture, provider, cost, or migration appears: reopen Plan.
- Verification fails: return to the responsible Build slice and preserve evidence.
- Review finds a critical issue: fix and re-verify before Deploy.
- Release fails: follow rollback and return to Test.
- Production feedback changes the goal: human triage creates new Intent.
