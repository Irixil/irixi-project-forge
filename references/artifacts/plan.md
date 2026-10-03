# Implementation Plan Artifact Template

Read accepted intent and specification, repository rules, code, and environment. Perform read-only intake before drafting.

This is a menu of decision-relevant fields, not a form the beginner must fill. Keep the first usable slice, promised checks, real constraints and any necessary authority explicit. Include other sections only when triggered; a short “not applicable — no external service” is enough for an irrelevant category. A precise user-decided successor follows SKILL.md's correction rule; do not request duplicate acceptance because a template was rewritten. Do not invent a compliance department or a wrapper layer for a simple local utility.

```markdown
# Plan: {iteration}

> Status: Draft
> Source of truth: This file
> Based on: Accepted [intent.md](intent.md) and [spec.md](spec.md)
> Decision record: Pending

## Technical fit
- Read-only intake baseline: branch or worktree, code revision, dirty files, accepted artifact versions, and environment date:
- Existing architecture and choices retained:
- Path: backend-first / end-to-end vertical slice
- Recommended stack and product impact:
- Required modules and triggering requirements:
- Applicable handbook routes: general build / frontend / release / maintain; reason for every route marked not applicable:
- Required work-item IDs created from each applicable route in `handbook-routing.md`:
- Explicitly deferred infrastructure:

## Existing-parts review
- Review date and exact small behavior needed, or documented reason the bounded scan was skipped:
- Platform/standard baseline and smallest self-build baseline:
- Candidates: exact repository URL, immutable commit or published artifact, relevant files permitted for review, and evidence date:
- Useful part only, plus what will not be imported:
- Actual use and distribution mode: unmodified/modified; source/binary; static/dynamic linking or IPC; SaaS/API; internal/external distribution; outbound product license:
- License or separate rights-holder permission, permission evidence and scope when used, file-level notices, attribution/source/source-offer duties or explicit waiver, service commercial/data/termination terms, shipped locations, and unresolved legal question:
- Named authorized legal/open-source compliance owner, exact review scope, evidence, and conclusion when triggered; unresolved rights mean reject/block, not accepted risk:
- Maintenance, tests, documentation, advisories, direct/transitive dependencies, install behavior, services, accounts, network calls, information sent out, permissions, and cost:
- Disposition for each: maintained package or stable API / adapt small licensed or separately permitted module / independently implement pattern / reject / bounded technical-fit experiment only after rights, origin, and supply-chain hard gates pass:
- Chosen integration boundary, immutable source, resolved lockfile, artifact integrity value or digest, internal owner, update rule, and removal or replacement path:
- Experiment boundary when applicable: question; success threshold; time and cost ceiling; discard condition; passed hard gates; isolated non-privileged sandbox/container; mounts and host access; network allowlist; lifecycle-script controls; resource limits; action log; destroy evidence:
- Planned SBOM tied to release digest, or minimum manual inventory and tooling limitation:
- Live-search or paper-review gaps explicitly unverified:

## Contracts
- Data and migrations:
- Task state and recovery:
- APIs and interfaces:
- Models, prompts, tools, permissions, budgets, and stopping conditions:
- Secrets, identity, files, logging, and cost boundaries:

## Execution effort (only when repair or experimentation may loop)
- Time/cost/attempt bounds and observable progress; use SKILL.md defaults if no existing limit:
- Stop condition, smallest alternative and resume condition:
- Parallel subtasks only when useful and authorized: shared goal/contract, ownership, separate outputs and single integration writer:

## First thin slice
- Active `DZ-GOAL` and Must IDs advanced by this slice:
- User-visible loop:
- Files or modules affected:
- Explicit exclusions:
- Deterministic checks:
- Real acceptance evidence:
- Rollback or discard path:

## Staged delivery
| Stage | User-visible result | Dependencies | Files/modules | Verification | Risks | Parallel? |
|---|---|---|---|---|---|---|

Map every Must ID in the accepted Specification to required work using its exact promise as an acceptance criterion, and keep the chain `DZ-GOAL → Must → work item → next action` visible. Technical route items may have additional criteria. Before a successor Plan is accepted, identify old work to keep, revise or retire and why; use carry-work after acceptance instead of retyping compatible tasks. Preserving implementation never transfers old Passed evidence.

## Alternatives not chosen
- Alternative — why rejected now — revisit trigger:

## Changes from assessed proposals or recorded problems (successor Draft only)
| Proposal conversation/journal reference or Issue ID | Intended benefit, professional verdict, and main hole | Old accepted approach | Complete proposed approach | Concrete product, cost, migration, dependency, or operating effect |
|---|---|---|---|---|

## Authorization points
- Account, credential, cost, sensitive data, external write, data change, legal/open-source compliance decision, or release requiring fresh action:

## Handoff completeness
- Could an engineer with no chat history implement and verify this? yes / no
- Remaining ambiguity:
```

For new or undecided content, acceptance means the user has inspected and accepted this exact Draft's product impact, platforms, material cost, deferred capabilities, and stage order. Apply the core correction rule to already-decided changes. Any actually triggered organizational policy, legal or open-source compliance, security, privacy, financial, regulated, or production risk boundary requires the relevant authorized owner and evidence for the exact version and use. Plan acceptance cannot create missing reuse rights or waive a hard gate. An execution-capable delivery AI remains accountable for technical correctness through implementation, proportionate tests and review; a chat-only AI must hand this responsibility to a capable execution environment.

Immediately after acceptance, create required project-ledger work items for every applicable general-build, frontend, release, and maintain route item. Do not leave the handbook only as prose in this Plan.
