# Issue Learning Loop

Use this reference whenever development, testing, review, or real use reveals a material problem. The purpose is to stop the same mistake from being forgotten or rediscovered while keeping accepted product decisions under human control.

A user's proposed modification may be a response to a real problem, but it is not automatically the right repair. First use [change-proposal-review.md](change-proposal-review.md) to assess its value, holes, side effects, and better form. Then route an observed problem here; route a new idea, accepted product change, or technical-route change to its existing governing home.

## What to record

Record a problem when it changes a user outcome, blocks an accepted flow, reveals a missing state or edge case, contradicts an accepted assumption, creates meaningful cost or safety exposure, or is likely to recur. Do not fill the ledger with one-off spelling fixes or harmless noise unless repetition makes them material.

Capture the evidence in observable terms:

- where it came from;
- what should have happened;
- what actually happened;
- who or what is affected;
- the route DZ selected;
- the linked work and later proof.

The AI selects the internal category. Do not ask a beginner to choose among technical labels.

## Route the problem to one home

| Internal kind | Use when | Durable home | What DZ does next |
|---|---|---|---|
| `implementation_gap` | The agreed behavior is right, but the product does not do it | linked work item | Record it, repair the smallest cause inside the accepted plan, and rerun a focused regression check. |
| `specification_gap` | User-visible behavior, a page state, recovery, stored or shared information, access, or an acceptance example was never agreed | Specification successor Draft or complete diff | Show the old wording, proposed wording, and concrete effect; wait for the user to accept before implementation. |
| `plan_gap` | The technical approach, provider, dependency, migration, operating cost, or delivery method must change | Plan successor Draft or complete diff | Explain the visible consequence and alternatives; reopen Specification too if the user experience, information, access, cost, or scope changes. |
| `new_idea` | It could be useful but is not required to repair the accepted product | deferred/backlog record | Keep it visible without silently adding it to the current version. |
| `intent_conflict` | New evidence weakens the target user's problem, expected value, or success signal | Intent successor Draft | Reopen the reason for making the product before investing further. |
| `production_feedback` | It was observed after release | feedback record, then human triage | Diagnose and route it to defect, monitor, new intent, or dismissal; do not let popularity or one report silently change the product. |

Never paste every issue into the PRD. Only an accepted change in product behavior belongs in the governing product record. Code defects stay with delivery work; technical choices stay in the Plan; later ideas stay in the backlog; production reports stay in feedback until triaged.

## When to interrupt the user

Do not repeatedly interrupt for an ordinary implementation defect when all of these are true:

- the accepted user-visible behavior stays unchanged;
- no new information is collected, stored, sent, or exposed;
- no access rule, provider, material cost, current scope, external action, deletion, migration, public release, or other authorization boundary changes;
- the fix fits an accepted current work item and plan;
- the AI can make a small reversible repair and verify it.

Record the issue, repair it, and report what happened with the evidence. If any condition is false or uncertain, pause before implementation and show the user:

```text
原来写的是：[old accepted wording]
现在发现：[observable problem]
我建议改成：[complete proposed wording]
这样会影响：[what the user will do or what will happen to their information, access, cost, or current version]
上面哪里不对？都对就直接告诉我。
```

Acceptance of that visible change updates the appropriate decision artifact through the normal artifact lifecycle. It does not authorize a separate paid, destructive, public, production, sensitive-data, or external action.

## Fixed is not finished

Use these meanings consistently:

- `open`: observed and recorded, not yet routed in practice;
- `triaged`: DZ selected the route and next handling;
- `waiting_user`: the next repair would change an accepted product or action decision;
- `in_progress`: an accepted, linked repair is underway;
- `implemented_unverified`: code or content changed, but the result has not been proven;
- `verified`: the problem no longer reproduces on the current target, passed evidence is linked, and a repeatable regression check or equivalent prevention exists;
- `deferred`: intentionally later, with the reason retained;
- `dismissed`: not a current problem, with the reason retained.

Never move directly from “changed” to `verified`. A verbal claim, clean build, or reachable page is insufficient unless it actually exercises the failed behavior. When no check ran, tell the user: “已经改了，但还没证明真的解决。”

## Resume and handoff

Every fresh or mid-task DZ activation reads unresolved issues and later issue changes together with accepted decisions, current files, checks, risks, and visible conversation. The continuity summary names material problems that were found, what was changed, what remains unproven, and what DZ recommends doing next. The saved next action remains only an old proposal.

At pause, cancellation, closure, or handoff, retain every unresolved or deliberately deferred issue. Closing work never turns an unverified issue into a verified one.
