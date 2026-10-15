# Data sources: what's synthetic and what's public

## Synthetic (invented for this demo)
Everything below is made up. Any resemblance to a real company or person is a coincidence.
- All three policy files: PC-2026-0417 (Prairie Ridge Cold Storage LLC), LF-2026-1188 (D. Okafor), RE-2026-0072 (Heartland Mutual Insurance Co.)
- All names, addresses, ages, medical readings, limits, layers, loss amounts, and percentages inside those files
- The forms library: EB-204, WP-11, HC-3, their editions, retirement dates, and the changes listed
- The agent name (UW-Summary-Agent v0.3), its output sentences, the $4,800 return premium request, ticket ESC-0001, and every ledger timestamp
- The watchlist cases in step 6: the state of "Westland" (not a real state), files PC-2026-0533, PC-2026-0611, CL-2026-1201, CL-2026-1244, CL-2026-1290, the appetite and filing statuses, the treaty territorial exclusion, the device ID, bank account ending 4471, the look-alike domain, and every signal listed
- All nine curveballs in step 7: claim CL-2026-1310 and its handwritten note (drawn as an image in the page, not a real scan), the OCR confidence 0.58, every amount, format, policy number 00047213, the 2,000-line rounding example, Privacy Notice PN-7 and its editions, the loss time and policy inception, the treaty bordereau, the names John Miller and Jon Mіller, VIN tail 2291, the 03/04/2026 date, the producer license dates, and every dollar impact (all labeled as estimates)
- The role names on the permission card (they're generic job titles, not people)

Every file in the demo carries a purple **SYNTHETIC SAMPLE DATA** label.

## Public (real, cited)
Accessed 2026-10-12.

| Source | Used for | URL |
|---|---|---|
| NAIC Model Bulletin: Use of Artificial Intelligence Systems by Insurers, adopted Dec 4, 2023 | Section 3 (AIS Program Guidelines 1.3, 2.3(b), 2.3(d), 3.1, 3.2, 3.4, 3.6; risk consideration (iii)); Section 4 items 1.1(e)(i)(1), 1.3, 1.3(b) | https://content.naic.org/sites/default/files/cmte-h-big-data-artificial-intelligence-wg-ai-model-bulletin.pdf.pdf |
| Colorado 3 CCR 702-10, Regulation 10-1-1, amended effective Oct 15, 2025 | Sec. 3 applicability; Sec. 4.D ECDIS definition; Sec. 5.A.6, 5.A.9, 5.C | https://sos.state.co.us/CCR/GenerateRulePdf.do?fileName=3+CCR+702-10&ruleVersionId=12182 |
| Verisk State of Insurance Fraud study | Step 6 card C context stat | https://www.verisk.com/49411b/siteassets/media/campaigns/gated/claims/verisk-state-of-insurance-fraud-study.pdf |
| Milliman, Accidents that never happened (Dec 2025) | Step 6 card C context stat | https://media.milliman.com/v1/media/edge/images/millimaninc5660-milliman6442-prod27d5-0001/media/Milliman/PDFs/2025-Articles/12-3-25_Accidents-that-never-happened.pdf |
| Unicode Technical Standard #39, Unicode Security Mechanisms (confusables) | Step 7 look-alike name check; the method, not a statistic | https://www.unicode.org/reports/tr39/ |
| NAIC adoption map (status as of Oct 8, 2026) | Background only, not shown in the demo | https://content.naic.org/sites/default/files/legal-adoption-map-ai-model-bulletin.pdf |

## Public statistics
Only two public statistics appear, both in step 6 card C, each with its source link on screen:
| Stat | Source | URL |
|---|---|---|
| 99% of insurers surveyed had encountered manipulated or AI-altered documentation | Verisk, State of Insurance Fraud study | https://www.verisk.com/49411b/siteassets/media/campaigns/gated/claims/verisk-state-of-insurance-fraud-study.pdf |
| People spotted AI-generated car damage images at roughly chance, about 50% | Milliman, "Accidents that never happened: Generative AI and fraud in motor insurance," Dec 2025 | https://media.milliman.com/v1/media/edge/images/millimaninc5660-milliman6442-prod27d5-0001/media/Milliman/PDFs/2025-Articles/12-3-25_Accidents-that-never-happened.pdf |

Every other number on screen is synthetic. If you add a stat in your own version, put its source next to it on screen.

## v1.3 curveballs
All 27 curveball records are synthetic, including the dollar impacts (for example a $2,560 depreciation shortfall, an $8M vs $1M hours-clause recovery, a $36,000 copy-paste total gap, a 0.86 name-match score, a 92% annuity concentration). The person and company names on the sanctions-style card are fictional. Nothing is matched against a real list.

The context links on each card are real public sources about the friction:

| ID | Curveball | Category | Public friction context |
|---|---|---|---|
| HW | Handwritten amount misread | Claims | [J.D. Power 2025 property claims study](https://www.jdpower.com/business/press-releases/2025-us-property-claims-satisfaction-study) |
| TZ | Time zone date shift | Claims | [NAIC complaint reasons](https://eapps.naic.org/documents/cis_aggregate_complaints_by_reason_codes.pdf) |
| CC | Claim acknowledgment clock | Claims | [NAIC complaint reasons](https://eapps.naic.org/documents/cis_aggregate_complaints_by_reason_codes.pdf) |
| DP | Depreciation math | Claims | [r/adjusters thread on ACV vs RCV](https://www.reddit.com/r/adjusters/comments/1g3vwy3/home_insurance_estimate_replacement_cost_value/) |
| MT | Matching siding | Claims | [IRMI on matching](https://www.irmi.com/articles/expert-commentary/matching-problem-in-property-insurance-claims) |
| RD | Rounding drift | Payments and Billing | [NAIC complaint reasons](https://eapps.naic.org/documents/cis_aggregate_complaints_by_reason_codes.pdf) |
| SB | Deductible owed after subrogation | Payments and Billing | [MWL on deductible reimbursement](https://www.mwl-law.com/under-deductible-subrogation-deductible-reimbursement-helping-insureds-battle-the-cost-of-insurance/) |
| PP | Late payment after settlement | Payments and Billing | [NAIC complaint reasons](https://eapps.naic.org/documents/cis_aggregate_complaints_by_reason_codes.pdf) |
| PB | Premium increase or double billing | Payments and Billing | [NAIC complaint reasons](https://eapps.naic.org/documents/cis_aggregate_complaints_by_reason_codes.pdf) |
| SC | Stale compliance doc | Underwriting and Policy | [Illinois 2025 complaint ratio report](https://idoi.illinois.gov/content/dam/soi/en/web/insurance/reports/reports/2025-complaint-ratio-report.pdf) |
| PL | Prompt-like text in a note | Underwriting and Policy | [Illinois 2025 complaint ratio report](https://idoi.illinois.gov/content/dam/soi/en/web/insurance/reports/reports/2025-complaint-ratio-report.pdf) |
| PI | Policy identifier mismatch | Underwriting and Policy | [Washington OIC premium increase transparency](https://www.insurance.wa.gov/about-us/current-initiatives/premium-increase-transparency/insurers-need-explain-premium-increases) |
| AU | Auth on file, denied anyway | Health/Auth | [KFF prior authorization metrics](https://www.kff.org/patient-consumer-protections/prior-authorization-metrics-provide-new-insights-into-insurer-practices-but-gaps-remain/) |
| LC | Life contestability with name/DOB mismatch | Life | [WSJ on the contestability period](https://www.wsj.com/buyside/personal-finance/life-insurance/life-insurance-contestability-period?eafs_enabled=) |
| AN | Annuity suitability | Life | [Connecticut 2025 complaint activity report](https://portal.ct.gov/cid/-/media/cid/reports/complaint-rankings/2025-annual-complaints-activity-reports.pdf?hash=00FA51C9A4900C29B31216DB994C962B&rev=d57e43b0742049acb73937483525f24b) |
| WC | Workers' comp date-of-injury mismatch | Workers' Comp | [Minnesota DLI 2026 workers' comp report](https://dli.mn.gov/sites/default/files/pdf/wcfact26.pdf) |
| UN | Unit mix-up | Reinsurance | [Lloyd's Coverholder Reporting Standards v5.1](https://assets.lloyds.com/media/8b074f5e-61c8-4e14-876e-ad8cd1264614/Y5199---Lloyd%E2%80%99s-Coverholder-Reporting-Standards-Version-5.1.pdf) |
| TN | Treaty notice missed | Reinsurance | [Fifth Circuit 2025 late-notice opinion](https://www.ca5.uscourts.gov/opinions/pub/24/24-10392-CV0.pdf) |
| WH | Wildfire hours clause | Reinsurance | [Artemis on wildfire hours clauses](https://www.artemis.bm/news/hours-clause-questions-raised-over-california-wildfire-reinsurance-claims/) |
| BX | Late MGA bordereaux | Reinsurance | [Lloyd's Coverholder Reporting Standards v5.1](https://assets.lloyds.com/media/8b074f5e-61c8-4e14-876e-ad8cd1264614/Y5199---Lloyd%E2%80%99s-Coverholder-Reporting-Standards-Version-5.1.pdf) |
| HG | Homoglyph duplicate | Fraud and Identity | [Unicode TR39 confusables](https://www.unicode.org/reports/tr39/) |
| PH | AI photo provenance (route to SIU, never call it fraud) | Fraud and Identity | [Verisk State of Insurance Fraud study](https://www.verisk.com/49411b/siteassets/media/campaigns/gated/claims/verisk-state-of-insurance-fraud-study.pdf) |
| OF | Sanctions-style near-match (fictional names) | Fraud and Identity | [U.S. Treasury OFAC SDN list (what real screening uses)](https://ofac.treasury.gov/specially-designated-nationals-and-blocked-persons-list-sdn-human-readable-lists) |
| WT | Hidden white text in a PDF | Fraud and Identity | [Verisk State of Insurance Fraud study](https://www.verisk.com/49411b/siteassets/media/campaigns/gated/claims/verisk-state-of-insurance-fraud-study.pdf) |
| DT | Data type mismatch | Data Quirks | [Lloyd's Coverholder Reporting Standards v5.1](https://assets.lloyds.com/media/8b074f5e-61c8-4e14-876e-ad8cd1264614/Y5199---Lloyd%E2%80%99s-Coverholder-Reporting-Standards-Version-5.1.pdf) |
| DS | Duplicate submission | Data Quirks | [NAIC complaint reasons](https://eapps.naic.org/documents/cis_aggregate_complaints_by_reason_codes.pdf) |
| CP | Copy-paste totals | Data Quirks | [Lloyd's Coverholder Reporting Standards v5.1](https://assets.lloyds.com/media/8b074f5e-61c8-4e14-876e-ad8cd1264614/Y5199---Lloyd%E2%80%99s-Coverholder-Reporting-Standards-Version-5.1.pdf) |
