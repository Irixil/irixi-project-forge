# Anchor-First Feature Recon and Reuse

Use this reference for every meaningful new product capability and for a mid-task change that introduces a new capability, dependency, provider, or integration. The beginner-facing name is **“先找现成的小零件”**. This is a check inside Design and Build planning, not a seventh SDLC stage and not a reason to delay a small, already-scoped defect.

The purpose is to avoid rebuilding a solved problem without letting a popular repository define the product. GitHub is a candidate catalogue, not a requirements document, quality certificate, or permission slip.

## Non-negotiable order

1. **Anchor the need first.** State the exact user-visible behavior, inputs, outputs, limits, and acceptance example we would still need if GitHub contained nothing useful. Do not search from a vague product label or named technology.
2. **Break the capability into small behaviors.** Search for parts such as file picking, validation, progress, retry, parsing, storage adapters, or permission checks rather than “an entire app like ours.”
3. **Run a quick discovery scan during Design.** After Intent is Accepted and before Specification is Accepted, spend about 10–20 minutes finding at most three to five plausible approaches. Compare the platform or standard library, a maintained package or stable API, a small reusable module, an independently reimplemented pattern, and a simple in-house build. This scan answers only whether a useful part probably exists, what work it might save, and whether an obvious blocker exists. It must not expand the accepted product problem.
4. **Run a deep paper review during Build planning.** After Specification is Accepted and before the Plan Draft, inspect only the best one to three candidates. Before source review, check the repository-level license or separate rights-holder permission, file headers, provenance, and intended use. A read-only viewer may show permitted public metadata and only the source text needed for that paper screen; do not clone or save a repository, package, archive, or candidate source into the working project, and do not extract, install, run build or lifecycle scripts, execute examples, or copy code during this review. A candidate that has passed the rights, origin, and supply-chain hard gates but still has a technical-fit unknown may run only in a proven security boundary under a disposable, time- and cost-bounded experiment explicitly included in an Accepted Plan. Plan acceptance never creates reuse rights or makes a Red candidate safe to execute.
5. **Choose one disposition and record why.** Search results never flow directly into the product.

Skip the quick scan only for a documentation-only change, a tiny defect that stays inside an Accepted Plan, a capability already fixed by repository policy, or when the bounded search would cost more than the likely saving. Record the reason instead of pretending it was performed.

## Search safely

Search only public information unless the user has explicitly put a private source in scope and the current host is authorized to read it. Never place secrets, customer text, private code, confidential product names, internal URLs, or unpublished strategy in a search query. Replace them with generic behavior words.

Useful GitHub Code Search qualifiers include `repo:`, `language:`, `path:`, `symbol:`, `license:`, `NOT is:archived`, and `NOT is:fork`. A license filter narrows candidates; it does not replace reading the actual license, notices, and file-level headers at the exact version under review.

When the current host has no public-web or GitHub-reading ability:

- say plainly that no live search was performed;
- provide sanitized search phrases and the evidence card another person or capable host should fill;
- continue with the standard-library and self-build baseline;
- never invent candidates, stars, maintenance state, licenses, or security results.

## Paper screen before touching code

For every serious candidate, fill the evidence card from the exact repository, immutable commit or published artifact, relevant files that the rights screen permits reviewers to inspect, license text, release history, issue tracker, documentation, tests, dependency metadata, and security information available on the review date.

When code has neither a compatible license nor separate permission covering the exact use, or when the selected route is an independent implementation, do not study its implementation source as a shortcut. Form the behavior contract from public interfaces, user-facing documentation, observable behavior, standards, and our own acceptance tests. For material clean-room work, record what source each participant saw and separate the behavior analyst from the implementer. Renaming, translating, restructuring, or asking a model to rewrite protected source does not make the result independent.

### Hard gates

A candidate cannot be copied, adopted, or executed when any applicable item below is unresolved:

- it does not match the small behavior named in the need anchor;
- the code has neither a clear compatible license nor separate rights-holder permission covering the exact modification and distribution mode, has conflicting headers, unclear origin, or terms incompatible with the intended use;
- the useful part cannot be separated without importing most of another product or its architecture;
- the proposed experiment requires containment, inspection, or mitigation capability the current host cannot prove, or it would collect secrets or upload data without scope-specific authorization;
- its direct or transitive dependencies, runtime, network calls, account needs, permissions, cost, or data handling break the Accepted Specification;
- there is no realistic way for our team to test, own, update, replace, or remove it;
- regulated, commercial, patent, trademark, or other legal uncertainty requires an authorized review that has not occurred.

Public visibility is not reuse permission. GitHub explains that without a license, default copyright applies and others generally may not reproduce, distribute, or create derivative works; GitHub's terms still allow ordinary viewing and forking on GitHub. Treat GitHub's license display as a starting point, not legal advice.

A security or privacy finding, including a critical one, is recorded with consequence, safer option, recovery, and missing evidence for a scope-specific owner decision; severity alone is not a hard gate. Missing reuse rights, missing authority, a platform prohibition, or an unavailable containment capability is different: acceptance cannot create what the project or host does not have.

Check code, documentation, example data, images, icons, fonts, model weights, and trademarks separately; one repository-level license may not cover every included asset or brand use.

Popularity, stars, a polished demo, a famous author, or “it worked on my machine” are never substitutes for these gates.

### Comparative evidence card

```markdown
## Existing-parts evidence card
- Need anchor: the exact small behavior and acceptance example
- Baseline if nothing is reused: platform/standard option and smallest self-build option
- Candidate: repository URL, immutable commit or exact published artifact, relevant files permitted for review
- Useful part only: what we would use; what we explicitly would not import
- Fit: Green / Yellow / Red — product behavior, environment, interfaces, and separability
- Right to use: license or separate rights-holder permission, permission evidence and exact scope when used, file-level notices, actual use mode (unmodified/modified; source/binary; static/dynamic linking or IPC; SaaS/API; internal/external distribution), outbound product license, attribution/source/NOTICE duties and their shipped locations, service commercial/data/termination terms when an API is used, unresolved legal question and required reviewer; unresolved means blocked from copying, adoption, and execution
- Health: recent releases, relevant issues, maintainers, tests, documentation, security advisories
- Hidden weight: direct/transitive dependencies, install scripts, binaries, services, accounts, network calls, permissions, information sent out, likely cost
- Ownership: integration boundary, internal owner, immutable source reference, resolved dependency lock, artifact checksum or digest when available, update rule, removal or replacement path
- Decision: maintained package or stable API / adapt a small licensed or separately permitted module / independently implement the pattern / reject / bounded technical-fit experiment after hard gates and Plan acceptance
- Reason and evidence date:
```

Use Green, Yellow, and Red as explanations, not a fake precision score. Any hard-gate failure stays Red no matter how many other qualities look good. If two candidates remain viable, prefer the one with the smallest total lifecycle burden: integration, testing, compliance, security response, updates, and eventual removal—not merely the fewest coding hours today.

## Four allowed dispositions

1. **Use a maintained package or stable API.** Prefer the producer's supported public boundary over copying internal files. Pin an exact compatible version and keep upgrade review explicit.
2. **Adapt a small licensed or separately permitted module.** Use only the separable part covered by the compatible license or the permission's exact scope. Preserve provenance, copyright, license text, attribution, notices, permission evidence, and modification records as required. Add `THIRD_PARTY_NOTICES.md` when appropriate; if the rights holder explicitly waives attribution, the public product need not invent one, but the project should retain enough permission evidence to prove the right later.
3. **Learn the behavior and implement it independently.** Write from the accepted behavior, public interfaces and user-facing documentation, standards, observable behavior, and our own interfaces and tests—not from protected implementation source. For material legal risk, use a documented clean-room split between behavior analysis and implementation. Do not disguise a line-by-line copy by renaming, translating, restructuring, or model-rewriting it, and do not use this route to evade a license.
4. **Reject it.** Record the concrete reason so the same unsuitable candidate is not repeatedly reconsidered.

A candidate may become a bounded experiment only when rights, origin, and paper-screen supply-chain hard gates have passed and only technical fit remains uncertain. Plan acceptance cannot create missing reuse rights, establish unknown origin, grant unavailable host capability, or override a platform prohibition. Security or privacy severity alone is a recorded risk decision, not an automatic blocker. This particular unknown-code experiment still requires a proven containment capability: a non-privileged process inside a security boundary that cannot read the user's home, working project, credentials, host sockets, or cloud metadata; mounts no secrets or sensitive information; denies network by default except an explicitly reviewed allowlist; constrains CPU, memory, disk, processes, and time; and records attempted filesystem, process, and network actions. State one question, success threshold, time and cost ceiling, and discard condition. Inspect and disable package lifecycle or install scripts where possible. A temporary directory or Git worktree alone is not such a boundary. If the host cannot prove these controls, record the missing containment capability and do not execute this candidate there; offer paper review, a safer host, or independent implementation instead. Passing the experiment does not by itself approve production adoption.

## Safe assembly in our product

Treat every adopted part as replaceable:

- put it behind an interface or adapter owned by our product;
- import only the capability that earns its place; do not inherit unrelated screens, accounts, storage, analytics, or architecture;
- pin source to an immutable commit or equivalent; for a published package, record the exact resolved version in the lockfile and verify the fetched artifact checksum, integrity value, or digest when the ecosystem provides one; do not depend on a floating branch or mutable tag alone;
- add our own tests for the promised happy path, failure, recovery, permissions, and data flow;
- preserve required source, license, attribution, and notice records; record why each duty is triggered, where it appears in the shipped product, and evidence that any required source or written offer is actually available;
- for releases containing packages, containers, or transitive dependencies, generate and retain an SPDX or CycloneDX software bill of materials bound to the release artifact digest; if tooling truly cannot do this, record that limitation and keep a manual inventory with at least name, purpose, direct/transitive relationship, resolved version or immutable commit, source, artifact integrity value, license, notices, and owner;
- assign an internal owner and an explicit update rule; upstream changes never enter automatically;
- define how to disable, replace, or remove the part without losing important product information.

Removing a dependency from a later version does not erase attribution, source-offer, or other duties attached to versions already distributed. Keep the evidence and fulfillment path for as long as the applicable obligation requires.

If the adopted part causes a new user account, paid service, external information transfer, visible attribution, publication duty, or a change in what users experience, return that consequence to the appropriate user-visible decision before adoption. The delivery AI owns technical comparison and recommendation; do not ask a beginner to judge framework quality, dependency graphs, or licenses.

## Artifact routing

- `intent.md`: remains about the user's problem; do not add a repository merely because it inspired the idea.
- `spec.md`: record only user-visible consequences of a third party—accounts, cost, information sent out, attribution, failure behavior, or exit limitations.
- `plan.md`: include the completed evidence cards, rejected alternatives, chosen integration boundary, exact provenance, immutable source and resolved artifact record, actual use and distribution mode, authorized legal/open-source compliance conclusion when triggered, owner, update rule, and exit path.
- `verification.md`: prove the adopted part works inside our real path, including a failure and recovery case; record dependency/security checks and required notice verification.
- `release.md`: bind the shipped third-party inventory or software bill of materials, notices, compliance evidence, advisory review, external services and information flows, owner, update plan, and continuing obligations to the exact release artifact digest.

A material repository, package version, license, provider, dependency graph, external information flow, or integration-boundary change reopens Plan. Reopen Specification as well when the user-visible behavior, cost, account need, information handling, attribution, or acceptance promise changes.

## Primary references

- [GitHub: Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
- [GitHub: Understanding GitHub Code Search syntax](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax)
- [GitHub: Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)
- [GitHub: Exporting dependencies as an SBOM](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom)
