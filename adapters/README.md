# DZ Adapter Interface

This directory is for AI hosts and application developers. End users do not need to fill in a capability card.

## Loader flow

1. Fetch [`dz-manifest.json`](../dz-manifest.json), then load its `adapter_rules` and `capability_schema` entries.
2. Choose `agent_skill` when the host supports Agent Skills; otherwise choose `universal_prompt`. Expose the manifest's reference sets through retrieval or load only the set needed for the current decision; do not blindly concatenate every file.
3. Build a capability card from trusted host configuration and the actual tool registry.
4. Validate it against the capability schema. If the version, fields, or values fail validation, discard the entire card without injecting its raw content. Use only independently observable host facts, set everything else to `unknown`, and fall back to `guide`.
5. Starting with the first item in `selection_order`, choose the first profile for which every `required_capabilities` value is strictly equal to `yes`. If none matches, choose `guide`.
6. Load the chosen core entry point and add the validated card plus the selected profile's behavior limit in a trusted instruction message.
7. Keep conversation state, execute tools, enforce permissions, and persist records in the host application.

A tool failure immediately downgrades the affected behavior. The profile controls execution mechanics only; it never skips product confirmation or grants authorization.

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
