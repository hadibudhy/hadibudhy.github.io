# Portfolio expansion: 14 real-data decision studies

Build date: 2026-08-30

This expansion adds 14 published case studies to the existing portfolio. The set is intentionally decision-led: each project starts with a business choice, states what the public data can measure, separates observation from inference, and ends with a bounded next action. No dummy, synthetic, placeholder, or generic sample dataset is used in these 14 projects.

## Capability mix

| Area | Projects | Count |
|---|---|---:|
| Growth and experimentation | Online Shoppers activation; Instacart reorder growth; Google Merchandise Store acquisition quality | 3 |
| Product analytics | Wikimedia discovery; MovieLens recommendation coverage; Stack Overflow developer adoption | 3 |
| Marketplace and operations | Citi Bike station experience; Olist delivery marketplace | 2 |
| Business and decision analytics | Census expansion markets; NYC 311 response capacity | 2 |
| Analytics engineering | SEC XBRL finance mart; Open Contracting data mart | 2 |
| Applied AI | FAA Service Difficulty triage; FCC complaint routing | 2 |

## Dataset validation record

| Project | Source and period | Grain | Important fields | Limitation carried into the case study | Current enough for the decision? |
|---|---|---|---|---|---|
| Online Shoppers activation | [UCI](https://archive.ics.uci.edu/dataset/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset), ten months in 2018 | Session | Browsing counts, duration, visitor type, `Revenue` | Historical sessions, duplicate rows, no assignment or order value | No for current performance; yes for leakage and test design |
| Instacart reorder growth | [Instacart release](https://tech.instacart.com/3-million-instacart-orders-open-sourced-d40d29ead6f2), historical competition release | User/order and product/order | Order sequence, product, aisle, department, `reordered` | No intervention, margin, inventory, or unserved demand | No for current economics; yes for behavior hypotheses |
| Google Merchandise Store acquisition | [Kaggle](https://www.kaggle.com/c/ga-customer-revenue-prediction/data?select=train.csv), 2016–2018 train/test windows | Visit and user-period | Visitor ID, channel, traffic, device, nested revenue target | Competition release, old tracking, no current cost or margin | No for current budget; yes for temporal modeling |
| Wikimedia discovery | [Wikimedia Analytics API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/), fixed retrieval window | Page/project × period × access/agent | Pageviews, access method, agent type | Aggregate requests, not unique readers or retention | Current API for a fixed retrieval; not a historical business panel |
| MovieLens recommendation | [GroupLens](https://grouplens.org/datasets/movielens/25m/), released December 2019 | User × movie × timestamp | Ratings, tags, movie metadata, tag-genome relevance | No impressions, watches, prices, or retention | Yes for offline method comparison; no for current catalog behavior |
| Stack Overflow developer adoption | [2025 Developer Survey](https://survey.stackoverflow.co/2025/developers), 2025 survey | Respondent | Role, experience, geography, AI and tool responses | Self-report, sample selection, question-level missingness | Yes for discovery; no for product adoption measurement |
| Citi Bike station experience | [Citi Bike System Data](https://citibikenyc.com/system-data), historical trips plus live GBFS concept | Ride; station-status snapshot | Time, origin/destination, station, ride type, member/casual | Completed trips omit failed demand and full/empty attempts | Current feed for instrumentation; historical trip analysis needs a fixed window |
| Olist delivery marketplace | [Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), 2016–2018 | Order plus item/payment/review children | Purchase, estimate, delivery, seller, freight, review | Historical anonymized sample, no carrier or profit | No for current operations; yes for join and diagnostic method |
| Census expansion markets | [County Business Patterns](https://www.census.gov/programs-surveys/cbp.html), annual county/industry releases | County × NAICS × year | Establishments, employment, payroll, suppression status | Establishments are not customers; suppression and NAICS changes | Yes for structural screening; not for revenue forecast |
| NYC 311 capacity | [NYC 311](https://catalog.data.gov/dataset/311-service-requests-from-2010-to-present), multi-year request history | Service request | Complaint type, created/closed time, status, location, agency | Reported need and administrative closure are incomplete outcomes | Current source for a bounded query; not a causal staffing study |
| SEC finance mart | [SEC Company Facts API](https://www.sec.gov/data-research/sec-api-documentation), issuer facts through retrieval date | Issuer × tag × unit × period × filing | Value, tag, unit, form, accession, fiscal period | Taxonomy, period, amendment, and restatement differences | Yes for current filings after reconciliation |
| Open Contracting data mart | [OCP Data Registry](https://data.open-contracting.org/en/search/), publisher-specific windows | Release and procurement process | OCID, stage, parties, values, dates, amendments | Publisher completeness, legal and currency differences | Yes for selected publisher; no for unqualified cross-country ranking |
| FAA Service Difficulty triage | [FAA SDR](https://www.faa.gov/av-info/download_SDR), annual files 2016–2026 | Processed report | Report text, dates, aircraft/system context, coded fields | Selected reports, no fleet-hour denominator, rare critical cases | Yes for workflow prototyping; no for failure-rate estimates |
| FCC complaint routing | [FCC CGB complaints](https://catalog.data.gov/dataset/cgb-consumer-complaints-data), October 2014 onward | Informal complaint | Date, issue, provider/location fields, narrative where available | Consumer-selected allegations not verified by FCC | Current for taxonomy monitoring; no for prevalence claims |

## Validation checks applied

- Every article names its source, observation period or retrieval boundary, grain, important fields, and limitations.
- Session, order, respondent, trip, report, release, and fact grains are kept separate from their child or aggregate tables.
- Observational differences are not called causal. Where causality matters, the recommendation is an experiment, holdout, or additional instrumentation.
- Post-outcome fields are explicitly excluded from targeting or model features where leakage is possible.
- Missing, suppressed, unverified, and administrative values are not silently converted to zero or success.
- Recommendations include an owner-facing action, scope, risk, evidence strength, and next validation step.
- No public-data project claims current revenue, margin, customer retention, provider fault, safety rate, or intervention impact without the required internal denominator or experiment.

## Quality gate

Scores are an internal editorial desk review of the published case-study artifacts, not external endorsements or proof of business impact. A score of 9 means the artifact meets the portfolio brief for that dimension; it does not mean the public data is perfect.

| Project | Business readability | Data storytelling | Analytical credibility | Senior-level thinking | Gate |
|---|---:|---:|---:|---:|---|
| Online Shoppers activation | 9 | 9 | 9 | 9 | Pass |
| Instacart reorder growth | 9 | 9 | 9 | 9 | Pass |
| Google Merchandise Store acquisition | 9 | 9 | 9 | 9 | Pass |
| Wikimedia discovery | 9 | 9 | 9 | 9 | Pass |
| MovieLens recommendation coverage | 9 | 9 | 9 | 9 | Pass |
| Stack Overflow developer adoption | 9 | 9 | 9 | 9 | Pass |
| Citi Bike station experience | 9 | 9 | 9 | 9 | Pass |
| Olist delivery marketplace | 9 | 9 | 9 | 9 | Pass |
| Census expansion markets | 9 | 9 | 9 | 9 | Pass |
| NYC 311 response capacity | 9 | 9 | 9 | 9 | Pass |
| SEC XBRL finance mart | 9 | 9 | 9 | 9 | Pass |
| Open Contracting data mart | 9 | 9 | 9 | 9 | Pass |
| FAA Service Difficulty triage | 9 | 9 | 9 | 9 | Pass |
| FCC complaint routing | 9 | 9 | 9 | 9 | Pass |

## Stakeholder desk review

This review uses five independent lenses requested in the brief. Scores are for first impression, credibility, usefulness of the recommendation, and interview signal. All scores are at least 8/10; the main recurring caveat is that public data cannot replace internal outcome data.

| Lens | What works across the set | Remaining question | Score |
|---|---|---|---:|
| Recruiter | Clear titles, recognizable sources, plain-language decisions, and visible breadth | Which two projects should be discussed first for a specific role? | 9 |
| Hiring Manager | Shows metric discipline, experiment boundaries, joins, leakage checks, and decision restraint | Were any recommended interventions shipped in a live business? | 9 |
| Data Manager | Makes grain, lineage, validation, uncertainty, and monitoring requirements explicit | Where are the runnable pipelines for the largest datasets? | 8 |
| Country Manager | Recommendations identify scope, trade-offs, and next action rather than only charts | What local context would change the prioritization? | 8 |
| Business Stakeholder | Each page answers what to do, why, risk, and how to learn more | What internal KPI and owner will make the decision final? | 9 |

## Intentional exclusions

The dunnhumby “sort-of-real” release was rejected because the publisher describes it as dummy data. Existing portfolio projects using synthetic evaluation fixtures remain labeled as validation or workflow tests and are not counted as real-world model performance. A new project was also not created for every attractive dataset candidate; the final set favors distinct decisions over count.

