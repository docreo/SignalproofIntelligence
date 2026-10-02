# Community CLI Migration Provenance

## Destination

`docreo/SignalproofIntelligence`

Stable public path: `community-cli/`

## Public source

The migration began from the sanitized Public1 repository:

`docreo/docreo-Signalproof-Public1`

Public1 main tree observed for migration: `9a3e19cb173b99ca79d99dd5c196b5abfa50f938`.

The destination repository was created independently and does not import the Public1 Git history.

## Migration changes

The destination Community CLI intentionally diverges from Public1 by:

- retaining the `signalproof-community` launcher and `community-cli/` directory;
- increasing public local connector declarations from two to four;
- removing Public1 model-download behavior entirely;
- making `setup` a read-only readiness/connector check;
- reimplementing the approved site terminal visual with public-only status values;
- adding repository-level public boundary, security, contribution, attribution, sanitization and CI controls.

## Excluded provenance

No private Signalproof Git history, credentials, runtime configuration, server inventories, internal route IDs, Build Ledger evidence, model-training state, workstation paths, or model weights were migrated.

## Release truth

This file records source/migration provenance only. A candidate branch or passing CI does not by itself constitute a public release or production promotion.
