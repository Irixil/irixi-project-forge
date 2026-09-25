# Specification Artifact Template

Read accepted `intent.md` before drafting.

```markdown
# Specification: {product or iteration}

> Status: Draft
> Source of truth: This file
> Based on: Accepted [intent.md](intent.md)
> Decision record: Pending

## Goal trace
- Active `DZ-GOAL` copied exactly from accepted Intent:
- How this version measurably advances that goal:
- Any part of the final goal deliberately left for a later version:

## Product definition
- One-sentence product:
- Product shape: application / deterministic workflow / agent / hybrid
- Primary target: Web / mobile / desktop / extension / API / other

## Primary end-to-end flow
1. User provides:
2. Product does:
3. User sees or confirms:
4. Product returns or changes:
5. State that must persist:

## MVP boundary
### Must
- [DZ-MUST:R1] {One complete observable required outcome, including decisive input, result and boundary}
- [DZ-MUST:R2] {Another independently checkable required outcome, only if applicable}

Keep one complete promise per line. Reuse stable IDs in successors; changed wording needs visible acceptance. Remove unused example items. These lines, outside code fences in the saved specification, are the canonical required outcomes, not a second checklist maintained elsewhere. Explain them naturally to the user; the AI handles the labels. Evidence IDs or rationale may be recorded below without duplicating the governing promise.

Every Must must support the active `DZ-GOAL`, and the Must set must cover every promise this version claims. A valuable capability that does not advance the goal belongs in Later or Won't unless the user explicitly accepts a successor Intent.

### Later hypotheses
- Capability — revisit trigger:

### Won't in this iteration
- Exclusion — reason:

## Users, roles, data, and permissions
- Roles and access boundaries:
- Data sources, rights, sensitivity, retention, and deletion:
- User-visible third-party effects: new account, spending, information sent elsewhere, attribution, failure behavior, or exit limitation:
- External writes, spending, publication, or destructive actions:
- Human confirmation points:

## States and recovery
- Loading / empty / queued / running / waiting / partial / failed:
- Timeout / disconnect / retry / cancel / refresh / resume:
- Source of truth for task and business state:

## AI or agent contract
- Why a model is needed:
- Deterministic parts:
- Model-judgment parts:
- Quality rubric and representative cases:
- Failure impact and human takeover:
- Agent Card or Harness Canvas link, if applicable:

## Acceptance criteria
| Must ID | Additional representative case (does not replace the promise) | Required evidence |
|---|---|---|

## Concern register
| Concern | Severity | Consequence | Safer option and recovery | Required decision owner | Mitigate / accept and continue / pause / cancel | Decision scope and evidence | Status |
|---|---|---|---|---|---|---|---|

## Assumptions and unresolved questions
- Assumption — confidence — validation method — owner:

## Changes from assessed proposals or recorded problems (successor Draft only)
| Proposal conversation/journal reference or Issue ID | Intended benefit, professional verdict, and main hole | Old accepted wording or missing case | Complete proposed wording | Concrete user, information, access, cost, or scope effect |
|---|---|---|---|---|

## Handbook applicability
- Applicable technical, frontend, and deployment baselines:
- Defaults intentionally not used and why:
- Technical assumptions requiring an approved spike:
```

Acceptance means the user has inspected and accepted this exact Draft's experience, Must/Later/Won't boundary, acceptance criteria, and ordinary product tradeoffs. Any triggered organizational policy, legal or open-source compliance, security, privacy, financial, or production boundary requires a decision by its named authorized owner. A residual risk may be accepted and carried forward when that owner is entitled to decide it, regardless of severity; this does not certify frameworks, code quality, or missing evidence. Missing authority or reuse rights remains a blocker.
