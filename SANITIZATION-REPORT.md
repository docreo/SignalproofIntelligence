# Sanitization Report

Repository: `docreo/SignalproofIntelligence`  
Candidate: `community-cli-v2-rd1-sanitized-four-model-20261002`

## Migration source

The Community CLI originated from the sanitized Public1 `community-cli/` surface. It was copied into this fresh public repository without importing private Signalproof Git history or private runtime files.

## Included

- stable `community-cli/` directory;
- `signalproof-community` launcher;
- Signalproof-authored standard-library installer;
- four local connector declarations: Granite, Qwen, Gemma, Ministral;
- local loopback-only advisory inference;
- site-matched V3/RD4 terminal presentation implemented with public-only state;
- Apache-2.0 repository license for Signalproof-authored work;
- third-party notices;
- public boundary and security documentation;
- CODEOWNERS / PR template;
- CI for tests and sanitization.

## Explicitly excluded

- model weights and model download/install logic;
- private Signalproof model routes and internal route IDs;
- private servers, VPS workers, SSH surfaces, infrastructure inventory;
- private credentials, connectors, tenant state, customer data;
- private model-training state/checkpoints;
- internal development, Build Ledger, Assurance, quarantine, or runtime evidence;
- developer workstation paths/worktrees/mounts;
- private-network topology;
- inherited authentication to private Signalproof infrastructure.

## Runtime boundary

The Community CLI connects only to exact model tags already present in the user's own local Ollama inventory. Missing models fail closed. Route changes are explicit. No silent substitution occurs.

## Visual boundary

The site/private visual language is reproduced independently: six-row gold/yellow wordmark, red rules, Signalproof Intelligence header, thin gold status box, green user prompt, and Sagittarius Horizon generation line. All private status values are replaced by public facts.

## Model distribution boundary

`weights_bundled=false` and `model_install_authority=false` are part of the runtime reporting contract. The repository contains no model binaries and no model-pull execution path.
