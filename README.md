# Irixi Project Forge

Irixi Project Forge is a guided Codex Skill for taking a nontechnical product manager or beginner from a rough idea to a scoped, verified, releasable application or agent.

Its short invocation name is `dz`.

## What makes it different

DZ does not treat “build me an app” as permission to start coding immediately. It first helps the user discover the real problem, challenges missing assumptions, recommends safe defaults when the user is unsure, and asks for explicit acceptance at the decisions that require human judgment.

The default behavior is:

- start in plain-language product discovery;
- ask one highest-value question at a time, never more than three per round;
- distinguish confirmed facts, recommendations, assumptions, unknowns, and non-goals;
- point out product, adoption, data, AI-necessity, safety, cost, and operational blind spots;
- recommend one path instead of making a beginner choose technical frameworks;
- forbid formal implementation before accepted intent, specification, and plan;
- judge completion by real evidence rather than generated summaries, mocks, builds, commands, or reachable URLs alone.

## AI-native SDLC

DZ follows the six-stage loop and committed-artifact principle from Anthropic's [AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), adapted to Codex:

```text
PLAN        DESIGN       BUILD          TEST              DEPLOY             MAINTAIN
intent.md → spec.md → plan.md + code → verification.md → review/release.md → new intent.md
```

Each stage reads the accepted artifact from the previous stage. The user approves product intent, MVP boundaries, and ordinary tradeoffs; a named authorized owner approves any organizational, legal, security, privacy, financial, or production risk. Codex recommends architecture, implements the accepted plan, verifies behavior, and exposes concerns.

`PROJECT.md` is only a compact dashboard and link index. It no longer compresses intent, specification, plan, and evidence into one document.

## The beginner journey

### 1. Clarify the idea

DZ restates the idea, calls out its biggest blind spot, and asks a small number of questions about the user, triggering situation, current workaround, desired outcome, evidence, and success signal. When the user says “I don't know,” DZ recommends a reversible assumption and a cheap validation method.

Output: accepted `intent.md`.

### 2. Define the first product

DZ converts the accepted intent into one primary flow, Must / Later / Won't boundaries, states and recovery, data and permissions, acceptance scenarios, and a concern register. It challenges whether AI or an agent is actually necessary.

Output: accepted `spec.md` and an Agent Card when relevant.

### 3. Approve the implementation plan

DZ inspects the project and environment, chooses backend-first or a thin end-to-end vertical slice, applies the technology, frontend, and deployment baselines from Irixi's three handbooks, and recommends one minimal technical route.

Output: accepted `plan.md`.

### 4. Build and verify thin slices

DZ implements one real business loop at a time. Model-backed paths use mock regression plus real-model or real-tool smoke tests. UI paths use the real backend and browser, including applicable task states, device sizes, interruption, and recovery. Higher-risk work receives fresh-context verification.

Output: code, tests, and `verification.md`.

### 5. Review and release

The diff is reviewed against intent, spec, and plan. Production preparation covers access, secrets, durable data and files, migration, backup and restore, monitoring, cost, smoke tests, and rollback. DZ stops at an informed production approval gate.

Output: `review.md` and `release.md`.

### 6. Learn from production

Feedback, incidents, and metrics are captured as evidence, triaged by a human, and converted into a new intent only when the product goal needs to change. Resolved failures become tests or evals.

Output: feedback records and, when accepted, a new `intent.md`.

## Technical-handbook integration

The Skill incorporates the decision flow from three Irixi handbooks:

- *AI Product Vibe Coding General Technology Stack Handbook*;
- *AI Product Vibe Coding General Frontend Technology Stack Handbook*;
- *AI Agent Product Launch and Deployment Handbook*.

The handbooks provide mandatory engineering baselines, replaceable defaults, requirement-triggered modules, frontend task-state and browser quality standards, dual-layer model verification, and production readiness checks.

DZ also corrects several risky shortcuts that should not become universal rules:

- prefer least-privilege and short-lived cloud credentials over blanket FullAccess;
- never request secrets in chat;
- do not treat warm-instance ephemeral disk as durable storage for valuable or multi-user data;
- do not treat a reachable URL as proof of a successful product release;
- do not treat invitation codes as a universal public identity system;
- review monitoring and analytics for sensitive-data leakage;
- recheck current provider documentation, eligibility, pricing, limits, and runtime versions at release time.

## Codex-native adaptation

DZ uses Codex's native harness rather than copying Claude-specific commands:

- Plan mode for read-only discovery and implementation planning where supported;
- `AGENTS.md` for stable repository knowledge;
- Skills for reusable cross-project method;
- current plans for execution progress;
- subagents and worktrees only for genuinely independent work;
- sandboxing, approvals, tests, evals, CI, and review as layered controls;
- provider Skills or official documentation for deployment details;
- production authority remains with a named owner authorized for the target environment; for a personal project this may be the user.

See [`references/codex-native.md`](references/codex-native.md) for the mapping to the open-source [`openai/codex`](https://github.com/openai/codex) harness and official Codex capabilities.

## Install

Clone the repository as `dz`, then place or symlink it into the user Skills directory:

```bash
git clone https://github.com/Irixil/irixi-project-forge.git dz
mkdir -p "$HOME/.agents/skills"
ln -s "/absolute/path/to/dz" "$HOME/.agents/skills/dz"
```

Codex usually detects Skill changes automatically. If it does not appear, restart Codex and use a fresh task.

## Use

Start from a vague idea:

```text
$dz I have an idea for an AI product, but I am not technical. Guide me step by step. Start by helping me clarify the user problem and do not write code until I explicitly approve the intent, specification, and plan.
```

In ChatGPT desktop when the local `@` Skill picker is available, select `@dz`. Standalone local Skills are also supported by Codex CLI and the IDE extension. Web or mobile distribution requires packaging the Skill in a plugin; installing this local folder alone does not make `@dz` appear there. See the official [Codex Skills documentation](https://developers.openai.com/codex/skills).

Bring an existing PRD:

```text
$dz Read this PRD. Preserve what is already confirmed, identify only the material product and risk gaps, and take me through the missing gates before implementation.
```

Resume a project:

```text
$dz Continue this project. Read PROJECT.md, the accepted files under docs/sdlc, AGENTS.md, and the latest verification evidence. Tell me the supported stage, the earliest missing gate, and the single next decision.
```

Audit release readiness:

```text
$dz Audit whether this product is genuinely ready for production. Do not deploy yet. Check accepted artifacts, real evidence, identity, secrets, persistence, monitoring, cost, and rollback, then explain the blockers in product language.
```

## Structure

```text
dz/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── guided-dialogue.md
    ├── artifact-chain.md
    ├── artifacts/
    │   ├── intent.md
    │   ├── spec.md
    │   ├── plan.md
    │   ├── verification.md
    │   ├── review-release.md
    │   └── feedback.md
    ├── phase-gates.md
    ├── handbook-routing.md
    ├── agent-harness.md
    ├── codex-native.md
    └── forward-tests.md
```

## Validation

The package is structurally checked with the Codex Skill validator. Its maintenance protocol defines seven fresh-context behavioral test families:

1. a vague “product for everyone” idea;
2. a fashionable, over-scoped multi-agent architecture;
3. an agent requesting excessive email, scheduling, sending, and payment authority;
4. an unsafe request to deploy personal data, frontend secrets, and weak persistence directly to production;
5. premature coding requests between each of the three artifact gates;
6. a legitimate Fast Track request that must retain three confirmations;
7. a monitoring alert that must not inherit authority to create a change.

The test oracles are in [`references/forward-tests.md`](references/forward-tests.md). Run them in fresh tasks before releasing material behavior changes; they judge decision order and observable behavior rather than exact wording.

## License

No license has been selected. The source is publicly visible, but no permission to copy, modify, or redistribute is granted unless the author adds a license.
