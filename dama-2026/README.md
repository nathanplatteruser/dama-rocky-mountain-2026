# The Four Gateways: security and data privacy for AI agents

Hands-on labs for **DAMA Rocky Mountain, October 22, 2026**. Presented by Nathan Platter, Lincoln NE.

**All data is SYNTHETIC SAMPLE DATA.** Every name, number, and ID is invented. Nothing here needs an internet connection or an API key, and nothing leaves your laptop.

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

The labs refuse to call any Ollama host other than localhost. The guardrails still decide the outcome when a real model answers differently from the mock, and that is the point: the model can be swapped, the gates stay.

## Use it in your own product

1. Copy `agents/AGENTS.md` and `agents/guardrails.yaml` and rewrite them for your agent.
2. Port the four functions: `classify/redact`, `gate`, `retrieve/trace_ok`, `reconcile` plus `record`.
3. Write one test per rule, like `test_gateways.py`.

MIT license. Teaching example, not legal advice.
