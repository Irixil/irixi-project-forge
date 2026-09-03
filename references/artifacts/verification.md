# Verification Artifact Template

Update throughout Build and finalize in Test. This is evidence, not a human-acceptance artifact.

```markdown
# Verification: {iteration}

> Status: In progress | Passed | Blocked | Superseded
> Source of truth: This file
> Based on: Accepted spec and plan
> Accepted decision-contract digest, target epoch, implementation revision, built artifact digest, resolved lockfile digest, and environment:

## Environment
- Runtime, model, browser/device, backend, data set, and relevant configuration versions:

## Acceptance evidence
| Criterion | Method | Exact input/action | Expected | Observed | Evidence | Verdict |
|---|---|---|---|---|---|---|

## Verification layers
- Mock and deterministic tests:
- Real model, tool, or integration smoke:
- Browser and device checks:
- Failure, recovery, permissions, persistence, cost, and rollback checks:
- Adopted parts: immutable source or exact resolved package; repository-to-published-artifact mapping; fetched artifact integrity/digest; provenance:
- Compliance: actual use/distribution mode; license and service terms; named owner evidence when triggered; required notices/source offers and their shipped locations:
- Supply chain: direct/transitive dependency and advisory check; SPDX/CycloneDX SBOM bound to the tested artifact digest, or minimum manual inventory plus tooling limitation:
- Runtime: observed filesystem/process/network/information flow; sandbox and destroy evidence for any experiment; our happy/failure/recovery tests; disable or replacement evidence:

## Findings and corrections
- Finding — severity — fix — recheck evidence:

## Recorded-issue regression evidence
| Issue ID | Former failure reproduced | Repair | Current-target recheck | Repeatable prevention | Verdict |
|---|---|---|---|---|---|

## Unverified and limitations
- Item — reason — impact — next action:

## User-requested pause or closure
- Continue / pause / cancel / close with unverified work:
- User-visible reason and decision reference:
- Product verdict preserved as verified / partially verified / implemented but unverified / cancelled:
- Smallest future check and resume condition:

## Final verdict
- Must items passed:
- Critical findings open:
- Ready for independent review: yes / no
```

Never replace exact outputs or inspectable evidence with “the AI checked it.” Label mocks, simulations, and real systems distinctly. Bind every Passed row to its exact accepted-decision contract, criterion, explicit target epoch, non-empty durable evidence artifact and digest, tested revision, environment, and method. All Must rows pass on that target with no unresolved Failed or Unverified gap. A same-target pass may resolve such a same-target gap; a new target epoch reruns every Must row even when revision text is unchanged. Mark Passed only when every Must item has evidence and no critical finding remains. An authorized owner may still knowingly continue or release an exact accepted residual-risk scope, but that finding stays visible and the artifact remains below Passed. The user may stop before Passed; preserve the honest status and provide a handoff instead of refusing to end. Local model-written ledger fields are consistency records, not trusted attestations unless a host-controlled runner issued them. Risk acceptance never changes a Failed or Unverified result.
