# Flight Recorder

> **New here? Read the [Four Gateways setup guide (PDF)](../docs/Four-Gateways-Setup-Guide.pdf).** The four gateways view is on by default; add `?gateways=0` for the plain view.

A free, offline walkthrough of a governed AI workflow for insurance. It shows five guardrails on one underwriting-summary agent, then turns the action log into a regulator-ready evidence pack.

**Everything in the policy files is SYNTHETIC SAMPLE DATA.** See [DATA-SOURCES.md](DATA-SOURCES.md) for exactly what's invented and what's public. The "agent" is scripted, so the demo runs the same way every time with no internet, no account, and no model. Swap in any model your company approves. The guardrails are the point, not the model.

## What you'll see (about 18 minutes)
1. **Permission card.** What the agent may do, what it may never do, and who answers for it.
2. **Summaries with sources.** Three files (P&C commercial property, individual life, property cat reinsurance). Every sentence carries a source tag you can click.
3. **Second-pass verifier.** A separate check opens each cited line and confirms every number and term is there. Unsupported sentences come out. Sentences that rest on a replaced form are marked "supported by a superseded source."
4. **Last year's form.** Every form, rider, and clause reference is checked against a forms library, with or without an edition date. A retired edition (EB-204) and an undated clause (HC-3) are held until an underwriter confirms the current version.
5. **Out-of-scope action.** An instruction hidden in a broker note asks the agent to issue a $4,800 return premium. The gate blocks it, logs it, and escalates to named roles.
6. **Watchlist: sneaky cases.** Three scenario cards where the system suspects something and pulls in a named person: (a) a state market exit, so the file conflicts with current appetite and filings (to the regional Underwriting Manager); (b) a reinsurer that excluded a state the primary still writes, so the ceded share may be uncovered (to the Ceded Reinsurance Manager); (c) impersonation signals such as a callback mismatch, video metadata dated before the loss, a look-alike approval email, and the same device and bank account across three claims (to an SIU Analyst). Reason codes on every card. The system never decides and never declares fraud.
7. **Curveballs.** Nine traps that fool a QC check and a careful person, each with a naive result, the guardrail result, what would have gone wrong, an estimated impact, a reason code, and a named reviewer: a handwritten margin edit OCR misread ($1,500 vs $7,500), amounts stored as text (European format, scientific notation, trailing space, dropped leading zero), rounding drift ($0.005 x 2,000 lines = $10), a stale privacy notice ranked first by search, a loss 3 minutes before coverage hidden by UTC, a treaty schedule in thousands, a duplicate claim with a look-alike name (Cyrillic letter), a 03/04 date that could be March or April, and a producer license that expired before binding.
8. **Closer: the regulator asks.** One click builds an evidence pack from the ledger, mapped to the NAIC AI Model Bulletin and Colorado 3 CCR 702-10.

## Step 0: quick intake (v1.4)
Five one-tap questions (about 10 seconds) before the permission card: role, AI familiarity, closeness to the raw data, line of business, and what you want to see. Or tap "Skip, show me everything." The answers set a profile:
- **Executive view** (C-suite, VP): a bottom line and "what would have happened" on each step, a dollar impact summary on step 7 with card details collapsed, and an executive scorecard at the end.
- **Manager view** (Director, Manager): who gets escalated, team workload by reviewer role, and checklist items.
- **Practitioner view** (hands-on): raw values on every curveball card, reason codes open, and the ledger fully expanded.
- **Technical lines** are added for anyone who builds or governs AI workflows or lives in the data.
- **Line of business** sets the four presenter picks on step 7.

A "Tailored for" chip with a change link sits on every step. The profile is the first ledger entry, and every change is logged and included in the evidence pack. Your answers stay in this browser. Nothing is saved or sent, and there are no network calls.

## Step 7: curveballs (v1.3)
27 curveballs in 9 categories: Claims, Payments and Billing, Underwriting and Policy, Health/Auth, Life, Workers' Comp, Reinsurance, Fraud and Identity, Data Quirks. Filter chips switch categories. The default view is Presenter picks (HW, DP, AU, TZ). "Re-run all checks" and "Mark all spot-checks done" handle the full set. Every hold and spot-check is written to the ledger with its category, and all 27 appear in the evidence pack. Full list: [takehomes/curveball-checklist.md](takehomes/curveball-checklist.md).

## Run it
No install needed.

**Mac:** download or clone this folder, then double-click `index.html`. It opens in Safari or Chrome.
**Windows:** download the ZIP (green Code button, Download ZIP), right-click, Extract All, then double-click `index.html`. It opens in Edge or Chrome.

Optional local server (either OS, if your browser blocks downloads from local files):
```
python3 -m http.server 8000      # Mac
py -m http.server 8000           # Windows
```
Then open http://localhost:8000.

Use the left and right arrow keys to move between steps. Jump straight to a step by adding `#step1` through `#step8` to the address. "Reset demo" starts over.

## Files
- `index.html` the whole demo, one file
- `takehomes/` permission-card template, pilot-to-production checklist, and curveball checklist

## Sources for the regulatory mapping (accessed 2026-10-12)
| Source | Exact sections used | URL |
|---|---|---|
| NAIC Model Bulletin: Use of Artificial Intelligence Systems by Insurers, adopted Dec 4, 2023 | Sec. 3: AIS Program Guidelines 1.3, 2.3(b), 2.3(d), 3.1, 3.2, 3.4, 3.6, and risk consideration (iii). Sec. 4: items 1.1(e)(i)(1), 1.3, 1.3(b) | https://content.naic.org/sites/default/files/cmte-h-big-data-artificial-intelligence-wg-ai-model-bulletin.pdf.pdf |
| Colorado 3 CCR 702-10, Regulation 10-1-1, amended effective Oct 15, 2025 | Sec. 3 (applicability: individual life, private passenger auto, health benefit plans), Sec. 4.D (ECDIS), Sec. 5.A.6, 5.A.9, 5.C | https://sos.state.co.us/CCR/GenerateRulePdf.do?fileName=3+CCR+702-10&ruleVersionId=12182 |

Check each reference against your own state's adopted version. This is a teaching example, not legal advice.

## Testing
Run `node tests/gateways.mjs` (needs the playwright package) and `python3 tests/test_ollama.py`.

## License
MIT. Copy it, change it, use it at work.
