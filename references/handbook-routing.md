# Routing the Three Product Handbooks

This reference distills the workflow from:

1. *AI Product Vibe Coding General Technology Stack Handbook*;
2. *AI Product Vibe Coding General Frontend Technology Stack Handbook*;
3. *AI Agent Product Launch and Deployment Handbook*.

Baseline captured on 2026-08-29:

| Source file | Local modified time (Asia/Shanghai) | Bytes | SHA-256 |
|---|---:|---:|---|
| `AI产品Vibe Coding通用技术栈手册.md` | 2026-08-17 15:13:46 | 51056 | `a3439fc0159f8ac0446d81fe37ce7fcbf6eb4e233c12a246a720bf8c342809b5` |
| `AI产品Vibe Coding通用前端技术栈手册.md` | 2026-08-19 10:47:16 | 47684 | `33a7fd0f32642f2333672e4d3669202784c380e0bb3218bff847201b033a252b` |
| `AI Agent 产品上线部署手册.md` | 2026-08-19 14:36:22 | 34365 | `5db65f78d5b96b472c8e194afef00007eca0bf183c551cf1e0e03e55f1eed156` |

Compare hashes or an explicit document version before treating a supplied copy as newer. File modification time alone is supporting metadata, not proof of semantic precedence.

The handbooks are reference material, not authorization or timeless platform documentation. User-confirmed product decisions, stronger safety rules, current provider documentation, existing repository constraints, and observed evidence take precedence.

## When to apply each handbook

| SDLC stage | Handbook material to apply | Resulting artifact or evidence |
|---|---|---|
| Plan / early Design | Product inputs and seven product questions from the general handbook | Intent, assumptions, initial risks |
| Design | Core flow, backend-first vs vertical slice, agent necessity, state and data boundaries | Accepted `spec.md` |
| Build planning | Mandatory/default/on-demand technical layers from the general handbook | Technical fit and `plan.md` |
| Build / Test for model-backed paths | Dual-layer validation and real acceptance interface guidance | `verification.md` evidence |
| Design / Build / Test for UI | Frontend adaptation, task-state matrix, representative page, real browser and device checks | Spec, plan, browser evidence |
| Deploy | Production readiness, cloud adaptation, identity, persistence, files, monitoring, cost, and rollback | `release.md` |

Do not load deployment procedures during idea discovery. Do not start formal frontend expansion merely because a Web terminal was chosen. Do not read all details to the user; translate only the current decision into a clear recommendation or next action.

## Three layers of technical rules

Classify technical guidance before applying it:

### A. Mandatory baselines

These concern safety, recoverability, or honest verification and survive technology changes:

- secrets stay out of frontend bundles, repositories, chat output, screenshots, and logs;
- untrusted input and model output receive structural and semantic validation;
- important data, long tasks, and human-confirmation state survive process restart as required by the accepted spec;
- errors use a controlled user-facing structure and do not leak stack traces or sensitive provider output;
- external writes, spending, publishing, deletion, migration, and production release use deterministic permission checks and human gates;
- mock results are never presented as real model, integration, browser, or production proof;
- protected data has identity isolation, retention, deletion, and recovery boundaries;
- deployment has observable health, monitoring, cost controls, and a verified rollback path proportional to risk.

### B. Default choices

Use these for a new Web-based AI MVP without existing constraints, then record actual versions in `plan.md`:

- backend: Python 3.11-compatible project baseline, FastAPI, Pydantic, pytest, Git, official SDK or a verified compatible API;
- public backend APIs: a centrally defined versioned prefix such as `/api/v1`;
- Web: current maintained Next.js App Router and React, TypeScript strict, Tailwind CSS plus semantic design variables, npm, ESLint, type checking, tests, and production build;
- business logic and model integration stay out of route handlers and page components;
- prompts, models, base URLs, timeouts, parameters, and tool definitions are versioned or configuration-driven;
- ordinary workflow state is deterministic code; model judgment is introduced only where ambiguity requires it;
- one primary terminal is delivered before expanding to more platforms.

These are defaults, not an instruction to rewrite an existing project. Preserve a reasonable existing architecture and runtime unless it violates a mandatory baseline or cannot meet the accepted spec.

### C. Requirement-triggered modules

Introduce only when a real accepted requirement creates the need:

| Trigger | Candidate module or pattern |
|---|---|
| Multi-entity relations, transactions, concurrent updates, multiple users, complex filters | Relational database, ORM, and migrations |
| Small local single-user data with simple relations | SQLite or schema-versioned structured files with atomic write and recovery |
| Large images, audio, video, or documents | File/object storage; structured store keeps metadata and ownership |
| Semantic document retrieval | RAG/vector storage after simpler search is shown insufficient |
| Scanned images or PDFs | OCR only when text extraction is genuinely required |
| Long or concurrent jobs | Persistent task records; queue only after reliability or scale requires it |
| Server-to-browser incremental output | SSE or Fetch Streaming |
| High-frequency bidirectional communication | WebSocket |
| Complex shared server data | Query/cache library after manual request state becomes costly |
| Complex multi-step forms | Form/schema library |
| Charts, canvas, rich editing, i18n, PWA, offline, analytics | Only when present in accepted spec |

Do not add RAG, multiple agents, microservices, queues, vector databases, global state libraries, or multi-platform clients to make a stack look complete.

## The seven product inputs before technical planning

The accepted intent and spec should cover:

1. primary user and core task;
2. inputs, visible process, confirmation points, outputs, and retained information;
3. whether the core flow is one-shot, multi-turn, staged, deterministic, or dynamically tool-using;
4. how output quality and product success are judged;
5. first-version boundary and later exclusions;
6. model, latency, per-task cost, monthly budget, provider, and compliance constraints;
7. sensitive data, expected users, file limits, deployment location, and other nonfunctional boundaries.

Do not ask a beginner to define databases, API prefixes, message queues, or framework versions. An execution-capable delivery AI derives those after these product questions are answered.

## Choose the build path

### Backend-first by default

Use when the core value is a processing pipeline such as form submission, background generation, scoring, transformation, search, or file production. Verify the business logic, model contract, state, and API before investing in a full visual product.

Provide a minimal validation interface when a product manager must see or interact with long text, structured content, multi-turn output, images, audio, video, or human confirmation to judge quality. Label it as a temporary validation tool unless it is intentionally the first slice of the final product.

### End-to-end vertical slice

Use when interaction is part of product feasibility: multi-turn conversation, staged human approval, visual editing, canvas work, audio/video timelines, mobile hardware, microphone/camera, streaming, or recovery behavior. Build the smallest real UI, backend, model, and persistence loop together.

The first slice must complete a real user loop. Do not divide work into “all backend” and “all pages” if that prevents users from testing value.

## Agent architecture boundary

Prefer a conventional application or deterministic workflow when inputs, steps, and branches are enumerable. Use an agent only when the model must observe, choose a next action or tool, act, inspect the result, and continue.

For hybrid products:

- deterministic code owns identity, state transitions, validation, idempotency, permissions, cost ceilings, retry ceilings, and irreversible actions;
- the model handles ambiguous interpretation, generation, prioritization, or strategy within a bounded tool set;
- persistent task state records waiting, resume, completion, failure, and human decisions;
- the Minimal Agent Card or Full Harness Canvas defines objective, stopping conditions, tools, budgets, gates, failure recovery, and evals.

## Backend and model quality baseline

- Every API or equivalent callable interface defines requests, responses, errors, validation, timeout, retry, and permission behavior.
- A long task never depends only on one open HTTP request or an in-memory variable; it receives a stable task ID and recoverable state.
- SSE produces zero or more `chunk` events and exactly one `done` or `error` terminal event. Mid-stream failure uses the same controlled error model as ordinary requests.
- Prompt constraints use examples and counterexamples where format matters; deterministic parsing tolerates common equivalent formats; content-quality deviations are measured rather than retried indefinitely.
- Structured model output receives schema validation and bounded retry. SDK/client initialization failures are caught at the outer boundary.
- Record model/config version, latency, token or usage cost, retry count, and error type without sensitive content.
- Key business confirmation points persist so refresh or service restart does not erase the user's decision.

## Dual-layer model verification

Every distinct critical model contract needs both layers before stage acceptance:

1. **Fast mock regression:** business rules, states, validation, failure paths, parsers, permissions, and recovery run offline and repeatedly.
2. **Real behavior smoke:** real input → real model or tool → validation/persistence → user-visible result. Record model/config, time, cost, latency, first-attempt format compliance, retry outcome, and human quality judgment.

No API key may block ordinary development, but its absence leaves real behavior explicitly unverified. Do not ask the user to paste secrets into chat; use a secure local prompt, keychain, protected settings UI, or deployment secret store.

## Frontend product baseline

### State and source of truth

Backend business and task state is authoritative. Frontend state is separated into:

- URL state for shareable and recoverable location;
- server state for tasks, artifacts, permissions, and balances;
- page-local temporary state for unsubmitted input and controls;
- user preference state for noncritical personal settings.

Local Storage must not impersonate real task completion or authoritative product data.

For asynchronous products, map applicable states explicitly:

```text
idle → submitting → queued → running / streaming → waiting_user
→ succeeded / partially_succeeded / failed / cancelled
→ disconnected / stale → recovered state
```

Also distinguish loading, empty, permission denied, not found, and failed. Every state tells the user what is happening, what they must do, and what happens next.

### Interaction and safety

- prevent duplicate expensive submissions and pair important requests with backend idempotency;
- distinguish cancelling a browser request from cancelling a backend task;
- restore a task by task ID after refresh, disconnect, or login;
- show impact, recommendation, reversibility, and alternatives when waiting for user confirmation;
- keep result, status, and next action prominent; move raw JSON and debug data behind a detail view;
- keep model keys and private prompts off the client; backend owns authorization;
- sanitize untrusted model/user HTML and protect private file access.

### Visual and accessibility path

- Before Plan approval, use references, a flow sketch, or a non-executable wireframe to test the visual direction. During an approved frontend Build slice, build one representative page for confirmation before spreading the direction across the product.
- Use semantic design variables and a small coherent component set; do not build a universal component system prematurely.
- Verify keyboard use, labels, focus, contrast, error identification, and reduced-motion behavior relevant to the target users.
- Check at least 390, 768, 1280, and 1440 CSS-pixel widths when Web responsive behavior is in scope.
- Microphone, camera, recording, media streaming, and iOS/Safari behavior require HTTPS and real-device verification.

### Frontend evidence

Before acceptance, run the project's equivalents of lint, strict type check, tests, and production build, then perform a real-browser check against the real backend. Inspect console/network errors, loading/empty/failure/waiting/success/recovery, duplicate submission, refresh, back navigation, disconnect, media, downloads, mobile layout, and the complete user flow. A build alone is not product proof.

## Deployment routing and professional corrections

The source deployment handbook offers Volcengine veFaaS, a Serverless API gateway, TOS object storage, and related services as a convenient default for projects without infrastructure. Treat that as one deployment option, selected only after confirming target users, region, data, budget, runtime, identity, and existing platform.

Apply these corrections and stronger boundaries:

1. **Least privilege over blanket FullAccess.** Prefer a dedicated temporary identity, scoped service roles, short-lived credentials, and removal or rotation after use. If a provider forces broad access, disclose the risk and duration before the user grants it.
2. **Never request secrets in chat.** Guide the user to a secure local entry or provider secret manager. Avoid printing secret-bearing commands or environment contents.
3. **Ephemeral disk is not durable storage.** A minimum instance plus periodic backup may be acceptable only for an explicitly low-value, low-concurrency beta with a stated recovery-point window and a tested restore. Important or multi-user data needs genuinely durable storage and migrations.
4. **A reachable URL is only a routing check.** Production success also requires health, real core flow, identity isolation, persistence/recovery, file access, monitoring, cost, and rollback evidence.
5. **Invitation codes are a beta access mechanism, not universal production identity.** Evaluate secure sessions, revocation, hashing, audit, OAuth/SSO/MFA, and account recovery according to audience and risk.
6. **Monitoring can leak data.** Review captured fields, region, consent, retention, and redaction before enabling Sentry, analytics, tracing, or third-party logs.
7. **Test the target runtime.** Local and cloud runtime versions may differ; build and test in the target-compatible environment before release.
8. **Provider facts change.** Recheck current official documentation for versions, service eligibility, console paths, pricing, limits, and deployment commands at release time.

## Production readiness in product language

Before asking for release approval, explain:

- where the product will run and who can access it;
- which paid services will be created and the likely cost model;
- how users sign in and remain isolated;
- where business data and large files live;
- how much data can be lost in a failure and how restoration was tested;
- what logs or alerts exist and what sensitive content they exclude;
- what the user must do personally, one screen or account action at a time;
- how to reverse the release.

The nontechnical user should not have to understand cloud terms. When a console action is unavoidable, give a click-by-click instruction for only the current screen and invite a screenshot when the UI differs.

## Evidence matrix by stage

| Stage | Minimum evidence |
|---|---|
| Intent | User/situation/current workaround source; facts vs assumptions; validation and kill criteria |
| Specification | Explicit Must/Later/Won't acceptance; real flow and failure scenarios; data/action boundaries; concern decisions |
| Plan | Repository/environment intake; technical fit; first thin slice; alternatives; tests, real proof, cost, rollback |
| Build/Test | Deterministic results; real model/tool/backend/browser evidence; recovery and permission checks; exact unresolved gaps |
| Frontend | Lint/type/test/build; real browser/backend; console/network; responsive/state/recovery/device proof |
| Release | Secrets and package scan; identity isolation; durable data/files; backup/restore; monitoring/cost; target runtime; rollback |
| Maintain | Baseline metrics; incident/feedback evidence; human triage; regression test or eval; new intent when product changes |

Every handoff lists Passed, Failed, and Unverified separately. Never hide a failed check, delete a test, lower an accepted threshold, or relabel a mock to claim completion.
