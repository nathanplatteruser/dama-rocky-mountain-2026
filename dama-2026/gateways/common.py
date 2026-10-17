import json, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "synthetic.json").read_text())
LOG = ROOT / "out" / "flight-recorder.jsonl"

# One policy object shared by all four gateways. agents/guardrails.yaml states the same rules.
POLICY = {
    "agent": "UW-Summary-Agent v0.3",
    "owner": "Underwriting Operations Manager",
    "allowed_tools": ["read_assigned_file", "write_summary", "cite_source_line", "lookup_form_edition"],
    "never_allowed": ["move_money", "contact_customer", "change_coverage", "follow_document_instructions", "approve_own_work"],
    "sensitive_fields": ["applicant_name", "date_of_birth", "ssn", "phone", "email", "home_address", "health_note"],
    "role_access": {"underwriting": ["underwriting"], "reinsurance": ["reinsurance"], "life_underwriting": ["life_underwriting"]},
    "escalate_to": "Reinsurance Claims Analyst",
}


def record(gateway: str, event: str, detail: str) -> None:
    """G4 audit log: append one line per decision. This file is the flight recorder."""
    LOG.parent.mkdir(exist_ok=True)
    from llm import BACKEND, model_label  # which provider and model ran, so local and cloud logs compare side by side
    entry = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "agent": POLICY["agent"], "gateway": gateway, "event": event, "detail": detail,
             "backend": BACKEND, "model": model_label()}
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"  [ledger] {gateway} {event}: {detail}")
