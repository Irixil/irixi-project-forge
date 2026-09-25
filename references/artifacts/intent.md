# Intent Artifact Template

Draft only after discovery is concrete enough for review.

```markdown
# Intent: {short outcome}

> Status: Draft
> Source of truth: This file
> Based on: User discovery and cited evidence
> Decision record: Pending

## Originator's words
- The idea or problem as the user described it:

## Primary user and triggering situation
- Primary user:
- Triggering moment:
- User, buyer, and approver if different:

## Problem and current workaround
- Current behavior:
- Main pain or loss:
- Why the workaround is insufficient:
- Available evidence IDs, source kinds, and limits:

## Desired outcome
- [DZ-GOAL] {One observable, solution-independent final result for the primary user}
- Success condition that would show this result was reached:
- Initial success signals and whether each is observed evidence or an owner-chosen test threshold:
- Why now:

Keep exactly one `DZ-GOAL` line outside fenced examples. It is the active goal anchor after this Intent is accepted. Features, tools, architecture, milestones, and the next action are ways to reach it, not substitutes for it.

## Evidence and current recommendation
- Recommendation: Proceed / Proceed if / Hold or rethink
- Strongest supporting evidence:
- Strongest contrary or missing evidence:
- Cheapest decisive test:

| Evidence ID | What was observed | Source and date | What it supports | What it does not prove | Confidence |
|---|---|---|---|---|---|
| | | | | | |

> Omit the table only when this is a clear personal utility and the owner's own repeated behavior is the direct evidence. Never invent a citation to make the document look complete. Keep detailed cards in `discovery-evidence.md` when research materially affects the decision.

## Constraints
- Time, budget, platform, data, privacy, permissions, or policy:

## Assumptions and open questions
- Assumption — confidence — validation method:

## Changes from assessed proposals or recorded problems (successor Draft only)
| Proposal conversation/journal reference or Issue ID | Goal relationship: supports / replaces / deviates / unclear | Intended benefit, professional verdict, and main hole | Old and proposed goal wording | Evidence that challenges the old intent | Concrete effect on who is helped, which trouble matters, or how usefulness is judged |
|---|---|---|---|---|---|

## Kill criteria
- Evidence that would cause us to stop, narrow, or rethink:

## Explicit exclusions
- Problems or users this intent does not cover:
```

Acceptance means the user has inspected and accepted this exact Draft's user, situation, one `DZ-GOAL` final-result anchor, success condition, success signals, and material constraints. It does not approve features, architecture, or implementation.
