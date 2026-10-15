# Curveball checklist: 27 things that fool a QC check and a careful reviewer

Every card in step 7 shows the naive result, what the guardrail caught, the impact (labeled as an estimate), a reason code, the named reviewer, and a spot-check button. All data on the cards is synthetic. The context links are real public sources describing the friction, not sources for the synthetic numbers.

Presenter picks: HW, DP, AU, TZ.

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

## Use it on your own pipeline
For each row, ask: would our check hold this, who reviews it, and does the hold land in a log someone can replay?
