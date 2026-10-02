# Signalproof Intelligence Community CLI

Sanitized, local-only public connector edition of the Signalproof CLI.

The directory and launcher remain stable:

- repository path: `community-cli/`
- command: `signalproof-community`
- current community release: `0.3.0`
- current community build identity: `V2/RD1`
- visual language: `V3/RD4`
- generation family: `Sagittarius Horizon`

## What this public CLI does

It connects to supported models that **the user already has installed** in their own local Ollama runtime. It does not ship, download, install, mirror, host, or redistribute model weights.

| Alias | Exact local Ollama tag | Upstream family |
| --- | --- | --- |
| `granite` | `granite4.2:8b` | IBM Granite |
| `qwen` | `qwen3.6:latest` | Qwen / Alibaba |
| `gemma` | `gemma4:latest` | Google Gemma |
| `ministral` | `ministral-3:3b` | Mistral AI Ministral |

These are connector declarations, not bundled dependencies and not claims that Signalproof created or retrained the upstream weights.

## Requirements

- Python 3.11+
- a user-managed local Ollama service on loopback
- any supported model the user independently chooses to install under its upstream terms

## Install the CLI

```text
python install.py
```

The source installer installs only the Signalproof-authored Community CLI and launcher. It installs no model runtime and no model weights.

## Read-only readiness check

```text
signalproof-community setup
signalproof-community status
signalproof-community models
```

`setup` is retained for Public1 compatibility but is now read-only. It reports which exact connectors are available locally and never performs a model download.

## Chat

```text
signalproof-community chat granite
signalproof-community chat qwen
signalproof-community chat gemma
signalproof-community chat ministral
```

Inside chat:

```text
/help
/status
/routes
/model granite
/model qwen
/model gemma
/model ministral
/exit
```

A model change is explicit. If the requested exact model is missing locally, the route remains unchanged. There is no silent fallback.

## Visual contract

The public CLI mirrors the approved site/private CLI visual language without importing private runtime state:

- six-row gold/yellow Signalproof wordmark;
- red separator rules;
- Signalproof Intelligence / Human-Controlled AI Systems heading;
- `SP://COMMUNITY` public plane;
- thin gold status outline with the title embedded in the top border;
- green `YOU [model] >` prompt;
- Sagittarius Horizon generation line below the prompt.

The status panel contains only public facts: local user, loopback transport, public alias, upstream model identity, exact connector tag, and locally observed readiness. It does **not** expose private Orchestrator routes, Signal Keys, server identities, internal ports, private evidence, or workstation paths.

## Authority boundary

The Community CLI is advisory-only:

- loopback HTTP transport only;
- four explicit local connectors;
- no model download/install authority;
- no model weights bundled;
- no tool/file/browser/credential authority;
- no private Signalproof infrastructure access;
- no remote worker/VPS routes;
- no silent fallback;
- exact local digest surfaced before inference.

See [SECURITY.md](SECURITY.md), [MODELS.md](MODELS.md), and the repository [PUBLIC-BOUNDARY.md](../PUBLIC-BOUNDARY.md).
