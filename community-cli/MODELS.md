# Public Model Connector Registry

Signalproof Intelligence Community CLI 0.3.0 declares four local connector targets. **No model weights are distributed by this repository.**

| Alias | Exact local tag | Upstream | Signalproof role |
| --- | --- | --- | --- |
| `granite` | `granite4.2:8b` | IBM | connector only |
| `qwen` | `qwen3.6:latest` | Qwen / Alibaba | connector only |
| `gemma` | `gemma4:latest` | Google | connector only |
| `ministral` | `ministral-3:3b` | Mistral AI | connector only |

For every connector:

- transport: user-owned local Ollama loopback;
- mode: `NON_EXECUTING_ADVISORY`;
- direct model authority: `false`;
- model install authority: `false`;
- bundled weights: `false`;
- silent model fallback: prohibited.

The user is responsible for obtaining and operating any selected model/runtime under the applicable upstream license and terms. Signalproof does not relicense upstream model weights.

Sagittarius Horizon names the current Signalproof generation. The proprietary Sagittarius Horizon model is **not** distributed by this public Community CLI and is not represented as one of these four upstream connector targets.
