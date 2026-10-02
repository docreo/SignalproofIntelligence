# Security Policy

## Public security boundary

This repository is a sanitized public surface. The Community CLI is local-only and advisory-only.

Security invariants:

- no credentials/private keys in source;
- no customer or tenant data;
- no private Signalproof infrastructure or private route IDs;
- no private training state or internal evidence;
- no developer workstation paths;
- loopback-only Community CLI model transport;
- no hidden model downloads or model-weight redistribution;
- no silent model fallback;
- no tool/file/browser/credential/model-install authority;
- exact-route failure closed when the selected local model is unavailable.

## Vulnerability reports

Use GitHub private security reporting when available. Do not publish secrets, exploit details, credentials, customer data, or private infrastructure in public issues.

CI is a prevention layer, not a substitute for human review.
