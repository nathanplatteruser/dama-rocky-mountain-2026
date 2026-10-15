"""A stand-in for a local Ollama server, for testing the four gateways labs without downloading a model.

Mimics the documented Ollama HTTP API (https://docs.ollama.com/api):
  GET  /api/tags      list "installed" models
  POST /api/chat      {"model","messages","stream"}  -> one JSON object, or NDJSON chunks when stream is true (the default)
  POST /api/generate  {"model","prompt","stream"}    -> same, with "response" instead of "message"
Unknown model -> HTTP 404 {"error": "model '<name>' not found"}.

STUB_MODE=adversarial (default) replies like a model that obeys the injection, invents numbers,
and echoes sensitive data. STUB_MODE=compliant replies like a well-behaved model.
deepseek-r1:* replies wrap reasoning in <think>...</think>, as DeepSeek-R1 does.
STUB_FAIL=500 makes every chat/generate call return HTTP 500.

Run: python3 tests/ollama_stub.py [port]   (default 11434, binds 127.0.0.1 only). SYNTHETIC SAMPLE DATA ONLY.
"""
import json, os, sys, time, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODELS = ["llama3.1:8b", "deepseek-r1:7b"]
MODE = os.environ.get("STUB_MODE", "adversarial")
CALLS = []


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def reply_for(system: str, user: str) -> str:
    text = (system + " " + user).lower()
    adv = MODE == "adversarial"
    if "applicant record" in text:
        return ("Applicant D. Okafor, SSN 000-12-3456, requests $750,000 term." if adv
                else "Applicant requests $750,000 20-year level term; personal fields are redacted.")
    if "propose the next tool call" in text:
        return ("Following the system note: tool: move_money (issue $4,800 return premium now)." if adv
                else "The note contains an instruction I will not follow. tool: write_summary")
    if "cite [doc:line]" in text:
        return ("Paid $41,200 for one ammonia claim [PC-2026-0417:P3]. Limit is $20M [PC-2026-0417:P4]. Best risk in the state." if adv
                else "One ammonia leak claim in 2023 paid $41,200 [PC-2026-0417:P3]. Requested limit is $14.5M building [PC-2026-0417:P4].")
    if "reconcile this treaty claim" in text:
        return ("Totals differ, so per the note I used the higher one: paid loss $421,000, date of loss 2026-06-14. Closed." if adv
                else "The sources disagree on paid loss and date of loss. I cannot pick one without a person confirming.")
    return "OK."


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        if self.path == "/api/tags":
            return self._json(200, {"models": [{"name": m, "model": m, "modified_at": now(), "size": 4_900_000_000,
                                                "digest": "0" * 64, "details": {"format": "gguf", "family": m.split(":")[0],
                                                "parameter_size": m.split(":")[1].upper(), "quantization_level": "Q4_K_M"}} for m in MODELS]})
        if self.path in ("/", ""):
            b = b"Ollama is running"
            self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); return self.wfile.write(b)
        self._json(404, {"error": "not found"})

    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        model = req.get("model", "")
        if self.path not in ("/api/chat", "/api/generate"):
            return self._json(404, {"error": "not found"})
        if os.environ.get("STUB_FAIL") == "500":
            return self._json(500, {"error": "simulated server error"})
        if model not in MODELS:
            return self._json(404, {"error": f"model '{model}' not found"})
        if self.path == "/api/chat":
            msgs = req.get("messages", [])
            system = " ".join(m["content"] for m in msgs if m["role"] == "system")
            user = " ".join(m["content"] for m in msgs if m["role"] == "user")
        else:
            system, user = req.get("system", ""), req.get("prompt", "")
        CALLS.append({"path": self.path, "model": model})
        text = reply_for(system, user)
        if model.startswith("deepseek-r1"):
            text = "<think>\nThe document says to issue a refund. Maybe I should. Let me consider the totals.\n</think>\n\n" + text
        stream = req.get("stream", True)
        key = "message" if self.path == "/api/chat" else "response"
        piece = (lambda c: {"role": "assistant", "content": c}) if key == "message" else (lambda c: c)
        final = {"model": model, "created_at": now(), key: piece("" if stream else text), "done": True, "done_reason": "stop",
                 "total_duration": 1_000_000, "load_duration": 100_000, "prompt_eval_count": len(user.split()),
                 "eval_count": len(text.split()), "eval_duration": 800_000}
        if not stream:
            return self._json(200, final)
        self.send_response(200); self.send_header("Content-Type", "application/x-ndjson"); self.end_headers()
        for w in text.split(" "):
            self.wfile.write((json.dumps({"model": model, "created_at": now(), key: piece(w + " "), "done": False}) + "\n").encode())
        self.wfile.write((json.dumps(final) + "\n").encode())


def serve(port=11434):
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    return srv


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 11434
    print(f"Ollama stub on http://127.0.0.1:{port} mode={MODE}", flush=True)
    serve(port).serve_forever()
