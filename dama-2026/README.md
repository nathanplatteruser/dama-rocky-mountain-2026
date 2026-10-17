# The Four Gateways: security and data privacy for AI agents

Hands-on labs for **DAMA Rocky Mountain, October 22, 2026**. Presented by Nathan Platter, Lincoln NE.

**All data is SYNTHETIC SAMPLE DATA.** Every name, number, and ID is invented. Mock mode and the local Ollama mode need no internet connection and no API key, and nothing leaves your laptop. The optional cloud model mode (below) sends the redacted synthetic data to the provider you choose.

- Setup guide: [Word](../docs/Four-Gateways-Setup-Guide.docx) | [PDF](../docs/Four-Gateways-Setup-Guide.pdf)
- Clickable demo with the overlay on: [Flight Recorder, four gateways view](https://nathanplatteruser.github.io/dama-rocky-mountain-2026/flight-recorder/) (or open `../flight-recorder/index.html`)

## The four gateways

| Gateway | Control | Code | Agent rule | Demo step |
|---|---|---|---|---|
| G1. Use | Classify every field; redact sensitive fields; sensitive data goes only to a local model | [`gateways/g1_classify_redact.py`](gateways/g1_classify_redact.py) | [AGENTS.md G1](agents/AGENTS.md#g1-use-classify-before-you-touch), `guardrails.yaml > G1_use` | Step 2 (raw vs redacted toggle), Step 7 |
| G2. Prompt | Locked instructions, prompt-injection defense, tool allow-list enforced in code | [`gateways/g2_prompt_guard.py`](gateways/g2_prompt_guard.py) | [AGENTS.md G2](agents/AGENTS.md#g2-prompt-your-instructions-are-locked), `guardrails.yaml > G2_prompt` | Step 1 (permission card), Step 5 (blocked $4,800) |
| G3. Context | Permissioned retrieval, minimum data, a source trace on every sentence | [`gateways/g3_context_scope.py`](gateways/g3_context_scope.py) | [AGENTS.md G3](agents/AGENTS.md#g3-context-least-data-always-traced), `guardrails.yaml > G3_context` | Step 2 (source tags), Step 4 (current forms only) |
| G4. Self-check and exit | Fail closed, ask a named human one specific question, log every decision | [`gateways/g4_selfcheck_exit.py`](gateways/g4_selfcheck_exit.py) | [AGENTS.md G4](agents/AGENTS.md#g4-self-check-and-exit-fail-closed), `guardrails.yaml > G4_selfcheck_exit` | Step 3 (fail-closed record), Steps 5 and 6, Closer (audit log) |

The prompt asks; the code enforces. Every rule in `agents/AGENTS.md` has a matching check in `gateways/`, and `test_gateways.py` fails if `guardrails.yaml` and the code drift apart.

## Run it

Needs Python 3.10 or newer. No packages to install.

```bash
cd dama-2026
python3 run_all.py              # mock mode, no model needed (Windows: py run_all.py)
python3 -m unittest -v test_gateways
```

With a local model through [Ollama](https://ollama.com):

```bash
ollama pull llama3.1:8b
FR_BACKEND=ollama FR_MODEL=llama3.1:8b python3 run_all.py
```

Windows PowerShell: `$env:FR_BACKEND="ollama"; $env:FR_MODEL="deepseek-r1:7b"; py run_all.py`

Test the Ollama path with no download: `python3 tests/test_ollama.py` (from the repo root) runs every lab against a bundled stand-in for the Ollama API, as `llama3.1:8b` and `deepseek-r1:7b`, with a misbehaving model that obeys the injection and invents numbers. Add `--real llama3.1:8b` to include your real Ollama. Or `make test-ollama`.

Each lab also runs alone, for example `python3 gateways/g4_selfcheck_exit.py`. Every decision is appended to `out/flight-recorder.jsonl`, the audit log.

The Ollama mode refuses to call any Ollama host other than localhost. The guardrails still decide the outcome when a real model answers differently from the mock, and that is the point: the model can be swapped, the gates stay.

## Cloud model option (optional, paid)

Same labs, same prompts, same four gateways, same audit log. Only the model changes. Use it if you would rather run Claude, Grok, or ChatGPT than install a local model. You bring your own API key.

| Backend | Provider | Key (environment variable) | Default model | Cost |
|---|---|---|---|---|
| `mock` (default) | none, scripted | none | scripted | Free |
| `ollama` | your laptop | none | `llama3.1:8b` | Free |
| `anthropic` | Anthropic Claude | `ANTHROPIC_API_KEY` | `claude-opus-5-5` | Paid, per token |
| `xai` | xAI Grok | `XAI_API_KEY` | `grok-4.7` | Paid, per token |
| `openai` | OpenAI (ChatGPT models) | `OPENAI_API_KEY` | `gpt-6.1-sol` | Paid, per token |
| `compatible` | any OpenAI-compatible server (OpenRouter, Azure, LM Studio, vLLM) | `FR_API_KEY` (optional for local servers) | set `FR_MODEL`; also set `FR_BASE_URL` | Depends on the server |

```bash
cd dama-2026
export ANTHROPIC_API_KEY=...            # paste your own key; the labs never save it
FR_BACKEND=anthropic python3 run_all.py # Claude Opus by default
FR_BACKEND=anthropic FR_MODEL=claude-sonnet-5-5 python3 run_all.py   # pick any model your account has
FR_BACKEND=xai python3 run_all.py       # needs XAI_API_KEY
FR_BACKEND=openai python3 run_all.py    # needs OPENAI_API_KEY; try FR_MODEL=gpt-6-astra for the flagship
FR_BACKEND=compatible FR_BASE_URL=https://openrouter.ai/api/v1 FR_MODEL=<model> FR_API_KEY=... python3 run_all.py
```

Windows PowerShell: `$env:ANTHROPIC_API_KEY="..."; $env:FR_BACKEND="anthropic"; py run_all.py`. Switch back to the free local model with `FR_BACKEND=ollama`, or to mock mode by removing `FR_BACKEND`.

What stays the same, so you can compare side by side: the system prompts, the redaction, the injection check, the tool gate, the source trace, the fail-closed reconcile, and the four PASS checks. Every audit log line now carries `backend` and `model`, so a local log and a cloud log line up event for event. A cloud run adds one `G1 CLOUD EGRESS CHECKED` line before each model call.

What changes, and why it is a Gateway 1 decision: a cloud run sends data to the provider. Here that data is SYNTHETIC and already redacted. Before every call, `gateways/cloud.py` scans the outgoing text and refuses to send if any raw sensitive value (SSN, phone, email, name, date of birth, address, health note) is present. On the OpenAI and xAI Responses API it also sets `store: false`. In your own systems, check your provider agreement (retention, training use, region) before any real data goes to a cloud model.

Keys: read from the environment at call time, sent only to the provider you picked, never printed, logged, or written to disk. Do not paste a key into a file in this folder, and never commit one. Cost: a full run is four short calls, usually a few cents or less; check your provider's pricing page. Cloud models answer differently from run to run; the gates still decide the outcome.

Test the cloud path with no key and no internet: `python3 tests/test_cloud.py` (from the repo root) runs every lab against a bundled stand-in for the Anthropic, Responses, and Chat Completions APIs, with the same misbehaving model the Ollama test uses. Add `--real anthropic` (or `--real-xai`) for one real, paid run. Or `make test-cloud`.

## Use it in your own product

1. Copy `agents/AGENTS.md` and `agents/guardrails.yaml` and rewrite them for your agent.
2. Port the four functions: `classify/redact`, `gate`, `retrieve/trace_ok`, `reconcile` plus `record`.
3. Write one test per rule, like `test_gateways.py`.

MIT license. Teaching example, not legal advice.
