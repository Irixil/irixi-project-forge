# Implementation Plan Artifact Template

Read accepted intent and specification, repository rules, code, and environment. Perform read-only intake before drafting.

```markdown
# Plan: {iteration}

> Status: Draft
> Source of truth: This file
> Based on: Accepted [intent.md](intent.md) and [spec.md](spec.md)
> Decision record: Pending

## Technical fit
- Existing architecture and choices retained:
- Path: backend-first / end-to-end vertical slice
- Recommended stack and product impact:
- Required modules and triggering requirements:
- Explicitly deferred infrastructure:

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
- Account, credential, cost, sensitive data, external write, data change, or release requiring fresh action:

## Handoff completeness
- Could an engineer with no chat history implement and verify this? yes / no
- Remaining ambiguity:
```

Acceptance means the user has inspected and accepted this exact Draft's product impact, platforms, material cost, deferred capabilities, and stage order. Any triggered organizational or regulated risk boundary requires its named authorized owner. Codex remains accountable for technical correctness through implementation, tests, and independent review.
