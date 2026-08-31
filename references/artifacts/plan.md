# Implementation Plan Artifact Template

Read accepted intent and specification, repository rules, code, and environment. Perform read-only intake before drafting.

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
- License, file-level notices, attribution/source/source-offer duties, service commercial/data/termination terms, shipped locations, and unresolved legal question:
- Named authorized legal/open-source compliance owner, exact review scope, evidence, and conclusion when triggered; unresolved rights mean reject/block, not accepted risk:
- Maintenance, tests, documentation, advisories, direct/transitive dependencies, install behavior, services, accounts, network calls, information sent out, permissions, and cost:
- Disposition for each: maintained package or stable API / adapt small licensed module / independently implement pattern / reject / bounded technical-fit experiment only after rights, origin, and supply-chain hard gates pass:
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

## First thin slice
- User-visible loop:
- Files or modules affected:
- Explicit exclusions:
- Deterministic checks:
- Real acceptance evidence:
- Rollback or discard path:

## Staged delivery
| Stage | User-visible result | Dependencies | Files/modules | Verification | Risks | Parallel? |
|---|---|---|---|---|---|---|

## Alternatives not chosen
- Alternative — why rejected now — revisit trigger:

## Authorization points
- Account, credential, cost, sensitive data, external write, data change, legal/open-source compliance decision, or release requiring fresh action:

## Handoff completeness
- Could an engineer with no chat history implement and verify this? yes / no
- Remaining ambiguity:
```

Acceptance means the user has inspected and accepted this exact Draft's product impact, platforms, material cost, deferred capabilities, and stage order. Any triggered organizational policy, legal or open-source compliance, security, privacy, financial, regulated, or production risk boundary requires its named authorized owner and evidence for the exact version and use. Plan acceptance cannot create missing reuse rights or waive a hard gate. An execution-capable delivery AI remains accountable for technical correctness through implementation, tests, and independent review; a chat-only AI must hand this responsibility to a capable execution environment.

Immediately after acceptance, create required project-ledger work items for every applicable general-build, frontend, release, and maintain route item. Do not leave the handbook only as prose in this Plan.
