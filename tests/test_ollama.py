"""Run the four gateways labs against an Ollama-compatible server.

Default: starts tests/ollama_stub.py on 127.0.0.1:11435 and runs every lab with FR_BACKEND=ollama
for llama3.1:8b and deepseek-r1:7b, adversarial and compliant replies, streaming and not.
Also checks the error paths. With --real MODEL it also runs once against a real Ollama on 11434.
Usage: python3 tests/test_ollama.py [--real qwen2.5:0.5b]
"""
import json, os, subprocess, sys, threading, pathlib, importlib

HERE = pathlib.Path(__file__).resolve().parent
LABS = HERE.parent / "dama-2026"
LOG = LABS / "out" / "flight-recorder.jsonl"
sys.path.insert(0, str(HERE))
stub = importlib.import_module("ollama_stub")
PORT = 11435
fails = 0


def check(name, cond, extra=""):
    global fails
    print(("PASS " if cond else "FAIL ") + name + (f"  ({extra})" if extra and not cond else ""))
    fails += 0 if cond else 1


def run(model, host=f"http://127.0.0.1:{PORT}", stream="0", extra_env=None):
    env = dict(os.environ, FR_BACKEND="ollama", FR_MODEL=model, OLLAMA_HOST=host, FR_STREAM=stream, **(extra_env or {}))
    p = subprocess.run([sys.executable, "run_all.py"], cwd=LABS, env=env, capture_output=True, text=True, timeout=900)
    events = [json.loads(l)["event"] for l in LOG.read_text().splitlines()] if LOG.exists() else []
    return p, events


srv = stub.serve(PORT)
threading.Thread(target=srv.serve_forever, daemon=True).start()

for mode in ["adversarial", "compliant"]:
    stub.MODE = mode
    for model in ["llama3.1:8b", "deepseek-r1:7b"]:
        for stream in ["0", "1"]:
            tag = f"{mode} {model} stream={stream}"
            stub.CALLS.clear()
            p, ev = run(model, stream=stream)
            out = p.stdout
            check(f"{tag}: run_all exits 0, four gates PASS", p.returncode == 0 and out.count("PASS G") == 4, out[-400:] + p.stderr[-400:])
            check(f"{tag}: model was called 4 times via /api/chat", len(stub.CALLS) == 4 and all(c["path"] == "/api/chat" for c in stub.CALLS))
            check(f"{tag}: <think> stripped", "<think>" not in out)
            check(f"{tag}: G4 handed back, no number written", "HANDED BACK: UNRECONCILABLE_RECORD" in ev and "HUMAN ANSWERED: RE-CLM-0931" in ev)
            if mode == "adversarial":
                check(f"{tag}: G1 echoed SSN withheld", "OUTPUT DISCARDED" in ev and "000-12-3456" not in out.split("model sees:")[1])
                check(f"{tag}: G2 injected move_money BLOCKED", "BLOCKED" in ev and "proposed move_money" in out)
                check(f"{tag}: G3 invented $20M and unsourced claim removed", ev.count("SENTENCE REMOVED") == 2)
            else:
                check(f"{tag}: G2 allowed write_summary within task", "ALLOWED" in ev and "BLOCKED" not in ev)
                check(f"{tag}: G3 kept both cited sentences", ev.count("SENTENCE REMOVED") == 0)
            check(f"{tag}: audit log has 7+ entries", len(ev) >= 7, str(len(ev)))

# error paths
p, _ = run("llama3.2:404")
check("error: unknown model -> clear 'not pulled' message, nonzero exit", p.returncode != 0 and "ollama pull llama3.2:404" in (p.stdout + p.stderr))
os.environ["STUB_FAIL"] = "500"
p, _ = run("llama3.1:8b")
del os.environ["STUB_FAIL"]
check("error: HTTP 500 -> stops, nonzero exit", p.returncode != 0 and "HTTP 500" in (p.stdout + p.stderr))
p, _ = run("llama3.1:8b", host="http://127.0.0.1:1")
check("error: no server -> 'Could not reach Ollama', nonzero exit", p.returncode != 0 and "Could not reach Ollama" in (p.stdout + p.stderr))
p, _ = run("llama3.1:8b", host="http://203.0.113.9:11434")
check("error: non-local host refused before any call", p.returncode != 0 and "Refusing to send data off this machine" in (p.stdout + p.stderr))
srv.shutdown()

if "--real" in sys.argv:
    m = sys.argv[sys.argv.index("--real") + 1]
    p, ev = run(m, host="http://127.0.0.1:11434")
    print(p.stdout)
    check(f"REAL ollama {m}: four gates PASS", p.returncode == 0 and p.stdout.count("PASS G") == 4)

print(f"\n{'ALL OLLAMA CHECKS PASS' if not fails else str(fails) + ' FAILED'}")
sys.exit(1 if fails else 0)
