# Public Distribution Boundary

Signalproof Intelligence is a sanitized public distribution surface.

## Never publish here

- private Signalproof server/VPS/worker routes or private route IDs;
- SSH identities, keys, tokens, credentials, connector secrets, or tenant secrets;
- customer/tenant data or configuration;
- internal Build Ledger, Assurance, quarantine, or operator evidence;
- private model-training checkpoints, hashes, state, or training authority;
- developer workstation paths, worktrees, home paths, mounts, or local evidence paths;
- private-network addresses or internal topology;
- implicit or pre-authorized access to private Signalproof infrastructure.

## Community CLI connection rule

The public Community CLI may connect only to a user-managed local Ollama service over HTTP loopback.

The repository declares four exact connector targets. It does **not** bundle, host, mirror, download, install, or redistribute model weights. Missing models remain missing until the user independently installs them under the applicable upstream terms.

Public code has no inherited access to private Signalproof infrastructure.

## Visual parity rule

Public presentation may reproduce the approved Signalproof terminal visual language, but every displayed field must be public-safe. Private Orchestrator routes, Signal Keys, private identities, internal ports, private evidence, and developer paths must not be copied merely to achieve visual parity.

## Future remote access

Any future remote connection must be a separately reviewed authenticated surface with explicit login, narrowly scoped authorization, revocation/disconnect behavior, no inherited private credentials, and fail-closed unauthenticated tests.

## Enforcement

`tools/check_public_sanitization.py` and repository CI block common public-boundary violations. CODEOWNERS requests owner review. Repository-level GitHub branch/ruleset enforcement is an administrative setting and is tracked separately in `REPOSITORY-PROTECTION.md`.
