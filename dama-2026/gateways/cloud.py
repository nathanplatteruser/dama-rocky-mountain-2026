"""Cloud model option for the labs: Anthropic Claude, xAI Grok, OpenAI, or any OpenAI-compatible server.

Same prompts, same four gateways, same audit log as the local Ollama path. Only the model changes.
You bring your own API key in an environment variable. The key is read at call time, sent only to
the provider you picked, and never printed, logged, or written to disk.

  FR_BACKEND=anthropic   key: ANTHROPIC_API_KEY   default model: claude-opus-5-5
  FR_BACKEND=xai         key: XAI_API_KEY         default model: grok-4.7
  FR_BACKEND=openai      key: OPENAI_API_KEY      default model: gpt-6.1-sol
  FR_BACKEND=compatible  key: FR_API_KEY (optional for local servers), base URL: FR_BASE_URL (required)

FR_MODEL overrides the model. FR_BASE_URL overrides the endpoint for any provider (tests, proxies, gateways).
FR_MAX_TOKENS caps the reply, including any thinking or reasoning tokens (default 16000; you pay only for what is used).

Cloud runs send SYNTHETIC SAMPLE DATA to the provider. That is a Gateway 1 decision, so before every call
this module checks the outgoing text: if any raw sensitive value from the record (SSN, phone, email, name,
date of birth, address, health note) is present, it refuses to send and the run stops. Fail closed.
Only the Python standard library is used.
"""
import json, os, re, urllib.error, urllib.request

PROVIDERS = {
    "anthropic":  {"label": "Anthropic Claude", "key_env": "ANTHROPIC_API_KEY", "model": "claude-opus-5-5",
                   "base": "https://api.anthropic.com/v1", "api": "messages"},
    "xai":        {"label": "xAI Grok", "key_env": "XAI_API_KEY", "model": "grok-4.7",
                   "base": "https://api.x.ai/v1", "api": "responses"},
    "openai":     {"label": "OpenAI", "key_env": "OPENAI_API_KEY", "model": "gpt-6.1-sol",
                   "base": "https://api.openai.com/v1", "api": "responses"},
    "compatible": {"label": "OpenAI-compatible", "key_env": "FR_API_KEY", "model": "",
                   "base": "", "api": "chat"},
}

# Patterns that must never leave the machine. Dates are checked by exact value, not by pattern,
# because claim dates (2026-06-14) are INTERNAL, not personal data.
EGRESS_PATTERNS = {"ssn": r"\b\d{3}-\d{2}-\d{4}\b", "phone": r"\b\d{3}-\d{3}-\d{4}\b", "email": r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"}
LOCAL_HOSTS = ("localhost", "127.0.0.1", "::1", "[::1]")


def default_model(backend: str) -> str:
    return PROVIDERS.get(backend, {}).get("model", "")


def _host(url: str) -> str:
    rest = url.split("//", 1)[-1]
    return rest.split("/", 1)[0].rsplit(":", 1)[0] if not rest.startswith("[") else rest.split("]")[0] + "]"


def endpoint(backend: str) -> str:
    p = PROVIDERS[backend]
    base = (os.environ.get("FR_BASE_URL") or p["base"]).rstrip("/")
    if not base:
        raise SystemExit("FR_BACKEND=compatible needs FR_BASE_URL, for example https://openrouter.ai/api/v1 or http://localhost:1234/v1")
    if not base.startswith("https://") and _host(base) not in LOCAL_HOSTS:
        raise SystemExit("Refusing to send an API key over plain http. FR_BASE_URL must start with https:// (http is allowed only for localhost).")
    return base + {"messages": "/messages", "responses": "/responses", "chat": "/chat/completions"}[p["api"]]


def sensitive_values() -> list:
    from common import DATA, POLICY
    rec = DATA["contact_sheet"]
    return [str(rec[f]) for f in POLICY["sensitive_fields"] if f in rec]


def egress_check(text: str) -> list:
    """Return what would leak. Empty list means the payload may leave."""
    found = [k for k, p in EGRESS_PATTERNS.items() if re.search(p, text)]
    found += [f"value:{v[:3]}..." for v in sensitive_values() if v in text]
    return found


def _scrub(msg: str, key: str) -> str:
    return msg.replace(key, "[KEY]") if key else msg


def complete(backend: str, model: str, system: str, user: str) -> str:
    from common import record
    p = PROVIDERS[backend]
    if not model:
        raise SystemExit("FR_BACKEND=compatible needs FR_MODEL, the model name your server expects.")
    key = os.environ.get(p["key_env"], "").strip()
    if not key and backend != "compatible":
        raise SystemExit(f"{p['label']} needs an API key. Set {p['key_env']} in this terminal (it is never saved by the labs), "
                         "or unset FR_BACKEND to use mock mode.")
    url = endpoint(backend)
    leaks = egress_check(system + "\n" + user)
    if leaks:
        record("G1", "CLOUD CALL REFUSED", f"{backend}/{model}: outgoing text contained {len(leaks)} sensitive item(s) {leaks}; nothing sent")
        raise SystemExit("Refusing to send: the outgoing text contains sensitive data. Redact it first, or use the local model.")
    record("G1", "CLOUD EGRESS CHECKED", f"{backend}/{model}: 0 sensitive values in payload; SYNTHETIC SAMPLE DATA sent to {p['label']}")
    max_tokens = int(os.environ.get("FR_MAX_TOKENS", "16000"))
    headers = {"Content-Type": "application/json"}
    if p["api"] == "messages":
        headers.update({"x-api-key": key, "anthropic-version": "2023-06-01"})
        body = {"model": model, "max_tokens": max_tokens, "system": system, "messages": [{"role": "user", "content": user}]}
    elif p["api"] == "responses":
        headers["Authorization"] = f"Bearer {key}"
        body = {"model": model, "instructions": system, "input": user, "store": False, "max_output_tokens": max_tokens}
    else:
        if key:
            headers["Authorization"] = f"Bearer {key}"
        body = {"model": model, "max_tokens": max_tokens,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    if os.environ.get("FR_TEMPERATURE"):
        body["temperature"] = float(os.environ["FR_TEMPERATURE"])
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=int(os.environ.get("FR_TIMEOUT", "180"))) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read() or b"{}").get("error", "")
            detail = detail.get("message", "") if isinstance(detail, dict) else str(detail)
        except Exception:
            detail = ""
        detail = _scrub(str(detail)[:200], key)
        hint = {401: f"the key in {p['key_env']} was rejected", 403: "the key is not allowed to use this model",
                404: f"model '{model}' was not found; set FR_MODEL to a model your account can use",
                429: "rate limit or no credits left on the account"}.get(e.code, "")
        raise SystemExit(f"{p['label']} returned HTTP {e.code}{': ' + hint if hint else ''}. {detail}".strip())
    except OSError as e:
        raise SystemExit(f"Could not reach {p['label']} at {_host(url)} ({_scrub(str(e), key)}). Check your internet connection, "
                         "or unset FR_BACKEND to use mock mode.")
    return extract_text(p["api"], data)


def extract_text(api: str, data: dict) -> str:
    if api == "messages":  # Anthropic: keep text blocks, drop thinking blocks
        return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text").strip()
    if api == "responses":  # OpenAI and xAI Responses API: message items only, never reasoning summaries
        if isinstance(data.get("output_text"), str) and data["output_text"]:
            return data["output_text"].strip()
        return "".join(c.get("text", "") for item in data.get("output", []) if item.get("type") == "message"
                       for c in item.get("content", []) if c.get("type") == "output_text").strip()
    return ((data.get("choices") or [{}])[0].get("message", {}).get("content") or "").strip()
