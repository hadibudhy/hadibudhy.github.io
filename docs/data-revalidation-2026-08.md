# Public data revalidation: 20 August 2026

This note records the public-source re-download and structural inspection completed before reworking the portfolio analyses. Raw files are kept locally under `analysis_data/` and excluded from Git so the public repository does not publish third-party datasets or personal-level records. The local inventory includes SHA-256 hashes and the profiling output includes columns, types, missingness, and duplicate checks.

## Validated sources

| Portfolio project | Source inspected | Observed file | Structural result | Important caveat |
|---|---|---|---|---|
| Online Retail customer growth | [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online%2Bretail) | `Online Retail.xlsx` | 541,909 rows, 8 columns, 5,268 duplicate rows, 135,080 missing `CustomerID` values | The unit is a transaction line. Cancellations, non-positive quantities/prices, duplicates, and incomplete December 2011 require explicit treatment. |
| Clickstream product funnel | [UCI Clickstream Data for Online Shopping](https://archive.ics.uci.edu/dataset/553/clickstream%2Bdata%2Bfor%2Bonline%2Bshopping) | `e-shop clothing 2008.csv` | 165,474 events, 14 columns, no missing values in the downloaded table | The unit is an event, not a customer or confirmed order. The five-month window is historical and has no revenue or experiment assignment. |
| Bank marketing efficiency | [UCI Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank%5C%5C%2Bmarketing) | `bank-full.csv`, `bank.csv`, plus `bank-additional` files | 45,211-row and 4,521-row bank files; separate 41,188-row and 4,119-row additional files; semicolon-delimited | These are related but different campaign tables. They must not be silently combined. Contact duration is post-contact information and would leak into a pre-call targeting model. |
| NYC taxi operations | [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) | January 2025 yellow taxi Parquet plus official zone lookup | 3,475,226 trips, 20 columns; 265 zone rows | Five trip fields are missing for 540,149 records. TLC submissions may contain incomplete or inaccurate records. One month cannot establish a full-year operating pattern. |
| NYC restaurant quality | [NYC Restaurant Inspection Results](https://data.cityofnewyork.us/d/43nn-pn8j) | Current public CSV | 295,473 rows, 27 columns; substantial missing grade and location fields | One inspection can span multiple violation rows. The source warns that administrative records can contain data-entry or transfer errors. |
| World Happiness analysis | [World Happiness Report Figure 2.1 data](https://www.worldhappiness.report/data-sharing/) | `WHR26_Data_Figure_2.1.xlsx` | 2,116 country-year rows, 13 columns, no duplicate rows; factor and confidence-band fields are missing for roughly half the rows | This is the 2026 release and should not be mixed with the older 2025 release used for prior charts. The values are country-level associations, not causal estimates. |
| Airfare pricing context | [Bureau of Transportation Statistics fare series](https://www.bts.gov/content/national-level-domestic-average-fare-series) | Public BTS series referenced by the case | Public benchmark source located; raw series still needs a machine-readable extract before numeric claims are reissued | National average fare cannot identify route elasticity, margin, fare mix, or customer willingness to pay. |
| SEC company performance | [SEC Company Facts API](https://www.sec.gov/data-research/sec-api-documentation) | Microsoft CIK 0000789019 JSON | JSON downloaded and parsed; top-level entity and XBRL facts are present | XBRL facts can contain amended filings, restatements, different fiscal periods, and multiple taxonomy tags. Annual values need period/form/tag reconciliation. |
| Airbnb marketplace health | [Inside Airbnb data](https://insideairbnb.com/get-the-data/) | NYC listing snapshot dated 14 June 2026 | 30,555 listings, 19 columns; 8,758 missing prices, 8,616 missing review fields, 25,269 missing licenses | Listings are supply-side observations, not bookings. Occupancy, revenue, and causal marketplace effects cannot be inferred directly. |
| Workforce planning | [BLS JOLTS](https://www.bls.gov/jlt/) | 2025 BLS API response for openings, hires, quits, and total separations | JSON response downloaded and parsed for the four national series | It is not employee-level data and cannot identify a company, manager, team, or role causing turnover. |
| Credit default risk | [UCI Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default%2Bof%2Bcredit%2Bcard%2Bclients) | `default of credit card clients.xls` | 30,000 rows, 25 columns including the ID and observed default target; no missing or duplicate rows | Historical Taiwan credit data from 2005. Category codes and fairness/generalization need validation before any policy claim. |
| ComplaintFlow AI triage | [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) plus checked-in evaluation fixture | Local project fixture, not a copied public complaint dump | The repository contains a 20-case synthetic labeled fixture and evaluation code | The fixture validates the software contract, not real-world model performance. CFPB complaints are not a representative sample of all consumer experiences. |

## Sources not reproducible from the current repository

| Project | What was found | Status | Required next step |
|---|---|---|---|
| Customer value / MDS | The project links to a GitHub code repository but declares no public raw-data source, file name, row count, or license. | **Blocked** | Obtain the original sanitized input or rewrite the case as a pipeline-design project without claiming data findings. |
| Netflix content strategy | The legacy analysis identifies the Shivam Bhandari Kaggle Netflix titles dataset, but an anonymous Kaggle API download was not available during this pass. | **Blocked pending source access** | Re-download through an authorized Kaggle session or provide the exact archived CSV and version. Do not use a mirror without provenance checks. |
| Fake job detection | The case identifies the Employment Scam Aegean Dataset and the public Kaggle listing, but an anonymous Kaggle API download was not available during this pass. | **Blocked pending source access** | Re-download through an authorized Kaggle session or provide the exact 17,880-row source/version. The existing model metrics must remain draft evidence until reproduced. |

## What this changes before reanalysis

1. Public-data projects with a validated local source can now be re-run from the actual files rather than from chart captions.
2. The World Happiness analysis must use one release consistently. The newly downloaded 2026 workbook is not interchangeable with the prior 2025 narrative.
3. Bank Marketing requires separate treatment of the four supplied tables and strict leakage controls around call duration.
4. Retail, restaurant, taxi, Airbnb, and credit-risk analysis must carry the observed missingness and duplicate checks into the published methodology.
5. SEC, BTS, and JOLTS are context or reporting datasets, not substitutes for company-level operational, route-level pricing, or employee-level causal data.
6. Netflix, fake-job, and MDS conclusions should not be strengthened until the underlying inputs are reproducible.

## Local artifacts

- `analysis_data/inventory.json`: source URLs, file sizes, SHA-256 hashes, and download-level inspection.
- `analysis_data/profiles.json`: table structures, row counts, data types, missingness, and duplicate checks.
- `scripts/download_inspect_sources.py`: repeatable public-source download step.
- `scripts/profile_downloaded_sources.py`: repeatable table profiling step, including nested archives and semicolon-delimited UCI files.

This is a validation report, not a claim that every existing project is ready for publication. The next step is to reproduce each numeric finding from the validated source, test the assumptions, and remove unsupported claims.
