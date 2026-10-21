"""A stand-in for the cloud model APIs, for testing the cloud option with no key and no internet.

Mimics the request and response shapes of:
  POST /v1/messages          Anthropic Messages API (x-api-key + anthropic-version headers; thinking + text blocks)
  POST /v1/responses         OpenAI and xAI Responses API (Bearer key; reasoning item + message item)
  POST /v1/chat/completions  OpenAI-compatible Chat Completions (Bearer key optional)
Replies come from ollama_stub.reply_for, so local and cloud runs see the same adversarial or cooperative model.
Key must equal STUB_KEY or the stub returns HTTP 401. Model 'missing-model' returns HTTP 404.
STUB_FAIL=429 makes every call return HTTP 429. Binds 127.0.0.1 only. SYNTHETIC SAMPLE DATA ONLY.
"""
import json, os, re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import ollama_stub

STUB_KEY = "sk-test-NOT-A-REAL-KEY-0000"
CALLS = []


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}"
        req = json.loads(raw)
        path = self.path
        auth = self.headers.get("x-api-key") if path == "/v1/messages" else (self.headers.get("Authorization") or "").removeprefix("Bearer ")
        CALLS.append({"path": path, "model": req.get("model"), "body": raw.decode(), "auth_ok": auth == STUB_KEY,
                      "anthropic_version": self.headers.get("anthropic-version"), "has_auth": bool(auth)})
        if os.environ.get("STUB_FAIL") == "429":
            return self._json(429, {"error": {"message": "rate limited (stub)"}})
        if path in ("/v1/messages", "/v1/responses") and auth != STUB_KEY:
            return self._json(401, {"error": {"type": "authentication_error", "message": f"invalid x-api-key {auth}"}})
        if req.get("model") == "missing-model":
            return self._json(404, {"error": {"message": "model not found (stub)"}})
        if path == "/v1/messages":
            system, user = req.get("system", ""), " ".join(m["content"] for m in req["messages"])
            text = ollama_stub.reply_for(system, user)
            return self._json(200, {"id": "msg_stub", "type": "message", "role": "assistant", "model": req["model"],
                                    "content": [{"type": "thinking", "thinking": "SECRET-THOUGHTS should never print", "signature": "x"},
                                                {"type": "text", "text": text}], "stop_reason": "end_turn",
                                    "usage": {"input_tokens": 10, "output_tokens": 10}})
        if path == "/v1/responses":
            text = ollama_stub.reply_for(req.get("instructions", ""), req.get("input", ""))
            if str(req.get("model", "")).startswith("grok"):  # Grok style: source tag after the period
                text = re.sub(r"\s*(\[[A-Z]{2}-\d{4}-\d{4}:[A-Z]\d\])\.", r". \1", text)
            return self._json(200, {"id": "resp_stub", "object": "response", "model": req["model"], "status": "completed",
                                    "output": [{"type": "reasoning", "summary": [{"type": "summary_text", "text": "SECRET-THOUGHTS should never print"}]},
                                               {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": text, "annotations": []}]}],
                                    "usage": {"input_tokens": 10, "output_tokens": 10, "total_tokens": 20}})
        if path == "/v1/chat/completions":
            msgs = req.get("messages", [])
            text = ollama_stub.reply_for(" ".join(m["content"] for m in msgs if m["role"] == "system"),
                                         " ".join(m["content"] for m in msgs if m["role"] == "user"))
            return self._json(200, {"id": "chat_stub", "object": "chat.completion", "model": req["model"],
                                    "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}]})
        self._json(404, {"error": {"message": "not found"}})


def serve(port):
    return ThreadingHTTPServer(("127.0.0.1", port), H)
