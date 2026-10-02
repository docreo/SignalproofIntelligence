# Contributing

Signalproof Intelligence is public-first.

Never submit credentials, customer data, private infrastructure, private route IDs, internal evidence, private model-training state, or developer-machine paths.

## Community CLI contract

The `community-cli/` directory and `signalproof-community` command are stable public surfaces.

Changes must preserve:

- local loopback-only model connections;
- explicit route selection;
- no silent fallback;
- no model download/install authority;
- no bundled model weights;
- public-only terminal status fields;
- sanitization and test gates.

Use a branch and pull request. Add or update tests for changed behavior. Do not weaken security, sanitization, license, or provenance controls merely to obtain PASS.
