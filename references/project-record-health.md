# Project Record Health

Use this reference when DZ resumes a project with drift or contradictory records, after several material issue changes, when the user asks what has been done or forgotten, and before a consequential review, release, or handoff. The purpose is to keep one understandable project memory without creating another competing source of truth.

## One fact, one durable home

Keep each kind of information in its governing place and link to it elsewhere:

| Information | Canonical home |
|---|---|
| who has which problem and why the product may be worth making | current governing Intent plus optional `discovery-evidence.md` |
| what users can do, what is left out, information handling, states, and acceptance examples | current governing Specification |
| technical route, dependencies, delivery order, cost, and recovery | current governing Plan |
| current implementation work | work ledger item |
| reproducible result | evidence artifact and verification record |
| observed problem and its route | issue ledger |
| later idea | backlog or deferred issue |
| production observation | feedback record until triaged |

Do not copy the same fact into several authoritative files. Derived dashboards and handoffs summarize and link; they do not silently become the master record.

## Focused health check

Begin read-only and compare the full visible conversation, journal, current files, accepted decisions, issues, work, and evidence. Check:

1. **Duplicates:** the same decision, issue, or evidence appears more than once under different names.
2. **Conflicts:** two current-looking records promise different users, behavior, information handling, cost, or next action.
3. **Stale claims:** a former decision or result still looks current after a material change, new target, or contrary observation.
4. **Orphans:** code, a feature, a decision, evidence, or an unresolved issue has no valid link to the current product contract and work.
5. **False completion:** “done,” “fixed,” or “released” is claimed without the required current real-path evidence.
6. **Broken traceability:** an important product statement cites a missing, changed, inaccessible, or irrelevant source.
7. **Forgotten work:** unresolved, deferred, waiting-user, or later-changed issues are absent from the proposed next action or handoff.
8. **Index drift:** generated dashboards and views disagree with their source records.

Age alone does not make a record stale. A stable old decision may remain valid. A new file does not automatically outrank an accepted decision, and an accepted decision does not erase later useful work.

## Repair rules

- Regenerate a derived dashboard or index from its source when that is authorized; do not hand-edit it into a second truth.
- Merge duplicate unaccepted notes into one canonical record and preserve any distinct evidence.
- Never silently rewrite an Accepted Intent, Specification, or Plan. A material correction becomes a visible successor Draft or complete diff and waits for the appropriate owner.
- Route an orphaned implementation through the takeover keep/review decision. Preserve it until its fit is known.
- Route a material health finding through the existing issue-learning loop. Do not create a separate permanent “health issue” system.
- Keep old evidence as history. Mark why it no longer governs the current target rather than deleting it.
- If a source cannot be recovered, state exactly which claim is now uncertain and propose the smallest way to re-establish it.

## User-facing report

Do not dump the audit table on a beginner. Use at most four one-sentence bullets in one block, normally under about 220 Chinese characters, with no second list or prose appendix. Report only what changes the next decision:

1. what is still agreed and can stay;
2. what later changed or conflicts;
3. what is written as finished but nobody has actually proved on the current version;
4. the recommended repair order and why, followed by one question.

Use concrete examples and ordinary language. “The page now sends a message, but the current written agreement says the owner sends it personally” is useful. “Specification drift detected” is not.

Keep duplicate IDs, source paths, old revisions, and the full repair table in the project record. In the user reply, group them under the four questions above and name only examples that change the next choice.

## Completion standard

The records are healthy enough to proceed when each material current fact has one governing home, important links resolve, contradictions are either repaired or visible as waiting decisions, every completion claim matches current evidence, unresolved issues remain visible, and the proposed next action follows the current accepted product rather than the loudest or newest note.
