# DAMA Rocky Mountain 2026: The Four Gateways of AI Security and Data Privacy

Teaching materials for the DAMA Rocky Mountain session, October 2026. Presented by Nathan Platter, Lincoln NE.

**No pitch.** Nothing here is for sale and no product is named. It is vendor-neutral teaching material: take it and use it under the MIT license.

**Live demo (four gateways view on):** https://nathanplatteruser.github.io/dama-rocky-mountain-2026/flight-recorder/

Add `?gateways=0` for the plain view. All policy data is SYNTHETIC SAMPLE DATA; see [DATA-SOURCES.md](flight-recorder/DATA-SOURCES.md).

**Setup guide:** [PDF](docs/Four-Gateways-Setup-Guide.pdf) | [Word](docs/Four-Gateways-Setup-Guide.docx)

## The four gateways

1. **Use:** classify every field before it reaches a model; redact, or route sensitive records to a local model only. Check the output too.
2. **Prompt:** locked instructions, prompt-injection defense, and a tool allow-list. Text inside a document is data, never an instruction.
3. **Context:** permissioned retrieval, a source on every claim, the minimum data for the task.
4. **Self-check and exit:** fail closed, ask a named human a specific question, and write every decision to the audit log.

## What is here

- [`flight-recorder/`](flight-recorder/) the clickable demo, including the closing comparison table (fully human, OCR plus review, single-pass AI, agentic) with editable inputs
- [`flight-recorder/takehomes/`](flight-recorder/takehomes/) permission-card template, pilot-to-production checklist, curveball checklist
- [`dama-2026/`](dama-2026/) four gateways labs in Python (mock mode or a local model through Ollama), AGENTS.md, guardrails.yaml
- [`docs/`](docs/) setup guide (.pdf and .docx)
- [`tests/`](tests/) `gateways.mjs` (browser checks), `test_ollama.py` (labs against a bundled Ollama API stub, or your real Ollama)

## Run it

```
cd dama-2026 && python3 run_all.py && python3 -m unittest test_gateways
python3 tests/test_ollama.py
```

Or `make test`. Windows users without make: run the python commands directly.

Free to use under the MIT license.
