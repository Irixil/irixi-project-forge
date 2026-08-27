# PROJECT.md Project Contract

`PROJECT.md` is the default single source of truth, distilling the intent, specification, plan, and evidence of an AI-native SDLC into a maintainable one-page contract. Start with the minimum core and expand the conditional sections only when genuine complexity emerges. Git already preserves authorship and timestamps, so do not manually duplicate versions, dates, or owners in the document body.

Create the file only after the project location is clear, the current mode permits writing, and the user has requested a formal kickoff. Update it only when a substantive decision is made, the project moves between phases, work pauses or changes hands, or new verification evidence becomes available. Anything unconfirmed must be marked as an assumption or pending decision.

If Jira, Notion, Figma, or another system is the official source of truth, record only its link, ID, version, and a local summary. Do not maintain two disconnected “final versions.”

## Minimum Core Template

```markdown
# Project Name

> Current status: DISCOVERY

## Goal

- Target users:
- Real-world context and problem:
- Desired outcome:
- Success signals:

## Scope for This Iteration

### Must Do
- [Capability + verifiable acceptance criterion]

### Not in Current Scope
- [Non-goal + reason for deferral]

### Key Constraints
- Platform / time / budget / data / privacy / permissions:

## Decisions and Unknowns

### Confirmed Decisions
- [Decision + rationale]

### Key Assumptions
- [Assumption + validation method]

### Pending Decisions
- [Question + recommended default + decision deadline]

## Current Thin Slice

- Deliverable for this phase:
- Out of scope:
- Implementation approach:
- Acceptance evidence:
- Next step:

## Latest Verification and Limitations

- Passed: [Acceptance item + method + result or evidence location]
- Not verified:
- Known limitations:
- Current blockers:
```

This is sufficient for a lightweight project. The user may accept the intent, scope, and plan together in a single “one-page project kickoff confirmation.”

## Conditional Sections

Add a section only when its condition applies. Do not generate empty tables.

### Critical Flows and States

Use for multi-page, asynchronous, streaming, audio/video, complex failure recovery, or multi-role products:

```markdown
## Critical Flows and States
- Primary flow:
- Human confirmation points:
- Loading / empty / failure / permission / disconnect / recovery states:
- Source of truth for data and task state:
```

### Technical Fit Statement

Add when beginning formal implementation or taking over an existing codebase:

```markdown
## Technical Fit Statement
- Product shape: conventional application / workflow / Agent / hybrid
- Existing project choices to retain:
- Approach: back-end-first / vertical slice
- New choices and rationale:
- Explicitly deferred capabilities:
- Security, data, cost, recoverability, and deployment boundaries:
```

### Phase Plan

Add when the work has multiple phases that can be accepted independently:

```markdown
## Phase Plan
| Phase | Deliverable | Dependencies | Acceptance Evidence | Risks | Can Run in Parallel |
|---|---|---|---|---|---|
```

### Change Impact

Add when a substantive addition or replacement is requested after the scope is locked:

```markdown
## Change Impact
- Request:
- Impact on scope / schedule / architecture / cost / acceptance:
- Decision: accept / replace / defer / reject
```

### Formal Handoff

Add for multi-person collaboration, a prolonged pause, or release preparation:

```markdown
## Handoff
- Completed:
- Incomplete:
- How to run and verify:
- Known risks and recovery:
- Codex’s next step:
- User’s next step:
```

### Agent Harness

When the product includes an Agent, add the Minimal Agent Card first. Use the Full Agent Harness Canvas in [agent-harness.md](agent-harness.md) only when the relevant risks are triggered.

## When to Split Files

Split content into `docs/product/intent.md`, `spec.md`, `plan.md`, `decisions.md`, or `verification.md` only when at least one of the following is true:

- `PROJECT.md` has become difficult to read in a single review;
- separate teams maintain intent, design, and implementation;
- decisions or verification evidence require an independent audit;
- multiple feature streams are being developed in parallel under different plans.

After splitting, `PROJECT.md` must still contain the current status, authoritative links, key boundaries, and next step. Do not duplicate the full text and create drift.

## Boundaries of AGENTS.md

Once work enters the coding phase, inspect or create a concise `AGENTS.md` containing only the stable information Codex needs every time it enters the repository:

- the project purpose and directory map;
- installation, startup, test, build, and formatting commands;
- architectural constraints, coding conventions, and security boundaries;
- areas that may and may not be modified;
- project-specific rules that require particular attention during code review.

Do not include the current milestone, one-off preferences, lengthy background, or unverified assumptions. Keep project status in `PROJECT.md`, execution steps in Codex’s current plan, and behavioral constraints in tests, evals, or CI.

Codex usually discovers `AGENTS.md` when a run or TUI session starts. If the file is created or changed during the current session, do not assume its instructions have been reloaded automatically. Restart the relevant session or read the file explicitly before relying on the new rules.
