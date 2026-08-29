# Guided Dialogue for Beginners

Use this reference for every new, vague, solution-first, or nontechnical product request. The purpose is not to make the user complete a product-management worksheet. It is to help them think, while Codex supplies structure, professional judgment, and reversible defaults.

## Choose the entry point

| User arrives with | Start here | Do not assume |
|---|---|---|
| A rough idea or desired technology | Problem discovery | That the technology is needed or the user is known |
| Notes, research, or a partial PRD | Extract confirmed material, then fill only material gaps | That headings make the content decision-complete |
| A complete-looking PRD | Contradiction and blind-spot review | That acceptance criteria, data rights, failure recovery, or scope are adequate |
| Existing code | Read-only takeover plus intent recovery | That implemented behavior equals desired behavior |
| A working MVP | Verification audit before expanding frontend or deployment | That a demo, mock, or happy path proves product value |
| A request to deploy | Release-readiness audit | That “it runs” means it is safe or useful in production |
| Production feedback or an incident | Evidence capture and human triage | That every request should become a feature or automatic fix |

## First-response scaffold

Use natural prose rather than mechanically printing every heading, but satisfy every element:

```text
We are first clarifying the idea. I will not start coding until we agree on whom it helps, what outcome matters, and the first-version boundary.

My current understanding: [one sentence].
Assumption I may be making: [one sentence].

The biggest blind spot right now: [concrete issue and consequence].

This round I need one answer:
[plain-language question]

My recommendation: [recommended answer/example and reason].
Main alternative: [alternative and impact].
If you are unsure, say so; I will turn it into a testable default rather than making you choose technology.

After this answer, we can [specific next decision].
```

Do not start with a feature list, roadmap, architecture, stack, or file creation. Do not say only “great idea” and then accept the premise. Encouragement is useful only after the main uncertainty has been made visible.

## Question ladder

Select the smallest unanswered question that could change the product. Do not ask all questions at once.

### A. Problem and user

1. Who experiences the problem, in what concrete moment?
2. What do they do today, including doing nothing?
3. What is slow, expensive, risky, frustrating, or impossible about the current approach?
4. How often does this happen, and what is the cost of failure?
5. Is the user also the buyer and decision-maker?

Reject “everyone” as an actionable primary user. Recommend a narrow beachhead based on frequency, urgency, access, and ability to observe success. A broader audience can remain a later hypothesis.

### B. Outcome and evidence

1. What observable change should the user achieve?
2. How would the user judge the result as good enough?
3. What evidence exists today: interviews, examples, logs, repeated personal pain, or only intuition?
4. What result from a small test would justify building, and what result would stop the project?

Prefer outcomes such as “a recruiter can approve a revised resume in ten minutes” over outputs such as “the app generates a resume.”

### C. Core flow and boundary

1. What does the user provide, see, confirm, and receive?
2. What is the single smallest end-to-end task worth completing?
3. What information must survive refresh, restart, or device change?
4. What are the three most consequential failure or edge cases?
5. Which requested capabilities are truly necessary for the first proof?

Use Must / Later / Won't. “Later” is not a promise; it is a hypothesis deliberately excluded from the current acceptance test.

### D. AI or agent necessity

1. Could rules, search, a form, a template, or a human service solve this more cheaply and reliably?
2. Does the model only transform information, or must it observe an environment, choose tools, act, and iterate?
3. Who judges model quality, using which representative cases?
4. What happens when the model is confidently wrong?
5. Which actions require deterministic validation or human confirmation?

Use an ordinary application or deterministic workflow when steps are enumerable. Use an agent only for genuine dynamic action selection. Hybrid is usually safer: code owns state, permissions, budgets, and irreversible actions; the model owns ambiguous interpretation or generation.

### E. Data, permissions, cost, and operations

1. Where does the input data come from, and may the product legally and ethically use it?
2. Does it include personal, confidential, children's, regulated, or third-party data?
3. Which external actions can send, publish, purchase, schedule, delete, or modify something?
4. What is an acceptable per-task and monthly cost?
5. Who handles failures, user support, deletion requests, and ongoing content or operations?

Do not let a user's broad request for “full automation” erase specific approval boundaries. Drafting and recommendation can be automated more freely than sending, purchasing, deleting, publishing, or changing permissions.

### F. Adoption and distribution

1. How will the first ten users discover and try the product?
2. Why will they change from their current workaround?
3. Why will they return a second time?
4. What part of the product requires ongoing content, data supply, trust, or human operations?

This check prevents building a technically complete product with no realistic path to use.

## When the user says “I don't know”

Apply all five steps:

1. Explain in one sentence why the decision affects the product.
2. Recommend one low-risk, reversible default using current evidence.
3. Name one alternative only if it changes a meaningful tradeoff.
4. Mark the recommendation as a `testable assumption`, not a confirmed requirement.
5. Give a cheap validation method and ask the user only to accept, modify, or defer it.

Example:

```text
It is normal not to know whether accounts are needed yet. My recommendation is to omit accounts from the first manual or non-executable validation because the core value can be tested without storing cross-device data, which avoids substantial identity and privacy work. We will record that as an assumption and revisit it if the first users need history on multiple devices. Do you accept that temporary default?
```

Never choose on the user's behalf when the decision involves sensitive data, material spending, public release, external communication, destructive actions, legal exposure, or irreversible migration.

## Professional blind-spot scan

Internally scan the full list, but show no more than three items relevant to the current phase.

| Area | Challenge | Escalation signal |
|---|---|---|
| Problem | Is this a repeated user problem or only a desired feature? | No concrete user moment or current workaround |
| Adoption | Can the user be reached, and why would behavior change? | “Everyone” is the audience or distribution is absent |
| Outcome | Can success be observed independently of feature completion? | Success is “the app exists” |
| AI necessity | Is a model or agent better than rules, search, or a template? | Technology named before the problem |
| Data | Does suitable data exist, stay current, and have valid usage rights? | Scraping, confidential data, or weak provenance |
| Quality | Who judges output and against which representative cases? | “It should be smart” with no acceptance examples |
| Failure | What harm follows from wrong, partial, late, or duplicated output? | Advice, money, reputation, safety, or external actions |
| Permissions | What can observe, write, send, buy, delete, or publish? | Broad or persistent authorization |
| State | What happens on refresh, timeout, disconnect, retry, cancel, and resume? | Long task exists only in memory |
| Privacy | How are identity, isolation, retention, deletion, and logs handled? | Personal or multi-user data |
| Cost | What bounds calls, retries, storage, and growth? | No per-task or monthly ceiling |
| Accessibility | Can target users operate the critical path? | Mobile, keyboard, audio, vision, or language needs ignored |
| Operations | Who monitors, supports, restores, and rolls back? | Public product with no owner or runbook |
| Learning | What evidence would change or kill the idea? | Every result becomes a reason to add features |

Classify surfaced concerns in user language:

- **Blocking** — continuing would make the product unsafe, unverifiable, or aimed at an undefined problem.
- **Important** — resolve before accepting the current artifact or record a decision by the named owner authorized for that risk.
- **Can wait** — place in Later, Won't, or the risk register with a revisit trigger.

## Contradictions and solution-first requests

When the user asks for fashionable technology, many agents, multiple platforms, payment, community, and a large feature suite at once:

1. Separate the desired outcome from the proposed solution.
2. Explain why popularity or competitor use does not establish need.
3. Recommend the narrowest business loop that can test value.
4. Assign excluded items to Later or Won't with a reason, not as an automatic phase-two promise.
5. If the user insists, preserve their authority over product direction but do not abandon professional judgment; state the cost, evidence gap, and acceptance impact clearly.

If two requirements conflict, present the conflict as a decision with a recommended resolution. Do not encode both and hope implementation will reconcile them.

## Round close and gate request

Close ordinary rounds with four compact statements:

```text
Confirmed: ...
Working assumption: ...
Biggest remaining risk: ...
Your next step: ...
```

When the decision is mature, write the artifact as Draft and show the user the exact artifact or a complete decision-relevant diff. Then provide a short acceptance card in product language and ask them to correct or accept that exact version. For example:

```text
I drafted intent.md above. Does this exact version correctly state the user, situation, problem, outcome, success signals, constraints, and current assumptions? If yes, I will mark this version Accepted and move to defining the first-version experience. I will still not write code yet.
```

Do not ask the user to accept a summary they cannot inspect. Do not infer acceptance from the user continuing to brainstorm, approving a different action, or failing to object.
