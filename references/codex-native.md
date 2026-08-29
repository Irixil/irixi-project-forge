# Codex-Native Capability Mapping and Design Rationale

This document supports maintenance and explanation of the workflow; it does not need to be loaded at the start of every project. Its contents were checked on 2026-08-27 against the `openai/codex` `main` branch implementation snapshot at [`2c4a957`](https://github.com/openai/codex/commit/2c4a95736bea64256a50f7b8506bd33c181cc85a). That commit illustrates the source structure at the time; it does not establish the behavior of any product release. For current capabilities, consult the official documentation and the installed version first.

## Why this is a skill

Codex treats a skill as an authoring format for a reusable workflow: instructions live in `SKILL.md`, and the directory may include references, scripts, and assets as needed. Codex sees the name and description first and loads the full body only after the task matches, so this skill keeps frequently used decision rules in the entry point and places templates and details in references.

Personal skills used across projects live in `$HOME/.agents/skills`. Repository-specific skills live in `.agents/skills` within the repository or along the current directory path. Install this skill at the user level so it can be invoked explicitly in new projects. If a project has a unique workflow, add a narrower skill to that repository.

Official source: [Build skills](https://developers.openai.com/codex/skills)

## Responsibilities of skills, AGENTS.md, project artifacts, and tests

| Layer | Responsible for | Not responsible for |
|---|---|---|
| Skill | Cross-project methods, phases, interview patterns, and quality gates | One-off state for a particular project |
| Current task conversation | The latest user goal, corrections, recent decisions, tool results, and unfinished work visible in this task | Durable state across tasks or proof of an artifact gate that was never explicitly accepted |
| `AGENTS.md` | Stable commands, architecture, conventions, and prohibited actions that Codex must follow whenever it enters the repository | The current milestone or a long-form PRD |
| `PROJECT.md` | A compact status dashboard and links to the accepted SDLC artifacts | Replacing intent, specification, plan, evidence, or enforcement |
| `docs/sdlc/*.md` | Versioned intent, specification, plan, verification, review, release, and feedback records | Stable repository-wide instructions |
| Tests / evals / CI | Repeatable behavioral and quality constraints | Product goals and value judgments |
| Git / PR | Versions, diffs, authorship, acceptance, and rollback history | Complete business context |

Codex first reads the global `~/.codex/AGENTS.override.md`, or `~/.codex/AGENTS.md` if no override exists. It then reads `AGENTS.override.md` or `AGENTS.md` at each level from the project root to the current directory, with instructions closer to the current directory taking precedence. These files are typically loaded once at the beginning of a run or TUI session. Keep them short, precise, and stable. Start a new session after an update for the change to take effect reliably, and put rules that must be enforced deterministically into tests and CI.

Official source: [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)

## How Codex harness capabilities fit into the workflow

| Codex capability | Use in this workflow | Boundary |
|---|---|---|
| Plan mode | Read-only project intake, intent interviews, scope refinement, and a decision-complete plan | Use it only when the current surface supports it. It does not write files or perform development, and a skill cannot pretend to switch modes. |
| Current plan | Track progress after the execution plan has been approved | It is not Plan mode and does not replace the cross-session `PROJECT.md`. |
| `/goal` | Keep long-running work moving toward verifiable completion criteria | Use it only when the current surface supports it and the user sets it explicitly. It does not expand permissions or replace phase approval. |
| Local files, commands, and development tools | Read-only project intake, implementation, builds, and validation | Subject to the sandbox, writable roots, and approvals. |
| Subagents | Use a separate agent thread and context budget for research, comparison, test design, and review | They usually inherit the parent task's model, tools, sandbox, and approvals and share its checkout. They are not a security boundary and do not create worktrees automatically. |
| Worktree | Isolate concurrent writing tasks | It addresses Git working-directory collisions, not security or semantic conflicts. |
| Sandbox / approvals / Rules / Hooks | The sandbox sets technical boundaries, approvals govern escalation, Rules govern command policy, and Hooks add checks | Hosted tools may not pass through a local Hook. `PostToolUse` cannot undo a side effect, and a Hook is not a complete security boundary. |
| `/review` | Independently review a Git diff, commit, or baseline | By default it only reports findings. It is not an end-to-end product verifier and does not approve a merge. |
| Skills | Load stable, reusable methods | Do not pack all current project context into a skill. |
| MCP / plugins | Connect external systems and domain capabilities when needed | They require separate authentication and approval. External metadata does not grant authorization. |
| Scripts / CI | Run deterministic checks and hard gates | Do not encode product judgment as a brittle rule tree. |
| `codex exec` / SDK | Automate stable, repeatable agentic tasks that still require model judgment | Unattended execution cannot pause to ask a person to approve new permissions. Prefer the SDK for CI and jobs. |
| App Server | Integrate authentication, threads, approvals, and events when building a deeply integrated Codex client | Use the SDK for jobs and CI. A client should pin its Codex version and generate schemas from that version; experimental transports are not production guarantees. |

Official sources: [openai/codex README](https://github.com/openai/codex#readme), [Codex CLI](https://developers.openai.com/codex/cli/features), [Long-running work](https://learn.chatgpt.com/docs/long-running-work), [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Worktrees](https://developers.openai.com/codex/app/worktrees), [Code review](https://learn.chatgpt.com/docs/code-review), [Hooks](https://learn.chatgpt.com/docs/hooks), [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)

## Practical design lessons from the openai/codex repository

- `openai/codex` is the primary repository for the open-source Codex agent harness, including the local CLI core, SDK, and App Server. Codex products also span desktop, IDE, web, and cloud surfaces. Local surfaces operate on a local workspace, while cloud surfaces run in a hosted environment; their sandbox, file, network, and approval semantics may differ. Identify the current surface before using the capabilities it actually provides.
- The repository uses a root-level `AGENTS.md` for contribution and validation conventions and keeps repository-specific skills under [`.codex/skills`](https://github.com/openai/codex/tree/main/.codex/skills). This demonstrates that stable knowledge and reusable practices should be layered and version-controlled. `.codex/skills` is an example of that repository's internal layout, not the public installation location for skills; use `$HOME/.agents/skills` for personal skills and `.agents/skills` for repository skills.
- The repository's [Plan mode template](https://github.com/openai/codex/blob/main/codex-rs/collaboration-mode-templates/templates/plan.md) divides planning into grounding in the environment, an intent interview, and an implementation interview. That mechanism is distinct from an execution-time task list. This skill reuses the underlying idea rather than inventing another interview engine.
- The repository exposes different interfaces, including the [Rust core](https://github.com/openai/codex/tree/main/codex-rs/core), CLI/TUI, [App Server](https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md), and [SDK](https://github.com/openai/codex/tree/main/sdk). A skill should therefore describe a surface-independent workflow and let the current Codex surface select the tools it supports. Prefer the SDK for automation and CI jobs. Consider the App Server only when building a deeply interactive client, and recheck its current stability first.
- Approvals, sandboxing, non-interactive execution, MCP, skills, worktrees, subagents, and local review are all harness capabilities. This skill coordinates them instead of recreating them in every product repository.

Do not infer a stable public API from internal repository module names. Before using the SDK, App Server, or non-interactive mode, reread the current official documentation. Legacy Custom Prompts and `codex mcp-server` are not foundations of this workflow.

## Practical design lessons from the AI-native SDLC

Anthropic's playbook uses versioned artifacts to connect planning, design, building, testing, deployment, and maintenance into a loop. The adaptation for Codex retains:

- the artifact chain `intent → specification → plan → implementation/testing → review/release → feedback`;
- a substantive gate is crossed only after the preceding artifact has been accepted;
- agents gather, synthesize, execute, and verify, while people make value judgments and named authorized owners approve triggered risk and production changes;
- the original implementation agent continues making fixes, while the final verifier uses an independent context;
- skills provide guidance, while deterministic tools enforce requirements;
- automatic triggers are introduced gradually only after the manual feedback loop has matured.

This skill now keeps the artifact boundaries explicit even for personal projects: `intent.md`, `spec.md`, and `plan.md` represent different human decisions, while verification, review, and release capture different kinds of evidence and authority. `PROJECT.md` remains a compact dashboard pointing to the current accepted version of each artifact. Fast Track may shorten the documents, but it does not merge the confirmations.

When DZ is invoked midway through a task, the visible conversation and current workspace provide recovery evidence, while accepted project artifacts remain the durable gate record. DZ first maps observed work against gate-supported state, preserves useful changes, and fills only the earliest missing or contradicted contract. It must not assume access to invisible prior tasks or convert existing code into retrospective approval.

Anthropic's `CLAUDE.md` role maps to Codex's repository-level `AGENTS.md`: stable commands, architecture, conventions, protected areas, and recurring mistakes. Current product state and phase decisions remain in the SDLC artifacts.

Source: [The AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)

## Practical design lessons from three local handbooks

- Begin with a technical-fit statement before implementing the current phase.
- Begin before the technical handbooks when the user has only an idea: discover the user problem, desired outcome, evidence, success signals, and MVP boundary first. The handbooks assume a PRD or comparable product contract already exists.
- Treat security, privacy, recoverability, and honest validation as mandatory baselines; the technology stack is only a replaceable default.
- Choose a backend-first approach or an end-to-end vertical slice based on product value.
- Separate fast regression tests with mocks from acceptance tests with a real model or real browser.
- Keep the agent's model, prompt, tools, state, budgets, and human-confirmation points traceable.
- Design the frontend for the complete task lifecycle and its recovery paths.
- Deployment must cover secrets, identity isolation, persistence, observability, and rollback. Delegate provider-specific steps to a deployment skill when needed.
- Treat provider examples as changeable defaults. Prefer least privilege and secure secret entry; ephemeral disk plus a warm instance is not durable storage; and a reachable URL is not full production evidence.

## Practical design lessons from the local Agent Harness tutorial

- High-level phases and gates can be fixed, while the model chooses actions within each phase based on the environment.
- Permissions come before autonomy; tools and external systems do not grant authorization by themselves.
- Task lists, cross-session tasks, skills, project facts, and memory each have distinct boundaries.
- Subagents use independent contexts, while worktrees isolate only the working directories where changes are made.
- Convert fixed orchestration into scripts only after repeated validation, and make the resulting workflow persistent and recoverable.
- “The model wants to stop this turn” is not the same as “the objective is complete.” Completion criteria require verifiable evidence.

This workflow does not carry over Claude-specific APIs, environment variables, Hook formats, MCP configuration, or tutorial runtime code. When Codex already provides an equivalent harness capability, prefer the native one.

## Automation maturity

1. **Human-initiated:** The user accepts intent, boundaries, and the plan one by one; the named authorized release owner approves production; Codex executes and validates.
2. **Semi-automated:** Stable checks move into scripts, CI, code review, and repeatable commands.
3. **Controlled parallelism:** Clear tasks use subagents or worktrees, while a person can still review every result carefully.
4. **Event-triggered:** Monitoring or external events create intents for triage; they do not automatically expand production permissions.
5. **Bounded autonomy:** Only low-risk actions that are well rehearsed, reversible, and explicitly authorized run automatically.

Do not begin at level five. The ceiling on autonomy is determined by risk, evidence, and the capacity for human review—not by how many agents a machine can start at once.
