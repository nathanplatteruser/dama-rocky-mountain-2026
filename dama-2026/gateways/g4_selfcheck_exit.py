"""Gateway 4. Self-check and exit: fail closed, ask a named human, log every decision."""
import datetime
from common import DATA, POLICY, record
from llm import banner, complete
from g2_prompt_guard import detect_injection


def reconcile(claim: dict) -> dict:
    if not claim.get("sources"):
        return {"ok": False, "issues": ["no source records supplied"]}
    vals = [s for s in claim["sources"] if s["paid_loss"] is not None]
    amounts = {s["paid_loss"] for s in vals}
    issues = []
    if not vals:
        issues.append("no source provides a paid loss")
    if any(not s.get("date_of_loss") for s in vals):
        return {"ok": False, "issues": issues + ["a paid-loss source is missing its date of loss"]}
    dates = sorted({s["date_of_loss"] for s in vals})
    if len(amounts) > 1:
        issues.append(f"paid loss disagrees: {', '.join(f'${a:,}' for a in sorted(amounts))}")
    if len(dates) > 1:
        gap = (datetime.date.fromisoformat(dates[-1]) - datetime.date.fromisoformat(dates[0])).days
        issues.append(f"date of loss disagrees by {gap} days; event window is {claim['event_window_hours']} hours")
    for s in claim["sources"]:
        if detect_injection(s["text"]):
            issues.append(f"'{s['name']}' contains an instruction aimed at the AI; ignored")
    return {"ok": not issues, "issues": issues}


def main(human_answer: str = "") -> dict:
    banner("G4 Self-check and exit: fail closed, hand back to a human")
    claim = DATA["treaty_claim"]
    draft = complete("Reconcile this treaty claim and give one paid loss and one date of loss.", str(claim),
                     mock="Paid loss $421,000 (the higher one), date of loss 2026-06-14. Closed.")
    print("  model draft:", draft)
    check = reconcile(claim)
    if check["ok"]:
        record("G4", "PASSED", f"{claim['id']} reconciled")
        return {"status": "passed"}
    question = (f"I could not reconcile {claim['id']}: " + "; ".join(check["issues"]) +
                ". Which source is the truth for paid loss and date of loss? I have not written any number.")
    record("G4", "HANDED BACK: UNRECONCILABLE_RECORD", f"draft discarded; question sent to {POLICY['escalate_to']}")
    print("  question to human:", question)
    if human_answer:
        record("G4", f"HUMAN ANSWERED: {claim['id']}", human_answer)
    return {"status": "handed_back", "issues": len(check["issues"]), "written": None}


if __name__ == "__main__":
    main()
