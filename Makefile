# Four gateways labs. Windows users without make: run the python commands directly.
PY ?= python3
.PHONY: test test-mock test-ollama test-ollama-real
test: test-mock test-ollama
test-mock:
	cd dama-2026 && $(PY) run_all.py && $(PY) -m unittest test_gateways
test-ollama:          ## labs against the bundled Ollama API stub (no download)
	$(PY) tests/test_ollama.py
test-ollama-real:     ## also against your real Ollama: make test-ollama-real MODEL=llama3.1:8b
	$(PY) tests/test_ollama.py --real $(MODEL)
