# Expert Review for User-Proposed Changes

Use this reference when the user suggests or decides a product change. First distinguish exploration from a definite decision. Evaluate both proportionately, but do not demote the latter into a proposal or ask for approval of the user's exact words again. Follow SKILL.md's explicit-correction procedure for recording it. Product choice never automatically grants separate external-action authority.

## Choose the depth before the lens

Give every suggestion at least a real judgment. Match the depth to the consequence:

- **Small and reversible:** wording, spacing, an obvious typo, or a local implementation detail that stays inside accepted behavior may receive one short sentence explaining whether it helps and why, then proceed when the current task already authorizes that edit.
- **Material product change:** inspect the relevant factors below before implementation. Explain the consequence that affects the user's choice; do not turn the full internal review into a required questionnaire or a second approval of an explicit decision.
- **Unclear consequence:** treat it as material until the affected behavior is understood.

Do not make review length depend on how strongly the user states the idea. “Just do it” cannot settle an unspecified choice or authorize an unspecified outside action. Conversely, a precise user-authored change is a decision even before the AI has evaluated it; assess and record it using the core correction procedure, with only unsettled consequential choices left open.

## Classify the relationship to the active goal first

Read the exact `DZ-GOAL` in the current accepted Intent before a material review. Before Intent acceptance, use the user's current explicit desired outcome as a provisional anchor. Classify the proposal internally, and make the relationship visible when it could change the user's decision:

- **Supports:** it advances the same final user result. Review and route it to the earliest affected Specification, Plan, or work item.
- **Replaces:** it changes the beneficiary, observable final result, or success condition. Explain old versus new briefly. A definite user choice is already acceptance of that delta; record its successor Intent in the same turn. If it is only proposed, ask for the missing choice. Professional judgment does not veto an allowed owner decision.
- **Deviates:** it may be useful, but does not credibly advance the active goal and was not presented as a replacement. Default to **Do not adopt now** or Backlog, then return to the goal-critical next action.
- **Unclear:** keep the current goal unchanged. Ask one decision-changing question or run only the smallest authorized learning step that can resolve the relationship.

Changing the method, architecture, sequence, priority, or first slice is not by itself a goal replacement. Conversely, a more achievable proxy result is still a replacement if it changes what success means. Safety, law, rights, evidence, or feasibility may justify recommending a new goal or stopping; they never authorize a silent substitution.

## Start with the reason behind the suggestion

Restate two things before judging:

1. the concrete change the user appears to want;
2. the benefit or problem they appear to be pursuing.

If the proposed mechanism is weak but the underlying benefit is valuable, keep the benefit and recommend a better mechanism. Ask one question only when a missing fact could materially change the verdict. Do not force the user to defend a solution when DZ can infer a safe, reversible starting point and label that inference.

## Select the relevant professional lens

Choose one primary lens based on what the change affects, then add only a secondary lens that could change the recommendation. Do not stage a fake panel of experts or list every discipline.

| Change affects | Primary lens | Questions that matter |
|---|---|---|
| user problem, priority, audience, adoption, or price | product and market | Does it solve the accepted problem, for whom, with what evidence and opportunity cost? |
| flow, wording, layout, trust, or accessibility | user experience | Will people understand, complete, recover from, and trust the task? Who may be excluded? |
| model prompt, retrieval, agent tools, or autonomy | AI product and evaluation | Is AI needed, how will quality be judged, what happens when it is confidently wrong, and where must a human decide? |
| code structure, dependency, provider, performance, or migration | engineering | Is the smallest reliable route clear, maintainable, reversible, and compatible with current work? |
| identity, stored information, sharing, deletion, or outside actions | privacy and security | Who can see or act, what can leak or be abused, how is access limited, and how can the action be recovered? |
| release, support, monitoring, retries, or recurring cost | operations and business | Who operates it, what fails at scale, what does it cost, and how is it stopped or restored? |
| regulated, contractual, medical, legal, or financial consequence | relevant specialist boundary | Which current authoritative rule or qualified owner is needed, and which parts remain uncertain? |

The AI must not claim professional credentials it does not have. When a decisive fact is current, regulated, or high stakes, verify it from an authoritative source when the host can do so; otherwise identify the uncertainty and the person or evidence needed.

## Evaluate the proposal, not the user's confidence

For a material suggestion, inspect these decision factors internally:

1. **User value:** which accepted problem or observed failure improves, and for whom?
2. **Evidence:** what observed behavior, feedback, test, or constraint supports it? What is only preference or inference?
3. **Fit:** does it contradict a current accepted decision, remove an important human confirmation, or expand the product into a different job?
4. **Side effects:** what becomes harder, slower, more confusing, less accessible, less private, less reliable, or more expensive?
5. **Opportunity cost:** what current work is delayed or discarded, and is the benefit worth that trade?
6. **Feasibility and lifecycle:** can it be built, tested, operated, supported, reversed, and later removed without disproportionate burden?
7. **Cheapest learning step:** can a mock, manual trial, small comparison, feature flag, or narrow slice answer the central doubt before full investment?

For a proposal that reads broadly or takes an outside action without per-item confirmation, always inspect and record four failure groups even when only the most important two or three are shown to the beginner:

- irrelevant or excessive information becomes visible to the agent;
- a wrong action impersonates the owner or harms another person;
- a retry, timeout, or race causes duplicate or uncertain outside effects;
- the removed human checkpoint leaves no practical stop, review, or recovery path.

Do not invent evidence to fill the list. Name the strongest reason for the change, the most important hole, and the assumption most likely to reverse the recommendation. For a material change, make at least one concrete opportunity cost visible to the user: the current slice it delays, the recurring review or support work it creates, or the simpler improvement it displaces. “More complexity” alone is not concrete enough.

## Give one owned verdict

Use exactly one internal verdict:

- **Adopt:** the value is supported, the change fits the current product, and the cost and side effects are proportionate.
- **Adopt with changes:** the intent is useful, but the proposed form has a correctable flaw; show the improved form.
- **Test first:** the value or consequence is uncertain and one cheap check could change the decision; name the check and pass or stop result.
- **Do not adopt now:** it does not support the current problem, conflicts with stronger evidence or an accepted boundary, creates disproportionate cost or harm, or displaces more valuable work.

Never answer only “可以,” “好主意,” or “按你的来” for a material suggestion. Also do not oppose a change merely to appear independent. The verdict must follow the evidence and tradeoff.

In beginner-facing Chinese, lead with one of these natural sentences:

- “这个改动值得做，因为……”
- “方向是对的，但照现在这个说法做会……我建议改成……”
- “先别整套做，先用……试一下；如果……再继续。”
- “这次先不做更合适，因为它会……而我们现在更该先解决……”

Then name at most the two or three consequences that could change the user's decision. One should be a concrete delayed or recurring burden when that affects the tradeoff. Ask one natural question only for a material choice still missing under SKILL.md's correction rule; editing the saved record is not by itself a reason to ask again.

## Route and remember the result

Do not create a separate permanent suggestion database. Put the result in the existing governing place:

- a change to who the product helps, why it matters, or how success is judged belongs in successor Intent;
- a change to what people do, what is included, information handling, access, failure or recovery belongs in successor Specification;
- a technical route, provider, dependency, delivery, operating-cost or recovery change belongs in successor Plan;
- an observed problem follows the issue-learning loop;
- a useful but not-current idea goes to the backlog with the verdict and reason;
- a small in-contract implementation improvement stays with its work item.

Unaccepted proposals remain Draft. A definite user decision uses the correction procedure and becomes accepted without a second identical approval; only genuinely new choices wait. Record the decision/reference, assessment, effect and affected record. Preserve disagreement when the user chooses a direction contrary to DZ's recommendation; do not rewrite that assessment as support.

The user may knowingly choose a weaker ordinary product tradeoff. If they have authority and the action is otherwise allowed, continue after recording the decision and concrete consequence. Existing authorization rules still apply to spending, external writes, deletion, migration, sensitive information, public release, production access, and other consequential actions. Missing third-party rights or host capability cannot be converted into an accepted risk.

## Self-check before acting

- Did DZ compare the proposal with the exact active goal and classify it as supports, replaces, deviates, or unclear?
- If the user decided to replace the goal, was that exact change saved and verified without duplicate approval, and was the rejected route stopped? If still exploring, did it remain a proposal?
- Did DZ identify the benefit behind the requested mechanism?
- Did it choose the smallest relevant expert lens instead of pretending to summon a panel?
- Did it distinguish evidence, owner preference, inference, and unknowns?
- Did it give one clear verdict rather than praise plus a hidden caveat?
- Did it name the main hole and the concrete consequence?
- Did it make one concrete opportunity cost or recurring operating burden visible for a material change?
- Did it offer a better shape or the cheapest decisive test?
- Did it avoid silently changing an accepted decision?
- Did it preserve the user's final choice and any separate authorization boundary?
- For broad reading or autonomous outside action, did it check information scope, impersonation, duplicate or uncertain effects, and stop/recovery?
