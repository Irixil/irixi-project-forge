# Verification Artifact Template

Update throughout Build and finalize in Test. This is evidence, not a human-acceptance artifact.

```markdown
# Verification: {iteration}

> Status: In progress | Passed | Blocked | Superseded
> Source of truth: This file
> Based on: Accepted spec and plan
> Implementation revision, built artifact digest, resolved lockfile digest, and environment:

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

## Unverified and limitations
- Item — reason — impact — next action:

## Final verdict
- Must items passed:
- Critical findings open:
- Ready for independent review: yes / no
```

Never replace exact outputs or inspectable evidence with “the AI checked it.” Label mocks, simulations, and real systems distinctly. Mark Passed only when every Must item has evidence and no critical finding remains.
