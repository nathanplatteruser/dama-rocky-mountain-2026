# Four gateways labs. Windows users without make: run the python commands directly.
PY ?= python3
.PHONY: test test-mock test-ollama test-ollama-real test-cloud test-cloud-real
test: test-mock test-ollama test-cloud
test-mock:
	cd dama-2026 && $(PY) run_all.py && $(PY) -m unittest test_gateways
test-ollama:          ## labs against the bundled Ollama API stub (no download)
	$(PY) tests/test_ollama.py
test-ollama-real:     ## also against your real Ollama: make test-ollama-real MODEL=llama3.1:8b
	$(PY) tests/test_ollama.py --real $(MODEL)
test-cloud:           ## cloud option (Claude, Grok, OpenAI, compatible) against a bundled API stub (no key, no internet)
	$(PY) tests/test_cloud.py
test-cloud-real:      ## also one real run, paid: make test-cloud-real PROVIDER=anthropic (needs that provider's key in env)
	$(PY) tests/test_cloud.py --real $(PROVIDER)
