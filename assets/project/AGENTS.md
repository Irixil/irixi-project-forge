# DZ Project Continuity

DZ workflow guidance version: `2026-09-06.2`.

This is a DZ product project. Load the installed `dz` Skill before product work; if it is unavailable, say so instead of silently inventing a substitute.

At the start of a new task, or whenever DZ is invoked again after other work continued:

1. Begin read-only. Read `PROJECT.md` and run the current DZ state tool's `resume-report`.
2. Trust neither old chat nor the saved `next_action` by itself. The report checks the full journal, the generated current view, and the saved Git checkpoint mechanically. Use its compact present summary first. Read full history or affected files only when it reports a mismatch, unexplained change, unresolved contradiction, stale view, or material uncertainty.
3. Reconcile that with the visible conversation and any current running or external state. In plain language, report what exists now, what changed later, what remains uncertain, and the recommended next actions with reasons and meaningful choices.
4. Let the user correct that account and discuss the route before new project changes. This alignment does not accept unseen product wording or authorize a new external action.

The user's current explicit instruction takes priority over DZ workflow preferences within the allowed and authorized scope. If DZ itself forces a pause or route change, name the exact rule and concrete reason. Do safe, already-authorized, reversible preparation before asking. Do not request the same permission twice when the current message clearly specifies the action, target, and scope.

The latest explicitly accepted product wording is current; later brainstorming is not. When an accepted decision changes, keep the old version in history but remove it from the active view, supersede only affected downstream work, and preserve compatible implementation. Record meaningful decisions, changes, checks, failures, material issues, risk decisions, pauses, cancellations, and handoffs in the ledger during the same turn.

Independent read-only checks or isolated work may run in parallel. Serialize changes to the same files, decision, ledger state, production target, or external action. During implementation, test affected behavior and critical shared paths; run the full required acceptance set for a release candidate, material shared-contract change, or unbounded impact.

Before deploying to an internal test environment or preparing a public release, run a default AI preflight: check the current Must and core user paths end to end, then review changed code and critical shared paths. Run safe in-scope local checks without asking again. Report passed, failed, and unverified items separately. This prepares internal human testing and never replaces it or independent review.

Risk severity alone is not a refusal. Explain the consequence and safer route, then let an authorized user decide. Secrets, sensitive information, payment, external writes/messages, deletion, migration, public release, and production access still require current action-specific authorization. Stopping never becomes proof: only current Passed evidence can mark required work verified, and the user may pause, cancel, or close with an honest handoff at any time.

Merge this section with existing repository instructions instead of replacing them.
