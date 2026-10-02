# Community CLI Security Boundary

Signalproof Intelligence Community CLI is a sanitized public connector surface.

## Runtime boundary

- HTTP transport is limited to loopback hosts.
- Four exact model tags may be selected explicitly.
- No model weights are bundled, mirrored, downloaded, or installed.
- The CLI contains no package-manager or model-pull execution path.
- Missing local models fail closed; route selection remains unchanged.
- No silent model fallback is implemented.
- The model receives no filesystem, browser, credential, shell, tool, remote-server, or model-install authority.
- No public VPS/SSH/private-worker routes exist.
- No inherited authentication or private Signalproof credentials exist.

## Public/private separation

Public source must not contain private Signalproof route IDs, internal endpoint addresses, tenant/customer configuration, credentials, private model-training state, Build Ledger evidence, developer workstation paths, quarantine/evidence paths, or private infrastructure topology.

The site/private CLI visual style is reimplemented with public-only values. Presentation parity does not grant private capabilities.

## Remote access

Any future hosted or remote capability requires a separately designed authenticated connector with explicit login, scoped grants, revocation, public security review, and fail-closed unauthenticated behavior. This release has no such remote capability.
