# DZ Project Continuity

This repository is a DZ project. Before product, application, or agent work, load the installed `dz` Skill. In Codex, if the selector did not attach it, read `$HOME/.agents/skills/dz/SKILL.md` directly. On another host, use its installed DZ entry or persistent project instruction. If DZ cannot be loaded, say so instead of silently using an ordinary workflow.

At the start of every new task or session, read `PROJECT.md` and `.dz/state.json`, validate the ledger, inspect the latest valid `.dz/journal.jsonl` record, and reconcile them with the current files before changing anything. Begin with a short plain-language summary of what was last completed, what is waiting, and the next safe action. Do not restart discovery or rely on chat memory when the saved record already answers the question.

Treat accepted files under `docs/sdlc/` as the product decisions and `.dz/state.json` as the current execution snapshot.

- Run the DZ state check before acting and recover from `.dz/journal.jsonl` if the snapshot is damaged.
- Keep one work item in progress at a time. Record meaningful changes, checks, user decisions, failures, risks, pauses, and cancellations in the same turn.
- Bind work to the combined digest of the exact accepted Intent, Specification, and Plan. Bind evidence to that contract plus an explicit observed target epoch, exact acceptance statement, tested revision, environment, method, and hashed non-empty evidence file. Changing a decision or entering implementation clears the old target and downgrades old verified work. Every target reset requires fresh checks even when its revision text is unchanged. A rerun may resolve only a Failed or Unverified gap for that same statement and target. Never remove, change, or reorder history to obtain a pass, and recover when the snapshot differs from the journal.
- Keep decision order intact. A changed Intent supersedes Specification and Plan; a changed Specification supersedes Plan. Re-accepting an upstream decision does not revive downstream approval.
- Material actions wait for an informed, scope-specific user decision regardless of severity. If the authorized user accepts, bind one action lease to the accepted decisions, exact target/revision/environment, spending ceiling when applicable, and explicit expiry. Completion, failure, cancellation, expiry, or any bound fact change prevents further use; the host must enforce those limits outside the model.
- Once risk authorization is requested, pause or closure must not erase the pending decision or unconsumed lease.
- Use blocked only for a missing capability, authority, external condition, host permission, or third-party right. Risk severity is not a blocker type.
- The user may pause, cancel, or close at any time. Never translate that choice into verified completion or claim that an outside job stopped without a real status result. After cancellation, allow only a bounded signal and one status confirmation for work already running, plus the minimum ledger and handoff updates.
- Only passed evidence can move required work to verified.
- Before stopping, ensure the run is waiting for the user or authorization, blocked with a recovery condition, paused, or truthfully finished.
- A finished run accepts no ordinary project mutation until it is explicitly resumed; recording an outstanding outside-action outcome must not reopen or upgrade its verdict.

Merge this section with existing repository instructions instead of replacing them.
