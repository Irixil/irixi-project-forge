# Irixi Project Forge

A risk-adaptive Codex Skill for turning rough ideas into scoped, verified apps and agents.

Irixi Project Forge is designed for the part of product development that happens before and after coding: collaborative discovery, boundary setting, planning, staged implementation, real validation, release decisions, and learning from production feedback.

## What it does

- Brainstorms with you in short, high-leverage rounds instead of dumping a questionnaire.
- Separates confirmed facts, assumptions, open decisions, and explicit non-goals.
- Scales its process to the risk: lightweight, standard, or strict.
- Keeps project state in a compact `PROJECT.md` contract.
- Distinguishes ordinary apps, deterministic workflows, agents, and hybrid products.
- Uses thin end-to-end slices, reproducible evidence, and risk-based review gates.
- Maps the workflow onto native Codex capabilities such as Plan mode, `AGENTS.md`, Goals, subagents, worktrees, review, sandboxing, Skills, SDK, and MCP.

## Workflow

```text
Discovery
→ Intent accepted
→ MVP boundary locked
→ Plan approved
→ Thin-slice build
→ Verification
→ Release approval
→ Production feedback becomes the next intent
```

Small, local, reversible projects can combine intent, scope, and plan into one short kickoff approval. Sensitive data, external writes, paid actions, persistent memory, multi-tenant systems, infrastructure, and production releases trigger stricter controls.

## Install

Clone the repository as `dz`, then place or symlink it into your user Skills directory:

```bash
git clone https://github.com/Irixil/irixi-project-forge.git dz
mkdir -p "$HOME/.agents/skills"
ln -s "/absolute/path/to/dz" "$HOME/.agents/skills/dz"
```

Codex usually detects Skill changes automatically. If it does not appear, restart Codex.

## Use

Start a new project in Codex:

```text
$dz New project: I want to build...
```

In ChatGPT interfaces that use the `@` Skill picker, select it as `@dz`.

For a project with substantial uncertainty, enter Plan mode first when the current Codex surface supports it:

```text
/plan
$dz Help me explore this idea and lock the product boundary before implementation.
```

Resume an existing project:

```text
$dz Continue this project. Read PROJECT.md, AGENTS.md, and the latest verification evidence, then tell me the current stage and next gate.
```

## Structure

```text
dz/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── project-contract.md
    ├── phase-gates.md
    ├── agent-harness.md
    └── codex-native.md
```

## Design sources

The workflow combines:

- the artifact chain and human quality gates from [The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook);
- the current open-source Codex harness and its native concepts from [`openai/codex`](https://github.com/openai/codex);
- practical product, frontend, agent, validation, and deployment patterns distilled from Irixi's internal project manuals and harness studies.

See [`references/codex-native.md`](references/codex-native.md) for the capability mapping and important boundaries.

## Status

The Skill has been structurally validated and forward-tested against both a privacy-sensitive agent idea and a small local application idea.

## License

No license has been selected. The source is publicly visible, but no permission to copy, modify, or redistribute is granted unless the author adds a license.
