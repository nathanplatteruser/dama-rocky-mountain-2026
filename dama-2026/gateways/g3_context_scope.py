"""Gateway 3. Context: permissioned retrieval, source trace on every claim, minimum data."""
import re
from common import DATA, POLICY, record
from llm import banner, complete


def retrieve(role: str, query_terms: list, max_lines: int = 2) -> list:
    """Return only lines this role may see, only lines that match, and no more than needed."""
    allowed = POLICY["role_access"].get(role, [])
    hits, denied = [], []
    for doc in DATA["documents"]:
        if doc["owner_role"] not in allowed:
            denied.append(doc["id"])
            continue
        for tag, line in doc["lines"].items():
            if any(t.lower() in line.lower() for t in query_terms):
                hits.append({"doc": doc["id"], "line": tag, "text": line})
    return hits[:max_lines], denied


def trace_ok(answer: str, context: list) -> list:
    """Every sentence must cite [DOC:LINE] that was actually retrieved, and its numbers must appear there."""
    cited = {f"{c['doc']}:{c['line']}": c["text"] for c in context}
    problems = []
    for s in [x.strip() for x in re.split(r"(?<=\.)\s+", answer) if x.strip()]:
        refs = re.findall(r"\[([A-Z]{2}-\d{4}-\d{4}:[A-Z]\d)\]", s)
        if not refs or any(r not in cited for r in refs):
            problems.append(f"no valid source: {s}")
            continue
        nums = re.findall(r"\$?\d[\d,.]*M?", re.sub(r"\[.*?\]", "", s))
        if any(n.rstrip(".") not in " ".join(cited[r] for r in refs) for n in nums):
            problems.append(f"number not in source: {s}")
    return problems


def main() -> dict:
    banner("G3 Context: permissioned retrieval and source trace")
    ctx, denied = retrieve("underwriting", ["loss", "limit", "salary"])
    record("G3", "RETRIEVED", f"{len(ctx)} lines for role underwriting; denied docs {denied}")
    for c in ctx:
        print(f"  [{c['doc']}:{c['line']}] {c['text']}")
    answer = complete("Answer only from the context. Cite [DOC:LINE] after every sentence.",
                      "\n".join(f"[{c['doc']}:{c['line']}] {c['text']}" for c in ctx) + "\nQ: Summarize loss history and limits.",
                      mock="One ammonia leak claim in 2023 paid $41,200 [PC-2026-0417:P3]. Building limit requested is $15M [PC-2026-0417:P4]. Loss ratio is excellent.")
    print("  answer:", answer)
    problems = trace_ok(answer, ctx)
    for p in problems:
        record("G3", "SENTENCE REMOVED", p)
    return {"retrieved": len(ctx), "denied": denied, "removed": len(problems)}


if __name__ == "__main__":
    main()
