# Review and Release Artifact Templates

## review.md

Use an independent verifier for standard, public, sensitive, agentic, costly, or larger work.

```markdown
# Review: {iteration}

> Status: In review | Changes required | Passed | Superseded
> Source of truth: This file
> Reviewed revision:
> Reviewer context: independent verifier / code review / authorized policy owner

## Review basis
- intent.md:
- spec.md:
- plan.md:
- verification.md:
- Policies or repository rules:
- Existing-parts evidence, provenance, licenses, notices, and dependency/security review:
- Authorized legal/open-source compliance owner, exact version/use/distribution scope, conclusion, and evidence when triggered:

## Findings
| Severity | Area | Finding | Evidence | Required resolution | Status |
|---|---|---|---|---|---|

## Resolution and re-verification
- Finding — change — evidence — reviewer disposition:

## Verdict
- Behavior matches accepted intent and spec: yes / no
- No unresolved critical finding: yes / no
- Ready to prepare release: yes / no
```

The implementer may fix findings but cannot rewrite the independent verdict as their own.

## release.md

Prepare this before requesting production approval. Approval authorizes deployment to one named environment; it is not release completion.

```markdown
# Release: {version or iteration}

> Status: Draft | Approved | Deploying | Released | Rolled back | Superseded
> Source of truth: This file
> Target environment and audience:
> Reviewed revision:
> Release artifact digest and resolved lockfile digest:

## Release scope and evidence
- User-visible changes:
- Verification and review links:
- Known limitations and accepted risks:
- Accepted-risk record: concrete consequence, safer option, recovery, decision owner, exact action/revision/environment/amount/time, and decision evidence:

## Production readiness
- Identity and access isolation:
- Secrets and credential lifetime:
- Migrations, persistence, backup, recovery objective, and restore evidence:
- File storage and ownership:
- Logging, trace IDs, alerts, privacy, and cost controls:
- Dependencies, service limits, and target-runtime compatibility:
- Shipped SPDX/CycloneDX SBOM bound to the release digest, or minimum manual inventory and tooling limitation; immutable source/resolved package pins; fetched artifact integrity; repository-to-package mapping:
- Actual use/distribution mode, source/attribution/NOTICE/source-offer duties, their shipped locations and evidence, continuing duties for earlier distributed versions:
- Current advisories, external services and information flows, internal owner, update rule, and removal path:

## Deployment and rollback
- Deployment procedure:
- Health check and real core-flow smoke test:
- Rollback command or runbook:
- Rollback rehearsal evidence:
- Responsible human:

## Production approval
- Required approver role:
- Named authorized approver confirmed: yes / no
- Approval scope and environment:
- Approval record:
- Legal/open-source compliance owner, exact shipped parts/use/distribution scope, conclusion, and evidence when triggered; unresolved rights block release:

## Deployment record
- Start/end time and operator:
- Deployed revision:
- Result and deviations:

## Post-release evidence
- URL or access route:
- Identity-isolation check:
- Real core flow:
- Persistence or recovery check:
- Monitoring and alert check:
- Required notices and source/source-offer access check:
- Rollback readiness:
- Final result and follow-up:
```

After informed approval, set Deploying and perform the deployment, even when the named owner knowingly accepted a high or critical residual risk they are entitled to decide; severity alone is not a blocker, and do not repeatedly reopen the same decision unless its scope changes. Set Released only after recording the applicable post-release checks. A reachable URL proves routing only, so failed or skipped checks stay visible and the release must not be described as fully verified. If release fails, use the available rollback or recovery path, record evidence, set Rolled back when rollback actually succeeds, and return to Test. Missing or conflicting reuse rights, source provenance, or required legal/open-source compliance authority are blockers, never entries under “accepted risks.”
