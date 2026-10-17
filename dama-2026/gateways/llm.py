"""Model backend for the labs. Mock mode is the default and needs nothing installed.

Set FR_BACKEND=ollama to call a local Ollama server (http://localhost:11434).
Set FR_MODEL to pick the model, for example llama3.1:8b or deepseek-r1:7b.
Set FR_STREAM=1 to use streaming responses (NDJSON).
Cloud option (paid, your own API key): FR_BACKEND=anthropic, xai, openai, or compatible. See cloud.py.
Only the Python standard library is used, so there is nothing to pip install.
"""
import json, os, re, urllib.error, urllib.request

BACKEND = os.environ.get("FR_BACKEND", "mock").lower()
CLOUD = ("anthropic", "xai", "openai", "compatible")
if BACKEND in CLOUD:
    import cloud
    MODEL = os.environ.get("FR_MODEL") or cloud.default_model(BACKEND)
else:
    MODEL = os.environ.get("FR_MODEL", "llama3.1:8b")
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
if not OLLAMA.startswith("http"):
    OLLAMA = "http://" + OLLAMA


def _strip_think(text: str) -> str:
    # deepseek-r1 prints its reasoning inside <think> tags; keep only the answer
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()


def complete(system: str, user: str, mock: str) -> str:
    """Return a model reply. In mock mode return the scripted reply so runs are repeatable."""
    if BACKEND in CLOUD:
        return _strip_think(cloud.complete(BACKEND, MODEL, system, user))
    if BACKEND != "ollama":
        return mock
    host = OLLAMA.split("//", 1)[1].split(":")[0]
    if host not in ("localhost", "127.0.0.1", "::1"):
        raise SystemExit("Refusing to send data off this machine. OLLAMA_HOST must be localhost.")
    stream = os.environ.get("FR_STREAM", "0") == "1"
    body = json.dumps({"model": MODEL, "stream": stream, "options": {"temperature": 0},
                       "messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(OLLAMA + "/api/chat", data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            if not stream:
                return _strip_think(json.loads(r.read())["message"]["content"])
            out = []
            for line in r:  # NDJSON: one chunk per line, last one has "done": true
                if line.strip():
                    chunk = json.loads(line)
                    out.append(chunk.get("message", {}).get("content", ""))
                    if chunk.get("done"):
                        break
            return _strip_think("".join(out))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise SystemExit(f"Ollama is running but model '{MODEL}' is not pulled. Run: ollama pull {MODEL}")
        raise SystemExit(f"Ollama returned HTTP {e.code}.")
    except OSError as e:
        raise SystemExit(f"Could not reach Ollama at {OLLAMA} ({e}). Start it with `ollama serve`, or unset FR_BACKEND to use mock mode.")


def model_label() -> str:
    """Which model wrote the drafts, for the banner and the audit log."""
    return MODEL if BACKEND == "ollama" or BACKEND in CLOUD else "scripted"


def banner(title: str) -> None:
    where = " | CLOUD: synthetic data goes to the provider" if BACKEND in CLOUD else ""
    print(f"\n=== {title} | backend: {BACKEND}{' (' + MODEL + ')' if BACKEND == 'ollama' or BACKEND in CLOUD else ''} | SYNTHETIC SAMPLE DATA{where} ===")
