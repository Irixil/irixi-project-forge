# Production Feedback Artifact Template

Monitoring begins read-only. It may draft this record in chat or another non-persistent response. Writing the file requires current, scope-specific authorization; neither that file write nor monitoring can authorize code or external changes.

```markdown
# Feedback or Incident: {short description}

> Status: New | Triaged | Converted | Closed
> Source of truth: This file
> Production revision and environment:

## Evidence
- Source, observed behavior, metric, affected users, and time window:

## Impact and containment
- User impact:
- Immediate action and authorization:

## Diagnosis confidence
- Facts:
- Inferences:
- Unknowns:

## Human triage
- Dismiss / monitor / bounded defect within current spec / create new intent:
- Named decision owner and rationale:
- Linked issue-ledger ID and selected route:

## Regression protection
- Test, eval, monitor, runbook, or `AGENTS.md` lesson added:
```

Only human triage promotes feedback into a change. A changed goal returns to Intent. A bounded defect still re-enters the accepted plan, implementation, verification, review, and release boundaries and needs fresh authorization before code, PR, external write, or production change.
