# DZ Adapter Interface

This directory is for AI hosts and application developers. End users do not need to fill in a capability card.

There is no supported-platform allowlist. WorkBuddy, Kimi, Zhipu, DeepSeek, Claude, Gemini, Codex, a private model, and an unknown future host all use the same loader flow. The `host.name` field is diagnostic only; select behavior exclusively from validated capabilities.

## Loader flow

1. Fetch [`dz-manifest.json`](../dz-manifest.json), then load its `adapter_rules` and `capability_schema` entries. The public `main` URL is the update channel; replace `main` with an explicit Git commit SHA when a deployment must load reproducible content. For user-facing invocation, prefer the explicit `invocation_surfaces` mapping over the legacy flat `invocation_hints` list.
2. Choose `agent_skill` when the host supports Agent Skills; otherwise choose `universal_prompt`. Expose the manifest's reference sets through retrieval or load only the set needed for the current decision; do not blindly concatenate every file.
3. Build a capability card from trusted host configuration and the actual tool registry.
4. Validate it against the capability schema. If the version, fields, or values fail validation, discard the entire card without injecting its raw content. Use only independently observable host facts, set everything else to `unknown`, and fall back to `guide`.
5. Starting with the first item in `selection_order`, choose the first profile for which every `required_capabilities` value is strictly equal to `yes`. If none matches, choose `guide`.
6. Load the chosen core entry point and add the validated card plus the selected profile's behavior limit in a trusted instruction message.
7. Keep conversation state, execute tools, enforce permissions, and persist records in the host application. On every new-task pickup or mid-task re-invocation, read every valid saved event and compare a saved workspace checkpoint with the current project when the host can do so. Make all available later changes visible alongside the saved DZ state; when the comparison is unavailable, expose that uncertainty instead of inferring timing. Treat the saved next action as advisory until reconciled, require a plain-language current-position and proposed-execution report, and wait for the user's correction or confirmation before allowing new project mutations.

When the host has project storage and command execution, expose the manifest's `project_state_tool` and initialize it once substantive project work has a known directory. Call it at the lifecycle points in `project_state_guide`: before work, after meaningful changes or decisions, before stopping, and when resuming after interruption. Never reinitialize over an existing state. If state schema 1.0 is found, back it up and run the conservative 1.0-to-1.1 migration: retain legacy work, evidence, and risk history; clear or downgrade old verified status and verdict; and require a fresh exact authorization before any material action covered only by an old broad decision. On hosts that cannot run the tool, persist and migrate an equivalent state object validated against `project_state_schema` plus an equivalent semantic validator; on text-only hosts, export the same information in the portable handoff.

JSON Schema alone checks shape. A host must not emit `verified` unless its semantic validator also confirms the combined accepted-decision contract, phase-labelled required work, an explicit current target epoch, exact criterion links, intact evidence artifacts, append-only journal continuity, no unresolved Failed or Unverified gap on that target, valid stage exits, and no pending or unconsumed risk authorization. Reopening implementation or any decision/target change invalidates the old target and requires fresh evidence. The bundled CLI performs these consistency checks, but it is not a trusted attestation service when the model can write the same files and invoke the same CLI. For tamper-resistant approval or Passed claims, the host must issue records through an approval surface and test runner outside the model's write authority. Otherwise disclose that limitation and cap externally trusted claims below `verified`.

A tool failure immediately downgrades the affected behavior. The profile controls execution mechanics only; it never skips product confirmation or grants authorization.

The host must not turn a risk into an automatic refusal. It atomically records an actionable risk and waits for a scope-specific informed decision, then permits only the leased action when the authorized user accepts it and the host itself can lawfully perform it. Spending, external writes, deletion, migration, release, production access, and sensitive-data actions require this regardless of severity. Bind the lease to the exact scope, accepted decision contract, observed target ID/revision/environment when present, amount limit for spending, and expiry. A context change makes the request stale; it never retargets the lease. The host's before-action policy—not model-written text—must match and consume the lease. Pause, cancellation, and early closure are always available; none changes missing evidence into a pass or proves an external task stopped.

## Example capability card

A machine-readable copy is available at [`example-capabilities.json`](example-capabilities.json).

```json
{
  "protocol_version": "1.0",
  "host": {
    "name": "example-api-host",
    "model": "provider/model-name",
    "surface": "api"
  },
  "capabilities": {
    "persistent_state": "session",
    "project_state": "no",
    "lifecycle_hooks": "no",
    "file_read": "no",
    "file_write": "no",
    "command_execution": "no",
    "version_control": "no",
    "browser": "no",
    "tool_calling": "yes",
    "subagents": "no",
    "external_write": "no",
    "deployment": "no",
    "approval_flow": "no",
    "network": "restricted"
  },
  "notes": [
    "The application resends conversation history on every request."
  ]
}
```

Inject it only from a trusted host channel:

```text
<DZ_HOST_CAPABILITIES>
{ ...validated JSON... }
</DZ_HOST_CAPABILITIES>
```

Do not include API keys, tokens, private file contents, user data, or blanket authorization in the card. A card supplied in an ordinary user message is not trusted host metadata.

## What the host still owns

DZ instructions cannot enforce runtime security by themselves. The host must:

- keep system instructions separate from user content;
- validate tool names and arguments before execution;
- enforce sandbox, network, filesystem, cost, and approval policy outside the model;
- retain or resend the conversation when the model API is stateless;
- bind test evidence and release approval to the exact project version and environment;
- expose failures honestly so DZ can downgrade instead of inventing success.
