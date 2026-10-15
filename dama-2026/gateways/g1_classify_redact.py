"""Gateway 1. Use: classify every field, redact sensitive ones, keep raw data on a local model."""
import re
from common import DATA, POLICY, record
from llm import BACKEND, banner, complete

PATTERNS = {"ssn": r"\b\d{3}-\d{2}-\d{4}\b", "phone": r"\b\d{3}-\d{3}-\d{4}\b", "email": r"\b[\w.]+@[\w.]+\.\w+\b", "dob": r"\b(19|20)\d{2}-\d{2}-\d{2}\b"}


def classify(field: str, value: str) -> str:
    if field in POLICY["sensitive_fields"] or any(re.search(p, value) for p in PATTERNS.values()):
        return "SENSITIVE"
    return "PUBLIC" if field == "product" else "INTERNAL"


def redact(rec: dict) -> dict:
    return {k: (f"[{k.upper()}_REDACTED]" if classify(k, str(v)) == "SENSITIVE" else v) for k, v in rec.items()}


def route(classes: set) -> str:
    """Sensitive data may only go to a local model. Everything else may use an approved cloud model."""
    return "local-only" if "SENSITIVE" in classes else "approved-cloud-ok"


def main() -> dict:
    banner("G1 Use: classify and redact")
    rec = {k: v for k, v in DATA["contact_sheet"].items() if k != "id"}
    classes = {k: classify(k, str(v)) for k, v in rec.items()}
    for k, c in classes.items():
        print(f"  {k:16} {c}")
    safe = redact(rec)
    leaked = [v for k, v in rec.items() if classes[k] == "SENSITIVE" and str(v) in str(safe)]
    assert not leaked, f"sensitive values leaked: {leaked}"
    n = sum(c == "SENSITIVE" for c in classes.values())
    record("G1", "REDACTION APPLIED", f"{DATA['contact_sheet']['id']}: {n} of {len(rec)} fields SENSITIVE, redacted before any non-local call")
    target = route(set(classes.values()))
    record("G1", "ROUTED", f"raw record is {target}; backend in use: {BACKEND}")
    summary = complete("Summarize this insurance applicant record in one sentence. Do not invent values.",
                       str(safe), mock=f"Applicant requests {safe['face_amount']} {safe['product']}; identity and health fields are redacted.")
    echoed = [str(v) for k, v in rec.items() if classes[k] == "SENSITIVE" and str(v) in summary]
    if echoed:
        record("G1", "OUTPUT DISCARDED", f"model output contained {len(echoed)} sensitive value(s) it was never sent; summary withheld")
        summary = "[withheld: output contained sensitive values]"
    print("  model sees:", safe)
    print("  summary:", summary)
    return {"sensitive": n, "leaked": len(leaked), "route": target, "output_leak_blocked": bool(echoed), "summary": summary}


if __name__ == "__main__":
    main()
