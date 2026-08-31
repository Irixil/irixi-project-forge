# Choosing an Agent Architecture and Designing the Harness

## First decide whether an agent is the right architecture

A conventional application or deterministic workflow is usually a better fit when:

- the steps and branches can be enumerated reliably;
- the output can be produced with ordinary program logic;
- the model does not need to choose its next action autonomously after receiving feedback from the environment;
- the risk is high enough that the process must be strictly predictable.

Introduce an agent only when there is a genuine need for it:

- the environment or request is highly uncertain;
- the model must observe information, reason, choose tools, and continue based on the results;
- a single prompt cannot complete the task and multiple actions are required;
- manually encoding every branch would be brittle and would not generalize.

A hybrid product is often the most robust option: keep deterministic business rules, state transitions, spending limits, and high-risk actions in code, while leaving ambiguous interpretation, candidate generation, and strategy selection to the model.

## Start every agent with a minimal card

The delivery AI drafts the card; the user confirms the product behavior, while a named authorized owner confirms any triggered organizational or regulated action boundary. For a low-risk first version, begin with this card rather than requiring a complete governance worksheet.

```markdown
## Minimal Agent Card
- Objective and verifiable stopping condition:
- Data or environment the agent can observe:
- Available tools and actions:
- Actions that require action-specific human confirmation and the required owner role:
- Recovery after failure, timeout, or an uncertain result:
- 3–5 representative validation cases:
```

Explain the card in product language. A beginner should not be asked to invent tool schemas, retry algorithms, or security controls. The delivery AI recommends those boundaries and asks the relevant decision owner to confirm their effect. A statement such as "give the agent every permission" is not a valid replacement for the action-specific permission and recovery design.

Before the specification gate, challenge whether the requested autonomy is necessary. Search, analysis, ranking, and drafting can often run with broad read-only freedom, while sending, publishing, applying, scheduling, buying, deleting, changing permissions, or mutating infrastructure normally require deterministic checks and a meaningful confirmation boundary.

## When to expand to the full canvas

Use the full canvas if any of the following applies:

- sensitive, personal, or regulated data;
- external writes, message sending, deletion, spending, or infrastructure actions;
- persistent memory, multiple users, multiple tenants, or layered permissions;
- long-running or unattended operation;
- multiple tools, multiple agents, or concurrent execution;
- production use, a high cost of error, or changes that are difficult to reverse.

## Full Agent Harness Canvas

```markdown
# Agent Harness Canvas

## Objective and Stopping Conditions
- Whose objective the agent serves and what it must accomplish:
- When it starts:
- What counts as complete:
- When it must stop and return control to the user:

## Observation
- Inputs, files, logs, pages, or business state it can observe:
- Information that may be stale or untrusted:

## Tools and Action Interfaces
| Tool / action | Atomic input | Observable output | Side effects | Idempotency strategy |
|---|---|---|---|---|

## Knowledge
- Minimum always-on rules:
- Documentation / skills / API specifications loaded on demand:
- Authoritative sources and versions:

## State and Memory
- Current task state:
- Data that must be persisted:
- Stable facts that may be retained across sessions:
- Temporary or sensitive information that must not enter long-term memory:

## Permission Matrix
| Action | allow | confirm | deny | Rationale |
|---|---|---|---|---|

## Human Gates
- Product judgments that require human confirmation:
- High-risk actions that require human approval:
- How state is persisted and work resumes while waiting:

## Budgets
- Maximum steps / time / tokens / cost:
- Retry and backoff policy:
- Concurrency limit:

## Failure Modes
| Failure | Detection | User-visible state | Recovery / compensation |
|---|---|---|---|

## Evals
- Representative success cases:
- Boundary and adversarial cases:
- Tool-permission cases:
- Failure-recovery cases:
- Smoke test with real models and real tools:
```

## Harness implementation principles

- Make tools atomic, composable, and clearly described; validate parameters and outputs against structured schemas.
- Return tool-execution errors as observable results instead of allowing the entire task to fail silently.
- Centralize model-service integration, and make prompt, model, configuration, and tool versions traceable.
- Validate structured outputs, bound retries, and define an explicit exit condition.
- Give long-running work a stable task ID, explicit states, and recoverable storage; persist context while waiting for human input.
- Put external writes, spending, message sending, deletion, permission changes, and infrastructure changes behind deterministic policy and human gates. A gate explains the concrete risk and obtains a scoped decision; it is not an automatic refusal. After an authorized user accepts the disclosed residual risk, continue within that exact scope and retain the decision record.
- Treat authorization as scoped to an action, target, environment, amount, and time. Do not convert a broad statement made during design into standing production authority.
- Keep permission, risk, and evidence separate: permission says whether an action may run; risk records what may go wrong and the user's informed choice; evidence says what actually happened. Accepting risk cannot turn failure into success.
- A worktree isolates only code changes; the sandbox and approvals still govern network access, credentials, and system access.
- Store in memory only verified information that is stable across sessions and genuinely reusable; the current user request always takes precedence.
- Convert fixed orchestration into scripts only after it has proven stable through repeated use. Keep exploratory brainstorming model-driven instead of prematurely encoding it as a large node graph.

## Asynchronous task states

For an asynchronous or streaming agent, consider at least:

```text
idle → submitting → queued → running / streaming
→ waiting_user
→ succeeded / partially_succeeded / failed / cancelled
→ disconnected / stale
```

Every state should answer three questions: what is happening, what the user needs to do now, and what comes next. Backend task state is the source of truth; the UI must not present “cancellation requested” as “the backend task has been cancelled.” After a disconnection, the task should be resumable or queryable by task ID.

## Agent validation

1. **Fast deterministic layer:** mocks, unit tests, schemas, permissions, idempotency, budgets, and failure injection, run repeatedly during development.
2. **Real-behavior layer:** an end-to-end smoke test with real models and real tools, or in a safe test environment, run before accepting the phase.

For a low-risk first version, validate at least the 3–5 cases in the minimal card. For projects that use the full canvas, also assess task success rate, tool misuse, attempts to exceed permissions, retry counts, latency, token usage and cost, human takeover, and failure recovery. Turn every real incident into a new regression case. An independent verifier judges only whether the evidence meets the standard; it does not replace the tests themselves.
